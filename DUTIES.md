# Segregation of Duties (SOD) Policy: GitSentinel

## Role Definitions

### 1. Auditor (`auditor`)
* **Scope**: Read-only scanning of incoming diffs, credentials, and repository configurations.
* **Permissions**: `inspect`, `scan`, `audit`
* **Agent**: `git-sentinel`

### 2. Remediator (`remediator`)
* **Scope**: Proposing unified diff patches to replace hardcoded credentials with environment variables.
* **Permissions**: `generate_patch`, `propose_fix`
* **Agent**: `git-sentinel`

### 3. Approver (`approver`)
* **Scope**: Final human sign-off on pull requests or merge actions.
* **Permissions**: `merge`, `approve_override`
* **Boundary**: Human repository maintainer (never automated by agent).

## Conflict Rules
* An autonomous agent cannot approve its own remediation patches into production without human-in-the-loop review for high-risk changes.
* All secret remediation patches must require rotation confirmation from the account holder.
