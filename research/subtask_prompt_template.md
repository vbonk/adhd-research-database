'''
**Mission:** Research the topic "{{input}}" within the context of adult male ADHD (25-65, professional) and generate a single, validated knowledge entry in JSON format.

**Avatar Focus:** Professional, intelligent, working-age men (25-65) with potential or diagnosed ADD.

**Research Domains:**
1.  **Adult Male ADD Identification & Assessment:** Late diagnosis, masking, professional context.
2.  **Workplace & Career Impact:** Executive function, time management, accommodations.
3.  **Evidence-Based Treatments:** Medications, therapy, coaching, lifestyle interventions.
4.  **Life Management & Relationships:** Marriage, parenting, financial management.
5.  **Developmental Context:** Childhood patterns informing adult presentation.

**Methodology:**
1.  **Search:** Use academic databases (PubMed, PsycINFO, Google Scholar) to find high-quality sources (systematic reviews, meta-analyses, RCTs).
2.  **Extract:** Synthesize the most critical finding relevant to the target avatar.
3.  **Structure:** Populate the JSON schema below with the extracted information. Ensure 100% compliance.
4.  **Validate:** Double-check all fields for accuracy, especially `evidence_level`, `certainty_grade`, and `citations` (must include a valid DOI or URL).

**JSON Output Schema (Strict Compliance Required):**
```json
{
  "knowledge_id": "ADD-[Domain]-[UniqueId]",
  "domain": "string",
  "subtopic": "string",
  "knowledge_point": "string (max 200 chars)",
  "population": "string",
  "study_design": "string",
  "evidence_level": "integer",
  "effect_size": "string",
  "sample_size": "string",
  "risk_of_bias": "string",
  "certainty_grade": "string",
  "heterogeneity": {
    "I2": "number",
    "tau2": "number"
  },
  "publication_bias": {
    "method": "string",
    "result": "string"
  },
  "outcomes": ["string"],
  "limitations": "string",
  "funding_conflicts": "string",
  "ontology_codes": [{"system": "string", "code": "string"}],
  "citations": [{"type": "string", "value": "string"}],
  "keywords": ["string"],
  "actionable_insights": ["string"],
  "confidence_components": {
    "evidence_level": "integer",
    "sample_size": "integer",
    "recency_score": "number",
    "risk_of_bias": "string",
    "replication": "string",
    "heterogeneity_penalty": "number"
  },
  "confidence_score": "integer",
  "social_sentiment": "string",
  "last_updated": "YYYY-MM-DD"
}
```
'''

