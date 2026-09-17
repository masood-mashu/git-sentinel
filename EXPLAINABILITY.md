# GitSentinel Explainability Specification

This document provides a transparent, verifiable architectural breakdown of how **GitSentinel** operates, processes input, makes decisions, and enforces security boundaries.

---

## 1. Input Data and Data Sources Used

GitSentinel consumes unified git diffs, commit histories, and repository configuration files as its primary input data. These data sources include code additions, deletions, package manifests such as package.json, and repository directory structures. The agent ingests these inputs in raw text format and parses them into structured syntax trees and token streams for downstream analysis. External environmental configuration files are also monitored as sensitive data sources to ensure credentials are never inappropriately tracked.

---

## 2. How It Decides and Reasoning Process

The decision making process follows a deterministic, five-stage analytical pipeline designed to eliminate ambiguity and hallucination. When a pull request or git diff is received, the agent first evaluates syntax trees using the diff-scanner tool to identify risky patterns like arbitrary code execution. Next, the reasoning engine invokes the secret-detector tool to compute Shannon entropy scores and regex matches for exposed API keys and credentials. Finally, the agent correlates all findings against predefined security policies to issue a conclusive verdict of APPROVED, BLOCKED, or NEEDS_REVIEW alongside an automated patch when remediation is possible.

---

## 3. Constraints, Limitations, and Known Issues

GitSentinel operates under strict operational constraints to prevent false positives and non-deterministic behavior across different agent frameworks. The agent is deliberately limited to static diff analysis and cannot execute dynamic runtime sandbox testing of compiled binaries. Another known issue and limitation is that heavily obfuscated or encrypted secrets with low entropy may require secondary human review rather than autonomous blocking. Furthermore, the agent enforces a low temperature constraint of 0.1 to maintain strict predictability across all supported export frameworks.
