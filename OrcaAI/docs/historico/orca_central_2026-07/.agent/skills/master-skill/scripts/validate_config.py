#!/usr/bin/env python3
"""
master-skill config validator.

Validates .master-skill-config.json structure, content, and location.
Returns exit code 0 if valid, 1 if invalid (with diagnostic output).

Usage:
    python validate_config.py <config_path>
    python validate_config.py --find    # Auto-locate config file
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

SUPPORTED_SCHEMA_VERSIONS = ["1.0"]
REQUIRED_FIELDS = ["schema_version", "agent", "skills_path"]
CONFIG_FILENAME = ".master-skill-config.json"

# Agent-specific config locations (in search order)
AGENT_CONFIG_PATHS = [
    Path.home() / ".claude" / "skills" / CONFIG_FILENAME,
    Path.home() / ".antigravity" / "skills" / CONFIG_FILENAME,
    Path.home() / ".codex" / "skills" / CONFIG_FILENAME,
]

KNOWN_AGENTS = ["claude-code", "antigravity", "codex"]
KNOWN_FRAMEWORKS = ["bmad", "speckit", "antigravity-kit"]


def find_config() -> str | None:
    """Search for config file in standard locations.

    Search order:
      1. Current working directory
      2. Agent-specific skill folders (~/.claude/skills/, etc.)
    """
    # Check current directory first
    local = Path.cwd() / CONFIG_FILENAME
    if local.is_file():
        return str(local)

    # Check agent-specific locations
    for path in AGENT_CONFIG_PATHS:
        if path.is_file():
            return str(path)

    return None


def validate_config(config_path: str) -> tuple[bool, list[str], dict | None]:
    """Validate a master-skill config file.

    Returns:
        (is_valid, list_of_issues, parsed_config_or_none)
    """
    issues = []

    if not os.path.isfile(config_path):
        return False, [f"Config file not found: {config_path}"], None

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        return False, [f"Invalid JSON: {e}"], None
    except PermissionError:
        return False, [f"Permission denied: {config_path}"], None

    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in config:
            issues.append(f"Missing required field: '{field}'")

    if issues:
        return False, issues, None

    # Validate schema_version
    if config["schema_version"] not in SUPPORTED_SCHEMA_VERSIONS:
        issues.append(
            f"Unsupported schema_version: '{config['schema_version']}'. "
            f"Supported: {SUPPORTED_SCHEMA_VERSIONS}"
        )

    # Validate agent
    agent = config["agent"].lower().strip()
    if agent not in KNOWN_AGENTS:
        issues.append(
            f"Unknown agent: '{config['agent']}'. "
            f"Known: {KNOWN_AGENTS}. May still work if custom."
        )

    # Validate skills_path
    skills_path = config["skills_path"]
    if not os.path.isabs(skills_path):
        issues.append(f"skills_path should be absolute: '{skills_path}'")
    elif not os.path.isdir(skills_path):
        issues.append(f"skills_path directory not found: '{skills_path}'")

    # Validate framework (optional field, can be null)
    framework = config.get("framework")
    if framework is not None:
        if framework.lower().strip() not in KNOWN_FRAMEWORKS:
            issues.append(
                f"Unknown framework: '{framework}'. "
                f"Known: {KNOWN_FRAMEWORKS}. May still work if custom."
            )

    # Validate timestamps if present
    for ts_field in ["created_at", "updated_at"]:
        if ts_field in config:
            try:
                datetime.fromisoformat(config[ts_field].replace("Z", "+00:00"))
            except (ValueError, AttributeError):
                issues.append(
                    f"Invalid timestamp in '{ts_field}': '{config[ts_field]}'"
                )

    # Determine validity
    critical = [
        i for i in issues
        if "Missing required" in i
        or "Invalid JSON" in i
        or "Unsupported schema" in i
    ]

    if critical:
        return False, issues, config
    elif issues:
        return True, issues, config  # Valid with warnings
    else:
        return True, [], config


def main():
    # Handle --find flag
    if len(sys.argv) >= 2 and sys.argv[1] == "--find":
        found = find_config()
        if found:
            print(found)
            sys.exit(0)
        else:
            print("No config file found in any standard location.")
            sys.exit(1)

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python validate_config.py <config_path>")
        print("  python validate_config.py --find")
        sys.exit(1)

    config_path = sys.argv[1]
    is_valid, issues, config = validate_config(config_path)

    if is_valid and not issues:
        print(f"✅ Config válido: {config_path}")
        if config:
            print(f"   Agente:     {config.get('agent', '?')}")
            print(f"   Framework:  {config.get('framework', 'não configurado')}")
            print(f"   Skills:     {config.get('skills_path', '?')}")
        sys.exit(0)
    elif is_valid and issues:
        print(f"⚠️  Config válido (com avisos): {config_path}")
        for issue in issues:
            print(f"   ⚠️  {issue}")
        sys.exit(0)
    else:
        print(f"❌ Config inválido: {config_path}")
        for issue in issues:
            print(f"   ❌ {issue}")
        sys.exit(1)


if __name__ == "__main__":
    main()
