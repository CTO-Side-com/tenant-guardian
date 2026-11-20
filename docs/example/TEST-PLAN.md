# Tenant isolation test plan
Scoped tenant-isolation assessment. Not a guarantee of isolation, penetration-test attestation or compliance certification.

Use two distinct synthetic tenants and identities. Confirm own-tenant access before every negative case.
Do not run write, queue, restore, browser, database or network tests without approval for the specific environment.
Product: Synthetic two-tenant invoice API
Environment: local
Declared architecture: Synthetic shared service with explicit object ownership checks
In-scope systems: Owned loopback invoice fixture
Declared exclusions: No customer or production services
Scope unknowns: Writes, lists, database roles, storage, caches, jobs, websockets and AI paths are not tested by this GET demonstration.
These are catalog prompts with scope context, not an inferred endpoint inventory. Confirm applicability and authorization before execution; exclusions do not automatically mark a check inapplicable.

Architecture review: trace the selected isolation mechanism before choosing database and shared-state tests. No tenant_id column or RLS requirement is inferred.

## CTX-001 | Verify tenant identity from authenticated membership
Expected boundary: Bind the selected tenant to a server-verified principal and current membership.
Suggested test: Try a valid actor with another tenant selector and verify it cannot broaden access.
Record: actor, tenant, resource, positive control, denied operation, actual result, environment and date.

## CTX-002 | Treat client tenant selectors as untrusted input
Expected boundary: Headers, subdomains and parameters select context but cannot authorize it.
Suggested test: Change tenant headers and path selectors while retaining the original synthetic identity.
Record: actor, tenant, resource, positive control, denied operation, actual result, environment and date.

## CTX-003 | Separate tenant roles from platform administration
Expected boundary: Platform-wide privileges must be explicit and audited.
Suggested test: Use a tenant administrator identity against platform-wide operations and expect denial.
Record: actor, tenant, resource, positive control, denied operation, actual result, environment and date.

## CTX-004 | Isolate request and thread tenant context
Expected boundary: A previous request cannot determine the next request's tenant.
Suggested test: Alternate and concurrently execute requests for two tenants using reused workers.
Record: actor, tenant, resource, positive control, denied operation, actual result, environment and date.

## CTX-005 | Revalidate tenant switching and revoked membership
Expected boundary: Switching and delayed actions must reflect current access.
Suggested test: Revoke synthetic membership, replay sessions and retry a tenant switch.
Record: actor, tenant, resource, positive control, denied operation, actual result, environment and date.

## API-001 | Authorize tenant-owned objects on every read path
Expected boundary: Object IDs must not bypass the resource's tenant boundary.
Suggested test: Read tenant B's known synthetic object as actor A after successful own-object baselines.
Record: actor, tenant, resource, positive control, denied operation, actual result, environment and date.

## API-002 | Authorize create update and delete operations
Expected boundary: Ownership and tenant fields cannot be reassigned by untrusted writes.
Suggested test: In an isolated fixture, attempt cross-tenant update, delete and ownership reassignment; verify state is unchanged.
Record: actor, tenant, resource, positive control, denied operation, actual result, environment and date.

## API-003 | Scope list search aggregation and count endpoints
Expected boundary: Collections and derived values must not expose other tenants.
Suggested test: Compare tenant-specific lists, search, counts, facets and pagination using distinct synthetic records.
Record: actor, tenant, resource, positive control, denied operation, actual result, environment and date.

## API-004 | Validate nested and bulk resource ownership
Expected boundary: Nested IDs and batched operations must retain per-object authorization.
Suggested test: Mix synthetic A and B IDs in a batch and mismatched parent-child paths.
Record: actor, tenant, resource, positive control, denied operation, actual result, environment and date.

## API-005 | Protect exports reports and download endpoints
Expected boundary: Export generation and retrieval must retain tenant scope.
Suggested test: Generate an authorized synthetic export and attempt retrieval as another tenant.
Record: actor, tenant, resource, positive control, denied operation, actual result, environment and date.

## API-006 | Authorize websocket subscriptions and pushed events
Expected boundary: Subscription topics and fanout recipients must be tenant scoped.
Suggested test: Subscribe with A to B's synthetic topic and trigger a safe event in a fixture.
Record: actor, tenant, resource, positive control, denied operation, actual result, environment and date.

## DB-001 | Choose and document an enforceable data isolation model
Expected boundary: Shared tables, RLS, separate schemas or separate databases can provide the boundary.
Suggested test: Trace ordinary and privileged identities through the chosen isolation mechanism.
Record: actor, tenant, resource, positive control, denied operation, actual result, environment and date.

## DB-002 | Review direct key lookups joins and raw SQL
Expected boundary: All tenant-owned query paths must cross an enforced authorization boundary.
Suggested test: Test known foreign IDs through ORM get, joins, aggregates, raw SQL and repository helpers.
Record: actor, tenant, resource, positive control, denied operation, actual result, environment and date.

## DB-003 | Review PostgreSQL row security and bypass roles
Expected boundary: When RLS is relied on, ordinary request roles must not bypass the relevant policies.
Suggested test: Inspect role and policy metadata; test SELECT and writes as the actual request role with synthetic rows.
Record: actor, tenant, resource, positive control, denied operation, actual result, environment and date.

## DB-004 | Reset tenant context across pooled database connections
Expected boundary: Pooled connections must not retain another request's tenant context.
Suggested test: Alternate synthetic tenants on a reused connection, including rollback and exception paths.
Record: actor, tenant, resource, positive control, denied operation, actual result, environment and date.

## DB-005 | Scope relations constraints and referential operations
Expected boundary: Relations and error behavior must not allow foreign-tenant linkage or disclosure.
Suggested test: Attempt cross-tenant foreign-key assignments and assess errors without relying on RLS for referential checks.
Record: actor, tenant, resource, positive control, denied operation, actual result, environment and date.

## DB-006 | Review migrations views and privileged database functions
Expected boundary: New tables, views and elevated functions must preserve intended boundaries.
Suggested test: Exercise newly introduced and privileged query paths as ordinary tenant identities.
Record: actor, tenant, resource, positive control, denied operation, actual result, environment and date.

## CACHE-001 | Namespace tenant-dependent cache entries
Expected boundary: Shared keys are safe only for intentionally global values.
Suggested test: Prime the same endpoint as B then request as A using distinguishable synthetic payloads.
Record: actor, tenant, resource, positive control, denied operation, actual result, environment and date.

## CACHE-002 | Scope authorization and memoization caches
Expected boundary: Cached permission decisions must include the security-relevant context.
Suggested test: Reuse object identifiers across tenant and role changes and inspect resulting decisions.
Record: actor, tenant, resource, positive control, denied operation, actual result, environment and date.

## CACHE-003 | Scope cache invalidation and tenant deletion
Expected boundary: Invalidation must affect only the intended tenant and data class.
Suggested test: Invalidate synthetic A entries and verify B remains intact.
Record: actor, tenant, resource, positive control, denied operation, actual result, environment and date.

## CACHE-004 | Review CDN and response caching variation
Expected boundary: Authenticated tenant responses must not be reused for another tenant.
Suggested test: Alternate credentials through the same cache URL and inspect synthetic response markers.
Record: actor, tenant, resource, positive control, denied operation, actual result, environment and date.

## STORE-001 | Authorize object access beyond path naming
Expected boundary: Prefixes and opaque names are not access control by themselves.
Suggested test: Request a known foreign synthetic object through each download and storage access path.
Record: actor, tenant, resource, positive control, denied operation, actual result, environment and date.

## STORE-002 | Bind signed links to approved resources and operations
Expected boundary: Signing must follow authorization of the exact resource and requested action.
Suggested test: Try to obtain a signed link for a foreign object; assess the documented bearer-link sharing model separately.
Record: actor, tenant, resource, positive control, denied operation, actual result, environment and date.

## STORE-003 | Constrain object paths and tenant-prefix boundaries
Expected boundary: Traversal and prefix collisions must not escape the intended storage boundary.
Suggested test: Exercise synthetic path traversal variants and neighboring tenant names such as acme and acme-west.
Record: actor, tenant, resource, positive control, denied operation, actual result, environment and date.

## STORE-004 | Scope object deletion versions and retained copies
Expected boundary: Deletion and retention must respect tenant ownership and policy.
Suggested test: Use isolated synthetic versions to check only the selected tenant's allowed copies are affected.
Record: actor, tenant, resource, positive control, denied operation, actual result, environment and date.

## JOB-001 | Authenticate queued tenant context
Expected boundary: The producer's authority and the consumer's operation must establish scope.
Suggested test: Inject a foreign tenant selector in a synthetic queue message and verify independent authorization.
Record: actor, tenant, resource, positive control, denied operation, actual result, environment and date.

## JOB-002 | Scope retry idempotency and dead-letter state
Expected boundary: Shared queues and retry keys must not mix tenant-owned actions.
Suggested test: Reuse synthetic idempotency keys across tenants and exercise retries and dead-letter access.
Record: actor, tenant, resource, positive control, denied operation, actual result, environment and date.

## JOB-003 | Bind webhooks and service credentials to authorized tenants
Expected boundary: Inbound routing and internal identities require explicit authorized scopes.
Suggested test: Replay a synthetic webhook with mismatched tenant identifiers and a valid but differently scoped credential.
Record: actor, tenant, resource, positive control, denied operation, actual result, environment and date.

## JOB-004 | Limit tenant impact on shared worker capacity
Expected boundary: Tenant workloads should not exhaust shared resources beyond intended quotas.
Suggested test: Review queue concurrency and limits; load tests require separately approved scope.
Record: actor, tenant, resource, positive control, denied operation, actual result, environment and date.

## AI-001 | Enforce tenant filtering in vector and search retrieval
Expected boundary: Retrieval must use trusted context and independent authorization.
Suggested test: Index distinct synthetic markers for A and B, then retrieve as each tenant.
Record: actor, tenant, resource, positive control, denied operation, actual result, environment and date.

## AI-002 | Isolate conversation history memory and semantic caches
Expected boundary: Thread IDs and cached embeddings must not cross user or tenant scope.
Suggested test: Reuse synthetic thread and document IDs across actors and inspect retrieval and memory results.
Record: actor, tenant, resource, positive control, denied operation, actual result, environment and date.

## AI-003 | Enforce tool authorization outside model output
Expected boundary: Model-generated tenant selectors cannot override policy gates.
Suggested test: Place a synthetic instruction requesting B's data in A's document and verify tool-side denial.
Record: actor, tenant, resource, positive control, denied operation, actual result, environment and date.

## AI-004 | Keep traces datasets and evaluation artifacts tenant safe
Expected boundary: Debugging and evaluation outputs must not expose unapproved tenant data.
Suggested test: Inspect approved synthetic traces, exports and evaluation data access boundaries.
Record: actor, tenant, resource, positive control, denied operation, actual result, environment and date.

## LIFE-001 | Verify provisioning tenant deletion and failed setup cleanup
Expected boundary: Partial setup and offboarding must retain correct tenant boundaries.
Suggested test: Simulate failed provisioning and isolated synthetic tenant deletion; verify neighboring tenants remain unchanged.
Record: actor, tenant, resource, positive control, denied operation, actual result, environment and date.

## LIFE-002 | Scope backup restore and support access
Expected boundary: Recovery and support operations need explicit target authorization.
Suggested test: Restore into an isolated fixture and verify only the selected tenant is copied; review support access approvals.
Record: actor, tenant, resource, positive control, denied operation, actual result, environment and date.

## LIFE-003 | Protect tenant audit feeds and cross-tenant administration
Expected boundary: Centralized audit storage is acceptable when tenant-facing access is scoped.
Suggested test: Read synthetic audit events as A and test platform support actions through their explicit privileged path.
Record: actor, tenant, resource, positive control, denied operation, actual result, environment and date.
