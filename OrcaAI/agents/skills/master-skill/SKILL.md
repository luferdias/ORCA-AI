---
name: master-skill
description: >
  Orchestrator for AI agent development environments. Installs and configures agent
  frameworks (BMad, SpecKit, Antigravity Kit), loads external skill sets, and prepares
  the full working context in a single command. Activated EXCLUSIVELY by the
  /master-skill command — never triggers automatically. Use this skill whenever the
  user types /master-skill, /master-skill init, or /master-skill reset. Also trigger
  when the user mentions setting up an agent development environment, wants to install
  or switch agent frameworks, needs to load external skills into their session, or asks
  about configuring their AI coding workspace. Trigger phrases include: "configure my
  agent environment", "set up BMad", "load my skills", "switch framework",
  "reconfigure master-skill", "install speckit", "install antigravity kit".
---

# Master-Skill — Agent Environment Orchestrator

## Purpose

Single entry point to configure and bootstrap an AI agent development environment.
One command sets up everything: the chosen agent framework is installed, external skills
are loaded into context, and the session is ready for productive work.

## Activation Rule

This skill is command-gated. It activates ONLY when the user explicitly calls one of:

- `/master-skill` — Main execution (loads config, installs framework, loads skills)
- `/master-skill init` — First-run interactive setup
- `/master-skill reset` — Reconfigure from scratch

Do not run any setup, installation, or configuration unless one of these commands is
called. If the user asks about the skill without invoking the command, explain what it
does and how to use it — but do not execute it.

---

## Subcommands

### `/master-skill init`

First-run interactive setup. Guides the user through two questions, one at a time.
Wait for each answer before proceeding.

**Question 1 — Agent selection:**
Ask which AI coding agent the user is working with. Present these options:

- Claude Code
- Google Antigravity
- Codex (OpenAI)
- Other (let the user specify)

This determines where the config file is saved and any agent-specific behavior.

**Question 2 — External skills path:**
Ask for the path to the directory containing external skills. Validate before saving:

- Confirm the path exists and is a readable directory.
- Confirm it contains at least one subdirectory com a `SKILL.md` file.
- If validation fails, report the issue clearly and ask for a corrected path.
- Do NOT proceed with an invalid path.

**Save configuration:**
After collecting both answers, save the config as a `.master-skill-config.json` file
inside the agent's skill folder. The exact location depends on the selected agent:

| Agent              | Config location                                              |
|--------------------|--------------------------------------------------------------|
| Claude Code        | `~/.claude/skills/.master-skill-config.json`                 |
| Google Antigravity | `~/.antigravity/skills/.master-skill-config.json`            |
| Codex              | `~/.codex/skills/.master-skill-config.json`                  |
| Other              | Ask the user for the skill folder path, then save inside it  |

Config file format:

```json
{
  "schema_version": "1.0",
  "agent": "claude-code",
  "skills_path": "/absolute/path/to/skills",
  "framework": null,
  "created_at": "2026-03-27T10:00:00Z",
  "updated_at": "2026-03-27T10:00:00Z"
}
```

The `framework` field starts as `null` and is populated when the user installs a
framework via the main `/master-skill` command.

After saving, confirm to the user:

```
✅ Configuração salva com sucesso.
   Agente:      Claude Code
   Skills path: /path/to/skills
   Config:      ~/.claude/skills/.master-skill-config.json

   Execute /master-skill para instalar um framework e carregar suas skills.
```

---

### `/master-skill reset`

Deletes or ignores the existing config and re-runs the full `/master-skill init` flow.
Ask the user to confirm before deleting the existing configuration.

---

### `/master-skill` (main execution)

This is the primary command. Follow this sequence:

#### Step 1 — Locate and load configuration

Search for `.master-skill-config.json` in these locations (in order):

1. Current working directory
2. `~/.claude/skills/`
3. `~/.antigravity/skills/`
4. `~/.codex/skills/`

If no config is found, inform the user and run `/master-skill init` automatically.

If the config file exists, validate it using `scripts/validate_config.py` or by
checking these rules inline:

- `schema_version` must be `"1.0"` (or a supported version).
- `agent` must be present and non-empty.
- `skills_path` must be present and point to an existing directory.

If validation fails, report what's wrong and offer to run `/master-skill reset`.

#### Step 2 — Framework installation

Check the `framework` field in config:

- **If `null` (no framework chosen yet):** Ask the user which framework to install.
  Present the options and install the chosen one.
- **If already set:** Check if the framework is still installed (look for marker
  directories/files). If installed, skip. If missing, re-install.

Read the corresponding reference file for installation instructions:

| Framework       | Reference file              | Install command                                                                      |
|-----------------|-----------------------------|---------------------------------------------------------------------------------------|
| BMad            | `references/bmad.md`        | `npx bmad-method install`                                                             |
| Antigravity Kit | `references/antigravity.md` | `npx @vudovn/ag-kit init`                                                             |
| SpecKit         | `references/speckit.md`     | `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git`       |

After successful installation, update the config file:
- Set `framework` to the chosen value.
- Update `updated_at` timestamp.

#### Step 3 — Load external skills

Read the directory at `config.skills_path`. Use `scripts/scan_skills.py` to validate
and catalog the skills, or perform the validation inline:

1. List all subdirectories (skip hidden directories starting with `.`).
2. For each subdirectory, check for a `SKILL.md` file.
3. If `SKILL.md` exists, read its YAML frontmatter to extract `name` and `description`.
4. A directory without `SKILL.md` is not a valid skill — skip it silently.
5. A `SKILL.md` without `name` or `description` in frontmatter is invalid — skip with
   a warning.

Present a summary to the user:

```
Skills carregadas:
  1. nome-da-skill — Descrição curta
  2. outra-skill   — Descrição curta
  ...

Total: N skills válidas de /path/to/skills
Ignoradas: M diretórios sem SKILL.md válido
```

#### Step 4 — Confirm ready state

Print the final status report:

```
✅ master-skill — Ambiente pronto

   Framework:  BMad (instalado)
   Agente:     Claude Code
   Skills:     12 carregadas de /path/to/skills
   Config:     ~/.claude/skills/.master-skill-config.json

   Comandos disponíveis:
     /master-skill        — Recarregar ambiente
     /master-skill reset  — Reconfigurar do zero
```

---

## Error Handling

Report errors immediately and clearly. Do not silently fail.

| Scenario                              | Response                                              |
|---------------------------------------|-------------------------------------------------------|
| Config has unknown `schema_version`   | Warn about version mismatch, offer `/master-skill reset` |
| `skills_path` no longer exists        | Report the issue, ask for updated path                |
| Framework install command fails       | Show the error output, suggest manual installation    |
| A skill dir has no `SKILL.md`         | Skip silently, count in "ignored" summary             |
| A `SKILL.md` has malformed frontmatter| Skip with warning, count in "ignored" summary         |
| Config JSON is corrupted              | Report corruption, offer `/master-skill reset`        |
| Permission denied on skills_path      | Report permission issue, suggest `chmod` or new path  |
| `npx` or `uv` not found              | Explain what's needed and how to install it            |

---

## Important Constraints

- Never modify files inside the user's skills directory — treat it as read-only.
- Never execute scripts from external skills automatically — only read metadata.
- Never store sensitive information (tokens, passwords) in the config file.
- The config file is plain JSON with no executable content.
- The config file is saved inside the agent's skill folder, not in the project root.

---

## Reference Files

Read the appropriate reference file before attempting any framework installation:

- `references/bmad.md` — BMad installation, directory structure, verification
- `references/speckit.md` — SpecKit installation and workspace setup
- `references/antigravity.md` — Antigravity Kit installation and configuration
- `references/skill-manifest-schema.md` — What makes a valid external skill

These files contain the detailed steps, marker files for detecting existing installs,
and troubleshooting guidance. Always read the relevant file before running install
commands — do not rely on the summary table above alone.
