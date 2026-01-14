# Claude Code Conductor Plugin

A Claude Code plugin that implements **Context-Driven Development**: Spec → Plan → Implement.

This plugin is adapted from [gemini-cli-extensions/conductor](https://github.com/gemini-cli-extensions/conductor) for use with Claude Code.

## Installation

```bash
# Load the plugin locally
claude --plugin-dir /path/to/claude-code-conductor

# Or install permanently (coming soon)
# claude plugin install ./claude-code-conductor
```

## Commands

| Command | Description |
|---------|-------------|
| `/conductor:setup` | Initialize project context (run once per project) |
| `/conductor:newTrack` | Create a new feature/bug track with specs and plan |
| `/conductor:implement` | Execute the planned tasks |
| `/conductor:status` | Display current progress overview |
| `/conductor:revert` | Undo work by logical units (tasks, phases, tracks) |

## Workflow

1. **Setup** - Run `/conductor:setup` to initialize your project context
2. **Plan** - Use `/conductor:newTrack` to define a feature with specifications
3. **Implement** - Execute with `/conductor:implement`
4. **Monitor** - Check progress with `/conductor:status`

## Generated Structure

After setup, conductor creates:

```
conductor/
├── product.md            # Product description and goals
├── product-guidelines.md # Development guidelines
├── tech-stack.md         # Technology choices
├── workflow.md           # Development workflow
├── tracks.md             # Master list of all tracks
├── code_styleguides/     # Language-specific style guides
└── tracks/
    └── <track_id>/
        ├── spec.md       # Feature specification
        ├── plan.md       # Implementation plan
        └── metadata.json # Track metadata
```

## Syncing with Upstream

This plugin tracks the upstream conductor repository as a git submodule. To update:

```bash
cd claude-code-conductor
./scripts/sync-from-upstream.sh
```

## Directory Structure

```
claude-code-conductor/
├── .claude-plugin/
│   └── plugin.json       # Claude Code plugin manifest
├── commands/             # Converted markdown commands
├── scripts/
│   ├── convert-commands.py    # TOML → Markdown converter
│   └── sync-from-upstream.sh  # Update from upstream
├── templates -> upstream/templates  # Symlink to templates
└── upstream/             # Git submodule (original conductor repo)
```

## License

Apache-2.0 (same as upstream conductor)
