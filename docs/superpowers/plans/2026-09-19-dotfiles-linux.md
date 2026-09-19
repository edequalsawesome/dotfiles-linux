# Linux Dotfiles Repository Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build, publish, and activate a standalone Arch/Omarchy dotfiles repository without regressing the working desktop configuration.

**Architecture:** A small Bash installer links repository-owned user configuration into `$HOME`, backing up ordinary files first. Shell tests exercise installation in a temporary home. Root-owned system configuration remains documented and outside the installer.

**Tech Stack:** Bash, Git, Hyprland Lua configuration, Ghostty, tmux, zsh, Starship, Fastfetch, Zellij.

**Spec:** `docs/design.md`

## Global Constraints

- Repository name is `dotfiles-linux` and visibility is public.
- The macOS `dotfiles` repository remains unchanged.
- Preserve the current working Omarchy Ghostty and Hyprland behavior.
- Never copy credentials, SSH configuration, tokens, or agent runtime state.
- Installation must be idempotent and back up ordinary destination files.

## Review Focus

- Existing ordinary files must be backed up rather than overwritten.
- A second installer run must not create additional backups or fail.
- Missing optional source files must not leave broken links.
- All installed links must resolve into the active repository checkout.
- Ghostty must retain the Omarchy theme include, epoll backend, and CSI-u Shift+Enter binding.

---

### Task 1: Repository content and installer

**Files:**
- Create: `install.sh`, `tests/install-test.sh`, `README.md`
- Create: configuration directories copied from reviewed Linux and live Omarchy sources

**Interfaces:**
- Produces: `install.sh [--home PATH]`, an idempotent symlink installer.

- [ ] Write `tests/install-test.sh` covering backup, link targets, missing optional sources, and repeated installation.
- [ ] Run the test and verify it fails because `install.sh` is absent.
- [ ] Add the minimal installer and reviewed configuration files.
- [ ] Run the test and configuration syntax checks.
- [ ] Commit the repository contents.

### Task 2: Publish and activate

**Files:**
- Modify: live paths under `~` through the tested installer.

**Interfaces:**
- Consumes: Task 1's tested repository and installer.
- Produces: public GitHub repository and verified live symlinks.

- [ ] Create `edequalsawesome/dotfiles-linux` and push `main`.
- [ ] Preserve the old `~/dotfiles` checkout under a timestamped backup name.
- [ ] Clone the new repository to `~/dotfiles` and run its installer.
- [ ] Verify every link, Ghostty configuration, Hyprland configuration, and remote branch.
