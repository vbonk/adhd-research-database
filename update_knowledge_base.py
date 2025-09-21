import json
from datetime import datetime

# Load existing knowledge base
with open('/home/ubuntu/add_research_project/knowledge_base/knowledge_base.json', 'r') as f:
    kb = json.load(f)

# New research entries based on our findings
new_entries = [
    {
        "id": "lancet_2025_ostinelli_network_meta",
        "title": "Comparative efficacy and acceptability of pharmacological, psychological, and neurostimulatory interventions for ADHD in adults: a systematic review and component network meta-analysis",
        "authors": ["Edoardo G Ostinelli", "Marcel Schulze", "Caroline Zangani", "Luis C Farhat", "Anneka Tomlinson", "Cinzia Del Giovane"],
        "journal": "The Lancet Psychiatry",
        "publication_date": "2025-01-01",
        "doi": "10.1016/S2215-0366(24)00360-2",
        "study_type": "systematic_review",
        "evidence_level": "1a",
        "sample_size": 14887,
        "target_population": {
            "age_range": "≥18 years",
            "gender": "51.3% male, 45.6% female",
            "occupation": "Mixed adult population",
            "adhd_subtype": "All subtypes"
        },
        "methodology": {
            "design": "Systematic review and component network meta-analysis",
            "duration": "≥1 week for medications, ≥4 sessions for psychological therapies",
            "primary_outcomes": ["ADHD core symptom severity", "All-cause discontinuation"],
            "secondary_outcomes": ["Quality of life measures", "Functional outcomes"]
        },
        "key_findings": {
            "primary_results": "Stimulants and atomoxetine were the only interventions with evidence of beneficial effects on both self-reported and clinician-reported ADHD symptoms. Non-pharmacological interventions showed inconsistent effects across different raters.",
            "effect_sizes": {
                "stimulants_self_reported": -0.39,
                "stimulants_clinician_reported": -0.61,
                "atomoxetine_self_reported": -0.38,
                "atomoxetine_clinician_reported": -0.51,
                "cbt_clinician_reported": -0.76
            },
            "clinical_significance": "Stimulants and atomoxetine represent first-line pharmacological treatments with consistent efficacy across rating scales",
            "limitations": ["Short-term focus", "Limited quality of life data", "Inconsistent non-pharmacological effects"]
        },
        "workplace_relevance": {
            "productivity_impact": "Short-term efficacy data applicable to working adults requiring rapid symptom improvement",
            "accommodation_needs": ["Medication adherence support", "Flexible scheduling for therapy"],
            "career_implications": "Acceptability concerns with atomoxetine may affect long-term treatment adherence"
        },
        "quality_assessment": {
            "risk_of_bias": "low",
            "grade_rating": "moderate",
            "reviewer_notes": "Comprehensive methodology with component network meta-analysis approach"
        },
        "clinical_applications": {
            "diagnostic_utility": "Supports evidence-based treatment selection for adult ADHD",
            "treatment_recommendations": ["Stimulants as first-line", "Atomoxetine as alternative", "CBT as adjunctive therapy"],
            "monitoring_parameters": ["Symptom severity scales", "Discontinuation rates", "Functional outcomes"]
        },
        "tags": ["systematic_review", "network_meta_analysis", "pharmacological", "non_pharmacological", "adult_adhd", "treatment_efficacy"],
        "added_date": "2025-09-15",
        "last_reviewed": "2025-09-15"
    },
    {
        "id": "frontiers_2025_yang_nonpharmaco_network",
        "title": "Short-term and long-term effect of non-pharmacotherapy for adults with ADHD: a systematic review and network meta-analysis",
        "authors": ["Xinyue Yang", "Lin Zhang", "Jing Yu", "Meng Wang"],
        "journal": "Frontiers in Psychiatry",
        "publication_date": "2025-01-31",
        "doi": "10.3389/fpsyt.2025.1516878",
        "study_type": "systematic_review",
        "evidence_level": "1a",
        "sample_size": 2289,
        "target_population": {
            "age_range": "Adults",
            "gender": "Mixed",
            "occupation": "General adult population",
            "adhd_subtype": "All subtypes"
        },
        "methodology": {
            "design": "Systematic review and network meta-analysis",
            "duration": "Short-term and long-term follow-up",
            "primary_outcomes": ["Core ADHD symptoms", "Depression", "Anxiety"],
            "secondary_outcomes": ["Functional outcomes", "Quality of life"]
        },
        "key_findings": {
            "primary_results": "CBT showed exceptionally large effect sizes for both short-term and long-term improvement in core ADHD symptoms, depression, and anxiety. Mindfulness-based cognitive therapy recommended for patients without comorbidities.",
            "effect_sizes": {
                "cbt_adhd_short_term": -4.43,
                "cbt_adhd_long_term": -3.61,
                "cbt_depression_short_term": -4.16,
                "cbt_depression_long_term": -3.89,
                "cbt_anxiety_short_term": -2.12,
                "cbt_anxiety_long_term": -7.25
            },
            "clinical_significance": "CBT demonstrates very large and sustained effects on ADHD symptoms and comorbid emotional disorders",
            "limitations": ["High risk of bias in 48.6% of studies", "Very low to low confidence in most treatment effects"]
        },
        "workplace_relevance": {
            "productivity_impact": "Long-term CBT effects particularly valuable for sustained workplace functioning",
            "accommodation_needs": ["Structured CBT program access", "Time for therapy sessions"],
            "career_implications": "Emotional regulation improvements critical for professional advancement"
        },
        "quality_assessment": {
            "risk_of_bias": "moderate",
            "grade_rating": "low",
            "reviewer_notes": "Large effect sizes but quality concerns in underlying studies"
        },
        "clinical_applications": {
            "diagnostic_utility": "Supports CBT as primary non-pharmacological intervention",
            "treatment_recommendations": ["CBT for comprehensive symptom management", "Mindfulness-based therapy for uncomplicated cases"],
            "monitoring_parameters": ["ADHD symptom scales", "Depression and anxiety measures", "Long-term functional outcomes"]
        },
        "tags": ["systematic_review", "network_meta_analysis", "non_pharmacological", "cbt", "mindfulness", "long_term_outcomes"],
        "added_date": "2025-09-15",
        "last_reviewed": "2025-09-15"
    },
    {
        "id": "jmir_2025_oscarsson_workplace_stress",
        "title": "Web-Based Stress Management for Working Adults With Attention-Deficit/Hyperactivity Disorder (ADHD): Single-Arm, Open Pilot Trial",
        "authors": ["Martin Oscarsson", "Sandra Hammarbäck", "Karolina Blom Wiberg", "Alexander Rozental", "Ylva Ginsberg", "Per Carlbring", "Gerhard Andersson", "Fredrik Jönsson"],
        "journal": "JMIR Formative Research",
        "publication_date": "2025-05-29",
        "doi": "10.2196/66388",
        "study_type": "rct",
        "evidence_level": "2b",
        "sample_size": 36,
        "target_population": {
            "age_range": "Working adults",
            "gender": "Mixed working adults",
            "occupation": "Professional working adults",
            "adhd_subtype": "All subtypes"
        },
        "methodology": {
            "design": "Single-arm open pilot trial",
            "duration": "12-week intervention with 12-week follow-up",
            "primary_outcomes": ["Quality of life (AAQoL)", "Perceived stress", "Exhaustion"],
            "secondary_outcomes": ["ADHD symptoms", "Anxiety", "Depression"]
        },
        "key_findings": {
            "primary_results": "Web-based CBT intervention produced large to very large effect sizes across all measured domains with high adherence and no dropouts. 36% of participants showed clinically significant improvement in quality of life.",
            "effect_sizes": {
                "quality_of_life": 0.84,
                "adhd_symptoms": 0.98,
                "perceived_stress": 0.83,
                "exhaustion": 1.12,
                "anxiety": 1.70,
                "depression": 1.25
            },
            "clinical_significance": "Demonstrates feasibility and effectiveness of workplace-focused ADHD interventions",
            "limitations": ["Single-arm design", "Small sample size", "Pilot study requiring replication"]
        },
        "workplace_relevance": {
            "productivity_impact": "Very large effect on exhaustion and stress directly relevant to workplace performance",
            "accommodation_needs": ["Web-based platform access", "Flexible scheduling for modules"],
            "career_implications": "Comprehensive improvement in professional functioning and stress management"
        },
        "quality_assessment": {
            "risk_of_bias": "moderate",
            "grade_rating": "moderate",
            "reviewer_notes": "Pilot study with promising results but limited by single-arm design"
        },
        "clinical_applications": {
            "diagnostic_utility": "Supports workplace-focused intervention approaches",
            "treatment_recommendations": ["Web-based CBT for working adults", "Stress management focus", "Executive function training"],
            "monitoring_parameters": ["Quality of life measures", "Workplace stress indicators", "ADHD symptom severity"]
        },
        "tags": ["pilot_study", "workplace_intervention", "web_based", "cbt", "stress_management", "working_adults", "professional_men"],
        "added_date": "2025-09-15",
        "last_reviewed": "2025-09-15"
    }
]

# Add new entries to knowledge base
kb["research_entries"].extend(new_entries)

# Update metadata
kb["metadata"]["last_updated"] = "2025-09-15"
kb["metadata"]["version"] = "1.1"

# Save updated knowledge base
with open('/home/ubuntu/add_research_project/knowledge_base/knowledge_base.json', 'w') as f:
    json.dump(kb, f, indent=2)

print("Knowledge base updated successfully!")
print(f"Total research entries: {len(kb['research_entries'])}")
