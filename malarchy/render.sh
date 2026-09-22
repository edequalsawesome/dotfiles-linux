#!/usr/bin/env bash
# Produce a local 2880x1800 wallpaper. Photography is never staged for publication.
set -euo pipefail
asset_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
command -v chromium >/dev/null || { echo 'Chromium is required to render the wallpaper.' >&2; exit 1; }
command -v magick >/dev/null || { echo 'ImageMagick is required to record image provenance.' >&2; exit 1; }
if command -v trash >/dev/null; then
  trash_command=(trash)
elif command -v gio >/dev/null; then
  trash_command=(gio trash)
else
  echo 'A desktop trash command (trash or gio) is required for profile cleanup.' >&2
  exit 1
fi
mkdir -p "$asset_dir/local"
if [[ ! -s "$asset_dir/local/sudeikis-snl.jpg" ]]; then
  curl --fail --location --proto '=https' --max-time 60 \
    'https://www.thedailybeast.com/resizer/v2/XYXCRLO2BZKIXJXCKI77XTF7PA.jpg?auth=85602b292e4a48ef984a0de5f7e062610609165f0b95c4a099d390626efb53e3&height=1087&smart=true&width=1933' \
    --output "$asset_dir/local/sudeikis-snl.jpg.part"
  mv "$asset_dir/local/sudeikis-snl.jpg.part" "$asset_dir/local/sudeikis-snl.jpg"
fi
render_profile="$(mktemp -d "$asset_dir/local/render-profile.XXXXXX")"
trap '"${trash_command[@]}" "$render_profile"' EXIT
chromium --headless --disable-gpu --no-first-run --no-default-browser-check \
  --user-data-dir="$render_profile" --hide-scrollbars --allow-file-access-from-files \
  --force-device-scale-factor=2 --window-size=1440,900 --timeout=15000 \
  --screenshot="$asset_dir/local/wallpaper.png" "file://$asset_dir/wallpaper.html"
test -s "$asset_dir/local/wallpaper.png"
magick "$asset_dir/local/wallpaper.png" -set comment \
  'Malarchy collage; source: SNL / NBC, Jason Sudeikis as Joe Biden, 2021-10-23; photo via https://www.thedailybeast.com/jason-sudeikis-returns-as-snls-fun-and-lucid-joe-biden/ ; composition: wallpaper.html; no AI-generated imagery; local personal-use artifact.' \
  "$asset_dir/local/wallpaper.png"
printf 'Rendered %s\n' "$asset_dir/local/wallpaper.png"
