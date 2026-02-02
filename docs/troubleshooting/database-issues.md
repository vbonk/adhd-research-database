---
title: Database Issues Troubleshooting
description: Comprehensive guide for diagnosing and resolving PostgreSQL database issues in the ADHD Research Database system
audience: admin
difficulty: intermediate
---

# Database Issues Troubleshooting

This guide covers common PostgreSQL database issues encountered in the ADHD Research Database system and provides step-by-step solutions for each scenario.

## System Overview

| Component | Details |
|-----------|---------|
| Database Engine | PostgreSQL 14 |
| ORM/Schema Tool | Prisma 6.16 |
| Database Name | adhd_research |
| Database User | adhd_user |
| SQL Execution | PrismaClient wrapper via psql subprocess |

---

## Connection Issues

### Connection Refused Errors

**Symptom:**
```
Error: connect ECONNREFUSED 127.0.0.1:5432
FATAL: connection refused
psql: error: could not connect to server: Connection refused
```

**Cause:**
- PostgreSQL service is not running
- PostgreSQL is listening on a different port or interface
- Firewall blocking the connection

**Solution:**

1. Check if PostgreSQL is running:
```bash
sudo systemctl status postgresql
```

2. If stopped, start the service:
```bash
sudo systemctl start postgresql
```

3. Verify PostgreSQL is listening on the expected port:
```bash
sudo ss -tlnp | grep 5432
```

4. Check PostgreSQL configuration for listen addresses:
```bash
sudo grep -E "^(listen_addresses|port)" /etc/postgresql/14/main/postgresql.conf
```

5. If using Docker, ensure the container is running:
```bash
docker ps | grep postgres
docker start adhd-postgres  # if stopped
```

---

### Authentication Failures

**Symptom:**
```
FATAL: password authentication failed for user "adhd_user"
FATAL: Ident authentication failed for user "adhd_user"
Error: Authentication failed against database server
```

**Cause:**
- Incorrect password in connection string
- pg_hba.conf not configured for password authentication
- User does not exist in PostgreSQL

**Solution:**

1. Verify the user exists:
```bash
sudo -u postgres psql -c "SELECT usename FROM pg_user WHERE usename='adhd_user';"
```

2. Reset the user password if needed:
```bash
sudo -u postgres psql -c "ALTER USER adhd_user WITH PASSWORD 'new_secure_password';"
```

3. Check pg_hba.conf authentication method:
```bash
sudo grep adhd_user /etc/postgresql/14/main/pg_hba.conf
```

4. Ensure the line uses `md5` or `scram-sha-256` (not `ident` or `peer`):
```
# Add or modify this line in pg_hba.conf
host    adhd_research    adhd_user    127.0.0.1/32    scram-sha-256
```

5. Reload PostgreSQL configuration:
```bash
sudo systemctl reload postgresql
```

6. Update the DATABASE_URL in your .env file:
```
DATABASE_URL="postgresql://adhd_user:correct_password@localhost:5432/adhd_research"
```

---

### Permission Denied Errors

**Symptom:**
```
ERROR: permission denied for table research_papers
ERROR: permission denied for schema public
FATAL: permission denied for database "adhd_research"
```

**Cause:**
- User lacks required privileges on tables, schemas, or database
- Object ownership issues after migrations

**Solution:**

1. Grant database connection privileges:
```bash
sudo -u postgres psql -c "GRANT CONNECT ON DATABASE adhd_research TO adhd_user;"
```

2. Grant schema usage:
```bash
sudo -u postgres psql -d adhd_research -c "GRANT USAGE ON SCHEMA public TO adhd_user;"
```

3. Grant table privileges:
```bash
sudo -u postgres psql -d adhd_research -c "GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO adhd_user;"
```

4. Grant sequence privileges (required for auto-increment):
```bash
sudo -u postgres psql -d adhd_research -c "GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO adhd_user;"
```

5. Set default privileges for future objects:
```bash
sudo -u postgres psql -d adhd_research -c "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO adhd_user;"
sudo -u postgres psql -d adhd_research -c "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE, SELECT ON SEQUENCES TO adhd_user;"
```

---

### Database Does Not Exist

**Symptom:**
```
FATAL: database "adhd_research" does not exist
Error: P1003: Database `adhd_research` does not exist
```

**Cause:**
- Database was never created
- Database was dropped accidentally
- Connecting to wrong PostgreSQL instance

**Solution:**

1. List existing databases:
```bash
sudo -u postgres psql -c "\l"
```

2. Create the database if missing:
```bash
sudo -u postgres psql -c "CREATE DATABASE adhd_research OWNER adhd_user;"
```

3. Verify creation:
```bash
sudo -u postgres psql -c "\l adhd_research"
```

4. Run Prisma migrations to set up schema:
```bash
npx prisma migrate deploy
```

---

## Prisma and Migration Issues

### Migration Failures

**Symptom:**
```
Error: P3006: Migration failed to apply
Error: P3009: migrate found failed migrations in the target database
Error: Migration `20240115_add_categories` failed
```

**Cause:**
- Conflicting schema changes
- Failed migration left database in inconsistent state
- Missing dependencies between migrations

**Solution:**

1. Check migration status:
```bash
npx prisma migrate status
```

2. View failed migrations:
```bash
sudo -u postgres psql -d adhd_research -c "SELECT * FROM _prisma_migrations WHERE rolled_back_at IS NOT NULL OR finished_at IS NULL;"
```

3. For development environments, reset the database:
```bash
npx prisma migrate reset  # WARNING: Deletes all data
```

4. For production, manually fix the failed migration:
```bash
# Mark the failed migration as rolled back
sudo -u postgres psql -d adhd_research -c "UPDATE _prisma_migrations SET rolled_back_at = NOW() WHERE migration_name = '20240115_add_categories' AND finished_at IS NULL;"

# Fix the schema manually, then mark as applied
npx prisma migrate resolve --applied "20240115_add_categories"
```

5. If schema is out of sync, regenerate the client:
```bash
npx prisma generate
```

---

### Prisma Client Errors

**Symptom:**
```
Error: @prisma/client did not initialize yet
Error: PrismaClient is unable to be run in the browser
Error: Invalid `prisma.query()` invocation
```

**Cause:**
- Prisma client not generated after schema changes
- Client imported before initialization
- Schema mismatch between client and database

**Solution:**

1. Regenerate the Prisma client:
```bash
npx prisma generate
```

2. Ensure proper client initialization in code:
```javascript
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

// Ensure connection before queries
await prisma.$connect();
```

3. Validate schema matches database:
```bash
npx prisma db pull --force  # Pull current DB schema
npx prisma validate         # Validate schema file
```

4. If using the PrismaClient wrapper with psql subprocess, verify psql is available:
```bash
which psql
psql --version
```

---

### Schema Sync Problems

**Symptom:**
```
Error: P3005: The database schema is not empty
Error: Drift detected: Your database schema is not in sync
Warning: The following models are defined in the database but not in the schema
```

**Cause:**
- Manual database changes outside Prisma
- Migrations applied in different order across environments
- Schema file modified without migration

**Solution:**

1. Check for schema drift:
```bash
npx prisma migrate diff --from-schema-datamodel prisma/schema.prisma --to-schema-datasource prisma/schema.prisma
```

2. Introspect current database state:
```bash
npx prisma db pull
```

3. Create a migration to capture manual changes:
```bash
npx prisma migrate dev --name sync_manual_changes
```

4. For production, baseline the existing schema:
```bash
# Create baseline migration folder
mkdir -p prisma/migrations/0_init

# Generate SQL from current schema
npx prisma migrate diff --from-empty --to-schema-datamodel prisma/schema.prisma --script > prisma/migrations/0_init/migration.sql

# Mark as applied
npx prisma migrate resolve --applied 0_init
```

---

## Performance Issues

### Slow Queries

**Symptom:**
- API requests timing out
- Database CPU at 100%
- Queries taking several seconds

**Cause:**
- Missing indexes
- Unoptimized queries
- Table bloat from updates/deletes

**Solution:**

1. Enable query logging to identify slow queries:
```bash
sudo -u postgres psql -d adhd_research -c "ALTER SYSTEM SET log_min_duration_statement = 1000;"
sudo systemctl reload postgresql
```

2. Analyze query execution plans:
```bash
sudo -u postgres psql -d adhd_research -c "EXPLAIN ANALYZE SELECT * FROM research_papers WHERE category_id = 5;"
```

3. Check for missing indexes:
```bash
sudo -u postgres psql -d adhd_research -c "
SELECT schemaname, relname, seq_scan, seq_tup_read, idx_scan, idx_tup_fetch
FROM pg_stat_user_tables
WHERE seq_scan > idx_scan AND seq_tup_read > 10000
ORDER BY seq_tup_read DESC;
"
```

4. Create missing indexes:
```bash
sudo -u postgres psql -d adhd_research -c "CREATE INDEX CONCURRENTLY idx_papers_category ON research_papers(category_id);"
```

5. Update table statistics:
```bash
sudo -u postgres psql -d adhd_research -c "ANALYZE;"
```

6. Vacuum tables to reclaim space:
```bash
sudo -u postgres psql -d adhd_research -c "VACUUM ANALYZE research_papers;"
```

---

### Lock and Deadlock Issues

**Symptom:**
```
ERROR: deadlock detected
ERROR: canceling statement due to lock timeout
Queries hanging indefinitely
```

**Cause:**
- Long-running transactions holding locks
- Circular dependencies between transactions
- Bulk operations blocking other queries

**Solution:**

1. View current locks:
```bash
sudo -u postgres psql -d adhd_research -c "
SELECT pid, usename, pg_blocking_pids(pid) as blocked_by, query
FROM pg_stat_activity
WHERE state = 'active' AND wait_event_type = 'Lock';
"
```

2. Find blocking queries:
```bash
sudo -u postgres psql -d adhd_research -c "
SELECT blocked.pid AS blocked_pid,
       blocked.query AS blocked_query,
       blocking.pid AS blocking_pid,
       blocking.query AS blocking_query
FROM pg_stat_activity AS blocked
JOIN pg_stat_activity AS blocking ON blocking.pid = ANY(pg_blocking_pids(blocked.pid))
WHERE blocked.pid != blocked.pid;
"
```

3. Terminate blocking session (use with caution):
```bash
sudo -u postgres psql -d adhd_research -c "SELECT pg_terminate_backend(12345);"  -- Replace with actual PID
```

4. Set statement timeout to prevent long locks:
```bash
sudo -u postgres psql -d adhd_research -c "ALTER USER adhd_user SET statement_timeout = '30s';"
```

5. For deadlock prevention, ensure consistent lock ordering in application code.

---

## Storage Issues

### Disk Space Issues

**Symptom:**
```
ERROR: could not extend file: No space left on device
FATAL: could not write to log file
Database writes failing
```

**Cause:**
- Database growth exceeding disk capacity
- Transaction logs (WAL) accumulating
- Table bloat from frequent updates

**Solution:**

1. Check disk usage:
```bash
df -h /var/lib/postgresql
```

2. Check database sizes:
```bash
sudo -u postgres psql -c "SELECT pg_database.datname, pg_size_pretty(pg_database_size(pg_database.datname)) FROM pg_database ORDER BY pg_database_size(pg_database.datname) DESC;"
```

3. Find largest tables:
```bash
sudo -u postgres psql -d adhd_research -c "
SELECT relname, pg_size_pretty(pg_total_relation_size(relid))
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_total_relation_size(relid) DESC
LIMIT 10;
"
```

4. Clean up WAL files (if replication is not in use):
```bash
sudo -u postgres psql -c "SELECT pg_switch_wal();"
# Then remove old WAL files from pg_wal directory
```

5. Vacuum full to reclaim space (locks table):
```bash
sudo -u postgres psql -d adhd_research -c "VACUUM FULL research_papers;"
```

6. Archive or delete old data:
```bash
sudo -u postgres psql -d adhd_research -c "DELETE FROM audit_logs WHERE created_at < NOW() - INTERVAL '1 year';"
```

---

### Backup and Restore Failures

**Symptom:**
```
pg_dump: error: connection to database failed
pg_restore: error: could not execute query
Backup files corrupted or incomplete
```

**Cause:**
- Insufficient permissions for backup user
- Disk space exhausted during backup
- Network interruption during remote backup

**Solution:**

1. Verify backup user has required permissions:
```bash
sudo -u postgres psql -c "GRANT pg_read_all_data TO adhd_user;"  -- PostgreSQL 14+
```

2. Test backup manually:
```bash
pg_dump -U adhd_user -h localhost -d adhd_research -F c -f /tmp/test_backup.dump
```

3. Check backup file integrity:
```bash
pg_restore --list /tmp/test_backup.dump
```

4. For restore failures, check for existing objects:
```bash
pg_restore -U adhd_user -h localhost -d adhd_research --clean --if-exists -F c /path/to/backup.dump
```

5. Restore to a new database for testing:
```bash
sudo -u postgres psql -c "CREATE DATABASE adhd_research_restore OWNER adhd_user;"
pg_restore -U adhd_user -h localhost -d adhd_research_restore -F c /path/to/backup.dump
```

---

## Diagnostic Commands Reference

| Task | Command |
|------|---------|
| Check PostgreSQL status | `sudo systemctl status postgresql` |
| View PostgreSQL logs | `sudo tail -100 /var/log/postgresql/postgresql-14-main.log` |
| List databases | `sudo -u postgres psql -c "\l"` |
| List tables | `sudo -u postgres psql -d adhd_research -c "\dt"` |
| Check connections | `sudo -u postgres psql -c "SELECT * FROM pg_stat_activity;"` |
| View table sizes | `sudo -u postgres psql -d adhd_research -c "\dt+"` |
| Check locks | `sudo -u postgres psql -c "SELECT * FROM pg_locks WHERE NOT granted;"` |
| View running queries | `sudo -u postgres psql -c "SELECT pid, now() - pg_stat_activity.query_start AS duration, query FROM pg_stat_activity WHERE state = 'active';"` |
| Check replication status | `sudo -u postgres psql -c "SELECT * FROM pg_stat_replication;"` |
| View index usage | `sudo -u postgres psql -d adhd_research -c "SELECT * FROM pg_stat_user_indexes;"` |
| Check table bloat | `sudo -u postgres psql -d adhd_research -c "SELECT schemaname, relname, n_dead_tup FROM pg_stat_user_tables ORDER BY n_dead_tup DESC;"` |
| Test connection | `psql -U adhd_user -h localhost -d adhd_research -c "SELECT 1;"` |
| Check Prisma migrations | `npx prisma migrate status` |
| Validate Prisma schema | `npx prisma validate` |
| Generate Prisma client | `npx prisma generate` |

---

## Emergency Recovery Checklist

If the database is completely unresponsive:

1. **Stop the application** to prevent further connection attempts
2. **Check PostgreSQL status**: `sudo systemctl status postgresql`
3. **Check system resources**: `top`, `df -h`, `free -m`
4. **Review PostgreSQL logs**: `sudo tail -200 /var/log/postgresql/postgresql-14-main.log`
5. **Attempt graceful restart**: `sudo systemctl restart postgresql`
6. **If restart fails**, check for corrupted data files or full disk
7. **Restore from backup** if data corruption is detected
8. **Contact DBA** for complex recovery scenarios

---

## Related Documentation

- [Environment Setup](../setup/environment-setup.md)
- [Backup and Recovery](backup-recovery.md)
- [Performance Optimization](performance-optimization.md)
- [Security Configuration](../admin/security-configuration.md)

---

*Documentation generated for the ADHD Research Database project. For additional support, consult the PostgreSQL 14 documentation or contact the system administrator.*
