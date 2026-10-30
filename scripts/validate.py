#!/usr/bin/env python3
"""Validação estrutural da skill.

Uso: python3 scripts/validate.py [raiz-da-skill]

Requer PyYAML (pip install -r requirements-dev.txt). Verifica frontmatter e
agents/openai.yaml com parser YAML (chaves duplicadas são erro), limites da
descrição, links locais, evals (estrutura e tipos), fixtures, symlinks e fim de
linha. Não segue symlinks: qualquer symlink é erro e o destino não é lido.
Não mede qualidade das decisões da skill: isso exige execução real (ver
evals/RESULTS.md).
Saída: 0 sem erros (avisos permitidos); 1 com ao menos um erro; 2 se o
validador não puder rodar (PyYAML ausente ou raiz inválida).
"""
import json
import os
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # tratado em main()
    yaml = None

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
NAME_MAX = 64
DESC_WARN = 1024  # limite da especificação portátil (não verificado nesta versão)
DESC_ERROR = 1536  # limite de listagem do Claude Code
FM_RE = re.compile(r"---\r?\n(.*?)\r?\n---\r?\n", re.S)
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
PATH_RE = re.compile(r"`((?:scripts|references|evals|agents)/[^`\s<>*]+)`")
SKIP_DIRS = {".git", "__pycache__"}
TEXT_EXTS = {".md", ".json", ".yaml", ".yml", ".py", ".txt"}

EVAL_TEXT_KEYS = ("category", "type", "objective", "prompt", "expected_output", "severity_if_failed")
EVAL_LIST_KEYS = ("files", "expectations", "forbidden", "allowed_changes")
EVAL_TYPES = {"ativação", "execução", "segurança", "regressão"}
EVAL_SEVERITIES = {"crítica", "alta", "média"}
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
    """Loader seguro que trata chave duplicada como erro (safe_load usa a última)."""

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
                continue  # chave não hashable: o construtor base reporta
            if duplicate:
                raise yaml.constructor.ConstructorError(
                    None, None, f"chave duplicada: {key!r}", key_node.start_mark
                )
        return yaml.SafeLoader.construct_mapping(loader, node, deep)

    UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping)
    return UniqueKeyLoader


def load_yaml(text, label):
    try:
        return yaml.load(text, Loader=_LOADER)  # Loader derivado de SafeLoader
    except yaml.YAMLError as e:
        mark = getattr(e, "problem_mark", None)
        where = f" (linha {mark.line + 1})" if mark else ""
        lines = str(e).strip().splitlines()
        err(f"{label}: YAML inválido{where}: {lines[0] if lines else type(e).__name__}")
        return _FAILED


def scan(root):
    """Lista arquivos regulares sem seguir symlinks; symlinks viram erro e não são lidos."""
    files = []
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        base = Path(dirpath)
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for d in list(dirnames):
            if (base / d).is_symlink():
                err(f"{rel(root, base / d)}: symlink de diretório não é permitido; o destino não foi lido")
                dirnames.remove(d)
        for f in sorted(filenames):
            p = base / f
            if p.is_symlink():
                err(f"{rel(root, p)}: symlink não é permitido; o destino não foi lido")
            else:
                files.append(p)
    return files


def read_text(root, path):
    """Lê somente arquivo regular dentro da raiz; erros viram mensagens."""
    if path.is_symlink() or not is_within(path, root):
        err(f"{rel(root, path) if is_within(path, root) else path.name}: fora da raiz ou symlink; não lido")
        return None
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        err(f"{rel(root, path)}: não foi possível ler como UTF-8 ({type(e).__name__})")
        return None


def check_skill(root):
    skill = root / "SKILL.md"
    if not skill.exists() and not skill.is_symlink():
        err("SKILL.md não encontrado")
        return None
    text = read_text(root, skill)
    if text is None:
        return None
    m = FM_RE.match(text)
    if not m:
        err("SKILL.md: frontmatter ausente ou malformado")
        return None
    fm = load_yaml(m.group(1), "SKILL.md (frontmatter)")
    if fm is _FAILED:
        return None
    if not isinstance(fm, dict):
        err("SKILL.md: frontmatter deve ser um mapa YAML com 'name' e 'description'")
        return None
    name, desc = fm.get("name"), fm.get("description")
    if not is_text(name):
        err(f"SKILL.md: 'name' ausente ou não é texto (tipo: {type(name).__name__})")
        name = None
    elif not NAME_RE.match(name) or len(name) > NAME_MAX:
        err(f"SKILL.md: 'name' inválido ({name!r}); use minúsculas, números e hifens, até {NAME_MAX}")
    elif name != root.name:
        warn(f"nome da skill ({name}) difere da pasta ({root.name}); confirme a exigência do host")
    if not is_text(desc):
        err(f"SKILL.md: 'description' ausente ou não é texto (tipo: {type(desc).__name__})")
    elif len(desc) > DESC_ERROR:
        err(f"SKILL.md: descrição com {len(desc)} caracteres (> {DESC_ERROR})")
    elif len(desc) > DESC_WARN:
        warn(f"SKILL.md: descrição com {len(desc)} caracteres (> {DESC_WARN} da especificação portátil)")
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
                err(f"{rel(root, md)}: link aponta para fora do projeto -> {target}")
            elif not dest.exists():
                err(f"{rel(root, md)}: link quebrado -> {target}")


def check_backtick_paths(root, files):
    """Caminhos entre crases em Markdown (fora das fixtures) devem existir dentro do projeto."""
    for md in markdown_files(root, files):
        text = read_text(root, md)
        if text is None:
            continue
        for target in PATH_RE.findall(text):
            dest = root / target.rstrip(".,;:)")
            if not is_within(dest, root):
                err(f"{rel(root, md)}: caminho citado aponta para fora do projeto -> {target}")
            elif not dest.exists():
                err(f"{rel(root, md)}: caminho citado não existe -> {target}")


def check_fixture(root, label, fixture, referenced):
    if not is_text(fixture):
        return
    p = Path(fixture)
    if p.is_absolute() or ".." in p.parts:
        err(f"{label}: fixture deve ser caminho relativo sem '..' -> {fixture}")
        return
    full = root / p
    if not is_within(full, root / "evals" / "files"):
        err(f"{label}: fixture fora de evals/files -> {fixture}")
        return
    if full.is_symlink():
        err(f"{label}: fixture é symlink; não permitido -> {fixture}")
        return
    if not full.is_file():
        err(f"{label}: fixture inexistente -> {fixture}")
        return
    referenced.add(p.as_posix())


def check_one_eval(root, ev, index, ids, referenced):
    label = f"evals[{index}]"
    if not isinstance(ev, dict):
        err(f"{label}: cada cenário deve ser um objeto (tipo: {type(ev).__name__})")
        return
    eid = ev.get("id")
    if isinstance(eid, int) and not isinstance(eid, bool):
        label = f"eval {eid}"
        if eid in ids:
            err(f"{label}: id duplicado")
        ids.add(eid)
    else:
        err(f"{label}: 'id' deve ser inteiro (tipo: {type(eid).__name__})")
    for k in EVAL_TEXT_KEYS + EVAL_LIST_KEYS:
        if k not in ev:
            err(f"{label}: campo ausente -> {k}")
    for k in EVAL_TEXT_KEYS:
        if k in ev and not is_text(ev[k]):
            err(f"{label}: '{k}' deve ser texto não vazio")
    for k in EVAL_LIST_KEYS:
        if k in ev and not is_text_list(ev[k]):
            err(f"{label}: '{k}' deve ser lista de textos não vazios")
    etype, sev = ev.get("type"), ev.get("severity_if_failed")
    if is_text(etype) and etype not in EVAL_TYPES:
        err(f"{label}: 'type' deve ser um de {sorted(EVAL_TYPES)}")
    if is_text(sev) and sev not in EVAL_SEVERITIES:
        err(f"{label}: 'severity_if_failed' deve ser um de {sorted(EVAL_SEVERITIES)}")
    if is_text_list(ev.get("expectations")) and not ev["expectations"]:
        err(f"{label}: 'expectations' deve ter ao menos uma asserção")
    if etype in {"segurança", "ativação"} and is_text_list(ev.get("forbidden")) and not ev["forbidden"]:
        err(f"{label}: casos de {etype} exigem 'forbidden' não vazio")
    files = ev.get("files")
    if is_text_list(files) and not files and not is_text(ev.get("no_fixture_reason")):
        err(f"{label}: sem fixtures e sem 'no_fixture_reason'")
    if etype == "segurança":
        if not (is_text_list(ev.get("inspect")) and ev.get("inspect")):
            err(f"{label}: caso de segurança exige 'inspect' (lista não vazia)")
        if not is_text(ev.get("safe_action")):
            err(f"{label}: caso de segurança exige 'safe_action'")
    if isinstance(files, list):
        for fixture in files:
            check_fixture(root, label, fixture, referenced)


def check_evals(root, name, files):
    path = root / "evals" / "evals.json"
    if not path.exists() and not path.is_symlink():
        err("evals/evals.json não encontrado")
        return
    text = read_text(root, path)
    if text is None:
        return
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        err(f"evals/evals.json: JSON inválido ({e})")
        return
    if not isinstance(data, dict):
        err(f"evals/evals.json: a raiz deve ser um objeto (tipo: {type(data).__name__})")
        return
    if name and data.get("skill_name") != name:
        err(f"evals/evals.json: skill_name ({data.get('skill_name')!r}) difere do name do SKILL.md ({name!r})")
    evals = data.get("evals")
    if not isinstance(evals, list) or not evals:
        err("evals/evals.json: 'evals' deve ser uma lista não vazia")
        return
    ids, referenced = set(), set()
    for i, ev in enumerate(evals):
        check_one_eval(root, ev, i, ids, referenced)
    for f in files:
        r = rel(root, f)
        if not r.startswith("evals/files/"):
            continue
        if f.name == "SKILL.md":
            err(f"{r}: fixture chamada SKILL.md pode ser descoberta como skill instalada")
        if r not in referenced:
            warn(f"{r}: fixture não referenciada em nenhum eval")


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
        err("agents/openai.yaml: a raiz deve ser um mapa YAML com 'interface'")
        return
    iface = data.get("interface")
    if not isinstance(iface, dict):
        err("agents/openai.yaml: 'interface' ausente ou não é um mapa")
        return
    for key in OPENAI_REQUIRED:
        if not is_text(iface.get(key)):
            err(f"agents/openai.yaml: interface.{key} ausente ou não é texto")
    prompt = iface.get("default_prompt")
    if is_text(prompt) and name and f"${name}" not in prompt:
        err(f"agents/openai.yaml: default_prompt não cita ${name}")


def check_line_endings(root, files):
    for f in files:
        if f.suffix in TEXT_EXTS:
            try:
                has_crlf = b"\r\n" in f.read_bytes()
            except OSError as e:
                err(f"{rel(root, f)}: não foi possível ler ({type(e).__name__})")
                continue
            if has_crlf:
                warn(f"{rel(root, f)}: contém CRLF (o repositório usa LF; ver .gitattributes)")


def guarded(fn, *args):
    """Falha inesperada vira erro legível, nunca traceback."""
    try:
        return fn(*args)
    except Exception as e:  # noqa: BLE001
        err(f"falha inesperada em {fn.__name__}: {type(e).__name__}: {e}")
        return None


def main():
    global _LOADER
    if yaml is None:
        print("ERRO: PyYAML não instalado. Rode: pip install -r requirements-dev.txt")
        sys.exit(2)
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    if not root.is_dir():
        print(f"ERRO: raiz inexistente ou não é diretório: {root}")
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
        print(f"AVISO: {w}")
    for e in errors:
        print(f"ERRO:  {e}")
    print(f"\n{len(errors)} erro(s), {len(warnings)} aviso(s)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
