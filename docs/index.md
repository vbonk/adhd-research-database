---
title: ADHD Research Database Documentation
description: Comprehensive documentation for the evidence-based ADHD research database platform
audience: all
difficulty: beginner
---

# ADHD Research Database

> A comprehensive, evidence-based ADHD research database for professional adults (25-65), featuring validated assessment tools, treatment decision trees, and 281+ research findings.

```
┌─────────────────────────────────────────────────────────────────┐
│                    ADHD RESEARCH DATABASE                       │
│         Evidence-Based Research for Professional Adults         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   281 Research Entries    │    3 Assessment Frameworks          │
│   145 Enhanced Protocols  │    5 Intervention Categories        │
│   65+ Research Domains    │    Docker-Ready Deployment          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## What Is This Project?

The ADHD Research Database is a full-stack application providing:

- **Research Explorer** — Search and filter 281+ peer-reviewed research findings
- **Assessment Tools** — ASRS-based professional evaluation with scoring algorithms
- **Treatment Decision Trees** — Evidence-based intervention pathways
- **Intervention Library** — 14+ categorized interventions with implementation protocols
- **REST API** — Programmatic access to all research data
- **PostgreSQL Backend** — Normalized relational database with Prisma ORM

## Who Is This For?

```
┌─────────────────────────────────────────────────────────────────┐
│                       TARGET AUDIENCES                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌──────────┐ │
│  │ End Users  │  │ Healthcare │  │ Developers │  │  Admins  │ │
│  │            │  │ Providers  │  │            │  │          │ │
│  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘  └────┬─────┘ │
│        │               │               │              │        │
│        ▼               ▼               ▼              ▼        │
│   Research        Clinical        API Access      Deploy &    │
│   Browsing        Reference       Extensions      Maintain    │
│   Assessment      Treatment       Integrations    Monitor     │
│   Self-Help       Planning        Custom Apps     Scale       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Quick Navigation

| I want to... | Go to... |
|--------------|----------|
| Get started quickly | [Quickstart Guide](./quickstart.md) |
| Browse research findings | [User Guide](./guides/user/getting-started.md) |
| Deploy with Docker | [Deployment Guide](./guides/admin/deployment.md) |
| Use the REST API | [API Reference](./reference/api.md) |
| Understand the data schema | [Database Schema](./reference/database-schema.md) |
| Troubleshoot issues | [Troubleshooting](./troubleshooting/common-issues.md) |
| Contribute to development | [Developer Guide](./guides/developer/contributing.md) |
| Clinical decision support | [Healthcare Guide](./guides/healthcare/clinical-use.md) |

## Technology Stack

```
┌─────────────────────────────────────────────────────────────────┐
│                      ARCHITECTURE                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌──────────────┐                                             │
│   │   Frontend   │  Vanilla HTML/CSS/JS SPA                    │
│   │   (Browser)  │  No build step required                     │
│   └──────┬───────┘                                             │
│          │ HTTP/JSON                                           │
│          ▼                                                      │
│   ┌──────────────┐                                             │
│   │  Flask API   │  Python 3.11 + Flask 3.1                    │
│   │   Server     │  RESTful endpoints                          │
│   └──────┬───────┘                                             │
│          │ Prisma ORM                                          │
│          ▼                                                      │
│   ┌──────────────┐                                             │
│   │  PostgreSQL  │  Relational database                        │
│   │   Database   │  11 normalized tables                       │
│   └──────────────┘                                             │
│                                                                 │
│   ┌──────────────┐                                             │
│   │   Docker     │  Container orchestration                    │
│   │   Compose    │  One-command deployment                     │
│   └──────────────┘                                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | HTML5/CSS3/JavaScript | Single-page application |
| **Backend** | Flask 3.1 (Python 3.11) | REST API server |
| **ORM** | Prisma 6.16 | Database schema & queries |
| **Database** | PostgreSQL 14+ | Data persistence |
| **Deployment** | Docker Compose | Container orchestration |

## Documentation Structure

```
docs-new/
├── index.md                      # ← You are here
├── quickstart.md                 # 5-minute setup guide
│
├── guides/
│   ├── user/
│   │   ├── getting-started.md    # Full user onboarding
│   │   ├── research-explorer.md  # Using the search interface
│   │   └── assessments.md        # Taking ADHD assessments
│   │
│   ├── healthcare/
│   │   ├── clinical-use.md       # Clinical decision support
│   │   └── treatment-planning.md # Using decision trees
│   │
│   ├── admin/
│   │   ├── deployment.md         # Docker & cloud deployment
│   │   ├── configuration.md      # Environment variables
│   │   └── monitoring.md         # Health checks & logging
│   │
│   └── developer/
│       ├── architecture.md       # System design
│       ├── api-development.md    # Extending the API
│       ├── database.md           # Schema & migrations
│       └── contributing.md       # Development workflow
│
├── reference/
│   ├── api.md                    # REST API specification
│   ├── database-schema.md        # Table definitions
│   ├── data-formats.md           # JSON schemas
│   └── glossary.md               # Term definitions
│
└── troubleshooting/
    ├── common-issues.md          # 20+ error scenarios
    ├── database-issues.md        # PostgreSQL troubleshooting
    ├── docker-issues.md          # Container problems
    └── friction-log.md           # Known limitations
```

## Key Metrics

| Metric | Value |
|--------|-------|
| Research Entries | 281 |
| Enhanced Protocols | 145 |
| Research Domains | 65+ |
| Assessment Tools | 3 (ASRS, AAQoL, Decision Tree) |
| Intervention Categories | 5 |
| Evidence Levels | 5 (1A highest → 5 lowest) |
| Database Tables | 11 |
| API Endpoints | 6 |

## Deployment Options

| Option | Best For | Guide |
|--------|----------|-------|
| **Docker Compose** | Self-hosted, development | [Docker Deployment](./guides/admin/deployment.md#docker) |
| **Cloud Platforms** | Production, scaling | [Cloud Deployment](./guides/admin/deployment.md#cloud) |
| **Local Development** | Contributing, testing | [Dev Setup](./guides/developer/contributing.md#setup) |

## Research Focus

This database is specifically designed for **professional adult males (25-65)** with diagnosed or suspected ADHD, focusing on:

- Workplace performance and accommodations
- Executive function in professional settings
- Career advancement strategies
- Evidence-based treatment options
- Late diagnosis patterns and masking behaviors

---

**Designed by Anthony Velte & Claude Opus 4.5**

Built with care to help professionals access evidence-based ADHD research.

If this project helped you, consider starring the repo ⭐

---

**Next**: [Quickstart Guide](./quickstart.md) — Get running in 5 minutes
