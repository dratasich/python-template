#!/bin/bash
set -e

echo "Installing Python dependencies..."
uv sync

echo "Installing pre-commit hooks..."
uv run pre-commit install

echo "Setting up opencode configuration..."
git clone https://github.com/dratasich/opencode-config.git /tmp/opencode-config
mkdir -p ~/.config/opencode
cp -r /tmp/opencode-config/* ~/.config/opencode/
rm -rf /tmp/opencode-config

echo "devcontainer setup complete!"
