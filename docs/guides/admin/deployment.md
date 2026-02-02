---
title: Deployment Guide
description: Complete guide for deploying the ADHD Research Database in various environments including Docker, cloud platforms, and production configurations
audience: admin
difficulty: intermediate
---

# Deployment Guide

This guide covers deploying the ADHD Research Database application across various environments, from local Docker development to production cloud deployments.

## Architecture Overview

```
+------------------------------------------------------------------+
|                     ADHD Research Database                        |
+------------------------------------------------------------------+
|                                                                   |
|  +-------------------+     +-------------------+                  |
|  |                   |     |                   |                  |
|  |   Flask App       |     |   PostgreSQL 14   |                  |
|  |   (Python 3.11)   |<--->|   (Database)      |                  |
|  |                   |     |                   |                  |
|  |   Port: 5000      |     |   Port: 5432      |                  |
|  +-------------------+     +-------------------+                  |
|           |                         |                             |
|           v                         v                             |
|  +-------------------+     +-------------------+                  |
|  |   Health Check    |     |   postgres_data   |                  |
|  |   /health         |     |   (Volume)        |                  |
|  +-------------------+     +-------------------+                  |
|                                                                   |
|  +-------------------+                                            |
|  |   Adminer         |  (Development Profile Only)                |
|  |   Port: 8080      |                                            |
|  +-------------------+                                            |
|                                                                   |
|  Network: adhd-network (bridge)                                   |
+------------------------------------------------------------------+
```

## Prerequisites

Before deploying the ADHD Research Database, ensure you have the following installed and configured:

### Required Software

| Software | Minimum Version | Purpose |
|----------|-----------------|---------|
| Docker | 20.10+ | Container runtime |
| Docker Compose | 2.0+ | Multi-container orchestration |
| Git | 2.30+ | Source code management |
| Python | 3.11+ | Local development (optional) |

### System Requirements

| Environment | CPU | Memory | Storage |
|-------------|-----|--------|---------|
| Development | 2 cores | 4 GB | 10 GB |
| Staging | 2 cores | 4 GB | 20 GB |
| Production | 4+ cores | 8+ GB | 50+ GB |

### Network Requirements

- Outbound HTTPS access for package installation
- Inbound access to port 5000 (application)
- Inbound access to port 5432 (database, internal only recommended)
- Inbound access to port 8080 (Adminer, development only)

## Docker Compose Deployment

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-org/adhd-research-database.git
cd adhd-research-database
```

### Step 2: Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Copy the example environment file
cp .env.example .env

# Edit with your preferred editor
nano .env
```

Configure the following variables:

```bash
# Database Configuration
DATABASE_URL=postgresql://adhd_user:secure_password_here@postgres:5432/adhd_research

# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=0

# Security (generate a strong secret key)
SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
```

### Step 3: Build and Start Services

```bash
# Build the Docker images
docker compose build

# Start all services in detached mode
docker compose up -d

# Verify services are running
docker compose ps
```

### Step 4: Initialize the Database

```bash
# Run database migrations
docker compose exec app flask db upgrade

# (Optional) Seed initial data
docker compose exec app flask seed-data
```

### Step 5: Verify Deployment

```bash
# Check application health
curl http://localhost:5000/health

# Expected response:
# {"status": "healthy", "database": "connected", "timestamp": "..."}

# Check logs for any errors
docker compose logs -f app
```

### Development Profile with Adminer

For development environments, use the dev profile to include Adminer:

```bash
# Start with development profile
docker compose --profile dev up -d

# Access Adminer at http://localhost:8080
# Server: postgres
# Username: adhd_user
# Password: (from your .env)
# Database: adhd_research
```

## Docker Container Management

### Common Commands

```bash
# View running containers
docker compose ps

# View logs for all services
docker compose logs

# View logs for specific service
docker compose logs app
docker compose logs postgres

# Follow logs in real-time
docker compose logs -f app

# Restart a specific service
docker compose restart app

# Stop all services
docker compose stop

# Stop and remove containers (preserves volumes)
docker compose down

# Stop and remove containers AND volumes (data loss warning!)
docker compose down -v
```

### Container Shell Access

```bash
# Access Flask application shell
docker compose exec app bash

# Access PostgreSQL shell
docker compose exec postgres psql -U adhd_user -d adhd_research

# Run Flask CLI commands
docker compose exec app flask --help
docker compose exec app flask db migrate
docker compose exec app flask routes
```

### Resource Management

```bash
# View container resource usage
docker stats

# Inspect container details
docker compose exec app cat /proc/1/limits

# Check disk usage
docker system df
```

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | Yes | - | PostgreSQL connection string |
| `FLASK_ENV` | No | `production` | Flask environment (`development`, `production`) |
| `FLASK_DEBUG` | No | `0` | Enable debug mode (`0` or `1`) |
| `SECRET_KEY` | Yes | - | Flask session secret key (min 32 chars) |
| `LOG_LEVEL` | No | `INFO` | Logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`) |
| `MAX_CONTENT_LENGTH` | No | `16777216` | Maximum upload size in bytes (16MB) |
| `SQLALCHEMY_POOL_SIZE` | No | `5` | Database connection pool size |
| `SQLALCHEMY_MAX_OVERFLOW` | No | `10` | Max overflow connections |
| `GUNICORN_WORKERS` | No | `4` | Number of Gunicorn worker processes |
| `GUNICORN_THREADS` | No | `2` | Threads per worker |

### Database URL Format

```
postgresql://[user]:[password]@[host]:[port]/[database]
```

Examples:
```bash
# Local Docker
DATABASE_URL=postgresql://adhd_user:password@postgres:5432/adhd_research

# External database
DATABASE_URL=postgresql://adhd_user:password@db.example.com:5432/adhd_research

# With SSL
DATABASE_URL=postgresql://adhd_user:password@db.example.com:5432/adhd_research?sslmode=require
```

## Database Setup and Migrations

### Initial Setup

```bash
# Create database tables
docker compose exec app flask db upgrade

# Verify migrations
docker compose exec app flask db current

# Show migration history
docker compose exec app flask db history
```

### Creating New Migrations

```bash
# Generate migration from model changes
docker compose exec app flask db migrate -m "Add new_column to studies"

# Review the generated migration
docker compose exec app cat migrations/versions/latest_*.py

# Apply the migration
docker compose exec app flask db upgrade
```

### Rollback Migrations

```bash
# Rollback one migration
docker compose exec app flask db downgrade -1

# Rollback to specific revision
docker compose exec app flask db downgrade abc123

# Rollback all migrations (careful!)
docker compose exec app flask db downgrade base
```

### Database Maintenance

```bash
# Vacuum and analyze (optimize performance)
docker compose exec postgres psql -U adhd_user -d adhd_research -c "VACUUM ANALYZE;"

# Check database size
docker compose exec postgres psql -U adhd_user -d adhd_research -c "
  SELECT pg_size_pretty(pg_database_size('adhd_research'));
"

# List tables with sizes
docker compose exec postgres psql -U adhd_user -d adhd_research -c "
  SELECT schemaname, tablename,
         pg_size_pretty(pg_total_relation_size(schemaname || '.' || tablename)) as size
  FROM pg_tables
  WHERE schemaname = 'public'
  ORDER BY pg_total_relation_size(schemaname || '.' || tablename) DESC;
"
```

## Cloud Deployment Guides

### Railway

Railway provides simple container deployments with automatic SSL.

#### Step 1: Install Railway CLI

```bash
npm install -g @railway/cli
railway login
```

#### Step 2: Initialize Project

```bash
cd adhd-research-database
railway init
```

#### Step 3: Add PostgreSQL

```bash
railway add --plugin postgresql
```

#### Step 4: Configure Environment

```bash
# Set environment variables
railway variables set FLASK_ENV=production
railway variables set FLASK_DEBUG=0
railway variables set SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")

# DATABASE_URL is automatically set by Railway
```

#### Step 5: Deploy

```bash
railway up
```

#### Step 6: Run Migrations

```bash
railway run flask db upgrade
```

### Heroku

#### Step 1: Install Heroku CLI

```bash
# macOS
brew tap heroku/brew && brew install heroku

# Login
heroku login
```

#### Step 2: Create Application

```bash
cd adhd-research-database
heroku create adhd-research-db
```

#### Step 3: Add PostgreSQL Add-on

```bash
heroku addons:create heroku-postgresql:essential-0
```

#### Step 4: Configure Environment

```bash
heroku config:set FLASK_ENV=production
heroku config:set FLASK_DEBUG=0
heroku config:set SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
```

#### Step 5: Deploy

```bash
git push heroku main
```

#### Step 6: Run Migrations

```bash
heroku run flask db upgrade
```

#### Step 7: Scale Dynos

```bash
# Scale web dyno
heroku ps:scale web=1

# For production, consider:
heroku ps:scale web=2:standard-1x
```

### AWS (ECS/Fargate)

#### Prerequisites

- AWS CLI configured with appropriate credentials
- ECR repository created
- VPC with public and private subnets
- RDS PostgreSQL instance

#### Step 1: Build and Push Docker Image

```bash
# Authenticate with ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com

# Build image
docker build -t adhd-research-db .

# Tag for ECR
docker tag adhd-research-db:latest \
  123456789.dkr.ecr.us-east-1.amazonaws.com/adhd-research-db:latest

# Push to ECR
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/adhd-research-db:latest
```

#### Step 2: Create Task Definition

Create `ecs-task-definition.json`:

```json
{
  "family": "adhd-research-db",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "executionRoleArn": "arn:aws:iam::123456789:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "app",
      "image": "123456789.dkr.ecr.us-east-1.amazonaws.com/adhd-research-db:latest",
      "portMappings": [
        {
          "containerPort": 5000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {"name": "FLASK_ENV", "value": "production"},
        {"name": "FLASK_DEBUG", "value": "0"}
      ],
      "secrets": [
        {
          "name": "DATABASE_URL",
          "valueFrom": "arn:aws:secretsmanager:us-east-1:123456789:secret:adhd-db-url"
        },
        {
          "name": "SECRET_KEY",
          "valueFrom": "arn:aws:secretsmanager:us-east-1:123456789:secret:adhd-secret-key"
        }
      ],
      "healthCheck": {
        "command": ["CMD-SHELL", "curl -f http://localhost:5000/health || exit 1"],
        "interval": 30,
        "timeout": 5,
        "retries": 3
      },
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/adhd-research-db",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

#### Step 3: Register Task Definition

```bash
aws ecs register-task-definition --cli-input-json file://ecs-task-definition.json
```

#### Step 4: Create ECS Service

```bash
aws ecs create-service \
  --cluster adhd-cluster \
  --service-name adhd-research-db \
  --task-definition adhd-research-db \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx,subnet-yyy],securityGroups=[sg-xxx],assignPublicIp=ENABLED}" \
  --load-balancers "targetGroupArn=arn:aws:elasticloadbalancing:us-east-1:123456789:targetgroup/adhd-tg/xxx,containerName=app,containerPort=5000"
```

### Google Cloud Run

#### Step 1: Install gcloud CLI

```bash
# Install gcloud
curl https://sdk.cloud.google.com | bash

# Initialize
gcloud init

# Set project
gcloud config set project your-project-id
```

#### Step 2: Enable Required APIs

```bash
gcloud services enable run.googleapis.com
gcloud services enable sqladmin.googleapis.com
gcloud services enable secretmanager.googleapis.com
```

#### Step 3: Create Cloud SQL Instance

```bash
gcloud sql instances create adhd-db \
  --database-version=POSTGRES_14 \
  --tier=db-f1-micro \
  --region=us-central1

# Create database
gcloud sql databases create adhd_research --instance=adhd-db

# Create user
gcloud sql users create adhd_user \
  --instance=adhd-db \
  --password=secure_password_here
```

#### Step 4: Store Secrets

```bash
# Create secrets
echo -n "your-secret-key" | gcloud secrets create adhd-secret-key --data-file=-
echo -n "postgresql://adhd_user:password@/adhd_research?host=/cloudsql/project:region:adhd-db" | \
  gcloud secrets create adhd-database-url --data-file=-
```

#### Step 5: Build and Deploy

```bash
# Build with Cloud Build
gcloud builds submit --tag gcr.io/your-project/adhd-research-db

# Deploy to Cloud Run
gcloud run deploy adhd-research-db \
  --image gcr.io/your-project/adhd-research-db \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --add-cloudsql-instances your-project:us-central1:adhd-db \
  --set-env-vars FLASK_ENV=production,FLASK_DEBUG=0 \
  --set-secrets DATABASE_URL=adhd-database-url:latest,SECRET_KEY=adhd-secret-key:latest
```

#### Step 6: Run Migrations

```bash
# Connect via Cloud SQL Proxy for migrations
cloud_sql_proxy -instances=your-project:us-central1:adhd-db=tcp:5432 &

# Run migrations locally pointing to proxy
DATABASE_URL=postgresql://adhd_user:password@localhost:5432/adhd_research flask db upgrade
```

## Health Check Configuration

### Application Health Endpoint

The application exposes a health check endpoint at `/health`:

```python
# app/routes/health.py
@app.route('/health')
def health_check():
    try:
        # Check database connectivity
        db.session.execute(text('SELECT 1'))
        db_status = 'connected'
    except Exception as e:
        db_status = f'error: {str(e)}'

    return jsonify({
        'status': 'healthy' if db_status == 'connected' else 'unhealthy',
        'database': db_status,
        'timestamp': datetime.utcnow().isoformat()
    }), 200 if db_status == 'connected' else 503
```

### Docker Health Check

The Docker Compose configuration includes health checks:

```yaml
services:
  app:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  postgres:
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U adhd_user -d adhd_research"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 10s
```

### Load Balancer Health Checks

For production deployments behind a load balancer:

| Setting | Recommended Value |
|---------|-------------------|
| Path | `/health` |
| Protocol | HTTP or HTTPS |
| Port | 5000 |
| Interval | 30 seconds |
| Timeout | 10 seconds |
| Healthy threshold | 2 |
| Unhealthy threshold | 3 |

## SSL/TLS Configuration

### Local Development (Self-Signed)

```bash
# Generate self-signed certificate
openssl req -x509 -newkey rsa:4096 \
  -keyout key.pem -out cert.pem \
  -days 365 -nodes \
  -subj "/CN=localhost"

# Run with SSL
gunicorn --certfile=cert.pem --keyfile=key.pem -b 0.0.0.0:5000 app:app
```

### Production with Let's Encrypt

Using Nginx as a reverse proxy with Certbot:

```bash
# Install Certbot
apt-get install certbot python3-certbot-nginx

# Obtain certificate
certbot --nginx -d adhd-research.example.com

# Auto-renewal is configured automatically
```

### Nginx SSL Configuration

```nginx
server {
    listen 443 ssl http2;
    server_name adhd-research.example.com;

    ssl_certificate /etc/letsencrypt/live/adhd-research.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/adhd-research.example.com/privkey.pem;

    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers off;

    # Security headers
    add_header Strict-Transport-Security "max-age=63072000" always;
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

server {
    listen 80;
    server_name adhd-research.example.com;
    return 301 https://$server_name$request_uri;
}
```

### Database SSL

For production databases, always use SSL:

```bash
# Connection string with SSL
DATABASE_URL=postgresql://user:pass@host:5432/db?sslmode=require

# For stricter verification
DATABASE_URL=postgresql://user:pass@host:5432/db?sslmode=verify-full&sslrootcert=/path/to/ca.crt
```

## Backup Strategies

### Manual Database Backup

```bash
# Full database backup
docker compose exec postgres pg_dump -U adhd_user -d adhd_research > backup_$(date +%Y%m%d_%H%M%S).sql

# Compressed backup
docker compose exec postgres pg_dump -U adhd_user -d adhd_research | gzip > backup_$(date +%Y%m%d_%H%M%S).sql.gz

# Custom format (recommended for large databases)
docker compose exec postgres pg_dump -U adhd_user -d adhd_research -Fc > backup_$(date +%Y%m%d_%H%M%S).dump
```

### Restore from Backup

```bash
# Restore from SQL file
docker compose exec -T postgres psql -U adhd_user -d adhd_research < backup.sql

# Restore from compressed file
gunzip -c backup.sql.gz | docker compose exec -T postgres psql -U adhd_user -d adhd_research

# Restore from custom format
docker compose exec -T postgres pg_restore -U adhd_user -d adhd_research -c backup.dump
```

### Automated Backup Script

Create `scripts/backup.sh`:

```bash
#!/bin/bash
set -e

BACKUP_DIR="/backups/adhd-research"
RETENTION_DAYS=30
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Create backup
echo "Creating backup..."
docker compose exec -T postgres pg_dump -U adhd_user -d adhd_research -Fc > "$BACKUP_DIR/backup_$DATE.dump"

# Verify backup
if [ -f "$BACKUP_DIR/backup_$DATE.dump" ]; then
    SIZE=$(du -h "$BACKUP_DIR/backup_$DATE.dump" | cut -f1)
    echo "Backup created successfully: $SIZE"
else
    echo "Backup failed!"
    exit 1
fi

# Remove old backups
echo "Removing backups older than $RETENTION_DAYS days..."
find "$BACKUP_DIR" -name "backup_*.dump" -mtime +$RETENTION_DAYS -delete

# List current backups
echo "Current backups:"
ls -lh "$BACKUP_DIR"
```

### Cron Schedule for Automated Backups

```bash
# Edit crontab
crontab -e

# Add daily backup at 2 AM
0 2 * * * /path/to/adhd-research-database/scripts/backup.sh >> /var/log/adhd-backup.log 2>&1
```

### Cloud Backup Strategies

#### AWS S3

```bash
# Install AWS CLI
pip install awscli

# Upload backup to S3
aws s3 cp backup.dump s3://adhd-backups/$(date +%Y/%m/%d)/backup.dump

# Sync backup directory
aws s3 sync /backups/adhd-research s3://adhd-backups/ --delete
```

#### Google Cloud Storage

```bash
# Upload to GCS
gsutil cp backup.dump gs://adhd-backups/$(date +%Y/%m/%d)/backup.dump

# Sync backup directory
gsutil rsync -d /backups/adhd-research gs://adhd-backups/
```

## Scaling Considerations

### Horizontal Scaling

```
+------------------------------------------------------------------+
|                     Load Balanced Architecture                    |
+------------------------------------------------------------------+
|                                                                   |
|                    +------------------+                           |
|                    |   Load Balancer  |                           |
|                    |   (Nginx/ALB)    |                           |
|                    +--------+---------+                           |
|                             |                                     |
|         +-------------------+-------------------+                 |
|         |                   |                   |                 |
|  +------v------+    +-------v-----+    +-------v-----+           |
|  |  App Node 1 |    |  App Node 2 |    |  App Node 3 |           |
|  |  (Flask)    |    |  (Flask)    |    |  (Flask)    |           |
|  +------+------+    +-------+-----+    +-------+-----+           |
|         |                   |                   |                 |
|         +-------------------+-------------------+                 |
|                             |                                     |
|                    +--------v---------+                           |
|                    |   PostgreSQL     |                           |
|                    |   (Primary)      |                           |
|                    +--------+---------+                           |
|                             |                                     |
|                    +--------v---------+                           |
|                    |   PostgreSQL     |                           |
|                    |   (Read Replica) |                           |
|                    +------------------+                           |
+------------------------------------------------------------------+
```

### Docker Swarm Scaling

```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml adhd-research

# Scale app service
docker service scale adhd-research_app=3

# View service status
docker service ls
docker service ps adhd-research_app
```

### Kubernetes Scaling

```yaml
# kubernetes/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: adhd-research-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: adhd-research
  template:
    metadata:
      labels:
        app: adhd-research
    spec:
      containers:
      - name: app
        image: adhd-research-db:latest
        ports:
        - containerPort: 5000
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: adhd-research-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: adhd-research-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### Database Connection Pooling

For scaled deployments, use PgBouncer:

```yaml
# docker-compose.prod.yml
services:
  pgbouncer:
    image: edoburu/pgbouncer:1.18.0
    environment:
      DATABASE_URL: postgresql://adhd_user:password@postgres:5432/adhd_research
      POOL_MODE: transaction
      MAX_CLIENT_CONN: 1000
      DEFAULT_POOL_SIZE: 20
    ports:
      - "6432:5432"
    depends_on:
      - postgres
```

Update application to connect through PgBouncer:

```bash
DATABASE_URL=postgresql://adhd_user:password@pgbouncer:5432/adhd_research
```

### Performance Tuning

#### PostgreSQL Configuration

```sql
-- Adjust for available memory (example: 4GB server)
ALTER SYSTEM SET shared_buffers = '1GB';
ALTER SYSTEM SET effective_cache_size = '3GB';
ALTER SYSTEM SET work_mem = '256MB';
ALTER SYSTEM SET maintenance_work_mem = '512MB';

-- Reload configuration
SELECT pg_reload_conf();
```

#### Gunicorn Workers

Calculate optimal workers:

```bash
# Formula: (2 x CPU cores) + 1
# For 4-core server:
GUNICORN_WORKERS=9

# With threads
gunicorn -w 4 --threads 2 -b 0.0.0.0:5000 app:app
```

## Troubleshooting

### Common Issues

#### Container Won't Start

```bash
# Check logs
docker compose logs app

# Check container status
docker compose ps

# Inspect container
docker inspect adhd-research-database-app-1
```

#### Database Connection Failed

```bash
# Verify postgres is running
docker compose ps postgres

# Test connection
docker compose exec postgres pg_isready -U adhd_user

# Check network
docker network inspect adhd-network
```

#### Health Check Failing

```bash
# Test health endpoint directly
docker compose exec app curl -v http://localhost:5000/health

# Check app logs
docker compose logs --tail=50 app
```

### Debug Mode

For troubleshooting, temporarily enable debug mode:

```bash
# Update environment
docker compose exec app env FLASK_DEBUG=1

# Or restart with debug
FLASK_DEBUG=1 docker compose up app
```

---

*This documentation is part of the ADHD Research Database project. For more information, see the [main documentation](../../index.md).*
