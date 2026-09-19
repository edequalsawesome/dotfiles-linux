#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
target_home="$HOME"

if [[ "${1:-}" == "--home" ]]; then
  [[ $# -eq 2 ]] || { echo "Usage: $0 [--home PATH]" >&2; exit 2; }
  target_home="$2"
elif [[ $# -ne 0 ]]; then
  echo "Usage: $0 [--home PATH]" >&2
  exit 2
fi

backup_and_link() {
  local source="$repo_dir/$1"
  local target="$target_home/$2"

  [[ -e "$source" ]] || { echo "Missing source: $source" >&2; exit 1; }
  mkdir -p "$(dirname "$target")"

  if [[ -L "$target" && "$(readlink "$target")" == "$source" ]]; then
    return
  fi

  if [[ -e "$target" && ! -L "$target" ]]; then
    local backup="$target.bak"
    if [[ -e "$backup" || -L "$backup" ]]; then
      backup="$target.bak.$(date +%Y%m%d%H%M%S)"
    fi
    mv "$target" "$backup"
    echo "Backed up $target -> $backup"
  elif [[ -L "$target" ]]; then
    rm "$target"
  fi

  ln -s "$source" "$target"
  echo "Linked $target -> $source"
}

while IFS=: read -r source target; do
  backup_and_link "$source" "$target"
done <<'LINKS'
zsh/.zshrc:.zshrc
zsh/.zprofile:.zprofile
zsh/.zshenv:.zshenv
tmux/.tmux.conf:.tmux.conf
tmux/prefix-swap.sh:.config/tmux/prefix-swap.sh
git/.gitconfig:.gitconfig
git/.gitconfig-a8c:.gitconfig-a8c
ghostty/config:.config/ghostty/config
fastfetch/config.jsonc:.config/fastfetch/config.jsonc
fastfetch/config-tmux.jsonc:.config/fastfetch/config-tmux.jsonc
fastfetch/rocket.png:.config/fastfetch/rocket.png
fastfetch/rocket.txt:.config/fastfetch/rocket.txt
starship/starship.toml:.config/starship.toml
zellij/config.kdl:.config/zellij/config.kdl
zellij/layouts/default.kdl:.config/zellij/layouts/default.kdl
zellij/layouts/vertical.kdl:.config/zellij/layouts/vertical.kdl
hypr/input.lua:.config/hypr/input.lua
hypr/bindings.lua:.config/hypr/bindings.lua
hypr/hyprland.lua:.config/hypr/hyprland.lua
bin/claude-session:bin/claude-session
LINKS

echo "Linux dotfiles installed for $target_home"
