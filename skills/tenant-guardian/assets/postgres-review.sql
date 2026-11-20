-- Read-only metadata prompts. Run only on an explicitly authorized environment.
-- Review schema/table names before sharing; this does not execute tenant queries.
SELECT current_user, rolname, rolsuper, rolbypassrls
FROM pg_roles WHERE rolname = current_user;

SELECT n.nspname AS schema_name, c.relname AS table_name,
       c.relrowsecurity AS row_security_enabled,
       c.relforcerowsecurity AS owner_subject_to_row_security,
       pg_get_userbyid(c.relowner) AS table_owner
FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace
WHERE c.relkind IN ('r','p') AND n.nspname NOT IN ('pg_catalog','information_schema')
ORDER BY n.nspname,c.relname;

SELECT schemaname,tablename,policyname,permissive,roles,cmd,qual,with_check
FROM pg_policies ORDER BY schemaname,tablename,policyname;
