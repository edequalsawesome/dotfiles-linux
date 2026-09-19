#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
test_home="$(mktemp -d)"
trap 'rm -rf "$test_home"' EXIT

printf 'keep me\n' > "$test_home/.zshrc"

"$repo_dir/install.sh" --home "$test_home"

assert_link() {
  local target="$1"
  local source="$2"
  test -L "$target"
  test "$(readlink "$target")" = "$source"
  test -e "$target"
}

assert_link "$test_home/.zshrc" "$repo_dir/zsh/.zshrc"
assert_link "$test_home/.tmux.conf" "$repo_dir/tmux/.tmux.conf"
assert_link "$test_home/.gitconfig" "$repo_dir/git/.gitconfig"
assert_link "$test_home/.config/ghostty/config" "$repo_dir/ghostty/config"
assert_link "$test_home/.config/hypr/input.lua" "$repo_dir/hypr/input.lua"
assert_link "$test_home/.config/starship.toml" "$repo_dir/starship/starship.toml"

test "$(cat "$test_home/.zshrc.bak")" = "keep me"

backup_count_before="$(find "$test_home" -name '*.bak' | wc -l)"
"$repo_dir/install.sh" --home "$test_home"
backup_count_after="$(find "$test_home" -name '*.bak' | wc -l)"
test "$backup_count_before" = "$backup_count_after"

find "$test_home" -type l -print0 | while IFS= read -r -d '' link; do
  test -e "$link"
done

echo "install-test: PASS"
