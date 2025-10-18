# Setup Guide

## Environment Configuration

This project requires environment variables for secure configuration. Follow these steps to set up your development environment.

### 1. Create Environment File

Copy the example environment file:

```bash
cp .env.example .env
```

### 2. Configure Database Connection

Edit `.env` and update the `DATABASE_URL`:

```env
DATABASE_URL=postgresql://your_username:your_password@localhost:5432/adhd_research
```

**Important Security Notes:**
- NEVER commit the `.env` file to version control (it's already in `.gitignore`)
- Use a strong, unique password for your database
- In production, use a secrets manager (e.g., AWS Secrets Manager, Azure Key Vault)

### 3. Configure PostgreSQL Path

Update `PSQL_PATH` in `.env` based on your PostgreSQL installation:

**Homebrew on Apple Silicon (M1/M2/M3):**
```env
PSQL_PATH=/opt/homebrew/opt/postgresql@14/bin/psql
```

**Homebrew on Intel Mac:**
```env
PSQL_PATH=/usr/local/opt/postgresql@14/bin/psql
```

**System Installation:**
```env
PSQL_PATH=/usr/bin/psql
```

**Find your psql path:**
```bash
which psql
```

### 4. Set Prisma Schema Path

Update `PRISMA_SCHEMA_PATH` with the absolute path to your schema:

```env
PRISMA_SCHEMA_PATH=/absolute/path/to/adhd-research-database/prisma/schema.prisma
```

### 5. Install Dependencies

```bash
cd adhd_research_api
pip install -r requirements.txt
```

### 6. Verify Configuration

Test your database connection:

```python
from src.database_config import prisma

# This should connect without errors
entries = prisma.find_many_research_entries(include_relations=False)
print(f"Found {len(entries)} research entries")
```

## Upgrading from Previous Version

If you're upgrading from a version with hardcoded credentials:

### CRITICAL: Security Actions Required

1. **Create `.env` file** (see steps above)
2. **Rotate database password immediately**:
   ```sql
   ALTER USER adhd_user WITH PASSWORD 'new_strong_password_here';
   ```
3. **Update `.env`** with new password
4. **Verify old password is revoked**:
   ```bash
   # This should fail:
   psql postgresql://adhd_user:adhd_password@localhost:5432/adhd_research
   
   # This should work:
   psql $DATABASE_URL  # from your .env
   ```

### Why Password Rotation is Critical

The previous version had the database password `adhd_password` hardcoded in source code. Since this is a public repository, this password was visible to anyone. You MUST:

1. Change the database password
2. Update all applications using this database
3. Audit database logs for unauthorized access

## Production Deployment

### Environment Variables in Production

**DO NOT** use `.env` files in production. Instead:

1. **Docker**: Use docker secrets or environment variables
   ```yaml
   environment:
     - DATABASE_URL=${DATABASE_URL}
   ```

2. **Kubernetes**: Use Kubernetes secrets
   ```yaml
   env:
     - name: DATABASE_URL
       valueFrom:
         secretKeyRef:
           name: db-credentials
           key: url
   ```

3. **Cloud Platforms**:
   - AWS: Use Systems Manager Parameter Store or Secrets Manager
   - Azure: Use Azure Key Vault
   - Google Cloud: Use Secret Manager

### Security Checklist

Before deploying to production:

- [ ] `.env` file is NOT committed to git
- [ ] Production database uses strong password (20+ characters)
- [ ] Database password is stored in secrets manager
- [ ] Database user has minimal required permissions
- [ ] SSL/TLS is enabled for database connections
- [ ] Application uses HTTPS only
- [ ] Rate limiting is configured
- [ ] Dependencies are up to date (`pip list --outdated`)
- [ ] Security headers are configured
- [ ] Logging and monitoring are enabled

## Troubleshooting

### "DATABASE_URL environment variable is required"

You haven't created a `.env` file or the `DATABASE_URL` is not set. Follow steps 1-2 above.

### "Connection refused" or "could not connect to server"

1. Verify PostgreSQL is running: `brew services list` (macOS) or `systemctl status postgresql` (Linux)
2. Check database URL is correct in `.env`
3. Verify database exists: `psql -l`

### "psql: command not found"

Update `PSQL_PATH` in `.env` with the correct path to psql (see step 3).

## Support

For security issues, see [SECURITY.md](SECURITY.md).

For general support, create a GitHub issue.
