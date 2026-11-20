# Tenant-isolation methodology

## Boundary model

Map principal -> verified membership/service scope -> selected tenant -> action -> resource -> enforcement -> audit. Tenant IDs in headers, paths and queue messages are selectors, not independent authority. Public/global data and authorized platform-wide administration can legitimately cross tenants and must be classified explicitly. A tenant administrator is not automatically a platform administrator.

Distinguish confidentiality, integrity and availability. GET probes examine only narrow confidentiality cases. Cross-tenant updates, object ownership changes, shared-worker exhaustion and incorrect deletes require application-specific tests in an isolated fixture. Do not run destructive, load or restore tests under a read-only audit authorization.

## Evidence model

Each assessment check records a state, reviewer, rationale, evidence references, optional verified scope and remediation. Evidence kinds are code, configuration, architecture, operational and test. A code trace can confirm a code-path issue; runtime verification requires a relevant negative test and working positive controls. Every evidence item carries its actual environment, date, method and scope. An optional SHA256 is only a reference-integrity hint; the validator checks its format, not the source bytes.

Synthetic actors must have independently confirmed tenant memberships and access to distinct fixture resources. Positive controls demonstrate working credentials, endpoint routing and known resource ownership. A 403 for an expired identity proves nothing about object authorization. A 200 without the expected marker does not establish either leakage or denial. Any response status containing a known foreign seeded marker is relevant evidence of leakage, subject to fixture/provenance review. Never seed markers in request paths or credentials, where reflection could be mistaken for disclosure.

The optional GET runner reports observations only. A reviewer must trace request-to-resource relevance before adding probe outputs as evidence. No automatic whole-product verification, risk percentage or audit opinion is produced.

## Threat and test design

For each boundary, record an allowed own-tenant case and a denied foreign-tenant case for the same action/resource type. Reuse known IDs; do not enumerate unknown customers. Exercise direct, nested, collection, bulk, export and asynchronous paths separately. Test ordinary roles and explicit platform roles against their own documented permissions. Recheck revoked memberships, reused connections, retries, mixed batches and partially completed lifecycle operations.

If no runtime fixture or human owner is available, report code leads and unknowns. Do not fabricate positive controls, reviewer identities or production observations. Fixture setup, SQL execution and environment access are separate actions that need authorized scope.

## Closure

Confirmed failures need affected-path evidence, impact, owner, a bounded fix and a regression test with both positive and negative cases. Record any tested denials narrowly using verified_scope. Preserve baseline findings and stale evidence on recheck. A patched query without a relevant regression test does not establish closure of all related paths.
