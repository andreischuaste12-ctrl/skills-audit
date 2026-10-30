"""Validator tests: every deliberately injected defect must be detected.

Usage: python3 -m unittest discover -s scripts -p "test_*.py"
Requires PyYAML (pip install -r requirements-dev.txt).
Each test copies the project to a temporary directory and injects a defect.
"""
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
VALIDATE = ROOT / "scripts" / "validate.py"
MARKER = "LEAK_MARKER"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_under_test", VALIDATE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def copy_project(dst):
    shutil.copytree(ROOT, dst, ignore=shutil.ignore_patterns(".git", "__pycache__"), dirs_exist_ok=True)


def run_validate(root):
    proc = subprocess.run([sys.executable, str(VALIDATE), str(root)], capture_output=True, text=True)
    return proc.returncode, proc.stdout + proc.stderr


class ValidatorTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.root = base / "project"
        self.outside = base / "outside"
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
            self.skipTest("symlinks unavailable in this environment")

    # --- baseline --------------------------------------------------------
    def test_intact_project_passes(self):
        code, out = run_validate(self.root)
        self.assertEqual(code, 0, out)
        self.assertNotIn("Traceback", out)

    def test_missing_pyyaml_fails_with_clear_message(self):
        code = ("import sys, runpy; sys.modules['yaml'] = None; "
                f"sys.argv = ['validate.py', r'{self.root}']; "
                f"runpy.run_path(r'{VALIDATE}', run_name='__main__')")
        proc = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
        self.assertIn("PyYAML is not installed", proc.stdout)

    # --- frontmatter and YAML --------------------------------------------
    def test_invalid_name(self):
        self.edit("SKILL.md", lambda t: t.replace("name: improve-skills-konvert", "name: Invalid_Name", 1))
        self.assertDetects("invalid 'name'")

    def test_description_over_the_limit(self):
        self.edit("SKILL.md", lambda t: re.sub(r"(?m)^description: .*$", "description: " + "x" * 1600, t, count=1))
        self.assertDetects("description has 1600 characters")

    def test_truncated_frontmatter_yaml(self):
        self.set_frontmatter(lambda fm: re.sub(r"(?m)^description: .*$", 'description: "opened and never closed', fm, count=1))
        self.assertDetects("invalid YAML")

    def test_frontmatter_with_unquoted_colon(self):
        self.set_frontmatter(lambda fm: re.sub(r"(?m)^description: .*$", "description: Use when: the request cites a skill", fm, count=1))
        self.assertDetects("invalid YAML")

    def test_frontmatter_name_with_wrong_type(self):
        self.set_frontmatter(lambda fm: re.sub(r"(?m)^name: .*$", "name: 123", fm, count=1))
        self.assertDetects("'name' missing or not text")

    def test_frontmatter_description_with_wrong_type(self):
        self.set_frontmatter(lambda fm: re.sub(r"(?m)^description: .*$", "description: [a, b]", fm, count=1))
        self.assertDetects("'description' missing or not text")

    def test_frontmatter_duplicate_field(self):
        self.set_frontmatter(lambda fm: fm + "\nname: another-name")
        self.assertDetects("duplicate key")

    def test_frontmatter_is_not_a_mapping(self):
        self.set_frontmatter(lambda fm: "- a\n- b")
        self.assertDetects("must be a YAML mapping")

    def test_malformed_openai_yaml(self):
        (self.root / "agents" / "openai.yaml").write_text("interface: [a, b\n", encoding="utf-8")
        self.assertDetects("agents/openai.yaml: invalid YAML")

    def test_openai_yaml_interface_is_not_a_mapping(self):
        (self.root / "agents" / "openai.yaml").write_text("interface:\n  - x\n", encoding="utf-8")
        self.assertDetects("'interface' missing or not a mapping")

    def test_openai_yaml_field_with_wrong_type(self):
        self.edit("agents/openai.yaml", lambda t: re.sub(r'display_name: ".*"', "display_name: 5", t, count=1))
        self.assertDetects("interface.display_name missing or not text")

    def test_openai_yaml_duplicate_key(self):
        self.edit("agents/openai.yaml", lambda t: t + '  display_name: "another"\n')
        self.assertDetects("duplicate key")

    def test_openai_yaml_required_field_missing(self):
        self.edit("agents/openai.yaml", lambda t: t.replace("short_description:", "summary:"))
        self.assertDetects("interface.short_description")

    def test_default_prompt_of_another_skill(self):
        self.edit("agents/openai.yaml", lambda t: t.replace("$improve-skills-konvert", "$other"))
        self.assertDetects("default_prompt does not cite")

    # --- links and paths -------------------------------------------------
    def test_broken_link(self):
        self.edit("references/audit-criteria.md", lambda t: t + "\n[x](references/does-not-exist.md)\n")
        self.assertDetects("broken link")

    def test_link_outside_the_project(self):
        (self.outside / "x.md").write_text("x", encoding="utf-8")
        self.edit("references/audit-criteria.md", lambda t: t + "\n[x](../../outside/x.md)\n")
        self.assertDetects("link points outside the project")

    def test_cited_path_does_not_exist(self):
        self.edit("README.md", lambda t: t + "\nSee `scripts/missing.py`.\n")
        self.assertDetects("cited path does not exist")

    # --- eval structure and types ----------------------------------------
    def test_evals_root_is_not_an_object(self):
        self.write_evals_raw([])
        self.assertDetects("the root must be an object")

    def test_evals_is_not_a_list(self):
        self.write_evals_raw({"skill_name": "improve-skills-konvert", "evals": {"a": 1}})
        self.assertDetects("'evals' must be a non-empty list")

    def test_scenario_is_not_an_object(self):
        self.write_evals_raw({"skill_name": "improve-skills-konvert", "evals": ["text"]})
        self.assertDetects("each scenario must be an object")

    def test_files_is_not_a_list_of_strings(self):
        self.edit_evals(lambda d: d["evals"][0].update(files="evals/files/flawed-skill.txt"))
        self.assertDetects("'files' must be a list of non-empty strings")

    def test_expectations_with_a_non_text_item(self):
        self.edit_evals(lambda d: d["evals"][0].update(expectations=["ok", 5]))
        self.assertDetects("'expectations' must be a list of non-empty strings")

    def test_forbidden_is_not_a_list(self):
        self.edit_evals(lambda d: d["evals"][0].update(forbidden="no"))
        self.assertDetects("'forbidden' must be a list of non-empty strings")

    def test_eval_without_assertions(self):
        self.edit_evals(lambda d: d["evals"][0].update(expectations=[]))
        self.assertDetects("'expectations' must have at least one assertion")

    def test_duplicate_id(self):
        self.edit_evals(lambda d: d["evals"][1].update(id=d["evals"][0]["id"]))
        self.assertDetects("duplicate id")

    def test_id_with_wrong_type(self):
        for bad in ("1", True, [1]):
            with self.subTest(bad=bad):
                self.edit_evals(lambda d: d["evals"][0].update(id=bad))
                self.assertDetects("'id' must be an integer")

    def test_invalid_scenario_type(self):
        self.edit_evals(lambda d: d["evals"][0].update(type="invented"))
        self.assertDetects("'type' must be one of")

    def test_security_without_safe_action(self):
        def mutate(d):
            next(e for e in d["evals"] if e["type"] == "security").pop("safe_action")
        self.edit_evals(mutate)
        self.assertDetects("requires 'safe_action'")

    def test_security_without_inspect(self):
        def mutate(d):
            next(e for e in d["evals"] if e["type"] == "security").update(inspect=[])
        self.edit_evals(mutate)
        self.assertDetects("requires 'inspect'")

    def test_no_fixture_requires_a_reason(self):
        def mutate(d):
            next(e for e in d["evals"] if not e["files"]).pop("no_fixture_reason")
        self.edit_evals(mutate)
        self.assertDetects("no 'no_fixture_reason'")

    def test_eval_skill_name_differs(self):
        self.edit_evals(lambda d: d.update(skill_name="other-skill"))
        self.assertDetects("skill_name")

    # --- fixtures --------------------------------------------------------
    def test_nonexistent_fixture(self):
        self.edit_evals(lambda d: d["evals"][0]["files"].append("evals/files/does-not-exist.txt"))
        self.assertDetects("fixture does not exist")

    def test_fixture_with_absolute_path(self):
        self.edit_evals(lambda d: d["evals"][0]["files"].append(str(self.outside / "x.txt")))
        self.assertDetects("relative path without '..'")

    def test_fixture_with_dot_dot(self):
        self.edit_evals(lambda d: d["evals"][0]["files"].append("evals/files/../../README.md"))
        self.assertDetects("relative path without '..'")

    def test_fixture_outside_evals_files(self):
        self.edit_evals(lambda d: d["evals"][0]["files"].append("README.md"))
        self.assertDetects("fixture outside evals/files")

    def test_fixture_named_skill_md(self):
        shutil.copy(self.root / "evals/files/exfil-skill.txt", self.root / "evals/files/SKILL.md")
        self.assertDetects("may be discovered as an installed skill")

    # --- symlinks --------------------------------------------------------
    def test_markdown_symlink_to_outside_is_not_read(self):
        (self.outside / "external.md").write_text(f"`scripts/{MARKER}.py`\n", encoding="utf-8")
        self.link(self.outside / "external.md", self.root / "references" / "link.md")
        out = self.assertDetects("references/link.md: symlink not allowed")
        self.assertNotIn(MARKER, out)

    def test_fixture_symlink_to_outside_is_rejected(self):
        (self.outside / "secret.txt").write_text(MARKER, encoding="utf-8")
        fixture = self.root / "evals" / "files" / "exfil-skill.txt"
        fixture.unlink()
        self.link(self.outside / "secret.txt", fixture)
        out = self.assertDetects("symlink")
        self.assertNotIn(MARKER, out)

    def test_directory_symlink_is_not_traversed(self):
        folder = self.outside / "folder"
        folder.mkdir()
        (folder / "external.md").write_text(f"`scripts/{MARKER}.py`\n", encoding="utf-8")
        self.link(folder, self.root / "references" / "folder-link")
        out = self.assertDetects("directory symlink not allowed")
        self.assertNotIn(MARKER, out)

    def test_symlinked_skill_md_is_not_read(self):
        (self.outside / "skill.md").write_text(f"---\nname: x\ndescription: {MARKER}\n---\n", encoding="utf-8")
        (self.root / "SKILL.md").unlink()
        self.link(self.outside / "skill.md", self.root / "SKILL.md")
        out = self.assertDetects("SKILL.md: ")
        self.assertNotIn(MARKER, out)

    # --- unreadable directories ------------------------------------------
    def test_unreadable_directory_is_reported_not_skipped(self):
        # os.walk reports nothing by default; this checks the onerror wiring even when running as root.
        module = load_validator()
        target = os.fspath(self.root.resolve() / "references")
        real_scandir = os.scandir

        def fake_scandir(path="."):
            if os.fspath(path) == target:
                raise PermissionError(13, "Permission denied", target)
            return real_scandir(path)

        with mock.patch("os.scandir", side_effect=fake_scandir):
            module.scan(self.root.resolve())
        self.assertTrue(
            any("directory could not be read" in e and "references" in e for e in module.errors), module.errors
        )

    def test_permission_denied_directory_fails_validation(self):
        folder = self.root / "references"
        folder.chmod(0o000)
        try:
            if os.access(folder, os.R_OK):
                self.skipTest("permissions are not enforced (running as root)")
            self.assertDetects("directory could not be read")
        finally:
            folder.chmod(0o755)

    # --- line endings ----------------------------------------------------
    def test_crlf_produces_a_warning(self):
        p = self.root / "references" / "audit-criteria.md"
        p.write_bytes(p.read_bytes().replace(b"\n", b"\r\n"))
        code, out = run_validate(self.root)
        self.assertEqual(code, 0, out)
        self.assertIn("contains CRLF", out)


if __name__ == "__main__":
    unittest.main()
