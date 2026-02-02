---
title: Common Issues and Troubleshooting
description: Solutions for frequently encountered problems when setting up and running the ADHD Research Database
audience: all
difficulty: intermediate
---

# Common Issues and Troubleshooting

This guide covers the most frequently encountered issues when installing, configuring, and running the ADHD Research Database. Each issue includes symptoms, causes, solutions, and prevention tips.

## Quick Diagnostic Commands

Before diving into specific issues, use these commands to quickly assess your environment:

| Check | Command | Expected Output |
|-------|---------|-----------------|
| Node.js version | `node --version` | v18.x or v20.x |
| npm version | `npm --version` | 9.x or 10.x |
| Python version | `python --version` | 3.10+ |
| Docker status | `docker info` | No errors |
| PostgreSQL connection | `docker exec adhd-db pg_isready` | accepting connections |
| App container status | `docker ps --filter name=adhd` | Containers running |
| API health | `curl http://localhost:5000/api/health` | `{"status": "healthy"}` |
| Port 5000 in use | `lsof -i :5000` | Shows process or empty |
| Port 5432 in use | `lsof -i :5432` | Shows postgres or empty |
| Disk space | `df -h` | Sufficient space available |
| Memory usage | `free -m` | Sufficient memory available |

---

## Installation Issues

### Issue 1: npm install fails with EACCES permission error

**Symptoms:**
```
npm ERR! Error: EACCES: permission denied, access '/usr/local/lib/node_modules'
npm ERR! code EACCES
```

**Cause:**
npm is trying to install packages globally in a directory that requires root permissions, or your local npm cache has incorrect permissions.

**Solution:**

Option 1 - Fix npm permissions:
```bash
# Create a directory for global packages
mkdir -p ~/.npm-global

# Configure npm to use the new directory
npm config set prefix '~/.npm-global'

# Add to your shell profile (~/.bashrc, ~/.zshrc)
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

# Retry installation
npm install
```

Option 2 - Fix cache permissions:
```bash
sudo chown -R $(whoami) ~/.npm
npm cache clean --force
npm install
```

**Prevention:**
- Avoid using `sudo` with npm install
- Set up npm prefix during initial Node.js configuration
- Use nvm (Node Version Manager) which handles permissions correctly

---

### Issue 2: npm install fails with node-gyp errors

**Symptoms:**
```
gyp ERR! build error
gyp ERR! stack Error: `make` failed with exit code: 2
npm ERR! code ELIFECYCLE
```

**Cause:**
Missing build tools required for compiling native Node.js modules.

**Solution:**

For Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install -y build-essential python3
npm install
```

For macOS:
```bash
xcode-select --install
npm install
```

For Windows:
```powershell
# Run as Administrator
npm install --global windows-build-tools
npm install
```

**Prevention:**
- Install build tools before starting the project
- Document system requirements in your setup process
- Consider using Docker to avoid build tool issues

---

### Issue 3: pip install fails with "No matching distribution"

**Symptoms:**
```
ERROR: Could not find a version that satisfies the requirement package==x.x.x
ERROR: No matching distribution found for package==x.x.x
```

**Cause:**
The specified package version does not exist, or your Python version is incompatible.

**Solution:**
```bash
# Check your Python version
python --version

# Ensure you're using Python 3.10+
python3.10 -m pip install -r requirements.txt

# Or update the package to an available version
pip install package  # Without version constraint to get latest
```

If the package requires a newer Python:
```bash
# Install pyenv for Python version management
curl https://pyenv.run | bash

# Install required Python version
pyenv install 3.11.0
pyenv local 3.11.0

# Retry
pip install -r requirements.txt
```

**Prevention:**
- Test requirements.txt with multiple Python versions
- Use version ranges instead of exact versions where possible
- Document minimum Python version clearly

---

### Issue 4: pip install fails with SSL certificate error

**Symptoms:**
```
pip is configured with locations that require TLS/SSL, however the ssl module in Python is not available
WARNING: Retrying (Retry(total=4...)) after connection broken by 'SSLError'
```

**Cause:**
Python was compiled without SSL support, or SSL certificates are outdated.

**Solution:**

For Ubuntu/Debian:
```bash
sudo apt-get install -y libssl-dev
# Reinstall Python if necessary
```

For macOS:
```bash
# Update certificates
pip install --upgrade certifi

# Or specify certificate path
pip install --cert /path/to/certificate.pem -r requirements.txt
```

Temporary workaround (not recommended for production):
```bash
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

**Prevention:**
- Keep SSL certificates updated
- Use official Python installers
- Ensure OpenSSL is installed before compiling Python

---

### Issue 5: Node.js version mismatch

**Symptoms:**
```
error engine@x.x.x: The engine "node" is incompatible with this module
error Found incompatible module
SyntaxError: Unexpected token '??='
```

**Cause:**
The installed Node.js version is older than required (project requires Node.js 18+).

**Solution:**
```bash
# Check current version
node --version

# Using nvm (recommended)
nvm install 20
nvm use 20

# Using n (alternative)
sudo npm install -g n
sudo n 20

# Verify new version
node --version

# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Prevention:**
- Use `.nvmrc` file in project root specifying Node.js version
- Add engines field to package.json
- Use Docker for consistent Node.js version

---

### Issue 6: Missing system dependencies for Prisma

**Symptoms:**
```
Error: Unknown binaryTarget linux-musl-openssl-3.0.x
Prisma Client could not locate the Query Engine binary
```

**Cause:**
Prisma requires specific OpenSSL versions and native libraries that may be missing.

**Solution:**

For Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install -y openssl libssl-dev

# Regenerate Prisma client
npx prisma generate
```

For Alpine Linux (Docker):
```dockerfile
# Add to Dockerfile
RUN apk add --no-cache openssl
```

Set binary targets in schema.prisma:
```prisma
generator client {
  provider      = "prisma-client-js"
  binaryTargets = ["native", "linux-musl-openssl-3.0.x"]
}
```

**Prevention:**
- Specify all target platforms in schema.prisma
- Use consistent base images in Docker
- Test on all deployment environments

---

## Database Issues

### Issue 7: Connection refused to PostgreSQL

**Symptoms:**
```
psycopg2.OperationalError: connection refused
Error: P1001: Can't reach database server at localhost:5432
ECONNREFUSED 127.0.0.1:5432
```

**Cause:**
PostgreSQL is not running, not accepting connections, or the connection details are wrong.

**Solution:**

Check if PostgreSQL container is running:
```bash
docker ps | grep postgres

# If not running, start it
docker-compose up -d db

# Check container logs
docker-compose logs db
```

Verify connection settings:
```bash
# Check DATABASE_URL in .env
cat .env | grep DATABASE_URL

# Expected format:
# DATABASE_URL="postgresql://user:password@localhost:5432/adhd_research"
```

Test direct connection:
```bash
docker exec -it adhd-db psql -U adhd_user -d adhd_research -c "SELECT 1"
```

If PostgreSQL is running but refusing connections:
```bash
# Check if port is exposed
docker port adhd-db

# Restart the container
docker-compose restart db
```

**Prevention:**
- Use health checks in docker-compose.yml
- Implement connection retry logic in application
- Monitor container status with alerting

---

### Issue 8: PostgreSQL authentication failed

**Symptoms:**
```
FATAL: password authentication failed for user "adhd_user"
Error: P1000: Authentication failed against database server
```

**Cause:**
Incorrect credentials in DATABASE_URL or password was changed.

**Solution:**

Verify credentials match:
```bash
# Check .env file
cat .env | grep DATABASE_URL

# Check docker-compose.yml
grep POSTGRES .env
```

Reset the password if necessary:
```bash
# Connect as postgres superuser
docker exec -it adhd-db psql -U postgres

# In psql:
ALTER USER adhd_user WITH PASSWORD 'new_password';
\q

# Update .env with new password
```

If using a fresh database:
```bash
# Remove existing volume and recreate
docker-compose down
docker volume rm adhd-research-database_postgres_data
docker-compose up -d db
```

**Prevention:**
- Use environment variables for credentials, not hardcoded values
- Document password requirements
- Use secrets management in production

---

### Issue 9: Database "adhd_research" does not exist

**Symptoms:**
```
FATAL: database "adhd_research" does not exist
Error: P1003: Database adhd_research does not exist
```

**Cause:**
The database was not created during initial setup or was accidentally dropped.

**Solution:**

Create the database manually:
```bash
# Connect to PostgreSQL as superuser
docker exec -it adhd-db psql -U postgres

# Create database
CREATE DATABASE adhd_research;
GRANT ALL PRIVILEGES ON DATABASE adhd_research TO adhd_user;
\q

# Run migrations
npx prisma migrate deploy
```

Or recreate from docker-compose:
```bash
docker-compose down
docker-compose up -d db

# Wait for database to be ready
sleep 5

# Initialize schema
npx prisma migrate deploy
npx prisma db seed
```

**Prevention:**
- Use init scripts in Docker to create database automatically
- Document database setup steps clearly
- Add database existence check to startup scripts

---

### Issue 10: Prisma migration failed

**Symptoms:**
```
Error: P3009: migrate found failed migrations
Error: P3006: Migration failed to apply cleanly
```

**Cause:**
A previous migration failed partway through, leaving the database in an inconsistent state.

**Solution:**

Check migration status:
```bash
npx prisma migrate status
```

If migrations are out of sync:
```bash
# Mark migration as applied (if already manually applied)
npx prisma migrate resolve --applied "migration_name"

# Or roll back and retry
npx prisma migrate resolve --rolled-back "migration_name"
npx prisma migrate deploy
```

For development environments, reset completely:
```bash
# WARNING: This deletes all data
npx prisma migrate reset
```

**Prevention:**
- Always test migrations on a copy of production data
- Use transactions in migrations where possible
- Keep backups before running migrations

---

### Issue 11: Database connection pool exhausted

**Symptoms:**
```
Error: P2024: Timed out fetching a new connection from the connection pool
QueuePool limit overflow
Too many connections for role "adhd_user"
```

**Cause:**
Too many concurrent connections or connections not being released properly.

**Solution:**

Increase connection pool size in DATABASE_URL:
```bash
# Add connection_limit parameter
DATABASE_URL="postgresql://user:pass@localhost:5432/db?connection_limit=20"
```

Check and terminate idle connections:
```bash
docker exec -it adhd-db psql -U postgres -d adhd_research

-- View active connections
SELECT * FROM pg_stat_activity WHERE datname = 'adhd_research';

-- Terminate idle connections
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE datname = 'adhd_research'
AND state = 'idle'
AND pid <> pg_backend_pid();
```

Increase PostgreSQL max connections:
```bash
# In docker-compose.yml, add command
command: postgres -c max_connections=200
```

**Prevention:**
- Configure appropriate pool sizes based on expected load
- Implement connection timeouts
- Monitor connection usage

---

## API Issues

### Issue 12: 500 Internal Server Error

**Symptoms:**
```
HTTP 500 Internal Server Error
{"error": "Internal server error"}
```

**Cause:**
Unhandled exception in the application code.

**Solution:**

Check application logs:
```bash
# View Flask logs
docker-compose logs app

# Or if running locally
flask run --debug
```

Common causes and fixes:

Database connection issue:
```bash
# Verify database is accessible
curl http://localhost:5000/api/health
```

Missing environment variable:
```bash
# Check all required variables are set
cat .env

# Ensure .env is loaded
export $(cat .env | xargs)
```

Enable debug mode for detailed errors:
```python
# In development only
app.config['DEBUG'] = True
```

**Prevention:**
- Implement comprehensive error handling
- Use structured logging
- Set up error monitoring (Sentry, etc.)
- Test error scenarios in CI/CD

---

### Issue 13: 404 Not Found for API endpoints

**Symptoms:**
```
HTTP 404 Not Found
{"error": "Endpoint not found"}
```

**Cause:**
Incorrect URL path, missing route registration, or blueprint not loaded.

**Solution:**

Verify correct endpoint:
```bash
# List all registered routes
flask routes

# Test with correct URL
curl http://localhost:5000/api/research
```

Check route registration:
```python
# Ensure blueprint is registered in app.py
from routes.research import research_bp
app.register_blueprint(research_bp, url_prefix='/api')
```

Common URL mistakes:
```bash
# Wrong: Missing /api prefix
curl http://localhost:5000/research

# Correct: Include /api prefix
curl http://localhost:5000/api/research

# Wrong: Trailing slash mismatch
curl http://localhost:5000/api/research/

# Check if strict_slashes is set
```

**Prevention:**
- Document all API endpoints
- Use consistent URL patterns
- Implement API versioning (/api/v1/)
- Add 404 handler with helpful message

---

### Issue 14: Empty results from API

**Symptoms:**
```json
{
  "data": [],
  "total": 0
}
```

**Cause:**
Database has no data, query filters are too restrictive, or wrong database is being queried.

**Solution:**

Verify data exists:
```bash
docker exec -it adhd-db psql -U adhd_user -d adhd_research -c "SELECT COUNT(*) FROM research_papers;"
```

Check query parameters:
```bash
# Remove filters to test
curl "http://localhost:5000/api/research"

# Then add filters one by one
curl "http://localhost:5000/api/research?year=2024"
```

Seed the database if empty:
```bash
npx prisma db seed
```

Verify correct database:
```bash
# Check DATABASE_URL points to correct database
echo $DATABASE_URL
```

**Prevention:**
- Seed development databases with sample data
- Add data existence checks in documentation
- Implement helpful messages for empty results

---

### Issue 15: CORS errors in browser

**Symptoms:**
```
Access to fetch at 'http://localhost:5000/api/research' from origin 'http://localhost:3000'
has been blocked by CORS policy
```

**Cause:**
Cross-Origin Resource Sharing is not configured to allow requests from the frontend origin.

**Solution:**

Configure CORS in Flask:
```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://localhost:5173"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

For development, allow all origins:
```python
# Development only - not for production
CORS(app, resources={r"/api/*": {"origins": "*"}})
```

Verify CORS headers in response:
```bash
curl -I -X OPTIONS http://localhost:5000/api/research \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: GET"
```

**Prevention:**
- Configure CORS during initial setup
- Document allowed origins
- Use environment variables for CORS origins
- Test frontend-backend integration early

---

### Issue 16: API request timeout

**Symptoms:**
```
Error: timeout of 30000ms exceeded
504 Gateway Timeout
```

**Cause:**
Long-running database queries, unoptimized endpoints, or resource constraints.

**Solution:**

Identify slow queries:
```bash
docker exec -it adhd-db psql -U adhd_user -d adhd_research

-- Enable query logging
ALTER SYSTEM SET log_min_duration_statement = 1000;
SELECT pg_reload_conf();

-- Check slow queries
SELECT * FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10;
```

Add database indexes:
```sql
CREATE INDEX idx_research_year ON research_papers(publication_year);
CREATE INDEX idx_research_topic ON research_papers(topic);
```

Implement pagination:
```python
@app.route('/api/research')
def get_research():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    # Limit maximum per_page
    per_page = min(per_page, 100)
```

**Prevention:**
- Set reasonable timeouts on all endpoints
- Implement pagination by default
- Monitor query performance
- Add database indexes for common queries

---

## Docker Issues

### Issue 17: Container won't start

**Symptoms:**
```
ERROR: for app  Cannot start service app: driver failed programming external connectivity
Container exited with code 1
```

**Cause:**
Port conflict, missing dependencies, configuration error, or resource constraints.

**Solution:**

Check container logs:
```bash
docker-compose logs app
```

Check for port conflicts:
```bash
# See what's using port 5000
lsof -i :5000

# Kill the process if necessary
kill -9 <PID>
```

Verify all dependencies are ready:
```bash
# Check if database is running first
docker-compose up -d db
docker-compose logs db

# Then start the app
docker-compose up -d app
```

Rebuild the container:
```bash
docker-compose build --no-cache app
docker-compose up -d app
```

**Prevention:**
- Use health checks and depends_on in docker-compose.yml
- Document required ports clearly
- Use unique ports for different projects

---

### Issue 18: Port already in use

**Symptoms:**
```
Error starting userland proxy: listen tcp 0.0.0.0:5000: bind: address already in use
Error response from daemon: Ports are not available
```

**Cause:**
Another process or container is already using the required port.

**Solution:**

Find and stop the conflicting process:
```bash
# Find process on port 5000
lsof -i :5000
# or
netstat -tlnp | grep 5000

# Kill the process
kill -9 <PID>

# Or stop conflicting container
docker stop <container_id>
```

Use a different port:
```yaml
# In docker-compose.yml
services:
  app:
    ports:
      - "5001:5000"  # Map to different host port
```

**Prevention:**
- Document all required ports
- Use docker-compose down before switching projects
- Consider using unique port ranges per project

---

### Issue 19: Docker health check failures

**Symptoms:**
```
Container unhealthy
Health check failed
```

**Cause:**
Application not responding to health check endpoint, slow startup, or misconfigured health check.

**Solution:**

Check health check configuration:
```yaml
# In docker-compose.yml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:5000/api/health"]
  interval: 30s
  timeout: 10s
  retries: 5
  start_period: 40s  # Allow time for startup
```

Verify health endpoint works:
```bash
# From inside container
docker exec adhd-app curl http://localhost:5000/api/health

# From host
curl http://localhost:5000/api/health
```

Increase health check tolerance:
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:5000/api/health"]
  interval: 30s
  timeout: 30s      # Increase timeout
  retries: 10       # More retries
  start_period: 60s # More startup time
```

**Prevention:**
- Implement a lightweight health check endpoint
- Configure appropriate start_period for slow-starting apps
- Log health check failures for debugging

---

### Issue 20: Docker volume permission issues

**Symptoms:**
```
PermissionError: [Errno 13] Permission denied
EACCES: permission denied, open '/data/file'
```

**Cause:**
Container runs as different user than host, or volume has incorrect permissions.

**Solution:**

Fix volume permissions:
```bash
# Check current permissions
ls -la ./data

# Fix permissions
sudo chown -R 1000:1000 ./data

# Or make writable by all (development only)
chmod -R 777 ./data
```

Run container as current user:
```yaml
# In docker-compose.yml
services:
  app:
    user: "${UID}:${GID}"
```

Use named volumes instead of bind mounts:
```yaml
volumes:
  app_data:
    driver: local

services:
  app:
    volumes:
      - app_data:/data
```

**Prevention:**
- Document required permissions
- Use named volumes for persistent data
- Set appropriate user in Dockerfile

---

## Data Issues

### Issue 21: Database empty after setup

**Symptoms:**
```json
{"data": [], "total": 0}
```
All API endpoints return empty results after fresh setup.

**Cause:**
Seed script was not run, or seed failed silently.

**Solution:**

Run the seed script:
```bash
npx prisma db seed
```

Verify seed completed:
```bash
docker exec -it adhd-db psql -U adhd_user -d adhd_research

-- Check table counts
SELECT
  (SELECT COUNT(*) FROM research_papers) as papers,
  (SELECT COUNT(*) FROM authors) as authors,
  (SELECT COUNT(*) FROM topics) as topics;
```

If seed fails, check for errors:
```bash
# Run with verbose output
npx prisma db seed -- --verbose
```

Manual data insert for testing:
```sql
INSERT INTO topics (name, description)
VALUES ('ADHD Medication', 'Research on ADHD medications');
```

**Prevention:**
- Add seed verification to setup scripts
- Log seed results
- Include seed in CI/CD pipeline

---

### Issue 22: Data not displaying in frontend

**Symptoms:**
- API returns data correctly when tested with curl
- Frontend shows empty state or loading forever

**Cause:**
Frontend-backend communication issue, data transformation error, or state management bug.

**Solution:**

Verify API response format:
```bash
curl http://localhost:5000/api/research | jq .
```

Check browser console for errors:
```javascript
// Open browser DevTools (F12) and check:
// 1. Network tab - is the request being made?
// 2. Console tab - any JavaScript errors?
// 3. Response tab - what data is returned?
```

Verify frontend is pointing to correct API:
```javascript
// Check API base URL in frontend config
console.log(process.env.REACT_APP_API_URL);
// or
console.log(import.meta.env.VITE_API_URL);
```

Test with hardcoded data:
```javascript
// Temporarily use mock data to isolate issue
const [data, setData] = useState([{ id: 1, title: 'Test' }]);
```

**Prevention:**
- Add loading and error states in frontend
- Log API responses during development
- Use TypeScript for type safety

---

### Issue 23: Migration creates duplicate columns

**Symptoms:**
```
Error: column "status" of relation "research_papers" already exists
```

**Cause:**
Migration was partially applied or run multiple times.

**Solution:**

Check current schema:
```bash
docker exec -it adhd-db psql -U adhd_user -d adhd_research -c "\d research_papers"
```

Mark migration as applied:
```bash
npx prisma migrate resolve --applied "20240101000000_add_status"
```

Or reset migration history (development only):
```bash
# WARNING: Resets entire database
npx prisma migrate reset
```

**Prevention:**
- Use idempotent migrations (IF NOT EXISTS)
- Test migrations on fresh database
- Track migration state in version control

---

## Performance Issues

### Issue 24: Slow API responses

**Symptoms:**
- API responses take more than 2 seconds
- Database queries are slow
- Application feels sluggish

**Cause:**
Missing database indexes, N+1 query problems, or unoptimized queries.

**Solution:**

Identify slow queries:
```sql
-- In PostgreSQL
SELECT query, calls, total_time, mean_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;
```

Add missing indexes:
```sql
-- Common indexes for research database
CREATE INDEX idx_papers_year ON research_papers(publication_year);
CREATE INDEX idx_papers_topic ON research_papers(topic_id);
CREATE INDEX idx_papers_created ON research_papers(created_at);
CREATE INDEX idx_papers_title_gin ON research_papers USING gin(to_tsvector('english', title));
```

Optimize Prisma queries:
```javascript
// Bad: N+1 query
const papers = await prisma.researchPaper.findMany();
for (const paper of papers) {
  const authors = await prisma.author.findMany({ where: { paperId: paper.id }});
}

// Good: Include related data
const papers = await prisma.researchPaper.findMany({
  include: { authors: true }
});
```

Enable query caching:
```python
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/research')
@cache.cached(timeout=300)
def get_research():
    # ...
```

**Prevention:**
- Add indexes during schema design
- Use query analysis tools
- Implement caching strategy
- Set up performance monitoring

---

### Issue 25: High memory usage

**Symptoms:**
```
Container killed due to OOM (Out of Memory)
JavaScript heap out of memory
MemoryError in Python
```

**Cause:**
Memory leaks, loading too much data at once, or insufficient container resources.

**Solution:**

Increase container memory:
```yaml
# In docker-compose.yml
services:
  app:
    deploy:
      resources:
        limits:
          memory: 1G
        reservations:
          memory: 512M
```

Implement pagination and streaming:
```python
# Don't load everything at once
def get_all_papers():
    # Bad
    return Paper.query.all()  # Loads everything into memory

    # Good
    page = request.args.get('page', 1, type=int)
    return Paper.query.paginate(page=page, per_page=50)
```

Monitor memory usage:
```bash
# Check container memory
docker stats

# Check process memory
ps aux --sort=-%mem | head
```

**Prevention:**
- Set memory limits in docker-compose.yml
- Use streaming for large datasets
- Implement pagination
- Profile memory usage regularly

---

### Issue 26: Database connection timeout under load

**Symptoms:**
```
Error: Connection timed out
QueuePool limit of size 5 overflow 10 reached
```

**Cause:**
Connection pool exhausted under high concurrent load.

**Solution:**

Increase connection pool:
```python
# SQLAlchemy
app.config['SQLALCHEMY_POOL_SIZE'] = 20
app.config['SQLALCHEMY_MAX_OVERFLOW'] = 40
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 30
```

```prisma
// Prisma - in DATABASE_URL
postgresql://user:pass@host:5432/db?connection_limit=20&pool_timeout=30
```

Use connection pooler (PgBouncer):
```yaml
# docker-compose.yml
pgbouncer:
  image: edoburu/pgbouncer
  environment:
    DATABASE_URL: postgresql://user:pass@db:5432/adhd_research
    POOL_MODE: transaction
    MAX_CLIENT_CONN: 200
```

**Prevention:**
- Configure appropriate pool sizes
- Use connection pooler in production
- Load test before deployment

---

## Diagnostic Procedures

### Full System Health Check

Run this sequence to diagnose most issues:

```bash
#!/bin/bash
echo "=== ADHD Research Database Health Check ==="

echo -e "\n1. Docker Status:"
docker-compose ps

echo -e "\n2. Container Logs (last 20 lines):"
docker-compose logs --tail=20

echo -e "\n3. Database Connection:"
docker exec adhd-db pg_isready -U adhd_user -d adhd_research

echo -e "\n4. Database Tables:"
docker exec adhd-db psql -U adhd_user -d adhd_research -c "\dt"

echo -e "\n5. Record Counts:"
docker exec adhd-db psql -U adhd_user -d adhd_research -c "
SELECT
  (SELECT COUNT(*) FROM research_papers) as papers,
  (SELECT COUNT(*) FROM authors) as authors,
  (SELECT COUNT(*) FROM topics) as topics;"

echo -e "\n6. API Health:"
curl -s http://localhost:5000/api/health | jq .

echo -e "\n7. Disk Space:"
df -h / /var/lib/docker 2>/dev/null || df -h /

echo -e "\n8. Memory Usage:"
free -m

echo -e "\n=== Health Check Complete ==="
```

### Collecting Debug Information

When reporting an issue, include this information:

```bash
# System information
uname -a
docker --version
docker-compose --version
node --version
python --version

# Container status
docker-compose ps
docker-compose logs --tail=100 > debug-logs.txt

# Environment (sanitized)
cat .env | grep -v PASSWORD | grep -v SECRET

# Database status
docker exec adhd-db pg_isready
docker exec adhd-db psql -U adhd_user -d adhd_research -c "SELECT version();"
```

---

## When to Seek Help

Contact the development team or open an issue if:

1. **Data loss occurred** - Any situation where data was unexpectedly deleted or corrupted
2. **Security concern** - Authentication bypass, exposed credentials, or suspicious activity
3. **Persistent failures** - Issue persists after following all troubleshooting steps
4. **Performance degradation** - System becomes unusable despite optimization
5. **Undocumented error** - Error message not covered in this guide

### How to Report Issues

When opening an issue, include:

1. **Description**: Clear summary of the problem
2. **Steps to reproduce**: Exact commands or actions that cause the issue
3. **Expected behavior**: What should happen
4. **Actual behavior**: What actually happens
5. **Environment**: OS, Docker version, Node.js version, Python version
6. **Logs**: Relevant error messages and logs
7. **Screenshots**: If applicable, especially for UI issues

### Support Resources

- **GitHub Issues**: For bug reports and feature requests
- **Documentation**: Check other docs in `/docs-new/` for detailed guides
- **API Reference**: `/docs-new/reference/api.md` for endpoint details
- **Architecture Guide**: `/docs-new/architecture/` for system design

---

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/14/)
- [Prisma Documentation](https://www.prisma.io/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

*This troubleshooting guide is part of the ADHD Research Database documentation. Last updated: 2024*

*Generated with the assistance of Claude AI by Anthropic*
