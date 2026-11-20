- [ ] Collect evidence: Verify tenant identity from authenticated membership (CTX-001)
  Collect scoped evidence; preserve unknowns. Done when: Try a valid actor with another tenant selector and verify it cannot broaden access.
- [ ] Collect evidence: Treat client tenant selectors as untrusted input (CTX-002)
  Collect scoped evidence; preserve unknowns. Done when: Change tenant headers and path selectors while retaining the original synthetic identity.
- [ ] Collect evidence: Separate tenant roles from platform administration (CTX-003)
  Collect scoped evidence; preserve unknowns. Done when: Use a tenant administrator identity against platform-wide operations and expect denial.
- [ ] Collect evidence: Isolate request and thread tenant context (CTX-004)
  Collect scoped evidence; preserve unknowns. Done when: Alternate and concurrently execute requests for two tenants using reused workers.
- [ ] Collect evidence: Revalidate tenant switching and revoked membership (CTX-005)
  Collect scoped evidence; preserve unknowns. Done when: Revoke synthetic membership, replay sessions and retry a tenant switch.
- [ ] Fix: Authorize tenant-owned objects on every read path (API-001)
  Enforce the fixture ownership check independently of the requested object identifier. Done when: Both own-tenant controls succeed and both foreign fixture reads return marker-free denials. This covers GET only.
- [ ] Collect evidence: Authorize create update and delete operations (API-002)
  Collect scoped evidence; preserve unknowns. Done when: In an isolated fixture, attempt cross-tenant update, delete and ownership reassignment; verify state is unchanged.
- [ ] Collect evidence: Scope list search aggregation and count endpoints (API-003)
  Collect scoped evidence; preserve unknowns. Done when: Compare tenant-specific lists, search, counts, facets and pagination using distinct synthetic records.
- [ ] Collect evidence: Validate nested and bulk resource ownership (API-004)
  Collect scoped evidence; preserve unknowns. Done when: Mix synthetic A and B IDs in a batch and mismatched parent-child paths.
- [ ] Collect evidence: Protect exports reports and download endpoints (API-005)
  Collect scoped evidence; preserve unknowns. Done when: Generate an authorized synthetic export and attempt retrieval as another tenant.
- [ ] Collect evidence: Authorize websocket subscriptions and pushed events (API-006)
  Collect scoped evidence; preserve unknowns. Done when: Subscribe with A to B's synthetic topic and trigger a safe event in a fixture.
- [ ] Collect evidence: Choose and document an enforceable data isolation model (DB-001)
  Collect scoped evidence; preserve unknowns. Done when: Trace ordinary and privileged identities through the chosen isolation mechanism.
- [ ] Collect evidence: Review direct key lookups joins and raw SQL (DB-002)
  Collect scoped evidence; preserve unknowns. Done when: Test known foreign IDs through ORM get, joins, aggregates, raw SQL and repository helpers.
- [ ] Collect evidence: Review PostgreSQL row security and bypass roles (DB-003)
  Collect scoped evidence; preserve unknowns. Done when: Inspect role and policy metadata; test SELECT and writes as the actual request role with synthetic rows.
- [ ] Collect evidence: Reset tenant context across pooled database connections (DB-004)
  Collect scoped evidence; preserve unknowns. Done when: Alternate synthetic tenants on a reused connection, including rollback and exception paths.
- [ ] Collect evidence: Scope relations constraints and referential operations (DB-005)
  Collect scoped evidence; preserve unknowns. Done when: Attempt cross-tenant foreign-key assignments and assess errors without relying on RLS for referential checks.
- [ ] Collect evidence: Review migrations views and privileged database functions (DB-006)
  Collect scoped evidence; preserve unknowns. Done when: Exercise newly introduced and privileged query paths as ordinary tenant identities.
- [ ] Collect evidence: Namespace tenant-dependent cache entries (CACHE-001)
  Collect scoped evidence; preserve unknowns. Done when: Prime the same endpoint as B then request as A using distinguishable synthetic payloads.
- [ ] Collect evidence: Scope authorization and memoization caches (CACHE-002)
  Collect scoped evidence; preserve unknowns. Done when: Reuse object identifiers across tenant and role changes and inspect resulting decisions.
- [ ] Collect evidence: Scope cache invalidation and tenant deletion (CACHE-003)
  Collect scoped evidence; preserve unknowns. Done when: Invalidate synthetic A entries and verify B remains intact.
- [ ] Collect evidence: Review CDN and response caching variation (CACHE-004)
  Collect scoped evidence; preserve unknowns. Done when: Alternate credentials through the same cache URL and inspect synthetic response markers.
- [ ] Collect evidence: Authorize object access beyond path naming (STORE-001)
  Collect scoped evidence; preserve unknowns. Done when: Request a known foreign synthetic object through each download and storage access path.
- [ ] Collect evidence: Bind signed links to approved resources and operations (STORE-002)
  Collect scoped evidence; preserve unknowns. Done when: Try to obtain a signed link for a foreign object; assess the documented bearer-link sharing model separately.
- [ ] Collect evidence: Constrain object paths and tenant-prefix boundaries (STORE-003)
  Collect scoped evidence; preserve unknowns. Done when: Exercise synthetic path traversal variants and neighboring tenant names such as acme and acme-west.
- [ ] Collect evidence: Scope object deletion versions and retained copies (STORE-004)
  Collect scoped evidence; preserve unknowns. Done when: Use isolated synthetic versions to check only the selected tenant's allowed copies are affected.
- [ ] Collect evidence: Authenticate queued tenant context (JOB-001)
  Collect scoped evidence; preserve unknowns. Done when: Inject a foreign tenant selector in a synthetic queue message and verify independent authorization.
- [ ] Collect evidence: Scope retry idempotency and dead-letter state (JOB-002)
  Collect scoped evidence; preserve unknowns. Done when: Reuse synthetic idempotency keys across tenants and exercise retries and dead-letter access.
- [ ] Collect evidence: Bind webhooks and service credentials to authorized tenants (JOB-003)
  Collect scoped evidence; preserve unknowns. Done when: Replay a synthetic webhook with mismatched tenant identifiers and a valid but differently scoped credential.
- [ ] Collect evidence: Limit tenant impact on shared worker capacity (JOB-004)
  Collect scoped evidence; preserve unknowns. Done when: Review queue concurrency and limits; load tests require separately approved scope.
- [ ] Collect evidence: Enforce tenant filtering in vector and search retrieval (AI-001)
  Collect scoped evidence; preserve unknowns. Done when: Index distinct synthetic markers for A and B, then retrieve as each tenant.
- [ ] Collect evidence: Isolate conversation history memory and semantic caches (AI-002)
  Collect scoped evidence; preserve unknowns. Done when: Reuse synthetic thread and document IDs across actors and inspect retrieval and memory results.
- [ ] Collect evidence: Enforce tool authorization outside model output (AI-003)
  Collect scoped evidence; preserve unknowns. Done when: Place a synthetic instruction requesting B's data in A's document and verify tool-side denial.
- [ ] Collect evidence: Keep traces datasets and evaluation artifacts tenant safe (AI-004)
  Collect scoped evidence; preserve unknowns. Done when: Inspect approved synthetic traces, exports and evaluation data access boundaries.
- [ ] Collect evidence: Verify provisioning tenant deletion and failed setup cleanup (LIFE-001)
  Collect scoped evidence; preserve unknowns. Done when: Simulate failed provisioning and isolated synthetic tenant deletion; verify neighboring tenants remain unchanged.
- [ ] Collect evidence: Scope backup restore and support access (LIFE-002)
  Collect scoped evidence; preserve unknowns. Done when: Restore into an isolated fixture and verify only the selected tenant is copied; review support access approvals.
- [ ] Collect evidence: Protect tenant audit feeds and cross-tenant administration (LIFE-003)
  Collect scoped evidence; preserve unknowns. Done when: Read synthetic audit events as A and test platform support actions through their explicit privileged path.
