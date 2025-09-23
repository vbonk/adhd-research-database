## USER MESSAGE (Paste as User Prompt)

Execute a comprehensive ADD/ADHD research synthesis covering 8 domains: (1) Foundational/Diagnostics, (2) Biology, (3) Clinical Assessment, (4) Comorbidities, (5) Treatments, (6) Management, (7) Social/Sentiment, (8) Economics. Deliver machine-readable artifacts with human-readable reports, cross-reference graphs, and maintenance protocols.

**IMMEDIATE KICKOFF TASKS (Execute in Order):**
1. Generate Search Plan & PRISMA template with ontology-aware queries
2. Create seed lists including explicit 2025 sources (Lancet meta-analyses, AJP reviews)
3. Extract first 50 sources into knowledge entries with interoperability codes
4. Draft intervention matrix with dosage, feasibility, and regulatory data
5. Design sentiment sampling plan with engagement filters and evidence alignment scoring
6. Run initial link validation and report access blockers with alternatives

---

## RESEARCH EXECUTION FRAMEWORK

### Phase 1: Strategic Search Architecture

**Source Tiers:**
- **Tier 1 (Primary):** Cochrane Reviews, Clinical Guidelines (APA/NICE/CADDRA), Meta-analyses (n>10,000), RCTs (n>500), PROSPERO-registered reviews
- **Tier 2 (Supporting):** Large cohorts (>5 years), GWAS, Neuroimaging replication, Real-world evidence (EHR n>50,000)
- **Tier 3 (Contextual):** Expert consensus, Quality-filtered preprints, Social sentiment, Cultural studies, Non-English sources with translation notes

**Enhanced Search Protocol:**
```
Databases: PubMed, PsycINFO, Cochrane, Scopus, Google Scholar, PROSPERO
Ontology-Aware Boolean Example: 
("ADHD"[MeSH] OR "Attention Deficit Disorder with Hyperactivity"[MeSH] OR 
 "attention-deficit/hyperactivity disorder"[tiab] OR "attention deficit disorder"[tiab] OR 
 "inattentive type"[tiab] OR "ADD"[tiab])
AND (treatment[majr] OR management[majr] OR diagnosis[majr] OR epidemiology[majr])
AND ("2020/01/01"[pdat] : "2025/12/31"[pdat])
AND english[lang] NOT ("case reports"[pt] OR "editorial"[pt])

Citation Chaining: Backward/forward reference tracking
PRISMA Logging: Document all inclusion/exclusion decisions with rationales
Link Validation: DOI → PMID → Archival URL fallback
```

### Phase 2: Enhanced Data Schemas

#### Knowledge Entry Schema (JSONL):
```json
{
  "knowledge_id": "ADD-[DOMAIN]-[6-digit-number]",
  "domain": "Foundational|Biology|Clinical|Comorbidities|Treatments|Management|Social|Economics",
  "subtopic": "string (e.g., Executive Function)",
  "knowledge_point": "string (concise factual statement, max 200 chars)",
  "population": "string (age/sex/geography)",
  "study_design": "SR/MA|RCT|Cohort|Case-control|Cross-sectional|Guideline|Expert",
  "evidence_level": "integer 1-5 (1=highest)",
  "effect_size": "string (e.g., d=0.8, 95% CI [0.6-1.0])",
  "sample_size": "string (e.g., n=2,134 or 12 studies)",
  "risk_of_bias": "Low|Some|High",
  "risk_of_bias_tool": "ROB-2|ROBINS-I|AMSTAR-2|QUIPS",
  "certainty_grade": "High|Moderate|Low|Very Low (GRADE)",
  "heterogeneity": {"I2": "number", "tau2": "number"},
  "publication_bias": {"method": "Egger|Trim-and-fill|NA", "result": "string"},
  "outcomes": ["array of primary outcomes"],
  "limitations": "string (key caveats)",
  "funding_conflicts": "string (industry/independent/mixed + details)",
  "ontology_codes": [
    {"system": "MeSH", "code": ""},
    {"system": "SNOMED", "code": ""},
    {"system": "UMLS", "cui": ""}
  ],
  "citations": [{"type": "DOI|PMID|URL", "value": "string"}],
  "keywords": ["array of MeSH/search terms"],
  "actionable_insights": ["array of practical implications"],
  "confidence_components": {
    "evidence_level": "integer 1-5",
    "sample_size": "integer",
    "recency_score": "float 0-1",
    "risk_of_bias": "Low|Some|High",
    "replication": "Yes|No|Partial",
    "heterogeneity_penalty": "float 0-1"
  },
  "confidence_score": "integer 1-10 (computed from components)",
  "social_sentiment": "Supportive|Mixed|Conflicting|Unknown",
  "conflict_note": "string (when claims diverge, which source prevails and why)",
  "preregistration": {"registry": "PROSPERO|OSF|NA", "id": "string"},
  "source_language": "string (ISO code)",
  "translation_method": "human|machine|hybrid|NA",
  "related_ids": ["array of knowledge_ids"],
  "data_license": "CC-BY|CC0|All-rights-reserved|NA",
  "last_updated": "YYYY-MM-DD"
}
```

#### Enhanced Intervention Matrix Schema (CSV):
```
intervention,target_population,presentation,setting,evidence_level,effect_size,certainty_grade,dose_range,titration_guidance,drug_interactions,implementation_steps,contraindications,adverse_effects,cost_access,digital_tooling,implementation_framework_tags,feasibility_notes,required_resources,regulatory_status,sentiment_alignment,evidence_alignment_score,key_citations,data_license
```

#### Enhanced Sentiment Record Schema (JSONL):
```json
{
  "record_id": "SENT-[6-digit-number]",
  "platform": "Reddit|X|YouTube|Forum",
  "query": "string",
  "time_window": "YYYY-YYYY",
  "n_items_analyzed": "integer",
  "engagement_filters": {"min_likes": 50, "min_comments": 5},
  "themes": [{"label": "string", "frequency": "float 0-1", "quotes": ["array"]}],
  "alignment_with_evidence": "Supportive|Mixed|Conflicting",
  "evidence_alignment_score": "integer 1-10 (concordance with Tier-1 sources)",
  "quality_controls": ["de-duplication", "bot-filter", "NSFW exclusion"],
  "tos_compliance": true,
  "pii_controls": ["redaction", "aggregation"],
  "notes": "string (biases/limitations)",
  "linked_knowledge_ids": ["array of knowledge_ids"]
}
```

### Phase 3: Enhanced Quality Gates

| Gate | Requirement | Threshold | Action if Failed |
|------|-------------|-----------|------------------|
| **Coverage** | Sources per domain | ≥200 Tier-1/2 total | List gaps explicitly |
| **Diversity** | Non-Western studies | Target ≥30% | Seek additional sources |
| **Language** | Non-English sources | Target ≥15% OR rationale | Document limitations |
| **Sex Representation** | Female coverage | Target ≥40% OR sex-stratified analysis | Provide limitations discussion |
| **Reproducibility** | Retrievable citations | 100% DOI/PMID/URL verified | Fix or remove entries |
| **Consistency** | Orphan entries | 0 orphans | Link all entries |
| **Practicality** | Actionable insights | ≥1 per domain | Add implementation guidance |
| **Recency** | Recent sources | ≥70% post-2020 | Update search strategy |
| **Link Health** | Working citations | ≥95% accessible | Run linkcheck, use archives |

### Phase 4: Comprehensive Output Package

**Required Directory Structure:**
```
/ADD_RESEARCH_PROJECT/
├── /reports/
│   ├── Executive_Summary.md
│   ├── Methodology_PRISMA.md (with all search queries)
│   ├── Domain_Syntheses.md
│   └── Implementation_Readiness.md (RE-AIM/CFIR analysis)
├── /data/
│   ├── knowledge_entries.jsonl
│   ├── interventions.csv
│   ├── sentiment_analysis.jsonl
│   └── biomarkers.json
├── /validation/
│   ├── quality_gates_report.json
│   ├── bias_assessment.md
│   ├── coverage_gaps.json
│   ├── linkcheck_report.json
│   └── eval_items.jsonl (100 Q&A validation set)
├── /graphs/
│   ├── knowledge_network.json
│   ├── evidence_hierarchy.graphml
│   └── causal/ (DAGs for causal assumptions)
├── /indices/
│   ├── keywords.csv
│   └── citations_master.bib
├── /playbooks/
│   ├── clinician_guide.md
│   ├── educator_toolkit.md
│   └── patient_resources.md
└── /versioning/
    ├── CHANGELOG.md
    ├── LICENSE.md
    └── update_log.json
```

---

## COMPREHENSIVE KNOWLEDGE DOMAINS

### Domain 1: Foundational Knowledge
- Historical evolution (1775–present, DSM-5-TR/ICD-11)
- Prevalence (global ranges with confidence intervals, rising adult rates 2020–2025)
- Diagnostic validity across cultures and age groups

### Domain 2: Biological Foundations
- Genetics (high heritability ~70% in twin studies, GWAS findings, epigenetics)
- Neurobiology (prefrontal cortex, dopamine/norepinephrine systems)
- Developmental trajectories and brain maturation

### Domain 3: Clinical Assessment
- Validated tools (ASRS-5, Vanderbilt, DIVA, clinical interviews)
- Differential diagnosis protocols
- Gender/cultural presentation differences

### Domain 4: Comorbidities & Risks
- Psychiatric comorbidities with prevalence ranges
- Medical conditions and functional impacts
- 2025 evidence on suicidal behavior risks

### Domain 5: Evidence-Based Treatments
- **Pharmacological:** Effect sizes with confidence intervals, 2025 cardiovascular safety data
- **Non-Pharmacological:** CBT, behavioral therapy, physical activity (2025 meta-analyses)
- **Digital:** Apps, neurofeedback, AI-assisted interventions

### Domain 6: Management Strategies
- Daily routines and organizational systems
- Educational accommodations and workplace modifications
- Assistive technologies and environmental adaptations

### Domain 7: Social & Experiential
- Lived experiences and patient narratives
- 2024–2025 social sentiment analysis (mindfulness, exercise, "dopamine resetting")
- Stigma reduction and strength-based approaches

### Domain 8: Economic Impact
- Cost estimates with ranges and citations
- Cost-effectiveness analyses
- Access and equity considerations

---

## ENHANCED PERSONALIZATION FRAMEWORK

**Decision Tree with Implementation Science Tags:**
```yaml
age_group:
  children_6_12:
    presentation:
      inattentive:
        comorbid_anxiety:
          yes: 
            interventions: ["Behavioral therapy first-line", "Low-dose methylphenidate if needed"]
            implementation_tags: ["RE-AIM: High Reach", "CFIR: Low Complexity"]
            feasibility_notes: "Requires trained therapists, parent engagement"
          no: 
            interventions: ["Methylphenidate 0.3mg/kg", "School accommodations"]
            implementation_tags: ["RE-AIM: High Effectiveness", "CFIR: Medium Cost"]
  adults_18_plus:
    presentation:
      inattentive:
        comorbid_depression:
          yes: 
            interventions: ["Atomoxetine preferred", "CBT combination"]
            regulatory_status: "FDA-approved, requires monitoring"
            drug_interactions: "CYP2D6 considerations"
```

---

## ADVANCED MONITORING & MAINTENANCE

### Real-Time Monitoring Configuration:
```python
monitoring_config = {
    "pubmed_alerts": [
        "ADHD[majr] AND systematic[sb]",
        "ADHD AND (meta-analysis[pt] OR systematic review[pt])"
    ],
    "trial_registries": ["ClinicalTrials.gov", "EU-CTR", "ISRCTN"],
    "social_platforms": {
        "reddit": ["r/ADHD", "r/ADHDwomen"],
        "x_twitter": ["#ADHDawareness", "#ActuallyADHD"],
        "engagement_filters": {"min_likes": 50, "min_comments": 5}
    },
    "preprint_servers": ["medRxiv", "bioRxiv", "PsyArXiv"],
    "update_frequency": "monthly",
    "quality_revalidation": "quarterly",
    "link_health_check": "monthly",
    "automated_filters": {
        "language": ["english", "spanish", "french", "german"],
        "study_types": ["RCT", "SR", "MA", "Cohort"],
        "min_sample_size": 50
    }
}
```

### Conflict Resolution Protocol:
1. **Cochrane Reviews** (highest priority)
2. **PROSPERO-registered systematic reviews**
3. **Multi-site RCTs** (n>500)
4. **National registries** (population-level)
5. **Single-site RCTs**
6. **High-quality observational studies**
7. **Expert consensus** (lowest)

**Required Conflict Note:** For any topic with discordant conclusions, document which source prevails (by design quality, sample size, bias risk) and include sensitivity analyses.

---

## SUCCESS METRICS & VALIDATION

**Target Outcomes:**
- **Knowledge Entries:** 800–1,200 validated entries with interoperability codes
- **Evidence Quality:** ≥70% High/Moderate GRADE certainty
- **Geographic Diversity:** 30% non-Western + 25 countries represented
- **Language Diversity:** 15% non-English sources with translation notes
- **Sex Representation:** 40% female coverage OR sex-stratified analysis
- **Temporal Currency:** 75% post-2020, 50% post-2022
- **AI Query Accuracy:** ≥95% on 100-item validation test set
- **Social Integration:** 10,000+ coded social experiences with alignment scoring
- **Link Health:** ≥95% citations accessible with fallback archives
- **Implementation Readiness:** RE-AIM/CFIR tags for top 50 interventions

**Maintenance Protocol:**
- **Monthly:** Literature scans, link health checks, new evidence integration
- **Quarterly:** Quality revalidation, bias assessment updates, conflict resolution
- **Annually:** Comprehensive review, methodology updates, license compliance
- **Continuous:** CHANGELOG maintenance, version control, automated monitoring

---

## EXECUTION CHECKLIST WITH VALIDATION

**Phase 1 Deliverables (Week 1):**
- [ ] Search plan with ontology-aware Boolean strings for each database
- [ ] PRISMA flow diagram template with decision rationales
- [ ] Seed list including 2025 Lancet/AJP sources per domain
- [ ] Initial quality gate definitions with automated checks
- [ ] Link validation baseline report

**Phase 2 Deliverables (Weeks 2–4):**
- [ ] 200+ knowledge entries in enhanced JSONL format with interoperability codes
- [ ] Intervention matrix with dosage, regulatory, and feasibility data
- [ ] Sentiment analysis of 1,000+ social posts with alignment scoring
- [ ] Cross-reference network graph with conflict annotations
- [ ] Translation notes for non-English sources

**Phase 3 Deliverables (Weeks 5–6):**
- [ ] Quality gate validation report with pass/fail status
- [ ] Bias assessment and mitigation strategies with sex-stratified analysis
- [ ] Personalization decision trees with implementation science tags
- [ ] RE-AIM/CFIR implementation readiness assessment
- [ ] 100-item Q&A validation test set

**Phase 4 Deliverables (Weeks 7–8):**
- [ ] Complete directory structure with all files and licenses
- [ ] Executive summary and methodology reports with search queries
- [ ] API endpoints for knowledge queries with ontology mapping
- [ ] Automated monitoring and update protocols
- [ ] Final link health and accessibility report

---

**Safety Prefix (apply to all outputs):**  
Educational information only, not medical advice; consult licensed professionals. Flag interventions with Very Low GRADE certainty and recommend professional oversight.
