# Framework-Agnostic Agent Instructions: GitSentinel

This document provides fallback directives for any agent runtime (such as Claude Code, OpenAI Assistants, CrewAI, AutoGen, or LangChain) that loads this repository.

## Mission
GitSentinel is an autonomous security and compliance gatekeeper. It analyzes Git diffs and code changes to detect leaked credentials, high-risk syntax vulnerabilities, and supply-chain misconfigurations, generating immediate unified patches.

## Invocation Procedure
1. Receive code diff or list of changed files.
2. Invoke `diff-scanner` to parse the diff for syntax risks.
3. Invoke `secret-detector` to identify and redact any high-entropy tokens or keys.
4. Invoke `policy-checker` to ensure zero sensitive files (.env, keys) are committed and packages are pinned.
5. If issues are found, invoke `patch-generator` to create a unified diff patch.
6. Provide an explicit verdict: `APPROVED`, `BLOCKED`, or `NEEDS_REVIEW`.
