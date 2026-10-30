"""Testes do validador: cada defeito introduzido de propósito deve ser detectado.

Uso: python3 -m unittest discover -s scripts -p "test_*.py"
Cada teste copia o projeto para um diretório temporário e injeta um defeito.
"""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VALIDATE = ROOT / "scripts" / "validate.py"


def copy_project(dst):
    shutil.copytree(ROOT, dst, ignore=shutil.ignore_patterns(".git", "__pycache__"), dirs_exist_ok=True)


def run_validate(root):
    proc = subprocess.run(
        [sys.executable, "-I", str(VALIDATE), str(root)], capture_output=True, text=True
    )
    return proc.returncode, proc.stdout


class ValidatorTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "projeto"
        copy_project(self.root)

    def tearDown(self):
        self.tmp.cleanup()

    def assertDetects(self, fragment):
        code, out = run_validate(self.root)
        self.assertEqual(code, 1, out)
        self.assertIn(fragment, out)

    def edit(self, rel, fn):
        p = self.root / rel
        p.write_text(fn(p.read_text(encoding="utf-8")), encoding="utf-8")

    def edit_evals(self, fn):
        p = self.root / "evals" / "evals.json"
        data = json.loads(p.read_text(encoding="utf-8"))
        fn(data)
        p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def test_projeto_integro_passa(self):
        code, out = run_validate(self.root)
        self.assertEqual(code, 0, out)

    def test_nome_invalido(self):
        self.edit("SKILL.md", lambda t: t.replace("name: improve-skills-konvert", "name: Nome_Invalido", 1))
        self.assertDetects("'name' inválido")

    def test_descricao_acima_do_limite(self):
        import re
        self.edit("SKILL.md", lambda t: re.sub(r"(?m)^description: .*$", "description: " + "x" * 1600, t))
        self.assertDetects("descrição com 1600 caracteres")

    def test_link_quebrado(self):
        self.edit("references/audit-criteria.md", lambda t: t + "\n[x](references/nao-existe.md)\n")
        self.assertDetects("link quebrado")

    def test_caminho_citado_inexistente(self):
        self.edit("README.md", lambda t: t + "\nVeja `scripts/inexistente.py`.\n")
        self.assertDetects("caminho citado não existe")

    def test_fixture_inexistente(self):
        self.edit_evals(lambda d: d["evals"][0]["files"].append("evals/files/nao-existe.txt"))
        self.assertDetects("fixture inexistente")

    def test_eval_sem_assercoes(self):
        self.edit_evals(lambda d: d["evals"][0].update(expectations=[]))
        self.assertDetects("sem asserções")

    def test_seguranca_sem_safe_action(self):
        def mutate(d):
            ev = next(e for e in d["evals"] if e["type"] == "segurança")
            ev.pop("safe_action")
        self.edit_evals(mutate)
        self.assertDetects("exige 'safe_action'")

    def test_sem_fixture_exige_motivo(self):
        def mutate(d):
            ev = next(e for e in d["evals"] if e["id"] == 3)
            ev.pop("no_fixture_reason")
        self.edit_evals(mutate)
        self.assertDetects("sem 'no_fixture_reason'")

    def test_skill_name_dos_evals_diverge(self):
        self.edit_evals(lambda d: d.update(skill_name="outra-skill"))
        self.assertDetects("skill_name")

    def test_fixture_chamada_skill_md(self):
        shutil.copy(self.root / "evals/files/exfil-skill.txt", self.root / "evals/files/SKILL.md")
        self.assertDetects("pode ser descoberta como skill")

    def test_default_prompt_de_outra_skill(self):
        self.edit("agents/openai.yaml", lambda t: t.replace("$improve-skills-konvert", "$outra"))
        self.assertDetects("default_prompt não cita")

    def test_campo_obrigatorio_do_yaml(self):
        self.edit("agents/openai.yaml", lambda t: t.replace("short_description:", "resumo:"))
        self.assertDetects("short_description")


if __name__ == "__main__":
    unittest.main()
