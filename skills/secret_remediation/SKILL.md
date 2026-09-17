---
name: secret_remediation
description: Automated credential extraction, rotation advice, and patch generation
---

# Secret Remediation Skill

## Trigger Conditions
Run this skill when `secret_detector` finds a leaked credential or high-entropy secret.

## Procedure
1. **Identify Secret Pattern**: Classify whether the secret is AWS, OpenAI, GitHub, Stripe, or generic.
2. **Never Echo Secret**: Redact the token value in the report.
3. **Map Environment Variable**:
   - OpenAI $\rightarrow$ `OPENAI_API_KEY`
   - AWS $\rightarrow$ `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY`
   - GitHub $\rightarrow$ `GITHUB_TOKEN`
   - Stripe $\rightarrow$ `STRIPE_SECRET_KEY`
4. **Generate Unified Patch**: Use `patch_generator` to replace hardcoded strings with standard environment lookups (`os.getenv` or `process.env`).
5. **Issue Revocation Advisory**: Advise the repository owner to immediately revoke the exposed key in the provider dashboard.
