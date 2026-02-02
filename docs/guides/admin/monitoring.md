---
title: Monitoring Guide
description: Configure monitoring, health checks, logging, and alerting for the ADHD Research Database
audience: admin
difficulty: intermediate
---

# Monitoring Guide

This guide covers monitoring configuration, health checks, logging setup, and alerting recommendations for the ADHD Research Database system.

## Architecture Overview

```
                    +------------------+
                    |   Monitoring     |
                    |    Dashboard     |
                    +--------+---------+
                             |
              +--------------+--------------+
              |              |              |
     +--------v----+  +------v------+  +---v-----------+
     |   Metrics   |  |    Logs     |  |    Alerts     |
     |  Collector  |  | Aggregator  |  |    Manager    |
     +--------+----+  +------+------+  +-------+-------+
              |              |                 |
    +---------+--------------+-----------------+---------+
    |                                                    |
    |              Docker Network                        |
    |                                                    |
    |  +-------------+          +------------------+     |
    |  |  PostgreSQL |          |    Flask App     |     |
    |  |   :5432     |          |      :5000       |     |
    |  |             |          |                  |     |
    |  | pg_isready  |<-------->|  /health         |     |
    |  | health chk  |          |  endpoint        |     |
    |  +-------------+          +------------------+     |
    |                                                    |
    +----------------------------------------------------+
```

## Health Check Endpoints

### Application Health Endpoint

The Flask application exposes a health check endpoint at `/health`.

**Endpoint:** `GET /health`

**Response (Healthy):**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "components": {
    "database": "connected",
    "api": "operational"
  }
}
```

**Response (Unhealthy):**
```json
{
  "status": "unhealthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "components": {
    "database": "disconnected",
    "api": "operational"
  },
  "error": "Database connection failed"
}
```

**HTTP Status Codes:**
- `200 OK` - All systems operational
- `503 Service Unavailable` - One or more components unhealthy

### Testing Health Endpoint

```bash
# Local check
curl -s http://localhost:5000/health | jq .

# With timeout for monitoring scripts
curl -s --max-time 5 http://localhost:5000/health

# Check specific component
curl -s http://localhost:5000/health | jq '.components.database'
```

## Docker Health Check Configuration

### PostgreSQL Health Check

The PostgreSQL container uses `pg_isready` for health verification.

```yaml
# docker-compose.yml
services:
  postgres:
    image: postgres:15
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
    ports:
      - "5432:5432"
```

**Health Check Parameters:**
| Parameter | Value | Description |
|-----------|-------|-------------|
| interval | 10s | Time between health checks |
| timeout | 5s | Maximum time for check to complete |
| retries | 5 | Consecutive failures before unhealthy |
| start_period | 30s | Grace period during startup |

### Flask Application Health Check

```yaml
# docker-compose.yml
services:
  app:
    build: .
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    ports:
      - "5000:5000"
    depends_on:
      postgres:
        condition: service_healthy
```

### Checking Container Health Status

```bash
# View health status for all containers
docker-compose ps

# Detailed health check logs
docker inspect --format='{{json .State.Health}}' adhd-research-app | jq .

# Watch health status in real-time
watch -n 5 'docker-compose ps'
```

## Log Configuration

### Log Locations

| Component | Log Location | Description |
|-----------|--------------|-------------|
| Flask App | stdout/stderr | Application logs |
| PostgreSQL | /var/log/postgresql/ | Database logs |
| Docker | /var/lib/docker/containers/*/\*.log | Container logs |

### Flask Application Log Format

```python
# Recommended logging configuration
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
```

**Sample Log Output:**
```
2024-01-15 10:30:00 [INFO] adhd_api: Request received: GET /api/studies
2024-01-15 10:30:01 [INFO] adhd_api: Response sent: 200 OK (150ms)
2024-01-15 10:30:05 [ERROR] adhd_api: Database connection timeout
```

### Viewing Container Logs

```bash
# View application logs
docker-compose logs -f app

# View database logs
docker-compose logs -f postgres

# View last 100 lines with timestamps
docker-compose logs --tail=100 -t app

# Filter logs by time
docker-compose logs --since="2024-01-15T10:00:00" app
```

### Log Aggregation Setup

For production deployments, consider centralized log aggregation.

**Option 1: Docker Logging Driver (Recommended for small deployments)**

```yaml
# docker-compose.yml
services:
  app:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

**Option 2: Fluentd/Fluent Bit**

```yaml
# docker-compose.yml
services:
  app:
    logging:
      driver: "fluentd"
      options:
        fluentd-address: "localhost:24224"
        tag: "adhd-research.app"
```

**Option 3: Loki + Promtail (Grafana Stack)**

```yaml
# promtail-config.yml
scrape_configs:
  - job_name: adhd-research
    static_configs:
      - targets:
          - localhost
        labels:
          job: adhd-research
          __path__: /var/lib/docker/containers/*/*.log
```

## Key Metrics to Monitor

### Application Metrics

| Metric | Target | Warning | Critical |
|--------|--------|---------|----------|
| Response Time (p50) | < 100ms | > 200ms | > 500ms |
| Response Time (p99) | < 500ms | > 1000ms | > 2000ms |
| Error Rate | < 1% | > 2% | > 5% |
| Request Rate | baseline | +50% | +100% |
| Memory Usage | < 70% | > 80% | > 90% |

### Database Metrics

| Metric | Target | Warning | Critical |
|--------|--------|---------|----------|
| Active Connections | < 80% max | > 80% | > 95% |
| Query Time (avg) | < 50ms | > 100ms | > 500ms |
| Connection Pool Usage | < 70% | > 80% | > 90% |
| Disk Usage | < 70% | > 80% | > 90% |

## Database Connection Monitoring

### Check Active Connections

```sql
-- Current connection count
SELECT count(*) FROM pg_stat_activity;

-- Connections by state
SELECT state, count(*)
FROM pg_stat_activity
GROUP BY state;

-- Long-running queries (> 30 seconds)
SELECT pid, now() - pg_stat_activity.query_start AS duration, query
FROM pg_stat_activity
WHERE (now() - pg_stat_activity.query_start) > interval '30 seconds'
  AND state != 'idle';
```

### Connection Pool Monitoring Script

```bash
#!/bin/bash
# monitor-connections.sh

MAX_CONNECTIONS=100
WARNING_THRESHOLD=80
CRITICAL_THRESHOLD=95

CURRENT=$(docker-compose exec -T postgres psql -U adhd_user -d adhd_research -t -c \
  "SELECT count(*) FROM pg_stat_activity;")

PERCENTAGE=$((CURRENT * 100 / MAX_CONNECTIONS))

if [ $PERCENTAGE -ge $CRITICAL_THRESHOLD ]; then
    echo "CRITICAL: Connection usage at ${PERCENTAGE}%"
    exit 2
elif [ $PERCENTAGE -ge $WARNING_THRESHOLD ]; then
    echo "WARNING: Connection usage at ${PERCENTAGE}%"
    exit 1
else
    echo "OK: Connection usage at ${PERCENTAGE}%"
    exit 0
fi
```

## API Response Time Monitoring

### Simple Response Time Check

```bash
#!/bin/bash
# check-response-time.sh

ENDPOINT="http://localhost:5000/health"
WARNING_MS=200
CRITICAL_MS=500

RESPONSE_TIME=$(curl -o /dev/null -s -w '%{time_total}' $ENDPOINT)
RESPONSE_MS=$(echo "$RESPONSE_TIME * 1000" | bc | cut -d. -f1)

if [ $RESPONSE_MS -ge $CRITICAL_MS ]; then
    echo "CRITICAL: Response time ${RESPONSE_MS}ms"
    exit 2
elif [ $RESPONSE_MS -ge $WARNING_MS ]; then
    echo "WARNING: Response time ${RESPONSE_MS}ms"
    exit 1
else
    echo "OK: Response time ${RESPONSE_MS}ms"
    exit 0
fi
```

### Prometheus Metrics (Optional)

Add Flask-Prometheus integration for detailed metrics:

```python
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# Endpoint metrics automatically collected
# Custom metrics
metrics.info('app_info', 'Application info', version='1.0.0')
```

## Alerting Recommendations

### Alert Priority Levels

| Priority | Response Time | Examples |
|----------|---------------|----------|
| P1 - Critical | < 15 minutes | Service down, data loss risk |
| P2 - High | < 1 hour | Degraded performance, high error rate |
| P3 - Medium | < 4 hours | Warning thresholds, capacity planning |
| P4 - Low | Next business day | Informational, optimization |

### Recommended Alerts

**Critical (P1):**
- Health check endpoint returns non-200 for 3+ minutes
- Database connection failures
- Container restart loops (> 3 restarts in 5 minutes)

**High (P2):**
- Response time p99 > 2 seconds
- Error rate > 5%
- Database connection pool > 90%

**Medium (P3):**
- Response time p99 > 1 second
- Disk usage > 80%
- Memory usage > 80%

### Simple Alerting Script

```bash
#!/bin/bash
# alert-check.sh - Run via cron every minute

HEALTH_URL="http://localhost:5000/health"
ALERT_EMAIL="admin@example.com"

# Check health endpoint
HTTP_STATUS=$(curl -s -o /dev/null -w '%{http_code}' --max-time 10 $HEALTH_URL)

if [ "$HTTP_STATUS" != "200" ]; then
    echo "ALERT: Health check failed with status $HTTP_STATUS" | \
        mail -s "[CRITICAL] ADHD Research DB Health Check Failed" $ALERT_EMAIL
fi
```

## Performance Tuning Tips

### PostgreSQL Tuning

```sql
-- Recommended settings for small deployments
-- Add to postgresql.conf or docker environment

shared_buffers = 256MB
effective_cache_size = 768MB
work_mem = 16MB
maintenance_work_mem = 128MB
max_connections = 100
```

### Flask Application Tuning

```python
# Use connection pooling
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=1800
)
```

### Docker Resource Limits

```yaml
# docker-compose.yml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M

  postgres:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 1G
        reservations:
          cpus: '1.0'
          memory: 512M
```

## Monitoring Checklist

Use this checklist for production deployments:

- [ ] Health check endpoints configured and tested
- [ ] Docker health checks enabled for all services
- [ ] Log rotation configured (max-size, max-file)
- [ ] Log aggregation system chosen and deployed
- [ ] Key metrics identified and baseline established
- [ ] Alerting thresholds configured
- [ ] Alert notification channels tested
- [ ] Database connection monitoring enabled
- [ ] Response time monitoring configured
- [ ] Resource limits set in Docker Compose
- [ ] Backup monitoring configured
- [ ] Runbook created for common alerts

---

*Documentation generated for the ADHD Research Database project.*
