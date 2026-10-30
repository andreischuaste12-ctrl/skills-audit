#!/usr/bin/env python3
"""Validação estrutural da skill (somente stdlib).

Uso: python3 scripts/validate.py [raiz-da-skill]

Verifica frontmatter, limites da descrição, links locais, evals, fixtures,
agents/openai.yaml e fim de linha. Não mede qualidade das decisões da skill:
isso exige execução real (ver evals/RESULTS.md).
Saída: 0 sem erros (avisos permitidos); 1 com ao menos um erro.
"""
import json
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
NAME_MAX = 64
DESC_WARN = 1024  # limite da especificação portátil (não verificado nesta versão)
DESC_ERROR = 1536  # limite de listagem do Claude Code
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
EVAL_KEYS = {
    "id", "category", "type", "objective", "prompt", "files", "expected_output",
    "expectations", "forbidden", "allowed_changes", "severity_if_failed",
}
EVAL_TYPES = {"ativação", "execução", "segurança", "regressão"}
EVAL_SEVERITIES = {"crítica", "alta", "média"}
PATH_RE = re.compile(r"`((?:scripts|references|evals|agents)/[^`\s<>*]+)`")

errors, warnings = [], []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def parse_frontmatter(text):
    m = re.match(r"---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    if not m:
        return None
    fields = {}
    for line in m.group(1).splitlines():
        k, sep, v = line.partition(":")
        if sep and not line.startswith((" ", "\t")):
            fields[k.strip()] = v.strip()
    return fields


def check_skill(root):
    skill = root / "SKILL.md"
    if not skill.is_file():
        err("SKILL.md não encontrado")
        return None
    fm = parse_frontmatter(skill.read_text(encoding="utf-8"))
    if fm is None:
        err("SKILL.md: frontmatter ausente ou malformado")
        return None
    name, desc = fm.get("name", ""), fm.get("description", "")
    if not name:
        err("SKILL.md: 'name' ausente")
    elif not NAME_RE.match(name) or len(name) > NAME_MAX:
        err(f"SKILL.md: 'name' inválido ({name!r}); use minúsculas, números e hifens, até {NAME_MAX}")
    elif name != root.name:
        warn(f"nome da skill ({name}) difere da pasta ({root.name}); confirme a exigência do host")
    if not desc:
        err("SKILL.md: 'description' ausente")
    elif len(desc) > DESC_ERROR:
        err(f"SKILL.md: descrição com {len(desc)} caracteres (> {DESC_ERROR})")
    elif len(desc) > DESC_WARN:
        warn(f"SKILL.md: descrição com {len(desc)} caracteres (> {DESC_WARN} da especificação portátil)")
    return name


def check_links(root):
    for md in sorted(root.rglob("*.md")):
        if ".git" in md.parts or "files" in md.relative_to(root).parts[:2]:
            continue
        for target in LINK_RE.findall(md.read_text(encoding="utf-8")):
            if re.match(r"^(https?:|mailto:|#)", target):
                continue
            path = target.split("#", 1)[0]
            if path and not (md.parent / path).exists():
                err(f"{md.relative_to(root)}: link quebrado -> {target}")


def check_backtick_paths(root):
    """Caminhos entre crases em Markdown (fora das fixtures) devem existir."""
    for md in sorted(root.rglob("*.md")):
        rel = md.relative_to(root)
        if ".git" in md.parts or rel.parts[:2] == ("evals", "files"):
            continue
        for target in PATH_RE.findall(md.read_text(encoding="utf-8")):
            if not (root / target.rstrip(".,;:)")).exists():
                err(f"{rel}: caminho citado não existe -> {target}")


def check_evals(root, name):
    path = root / "evals" / "evals.json"
    if not path.is_file():
        err("evals/evals.json não encontrado")
        return
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        err(f"evals/evals.json: JSON inválido ({e})")
        return
    if name and data.get("skill_name") != name:
        err(f"evals/evals.json: skill_name ({data.get('skill_name')!r}) difere do name do SKILL.md ({name!r})")
    ids, referenced = set(), set()
    for ev in data.get("evals", []):
        eid = ev.get("id")
        missing = EVAL_KEYS - ev.keys()
        if missing:
            err(f"eval {eid}: campos ausentes {sorted(missing)}")
        if eid in ids:
            err(f"eval {eid}: id duplicado")
        ids.add(eid)
        if not ev.get("expectations"):
            err(f"eval {eid}: sem asserções em 'expectations'")
        if ev.get("type") not in EVAL_TYPES:
            err(f"eval {eid}: 'type' deve ser um de {sorted(EVAL_TYPES)}")
        if ev.get("severity_if_failed") not in EVAL_SEVERITIES:
            err(f"eval {eid}: 'severity_if_failed' deve ser um de {sorted(EVAL_SEVERITIES)}")
        if not ev.get("forbidden") and ev.get("type") in {"segurança", "ativação"}:
            err(f"eval {eid}: casos de {ev.get('type')} exigem 'forbidden' não vazio")
        if not ev.get("files") and not ev.get("no_fixture_reason"):
            err(f"eval {eid}: sem fixtures e sem 'no_fixture_reason'")
        if ev.get("type") == "segurança":
            for k in ("inspect", "safe_action"):
                if not ev.get(k):
                    err(f"eval {eid}: caso de segurança exige '{k}'")
        for f in ev.get("files", []):
            referenced.add(f)
            if not (root / f).is_file():
                err(f"eval {eid}: fixture inexistente -> {f}")
    fixtures = root / "evals" / "files"
    if fixtures.is_dir():
        for f in sorted(p for p in fixtures.rglob("*") if p.is_file()):
            rel = f.relative_to(root).as_posix()
            if f.name == "SKILL.md":
                err(f"{rel}: fixture chamada SKILL.md pode ser descoberta como skill instalada")
            if rel not in referenced:
                warn(f"{rel}: fixture não referenciada em nenhum eval")


def check_openai_yaml(root, name):
    path = root / "agents" / "openai.yaml"
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    for key in ("display_name", "short_description", "default_prompt"):
        if not re.search(rf'^\s*{key}:\s*".+"', text, re.M):
            err(f"agents/openai.yaml: campo obrigatório ausente ou vazio -> {key}")
    m = re.search(r'default_prompt:\s*"(.*)"', text)
    if m and name and f"${name}" not in m.group(1):
        err(f"agents/openai.yaml: default_prompt não cita ${name}")


def check_line_endings(root):
    exts = {".md", ".json", ".yaml", ".yml", ".py", ".txt"}
    for f in sorted(root.rglob("*")):
        if f.is_file() and f.suffix in exts and ".git" not in f.parts:
            if b"\r\n" in f.read_bytes():
                warn(f"{f.relative_to(root)}: contém CRLF (o repositório usa LF; ver .gitattributes)")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    name = check_skill(root)
    check_links(root)
    check_backtick_paths(root)
    check_evals(root, name)
    check_openai_yaml(root, name)
    check_line_endings(root)
    for w in warnings:
        print(f"AVISO: {w}")
    for e in errors:
        print(f"ERRO:  {e}")
    print(f"\n{len(errors)} erro(s), {len(warnings)} aviso(s)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
