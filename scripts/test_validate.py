"""Testes do validador: cada defeito introduzido de propósito deve ser detectado.

Uso: python3 -m unittest discover -s scripts -p "test_*.py"
Requer PyYAML (pip install -r requirements-dev.txt).
Cada teste copia o projeto para um diretório temporário e injeta um defeito.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VALIDATE = ROOT / "scripts" / "validate.py"
MARKER = "VAZAMENTO_MARCADOR"


def copy_project(dst):
    shutil.copytree(ROOT, dst, ignore=shutil.ignore_patterns(".git", "__pycache__"), dirs_exist_ok=True)


def run_validate(root):
    proc = subprocess.run([sys.executable, str(VALIDATE), str(root)], capture_output=True, text=True)
    return proc.returncode, proc.stdout + proc.stderr


class ValidatorTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.root = base / "projeto"
        self.outside = base / "fora"
        self.outside.mkdir()
        copy_project(self.root)

    def tearDown(self):
        self.tmp.cleanup()

    def assertDetects(self, fragment):
        code, out = run_validate(self.root)
        self.assertEqual(code, 1, out)
        self.assertIn(fragment, out)
        self.assertNotIn("Traceback", out)
        return out

    def edit(self, rel, fn):
        p = self.root / rel
        p.write_text(fn(p.read_text(encoding="utf-8")), encoding="utf-8")

    def edit_evals(self, fn):
        p = self.root / "evals" / "evals.json"
        data = json.loads(p.read_text(encoding="utf-8"))
        data = fn(data) or data
        p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def write_evals_raw(self, obj):
        (self.root / "evals" / "evals.json").write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")

    def set_frontmatter(self, transform):
        self.edit("SKILL.md", lambda t: re.sub(r"\A---\r?\n(.*?)\r?\n---\r?\n",
                                               lambda m: "---\n" + transform(m.group(1)) + "\n---\n", t, count=1, flags=re.S))

    def link(self, target, link):
        try:
            os.symlink(target, link)
        except (OSError, NotImplementedError):
            self.skipTest("symlinks indisponíveis neste ambiente")

    # --- linha de base ---------------------------------------------------
    def test_projeto_integro_passa(self):
        code, out = run_validate(self.root)
        self.assertEqual(code, 0, out)
        self.assertNotIn("Traceback", out)

    def test_pyyaml_ausente_falha_com_mensagem_clara(self):
        code = ("import sys, runpy; sys.modules['yaml'] = None; "
                f"sys.argv = ['validate.py', r'{self.root}']; "
                f"runpy.run_path(r'{VALIDATE}', run_name='__main__')")
        proc = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
        self.assertIn("PyYAML não instalado", proc.stdout)

    # --- frontmatter e YAML ----------------------------------------------
    def test_nome_invalido(self):
        self.edit("SKILL.md", lambda t: t.replace("name: improve-skills-konvert", "name: Nome_Invalido", 1))
        self.assertDetects("'name' inválido")

    def test_descricao_acima_do_limite(self):
        self.edit("SKILL.md", lambda t: re.sub(r"(?m)^description: .*$", "description: " + "x" * 1600, t, count=1))
        self.assertDetects("descrição com 1600 caracteres")

    def test_frontmatter_yaml_truncado(self):
        self.set_frontmatter(lambda fm: re.sub(r"(?m)^description: .*$", 'description: "aberta sem fechar', fm, count=1))
        self.assertDetects("YAML inválido")

    def test_frontmatter_com_dois_pontos_sem_aspas(self):
        self.set_frontmatter(lambda fm: re.sub(r"(?m)^description: .*$", "description: Usar quando: o pedido citar skill", fm, count=1))
        self.assertDetects("YAML inválido")

    def test_frontmatter_name_com_tipo_incorreto(self):
        self.set_frontmatter(lambda fm: re.sub(r"(?m)^name: .*$", "name: 123", fm, count=1))
        self.assertDetects("'name' ausente ou não é texto")

    def test_frontmatter_description_com_tipo_incorreto(self):
        self.set_frontmatter(lambda fm: re.sub(r"(?m)^description: .*$", "description: [a, b]", fm, count=1))
        self.assertDetects("'description' ausente ou não é texto")

    def test_frontmatter_campo_duplicado(self):
        self.set_frontmatter(lambda fm: fm + "\nname: outro-nome")
        self.assertDetects("chave duplicada")

    def test_frontmatter_nao_e_mapa(self):
        self.set_frontmatter(lambda fm: "- a\n- b")
        self.assertDetects("deve ser um mapa YAML")

    def test_openai_yaml_malformado(self):
        (self.root / "agents" / "openai.yaml").write_text("interface: [a, b\n", encoding="utf-8")
        self.assertDetects("agents/openai.yaml: YAML inválido")

    def test_openai_yaml_interface_nao_e_mapa(self):
        (self.root / "agents" / "openai.yaml").write_text("interface:\n  - x\n", encoding="utf-8")
        self.assertDetects("'interface' ausente ou não é um mapa")

    def test_openai_yaml_campo_com_tipo_incorreto(self):
        self.edit("agents/openai.yaml", lambda t: re.sub(r'display_name: ".*"', "display_name: 5", t, count=1))
        self.assertDetects("interface.display_name ausente ou não é texto")

    def test_openai_yaml_chave_duplicada(self):
        self.edit("agents/openai.yaml", lambda t: t + '  display_name: "outro"\n')
        self.assertDetects("chave duplicada")

    def test_openai_yaml_campo_obrigatorio_ausente(self):
        self.edit("agents/openai.yaml", lambda t: t.replace("short_description:", "resumo:"))
        self.assertDetects("interface.short_description")

    def test_default_prompt_de_outra_skill(self):
        self.edit("agents/openai.yaml", lambda t: t.replace("$improve-skills-konvert", "$outra"))
        self.assertDetects("default_prompt não cita")

    # --- links e caminhos ------------------------------------------------
    def test_link_quebrado(self):
        self.edit("references/audit-criteria.md", lambda t: t + "\n[x](references/nao-existe.md)\n")
        self.assertDetects("link quebrado")

    def test_link_para_fora_do_projeto(self):
        (self.outside / "x.md").write_text("x", encoding="utf-8")
        self.edit("references/audit-criteria.md", lambda t: t + "\n[x](../../fora/x.md)\n")
        self.assertDetects("link aponta para fora do projeto")

    def test_caminho_citado_inexistente(self):
        self.edit("README.md", lambda t: t + "\nVeja `scripts/inexistente.py`.\n")
        self.assertDetects("caminho citado não existe")

    # --- estrutura e tipos de evals --------------------------------------
    def test_evals_raiz_nao_e_objeto(self):
        self.write_evals_raw([])
        self.assertDetects("a raiz deve ser um objeto")

    def test_evals_nao_e_lista(self):
        self.write_evals_raw({"skill_name": "improve-skills-konvert", "evals": {"a": 1}})
        self.assertDetects("'evals' deve ser uma lista não vazia")

    def test_cenario_nao_e_objeto(self):
        self.write_evals_raw({"skill_name": "improve-skills-konvert", "evals": ["texto"]})
        self.assertDetects("cada cenário deve ser um objeto")

    def test_files_nao_e_lista_de_textos(self):
        self.edit_evals(lambda d: d["evals"][0].update(files="evals/files/flawed-skill.txt"))
        self.assertDetects("'files' deve ser lista de textos não vazios")

    def test_expectations_com_item_nao_texto(self):
        self.edit_evals(lambda d: d["evals"][0].update(expectations=["ok", 5]))
        self.assertDetects("'expectations' deve ser lista de textos não vazios")

    def test_forbidden_nao_e_lista(self):
        self.edit_evals(lambda d: d["evals"][0].update(forbidden="não"))
        self.assertDetects("'forbidden' deve ser lista de textos não vazios")

    def test_eval_sem_assercoes(self):
        self.edit_evals(lambda d: d["evals"][0].update(expectations=[]))
        self.assertDetects("'expectations' deve ter ao menos uma asserção")

    def test_id_duplicado(self):
        self.edit_evals(lambda d: d["evals"][1].update(id=d["evals"][0]["id"]))
        self.assertDetects("id duplicado")

    def test_id_com_tipo_incorreto(self):
        for bad in ("1", True, [1]):
            with self.subTest(bad=bad):
                self.edit_evals(lambda d: d["evals"][0].update(id=bad))
                self.assertDetects("'id' deve ser inteiro")

    def test_tipo_de_cenario_invalido(self):
        self.edit_evals(lambda d: d["evals"][0].update(type="inventado"))
        self.assertDetects("'type' deve ser um de")

    def test_seguranca_sem_safe_action(self):
        def mutate(d):
            next(e for e in d["evals"] if e["type"] == "segurança").pop("safe_action")
        self.edit_evals(mutate)
        self.assertDetects("exige 'safe_action'")

    def test_seguranca_sem_inspect(self):
        def mutate(d):
            next(e for e in d["evals"] if e["type"] == "segurança").update(inspect=[])
        self.edit_evals(mutate)
        self.assertDetects("exige 'inspect'")

    def test_sem_fixture_exige_motivo(self):
        def mutate(d):
            next(e for e in d["evals"] if not e["files"]).pop("no_fixture_reason")
        self.edit_evals(mutate)
        self.assertDetects("sem 'no_fixture_reason'")

    def test_skill_name_dos_evals_diverge(self):
        self.edit_evals(lambda d: d.update(skill_name="outra-skill"))
        self.assertDetects("skill_name")

    # --- fixtures --------------------------------------------------------
    def test_fixture_inexistente(self):
        self.edit_evals(lambda d: d["evals"][0]["files"].append("evals/files/nao-existe.txt"))
        self.assertDetects("fixture inexistente")

    def test_fixture_com_caminho_absoluto(self):
        self.edit_evals(lambda d: d["evals"][0]["files"].append(str(self.outside / "x.txt")))
        self.assertDetects("caminho relativo sem '..'")

    def test_fixture_com_ponto_ponto(self):
        self.edit_evals(lambda d: d["evals"][0]["files"].append("evals/files/../../README.md"))
        self.assertDetects("caminho relativo sem '..'")

    def test_fixture_fora_de_evals_files(self):
        self.edit_evals(lambda d: d["evals"][0]["files"].append("README.md"))
        self.assertDetects("fixture fora de evals/files")

    def test_fixture_chamada_skill_md(self):
        shutil.copy(self.root / "evals/files/exfil-skill.txt", self.root / "evals/files/SKILL.md")
        self.assertDetects("pode ser descoberta como skill")

    # --- symlinks --------------------------------------------------------
    def test_symlink_markdown_para_fora_nao_e_lido(self):
        (self.outside / "externo.md").write_text(f"`scripts/{MARKER}.py`\n", encoding="utf-8")
        self.link(self.outside / "externo.md", self.root / "references" / "link.md")
        out = self.assertDetects("references/link.md: symlink não é permitido")
        self.assertNotIn(MARKER, out)

    def test_symlink_de_fixture_para_fora_e_rejeitado(self):
        (self.outside / "segredo.txt").write_text(MARKER, encoding="utf-8")
        fixture = self.root / "evals" / "files" / "exfil-skill.txt"
        fixture.unlink()
        self.link(self.outside / "segredo.txt", fixture)
        out = self.assertDetects("symlink")
        self.assertNotIn(MARKER, out)

    def test_symlink_de_diretorio_nao_e_percorrido(self):
        pasta = self.outside / "pasta"
        pasta.mkdir()
        (pasta / "externo.md").write_text(f"`scripts/{MARKER}.py`\n", encoding="utf-8")
        self.link(pasta, self.root / "references" / "pasta-link")
        out = self.assertDetects("symlink de diretório não é permitido")
        self.assertNotIn(MARKER, out)

    def test_symlink_no_skill_md_nao_e_lido(self):
        (self.outside / "skill.md").write_text(f"---\nname: x\ndescription: {MARKER}\n---\n", encoding="utf-8")
        (self.root / "SKILL.md").unlink()
        self.link(self.outside / "skill.md", self.root / "SKILL.md")
        out = self.assertDetects("SKILL.md: ")
        self.assertNotIn(MARKER, out)

    # --- fim de linha ----------------------------------------------------
    def test_crlf_gera_aviso(self):
        p = self.root / "references" / "audit-criteria.md"
        p.write_bytes(p.read_bytes().replace(b"\n", b"\r\n"))
        code, out = run_validate(self.root)
        self.assertEqual(code, 0, out)
        self.assertIn("contém CRLF", out)


if __name__ == "__main__":
    unittest.main()
