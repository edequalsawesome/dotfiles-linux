# Linux dotfiles agent instructions

This repository owns personal Arch Linux and Omarchy user configuration. Read `README.md`, `docs/design.md`, and `install.sh` before changing installation behavior.

Preserve Omarchy integration in `ghostty/config` and the small user-override pattern in `hypr/`. Never add credentials, SSH private material, session state, or files copied wholesale from `~/.codex` or `~/.claude`.

Use `apply_patch` for edits. Run `./tests/install-test.sh`, Bash syntax checks, and the relevant application's configuration check before committing. Changes are approved for direct commits to `main` after verification; push task-owned commits and verify the remote contains them.
