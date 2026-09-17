# GitSentinel Explainability Specification (EXPLAINABILITY.md)

This document provides a transparent, verifiable architectural breakdown of how **GitSentinel** reasons, evaluates inputs, selects tools, and formulates verdicts. It satisfies the transparency, accountability, and predictable behavior requirements of the **Open GitAgent Protocol (GAP)** and the **HiDevs Passport Clearance Pipeline (Checkpoint 2)**.

---

## 1. Decision Pipeline & Reasoning Flow

GitSentinel executes a deterministic, multi-stage reasoning pipeline for every code review or diff inspection:

```
[Incoming Git Diff / Commit]
            │
            ▼
 ┌──────────────────────┐
 │  1. Diff Ingestion   │  --> diff-scanner parses changed files, line numbers,
 └──────────┬───────────┘      and scans for dangerous execution patterns.
            │
            ▼
 ┌──────────────────────┐
 │ 2. Secret & Entropy  │  --> secret-detector runs regex signatures & Shannon entropy
 └──────────┬───────────┘      calculations to identify credentials without echoing them.
            │
            ▼
 ┌──────────────────────┐
 │ 3. Policy Compliance │  --> policy-checker checks repository files, dependency pinning,
 └──────────┬───────────┘      and sensitive file exclusions (.env, .pem).
            │
            ▼
 ┌──────────────────────┐
 │ 4. Patch Synthesis   │  --> If defects exist, patch-generator formulates unified diffs
 └──────────┬───────────┘      replacing hardcoded secrets with environment lookups.
            │
            ▼
 ┌──────────────────────┐
 │  5. Verdict & Audit  │  --> Issues structured decision (APPROVED / BLOCKED / NEEDS_REVIEW)
 └──────────────────────┘      and writes an immutable audit record to memory/audit.log.
```

---

## 2. Tool Selection Criteria & Invocation Logic

Every tool call by GitSentinel is strictly governed by transparent invocation criteria:

| Tool Name | Invocation Trigger | Expected Input | Output Artifact | Decision Influence |
| :--- | :--- | :--- | :--- | :--- |
| **`diff-scanner`** | Any incoming code diff or pull request. | Unified diff text (`diff_text`) | List of changed files & suspicious syntax patterns (`eval`, `exec`, `shell=True`). | Triggers `BLOCKED` if critical syntax risks are found. |
| **`secret-detector`** | Added or modified lines in diff. | Content string (`content`) | Classified secrets (AWS, OpenAI, GitHub PAT, JWT) with redacted previews. | Hard blocker: >=1 exposed secret triggers immediate `BLOCKED`. |
| **`policy-checker`** | File list or manifest changes. | File paths, `package.json`, `requirements.txt` | Policy violation list (forbidden files, unpinned dependencies). | Blocks on sensitive file commit; issues `WARN` for unpinned versions. |
| **`patch-generator`** | Detected secret or fixable flaw. | File path, original snippet, remediated replacement snippet | Unified diff patch ready for `git apply`. | Provides automated remediation attached to review verdict. |

---

## 3. Predictability & Determinism Safeguards

To prevent non-deterministic hallucinations and ensure identical evaluations across runtimes:

1. **Low Temperature Constraint:** Set to `0.1` in `agent.yaml` to ensure near-zero variance in classification.
2. **Deterministic Shannon Entropy Scoring:** Credential detection is grounded in mathematical entropy ($H(X) = -\sum P(x) \log_2 P(x)$) alongside strict regex signatures, eliminating false-positive hallucinations.
3. **Adversarial Resilience:** Comments within incoming source code attempting to override system behavior (e.g. `// gitagent-ignore`, `// override: approve`) are explicitly ignored by the parser.
4. **Coordinate Citations:** GitSentinel is forbidden by `RULES.md` from flagging any issue without citing exact file paths and line number coordinates.

---

## 4. Auditability & Memory Traceability

GitSentinel logs all evaluations to `memory/audit.log` with machine-readable fields:
* **Timestamp**: ISO 8601 UTC timestamp.
* **Commit/Diff Hash**: Cryptographic SHA-256 fingerprint of the reviewed input.
* **Violation Summary**: Count of critical, high, medium, and low severity findings.
* **Final Verdict**:
  * `APPROVED`: 0 secrets, 0 critical syntax risks, zero sensitive files.
  * `BLOCKED`: Leaked credential or command injection vulnerability detected.
  * `NEEDS_REVIEW`: High-severity policy warning requiring human confirmation.

---

## 5. Fallback & Human-in-the-Loop Escalation

* **Model Fallback Chain:** If `openai:gpt-4o` encounters rate limits or network degradation, GitSentinel automatically fails over to `anthropic:claude-3-5-sonnet` and `openai:gpt-4o-mini` without losing session state.
* **Segregation of Duties (DUTIES.md):** As an autonomous worker, GitSentinel holds the `auditor` and `remediator` roles. The `approver` role is reserved for human maintainers. All automated remediation patches require human sign-off before merging to production branches.
