#!/usr/bin/env python3
"""Structural validation of the skill.

Usage: python3 scripts/validate.py [skill-root]

Requires PyYAML (pip install -r requirements-dev.txt). Checks the frontmatter
and agents/openai.yaml with a YAML parser (duplicate keys are an error),
description limits, local links, evals (structure and types), fixtures,
symlinks, and line endings. It does not follow symlinks: any symlink is an
error and its destination is not read. It does not measure the quality of the
skill's decisions: that requires real execution (see evals/RESULTS.md).
Exit code: 0 with no errors (warnings allowed); 1 with at least one error;
2 if the validator cannot run (PyYAML missing or invalid root).
"""
import json
import os
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # handled in main()
    yaml = None

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
NAME_MAX = 64
DESC_WARN = 1024  # portable specification limit (not verified in this version)
DESC_ERROR = 1536  # Claude Code listing limit
FM_RE = re.compile(r"---\r?\n(.*?)\r?\n---\r?\n", re.S)
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
PATH_RE = re.compile(r"`((?:scripts|references|evals|agents)/[^`\s<>*]+)`")
SKIP_DIRS = {".git", "__pycache__"}
TEXT_EXTS = {".md", ".json", ".yaml", ".yml", ".py", ".txt"}

EVAL_TEXT_KEYS = ("category", "type", "objective", "prompt", "expected_output", "severity_if_failed")
EVAL_LIST_KEYS = ("files", "expectations", "forbidden", "allowed_changes")
EVAL_TYPES = {"activation", "execution", "security", "regression"}
EVAL_SEVERITIES = {"critical", "high", "medium"}
OPENAI_REQUIRED = ("display_name", "short_description", "default_prompt")

errors, warnings = [], []
_FAILED = object()
_LOADER = None


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def rel(root, path):
    return path.relative_to(root).as_posix()


def is_within(path, base):
    try:
        path.resolve().relative_to(base.resolve())
        return True
    except (OSError, ValueError, RuntimeError):
        return False


def is_text(v):
    return isinstance(v, str) and bool(v.strip())


def is_text_list(v):
    return isinstance(v, list) and all(is_text(x) for x in v)


def make_loader():
    """Safe loader that treats a duplicate key as an error (safe_load keeps the last one)."""

    class UniqueKeyLoader(yaml.SafeLoader):
        pass

    def construct_mapping(loader, node, deep=False):
        loader.flatten_mapping(node)
        seen = set()
        for key_node, _ in node.value:
            key = loader.construct_object(key_node, deep=deep)
            try:
                duplicate = key in seen
                seen.add(key)
            except TypeError:
                continue  # unhashable key: the base constructor reports it
            if duplicate:
                raise yaml.constructor.ConstructorError(
                    None, None, f"duplicate key: {key!r}", key_node.start_mark
                )
        return yaml.SafeLoader.construct_mapping(loader, node, deep)

    UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping)
    return UniqueKeyLoader


def load_yaml(text, label):
    try:
        return yaml.load(text, Loader=_LOADER)  # Loader derived from SafeLoader
    except yaml.YAMLError as e:
        mark = getattr(e, "problem_mark", None)
        where = f" (line {mark.line + 1})" if mark else ""
        lines = str(e).strip().splitlines()
        err(f"{label}: invalid YAML{where}: {lines[0] if lines else type(e).__name__}")
        return _FAILED


def scan(root):
    """List regular files without following symlinks; symlinks become errors and are not read."""
    files = []
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        base = Path(dirpath)
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for d in list(dirnames):
            if (base / d).is_symlink():
                err(f"{rel(root, base / d)}: directory symlink not allowed; destination not read")
                dirnames.remove(d)
        for f in sorted(filenames):
            p = base / f
            if p.is_symlink():
                err(f"{rel(root, p)}: symlink not allowed; destination not read")
            else:
                files.append(p)
    return files


def read_text(root, path):
    """Read only a regular file inside the root; failures become messages."""
    if path.is_symlink() or not is_within(path, root):
        err(f"{rel(root, path) if is_within(path, root) else path.name}: outside the root or a symlink; not read")
        return None
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        err(f"{rel(root, path)}: could not read as UTF-8 ({type(e).__name__})")
        return None


def check_skill(root):
    skill = root / "SKILL.md"
    if not skill.exists() and not skill.is_symlink():
        err("SKILL.md not found")
        return None
    text = read_text(root, skill)
    if text is None:
        return None
    m = FM_RE.match(text)
    if not m:
        err("SKILL.md: frontmatter missing or malformed")
        return None
    fm = load_yaml(m.group(1), "SKILL.md (frontmatter)")
    if fm is _FAILED:
        return None
    if not isinstance(fm, dict):
        err("SKILL.md: frontmatter must be a YAML mapping with 'name' and 'description'")
        return None
    name, desc = fm.get("name"), fm.get("description")
    if not is_text(name):
        err(f"SKILL.md: 'name' missing or not text (type: {type(name).__name__})")
        name = None
    elif not NAME_RE.match(name) or len(name) > NAME_MAX:
        err(f"SKILL.md: invalid 'name' ({name!r}); use lowercase letters, digits, and hyphens, up to {NAME_MAX}")
    elif name != root.name:
        warn(f"skill name ({name}) differs from the folder ({root.name}); confirm the host requirement")
    if not is_text(desc):
        err(f"SKILL.md: 'description' missing or not text (type: {type(desc).__name__})")
    elif len(desc) > DESC_ERROR:
        err(f"SKILL.md: description has {len(desc)} characters (> {DESC_ERROR})")
    elif len(desc) > DESC_WARN:
        warn(f"SKILL.md: description has {len(desc)} characters (> {DESC_WARN} of the portable specification)")
    return name if is_text(name) and NAME_RE.match(name) else None


def markdown_files(root, files):
    for f in files:
        r = f.relative_to(root).parts
        if f.suffix == ".md" and r[:2] != ("evals", "files"):
            yield f


def check_links(root, files):
    for md in markdown_files(root, files):
        text = read_text(root, md)
        if text is None:
            continue
        for target in LINK_RE.findall(text):
            if re.match(r"^(https?:|mailto:|#)", target):
                continue
            path = target.split("#", 1)[0]
            if not path:
                continue
            dest = md.parent / path
            if not is_within(dest, root):
                err(f"{rel(root, md)}: link points outside the project -> {target}")
            elif not dest.exists():
                err(f"{rel(root, md)}: broken link -> {target}")


def check_backtick_paths(root, files):
    """Paths in backticks in Markdown (outside fixtures) must exist inside the project."""
    for md in markdown_files(root, files):
        text = read_text(root, md)
        if text is None:
            continue
        for target in PATH_RE.findall(text):
            dest = root / target.rstrip(".,;:)")
            if not is_within(dest, root):
                err(f"{rel(root, md)}: cited path points outside the project -> {target}")
            elif not dest.exists():
                err(f"{rel(root, md)}: cited path does not exist -> {target}")


def check_fixture(root, label, fixture, referenced):
    if not is_text(fixture):
        return
    p = Path(fixture)
    if p.is_absolute() or ".." in p.parts:
        err(f"{label}: fixture must be a relative path without '..' -> {fixture}")
        return
    full = root / p
    if not is_within(full, root / "evals" / "files"):
        err(f"{label}: fixture outside evals/files -> {fixture}")
        return
    if full.is_symlink():
        err(f"{label}: fixture is a symlink; not allowed -> {fixture}")
        return
    if not full.is_file():
        err(f"{label}: fixture does not exist -> {fixture}")
        return
    referenced.add(p.as_posix())


def check_one_eval(root, ev, index, ids, referenced):
    label = f"evals[{index}]"
    if not isinstance(ev, dict):
        err(f"{label}: each scenario must be an object (type: {type(ev).__name__})")
        return
    eid = ev.get("id")
    if isinstance(eid, int) and not isinstance(eid, bool):
        label = f"eval {eid}"
        if eid in ids:
            err(f"{label}: duplicate id")
        ids.add(eid)
    else:
        err(f"{label}: 'id' must be an integer (type: {type(eid).__name__})")
    for k in EVAL_TEXT_KEYS + EVAL_LIST_KEYS:
        if k not in ev:
            err(f"{label}: missing field -> {k}")
    for k in EVAL_TEXT_KEYS:
        if k in ev and not is_text(ev[k]):
            err(f"{label}: '{k}' must be non-empty text")
    for k in EVAL_LIST_KEYS:
        if k in ev and not is_text_list(ev[k]):
            err(f"{label}: '{k}' must be a list of non-empty strings")
    etype, sev = ev.get("type"), ev.get("severity_if_failed")
    if is_text(etype) and etype not in EVAL_TYPES:
        err(f"{label}: 'type' must be one of {sorted(EVAL_TYPES)}")
    if is_text(sev) and sev not in EVAL_SEVERITIES:
        err(f"{label}: 'severity_if_failed' must be one of {sorted(EVAL_SEVERITIES)}")
    if is_text_list(ev.get("expectations")) and not ev["expectations"]:
        err(f"{label}: 'expectations' must have at least one assertion")
    if etype in {"security", "activation"} and is_text_list(ev.get("forbidden")) and not ev["forbidden"]:
        err(f"{label}: {etype} cases require a non-empty 'forbidden'")
    files = ev.get("files")
    if is_text_list(files) and not files and not is_text(ev.get("no_fixture_reason")):
        err(f"{label}: no fixtures and no 'no_fixture_reason'")
    if etype == "security":
        if not (is_text_list(ev.get("inspect")) and ev.get("inspect")):
            err(f"{label}: security case requires 'inspect' (non-empty list)")
        if not is_text(ev.get("safe_action")):
            err(f"{label}: security case requires 'safe_action'")
    if isinstance(files, list):
        for fixture in files:
            check_fixture(root, label, fixture, referenced)


def check_evals(root, name, files):
    path = root / "evals" / "evals.json"
    if not path.exists() and not path.is_symlink():
        err("evals/evals.json not found")
        return
    text = read_text(root, path)
    if text is None:
        return
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        err(f"evals/evals.json: invalid JSON ({e})")
        return
    if not isinstance(data, dict):
        err(f"evals/evals.json: the root must be an object (type: {type(data).__name__})")
        return
    if name and data.get("skill_name") != name:
        err(f"evals/evals.json: skill_name ({data.get('skill_name')!r}) differs from the SKILL.md name ({name!r})")
    evals = data.get("evals")
    if not isinstance(evals, list) or not evals:
        err("evals/evals.json: 'evals' must be a non-empty list")
        return
    ids, referenced = set(), set()
    for i, ev in enumerate(evals):
        check_one_eval(root, ev, i, ids, referenced)
    for f in files:
        r = rel(root, f)
        if not r.startswith("evals/files/"):
            continue
        if f.name == "SKILL.md":
            err(f"{r}: a fixture named SKILL.md may be discovered as an installed skill")
        if r not in referenced:
            warn(f"{r}: fixture not referenced by any eval")


def check_openai_yaml(root, name):
    path = root / "agents" / "openai.yaml"
    if not path.exists() and not path.is_symlink():
        return
    text = read_text(root, path)
    if text is None:
        return
    data = load_yaml(text, "agents/openai.yaml")
    if data is _FAILED:
        return
    if not isinstance(data, dict):
        err("agents/openai.yaml: the root must be a YAML mapping with 'interface'")
        return
    iface = data.get("interface")
    if not isinstance(iface, dict):
        err("agents/openai.yaml: 'interface' missing or not a mapping")
        return
    for key in OPENAI_REQUIRED:
        if not is_text(iface.get(key)):
            err(f"agents/openai.yaml: interface.{key} missing or not text")
    prompt = iface.get("default_prompt")
    if is_text(prompt) and name and f"${name}" not in prompt:
        err(f"agents/openai.yaml: default_prompt does not cite ${name}")


def check_line_endings(root, files):
    for f in files:
        if f.suffix in TEXT_EXTS:
            try:
                has_crlf = b"\r\n" in f.read_bytes()
            except OSError as e:
                err(f"{rel(root, f)}: could not read ({type(e).__name__})")
                continue
            if has_crlf:
                warn(f"{rel(root, f)}: contains CRLF (the repository uses LF; see .gitattributes)")


def guarded(fn, *args):
    """An unexpected failure becomes a readable error, never a traceback."""
    try:
        return fn(*args)
    except Exception as e:  # noqa: BLE001
        err(f"unexpected failure in {fn.__name__}: {type(e).__name__}: {e}")
        return None


def main():
    global _LOADER
    if yaml is None:
        print("ERROR: PyYAML is not installed. Run: pip install -r requirements-dev.txt")
        sys.exit(2)
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    if not root.is_dir():
        print(f"ERROR: root does not exist or is not a directory: {root}")
        sys.exit(2)
    _LOADER = make_loader()
    files = guarded(scan, root) or []
    name = guarded(check_skill, root)
    guarded(check_links, root, files)
    guarded(check_backtick_paths, root, files)
    guarded(check_evals, root, name, files)
    guarded(check_openai_yaml, root, name)
    guarded(check_line_endings, root, files)
    for w in warnings:
        print(f"WARNING: {w}")
    for e in errors:
        print(f"ERROR:   {e}")
    print(f"\n{len(errors)} error(s), {len(warnings)} warning(s)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
