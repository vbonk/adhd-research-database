---
title: Configuration Guide
description: Complete guide to configuring the ADHD Research Database application environment variables, Flask settings, and deployment options
audience: admin
difficulty: intermediate
---

# Configuration Guide

This guide covers all configuration options for the ADHD Research Database application, including environment variables, Flask settings, Prisma configuration, and deployment-specific considerations.

## Environment Variables

The application uses environment variables for configuration. These can be set directly in your shell, through a `.env` file, or via your container orchestration platform.

### Core Variables

| Variable | Required | Default | Description | Example |
|----------|----------|---------|-------------|---------|
| `DATABASE_URL` | Yes | - | PostgreSQL connection string | `postgresql://user:pass@localhost:5432/adhd_db?schema=public` |
| `FLASK_ENV` | No | `production` | Application environment mode | `development`, `staging`, `production` |
| `FLASK_DEBUG` | No | `false` | Enable debug mode and auto-reload | `true`, `false` |
| `SECRET_KEY` | Yes | - | Flask session encryption key | `your-secure-random-string-here` |
| `PRISMA_SCHEMA_PATH` | No | `./prisma/schema.prisma` | Path to Prisma schema file | `/app/prisma/schema.prisma` |
| `PSQL_PATH` | No | `/usr/bin/psql` | Path to PostgreSQL client binary | `/usr/local/bin/psql` |
| `HOST` | No | `0.0.0.0` | Server bind address | `127.0.0.1` |
| `PORT` | No | `5000` | Server port | `8080` |

### Optional Variables

| Variable | Required | Default | Description | Example |
|----------|----------|---------|-------------|---------|
| `LOG_LEVEL` | No | `INFO` | Application logging level | `DEBUG`, `INFO`, `WARNING`, `ERROR` |
| `LOG_FORMAT` | No | `standard` | Log output format | `standard`, `json` |
| `CORS_ORIGINS` | No | `*` | Allowed CORS origins | `https://example.com,https://app.example.com` |
| `MAX_CONTENT_LENGTH` | No | `16777216` | Maximum request size in bytes (16MB) | `33554432` |
| `SESSION_COOKIE_SECURE` | No | `true` | Require HTTPS for session cookies | `true`, `false` |
| `SESSION_COOKIE_HTTPONLY` | No | `true` | Prevent JavaScript access to cookies | `true`, `false` |

## DATABASE_URL Configuration

The `DATABASE_URL` follows the PostgreSQL connection string format:

```
postgresql://[user]:[password]@[host]:[port]/[database]?schema=[schema]
```

### Components

| Component | Description | Example |
|-----------|-------------|---------|
| `user` | Database username | `adhd_user` |
| `password` | Database password (URL-encoded if special chars) | `myP%40ssword` |
| `host` | Database server hostname or IP | `localhost`, `db.example.com` |
| `port` | PostgreSQL port | `5432` |
| `database` | Database name | `adhd_research` |
| `schema` | PostgreSQL schema | `public` |

### Environment-Specific Examples

**Local Development:**
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/adhd_dev?schema=public
```

**Docker Compose:**
```
DATABASE_URL=postgresql://adhd_user:adhd_pass@db:5432/adhd_research?schema=public
```

**Staging:**
```
DATABASE_URL=postgresql://adhd_staging:${DB_PASSWORD}@staging-db.internal:5432/adhd_staging?schema=public
```

**Production (with SSL):**
```
DATABASE_URL=postgresql://adhd_prod:${DB_PASSWORD}@prod-db.example.com:5432/adhd_production?schema=public&sslmode=require
```

### Special Characters in Passwords

If your password contains special characters, URL-encode them:

| Character | Encoded |
|-----------|---------|
| `@` | `%40` |
| `:` | `%3A` |
| `/` | `%2F` |
| `#` | `%23` |
| `?` | `%3F` |

## Flask Configuration

### Environment Modes

**Development (`FLASK_ENV=development`):**
- Debug mode enabled by default
- Detailed error pages with stack traces
- Auto-reload on code changes
- Not suitable for production

**Production (`FLASK_ENV=production`):**
- Debug mode disabled
- Generic error pages
- Optimized for performance
- Secure defaults enabled

### Debug Mode

```bash
# Enable debug mode (development only)
FLASK_DEBUG=true

# Disable debug mode (production)
FLASK_DEBUG=false
```

**Warning:** Never enable `FLASK_DEBUG=true` in production. It exposes sensitive information and allows arbitrary code execution through the debugger.

### Secret Key

Generate a secure secret key for production:

```bash
# Using Python
python -c "import secrets; print(secrets.token_hex(32))"

# Using OpenSSL
openssl rand -hex 32
```

The secret key is used for:
- Session cookie signing
- CSRF token generation
- Flash message security

## Prisma Configuration

### Schema Path

Set the schema path if not using the default location:

```bash
PRISMA_SCHEMA_PATH=/app/prisma/schema.prisma
```

### Database Commands

The application uses Prisma for database operations. Common commands:

```bash
# Generate Prisma client
npx prisma generate

# Run migrations
npx prisma migrate deploy

# Reset database (development only)
npx prisma migrate reset
```

### PSQL Path

For direct PostgreSQL operations, specify the psql binary location:

```bash
# Linux default
PSQL_PATH=/usr/bin/psql

# macOS Homebrew
PSQL_PATH=/usr/local/bin/psql

# Docker container
PSQL_PATH=/usr/bin/psql
```

## Security Settings

### Recommended Production Settings

```bash
# Session security
SESSION_COOKIE_SECURE=true
SESSION_COOKIE_HTTPONLY=true
SESSION_COOKIE_SAMESITE=Lax

# CORS (restrict to your domains)
CORS_ORIGINS=https://yourdomain.com

# Content limits
MAX_CONTENT_LENGTH=16777216
```

### CORS Configuration

The application enables CORS for all routes by default. For production, restrict allowed origins:

```bash
# Single origin
CORS_ORIGINS=https://app.example.com

# Multiple origins (comma-separated)
CORS_ORIGINS=https://app.example.com,https://admin.example.com
```

### Secret Key Best Practices

1. Use at least 32 bytes of random data
2. Never commit secrets to version control
3. Use different keys for each environment
4. Rotate keys periodically
5. Store in secure secret management (Vault, AWS Secrets Manager)

## Logging Configuration

### Log Levels

| Level | Description | Use Case |
|-------|-------------|----------|
| `DEBUG` | Detailed diagnostic information | Development troubleshooting |
| `INFO` | General operational messages | Normal operation monitoring |
| `WARNING` | Potential issues | Non-critical problems |
| `ERROR` | Errors that need attention | Failures requiring investigation |

### Log Format

**Standard format:**
```
2024-01-15 10:30:45,123 - INFO - Request processed successfully
```

**JSON format (recommended for production):**
```json
{"timestamp": "2024-01-15T10:30:45.123Z", "level": "INFO", "message": "Request processed successfully"}
```

## Environment-Specific Configuration

### Development

```bash
# .env.development
FLASK_ENV=development
FLASK_DEBUG=true
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/adhd_dev?schema=public
SECRET_KEY=dev-secret-key-not-for-production
LOG_LEVEL=DEBUG
CORS_ORIGINS=*
SESSION_COOKIE_SECURE=false
```

### Staging

```bash
# .env.staging
FLASK_ENV=production
FLASK_DEBUG=false
DATABASE_URL=postgresql://adhd_staging:${DB_PASSWORD}@staging-db:5432/adhd_staging?schema=public
SECRET_KEY=${STAGING_SECRET_KEY}
LOG_LEVEL=INFO
LOG_FORMAT=json
CORS_ORIGINS=https://staging.example.com
SESSION_COOKIE_SECURE=true
```

### Production

```bash
# .env.production
FLASK_ENV=production
FLASK_DEBUG=false
DATABASE_URL=postgresql://adhd_prod:${DB_PASSWORD}@prod-db:5432/adhd_production?schema=public&sslmode=require
SECRET_KEY=${PRODUCTION_SECRET_KEY}
LOG_LEVEL=WARNING
LOG_FORMAT=json
CORS_ORIGINS=https://app.example.com
SESSION_COOKIE_SECURE=true
SESSION_COOKIE_HTTPONLY=true
MAX_CONTENT_LENGTH=16777216
```

## Example .env File

```bash
# ===========================================
# ADHD Research Database Configuration
# ===========================================

# Database
DATABASE_URL=postgresql://adhd_user:your_password@localhost:5432/adhd_research?schema=public

# Flask
FLASK_ENV=development
FLASK_DEBUG=true
SECRET_KEY=change-this-to-a-secure-random-string

# Paths
PRISMA_SCHEMA_PATH=./prisma/schema.prisma
PSQL_PATH=/usr/bin/psql

# Server
HOST=0.0.0.0
PORT=5000

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=standard

# Security
CORS_ORIGINS=*
SESSION_COOKIE_SECURE=false
SESSION_COOKIE_HTTPONLY=true
MAX_CONTENT_LENGTH=16777216
```

## Docker vs Local Configuration

### Key Differences

| Aspect | Local | Docker |
|--------|-------|--------|
| Database host | `localhost` | Container name (e.g., `db`) |
| File paths | Absolute system paths | Container paths |
| Network | Host network | Docker network |
| Environment | `.env` file | Docker Compose env or secrets |

### Docker Compose Example

```yaml
services:
  app:
    environment:
      - DATABASE_URL=postgresql://adhd_user:adhd_pass@db:5432/adhd_research?schema=public
      - FLASK_ENV=production
      - SECRET_KEY_FILE=/run/secrets/flask_secret
    secrets:
      - flask_secret

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=adhd_user
      - POSTGRES_PASSWORD=adhd_pass
      - POSTGRES_DB=adhd_research

secrets:
  flask_secret:
    file: ./secrets/flask_secret.txt
```

### Local Development with Docker Database

When running the app locally but using a Docker database:

```bash
# Database in Docker
DATABASE_URL=postgresql://adhd_user:adhd_pass@localhost:5432/adhd_research?schema=public

# App runs locally
HOST=127.0.0.1
PORT=5000
```

### Container Path Mappings

| Local Path | Container Path |
|------------|----------------|
| `./prisma/schema.prisma` | `/app/prisma/schema.prisma` |
| `./logs/` | `/app/logs/` |
| `./.env` | Loaded via Docker Compose |

## Troubleshooting

### Common Issues

**Database connection refused:**
- Verify `DATABASE_URL` host and port
- Check if PostgreSQL is running
- Ensure network connectivity (Docker networks)

**Secret key errors:**
- Ensure `SECRET_KEY` is set
- Check for special characters that need escaping

**CORS errors:**
- Verify `CORS_ORIGINS` includes your frontend domain
- Check for trailing slashes in origins

**Prisma schema not found:**
- Verify `PRISMA_SCHEMA_PATH` is correct
- Check file permissions

---

*This documentation is part of the ADHD Research Database project.*
