# Linux Dotfiles Design

Create a public `edequalsawesome/dotfiles-linux` repository dedicated to Arch Linux and Omarchy. Keep the existing `dotfiles` repository focused on macOS.

The Linux repository owns portable shell and terminal preferences plus Omarchy user overrides. It installs through an idempotent script that backs up real destination files before replacing them with symlinks. It must preserve Omarchy's dynamic Ghostty theme and Hyprland integration, avoid credentials and agent runtime configuration, and document root-owned system settings instead of managing `/etc` directly.

The repository is cloned at `~/dotfiles` on Linux so existing shell paths remain valid. The previous macOS repository checkout is retained locally as a timestamped backup during migration.
