# Tenant Guardian
Scoped tenant-isolation assessment. Not a guarantee of isolation, penetration-test attestation or compliance certification.

Product: Synthetic two-tenant invoice API
Environment: local
Assessor: Automated synthetic demonstration; not a human or customer assessment
Architecture: Synthetic shared service with explicit object ownership checks
Systems: Owned loopback invoice fixture
Exclusions: No customer or production services
Scope unknowns: Writes, lists, database roles, storage, caches, jobs, websockets and AI paths are not tested by this GET demonstration.

## Confirmed findings and suspected gaps
API-001 | confirmed_gap | high | Authorize tenant-owned objects on every read path | Enforce the fixture ownership check independently of the requested object identifier.

## Assessment matrix

### CTX-001 | Verify tenant identity from authenticated membership
Status: insufficient_evidence
Rationale: No supported conclusion recorded.
Verified scope: None
Evidence: None
Reviewer: Unassigned; Owner: Unassigned
Next action: Collect scoped evidence and execute an authorized negative test.
Retest: Try a valid actor with another tenant selector and verify it cannot broaden access.

### CTX-002 | Treat client tenant selectors as untrusted input
Status: insufficient_evidence
Rationale: No supported conclusion recorded.
Verified scope: None
Evidence: None
Reviewer: Unassigned; Owner: Unassigned
Next action: Collect scoped evidence and execute an authorized negative test.
Retest: Change tenant headers and path selectors while retaining the original synthetic identity.

### CTX-003 | Separate tenant roles from platform administration
Status: insufficient_evidence
Rationale: No supported conclusion recorded.
Verified scope: None
Evidence: None
Reviewer: Unassigned; Owner: Unassigned
Next action: Collect scoped evidence and execute an authorized negative test.
Retest: Use a tenant administrator identity against platform-wide operations and expect denial.

### CTX-004 | Isolate request and thread tenant context
Status: insufficient_evidence
Rationale: No supported conclusion recorded.
Verified scope: None
Evidence: None
Reviewer: Unassigned; Owner: Unassigned
Next action: Collect scoped evidence and execute an authorized negative test.
Retest: Alternate and concurrently execute requests for two tenants using reused workers.

### CTX-005 | Revalidate tenant switching and revoked membership
Status: insufficient_evidence
Rationale: No supported conclusion recorded.
Verified scope: None
Evidence: None
Reviewer: Unassigned; Owner: Unassigned
Next action: Collect scoped evidence and execute an authorized negative test.
Retest: Revoke synthetic membership, replay sessions and retry a tenant switch.

### API-001 | Authorize tenant-owned objects on every read path
Status: confirmed_gap
Rationale: Only the deliberately vulnerable synthetic fixture disclosed both foreign invoice markers. The isolated mode denied the same configured reads.
Verified scope: None
Evidence: SYNTHETIC-GET-LEAK
Reviewer: Automated synthetic demonstration; Owner: Synthetic fixture owner
Next action: Enforce the fixture ownership check independently of the requested object identifier.
Retest: Both own-tenant controls succeed and both foreign fixture reads return marker-free denials. This covers GET only.

### API-002 | Authorize create update and delete operations
Status: insufficient_evidence
Rationale: No supported conclusion recorded.
Verified scope: None
Evidence: None
Reviewer: Unassigned; Owner: Unassigned
Next action: Collect scoped evidence and execute an authorized negative test.
Retest: In an isolated fixture, attempt cross-tenant update, delete and ownership reassignment; verify state is unchanged.

### API-003 | Scope list search aggregation and count endpoints
Status: insufficient_evidence
Rationale: No supported conclusion recorded.
Verified scope: None
Evidence: None
Reviewer: Unassigned; Owner: Unassigned
Next action: Collect scoped evidence and execute an authorized negative test.
Retest: Compare tenant-specific lists, search, counts, facets and pagination using distinct synthetic records.

### API-004 | Validate nested and bulk resource ownership
Status: insufficient_evidence
Rationale: No supported conclusion recorded.
Verified scope: None
Evidence: None
Reviewer: Unassigned; Owner: Unassigned
Next action: Collect scoped evidence and execute an authorized negative test.
Retest: Mix synthetic A and B IDs in a batch and mismatched parent-child paths.

### API-005 | Protect exports reports and download endpoints
Status: insufficient_evidence
Rationale: No supported conclusion recorded.
Verified scope: None
Evidence: None
Reviewer: Unassigned; Owner: Unassigned
Next action: Collect scoped evidence and execute an authorized negative test.
Retest: Generate an authorized synthetic export and attempt retrieval as another tenant.

### API-006 | Authorize websocket subscriptions and pushed events
Status: insufficient_evidence
Rationale: No supported conclusion recorded.
Verified scope: None
Evidence: None
Reviewer: Unassigned; Owner: Unassigned
Next action: Collect scoped evidence and execute an authorized negative test.
Retest: Subscribe with A to B's synthetic topic and trigger a safe event in a fixture.

### DB-001 | Choose and document an enforceable data isolation model
Status: insufficient_evidence
Rationale: No supported conclusion recorded.
Verified scope: None
Evidence: None
Reviewer: Unassigned; Owner: Unassigned
Next action: Collect scoped evidence and execute an authorized negative test.
Retest: Trace ordinary and privileged identities through the chosen isolation mechanism.

### DB-002 | Review direct key lookups joins and raw SQL
Status: insufficient_evidence
Rationale: No supported conclusion recorded.
Verified scope: None
Evidence: None
Reviewer: Unassigned; Owner: Unassigned
Next action: Collect scoped evidence and execute an authorized negative test.
Retest: Test known foreign IDs through ORM get, joins, aggregates, raw SQL and repository helpers.

### DB-003 | Review PostgreSQL row security and bypass roles
Status: insufficient_evidence
Rationale: No supported conclusion recorded.
Verified scope: None
Evidence: None
Reviewer: Unassigned; Owner: Unassigned
Next action: Collect scoped evidence and execute an authorized negative test.
Retest: Inspect role and policy metadata; test SELECT and writes as the actual request role with synthetic rows.

### DB-004 | Reset tenant context across pooled database connections
Status: insufficient_evidence
Rationale: No supported conclusion recorded.
Verified scope: None
Evidence: None
Reviewer: Unassigned; Owner: Unassigned
Next action: Collect scoped evidence and execute an authorized negative test.
Retest: Alternate synthetic tenants on a reused connection, including rollback and exception paths.

### DB-005 | Scope relations constraints and referential operations
Status: insufficient_evidence
Rationale: No supported conclusion recorded.
Verified scope: None
Evidence: None
Reviewer: Unassigned; Owner: Unassigned
Next action: Collect scoped evidence and execute an authorized negative test.
Retest: Attempt cross-tenant foreign-key assignments and assess errors without relying on RLS for referential checks.

### DB-006 | Review migrations views and privileged database functions
Status: insufficient_evidence
Rationale: No supported conclusion recorded.
Verified scope: None
Evidence: None
Reviewer: Unassigned; Owner: Unassigned
Next action: Collect scoped evidence and execute an authorized negative test.
Retest: Exercise newly introduced and privileged query paths as ordinary tenant identities.

### CACHE-001 | Namespace tenant-dependent cache entries
Status: insufficient_evidence
Rationale: No supported conclusion recorded.
Verified scope: None
Evidence: None
Reviewer: Unassigned; Owner: Unassigned
Next action: Collect scoped evidence and execute an authorized negative test.
Retest: Prime the same endpoint as B then request as A using distinguishable synthetic payloads.

### CACHE-002 | Scope authorization and memoization caches
Status: insufficient_evidence
Rationale: No supported conclusion recorded.
Verified scope: None
Evidence: None
Reviewer: Unassigned; Owner: Unassigned
Next action: Collect scoped evidence and execute an authorized negative test.
Retest: Reuse object identifiers across tenant and role changes and inspect resulting decisions.

### CACHE-003 | Scope cache invalidation and tenant deletion
Status: insufficient_evidence
Rationale: No supported conclusion recorded.
Verified scope: None
Evidence: None
Reviewer: Unassigned; Owner: Unassigned
Next action: Collect scoped evidence and execute an authorized negative test.
Retest: Invalidate synthetic A entries and verify B remains intact.

### CACHE-004 | Review CDN and response caching variation
Status: insufficient_evidence
Rationale: No supported conclusion recorded.
Verified scope: None
Evidence: None
Reviewer: Unassigned; Owner: Unassigned
Next action: Collect scoped evidence and execute an authorized negative test.
Retest: Alternate credentials through the same cache URL and inspect synthetic response markers.

### STORE-001 | Authorize object access beyond path naming
Status: insufficient_evidence
Rationale: No supported conclusion recorded.
Verified scope: None
Evidence: None
Reviewer: Unassigned; Owner: Unassigned
Next action: Collect scoped evidence and execute an authorized negative test.
Retest: Request a known foreign synthetic object through each download and storage access path.

### STORE-002 | Bind signed links to approved resources and operations
Status: insufficient_evidence
Rationale: No supported conclusion recorded.
Verified scope: None
Evidence: None
Reviewer: Unassigned; Owner: Unassigned
Next action: Collect scoped evidence and execute an authorized negative test.
Retest: Try to obtain a signed link for a foreign object; assess the documented bearer-link sharing model separately.

### STORE-003 | Constrain object paths and tenant-prefix boundaries
Status: insufficient_evidence
Rationale: No supported conclusion recorded.
Verified scope: None
Evidence: None
Reviewer: Unassigned; Owner: Unassigned
Next action: Collect scoped evidence and execute an authorized negative test.
Retest: Exercise synthetic path traversal variants and neighboring tenant names such as acme and acme-west.

### STORE-004 | Scope object deletion versions and retained copies
Status: insufficient_evidence
Rationale: No supported conclusion recorded.
Verified scope: None
Evidence: None
Reviewer: Unassigned; Owner: Unassigned
Next action: Collect scoped evidence and execute an authorized negative test.
Retest: Use isolated synthetic versions to check only the selected tenant's allowed copies are affected.

### JOB-001 | Authenticate queued tenant context
Status: insufficient_evidence
Rationale: No supported conclusion recorded.
Verified scope: None
Evidence: None
Reviewer: Unassigned; Owner: Unassigned
Next action: Collect scoped evidence and execute an authorized negative test.
Retest: Inject a foreign tenant selector in a synthetic queue message and verify independent authorization.

### JOB-002 | Scope retry idempotency and dead-letter state
Status: insufficient_evidence
Rationale: No supported conclusion recorded.
Verified scope: None
Evidence: None
Reviewer: Unassigned; Owner: Unassigned
Next action: Collect scoped evidence and execute an authorized negative test.
Retest: Reuse synthetic idempotency keys across tenants and exercise retries and dead-letter access.

### JOB-003 | Bind webhooks and service credentials to authorized tenants
Status: insufficient_evidence
Rationale: No supported conclusion recorded.
Verified scope: None
Evidence: None
Reviewer: Unassigned; Owner: Unassigned
Next action: Collect scoped evidence and execute an authorized negative test.
Retest: Replay a synthetic webhook with mismatched tenant identifiers and a valid but differently scoped credential.

### JOB-004 | Limit tenant impact on shared worker capacity
Status: insufficient_evidence
Rationale: No supported conclusion recorded.
Verified scope: None
Evidence: None
Reviewer: Unassigned; Owner: Unassigned
Next action: Collect scoped evidence and execute an authorized negative test.
Retest: Review queue concurrency and limits; load tests require separately approved scope.

### AI-001 | Enforce tenant filtering in vector and search retrieval
Status: insufficient_evidence
Rationale: No supported conclusion recorded.
Verified scope: None
Evidence: None
Reviewer: Unassigned; Owner: Unassigned
Next action: Collect scoped evidence and execute an authorized negative test.
Retest: Index distinct synthetic markers for A and B, then retrieve as each tenant.

### AI-002 | Isolate conversation history memory and semantic caches
Status: insufficient_evidence
Rationale: No supported conclusion recorded.
Verified scope: None
Evidence: None
Reviewer: Unassigned; Owner: Unassigned
Next action: Collect scoped evidence and execute an authorized negative test.
Retest: Reuse synthetic thread and document IDs across actors and inspect retrieval and memory results.

### AI-003 | Enforce tool authorization outside model output
Status: insufficient_evidence
Rationale: No supported conclusion recorded.
Verified scope: None
Evidence: None
Reviewer: Unassigned; Owner: Unassigned
Next action: Collect scoped evidence and execute an authorized negative test.
Retest: Place a synthetic instruction requesting B's data in A's document and verify tool-side denial.

### AI-004 | Keep traces datasets and evaluation artifacts tenant safe
Status: insufficient_evidence
Rationale: No supported conclusion recorded.
Verified scope: None
Evidence: None
Reviewer: Unassigned; Owner: Unassigned
Next action: Collect scoped evidence and execute an authorized negative test.
Retest: Inspect approved synthetic traces, exports and evaluation data access boundaries.

### LIFE-001 | Verify provisioning tenant deletion and failed setup cleanup
Status: insufficient_evidence
Rationale: No supported conclusion recorded.
Verified scope: None
Evidence: None
Reviewer: Unassigned; Owner: Unassigned
Next action: Collect scoped evidence and execute an authorized negative test.
Retest: Simulate failed provisioning and isolated synthetic tenant deletion; verify neighboring tenants remain unchanged.

### LIFE-002 | Scope backup restore and support access
Status: insufficient_evidence
Rationale: No supported conclusion recorded.
Verified scope: None
Evidence: None
Reviewer: Unassigned; Owner: Unassigned
Next action: Collect scoped evidence and execute an authorized negative test.
Retest: Restore into an isolated fixture and verify only the selected tenant is copied; review support access approvals.

### LIFE-003 | Protect tenant audit feeds and cross-tenant administration
Status: insufficient_evidence
Rationale: No supported conclusion recorded.
Verified scope: None
Evidence: None
Reviewer: Unassigned; Owner: Unassigned
Next action: Collect scoped evidence and execute an authorized negative test.
Retest: Read synthetic audit events as A and test platform support actions through their explicit privileged path.

## Evidence index
SYNTHETIC-GET-LEAK | test | docs/example/probes-vulnerable.json | Two fixture invoice objects and two distinct synthetic tenant identities; GET only | 2026-11-19

Counts describe reviewed evidence states, not an isolation score. A denied GET does not verify write, list, search, export, queue, cache, storage or AI paths.
PDF uses built-in Western fonts. Use Markdown for full Unicode. Review all outputs before sharing; redaction is limited.
