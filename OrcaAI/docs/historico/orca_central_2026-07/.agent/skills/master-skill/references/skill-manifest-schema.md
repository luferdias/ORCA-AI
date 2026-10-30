# External Skill Manifest Schema

## What Makes a Valid Skill

A valid external skill is a directory containing a `SKILL.md` file with proper YAML
frontmatter that includes both `name` and `description` fields.

## Required Structure

```
skill-name/
├── SKILL.md          # REQUIRED — Skill definition with YAML frontmatter
├── scripts/          # Optional — Executable helper scripts
├── references/       # Optional — Additional documentation
└── assets/           # Optional — Templates, icons, fonts
```

## SKILL.md Frontmatter Requirements

The file must begin with YAML frontmatter delimited by `---`:

```yaml
---
name: skill-name          # Required. Lowercase with hyphens.
description: >            # Required. What the skill does and when to use it.
  Short description of what the skill does.
---
```

Both `name` and `description` are required. If either is missing, the skill is invalid
and will be skipped during loading (with a warning).

## Validation Rules

When scanning a skills directory, apply these checks in order:

1. Entry is a directory (not a file) — skip files silently.
2. Directory name does not start with `.` — skip hidden directories silently.
3. `SKILL.md` exists inside the directory — skip without it (count as "ignored").
4. YAML frontmatter is parseable — skip with warning if malformed.
5. `name` field is present — skip with warning if missing.
6. `description` field is present — skip with warning if missing.

Skills passing all checks are valid and included in the loaded set.
