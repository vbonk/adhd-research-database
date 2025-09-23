# THE ULTIMATE ADD/ADHD RESEARCH PROMPT v4.0 — Package

**Version:** v4.0  
**Date:** 2025-09-12

This package contains copy‑ready prompts (System + User) and supporting schemas/templates to kick off a rigorous, auditable ADD/ADHD research program.

## Contents
- `SYSTEM_PROMPT.md` — Paste into your model’s **System** field.
- `USER_PROMPT.md` — Paste into your model’s **User** field to initiate execution.
- `schemas/knowledge_entry.schema.json` — JSON Schema for Knowledge Entries (strict).
- `schemas/sentiment_record.schema.json` — JSON Schema for Social Sentiment Records (strict).
- `templates/intervention_matrix_header.csv` — Canonical CSV header for the Intervention Matrix.
- `templates/PRISMA_Template.md` — Clean PRISMA logging template with sections ready to fill.
- `templates/Search_Plan_Template.md` — Structured outline for ontology-aware search plans.
- `templates/Quality_Gates_Checklist.md` — Checklist to operationalize quality gates.
- `templates/monitoring_config.py` — Drop‑in configuration object for real-time monitoring.

## How to Use
1. Open your research assistant environment (e.g., a Custom GPT or agent framework).
2. Copy the entire contents of `SYSTEM_PROMPT.md` into the **System** prompt.
3. Copy the entire contents of `USER_PROMPT.md` into the **User** prompt and run.
4. Store all generated artifacts under a project root similar to `/ADD_RESEARCH_PROJECT/` as referenced in the prompt.
5. Enforce **no hidden chain-of-thought**; only expose the process artifacts the prompt specifies (Search Logs, Evidence Tables, Conflict Notes).

## Notes
- All schemas are strict and designed for downstream validation.
- The package does not include a license. Apply your preferred license policy at the repository level.
