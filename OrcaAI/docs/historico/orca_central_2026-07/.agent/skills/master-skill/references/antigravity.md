# Antigravity Kit — Installation & Configuration

## Overview

Antigravity Kit provides workspace templates, agent configuration scaffolding, and
integration points for building AI-powered development workflows within the Google
Antigravity ecosystem and compatible agents.

## Prerequisites

- Node.js 18+ with npm/npx available
- An AI coding agent (Google Antigravity, Claude Code, etc.)

## Installation

Run the following command in the project root:

```bash
npx @vudovn/ag-kit init
```

This initializes the Antigravity Kit workspace structure in the current project.
The command is interactive and will ask about workspace preferences.

If `npx` is not available, install Node.js first:
```bash
# Ubuntu/Debian
sudo apt-get install -y nodejs npm

# macOS
brew install node
```

## Verifying Installation

After installation, check for these marker files and directories:

```
.ag-kit/              or    .antigravity/
├── agents/           # Agent definitions and configs
├── workflows/        # Workflow templates
├── config/           # Environment configuration
└── package.json      # Kit metadata
```

To verify programmatically:
- Check if `.ag-kit/` or `.antigravity/` directory exists
- Check if `package.json` exists inside the kit directory

## Agent-Specific Notes

**Google Antigravity (native):**
- The kit integrates natively — workspace settings are auto-detected
- Full feature set available

**Claude Code / Codex / Other:**
- Core templates and workflows work across all agents
- Some Antigravity-specific integrations may not be available
- Agent definitions may need manual adjustment

## Troubleshooting

| Issue | Resolution |
|-------|-----------|
| `npx: command not found` | Install Node.js 18+ |
| `@vudovn/ag-kit` not found | Check npm registry, verify network access |
| Permission denied | Run in a writable directory |
| Init hangs or times out | Check network connectivity to npm registry |
