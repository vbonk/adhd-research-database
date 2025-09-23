# Real-Time Monitoring Configuration (drop-in)
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
