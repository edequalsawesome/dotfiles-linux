"""Focused installer checks; fixtures are sent to the desktop trash."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock
import os
import shutil
import subprocess

spec = importlib.util.spec_from_file_location(
    "malarchy_installer", Path(__file__).resolve().parents[1] / "malarchy/install.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.home = Path(tempfile.mkdtemp(prefix=".malarchy-test-", dir=Path(__file__).resolve().parents[1]))
        self.menu = self.home / installer.MENU
        self.menu.parent.mkdir(parents=True)

    def tearDown(self):
        command = ["trash"] if shutil.which("trash") else ["gio", "trash"]
        subprocess.run([*command, str(self.home)], check=True)

    def test_late_failure_restores_all_originals(self):
        self.menu.write_text('{"personal": {"label": "Mine"}}')
        original = self.home / ".config/omarchy/branding/about.txt"
        original.parent.mkdir(parents=True)
        original.write_text("original branding")
        real_replace = os.replace

        def fail_menu(source, target):
            if target == self.menu:
                raise OSError("simulated late install failure")
            return real_replace(source, target)

        with mock.patch.object(installer.os, "replace", side_effect=fail_menu):
            with self.assertRaises(OSError):
                installer.install(self.home)
        self.assertFalse(original.is_symlink())
        self.assertEqual(original.read_text(), "original branding")
        self.assertEqual(self.menu.read_text(), '{"personal": {"label": "Mine"}}')
        self.assertFalse((self.home / ".local/bin/malarchy-about").is_symlink())
        self.assertFalse((self.home / ".config/omarchy/branding/screensaver.txt").is_symlink())

    def test_merge_and_repeat_preserves_original(self):
        original = '{ // custom menu\n"personal": {"action": "https://example.org/a//b",}, "about": {"icon": "i"},}'
        self.menu.write_text(original)
        installer.install(self.home)
        result = json.loads(self.menu.read_text())
        self.assertEqual(result["personal"]["action"], "https://example.org/a//b")
        self.assertEqual(result["about"]["icon"], "i")
        self.assertEqual(result["about"]["label"], "About Malarchy")
        backups = list((self.home / ".local/state/malarchy/backups").iterdir())
        self.assertEqual((backups[0] / installer.MENU).read_text(), original)
        installer.install(self.home)
        self.assertEqual(list((self.home / ".local/state/malarchy/backups").iterdir()), backups)
        for target, source in installer.LINKS.items():
            self.assertEqual((self.home / target).resolve(), installer.ASSETS / source)

    def test_symlink_is_backed_up_without_modifying_source(self):
        source = self.home / "original-menu.jsonc"
        source.write_text('{"personal": {"label": "Mine"}}')
        self.menu.symlink_to(source)
        installer.install(self.home)
        self.assertEqual(source.read_text(), '{"personal": {"label": "Mine"}}')
        backup = next((self.home / ".local/state/malarchy/backups").iterdir())
        self.assertTrue((backup / installer.MENU).is_symlink())

    def test_invalid_menu_does_not_mutate_branding(self):
        self.menu.write_text('{broken')
        with self.assertRaises(ValueError):
            installer.install(self.home)
        self.assertFalse((self.home / ".config/omarchy/branding").exists())
        self.assertEqual(self.menu.read_text(), '{broken')

    def test_directory_collision_fails_before_mutation(self):
        target = self.home / next(iter(installer.LINKS))
        target.mkdir(parents=True)
        with self.assertRaises(ValueError):
            installer.install(self.home)
        self.assertFalse((self.home / ".local/state/malarchy/backups").exists())

    def test_jsonc_strings_keep_comment_and_comma_lookalikes(self):
        source = r'{"x":{"label":"quote: \" // /* */ ,}",}, /*comment*/}'
        self.assertEqual(installer.parse_jsonc(source)["x"]["label"], 'quote: " // /* */ ,}')


if __name__ == "__main__":
    unittest.main()
