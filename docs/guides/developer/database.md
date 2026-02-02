---
title: Database Developer Guide
description: Complete guide to working with the PostgreSQL database using Prisma ORM, including schema management, migrations, seeding, and best practices.
audience: developer
difficulty: intermediate
---

# Database Developer Guide

This guide covers all aspects of database development for the ADHD Research Database, including Prisma schema management, migrations, data seeding, query patterns, and operational procedures.

## Table of Contents

1. [Overview](#overview)
2. [Prisma Schema Architecture](#prisma-schema-architecture)
3. [Running Migrations](#running-migrations)
4. [Creating New Migrations](#creating-new-migrations)
5. [Database Seeding](#database-seeding)
6. [Query Patterns and Best Practices](#query-patterns-and-best-practices)
7. [Adding New Tables](#adding-new-tables)
8. [Modifying Existing Schema](#modifying-existing-schema)
9. [Backup and Restore Procedures](#backup-and-restore-procedures)
10. [Common Prisma Commands Reference](#common-prisma-commands-reference)
11. [Troubleshooting](#troubleshooting)

---

## Overview

The ADHD Research Database uses:

- **PostgreSQL 14** as the relational database
- **Prisma 6.16** as the ORM and schema management tool
- **Normalized schema** with 11 interconnected tables
- **PrismaClient** wrapper for database operations

### Database Connection

The database connection is configured via the `DATABASE_URL` environment variable:

```bash
# Format
DATABASE_URL="postgresql://USER:PASSWORD@HOST:PORT/DATABASE?schema=public"

# Example for local development
DATABASE_URL="postgresql://postgres:password@localhost:5432/adhd_research?schema=public"
```

### Schema Location

The Prisma schema file is located at:

```
prisma/schema.prisma
```

---

## Prisma Schema Architecture

### Generator and Datasource Configuration

```prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}
```

### Entity Relationship Diagram

```
┌─────────────────────┐
│   ResearchEntry     │ (Central entity)
├─────────────────────┤
│ id                  │───┬──▶ TargetPopulation
│ title               │   │
│ authors[]           │   ├──▶ Methodology
│ journal             │   │
│ publicationDate     │   ├──▶ KeyFindings
│ doi                 │   │
│ studyType           │   ├──▶ WorkplaceRelevance
│ evidenceLevel       │   │
│ sampleSize          │   ├──▶ QualityAssessment
│ createdAt           │   │
│ updatedAt           │   ├──▶ ClinicalApplications
│ addedDate           │   │
│ lastReviewed        │   └──◀▶ Tag[] (many-to-many)
└─────────────────────┘

┌─────────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐
│ TreatmentRecommendation │  │   AssessmentTool    │  │   OutcomeMeasure    │
├─────────────────────────┤  ├─────────────────────┤  ├─────────────────────┤
│ id                      │  │ id                  │  │ id                  │
│ condition               │  │ name                │  │ name                │
│ treatmentType           │  │ acronym             │  │ domain              │
│ interventionName        │  │ purpose             │  │ measureType         │
│ evidenceLevel           │  │ targetPopulation    │  │ description         │
│ effectSize              │  │ administrationTime  │  │ scoringMethod       │
│ recommendationStrength  │  │ domains[]           │  │ interpretation...   │
│ targetPopulation        │  │ psychometricProps   │  │ clinicalSignif...   │
│ contraindications[]     │  │ clinicalUtility     │  │ minimumDetectable...│
│ sideEffects[]           │  │ limitations[]       │  │ createdAt           │
│ monitoringReqs[]        │  │ createdAt           │  │ updatedAt           │
│ createdAt               │  │ updatedAt           │  └─────────────────────┘
│ updatedAt               │  └─────────────────────┘
└─────────────────────────┘
```

### Models Overview

| Model | Purpose | Table Name |
|-------|---------|------------|
| `ResearchEntry` | Core research paper records | `research_entries` |
| `TargetPopulation` | Demographics of study participants | `target_populations` |
| `Methodology` | Study design and outcomes | `methodologies` |
| `KeyFindings` | Primary results and effect sizes | `key_findings` |
| `WorkplaceRelevance` | Workplace-specific implications | `workplace_relevance` |
| `QualityAssessment` | Bias and GRADE ratings | `quality_assessments` |
| `ClinicalApplications` | Diagnostic and treatment utility | `clinical_applications` |
| `Tag` | Categorization tags | `tags` |
| `TreatmentRecommendation` | Treatment guidance records | `treatment_recommendations` |
| `AssessmentTool` | Clinical assessment instruments | `assessment_tools` |
| `OutcomeMeasure` | Outcome measurement definitions | `outcome_measures` |

### Enums

The schema defines several enums for type safety:

```prisma
enum StudyType {
  SYSTEMATIC_REVIEW
  META_ANALYSIS
  RCT
  COHORT
  CASE_CONTROL
  CASE_SERIES
  EXPERT_OPINION
}

enum EvidenceLevel {
  LEVEL_1A  // Systematic review of RCTs
  LEVEL_1B  // Individual RCT with narrow CI
  LEVEL_2A  // Systematic review of cohort studies
  LEVEL_2B  // Individual cohort study
  LEVEL_3A  // Systematic review of case-control studies
  LEVEL_3B  // Individual case-control study
  LEVEL_4   // Case series
  LEVEL_5   // Expert opinion
}

enum RiskLevel { LOW, MODERATE, HIGH }
enum GradeRating { HIGH, MODERATE, LOW, VERY_LOW }
enum TreatmentType { PHARMACOLOGICAL, PSYCHOLOGICAL, BEHAVIORAL, NEUROSTIMULATION, LIFESTYLE, COMBINED }
enum RecommendationStrength { STRONG_FOR, CONDITIONAL_FOR, CONDITIONAL_AGAINST, STRONG_AGAINST }
enum OutcomeDomain { ADHD_SYMPTOMS, EXECUTIVE_FUNCTION, QUALITY_OF_LIFE, WORKPLACE_FUNCTIONING, ACADEMIC_PERFORMANCE, SOCIAL_FUNCTIONING, EMOTIONAL_REGULATION, COMORBID_SYMPTOMS }
enum MeasureType { SELF_REPORT, CLINICIAN_RATED, PERFORMANCE_BASED, PHYSIOLOGICAL, BEHAVIORAL_OBSERVATION }
```

---

## Running Migrations

### Development Environment

Use `migrate dev` for development. This command:

1. Creates a new migration if schema changes are detected
2. Applies all pending migrations
3. Regenerates Prisma Client

```bash
# Apply migrations and generate client
npx prisma migrate dev

# Apply with a specific migration name
npx prisma migrate dev --name add_new_field

# Skip seed after migration
npx prisma migrate dev --skip-seed
```

### Production Environment

Use `migrate deploy` for production. This command:

1. Applies all pending migrations
2. Does NOT create new migrations
3. Does NOT prompt interactively

```bash
# Apply pending migrations in production
npx prisma migrate deploy
```

### Checking Migration Status

```bash
# View migration status
npx prisma migrate status

# Example output:
# Migration                            Applied              Database
# 20240115_init                        Yes                  Yes
# 20240120_add_assessment_tools        Yes                  Yes
# 20240125_add_outcome_measures        Pending              No
```

### Resetting the Database

**Warning**: This destroys all data!

```bash
# Reset database (drops, recreates, applies all migrations)
npx prisma migrate reset

# Force reset without confirmation
npx prisma migrate reset --force
```

---

## Creating New Migrations

### Step 1: Modify the Schema

Edit `prisma/schema.prisma` with your changes:

```prisma
model ResearchEntry {
  // ... existing fields ...

  // Add new field
  abstractText  String?  @db.Text
}
```

### Step 2: Create the Migration

```bash
# Generate migration from schema changes
npx prisma migrate dev --name add_abstract_text
```

This creates a migration file at:
```
prisma/migrations/YYYYMMDDHHMMSS_add_abstract_text/migration.sql
```

### Step 3: Review the Generated SQL

Always review the generated SQL before committing:

```sql
-- Example migration.sql
ALTER TABLE "research_entries" ADD COLUMN "abstractText" TEXT;
```

### Step 4: Commit the Migration

```bash
git add prisma/
git commit -m "Add abstractText field to ResearchEntry"
```

### Creating Empty Migrations

For custom SQL operations:

```bash
# Create empty migration
npx prisma migrate dev --create-only --name custom_indexes

# Edit the migration.sql file manually
# Then apply:
npx prisma migrate dev
```

---

## Database Seeding

### Overview

The `migrate_data.js` script seeds the database with initial data from a JSON knowledge base.

### Running the Seed Script

```bash
# Run the data migration script
node migrate_data.js
```

### Seed Script Behavior

The script performs the following operations:

1. **Reads** `knowledge_base/knowledge_base.json`
2. **Creates** related entities (TargetPopulation, Methodology, etc.)
3. **Creates** or finds Tags (upsert behavior)
4. **Creates** ResearchEntry records with relationships
5. **Seeds** AssessmentTools and TreatmentRecommendations

### Sample Output

```
Starting data migration...
Migrating: Workplace Interventions for Adults with ADHD
 Migrated: Workplace Interventions for Adults with ADHD
Migrating: Cognitive Behavioral Therapy Efficacy
 Migrated: Cognitive Behavioral Therapy Efficacy
 Data migration completed successfully!

Migration Summary:
- Research Entries: 5
- Tags: 12
- Assessment Tools: 2
- Treatment Recommendations: 2
```

### Configuring Prisma Seed

Add to `package.json`:

```json
{
  "prisma": {
    "seed": "node migrate_data.js"
  }
}
```

Then use:

```bash
# Run seed via Prisma
npx prisma db seed
```

---

## Query Patterns and Best Practices

### Basic Queries

```javascript
const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

// Find all research entries
const entries = await prisma.researchEntry.findMany();

// Find by ID
const entry = await prisma.researchEntry.findUnique({
  where: { id: 'clm123abc...' }
});

// Find with conditions
const rcts = await prisma.researchEntry.findMany({
  where: {
    studyType: 'RCT',
    evidenceLevel: { in: ['LEVEL_1A', 'LEVEL_1B'] }
  }
});
```

### Including Relations

```javascript
// Include all related data
const entry = await prisma.researchEntry.findUnique({
  where: { id: 'clm123abc...' },
  include: {
    targetPopulation: true,
    methodology: true,
    keyFindings: true,
    workplaceRelevance: true,
    qualityAssessment: true,
    clinicalApplications: true,
    tags: true
  }
});

// Selective inclusion
const entries = await prisma.researchEntry.findMany({
  include: {
    keyFindings: true,
    tags: true
  }
});
```

### Filtering and Sorting

```javascript
// Complex filtering
const entries = await prisma.researchEntry.findMany({
  where: {
    AND: [
      { studyType: 'RCT' },
      { sampleSize: { gte: 100 } },
      { publicationDate: { gte: new Date('2020-01-01') } }
    ]
  },
  orderBy: [
    { publicationDate: 'desc' },
    { sampleSize: 'desc' }
  ],
  take: 10,
  skip: 0
});
```

### Searching Text Fields

```javascript
// Case-insensitive search
const results = await prisma.researchEntry.findMany({
  where: {
    OR: [
      { title: { contains: 'workplace', mode: 'insensitive' } },
      { journal: { contains: 'psychology', mode: 'insensitive' } }
    ]
  }
});
```

### Aggregations

```javascript
// Count by study type
const counts = await prisma.researchEntry.groupBy({
  by: ['studyType'],
  _count: { id: true }
});

// Average sample size
const avg = await prisma.researchEntry.aggregate({
  _avg: { sampleSize: true },
  _max: { sampleSize: true },
  _min: { sampleSize: true }
});
```

### Transactions

```javascript
// Interactive transaction
const result = await prisma.$transaction(async (tx) => {
  const population = await tx.targetPopulation.create({
    data: { ageRange: '25-45', gender: 'mixed', occupation: 'professional', adhdSubtype: 'combined' }
  });

  const entry = await tx.researchEntry.create({
    data: {
      title: 'New Study',
      // ... other fields
      targetPopulationId: population.id
    }
  });

  return entry;
});
```

### Performance Best Practices

1. **Select only needed fields**:
```javascript
const titles = await prisma.researchEntry.findMany({
  select: { id: true, title: true, publicationDate: true }
});
```

2. **Use pagination**:
```javascript
const page = 1;
const pageSize = 20;
const entries = await prisma.researchEntry.findMany({
  take: pageSize,
  skip: (page - 1) * pageSize
});
```

3. **Avoid N+1 queries** - use `include` instead of separate queries:
```javascript
// Bad: N+1 queries
const entries = await prisma.researchEntry.findMany();
for (const entry of entries) {
  const tags = await prisma.tag.findMany({ where: { researchEntries: { some: { id: entry.id } } } });
}

// Good: Single query with include
const entries = await prisma.researchEntry.findMany({
  include: { tags: true }
});
```

---

## Adding New Tables

### Step 1: Define the Model

Add the new model to `prisma/schema.prisma`:

```prisma
model Researcher {
  id            String   @id @default(cuid())
  name          String
  affiliation   String
  email         String?  @unique
  orcidId       String?  @unique
  specialties   String[]
  createdAt     DateTime @default(now())
  updatedAt     DateTime @updatedAt

  // Optional: Add relationships
  publications  ResearchEntry[] @relation("ResearcherPublications")

  @@map("researchers")
}
```

### Step 2: Update Related Models (if needed)

```prisma
model ResearchEntry {
  // ... existing fields ...

  // Add new relationship
  researchers   Researcher[] @relation("ResearcherPublications")
}
```

### Step 3: Create and Apply Migration

```bash
npx prisma migrate dev --name add_researcher_table
```

### Step 4: Update Seed Script (if needed)

Add seeding logic to `migrate_data.js`:

```javascript
// Seed researchers
const researchers = [
  {
    name: 'Dr. Jane Smith',
    affiliation: 'University of Research',
    email: 'jane.smith@example.edu',
    specialties: ['Adult ADHD', 'Workplace Psychology']
  }
];

for (const researcher of researchers) {
  await prisma.researcher.create({ data: researcher });
}
```

---

## Modifying Existing Schema

### Adding a New Field

```prisma
model ResearchEntry {
  // ... existing fields ...

  // Add new optional field (safe)
  peerReviewed  Boolean?
}
```

```bash
npx prisma migrate dev --name add_peer_reviewed_field
```

### Renaming a Field

Prisma does not auto-detect renames. Use `@map` to preserve data:

```prisma
model ResearchEntry {
  // Rename in code, keep DB column name
  paperTitle    String    @map("title")
}
```

Or create a custom migration:

```bash
npx prisma migrate dev --create-only --name rename_title_to_paper_title
```

Edit the migration:

```sql
ALTER TABLE "research_entries" RENAME COLUMN "title" TO "paper_title";
```

### Changing Field Types

**Caution**: May cause data loss!

1. Create a backup first
2. Review the migration SQL carefully
3. Test on a copy of production data

```bash
# Check current data
psql $DATABASE_URL -c "SELECT COUNT(*) FROM research_entries"

# Create backup
pg_dump -t research_entries > backup_research_entries.sql

# Then proceed with migration
npx prisma migrate dev --name change_field_type
```

### Making a Required Field Optional

```prisma
// Before
doi           String

// After (safe change)
doi           String?
```

### Making an Optional Field Required

**Caution**: Requires handling existing NULL values!

1. First, fill in NULL values:

```sql
UPDATE research_entries SET doi = 'unknown' WHERE doi IS NULL;
```

2. Then change the schema:

```prisma
doi           String
```

---

## Backup and Restore Procedures

### Creating Backups

#### Full Database Backup

```bash
# Backup entire database
pg_dump -h localhost -U postgres -d adhd_research -F c -f backup_$(date +%Y%m%d_%H%M%S).dump

# Backup with compression
pg_dump -h localhost -U postgres -d adhd_research -F c -Z 9 -f backup_compressed.dump
```

#### Table-Specific Backup

```bash
# Backup specific table
pg_dump -h localhost -U postgres -d adhd_research -t research_entries -f research_entries_backup.sql

# Backup multiple tables
pg_dump -h localhost -U postgres -d adhd_research -t research_entries -t tags -f entries_and_tags.sql
```

#### Schema-Only Backup

```bash
# Backup schema without data
pg_dump -h localhost -U postgres -d adhd_research --schema-only -f schema_backup.sql
```

#### Data-Only Backup

```bash
# Backup data without schema
pg_dump -h localhost -U postgres -d adhd_research --data-only -f data_backup.sql
```

### Restoring from Backup

#### Full Database Restore

```bash
# Restore from custom format
pg_restore -h localhost -U postgres -d adhd_research -c backup.dump

# Restore to a new database
createdb -h localhost -U postgres adhd_research_restored
pg_restore -h localhost -U postgres -d adhd_research_restored backup.dump
```

#### SQL File Restore

```bash
# Restore from SQL file
psql -h localhost -U postgres -d adhd_research -f backup.sql
```

### Automated Backup Script

Create `scripts/backup.sh`:

```bash
#!/bin/bash
set -e

BACKUP_DIR="/path/to/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DATABASE_URL="${DATABASE_URL:-postgresql://postgres:password@localhost:5432/adhd_research}"

# Create backup directory if not exists
mkdir -p "$BACKUP_DIR"

# Create backup
pg_dump "$DATABASE_URL" -F c -f "$BACKUP_DIR/adhd_research_$TIMESTAMP.dump"

# Keep only last 7 days of backups
find "$BACKUP_DIR" -name "adhd_research_*.dump" -mtime +7 -delete

echo "Backup completed: adhd_research_$TIMESTAMP.dump"
```

### Pre-Migration Backup

Always backup before migrations:

```bash
# Quick backup before migration
pg_dump $DATABASE_URL -F c -f pre_migration_$(date +%Y%m%d).dump

# Then run migration
npx prisma migrate deploy
```

---

## Common Prisma Commands Reference

| Command | Purpose | Environment |
|---------|---------|-------------|
| `npx prisma init` | Initialize Prisma in a project | Setup |
| `npx prisma generate` | Regenerate Prisma Client | All |
| `npx prisma db push` | Push schema changes without migration | Dev only |
| `npx prisma db pull` | Pull schema from existing database | Dev |
| `npx prisma migrate dev` | Create and apply migrations | Dev |
| `npx prisma migrate dev --name <name>` | Create named migration | Dev |
| `npx prisma migrate dev --create-only` | Create migration without applying | Dev |
| `npx prisma migrate deploy` | Apply pending migrations | Production |
| `npx prisma migrate reset` | Reset database and apply migrations | Dev only |
| `npx prisma migrate status` | Check migration status | All |
| `npx prisma db seed` | Run seed script | Dev |
| `npx prisma studio` | Open visual database browser | Dev |
| `npx prisma validate` | Validate schema syntax | All |
| `npx prisma format` | Format schema file | Dev |

### Environment-Specific Usage

```bash
# Development
npx prisma migrate dev --name add_new_feature
npx prisma studio

# Staging/Production
npx prisma migrate deploy
npx prisma migrate status

# CI/CD Pipeline
npx prisma generate
npx prisma migrate deploy
```

---

## Troubleshooting

### Common Issues

#### Migration Drift

**Problem**: Database schema doesn't match migration history.

```bash
# Check for drift
npx prisma migrate diff --from-schema-datasource prisma/schema.prisma --to-migrations ./prisma/migrations

# Reset if needed (dev only)
npx prisma migrate reset
```

#### Pending Migrations in Production

**Problem**: `migrate deploy` fails with pending migrations.

```bash
# Check status
npx prisma migrate status

# Mark migration as applied (if already applied manually)
npx prisma migrate resolve --applied <migration_name>
```

#### Connection Issues

**Problem**: Cannot connect to database.

```bash
# Test connection
npx prisma db pull

# Check DATABASE_URL format
echo $DATABASE_URL

# Verify PostgreSQL is running
pg_isready -h localhost -p 5432
```

#### Prisma Client Out of Sync

**Problem**: TypeScript errors after schema changes.

```bash
# Regenerate client
npx prisma generate

# If still issues, clear cache
rm -rf node_modules/.prisma
npx prisma generate
```

### Debug Mode

Enable query logging:

```javascript
const prisma = new PrismaClient({
  log: ['query', 'info', 'warn', 'error'],
});
```

### Getting Help

```bash
# Command-specific help
npx prisma migrate --help
npx prisma db --help

# Version info
npx prisma version
```

---

## Additional Resources

- [Prisma Documentation](https://www.prisma.io/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/14/)
- [Prisma Schema Reference](https://www.prisma.io/docs/reference/api-reference/prisma-schema-reference)
- [Prisma Client API](https://www.prisma.io/docs/reference/api-reference/prisma-client-reference)

---

*This documentation is part of the ADHD Research Database project. Generated with assistance from Claude AI.*
