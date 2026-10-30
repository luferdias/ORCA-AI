---
name: check-sinapi-iopes-codes
description: Validate and cross-check SINAPI and IOPES codes in local budgets, spreadsheets, memorials, and procurement lists. Use when Codex needs to identify construction cost-reference codes, compare them against local SINAPI/IOPES bases, flag missing or inconsistent items, or prepare a review report from CSV, XLSX, TSV, or JSON files.
---

# Check SINAPI IOPES Codes

## Overview

Use this skill to audit `SINAPI` and `IOPES` codes in local files. Extract candidate codes from the user's material, validate them against local reference tables, and return an objective report with missing codes, ambiguous system attribution, and description or unit mismatches.

## Workflow

1. Identify the input files.
2. Confirm whether the user already has local exported bases for `SINAPI` and `IOPES`.
3. Normalize the files into tabular form when needed.
4. Run the validation script against the budget/list and the reference bases.
5. Review the exceptions manually before concluding that a code is wrong.

## Inputs

Expect one or more of these inputs:

- Budget spreadsheet with item codes and descriptions
- Exported `SINAPI` table
- Exported `IOPES` table
- Optional memorial, scope, or procurement file that mentions codes inline

If the official bases are not present locally, stop treating the task as a formal validation. In that case, report that the audit is incomplete because the authoritative tables were not provided.

## Validation Steps

### 1. Inspect the source material

- Prefer spreadsheet exports over screenshots or PDFs.
- If the source is a PDF or free text, extract the code list into a table first.
- Detect whether the budget mixes `SINAPI` and `IOPES`; if mixed, require or derive a `sistema` column.

### 2. Prepare the references

- Use local files only; do not assume online data is current or accessible.
- Accept `.csv`, `.tsv`, `.json`, `.xlsx`, or `.xlsm`.
- Read [source-layout.md](references/source-layout.md) when column names are unusual or sheet selection is needed.

### 3. Run the validator

Use `scripts/validate_codes.py`:

```bash
python scripts/validate_codes.py \
  --source "orcamento.xlsx#Planilha1" \
  --catalog "sinapi=sinapi.xlsx#Composicoes" \
  --catalog "iopes=iopes.csv" \
  --json-out "relatorio-validacao.json"
```

The script:

- detects likely columns automatically
- normalizes code formatting
- validates each budget code against the chosen base
- flags missing items
- flags description and unit mismatches
- emits a readable summary and an optional JSON report

### 4. Review exceptions carefully

- Treat `missing` as high-suspicion, but verify whether the user supplied the right monthly/state base.
- Treat `mismatch` as a review queue, not automatic failure.
- Small description edits can be acceptable local adaptations; unit mismatches are usually more serious.

## Output Format

Return:

- a concise summary with counts
- a flat list of invalid or doubtful codes
- file and row references for each finding
- a short note about any validation limits, such as missing official bases or unidentified system

## Constraints

- Do not claim a code is officially valid without a matching local base row.
- Do not infer current official prices from memory.
- Do not merge `SINAPI` and `IOPES` into one undifferentiated catalog.
- Preserve the user's original code formatting in the report, even when comparing normalized forms internally.

## Resources

- Script: `scripts/validate_codes.py`
- Reference: [source-layout.md](references/source-layout.md)
