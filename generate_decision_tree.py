import json

# Load the updated knowledge base
with open("/home/ubuntu/add_research_project/knowledge_base/knowledge_base.json", "r") as f:
    kb = json.load(f)

# Generate the treatment decision tree
treatment_decision_tree = """
# Adult ADHD Treatment Decision Tree for Professional Men (25-55)

This decision tree provides a evidence-based pathway for selecting treatments for professional men with ADHD, based on the latest research.

```mermaid
graph TD
    A[Start: Diagnosis of Adult ADHD] --> B{Comorbidities?};
    B -->|Yes| C[Treat Comorbidities First or Concurrently];
    B -->|No| D{Patient Preference?};
    C --> D;
    D -->|Pharmacotherapy| E[First-Line: Stimulants];
    D -->|Psychotherapy| F[First-Line: CBT];
    E --> G{Response to Stimulants?};
    G -->|Good| H[Continue Stimulants & Monitor];
    G -->|Partial or Poor| I[Second-Line: Atomoxetine];
    I --> J{Response to Atomoxetine?};
    J -->|Good| K[Continue Atomoxetine & Monitor];
    J -->|Partial or Poor| L[Consider Adjunctive CBT];
    F --> M{Response to CBT?};
    M -->|Good| N[Continue CBT & Monitor];
    M -->|Partial or Poor| O[Consider Adjunctive Pharmacotherapy];
    H --> P[Workplace Stress Management];
    K --> P;
    L --> P;
    N --> P;
    O --> P;
    P --> Q[Web-Based CBT for Stress & Exhaustion];
    Q --> R[Monitor Quality of Life and Workplace Functioning];
```

## Treatment Principles

*   **Shared Decision-Making:** Treatment decisions should be made in collaboration with the patient, considering their preferences, values, and goals.
*   **Multimodal Approach:** A combination of medication and psychotherapy is often the most effective approach.
*   **Workplace Focus:** Treatment should address the specific challenges faced by professional men in the workplace, such as stress, burnout, and executive function deficits.
*   **Regular Monitoring:** Treatment progress should be regularly monitored using validated rating scales and measures of workplace functioning.

"""

with open("/home/ubuntu/add_research_project/frameworks/treatment_decision_tree.md", "w") as f:
    f.write(treatment_decision_tree)

print("Treatment decision tree generated successfully!")


