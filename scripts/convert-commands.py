#!/usr/bin/env python3
"""
Convert Gemini CLI conductor TOML commands to Claude Code Markdown format.

Usage:
    python3 scripts/convert-commands.py

This script reads TOML files from upstream/commands/conductor/ and converts
them to Claude Code's Markdown command format in commands/
"""

import re
from pathlib import Path

# Try tomllib (Python 3.11+) or fall back to tomli
try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib
    except ImportError:
        print("Error: Please install tomli: uv pip install tomli")
        exit(1)


def adapt_for_claude_code(prompt: str) -> str:
    """Apply adaptations to convert Gemini-specific content to Claude Code."""

    # Replace Gemini extension paths with Claude plugin paths
    prompt = prompt.replace(
        "~/.gemini/extensions/conductor/templates/",
        "${CLAUDE_PLUGIN_ROOT}/templates/"
    )

    # Replace .geminiignore with .claudeignore
    prompt = prompt.replace(".geminiignore", ".claudeignore")

    # Remove Gemini CLI specific instructions
    prompt = prompt.replace(
        'Gemini CLI built-in option "Modify with external editor" (if present), or with your favorite external editor',
        "your favorite external editor"
    )

    return prompt


def toml_to_markdown(toml_path: Path) -> str:
    """Convert a TOML command file to Claude Code Markdown format."""

    with open(toml_path, "rb") as f:
        data = tomllib.load(f)

    description = data.get("description", "No description provided")
    prompt = data.get("prompt", "")

    # Clean up the prompt
    prompt = prompt.strip()

    # Apply Claude Code adaptations
    prompt = adapt_for_claude_code(prompt)

    # Build the markdown content
    markdown = f"""---
description: {description}
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

{prompt}
"""

    return markdown


def convert_all_commands(
    source_dir: Path = Path("upstream/commands/conductor"),
    target_dir: Path = Path("commands")
):
    """Convert all TOML commands to Markdown."""

    # Ensure target directory exists
    target_dir.mkdir(parents=True, exist_ok=True)

    # Find all TOML files
    toml_files = list(source_dir.glob("*.toml"))

    if not toml_files:
        print(f"No TOML files found in {source_dir}")
        return

    print(f"Found {len(toml_files)} command(s) to convert:")

    for toml_path in sorted(toml_files):
        # Convert filename (e.g., newTrack.toml -> newTrack.md)
        md_name = toml_path.stem + ".md"
        md_path = target_dir / md_name

        try:
            markdown = toml_to_markdown(toml_path)
            md_path.write_text(markdown)
            print(f"  ✓ {toml_path.name} -> {md_name}")
        except Exception as e:
            print(f"  ✗ {toml_path.name}: {e}")

    print("\nConversion complete!")


if __name__ == "__main__":
    # Run from the plugin root directory
    script_dir = Path(__file__).parent
    plugin_root = script_dir.parent

    # Change to plugin root for relative paths to work
    import os
    os.chdir(plugin_root)

    convert_all_commands()
