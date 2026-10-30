# BMad Framework — Installation & Configuration

## Overview

BMad (BMad Method Agent Development) is a structured methodology for orchestrating
AI agents with role-based personas, task checklists, and iterative refinement workflows.

## Prerequisites

- Node.js 18+ with npm/npx available
- An AI coding agent (Claude Code, Codex, etc.)

## Installation

Run the following command in the project root:

```bash
npx bmad-method install
```

This installs the BMad method structure into the current project. The installer is
interactive and will guide through the initial configuration.

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
.bmad-method/          or    .bmad/
├── agents/            # Agent persona definitions
├── checklists/        # Task validation checklists
├── tasks/             # Task templates
└── templates/         # Output templates
```

To verify programmatically:
- Check if `.bmad-method/` or `.bmad/` directory exists
- Check if it contains at least an `agents/` subdirectory

## Post-Installation

Inform the user:
- Agent personas are available and ready for use
- Task templates can be customized for their specific workflows
- Checklists provide validation gates between task stages

## Troubleshooting

| Issue | Resolution |
|-------|-----------|
| `npx: command not found` | Install Node.js 18+ |
| `bmad-method` package not found | Check npm registry availability, verify network |
| Permission denied during install | Run in a directory where the user has write access |
| Partial installation | Remove the `.bmad-method/` directory and re-run |
