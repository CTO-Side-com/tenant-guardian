# Stack review prompts

## FastAPI, Next.js and other request handlers

Trace authentication, membership lookup and tenant selection independently. Review direct object lookup, GraphQL resolvers, route handlers, server actions, exports, websocket subscriptions and internal API calls. Middleware only helps when every relevant path traverses it. Verify object properties, nested IDs and collection-derived values as well as top-level endpoints.

## PostgreSQL and ORM

Do not presume RLS is mandatory for every architecture. For shared-table RLS, inspect all classified tenant-owned tables, policy command coverage, USING and WITH CHECK behavior, ordinary-role privileges, owners, superusers and BYPASSRLS. Table owners normally bypass RLS unless forced; superusers and BYPASSRLS roles remain privileged. Referential integrity checks can bypass row security and can reveal existence through errors. Review views, security-definer functions, migrations and raw SQL.

For pooled connections, prefer transaction-local tenant context where appropriate and explicitly test rollback, exception and reuse paths. Shared-table queries, schema switching and connection routing must use verified context. Separate schemas or databases still require trustworthy routing and bounded credentials. Use the bundled read-only SQL only after approval to query the specific environment; never assume its output proves runtime enforcement.

## Redis, CDN and memoization

Classify global versus tenant-dependent keys. Review permission caches, semantic caches, invalidation prefixes, object versions and response cache variation. Warm with B, read with A, then reverse. Namespace keys where the value varies by tenant; a global cache entry can be correct for intentionally shared data.

## S3-compatible storage

Prefixes are organization, not authorization. Trace object ownership and exact operation authorization before serving data or signing a link. A valid presigned link is often intentionally bearer-accessible until expiry; assess the signing endpoint, expiry and the product's sharing contract rather than treating all bearer access as a bug. Review traversal, adjacent tenant-prefix collisions, versions, deletion and replication.

## Queues and webhooks

A queue tenant field is not proof of a producer's authority. Authenticate the producer path and authorize the consumer action. Scope retries, dead-letter access and idempotency to the security-relevant context. Re-evaluate delayed operations when membership may change. Shared queues can be appropriate; review authorization and workload limits instead of demanding dedicated infrastructure without justification.

## RAG, pgvector and agents

Trace trusted tenant filters and authorization through vector search, keyword search, reranking, citations, document download, conversation history, tool calls, traces and caches. A prompt instruction is not an authorization boundary. Test a synthetic foreign instruction and known foreign markers. Similar embeddings or document IDs must not override resource scope. Document any intentionally shared corpus.
