# Security

## Reporting a vulnerability

Use "Report a vulnerability" in the repository's Security tab on GitHub (private reporting). That feature depends on the maintainer having enabled it in the repository settings, which has not been verified. If the option does not appear, open an issue asking for a private channel, without exploitable details.

Include: the affected file and excerpt, the condition under which it occurs, the impact, and steps to reproduce, with no real credentials.

## What is in scope

- Skill instructions that lead an agent to run commands, expose secrets, edit the target in an audit-only request, or act externally without authorization.
- `scripts/validate.py`: reading files outside the project, running code from the analyzed material, or leaking content.
- Fixtures in `evals/files/`: they contain malicious instructions **on purpose** (exfiltration, injection, suspicious install) to test the agent. That is not a vulnerability, as long as they stay as `.txt` text that nothing executes.

## Handling secrets

Do not put credentials, tokens, or personal data in code, fixtures, logs, or issues. A secret exposed in history must be revoked, not merely removed.
