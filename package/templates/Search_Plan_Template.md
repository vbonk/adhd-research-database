# Search Plan — Ontology-Aware

## Databases
PubMed, PsycINFO, Cochrane, Scopus, Google Scholar, PROSPERO

## Date Range
2020-01-01 to 2025-12-31

## Core Boolean (example)
("ADHD"[MeSH] OR "Attention Deficit Disorder with Hyperactivity"[MeSH] OR 
 "attention-deficit/hyperactivity disorder"[tiab] OR "attention deficit disorder"[tiab] OR 
 "inattentive type"[tiab] OR "ADD"[tiab])
AND (treatment[majr] OR management[majr] OR diagnosis[majr] OR epidemiology[majr])
AND (English[lang])
NOT ("case reports"[pt] OR "editorial"[pt])

## Ontology & Codes
- MeSH: ADHD
- ICD-11: 6A05
- DSM-5-TR: 314.xx
- SNOMED CT: 192127007 (example)
- UMLS CUIs: C0001973 (example)

## Inclusion/Exclusion
- Include: SR/MA, RCTs, large cohorts, guidelines; sample size thresholds as specified
- Exclude: Case reports, editorials, non-retrievable sources

## PRISMA Logging
Use `templates/PRISMA_Template.md` and capture decision rationales.

## Link Validation
DOI → PMID → archival URL fallback (e.g., perma.cc, web.archive.org)
