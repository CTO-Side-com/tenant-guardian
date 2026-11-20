# Primary source register

Reviewed 2026-11-19. Recheck versions for the target application's stack. The objective titles, tests and workflow are original CTOside material; external documentation remains authoritative for its own technology. The pack makes no claim of OWASP certification or endorsement.

| Key | Source | Use |
|---|---|---|
| owasp-multitenant | [OWASP Multi-Tenant Application Security](https://cheatsheetseries.owasp.org/cheatsheets/Multi_Tenant_Security_Cheat_Sheet.html) | Tenant context and boundary review across shared infrastructure |
| owasp-bola | [OWASP API1:2023 Broken Object Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/) | Object-level authorization threat framing |
| postgres-rls | [PostgreSQL row security](https://www.postgresql.org/docs/current/ddl-rowsecurity.html) | Role bypass, owners, policies and row security limitations |
| owasp-regression | [OWASP authorization regression testing](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Regression_Testing_Cheat_Sheet.html) | Positive/negative case design and authorization matrices |

The sources inform the objectives but are not copied as a checklist. User-approved boundaries and the application architecture determine relevance. An absent filter literal or tenant_id column is not itself a confirmed failure.
