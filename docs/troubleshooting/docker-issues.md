---
title: Docker Troubleshooting Guide
description: Solutions for common Docker and Docker Compose issues in the ADHD Research Database environment
audience: admin
difficulty: intermediate
---

# Docker Troubleshooting Guide

This guide covers common Docker issues you may encounter when running the ADHD Research Database application, including container startup failures, networking problems, and resource constraints.

## Environment Overview

The application uses Docker Compose with the following services:

| Service | Port | Purpose |
|---------|------|---------|
| postgres | 5432 | PostgreSQL database |
| app | 5000 | Flask application |
| adminer | 8080 | Database admin (dev profile) |

Additional components:
- **Volume**: `postgres_data` for database persistence
- **Network**: `adhd-network` (bridge driver)

---

## Container Won't Start

### Symptom

Container exits immediately after starting or fails to start entirely.

```
ERROR: Container adhd-app exited with code 1
```

### Common Causes

1. **Missing environment variables**
2. **Configuration file errors**
3. **Dependency service not ready**
4. **Entrypoint script failures**

### Solution

1. Check container logs for specific errors:
   ```bash
   docker-compose logs app
   docker-compose logs postgres
   ```

2. Verify environment variables are set:
   ```bash
   docker-compose config
   ```

3. Check if required files exist:
   ```bash
   docker-compose config --services
   ls -la .env
   ```

4. Start with verbose output:
   ```bash
   docker-compose up --no-start
   docker-compose start app
   docker logs -f adhd-app
   ```

5. Verify dependency services are healthy:
   ```bash
   docker-compose ps
   docker inspect --format='{{.State.Health.Status}}' adhd-postgres
   ```

---

## Network Connectivity Issues

### Symptom

Services cannot communicate with each other.

```
ERROR: could not connect to server: Connection refused
    Is the server running on host "postgres" and accepting TCP/IP connections on port 5432?
```

### Common Causes

1. **Service not on the same network**
2. **Service name resolution failure**
3. **Firewall blocking internal traffic**
4. **Network not created**

### Solution

1. Verify all services are on `adhd-network`:
   ```bash
   docker network inspect adhd-network
   ```

2. Test connectivity from app container:
   ```bash
   docker-compose exec app ping postgres
   docker-compose exec app nc -zv postgres 5432
   ```

3. Recreate the network if corrupted:
   ```bash
   docker-compose down
   docker network rm adhd-network
   docker-compose up -d
   ```

4. Check DNS resolution:
   ```bash
   docker-compose exec app cat /etc/hosts
   docker-compose exec app nslookup postgres
   ```

5. Verify network driver:
   ```bash
   docker network ls --filter name=adhd-network
   ```

---

## Volume Mount Problems

### Symptom

Data not persisting between restarts, or permission denied errors.

```
ERROR: permission denied while trying to connect to the Docker daemon socket
ERROR: PostgreSQL data directory has wrong ownership
```

### Common Causes

1. **Volume not created**
2. **Permission mismatch**
3. **Volume driver issues**
4. **Disk space exhaustion**

### Solution

1. Check volume exists and is mounted:
   ```bash
   docker volume ls | grep postgres_data
   docker volume inspect postgres_data
   ```

2. Verify volume contents:
   ```bash
   docker run --rm -v postgres_data:/data alpine ls -la /data
   ```

3. Fix permissions (use with caution):
   ```bash
   docker run --rm -v postgres_data:/data alpine chown -R 999:999 /data
   ```

4. Check available disk space:
   ```bash
   df -h
   docker system df
   ```

5. Recreate volume if corrupted (WARNING: data loss):
   ```bash
   docker-compose down
   docker volume rm postgres_data
   docker-compose up -d
   ```

---

## Health Check Failures

### Symptom

Container marked as unhealthy, dependent services won't start.

```
adhd-postgres    Up (unhealthy)
adhd-app         Waiting
```

### Common Causes

1. **Service not fully initialized**
2. **Health check command failing**
3. **Timeout too short**
4. **Resource constraints**

### Solution

1. Check health check status:
   ```bash
   docker inspect --format='{{json .State.Health}}' adhd-postgres | jq
   ```

2. Run health check manually:
   ```bash
   # For postgres
   docker-compose exec postgres pg_isready -U adhd_user -d adhd_research

   # For app
   docker-compose exec app curl -f http://localhost:5000/health
   ```

3. View health check logs:
   ```bash
   docker inspect --format='{{range .State.Health.Log}}{{.Output}}{{end}}' adhd-postgres
   ```

4. Increase health check intervals in docker-compose.yml:
   ```yaml
   healthcheck:
     test: ["CMD", "pg_isready", "-U", "adhd_user"]
     interval: 30s
     timeout: 10s
     retries: 5
     start_period: 60s
   ```

5. Check container resource usage:
   ```bash
   docker stats adhd-postgres --no-stream
   ```

---

## Resource Constraints

### Symptom

Containers killed unexpectedly, slow performance, or OOM errors.

```
ERROR: Container killed due to OOM
ERROR: Cannot allocate memory
```

### Common Causes

1. **Insufficient memory limits**
2. **CPU throttling**
3. **Disk I/O bottlenecks**
4. **Too many concurrent connections**

### Solution

1. Check current resource usage:
   ```bash
   docker stats --no-stream
   ```

2. View container limits:
   ```bash
   docker inspect --format='{{.HostConfig.Memory}}' adhd-app
   docker inspect --format='{{.HostConfig.NanoCpus}}' adhd-app
   ```

3. Increase memory limits in docker-compose.yml:
   ```yaml
   services:
     app:
       deploy:
         resources:
           limits:
             memory: 1G
             cpus: '1.0'
           reservations:
             memory: 512M
   ```

4. Check host system resources:
   ```bash
   free -h
   top -bn1 | head -20
   ```

5. Prune unused Docker resources:
   ```bash
   docker system prune -f
   docker volume prune -f
   ```

---

## Image Build Failures

### Symptom

Docker build fails during image creation.

```
ERROR: failed to solve: failed to compute cache key
ERROR: Service 'app' failed to build
```

### Common Causes

1. **Dockerfile syntax errors**
2. **Missing build context files**
3. **Network issues during package installation**
4. **Insufficient disk space**

### Solution

1. Build with verbose output:
   ```bash
   docker-compose build --no-cache --progress=plain app
   ```

2. Verify build context:
   ```bash
   cat .dockerignore
   ls -la $(docker-compose config | grep context | awk '{print $2}')
   ```

3. Check Dockerfile syntax:
   ```bash
   docker build --check .
   ```

4. Clear build cache:
   ```bash
   docker builder prune -f
   ```

5. Build specific stage for debugging:
   ```bash
   docker build --target base -t adhd-app:debug .
   ```

---

## Docker Compose Errors

### Symptom

Docker Compose commands fail with configuration errors.

```
ERROR: The Compose file is invalid
ERROR: Version in "./docker-compose.yml" is unsupported
```

### Common Causes

1. **YAML syntax errors**
2. **Invalid version specification**
3. **Missing required fields**
4. **Environment variable substitution failures**

### Solution

1. Validate compose file:
   ```bash
   docker-compose config
   ```

2. Check YAML syntax:
   ```bash
   python3 -c "import yaml; yaml.safe_load(open('docker-compose.yml'))"
   ```

3. Verify environment variables:
   ```bash
   docker-compose config --resolve-image-digests
   ```

4. Use specific compose file:
   ```bash
   docker-compose -f docker-compose.yml -f docker-compose.dev.yml config
   ```

5. Check Docker Compose version compatibility:
   ```bash
   docker-compose version
   docker version
   ```

---

## Container Crashes and Restarts

### Symptom

Container repeatedly restarts or exits unexpectedly.

```
adhd-app    Restarting (1) 5 seconds ago
```

### Common Causes

1. **Application errors**
2. **Signal handling issues**
3. **Dependency failures**
4. **Configuration problems**

### Solution

1. Check restart count and exit code:
   ```bash
   docker inspect --format='{{.RestartCount}}' adhd-app
   docker inspect --format='{{.State.ExitCode}}' adhd-app
   ```

2. View logs before crash:
   ```bash
   docker logs --tail 100 adhd-app
   docker-compose logs --tail 100 app
   ```

3. Run container interactively for debugging:
   ```bash
   docker-compose run --rm app /bin/bash
   ```

4. Check for OOM kills:
   ```bash
   dmesg | grep -i "killed process"
   docker inspect --format='{{.State.OOMKilled}}' adhd-app
   ```

5. Temporarily disable restart policy:
   ```bash
   docker update --restart=no adhd-app
   docker start adhd-app
   docker logs -f adhd-app
   ```

---

## Port Binding Issues

### Symptom

Port already in use error when starting containers.

```
ERROR: Bind for 0.0.0.0:5000 failed: port is already allocated
ERROR: address already in use
```

### Common Causes

1. **Another process using port 5000**
2. **Previous container not fully stopped**
3. **Host service conflict**
4. **Docker proxy issues**

### Solution

1. Find process using the port:
   ```bash
   # Linux
   sudo lsof -i :5000
   sudo netstat -tlnp | grep 5000

   # Alternative
   sudo ss -tlnp | grep 5000
   ```

2. Check for zombie containers:
   ```bash
   docker ps -a | grep adhd
   docker-compose ps
   ```

3. Force stop conflicting containers:
   ```bash
   docker-compose down
   docker stop $(docker ps -q --filter "publish=5000")
   ```

4. Kill the process using the port:
   ```bash
   sudo kill $(sudo lsof -t -i:5000)
   ```

5. Use alternative port mapping:
   ```bash
   # Temporary override
   docker-compose run -p 5001:5000 app
   ```

6. Check Docker proxy:
   ```bash
   ps aux | grep docker-proxy
   ```

---

## Log Access Problems

### Symptom

Cannot view or access container logs.

```
ERROR: No such container: adhd-app
ERROR: logs are not available for this container
```

### Common Causes

1. **Container doesn't exist**
2. **Logging driver misconfiguration**
3. **Log rotation issues**
4. **Disk space exhaustion**

### Solution

1. Verify container exists:
   ```bash
   docker ps -a --filter name=adhd
   ```

2. Check logging driver:
   ```bash
   docker inspect --format='{{.HostConfig.LogConfig.Type}}' adhd-app
   ```

3. Access logs directly:
   ```bash
   # Find log file location
   docker inspect --format='{{.LogPath}}' adhd-app

   # Read log file
   sudo cat $(docker inspect --format='{{.LogPath}}' adhd-app)
   ```

4. Configure log rotation in docker-compose.yml:
   ```yaml
   services:
     app:
       logging:
         driver: "json-file"
         options:
           max-size: "10m"
           max-file: "3"
   ```

5. Check disk space for logs:
   ```bash
   sudo du -sh /var/lib/docker/containers/*/
   ```

---

## Diagnostic Commands Reference

| Command | Purpose |
|---------|---------|
| `docker-compose ps` | List service status |
| `docker-compose logs -f [service]` | Stream service logs |
| `docker-compose config` | Validate compose file |
| `docker stats` | Real-time resource usage |
| `docker system df` | Disk usage summary |
| `docker network inspect adhd-network` | Network details |
| `docker volume inspect postgres_data` | Volume details |
| `docker inspect [container]` | Full container details |
| `docker-compose exec [service] sh` | Shell into container |
| `docker events` | Real-time Docker events |
| `docker-compose top` | Running processes |
| `docker system prune` | Clean unused resources |

---

## Quick Diagnostic Script

Run this script to gather diagnostic information:

```bash
#!/bin/bash
echo "=== Docker Version ==="
docker version --format '{{.Server.Version}}'

echo -e "\n=== Docker Compose Version ==="
docker-compose version --short

echo -e "\n=== Service Status ==="
docker-compose ps

echo -e "\n=== Resource Usage ==="
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"

echo -e "\n=== Network Status ==="
docker network inspect adhd-network --format '{{range .Containers}}{{.Name}}: {{.IPv4Address}}{{"\n"}}{{end}}'

echo -e "\n=== Volume Status ==="
docker volume ls --filter name=postgres_data

echo -e "\n=== Recent Logs (last 20 lines) ==="
docker-compose logs --tail 20

echo -e "\n=== Health Status ==="
for container in adhd-postgres adhd-app; do
    status=$(docker inspect --format='{{.State.Health.Status}}' $container 2>/dev/null || echo "N/A")
    echo "$container: $status"
done
```

---

## When to Escalate

Contact the development team if:

- Database corruption is suspected
- Persistent network issues after following all steps
- Resource constraints cannot be resolved with available hardware
- Security-related container compromises
- Reproducible bugs in container behavior

---

## Related Documentation

- [Database Troubleshooting](database-issues.md)
- [Application Errors](application-errors.md)
- [Getting Started Guide](../getting-started/installation.md)

---

*Documentation generated with AI assistance. Last updated: 2026-02-02.*
