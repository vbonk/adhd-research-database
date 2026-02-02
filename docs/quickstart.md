---
title: Quickstart Guide
description: Get the ADHD Research Database running in minutes with Docker or local installation
audience: all
difficulty: beginner
---

# Quickstart Guide

Get the ADHD Research Database up and running in under 10 minutes. Choose between Docker deployment (recommended for most users) or local installation for more control over your environment.

## Prerequisites

| Requirement | Docker Path | Local Path | Purpose |
|-------------|-------------|------------|---------|
| **Git** | Required | Required | Clone repository |
| **Docker** | 20.10+ | Not needed | Container runtime |
| **Docker Compose** | 2.0+ | Not needed | Multi-container orchestration |
| **PostgreSQL** | Not needed | 14+ | Database backend |
| **Node.js** | Not needed | 22+ | Prisma ORM runtime |
| **Python** | Not needed | 3.11+ | Flask API backend |
| **npm** | Not needed | 10+ | Package management |

## Installation Paths

### Option A: Docker Installation (Recommended)

The fastest way to get started. All dependencies are containerized.

**Step 1: Clone the repository**

```bash
git clone https://github.com/yourusername/adhd-research-database.git
cd adhd-research-database
```

**Step 2: Create environment file**

```bash
cp .env.example .env
```

Or create it manually:

```bash
cat > .env << 'EOF'
DATABASE_URL="postgresql://adhd_user:adhd_password@postgres:5432/adhd_research?schema=public"
FLASK_ENV=production
FLASK_DEBUG=false
EOF
```

**Step 3: Start the containers**

```bash
docker-compose up -d
```

This starts three services:
- `adhd-research-postgres` - PostgreSQL 14 database
- `adhd-research-app` - Flask API and web interface
- Health checks ensure proper startup order

**Step 4: Run database migrations**

```bash
docker-compose exec app npx prisma migrate deploy
docker-compose exec app npx prisma generate
```

**Step 5: Load initial data**

```bash
docker-compose exec app node migrate_data.js
```

The application is now running at `http://localhost:5000`.

---

### Option B: Local Installation

For developers who need full control or want to modify the codebase.

**Step 1: Clone the repository**

```bash
git clone https://github.com/yourusername/adhd-research-database.git
cd adhd-research-database
```

**Step 2: Install and configure PostgreSQL**

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install -y postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql

# macOS (Homebrew)
brew install postgresql@14
brew services start postgresql@14
```

**Step 3: Create database and user**

```bash
sudo -u postgres psql << 'EOF'
CREATE DATABASE adhd_research;
CREATE USER adhd_user WITH PASSWORD 'your_secure_password_here';
GRANT ALL PRIVILEGES ON DATABASE adhd_research TO adhd_user;
ALTER USER adhd_user CREATEDB;
\c adhd_research
GRANT ALL ON SCHEMA public TO adhd_user;
EOF
```

**Step 4: Configure environment**

```bash
cat > .env << 'EOF'
DATABASE_URL="postgresql://adhd_user:your_secure_password_here@localhost:5432/adhd_research?schema=public"
PRISMA_SCHEMA_PATH="./prisma/schema.prisma"
EOF
```

**Step 5: Install Node.js dependencies**

```bash
npm install
```

**Step 6: Install Python dependencies**

```bash
cd adhd_research_api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..
```

**Step 7: Run database migrations**

```bash
npx prisma migrate dev --name init
npx prisma generate
node migrate_data.js
```

**Step 8: Start the application**

```bash
cd adhd_research_api
source venv/bin/activate
python src/main.py
```

The application is now running at `http://localhost:5000`.

---

## Verify Installation

### Test the API

Run this command to verify the API is responding:

```bash
curl -s http://localhost:5000/api/research/stats | python3 -m json.tool
```

**Expected output:**

```json
{
    "success": true,
    "data": {
        "total_entries": 3,
        "by_evidence_level": {
            "LEVEL_1A": 2,
            "LEVEL_2B": 1
        },
        "workplace_focused": 3,
        "total_tags": 15
    },
    "error": null
}
```

### Test the Web Interface

Open your browser and navigate to:

- **Frontend**: http://localhost:5000
- **API Explorer**: http://localhost:5000/api/research

You should see the research database interface with search and filtering capabilities.

### Verify Database Connection

```bash
# Docker installation
docker-compose exec postgres psql -U adhd_user -d adhd_research -c "SELECT COUNT(*) FROM research_entries;"

# Local installation
psql postgresql://adhd_user:your_password@localhost:5432/adhd_research -c "SELECT COUNT(*) FROM research_entries;"
```

**Expected output:**

```
 count
-------
     3
(1 row)
```

---

## System Startup Flow

```
                    STARTUP SEQUENCE
    ================================================

    [Clone Repository]
            |
            v
    +---------------+
    |  Environment  |
    |  Configuration|
    +---------------+
            |
            v
    +===============================================+
    |           DOCKER PATH    |    LOCAL PATH     |
    |===============================================|
    |                          |                   |
    |  docker-compose up -d    |  Start PostgreSQL |
    |          |               |        |          |
    |          v               |        v          |
    |  +-------------+         |  +-------------+  |
    |  | PostgreSQL  |         |  | PostgreSQL  |  |
    |  | Container   |         |  | Service     |  |
    |  +-------------+         |  +-------------+  |
    |          |               |        |          |
    |          v               |        v          |
    |  +-------------+         |  npm install      |
    |  | Flask App   |         |  pip install      |
    |  | Container   |         |        |          |
    |  +-------------+         |        v          |
    |          |               |  +-------------+  |
    |          |               |  | Flask App   |  |
    |          |               |  | (local)     |  |
    |          |               |  +-------------+  |
    +===============================================+
            |                          |
            +------------+-------------+
                         |
                         v
              +-------------------+
              |  Prisma Migrate   |
              |  & Data Seeding   |
              +-------------------+
                         |
                         v
              +-------------------+
              |  APPLICATION      |
              |  READY            |
              |                   |
              |  Frontend: :5000  |
              |  API: :5000/api   |
              +-------------------+
```

---

## Common Commands

### Docker Commands

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f app

# Restart application
docker-compose restart app

# Access database shell
docker-compose exec postgres psql -U adhd_user -d adhd_research

# Run Prisma Studio (database GUI)
docker-compose exec app npx prisma studio
```

### Local Development Commands

```bash
# Activate Python environment
cd adhd_research_api && source venv/bin/activate

# Start development server
python src/main.py

# Run database migrations
npx prisma migrate dev

# Generate Prisma client
npx prisma generate

# Open Prisma Studio
npx prisma studio
```

---

## Troubleshooting Quick Fixes

| Problem | Docker Fix | Local Fix |
|---------|-----------|-----------|
| Port 5000 in use | `docker-compose down` then retry | `lsof -i :5000` and kill process |
| Database connection failed | Check `docker-compose logs postgres` | Verify PostgreSQL is running |
| Migration errors | `docker-compose exec app npx prisma migrate reset` | `npx prisma migrate reset` |
| Empty database | Re-run `node migrate_data.js` | Re-run `node migrate_data.js` |

For detailed troubleshooting, see [Troubleshooting Guide](troubleshooting/common-issues.md).

---

## Next Steps

Now that you have the ADHD Research Database running:

1. **Explore the Interface** - Browse research entries, use search and filters
2. **Read the User Guide** - [Getting Started Guide](guides/user/getting-started.md)
3. **Learn the API** - [API Reference](reference/api-endpoints.md)
4. **Configure for Production** - [Deployment Guide](guides/admin/deployment.md)

---

## Quick Reference

| Resource | URL |
|----------|-----|
| Web Interface | http://localhost:5000 |
| API Base | http://localhost:5000/api |
| Research Entries | http://localhost:5000/api/research |
| Statistics | http://localhost:5000/api/research/stats |
| Treatments | http://localhost:5000/api/treatments |
| Assessments | http://localhost:5000/api/assessments |
| Health Check | http://localhost:5000/health |

---

*This documentation is part of the ADHD Research Database project. For questions or issues, please open a GitHub issue.*
