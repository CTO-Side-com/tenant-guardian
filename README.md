# Tenant Guardian

**Find and test cross-tenant access paths in SaaS applications, with evidence and explicit scope.**

Built by [CTOside](https://ctoside.com). Python 3.9+, standard library only. Offline by default. Works as a coding-agent skill or a Claude Code plugin.

Tenant Guardian maps isolation across authentication, APIs, databases, caches, object storage, queues, AI retrieval and lifecycle operations. It keeps suspected code gaps, confirmed findings, tested denials and missing evidence separate.

## Included

- 36 original objectives across eight boundary areas.
- 10 conservative source/configuration heuristics with metadata-only findings.
- Evidence validation, scoped runtime conclusions, regression prompts and change-aware rechecks.
- Optional read-only probes for two synthetic tenant identities and explicitly selected GET paths.
- Working positive controls before cross-tenant requests; 401, empty success, redirects and transport errors remain inconclusive.
- A safe and a deliberately vulnerable synthetic loopback fixture.
- PDF/Markdown reports, risk register, hashed handoff manifest and Jira/Notion/Slack task files.
- Offline tests and loopback integration tests. No external traffic is needed to run the test suite.

This is a scoped engineering assessment, not an isolation guarantee, penetration-test attestation or compliance certification. An absence of scanner findings proves nothing about untested paths.

## Install

Extract this ZIP and open a terminal in the extracted `tenant-guardian` directory. Load the Claude Code plugin:

```bash
claude --plugin-dir .
```

Inside Claude Code, invoke:

```text
/tenant-guardian:tenant-guardian
```

Alternatively, copy `skills/tenant-guardian` to your coding agent's supported skills directory. Keep its LICENSE with the files.

## Ask your coding agent

```text
Use Tenant Guardian to review this SaaS read-only.
Map trusted tenant context through APIs, PostgreSQL, Redis, S3-compatible storage,
background jobs and AI retrieval. Distinguish global resources and authorized
platform administration from ordinary tenant paths. Produce a scoped evidence
matrix, a regression plan, PDF report and remediation tasks in tenant-output/.
Use only synthetic data. Do not execute network or write tests without explicit scope.
```

## Standalone commands

```bash
SKILL_DIR=skills/tenant-guardian
python3 "$SKILL_DIR/scripts/guardian.py" init --product "My SaaS" --environment staging --out tenant-output/assessment.json
python3 "$SKILL_DIR/scripts/guardian.py" scan --repo . --out tenant-output/scanner-findings.json
python3 "$SKILL_DIR/scripts/guardian.py" plan --assessment tenant-output/assessment.json --out tenant-output/TEST-PLAN.md
# Review and populate assessment.json using actual scoped evidence.
python3 "$SKILL_DIR/scripts/guardian.py" validate --assessment tenant-output/assessment.json
python3 "$SKILL_DIR/scripts/guardian.py" report --assessment tenant-output/assessment.json --out tenant-output/handoff --pdf
python3 "$SKILL_DIR/scripts/guardian.py" tasks --assessment tenant-output/assessment.json --out tenant-output/tasks
```

Initialization and plan generation refuse overwrite. Rechecks write a new assessment. Reports distinguish confirmed findings from suspected gaps and unknowns. Real assessments should stay outside public version control.

## Optional GET probes

Adapt the bundled `assets/probe-plan.json` for an explicitly authorized synthetic local/test/staging fixture. Credentials must already be in the named environment variables; never put token values in the plan or commands. Seed independent response markers in stored fixture data.

```bash
python3 skills/tenant-guardian/scripts/probe.py --plan tenant-probe-plan.json --dry-run
```

After the operator has authorized the exact origin and safe GET paths:

```bash
python3 skills/tenant-guardian/scripts/probe.py --plan tenant-probe-plan.json --allow-origin https://staging.example.com --allow-network --synthetic-only --out tenant-output/probes.json
```

Change the plan's origin to match the explicitly approved origin. HTTPS is required except for loopback fixtures. The runner does not follow redirects, use environment proxies, send writes, create fixtures or persist tokens, raw bodies, marker values or request paths. It caps response bytes and per-request time. Results require review and do not change assessment statuses.

A denied GET covers only that operation and fixture. Writes, collection queries, exports, websocket events, cache warming, DB roles, queue retries, restores and AI tools need separate authorized integration tests. GET handlers themselves must be reviewed for side effects before probing.

## Demonstration and verification

```bash
python3 -m unittest discover -s skills/tenant-guardian/tests -v
python3 docs/build_example.py
```

The example builder starts only owned synthetic loopback fixtures on ephemeral ports, probes isolated and vulnerable modes, then stops both servers. It generates probe metadata, a clearly synthetic evidence-linked assessment, PDF/Markdown reports, regression prompts and tracker tasks. No real company or customer system is assessed.

See [the synthetic report](docs/example/TENANT-ISOLATION.md), [safe observations](docs/example/probes-safe.json), and [vulnerable observations](docs/example/probes-vulnerable.json).

## Interpretation limits

RLS, dedicated databases, schema separation and scoped query enforcement can all be valid choices. A missing `tenant_id` literal is not proof of a bug. Prefixes and random IDs are not authorization by themselves. Presigned URLs may intentionally be bearer-accessible; assess authorization before signing and the documented sharing contract.

Markers are a narrow oracle: transformed fields, untested metadata and data beyond the response-size cap may not be detected. Runtime results and evidence fields need a responsible review. Redaction is limited and sharing requires manual inspection. PDF uses built-in Western fonts; Markdown preserves Unicode.

Original objectives reference OWASP tenant-security guidance, OWASP API authorization guidance and PostgreSQL documentation. No external endorsement or certification is claimed. Distributed under the MIT License.
