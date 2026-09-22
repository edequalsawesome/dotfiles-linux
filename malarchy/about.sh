#!/usr/bin/env bash
set -euo pipefail
fastfetch --logo "$HOME/.config/omarchy/branding/about.txt" --logo-type file
printf '\nPress any key to close.\n'
read -rsn1 || true
