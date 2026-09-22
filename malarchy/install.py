#!/usr/bin/env python3
"""Install only Malarchy user overrides, retaining originals in a backup folder."""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import tempfile

ASSETS = Path(__file__).resolve().parent
LINKS = {
    ".config/omarchy/branding/about.txt": "about.txt",
    ".config/omarchy/branding/screensaver.txt": "screensaver.txt",
    ".local/bin/malarchy-about": "about.sh",
}
MENU = ".config/omarchy/extensions/omarchy-menu.jsonc"


def parse_jsonc(text):
    # Match strings first so URLs and escaped quotes cannot become comments.
    tokens = r'"(?:\\.|[^"\\])*"|//[^\n]*|/\*[\s\S]*?\*/'
    clean = re.sub(tokens, lambda m: m[0] if m[0].startswith('"') else " ", text)
    clean = re.sub(r'"(?:\\.|[^"\\])*"|,(\s*[}\]])',
                   lambda m: m[1] if m[1] else m[0], clean)
    result = json.loads(clean)
    if not isinstance(result, dict):
        raise ValueError("Menu must be a JSON object")
    return result


def exists(path):
    return path.exists() or path.is_symlink()


def install(home):
    home = home.resolve()
    menu = home / MENU
    # Read and validate all inputs before writing anything.
    current = parse_jsonc(menu.read_text()) if exists(menu) else {}
    overrides = json.loads((ASSETS / "menu.json").read_text())
    for key, value in overrides.items():
        previous = current.get(key, {})
        if not isinstance(previous, dict):
            raise ValueError(f"Menu entry {key} must be an object")
        current[key] = {**previous, **value}
    menu_text = json.dumps(current, indent=2, ensure_ascii=False) + "\n"
    changes = []
    for target, source in LINKS.items():
        source_path = ASSETS / source
        if not source_path.is_file():
            raise ValueError(f"Missing source: {source_path}")
        path = home / target
        if not (path.is_symlink() and os.readlink(path) == str(source_path)):
            changes.append((target, source_path))
    if not exists(menu) or menu.read_text() != menu_text:
        changes.append((MENU, None))
    for target, _ in changes:
        path = home / target
        if path.is_dir():
            raise ValueError(f"Refusing to replace a directory: {path}")
    if not changes:
        print("Malarchy branding already installed.")
        return
    backup_root = home / ".local/state/malarchy/backups"
    backup_root.mkdir(parents=True, exist_ok=True)
    backup = Path(tempfile.mkdtemp(prefix="branding-", dir=backup_root))
    saved = []
    for target, _ in changes:
        path = home / target
        if exists(path):
            destination = backup / target
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, destination, follow_symlinks=False)
            saved.append(target)
    (backup / "manifest.json").write_text(json.dumps({
        "home": str(home), "changed": [p for p, _ in changes], "saved": saved,
    }, indent=2) + "\n")
    # Originals are safe before the first mutation. Atomic replacement never
    # writes through an existing destination symlink into another repository.
    installed = []
    try:
        for target, source in changes:
            path = home / target
            path.parent.mkdir(parents=True, exist_ok=True)
            staging = Path(tempfile.mkdtemp(prefix=".malarchy-", dir=path.parent))
            replacement = staging / "replacement"
            if source is None:
                replacement.write_text(menu_text)
            else:
                replacement.symlink_to(source)
            os.replace(replacement, path)
            installed.append(target)
            staging.rmdir()
            print(f"Installed {path}")
    except OSError:
        # Preserve failed replacements too; never delete user data during recovery.
        for target in reversed(installed):
            path = home / target
            failed = backup / "failed-install" / target
            failed.parent.mkdir(parents=True, exist_ok=True)
            os.replace(path, failed)
            if target in saved:
                shutil.copy2(backup / target, path, follow_symlinks=False)
        print(f"Installation rolled back. Recovery files: {backup}")
        raise
    print(f"Originals and manifest: {backup}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", type=Path, default=Path.home())
    args = parser.parse_args()
    try:
        install(args.home)
    except (OSError, ValueError) as error:
        parser.exit(1, f"Malarchy installation stopped: {error}\n")
