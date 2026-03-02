#!/bin/bash
# Setup build toolchain for kramdown-rfc drafts

set -e

# Use chruby if available (macOS with ruby-install)
if [ -f /opt/homebrew/opt/chruby/share/chruby/chruby.sh ]; then
    source /opt/homebrew/opt/chruby/share/chruby/chruby.sh
    chruby ruby-3.3.0
elif [ -f /usr/local/opt/chruby/share/chruby/chruby.sh ]; then
    source /usr/local/opt/chruby/share/chruby/chruby.sh
    chruby ruby-3.3.0
fi

echo "Using ruby: $(ruby --version)"

echo "Installing kramdown-rfc..."
gem install kramdown-rfc

echo "Installing xml2rfc..."
pip3 install xml2rfc

echo "Installing pre-commit hook..."
ln -sf ../../pre-commit-hook.sh .git/hooks/pre-commit
chmod +x pre-commit-hook.sh

echo "Done. Run 'make all' to build the draft."
