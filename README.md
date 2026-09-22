# dotfiles-linux

Personal Arch Linux and Omarchy configuration. The macOS configuration remains in [`edequalsawesome/dotfiles`](https://github.com/edequalsawesome/dotfiles).

The optional [Malarchy desktop layer](malarchy/README.md) adds Catppuccin-compatible collage branding: “Listen here, jack. It’s your computer.”

Malarchy development continues in the dedicated private [edequalsawesome/malarchy](https://github.com/edequalsawesome/malarchy) repository, including the artwork backup. The copy here is the initial public source snapshot.

## Install

```bash
gh repo clone edequalsawesome/dotfiles-linux ~/dotfiles
~/dotfiles/install.sh
```

The installer backs up ordinary destination files with a `.bak` suffix before creating absolute symlinks. Running it again is safe.

Useful packages for the included configuration:

```bash
omarchy-pkg-add zsh zsh-autosuggestions zsh-syntax-highlighting zellij ttf-hack-nerd
```

The configuration degrades gracefully when optional commands such as `zellij`, `fzf`, `fnm`, `mole`, `fastfetch`, or `starship` are absent. Oh My Zsh is supported but not required.

## Omarchy-specific configuration

- `hypr/` contains personal Hyprland overrides for the MacBook keyboard, trackpad, keyboard backlight, and scratchpad behavior.
- `ghostty/config` keeps Omarchy's dynamic theme include and the `epoll` backend workaround.
- `tmux/`, `fastfetch/`, `starship/`, and `zellij/` contain terminal preferences.

Root-owned machine settings are intentionally outside the installer. On this 2017 MacBook Pro those currently include `mbpfan`, the `systemd-logind` lid override, Broadcom firmware, the NVMe suspend override, and the MacBook Pro audio DKMS module.

The Apple SPI keyboard reports vendor `0x0000` on this machine, so libinput 1.31.3 misses its stock internal-keyboard rule. To make touchpad disable-while-typing pair with the built-in keyboard, install the narrow override in [`libinput/local-overrides.quirks`](libinput/local-overrides.quirks) as `/etc/libinput/local-overrides.quirks`, then log out and back in. Keep any other local rules if the destination already exists.

## Test

```bash
./tests/install-test.sh
bash -n install.sh tests/install-test.sh bin/claude-session
```
