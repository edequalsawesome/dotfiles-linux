# Source local secrets (not in dotfiles repo)
[[ -f ~/.secrets ]] && source ~/.secrets
[[ -f "$HOME/.cargo/env" ]] && . "$HOME/.cargo/env"
