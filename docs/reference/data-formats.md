---
title: Data Formats Reference
description: Complete reference for all JSON data structures used in the ADHD Research Database API
audience: developer
difficulty: intermediate
---

# Data Formats Reference

This document provides a complete reference for all JSON data structures returned by the ADHD Research Database API. Understanding these formats is essential for parsing responses and building integrations.

## API Response Wrapper

All API responses follow a consistent wrapper format:

```json
{
  "success": true,
  "data": [],
  "count": 0,
  "error": null
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Indicates if the request completed successfully |
| `data` | array \| object | The response payload (array for lists, object for single items) |
| `count` | number | Total number of items (for paginated responses) |
| `error` | string \| null | Error message if `success` is false, otherwise null |

### Success Response Example

```json
{
  "success": true,
  "data": [
    { "id": 1, "title": "Example Study" }
  ],
  "count": 1,
  "error": null
}
```

### Error Response Example

```json
{
  "success": false,
  "data": null,
  "count": 0,
  "error": "Invalid study type parameter"
}
```

## Research Entry Structure

Research entries are the primary data type in the database, representing peer-reviewed studies on ADHD in workplace contexts.

### Complete Example

```json
{
  "id": 142,
  "title": "Executive Function Interventions for Adults with ADHD in Corporate Settings",
  "authors": [
    "Smith, J.A.",
    "Johnson, M.B.",
    "Williams, K.C."
  ],
  "journal": "Journal of Occupational Health Psychology",
  "publicationDate": "2024-03-15",
  "doi": "10.1037/ocp0000123",
  "studyType": "randomized_controlled_trial",
  "evidenceLevel": "1a",
  "sampleSize": 248,

  "targetPopulation": {
    "ageRange": "25-55",
    "gender": "mixed",
    "occupation": "knowledge_workers",
    "adhdSubtype": "combined"
  },

  "methodology": {
    "design": "double-blind RCT with 12-month follow-up",
    "duration": "12 months",
    "primaryOutcomes": [
      "task_completion_rate",
      "error_frequency",
      "supervisor_ratings"
    ],
    "secondaryOutcomes": [
      "self_reported_stress",
      "job_satisfaction",
      "absenteeism"
    ]
  },

  "keyFindings": {
    "primaryResults": "Intervention group showed 34% improvement in task completion rates compared to control (p < 0.001)",
    "effectSizes": {
      "task_completion": {
        "cohens_d": 0.82,
        "confidence_interval": [0.65, 0.99],
        "interpretation": "large"
      },
      "error_reduction": {
        "cohens_d": 0.56,
        "confidence_interval": [0.39, 0.73],
        "interpretation": "medium"
      }
    },
    "clinicalSignificance": "Improvements exceeded minimal clinically important difference threshold",
    "limitations": [
      "Self-selected sample may limit generalizability",
      "Single geographic region",
      "High attrition in control group (18%)"
    ]
  },

  "workplaceRelevance": {
    "productivityImpact": "high",
    "accommodationNeeds": [
      "flexible_deadlines",
      "quiet_workspace",
      "task_management_tools",
      "regular_check_ins"
    ],
    "careerImplications": "Findings support structured intervention programs as effective workplace accommodations"
  },

  "qualityAssessment": {
    "riskOfBias": "low",
    "gradeRating": "A",
    "reviewerNotes": "Well-designed study with appropriate controls and statistical analysis"
  },

  "clinicalApplications": {
    "diagnosticUtility": "Provides validated outcome measures for workplace ADHD assessment",
    "treatmentRecommendations": [
      "Implement executive function coaching programs",
      "Combine with environmental modifications",
      "Monitor progress using standardized measures"
    ],
    "monitoringParameters": [
      "Weekly task completion logs",
      "Monthly supervisor feedback",
      "Quarterly psychometric reassessment"
    ]
  },

  "createdAt": "2024-04-01T10:30:00Z",
  "updatedAt": "2024-04-15T14:22:00Z"
}
```

### Study Type Values

| Value | Description |
|-------|-------------|
| `randomized_controlled_trial` | RCT with random assignment |
| `cohort_study` | Longitudinal observational study |
| `case_control` | Retrospective comparison study |
| `cross_sectional` | Point-in-time observational study |
| `case_series` | Description of multiple cases |
| `systematic_review` | Systematic analysis of existing studies |
| `meta_analysis` | Statistical synthesis of multiple studies |

### Evidence Level Values

| Level | Description |
|-------|-------------|
| `1a` | Systematic review of RCTs |
| `1b` | Individual RCT |
| `2a` | Systematic review of cohort studies |
| `2b` | Individual cohort study |
| `3a` | Systematic review of case-control studies |
| `3b` | Individual case-control study |
| `4` | Case series |
| `5` | Expert opinion |

## Treatment Recommendation Structure

Treatment recommendations synthesize evidence into actionable clinical guidance.

### Complete Example

```json
{
  "id": 27,
  "condition": "adult_adhd_inattentive",
  "treatmentType": "behavioral",
  "interventionName": "Cognitive Behavioral Therapy for ADHD",
  "evidenceLevel": "1b",
  "effectSize": {
    "cohens_d": 0.71,
    "confidence_interval": [0.55, 0.87],
    "nnt": 4
  },
  "recommendationStrength": "strong",
  "targetPopulation": {
    "ageRange": "18-65",
    "adhdSubtype": "inattentive",
    "setting": "outpatient",
    "severity": "moderate_to_severe"
  },
  "contraindications": [
    "Active substance use disorder",
    "Severe cognitive impairment",
    "Acute psychotic symptoms"
  ],
  "sideEffects": [
    "Initial increase in anxiety (transient)",
    "Time commitment burden",
    "Emotional processing fatigue"
  ],
  "monitoringRequirements": [
    "Baseline symptom assessment",
    "Weekly session attendance tracking",
    "Monthly outcome measure administration",
    "Treatment response evaluation at 8 weeks"
  ],
  "sourcedFrom": [142, 156, 189],
  "lastReviewed": "2024-02-01",
  "createdAt": "2023-09-15T08:00:00Z",
  "updatedAt": "2024-02-01T16:45:00Z"
}
```

### Recommendation Strength Values

| Value | Description |
|-------|-------------|
| `strong` | Benefits clearly outweigh risks; most patients should receive |
| `moderate` | Benefits likely outweigh risks; many patients should receive |
| `conditional` | Benefits and risks closely balanced; patient preference important |
| `weak` | Limited evidence; consider individual circumstances |

## Assessment Tool Structure

Assessment tools are validated instruments for measuring ADHD symptoms and outcomes.

### Complete Example

```json
{
  "id": 12,
  "name": "Adult ADHD Self-Report Scale",
  "acronym": "ASRS",
  "purpose": "Screening and symptom monitoring for adult ADHD",
  "targetPopulation": {
    "ageRange": "18+",
    "setting": "clinical_and_workplace",
    "languages": ["en", "es", "fr", "de", "zh"]
  },
  "administrationTime": "5-10 minutes",
  "domains": [
    "inattention",
    "hyperactivity",
    "impulsivity",
    "executive_function"
  ],
  "psychometricProperties": {
    "reliability": {
      "internal_consistency": {
        "cronbachs_alpha": 0.88,
        "interpretation": "good"
      },
      "test_retest": {
        "icc": 0.84,
        "interval": "2 weeks",
        "interpretation": "good"
      }
    },
    "validity": {
      "sensitivity": 0.91,
      "specificity": 0.74,
      "ppv": 0.78,
      "npv": 0.89,
      "auc": 0.87,
      "criterion_validity": {
        "comparison": "clinical_interview",
        "correlation": 0.82
      },
      "construct_validity": {
        "factor_structure": "two_factor",
        "cfi": 0.95,
        "rmsea": 0.06
      }
    },
    "normative_data": {
      "sample_size": 3200,
      "demographics": "US adult population",
      "cutoff_scores": {
        "likely_adhd": 14,
        "possible_adhd": 10
      }
    }
  },
  "clinicalUtility": "High utility for initial screening; should be combined with clinical interview for diagnosis",
  "limitations": [
    "Self-report bias",
    "Not diagnostic alone",
    "May underdetect inattentive subtype",
    "Cultural validation limited in some populations"
  ],
  "licensingInfo": {
    "availability": "free",
    "source": "WHO",
    "url": "https://www.hcp.med.harvard.edu/ncs/asrs.php"
  },
  "createdAt": "2023-06-01T09:00:00Z",
  "updatedAt": "2024-01-20T11:30:00Z"
}
```

## Effect Sizes JSON Format

Effect sizes quantify the magnitude of research findings. The API uses a standardized format:

```json
{
  "outcome_name": {
    "cohens_d": 0.75,
    "confidence_interval": [0.58, 0.92],
    "interpretation": "medium",
    "p_value": 0.001,
    "sample_size": 124
  }
}
```

### Interpretation Guidelines

| Cohen's d | Interpretation |
|-----------|----------------|
| < 0.2 | negligible |
| 0.2 - 0.5 | small |
| 0.5 - 0.8 | medium |
| > 0.8 | large |

### Additional Effect Size Metrics

When applicable, responses may include:

```json
{
  "hedges_g": 0.73,
  "odds_ratio": 2.4,
  "risk_ratio": 1.8,
  "nnt": 5,
  "r_squared": 0.42
}
```

## Psychometric Properties JSON Format

Assessment tools include detailed psychometric information:

```json
{
  "reliability": {
    "internal_consistency": {
      "cronbachs_alpha": 0.88,
      "mcdonalds_omega": 0.89,
      "interpretation": "good"
    },
    "test_retest": {
      "icc": 0.84,
      "pearson_r": 0.86,
      "interval": "2 weeks"
    },
    "inter_rater": {
      "kappa": 0.82,
      "interpretation": "substantial"
    }
  },
  "validity": {
    "sensitivity": 0.91,
    "specificity": 0.74,
    "ppv": 0.78,
    "npv": 0.89,
    "auc": 0.87
  }
}
```

## Statistics Response Format

The `/statistics` endpoint returns aggregated database metrics:

```json
{
  "success": true,
  "data": {
    "totalEntries": 1247,
    "byStudyType": {
      "randomized_controlled_trial": 312,
      "cohort_study": 428,
      "case_control": 156,
      "cross_sectional": 198,
      "systematic_review": 89,
      "meta_analysis": 64
    },
    "byEvidenceLevel": {
      "1a": 64,
      "1b": 312,
      "2a": 89,
      "2b": 428,
      "3a": 45,
      "3b": 156,
      "4": 98,
      "5": 55
    },
    "byYear": {
      "2024": 156,
      "2023": 312,
      "2022": 289,
      "2021": 245,
      "2020": 145
    },
    "treatmentRecommendations": 87,
    "assessmentTools": 34,
    "lastUpdated": "2024-04-15T00:00:00Z"
  },
  "count": 1,
  "error": null
}
```

## Error Response Format

All errors follow a consistent structure:

```json
{
  "success": false,
  "data": null,
  "count": 0,
  "error": "Descriptive error message"
}
```

### Common Error Messages

| Error | Cause |
|-------|-------|
| `"Invalid study type parameter"` | Unrecognized study type value |
| `"Entry not found"` | Requested ID does not exist |
| `"Invalid date format"` | Date not in ISO 8601 format |
| `"Missing required field: title"` | Required field omitted in request |
| `"Rate limit exceeded"` | Too many requests |

## TypeScript Interfaces

For TypeScript developers, here are interface definitions:

```typescript
interface ApiResponse<T> {
  success: boolean;
  data: T | null;
  count: number;
  error: string | null;
}

interface ResearchEntry {
  id: number;
  title: string;
  authors: string[];
  journal: string;
  publicationDate: string;
  doi: string;
  studyType: StudyType;
  evidenceLevel: EvidenceLevel;
  sampleSize: number;
  targetPopulation: TargetPopulation;
  methodology: Methodology;
  keyFindings: KeyFindings;
  workplaceRelevance: WorkplaceRelevance;
  qualityAssessment: QualityAssessment;
  clinicalApplications: ClinicalApplications;
  createdAt: string;
  updatedAt: string;
}

interface EffectSize {
  cohens_d: number;
  confidence_interval: [number, number];
  interpretation: 'negligible' | 'small' | 'medium' | 'large';
  p_value?: number;
  sample_size?: number;
}

interface TreatmentRecommendation {
  id: number;
  condition: string;
  treatmentType: string;
  interventionName: string;
  evidenceLevel: EvidenceLevel;
  effectSize: EffectSize & { nnt?: number };
  recommendationStrength: 'strong' | 'moderate' | 'conditional' | 'weak';
  targetPopulation: Record<string, string>;
  contraindications: string[];
  sideEffects: string[];
  monitoringRequirements: string[];
  sourcedFrom: number[];
  lastReviewed: string;
}

interface AssessmentTool {
  id: number;
  name: string;
  acronym: string;
  purpose: string;
  targetPopulation: Record<string, unknown>;
  administrationTime: string;
  domains: string[];
  psychometricProperties: PsychometricProperties;
  clinicalUtility: string;
  limitations: string[];
  licensingInfo: LicensingInfo;
}

type StudyType =
  | 'randomized_controlled_trial'
  | 'cohort_study'
  | 'case_control'
  | 'cross_sectional'
  | 'case_series'
  | 'systematic_review'
  | 'meta_analysis';

type EvidenceLevel = '1a' | '1b' | '2a' | '2b' | '3a' | '3b' | '4' | '5';
```

---

*Part of the ADHD Research Database documentation. For API usage examples, see the [API Reference](./api-reference.md).*
