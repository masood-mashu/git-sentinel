---
name: pr-review
description: Comprehensive security and compliance review workflow for Pull Request diffs
---

# PR Review Skill

## Trigger Conditions
Run this skill whenever a pull request, commit diff, or staged patch is submitted for review.

## Procedure
1. **Fetch Diff**: Ingest unified diff using `diff-scanner`.
2. **Scan for Syntax Vulnerabilities**: Detect SQLi, command injection, and dangerous execution patterns.
3. **Scan for Secrets**: Run `secret-detector` across added lines.
4. **Evaluate Policies**: Run `policy-checker` against repo file list.
5. **Issue Structured Verdict**:
   - `APPROVED`: 0 secrets, 0 critical syntax issues.
   - `BLOCKED`: >=1 secret or critical vulnerability found. Attach automated patch.
   - `NEEDS_REVIEW`: High severity or policy warning found.
6. **Log Audit Record**: Record entry in audit memory log.
