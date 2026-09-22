# Malarchy

*Listen here, jack. It’s your computer.*

This is the initial public source snapshot. Current development and the complete artwork backup live in the dedicated private [Malarchy repository](https://github.com/edequalsawesome/malarchy).

A personal Catppuccin desktop with a 1990s cut-and-paste magazine identity. Omarchy remains the engine. This layer supplies a local collage wallpaper, terminal wordmarks and three menu overrides: About Malarchy, a clearly labeled engine manual, and a hidden ONCE installer entry.

## Install

From the canonical dotfiles checkout (links point back to this checkout):

```sh
python3 malarchy/install.py
bash malarchy/render.sh
omarchy theme bg set "$PWD/malarchy/local/wallpaper.png"
```

The installer merges its menu fields into existing JSONC, retaining unrelated entries and fields. Comments are normalized away; the exact original file is backed up. It saves replaced files and symlinks under `~/.local/state/malarchy/backups/branding-*`, with a manifest listing changed and previously existing paths. Repeating the install makes no new backup when nothing changed. If applying a replacement fails, it restores previously replaced paths and retains both originals and failed replacements for recovery. A process kill or storage failure can still require manual recovery from the backup.

The normal dotfiles installer does not opt other machines into Malarchy. This explicit installer changes only user branding, the About launcher and menu overrides. Catppuccin, terminal startup (including Rocket), shortcuts, package sources, lock timing and installed applications remain intact.

Rendering needs Chromium, ImageMagick, curl, a desktop trash command (`trash` or `gio`), and a working graphical login environment. It downloads the sourced photograph only if missing and renders at 2880×1800 (16:10). The source composition is deliberately a desktop wallpaper, not a responsive web application. Use the browser page only as a rendering source. See `SOURCES.md` for provenance. Local photography and derived wallpapers are ignored by Git.

## Restore

Record the old background path using `readlink -f ~/.local/state/omarchy/current/background` before applying (`omarchy theme bg current` prints only its display name). Restore that path with `omarchy theme bg set /path/to/previous/image`.

For branding, use the printed backup directory's `manifest.json`: move each current path listed in `changed` to the desktop trash, then copy each path listed in `saved` back from the backup to the matching path under `home`, preserving symlinks (`cp -a`). Paths absent from `saved` did not previously exist. Restore the most recent applicable backup first. Review any edits made after installation before restoring; backups never expire automatically.

The About menu uses its own logo argument so the existing fastfetch Rocket logo stays unchanged in ordinary terminals. The screensaver reads Omarchy's supported `branding/screensaver.txt` override.
