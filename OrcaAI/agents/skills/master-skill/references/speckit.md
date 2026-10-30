# SpecKit — Installation & Configuration

## Overview

SpecKit is a specification-driven development framework for AI agents. It uses
structured specifications as the primary artifact that drives agent behavior,
code generation, and validation. Powered by the `specify-cli` command-line tool.

## Prerequisites

- Python 3.10+ installed
- `uv` package manager (recommended) or `pip`
- Git (for repository access)
- An AI coding agent (Claude Code, Codex, etc.)

## Installation

### Using uv (recommended)

```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
```

### Using pip (fallback)

```bash
pip install git+https://github.com/github/spec-kit.git --break-system-packages
```

### Installing uv (if not available)

```bash
# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or via pip
pip install uv --break-system-packages
```

## Verifying Installation

After installation, verify the CLI is available:

```bash
specify --version
```

Or check for installed workspace markers:

```
.speckit/              or    specs/
├── specs/             # Specification files
├── templates/         # Spec templates
└── config/            # Framework configuration
```

To verify programmatically:
- Check if `specify` command is available in PATH
- Or check if `.speckit/` directory exists in the project

## Post-Installation

Initialize a spec workspace in the project:

```bash
specify init
```

This creates the initial directory structure for specifications.

Inform the user:
- Spec templates are available for creating structured specifications
- The `specify` CLI provides validation, generation, and management commands
- Specs drive the agent's behavior — they are the primary working artifact

## Troubleshooting

| Issue | Resolution |
|-------|-----------|
| `uv: command not found` | Install uv: `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Git clone fails within install | Check network access to github.com |
| `specify: command not found` after install | Restart terminal or add `~/.local/bin` to PATH |
| Python version too old | Upgrade to Python 3.10+ |
| `pip install` fails with resolver | Use `uv` instead — it handles dependencies better |
