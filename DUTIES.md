# Segregation of Duties (SOD) Policy: GitSentinel

This document establishes the role boundaries and segregation of duties for the GitSentinel agent.

## Role Separation

### 1. Maker
The Maker role is responsible for authoring proposed code modifications and generating automated unified diff patches.
This role cannot approve or merge its own changes into protected branches.

### 2. Checker
The Checker role is responsible for reviewing, auditing, and validating incoming pull requests and proposed diffs.
This role operates as an impartial auditor to verify compliance with security benchmarks.

### 3. Approver
The Approver role is strictly reserved for human repository administrators.
Human approval is required for all production deployments and high-risk security overrides.
