---
title: Database Schema Reference
description: Complete technical documentation of the ADHD Research Database schema, including all tables, relationships, enums, and constraints
audience: developer
difficulty: intermediate
---

# Database Schema Reference

This document provides comprehensive documentation of the ADHD Research Database schema built with Prisma ORM and PostgreSQL.

## Overview

The database consists of 11 tables organized around a central `research_entries` table, with supporting tables for detailed categorization, quality assessment, and clinical application tracking.

## Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        ADHD Research Database Schema                         │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────┐       ┌──────────────────────┐
│   target_populations │       │    methodologies     │
│──────────────────────│       │──────────────────────│
│ id (PK)              │       │ id (PK)              │
│ ageRange             │       │ design               │
│ gender               │       │ duration             │
│ occupation           │       │ primaryOutcomes[]    │
│ adhdSubtype          │       │ secondaryOutcomes[]  │
└──────────┬───────────┘       └──────────┬───────────┘
           │ 1:1                          │ 1:1
           │                              │
           ▼                              ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                           research_entries (CENTRAL)                      │
│──────────────────────────────────────────────────────────────────────────│
│ id (PK)           │ title              │ authors[]         │ journal     │
│ publicationDate   │ doi (UNIQUE)       │ studyType (ENUM)  │ evidenceLevel│
│ sampleSize        │ createdAt          │ updatedAt         │             │
│ targetPopulationId│ methodologyId      │ keyFindingsId     │             │
│ workplaceRelevanceId │ qualityAssessmentId │ clinicalApplicationId       │
└───────┬──────────────────┬───────────────────┬────────────────────┬──────┘
        │ 1:1              │ 1:1               │ 1:1                │ M:N
        ▼                  ▼                   ▼                    ▼
┌───────────────┐  ┌────────────────┐  ┌───────────────────┐  ┌──────────┐
│  key_findings │  │ workplace_     │  │ quality_          │  │   tags   │
│───────────────│  │ relevance      │  │ assessments       │  │──────────│
│ id (PK)       │  │────────────────│  │───────────────────│  │ id (PK)  │
│ primaryResults│  │ id (PK)        │  │ id (PK)           │  │ name (U) │
│ effectSizes   │  │ productivity   │  │ riskOfBias        │  └──────────┘
│ clinical      │  │ Impact         │  │ gradeRating       │
│ Significance  │  │ accommodation  │  │ reviewerNotes     │
│ limitations[] │  │ Needs[]        │  └───────────────────┘
└───────────────┘  │ careerImpl     │
                   └────────────────┘
        │ 1:1
        ▼
┌───────────────────────┐
│ clinical_applications │
│───────────────────────│
│ id (PK)               │
│ diagnosticUtility     │
│ treatment             │
│ Recommendations[]     │
│ monitoringParameters[]│
└───────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                        STANDALONE REFERENCE TABLES                       │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────┐  ┌────────────────────┐  ┌────────────────────┐
│ treatment_recommendations│  │  assessment_tools  │  │  outcome_measures  │
│─────────────────────────│  │────────────────────│  │────────────────────│
│ id (PK)                 │  │ id (PK)            │  │ id (PK)            │
│ condition               │  │ name               │  │ name               │
│ treatmentType (ENUM)    │  │ acronym            │  │ domain (ENUM)      │
│ interventionName        │  │ purpose            │  │ measureType (ENUM) │
│ evidenceLevel (ENUM)    │  │ targetPopulation   │  │ description        │
│ effectSize              │  │ administrationTime │  │ scoringMethod      │
│ recommendationStrength  │  │ domains[]          │  │ interpretation     │
│ targetPopulation        │  │ psychometric       │  │ Guidelines         │
│ contraindications[]     │  │ Properties (JSON)  │  │ clinicalSignif     │
│ sideEffects[]           │  │ clinicalUtility    │  │ minimumDetectable  │
│ monitoringRequirements[]│  │ limitations[]      │  │ Change             │
└─────────────────────────┘  └────────────────────┘  └────────────────────┘
```

## Table Definitions

### research_entries

The central table storing all research study metadata and linking to detailed information tables.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | String | PK, UUID | Unique identifier |
| `title` | String | NOT NULL | Study title |
| `authors` | String[] | NOT NULL | List of author names |
| `journal` | String | NOT NULL | Publication journal name |
| `publicationDate` | DateTime | NOT NULL | Date of publication |
| `doi` | String | UNIQUE | Digital Object Identifier |
| `studyType` | StudyType | NOT NULL | Type of study (enum) |
| `evidenceLevel` | EvidenceLevel | NOT NULL | Evidence hierarchy level |
| `sampleSize` | Int | OPTIONAL | Number of participants |
| `createdAt` | DateTime | DEFAULT now() | Record creation timestamp |
| `updatedAt` | DateTime | AUTO | Last update timestamp |
| `targetPopulationId` | String | FK, UNIQUE | Link to target_populations |
| `methodologyId` | String | FK, UNIQUE | Link to methodologies |
| `keyFindingsId` | String | FK, UNIQUE | Link to key_findings |
| `workplaceRelevanceId` | String | FK, UNIQUE | Link to workplace_relevance |
| `qualityAssessmentId` | String | FK, UNIQUE | Link to quality_assessments |
| `clinicalApplicationId` | String | FK, UNIQUE | Link to clinical_applications |

### target_populations

Describes the demographic and clinical characteristics of study participants.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | String | PK, UUID | Unique identifier |
| `ageRange` | String | NOT NULL | Age range (e.g., "18-65") |
| `gender` | String | OPTIONAL | Gender distribution |
| `occupation` | String | OPTIONAL | Occupational context |
| `adhdSubtype` | String | OPTIONAL | ADHD presentation type |

### methodologies

Captures study design and outcome measurement details.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | String | PK, UUID | Unique identifier |
| `design` | String | NOT NULL | Study design description |
| `duration` | String | OPTIONAL | Study duration |
| `primaryOutcomes` | String[] | NOT NULL | Primary outcome measures |
| `secondaryOutcomes` | String[] | DEFAULT [] | Secondary outcome measures |

### key_findings

Stores primary results and statistical findings from studies.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | String | PK, UUID | Unique identifier |
| `primaryResults` | String | NOT NULL | Main findings summary |
| `effectSizes` | Json | OPTIONAL | Effect size data (Cohen's d, OR, etc.) |
| `clinicalSignificance` | String | OPTIONAL | Clinical relevance interpretation |
| `limitations` | String[] | DEFAULT [] | Study limitations |

**effectSizes JSON Structure:**
```json
{
  "cohensD": 0.75,
  "oddsRatio": 2.3,
  "confidenceInterval": {
    "lower": 0.45,
    "upper": 1.05
  },
  "pValue": 0.001
}
```

### workplace_relevance

Documents implications for workplace settings and accommodations.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | String | PK, UUID | Unique identifier |
| `productivityImpact` | String | OPTIONAL | Effect on work productivity |
| `accommodationNeeds` | String[] | DEFAULT [] | Recommended accommodations |
| `careerImplications` | String | OPTIONAL | Long-term career considerations |

### quality_assessments

Records methodological quality and bias assessments.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | String | PK, UUID | Unique identifier |
| `riskOfBias` | RiskLevel | NOT NULL | Bias risk assessment |
| `gradeRating` | GradeRating | NOT NULL | GRADE evidence rating |
| `reviewerNotes` | String | OPTIONAL | Additional reviewer comments |

### clinical_applications

Documents practical clinical utility and recommendations.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | String | PK, UUID | Unique identifier |
| `diagnosticUtility` | String | OPTIONAL | Usefulness for diagnosis |
| `treatmentRecommendations` | String[] | DEFAULT [] | Treatment suggestions |
| `monitoringParameters` | String[] | DEFAULT [] | Parameters to monitor |

### tags

Flexible tagging system for categorization.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | String | PK, UUID | Unique identifier |
| `name` | String | UNIQUE, NOT NULL | Tag name |

**Note:** Tags connect to research_entries via an implicit many-to-many join table `_ResearchEntryTags`.

### treatment_recommendations

Standalone reference table for treatment guidance.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | String | PK, UUID | Unique identifier |
| `condition` | String | NOT NULL | Target condition |
| `treatmentType` | TreatmentType | NOT NULL | Category of treatment |
| `interventionName` | String | NOT NULL | Specific intervention name |
| `evidenceLevel` | EvidenceLevel | NOT NULL | Supporting evidence level |
| `effectSize` | String | OPTIONAL | Reported effect size |
| `recommendationStrength` | RecommendationStrength | NOT NULL | Strength of recommendation |
| `targetPopulation` | String | OPTIONAL | Intended patient population |
| `contraindications` | String[] | DEFAULT [] | When not to use |
| `sideEffects` | String[] | DEFAULT [] | Known adverse effects |
| `monitoringRequirements` | String[] | DEFAULT [] | Required monitoring |

### assessment_tools

Reference table for clinical assessment instruments.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | String | PK, UUID | Unique identifier |
| `name` | String | NOT NULL | Full tool name |
| `acronym` | String | OPTIONAL | Common abbreviation |
| `purpose` | String | NOT NULL | Primary use case |
| `targetPopulation` | String | OPTIONAL | Intended population |
| `administrationTime` | String | OPTIONAL | Time to administer |
| `domains` | String[] | DEFAULT [] | Assessed domains |
| `psychometricProperties` | Json | OPTIONAL | Validity/reliability data |
| `clinicalUtility` | String | OPTIONAL | Practical usefulness |
| `limitations` | String[] | DEFAULT [] | Known limitations |

**psychometricProperties JSON Structure:**
```json
{
  "reliability": {
    "internalConsistency": 0.92,
    "testRetest": 0.87
  },
  "validity": {
    "sensitivity": 0.85,
    "specificity": 0.78,
    "convergent": "Strong correlation with CAARS"
  },
  "norms": "Adult population ages 18-65"
}
```

### outcome_measures

Reference table for standardized outcome definitions.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | String | PK, UUID | Unique identifier |
| `name` | String | NOT NULL | Measure name |
| `domain` | OutcomeDomain | NOT NULL | Domain category |
| `measureType` | MeasureType | NOT NULL | Assessment method type |
| `description` | String | NOT NULL | Detailed description |
| `scoringMethod` | String | OPTIONAL | How to calculate scores |
| `interpretationGuidelines` | String | OPTIONAL | Score interpretation |
| `clinicalSignificance` | String | OPTIONAL | Clinical meaning |
| `minimumDetectableChange` | String | OPTIONAL | Smallest meaningful change |

## Enum Definitions

### StudyType

Classifies research study designs according to evidence hierarchy.

| Value | Description |
|-------|-------------|
| `SYSTEMATIC_REVIEW` | Systematic review of multiple studies |
| `META_ANALYSIS` | Statistical synthesis of multiple studies |
| `RCT` | Randomized controlled trial |
| `COHORT` | Prospective or retrospective cohort study |
| `CASE_CONTROL` | Case-control comparison study |
| `CASE_SERIES` | Series of case reports |
| `EXPERT_OPINION` | Expert consensus or opinion |

### EvidenceLevel

Oxford Centre for Evidence-Based Medicine levels.

| Value | Description |
|-------|-------------|
| `LEVEL_1A` | Systematic review of RCTs with homogeneity |
| `LEVEL_1B` | Individual RCT with narrow CI |
| `LEVEL_2A` | Systematic review of cohort studies |
| `LEVEL_2B` | Individual cohort study or low-quality RCT |
| `LEVEL_3A` | Systematic review of case-control studies |
| `LEVEL_3B` | Individual case-control study |
| `LEVEL_4` | Case series or poor-quality cohort/case-control |
| `LEVEL_5` | Expert opinion without critical appraisal |

### RiskLevel

Bias risk assessment categories.

| Value | Description |
|-------|-------------|
| `LOW` | Minimal risk of bias |
| `MODERATE` | Some concerns about bias |
| `HIGH` | Significant bias concerns |

### GradeRating

GRADE evidence quality ratings.

| Value | Description |
|-------|-------------|
| `HIGH` | Very confident in effect estimate |
| `MODERATE` | Moderately confident; true effect likely close |
| `LOW` | Limited confidence; true effect may differ |
| `VERY_LOW` | Very little confidence in effect estimate |

### TreatmentType

Categories of therapeutic interventions.

| Value | Description |
|-------|-------------|
| `PHARMACOLOGICAL` | Medication-based treatment |
| `PSYCHOLOGICAL` | Therapy and counseling approaches |
| `BEHAVIORAL` | Behavior modification interventions |
| `NEUROSTIMULATION` | Brain stimulation techniques (TMS, tDCS) |
| `LIFESTYLE` | Diet, exercise, sleep interventions |
| `COMBINED` | Multimodal treatment approaches |

### RecommendationStrength

GRADE recommendation strength indicators.

| Value | Description |
|-------|-------------|
| `STRONG_FOR` | Strong recommendation to use intervention |
| `CONDITIONAL_FOR` | Conditional/weak recommendation for use |
| `CONDITIONAL_AGAINST` | Conditional/weak recommendation against |
| `STRONG_AGAINST` | Strong recommendation against use |

### OutcomeDomain

Clinical outcome measurement domains.

| Value | Description |
|-------|-------------|
| `ADHD_SYMPTOMS` | Core ADHD symptom measures |
| `EXECUTIVE_FUNCTION` | Cognitive control and planning |
| `QUALITY_OF_LIFE` | General well-being measures |
| `WORKPLACE_FUNCTIONING` | Job performance and productivity |
| `ACADEMIC_PERFORMANCE` | Educational achievement |
| `SOCIAL_FUNCTIONING` | Interpersonal relationships |
| `EMOTIONAL_REGULATION` | Affect management |
| `COMORBID_SYMPTOMS` | Co-occurring condition symptoms |

### MeasureType

Assessment methodology classifications.

| Value | Description |
|-------|-------------|
| `SELF_REPORT` | Patient-completed questionnaires |
| `CLINICIAN_RATED` | Professional assessment scales |
| `PERFORMANCE_BASED` | Objective task performance |
| `PHYSIOLOGICAL` | Biological measurements |
| `BEHAVIORAL_OBSERVATION` | Direct behavior monitoring |

## Relationships

### One-to-One Relationships

All detail tables have exclusive 1:1 relationships with `research_entries`:

- `research_entries` -> `target_populations` (via `targetPopulationId`)
- `research_entries` -> `methodologies` (via `methodologyId`)
- `research_entries` -> `key_findings` (via `keyFindingsId`)
- `research_entries` -> `workplace_relevance` (via `workplaceRelevanceId`)
- `research_entries` -> `quality_assessments` (via `qualityAssessmentId`)
- `research_entries` -> `clinical_applications` (via `clinicalApplicationId`)

These relationships use `UNIQUE` constraints on foreign keys to enforce exclusivity.

### Many-to-Many Relationships

- `research_entries` <-> `tags`: Implicit join table `_ResearchEntryTags`

## Example Data

### Research Entry with Related Data

```typescript
// Complete research entry example
const researchEntry = {
  id: "550e8400-e29b-41d4-a716-446655440000",
  title: "Methylphenidate vs Placebo in Adult ADHD: A Meta-Analysis",
  authors: ["Smith, J.", "Johnson, M.", "Williams, K."],
  journal: "Journal of Attention Disorders",
  publicationDate: new Date("2024-03-15"),
  doi: "10.1177/1087054724123456",
  studyType: "META_ANALYSIS",
  evidenceLevel: "LEVEL_1A",
  sampleSize: 4521,

  targetPopulation: {
    ageRange: "18-65",
    gender: "Mixed (52% male)",
    occupation: "Various professional settings",
    adhdSubtype: "Combined and Inattentive presentations"
  },

  methodology: {
    design: "Systematic review and meta-analysis of RCTs",
    duration: "Studies ranging 4-52 weeks",
    primaryOutcomes: ["ADHD-RS-IV total score", "CGI-S"],
    secondaryOutcomes: ["Quality of life", "Functional impairment"]
  },

  keyFindings: {
    primaryResults: "Significant symptom reduction with moderate effect size",
    effectSizes: {
      cohensD: 0.58,
      confidenceInterval: { lower: 0.45, upper: 0.71 },
      pValue: 0.001
    },
    clinicalSignificance: "Clinically meaningful improvement",
    limitations: ["Publication bias detected", "Heterogeneity in dosing"]
  },

  qualityAssessment: {
    riskOfBias: "LOW",
    gradeRating: "HIGH",
    reviewerNotes: "Well-conducted meta-analysis with pre-registered protocol"
  },

  tags: [
    { name: "methylphenidate" },
    { name: "adult-adhd" },
    { name: "meta-analysis" }
  ]
};
```

### Treatment Recommendation Example

```typescript
const treatmentRec = {
  id: "660e8400-e29b-41d4-a716-446655440001",
  condition: "Adult ADHD - Combined Presentation",
  treatmentType: "PHARMACOLOGICAL",
  interventionName: "Methylphenidate Extended-Release",
  evidenceLevel: "LEVEL_1A",
  effectSize: "SMD 0.58 (95% CI: 0.45-0.71)",
  recommendationStrength: "STRONG_FOR",
  targetPopulation: "Adults 18-65 without contraindications",
  contraindications: [
    "Uncontrolled hypertension",
    "Severe anxiety disorders",
    "History of substance abuse",
    "MAO inhibitor use within 14 days"
  ],
  sideEffects: [
    "Decreased appetite",
    "Insomnia",
    "Headache",
    "Dry mouth"
  ],
  monitoringRequirements: [
    "Blood pressure every 3 months",
    "Weight monitoring",
    "Sleep quality assessment",
    "Cardiovascular screening annually"
  ]
};
```

### Assessment Tool Example

```typescript
const assessmentTool = {
  id: "770e8400-e29b-41d4-a716-446655440002",
  name: "Adult ADHD Self-Report Scale",
  acronym: "ASRS-v1.1",
  purpose: "Screening and symptom monitoring for adult ADHD",
  targetPopulation: "Adults 18+",
  administrationTime: "5-10 minutes",
  domains: [
    "Inattention",
    "Hyperactivity",
    "Impulsivity"
  ],
  psychometricProperties: {
    reliability: {
      internalConsistency: 0.88,
      testRetest: 0.83
    },
    validity: {
      sensitivity: 0.68,
      specificity: 0.99
    }
  },
  clinicalUtility: "Validated screening tool recommended by WHO",
  limitations: [
    "Self-report bias",
    "Not diagnostic alone",
    "Requires clinical confirmation"
  ]
};
```

## Database Indexes

Recommended indexes for query optimization:

```sql
-- Primary search patterns
CREATE INDEX idx_research_entries_study_type ON research_entries(studyType);
CREATE INDEX idx_research_entries_evidence_level ON research_entries(evidenceLevel);
CREATE INDEX idx_research_entries_publication_date ON research_entries(publicationDate);

-- DOI lookups
CREATE UNIQUE INDEX idx_research_entries_doi ON research_entries(doi);

-- Tag searches
CREATE UNIQUE INDEX idx_tags_name ON tags(name);

-- Treatment lookups
CREATE INDEX idx_treatment_recs_type ON treatment_recommendations(treatmentType);
CREATE INDEX idx_treatment_recs_strength ON treatment_recommendations(recommendationStrength);

-- Outcome measure queries
CREATE INDEX idx_outcome_measures_domain ON outcome_measures(domain);
CREATE INDEX idx_outcome_measures_type ON outcome_measures(measureType);
```

## Migration Notes

When modifying the schema:

1. Always create a new Prisma migration: `npx prisma migrate dev --name descriptive_name`
2. Test migrations on a copy of production data first
3. Back up the database before applying to production
4. Update this documentation after schema changes

---

*Documentation generated for ADHD Research Database v1.0*
*Last updated: 2026-02-02*
*Schema source: prisma/schema.prisma*
