#!/bin/bash
#
# Sync conductor commands from upstream repository
#
# Usage:
#   ./scripts/sync-from-upstream.sh
#
# This script:
# 1. Updates the upstream git submodule to the latest version
# 2. Re-converts all TOML commands to Markdown format

set -e

# Change to plugin root directory
cd "$(dirname "$0")/.."

echo "=== Conductor Plugin Sync ==="
echo ""

# Update submodule
echo "Updating upstream submodule..."
git submodule update --remote upstream
echo ""

# Get the current upstream version
UPSTREAM_VERSION=$(cd upstream && git describe --tags 2>/dev/null || git rev-parse --short HEAD)
echo "Upstream version: $UPSTREAM_VERSION"
echo ""

# Run the converter
echo "Converting commands..."
python3 scripts/convert-commands.py

echo ""
echo "=== Sync Complete ==="
echo ""
echo "Next steps:"
echo "  1. Review changes: git diff commands/"
echo "  2. Test the plugin: claude --plugin-dir ."
echo "  3. Commit changes if everything works"
