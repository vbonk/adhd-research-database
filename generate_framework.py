import json

# Load the updated knowledge base
with open("/home/ubuntu/add_research_project/knowledge_base/knowledge_base.json", "r") as f:
    kb = json.load(f)

# Generate the assessment framework
assessment_framework = """
# Adult ADHD Assessment Framework for Professional Men (25-55)

This framework provides a structured approach to assessing adult ADHD in professional men, incorporating the latest research findings.

## I. Initial Screening

*   **Purpose:** To identify individuals who may be at risk for ADHD.
*   **Tools:**
    *   **Adult ADHD Self-Report Scale (ASRS):** A brief, validated screening tool for adult ADHD.
    *   **Workplace Performance Review:** Review of performance evaluations for patterns consistent with ADHD (e.g., missed deadlines, inconsistent performance).

## II. Comprehensive Diagnostic Evaluation

*   **Purpose:** To establish a formal diagnosis of ADHD and rule out other conditions.
*   **Components:**
    *   **Clinical Interview:** A detailed interview covering developmental history, academic and occupational functioning, and ADHD symptoms in childhood and adulthood.
    *   **DSM-5 Criteria:** Assessment of symptoms against the Diagnostic and Statistical Manual of Mental Disorders, 5th Edition (DSM-5) criteria for ADHD.
    *   **Rating Scales:**
        *   **Conners' Adult ADHD Rating Scales (CAARS):** A comprehensive rating scale for assessing ADHD symptoms and their impact on functioning.
        *   **Brown Attention-Deficit Disorder Symptom Assessment Scale (BADDS):** Focuses on executive function impairments.
    *   **Collateral Information:** Information from a spouse, partner, or close family member about the individual's symptoms and functioning.

## III. Workplace-Specific Assessment

*   **Purpose:** To evaluate the impact of ADHD on workplace functioning and identify specific areas of difficulty.
*   **Components:**
    *   **Workplace Stress and Burnout:**
        *   **Perceived Stress Scale (PSS-10):** To measure perceived stress levels.
        *   **Karolinska Exhaustion Disorder Scale (KEDS):** To assess workplace burnout.
    *   **Executive Functioning:**
        *   **Behavior Rating Inventory of Executive Function - Adult Form (BRIEF-A):** To assess executive function skills in a real-world context.
    *   **Quality of Life:**
        *   **Adult ADHD Quality of Life Scale (AAQoL):** To measure the impact of ADHD on overall quality of life.

## IV. Comorbidity Assessment

*   **Purpose:** To identify co-occurring mental health conditions that may affect treatment and functioning.
*   **Common Comorbidities:**
    *   **Anxiety Disorders:** (GAD-7)
    *   **Depressive Disorders:** (PHQ-9)
    *   **Substance Use Disorders:**

"""

with open("/home/ubuntu/add_research_project/frameworks/assessment_framework.md", "w") as f:
    f.write(assessment_framework)

print("Assessment framework generated successfully!")


