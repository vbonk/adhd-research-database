# ADHD Research Database - Deployment Guide

## Overview

This guide provides step-by-step instructions for deploying the ADHD Research Database system to production environments. The system consists of a PostgreSQL database, Flask API backend, and web frontend interface.

## Deployment Options

### Option 1: Local Development Deployment

**Prerequisites:**
- Ubuntu 22.04 or compatible Linux system
- PostgreSQL 14+
- Python 3.11+
- Node.js 22.13.0+

**Quick Start:**
```bash
# 1. Clone/copy the project files
cd /path/to/project

# 2. Set up PostgreSQL
sudo apt update && sudo apt install -y postgresql postgresql-contrib
sudo systemctl start postgresql && sudo systemctl enable postgresql

# 3. Create database and user
sudo -u postgres psql -c "CREATE DATABASE adhd_research;"
sudo -u postgres psql -c "CREATE USER adhd_user WITH PASSWORD 'adhd_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE adhd_research TO adhd_user;"
sudo -u postgres psql -c "ALTER USER adhd_user CREATEDB;"

# 4. Set up Node.js environment
npm install

# 5. Configure environment
echo 'DATABASE_URL="postgresql://adhd_user:adhd_password@localhost:5432/adhd_research?schema=public"' > .env

# 6. Run database migrations
npx prisma migrate dev --name init
npx prisma generate

# 7. Migrate data
node migrate_data.js

# 8. Start Flask application
cd adhd_research_api
source venv/bin/activate
python src/main.py
```

**Access:** http://localhost:5000

### Option 2: Production Deployment with Docker

**Create Dockerfile:**
```dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y nodejs

WORKDIR /app

# Copy package files
COPY package*.json ./
COPY adhd_research_api/requirements.txt ./

# Install dependencies
RUN npm install
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Generate Prisma client
RUN npx prisma generate

# Expose port
EXPOSE 5000

# Start command
CMD ["python", "adhd_research_api/src/main.py"]
```

**Create docker-compose.yml:**
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:14
    environment:
      POSTGRES_DB: adhd_research
      POSTGRES_USER: adhd_user
      POSTGRES_PASSWORD: adhd_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  app:
    build: .
    environment:
      DATABASE_URL: "postgresql://adhd_user:adhd_password@postgres:5432/adhd_research?schema=public"
    ports:
      - "5000:5000"
    depends_on:
      - postgres
    volumes:
      - .:/app

volumes:
  postgres_data:
```

**Deploy with Docker:**
```bash
# Build and start services
docker-compose up -d

# Run migrations
docker-compose exec app npx prisma migrate deploy
docker-compose exec app node migrate_data.js
```

### Option 3: Cloud Deployment (Railway/Heroku)

**For Railway:**
1. Connect your GitHub repository to Railway
2. Add PostgreSQL service
3. Configure environment variables:
   - `DATABASE_URL`: Provided by Railway PostgreSQL service
4. Deploy the Flask application

**For Heroku:**
1. Create Heroku app: `heroku create adhd-research-db`
2. Add PostgreSQL addon: `heroku addons:create heroku-postgresql:mini`
3. Configure buildpacks:
   ```bash
   heroku buildpacks:add heroku/nodejs
   heroku buildpacks:add heroku/python
   ```
4. Deploy: `git push heroku main`

## Environment Configuration

### Required Environment Variables

```bash
# Database connection
DATABASE_URL="postgresql://user:password@host:port/database?schema=public"

# Flask configuration
FLASK_ENV="production"
SECRET_KEY="your-secret-key-here"

# Optional: API configuration
API_RATE_LIMIT="100"
CORS_ORIGINS="https://yourdomain.com"
```

### Security Configuration

**Production Security Checklist:**
- [ ] Change default database password
- [ ] Use strong SECRET_KEY for Flask
- [ ] Enable HTTPS/TLS encryption
- [ ] Configure firewall rules
- [ ] Implement API rate limiting
- [ ] Add input validation and sanitization
- [ ] Enable database connection pooling
- [ ] Set up monitoring and logging

## Database Migration

### Initial Setup
```bash
# Run Prisma migrations
npx prisma migrate deploy

# Seed initial data
node migrate_data.js
```

### Schema Updates
```bash
# Create new migration
npx prisma migrate dev --name <migration_name>

# Apply to production
npx prisma migrate deploy
```

### Data Backup and Restore
```bash
# Backup
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore
psql $DATABASE_URL < backup_file.sql
```

## Performance Optimization

### Database Optimization
```sql
-- Add indexes for common queries
CREATE INDEX idx_research_entries_evidence_level ON research_entries(evidence_level);
CREATE INDEX idx_research_entries_publication_date ON research_entries(publication_date);
CREATE INDEX idx_research_entries_title_search ON research_entries USING gin(to_tsvector('english', title));

-- Analyze tables
ANALYZE research_entries;
ANALYZE target_populations;
```

### Application Optimization
```python
# Add to Flask app configuration
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,
    'pool_recycle': 120,
    'pool_pre_ping': True
}
```

## Monitoring and Health Checks

### Health Check Endpoints
```python
@app.route('/health')
def health_check():
    try:
        # Test database connection
        result = prisma.query_raw("SELECT 1;")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}, 500
```

### Monitoring Setup
```bash
# Install monitoring tools
pip install prometheus-flask-exporter

# Add to Flask app
from prometheus_flask_exporter import PrometheusMetrics
metrics = PrometheusMetrics(app)
```

## Troubleshooting

### Common Deployment Issues

**Database Connection Errors:**
```bash
# Test connection
psql $DATABASE_URL -c "SELECT version();"

# Check network connectivity
telnet hostname port
```

**Migration Failures:**
```bash
# Reset migrations (development only)
npx prisma migrate reset

# Check migration status
npx prisma migrate status
```

**Application Startup Errors:**
```bash
# Check logs
docker-compose logs app

# Debug mode
FLASK_DEBUG=1 python src/main.py
```

### Performance Issues

**Slow Queries:**
```sql
-- Enable query logging
ALTER SYSTEM SET log_statement = 'all';
SELECT pg_reload_conf();

-- Check slow queries
SELECT query, mean_exec_time, calls 
FROM pg_stat_statements 
ORDER BY mean_exec_time DESC 
LIMIT 10;
```

**Memory Issues:**
```bash
# Monitor memory usage
docker stats

# Adjust container limits
docker-compose.yml:
  services:
    app:
      mem_limit: 512m
```

## Maintenance

### Regular Maintenance Tasks

**Daily:**
- Monitor application logs
- Check database connectivity
- Verify API response times

**Weekly:**
- Review database performance metrics
- Update dependencies (security patches)
- Backup database

**Monthly:**
- Analyze database growth trends
- Review and optimize slow queries
- Update documentation

### Update Procedures

**Application Updates:**
```bash
# Pull latest code
git pull origin main

# Update dependencies
npm update
pip install -r requirements.txt --upgrade

# Run migrations
npx prisma migrate deploy

# Restart application
docker-compose restart app
```

**Database Updates:**
```bash
# Create migration
npx prisma migrate dev --name update_description

# Test in staging
npx prisma migrate deploy --preview-feature

# Deploy to production
npx prisma migrate deploy
```

## Rollback Procedures

### Application Rollback
```bash
# Rollback to previous version
git checkout <previous_commit>
docker-compose build app
docker-compose up -d app
```

### Database Rollback
```bash
# Restore from backup
psql $DATABASE_URL < backup_file.sql

# Or use Prisma migration rollback
npx prisma migrate resolve --rolled-back <migration_id>
```

## Support and Documentation

### Log Locations
- Application logs: `/var/log/flask/app.log`
- Database logs: `/var/log/postgresql/postgresql.log`
- System logs: `/var/log/syslog`

### Useful Commands
```bash
# Check application status
curl http://localhost:5000/health

# Database status
pg_isready -h localhost -p 5432

# View active connections
psql $DATABASE_URL -c "SELECT * FROM pg_stat_activity;"
```

This deployment guide provides comprehensive instructions for deploying the ADHD Research Database in various environments. Choose the deployment option that best fits your infrastructure and requirements.

