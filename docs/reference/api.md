---
title: API Reference
description: Complete API documentation for the ADHD Research Database REST endpoints
audience: developer
difficulty: intermediate
---

# API Reference

This document provides complete documentation for the ADHD Research Database REST API. The API provides programmatic access to evidence-based ADHD research, treatment recommendations, and assessment tools.

## Overview

The ADHD Research Database exposes a RESTful API for accessing research data programmatically. All endpoints return JSON responses and follow consistent conventions for error handling and response formatting.

### Base URL

```
http://localhost:5000/api
```

For production deployments, replace `localhost:5000` with your production domain.

### API Version

The current API version is **v1** (implicit in the base URL). Future versions will be explicitly versioned in the URL path.

## Authentication

**Current Status: No authentication required**

The API is currently open and does not require authentication. All endpoints are publicly accessible. This may change in future versions if user-specific features are added.

> **Note for Production**: If deploying in a production environment with sensitive data or rate limiting requirements, consider implementing API key authentication or OAuth 2.0.

## Response Format

All API responses follow a consistent JSON structure:

```json
{
  "success": true,
  "data": [...],
  "count": 42,
  "error": null
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Indicates whether the request was successful |
| `data` | array or object | The requested data (null on error) |
| `count` | number | Total number of items returned (for list endpoints) |
| `error` | string or null | Error message if success is false, null otherwise |

### Success Response Example

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "title": "Methylphenidate Efficacy Meta-Analysis",
      "evidence_level": "LEVEL_1A"
    }
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
  "error": "Resource not found"
}
```

---

## Endpoints

### Research Endpoints

#### GET /api/research

Retrieves all research entries with optional filtering.

**Description**

Returns a list of research entries from the database. Results can be filtered by evidence level, search terms, and workplace focus. Without filters, returns all research entries.

**Query Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `evidence_level` | string | No | Filter by evidence quality level |
| `search` | string | No | Full-text search across titles and abstracts |
| `workplace_focus` | boolean | No | Filter for workplace-related research only |

**Evidence Level Values**

| Value | Description |
|-------|-------------|
| `LEVEL_1A` | Systematic reviews of RCTs |
| `LEVEL_1B` | Individual RCTs with narrow CI |
| `LEVEL_2A` | Systematic reviews of cohort studies |
| `LEVEL_2B` | Individual cohort studies |
| `LEVEL_3A` | Systematic reviews of case-control studies |
| `LEVEL_3B` | Individual case-control studies |
| `LEVEL_4` | Case series |
| `LEVEL_5` | Expert opinion |

**Response**

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "title": "Methylphenidate for ADHD: A Systematic Review",
      "authors": "Smith J, Johnson M, Williams K",
      "publication_year": 2023,
      "journal": "Journal of ADHD Research",
      "evidence_level": "LEVEL_1A",
      "abstract": "This systematic review examines...",
      "workplace_focus": false,
      "tags": ["medication", "stimulants", "meta-analysis"],
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ],
  "count": 1,
  "error": null
}
```

**Example Requests**

Get all research:

```bash
curl -X GET "http://localhost:5000/api/research"
```

Filter by evidence level:

```bash
curl -X GET "http://localhost:5000/api/research?evidence_level=LEVEL_1A"
```

Search for specific terms:

```bash
curl -X GET "http://localhost:5000/api/research?search=methylphenidate"
```

Filter for workplace-focused research:

```bash
curl -X GET "http://localhost:5000/api/research?workplace_focus=true"
```

Combine multiple filters:

```bash
curl -X GET "http://localhost:5000/api/research?evidence_level=LEVEL_1B&workplace_focus=true&search=accommodations"
```

---

#### GET /api/research/{id}

Retrieves a specific research entry by its unique identifier.

**Description**

Returns the full details of a single research entry, including all metadata, tags, and associated information.

**Path Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | The unique identifier of the research entry |

**Response**

```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "Methylphenidate for ADHD: A Systematic Review",
    "authors": "Smith J, Johnson M, Williams K",
    "publication_year": 2023,
    "journal": "Journal of ADHD Research",
    "doi": "10.1234/adhd.2023.001",
    "evidence_level": "LEVEL_1A",
    "abstract": "This systematic review examines the efficacy of methylphenidate in treating ADHD symptoms across multiple randomized controlled trials...",
    "methodology": "Systematic review with meta-analysis of 45 RCTs",
    "sample_size": 5420,
    "key_findings": "Methylphenidate demonstrated significant improvement in ADHD symptoms with moderate effect size (d=0.78)",
    "limitations": "Publication bias detected; limited long-term follow-up data",
    "workplace_focus": false,
    "workplace_implications": null,
    "tags": ["medication", "stimulants", "meta-analysis", "efficacy"],
    "related_research_ids": [5, 12, 23],
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  },
  "count": 1,
  "error": null
}
```

**Error Response (Not Found)**

```json
{
  "success": false,
  "data": null,
  "count": 0,
  "error": "Research entry with id 999 not found"
}
```

**Example Request**

```bash
curl -X GET "http://localhost:5000/api/research/1"
```

---

#### GET /api/research/stats

Retrieves aggregate statistics about the research database.

**Description**

Returns summary statistics including total counts, breakdowns by evidence level, and other aggregate metrics useful for understanding the database contents.

**Response**

```json
{
  "success": true,
  "data": {
    "total_entries": 156,
    "by_evidence_level": {
      "LEVEL_1A": 12,
      "LEVEL_1B": 28,
      "LEVEL_2A": 18,
      "LEVEL_2B": 35,
      "LEVEL_3A": 8,
      "LEVEL_3B": 22,
      "LEVEL_4": 19,
      "LEVEL_5": 14
    },
    "workplace_focused": 43,
    "by_publication_year": {
      "2024": 15,
      "2023": 42,
      "2022": 38,
      "2021": 31,
      "2020": 20,
      "earlier": 10
    },
    "top_tags": [
      {"tag": "medication", "count": 67},
      {"tag": "workplace", "count": 43},
      {"tag": "assessment", "count": 38},
      {"tag": "cognitive-behavioral", "count": 29},
      {"tag": "accommodations", "count": 25}
    ],
    "last_updated": "2024-01-20T14:22:00Z"
  },
  "count": 1,
  "error": null
}
```

**Example Request**

```bash
curl -X GET "http://localhost:5000/api/research/stats"
```

---

### Treatment Endpoints

#### GET /api/treatments

Retrieves all treatment recommendations from the database.

**Description**

Returns a comprehensive list of treatment recommendations derived from the research evidence. Each treatment includes efficacy ratings, evidence quality indicators, and practical implementation guidance.

**Response**

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Methylphenidate",
      "category": "Pharmacological",
      "subcategory": "Stimulant Medications",
      "description": "First-line medication treatment for ADHD",
      "efficacy_rating": "High",
      "evidence_level": "LEVEL_1A",
      "age_groups": ["children", "adolescents", "adults"],
      "considerations": "Requires prescription; monitor for cardiovascular effects",
      "contraindications": ["Uncontrolled hypertension", "Glaucoma", "MAO inhibitor use"],
      "supporting_research_ids": [1, 5, 12],
      "workplace_applicable": true
    },
    {
      "id": 2,
      "name": "Cognitive Behavioral Therapy",
      "category": "Psychosocial",
      "subcategory": "Behavioral Interventions",
      "description": "Structured therapy focusing on executive function skills",
      "efficacy_rating": "Moderate-High",
      "evidence_level": "LEVEL_1B",
      "age_groups": ["adolescents", "adults"],
      "considerations": "Best combined with medication for optimal outcomes",
      "contraindications": [],
      "supporting_research_ids": [8, 15, 22],
      "workplace_applicable": true
    }
  ],
  "count": 2,
  "error": null
}
```

**Example Request**

```bash
curl -X GET "http://localhost:5000/api/treatments"
```

---

### Assessment Endpoints

#### GET /api/assessments

Retrieves all assessment tools documented in the database.

**Description**

Returns a list of validated assessment instruments for ADHD screening, diagnosis, and symptom monitoring. Includes psychometric properties and appropriate use cases.

**Response**

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Adult ADHD Self-Report Scale (ASRS-v1.1)",
      "abbreviation": "ASRS",
      "type": "Screening",
      "target_population": "Adults (18+)",
      "administration_time": "5 minutes",
      "items": 18,
      "domains": ["Inattention", "Hyperactivity-Impulsivity"],
      "scoring_method": "Symptom checklist with frequency ratings",
      "psychometrics": {
        "sensitivity": 0.91,
        "specificity": 0.74,
        "internal_consistency": 0.88
      },
      "validation_studies": [3, 17],
      "free_access": true,
      "source_url": "https://www.hcp.med.harvard.edu/ncs/asrs.php"
    },
    {
      "id": 2,
      "name": "Conners Adult ADHD Rating Scales",
      "abbreviation": "CAARS",
      "type": "Diagnostic/Monitoring",
      "target_population": "Adults (18+)",
      "administration_time": "15-20 minutes",
      "items": 66,
      "domains": ["Inattention", "Hyperactivity", "Impulsivity", "Self-Concept"],
      "scoring_method": "T-scores with normative comparison",
      "psychometrics": {
        "sensitivity": 0.85,
        "specificity": 0.82,
        "internal_consistency": 0.92
      },
      "validation_studies": [9, 14, 28],
      "free_access": false,
      "source_url": "https://www.pearsonclinical.com"
    }
  ],
  "count": 2,
  "error": null
}
```

**Example Request**

```bash
curl -X GET "http://localhost:5000/api/assessments"
```

---

### Tag Endpoints

#### GET /api/tags

Retrieves all available tags used to categorize research entries.

**Description**

Returns a list of all tags currently in use across the research database, along with usage counts. Useful for building filter interfaces or understanding the topical coverage of the database.

**Response**

```json
{
  "success": true,
  "data": [
    {
      "name": "medication",
      "count": 67,
      "category": "Treatment"
    },
    {
      "name": "workplace",
      "count": 43,
      "category": "Context"
    },
    {
      "name": "assessment",
      "count": 38,
      "category": "Evaluation"
    },
    {
      "name": "cognitive-behavioral",
      "count": 29,
      "category": "Treatment"
    },
    {
      "name": "accommodations",
      "count": 25,
      "category": "Intervention"
    },
    {
      "name": "executive-function",
      "count": 21,
      "category": "Symptom Domain"
    },
    {
      "name": "meta-analysis",
      "count": 18,
      "category": "Study Type"
    },
    {
      "name": "stimulants",
      "count": 15,
      "category": "Treatment"
    }
  ],
  "count": 8,
  "error": null
}
```

**Example Request**

```bash
curl -X GET "http://localhost:5000/api/tags"
```

---

## Error Handling

### HTTP Status Codes

The API uses standard HTTP status codes to indicate request outcomes:

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| `200` | OK | Request successful |
| `400` | Bad Request | Invalid request parameters |
| `404` | Not Found | Requested resource does not exist |
| `500` | Internal Server Error | Unexpected server error |

### Common Error Responses

#### Invalid Query Parameter

```json
{
  "success": false,
  "data": null,
  "count": 0,
  "error": "Invalid evidence_level value. Must be one of: LEVEL_1A, LEVEL_1B, LEVEL_2A, LEVEL_2B, LEVEL_3A, LEVEL_3B, LEVEL_4, LEVEL_5"
}
```

#### Resource Not Found

```json
{
  "success": false,
  "data": null,
  "count": 0,
  "error": "Research entry with id 999 not found"
}
```

#### Server Error

```json
{
  "success": false,
  "data": null,
  "count": 0,
  "error": "An unexpected error occurred. Please try again later."
}
```

### Error Handling Best Practices

When integrating with the API:

1. **Always check the `success` field** before processing `data`
2. **Handle 404 errors gracefully** - resources may be removed over time
3. **Implement retry logic** for 500 errors with exponential backoff
4. **Log error messages** from the `error` field for debugging

---

## Rate Limiting

**Current Status: No rate limiting implemented**

The API does not currently enforce rate limits. However, to ensure fair usage and system stability:

- Avoid making more than 100 requests per minute
- Cache responses where appropriate
- Use batch requests when available

> **Note**: Rate limiting may be implemented in future versions. Monitor the response headers for `X-RateLimit-*` headers if added.

---

## Best Practices

### Efficient API Usage

1. **Use filters to reduce response size**
   ```bash
   # Instead of fetching all and filtering client-side
   curl "http://localhost:5000/api/research?evidence_level=LEVEL_1A"
   ```

2. **Cache static data**
   Tags and assessment tools change infrequently. Cache these responses.

3. **Request only what you need**
   Use the list endpoint for overviews, detail endpoint only when needed.

### Integration Patterns

**Python Example**

```python
import requests

BASE_URL = "http://localhost:5000/api"

def get_research(evidence_level=None, search=None):
    params = {}
    if evidence_level:
        params["evidence_level"] = evidence_level
    if search:
        params["search"] = search

    response = requests.get(f"{BASE_URL}/research", params=params)
    data = response.json()

    if data["success"]:
        return data["data"]
    else:
        raise Exception(data["error"])

# Usage
level_1_research = get_research(evidence_level="LEVEL_1A")
```

**JavaScript Example**

```javascript
const BASE_URL = 'http://localhost:5000/api';

async function getResearch(options = {}) {
  const params = new URLSearchParams();

  if (options.evidenceLevel) {
    params.append('evidence_level', options.evidenceLevel);
  }
  if (options.search) {
    params.append('search', options.search);
  }

  const response = await fetch(`${BASE_URL}/research?${params}`);
  const data = await response.json();

  if (data.success) {
    return data.data;
  } else {
    throw new Error(data.error);
  }
}

// Usage
const research = await getResearch({ evidenceLevel: 'LEVEL_1A' });
```

---

## Changelog

### Version 1.0 (Current)

- Initial API release
- Research CRUD endpoints
- Treatment recommendations endpoint
- Assessment tools endpoint
- Tags endpoint
- Statistics endpoint

---

## Support

For API issues or feature requests:

- **GitHub Issues**: Report bugs or request features on the project repository
- **Documentation**: Check the full documentation for additional context

---

## Attribution

This API provides access to the ADHD Research Database, a curated collection of evidence-based ADHD research. All research data is sourced from peer-reviewed publications and attributed to original authors.

When using data from this API in publications or applications, please cite:

> ADHD Research Database. (2024). Evidence-Based ADHD Research API. Retrieved from http://localhost:5000/api

---

*Last updated: 2024*
