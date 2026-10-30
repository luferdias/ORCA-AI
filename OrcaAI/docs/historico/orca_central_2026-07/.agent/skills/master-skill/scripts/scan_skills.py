#!/usr/bin/env python3
"""
master-skill external skill scanner.

Scans a directory for valid skills (directories containing SKILL.md with
proper YAML frontmatter) and outputs a JSON catalog.

Usage:
    python scan_skills.py /path/to/skills/directory
"""

import json
import os
import re
import sys


def parse_yaml_frontmatter(content: str) -> dict | None:
    """Extract YAML frontmatter from markdown content.

    Parses key: value pairs between --- delimiters.
    Handles multi-line values with > or | continuation.
    Returns None if no valid frontmatter found.
    """
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return None

    frontmatter = {}
    current_key = None
    current_value_lines = []

    for line in match.group(1).split("\n"):
        kv_match = re.match(r"^(\w[\w-]*)\s*:\s*(.*)", line)
        if kv_match:
            if current_key:
                frontmatter[current_key] = " ".join(current_value_lines).strip()
            current_key = kv_match.group(1)
            value = kv_match.group(2).strip()
            if value in (">", "|"):
                current_value_lines = []
            else:
                current_value_lines = [value]
        elif current_key and line.strip():
            current_value_lines.append(line.strip())

    if current_key:
        frontmatter[current_key] = " ".join(current_value_lines).strip()

    return frontmatter


def scan_skill(skill_dir: str) -> dict:
    """Scan a single skill directory and return its metadata."""
    result = {
        "path": os.path.abspath(skill_dir),
        "dir_name": os.path.basename(skill_dir),
        "has_scripts": os.path.isdir(os.path.join(skill_dir, "scripts")),
        "has_references": os.path.isdir(os.path.join(skill_dir, "references")),
    }

    skill_md = os.path.join(skill_dir, "SKILL.md")

    if not os.path.isfile(skill_md):
        result["status"] = "skipped"
        result["reason"] = "No SKILL.md found"
        return result

    try:
        with open(skill_md, "r", encoding="utf-8") as f:
            content = f.read()
    except PermissionError:
        result["status"] = "invalid"
        result["reason"] = "Permission denied reading SKILL.md"
        return result
    except UnicodeDecodeError:
        result["status"] = "invalid"
        result["reason"] = "SKILL.md is not valid UTF-8"
        return result

    frontmatter = parse_yaml_frontmatter(content)

    if frontmatter is None:
        result["status"] = "invalid"
        result["reason"] = "No YAML frontmatter in SKILL.md"
        return result

    if "name" not in frontmatter:
        result["status"] = "invalid"
        result["reason"] = "Missing 'name' in frontmatter"
        return result

    if "description" not in frontmatter:
        result["status"] = "invalid"
        result["reason"] = "Missing 'description' in frontmatter"
        return result

    result["status"] = "valid"
    result["name"] = frontmatter["name"]
    result["description"] = frontmatter["description"][:200]
    return result


def scan_directory(skills_path: str) -> dict:
    """Scan a directory for all valid skills."""
    catalog = {
        "skills_path": os.path.abspath(skills_path),
        "loaded": [],
        "skipped": [],
        "summary": {"total_dirs": 0, "valid": 0, "invalid": 0, "skipped": 0},
    }

    if not os.path.isdir(skills_path):
        catalog["error"] = f"Directory not found: {skills_path}"
        return catalog

    for entry in sorted(os.listdir(skills_path)):
        entry_path = os.path.join(skills_path, entry)

        if not os.path.isdir(entry_path):
            continue
        if entry.startswith("."):
            continue

        catalog["summary"]["total_dirs"] += 1
        result = scan_skill(entry_path)

        if result["status"] == "valid":
            catalog["loaded"].append(result)
            catalog["summary"]["valid"] += 1
        elif result["status"] == "invalid":
            catalog["skipped"].append(result)
            catalog["summary"]["invalid"] += 1
        else:
            catalog["skipped"].append(result)
            catalog["summary"]["skipped"] += 1

    return catalog


def main():
    if len(sys.argv) < 2:
        print("Usage: python scan_skills.py <skills_directory>")
        sys.exit(1)

    catalog = scan_directory(sys.argv[1])
    print(json.dumps(catalog, indent=2, ensure_ascii=False))
    sys.exit(1 if "error" in catalog else 0)


if __name__ == "__main__":
    main()
