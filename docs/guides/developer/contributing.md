---
title: Contributing Guide
description: Complete guide for contributing code, research data, and documentation to the ADHD Research Database
audience: developer
difficulty: beginner
---

# Contributing Guide

Thank you for your interest in contributing to the ADHD Research Database. This guide covers everything you need to know to make meaningful contributions to the project.

## Table of Contents

- [Development Environment Setup](#development-environment-setup)
- [Code Style and Conventions](#code-style-and-conventions)
- [Git Workflow](#git-workflow)
- [Pull Request Process](#pull-request-process)
- [Testing Requirements](#testing-requirements)
- [Research Data Contribution Guidelines](#research-data-contribution-guidelines)
- [Code Review Checklist](#code-review-checklist)
- [Release Process](#release-process)
- [Community Guidelines](#community-guidelines)

---

## Development Environment Setup

### Prerequisites

- Python 3.11 or higher
- Node.js 18 LTS or higher
- PostgreSQL 15+
- Git 2.30+

### Initial Setup

1. **Fork and clone the repository:**

```bash
# Fork via GitHub UI first, then:
git clone https://github.com/YOUR_USERNAME/adhd-research-database.git
cd adhd-research-database
git remote add upstream https://github.com/ORG/adhd-research-database.git
```

2. **Create a virtual environment:**

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
.\venv\Scripts\activate   # Windows
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
npm install
```

4. **Set up the database:**

```bash
# Create the database
createdb adhd_research_dev

# Copy environment template
cp .env.example .env
# Edit .env with your database credentials

# Initialize Prisma
npx prisma generate
npx prisma migrate dev
```

5. **Seed development data:**

```bash
python scripts/seed_dev_data.py
```

6. **Verify setup:**

```bash
flask run --debug
# Visit http://localhost:5000/health
```

---

## Code Style and Conventions

### Python (PEP 8)

We follow PEP 8 with the following specifics:

- **Line length:** 88 characters (Black default)
- **Formatter:** Black
- **Linter:** Ruff
- **Type hints:** Required for all public functions

```python
# Good
def calculate_effect_size(
    treatment_mean: float,
    control_mean: float,
    pooled_std: float,
) -> float:
    """Calculate Cohen's d effect size.

    Args:
        treatment_mean: Mean of the treatment group.
        control_mean: Mean of the control group.
        pooled_std: Pooled standard deviation.

    Returns:
        Cohen's d effect size value.
    """
    return (treatment_mean - control_mean) / pooled_std
```

**Run formatting and linting:**

```bash
black .
ruff check . --fix
mypy src/
```

### JavaScript

- **Formatter:** Prettier
- **Linter:** ESLint
- **Style:** Airbnb base configuration

```bash
npm run lint
npm run format
```

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Python files | snake_case | `evidence_processor.py` |
| Python classes | PascalCase | `ResearchStudy` |
| Python functions | snake_case | `get_study_by_doi()` |
| JavaScript files | camelCase | `searchHandler.js` |
| Database tables | snake_case | `research_studies` |
| API endpoints | kebab-case | `/api/v1/research-studies` |

---

## Git Workflow

### Branch Naming

Use descriptive branch names with type prefixes:

```
feature/add-meta-analysis-support
fix/doi-validation-error
docs/update-api-reference
refactor/evidence-level-enum
chore/update-dependencies
```

### Commit Messages

Follow Conventional Commits specification:

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**

```
feat(api): add endpoint for bulk study import

Implements POST /api/v1/studies/bulk with support for
JSON and CSV formats. Includes validation and duplicate
detection.

Closes #142

---

fix(search): correct relevance scoring for workplace queries

The TF-IDF weights were not being applied correctly for
workplace-related terms. This fix improves search accuracy
for HR and manager use cases.
```

### Keeping Your Fork Updated

```bash
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

---

## Pull Request Process

### Contribution Flow

```
+----------------+     +----------------+     +----------------+
|                |     |                |     |                |
|  Fork & Clone  +---->+  Create Branch +---->+  Make Changes  |
|                |     |                |     |                |
+----------------+     +----------------+     +-------+--------+
                                                      |
                                                      v
+----------------+     +----------------+     +----------------+
|                |     |                |     |                |
|    Merged!     +<----+  Code Review   +<----+   Open PR      |
|                |     |                |     |                |
+----------------+     +----------------+     +----------------+
        |                     ^
        |                     |
        v                     |
+----------------+     +------+--------+
|                |     |               |
|   Released     |     | Address       |
|                |     | Feedback      |
+----------------+     +---------------+
```

### Before Opening a PR

1. **Update your branch:**

```bash
git fetch upstream
git rebase upstream/main
```

2. **Run the full test suite:**

```bash
pytest
npm test
```

3. **Check code quality:**

```bash
black --check .
ruff check .
mypy src/
npm run lint
```

4. **Update documentation** if needed

### PR Template

When opening a PR, include:

```markdown
## Summary
Brief description of changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring
- [ ] Research data addition

## Testing
Describe how you tested these changes.

## Checklist
- [ ] Tests pass locally
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

### Review Timeline

- Initial review: Within 3 business days
- Follow-up reviews: Within 2 business days
- Merge after approval: Within 1 business day

---

## Testing Requirements

### Test Coverage

- Minimum coverage: 80%
- New features: Must include tests
- Bug fixes: Must include regression test

### Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=src --cov-report=html

# Specific test file
pytest tests/test_evidence_levels.py

# Run tests matching pattern
pytest -k "test_doi"

# JavaScript tests
npm test
```

### Test Structure

```
tests/
    conftest.py              # Shared fixtures
    test_api/
        test_studies.py      # API endpoint tests
        test_search.py
    test_models/
        test_research_study.py
    test_services/
        test_evidence_processor.py
    integration/
        test_full_workflow.py
```

### Writing Tests

```python
import pytest
from src.services.evidence_processor import calculate_evidence_level

class TestEvidenceLevel:
    """Tests for evidence level calculation."""

    def test_meta_analysis_is_level_1(self):
        """Meta-analyses should be classified as Level 1."""
        study = {"study_type": "meta-analysis", "sample_size": 5000}
        assert calculate_evidence_level(study) == 1

    def test_rct_is_level_2(self):
        """RCTs should be classified as Level 2."""
        study = {"study_type": "rct", "sample_size": 200}
        assert calculate_evidence_level(study) == 2

    @pytest.mark.parametrize("study_type,expected", [
        ("cohort", 3),
        ("case-control", 4),
        ("case-series", 5),
    ])
    def test_observational_studies(self, study_type, expected):
        """Observational studies should be classified correctly."""
        study = {"study_type": study_type, "sample_size": 100}
        assert calculate_evidence_level(study) == expected
```

---

## Research Data Contribution Guidelines

Contributing research data is one of the most valuable ways to help the project. Follow these guidelines to ensure data quality and consistency.

### Required Information

Every research entry **must** include:

| Field | Required | Description |
|-------|----------|-------------|
| DOI | Yes | Digital Object Identifier |
| Full Citation | Yes | APA 7th edition format |
| Evidence Level | Yes | 1-5 classification |
| Study Type | Yes | Meta-analysis, RCT, cohort, etc. |
| Sample Size | Yes | Total participants |
| Key Findings | Yes | Summary of main results |
| Workplace Relevance | Yes | Assessment score 1-5 |

### DOI and Citation Requirements

**Always include the DOI** for traceability and deduplication:

```yaml
doi: "10.1016/j.jad.2021.05.028"
citation: |
  Faraone, S. V., Banaschewski, T., Coghill, D., Zheng, Y.,
  Biederman, J., Bellgrove, M. A., ... & Wang, Y. (2021).
  The World Federation of ADHD International Consensus Statement:
  208 Evidence-based conclusions about the disorder.
  Neuroscience & Biobehavioral Reviews, 128, 789-818.
```

### Evidence Level Classification

Use the following hierarchy:

```
Level 1: Meta-analyses and systematic reviews
         - Multiple high-quality studies synthesized
         - Rigorous methodology assessment

Level 2: Randomized Controlled Trials (RCTs)
         - Random assignment to conditions
         - Controlled comparison groups

Level 3: Cohort studies
         - Prospective or retrospective
         - Comparison groups without randomization

Level 4: Case-control studies
         - Comparison of cases to controls
         - Retrospective design

Level 5: Case series, case reports, expert opinion
         - Descriptive studies
         - No control group
```

### Workplace Relevance Assessment

Rate the study's applicability to workplace contexts:

| Score | Meaning | Criteria |
|-------|---------|----------|
| 5 | Directly applicable | Study conducted in workplace setting |
| 4 | Highly relevant | Findings easily translate to work |
| 3 | Moderately relevant | Some workplace implications |
| 2 | Limited relevance | Primarily clinical focus |
| 1 | Minimal relevance | Basic research only |

### Effect Sizes

Include effect sizes when reported in the study:

```yaml
effect_sizes:
  - measure: "Cohen's d"
    value: 0.82
    ci_lower: 0.65
    ci_upper: 0.99
    interpretation: "Large effect"
  - measure: "Odds Ratio"
    value: 2.5
    ci_lower: 1.8
    ci_upper: 3.5
```

**Effect Size Interpretation (Cohen's d):**
- Small: 0.2
- Medium: 0.5
- Large: 0.8

### Data Submission Format

Submit research data as YAML files:

```yaml
# studies/faraone-2021-consensus.yaml
doi: "10.1016/j.jad.2021.05.028"
citation: "Faraone, S. V., et al. (2021). The World Federation..."
title: "World Federation of ADHD International Consensus Statement"
authors:
  - "Faraone, S. V."
  - "Banaschewski, T."
  - "Coghill, D."
year: 2021
journal: "Neuroscience & Biobehavioral Reviews"

study_type: "systematic_review"
evidence_level: 1
sample_size: null  # Review article
countries: ["International"]

key_findings:
  - "ADHD is a valid disorder with substantial genetic component"
  - "Effective treatments exist for all age groups"
  - "Workplace accommodations improve outcomes"

workplace_relevance: 4
workplace_notes: |
  Consensus includes several conclusions directly relevant to
  workplace accommodations and adult ADHD management.

effect_sizes: []  # Not applicable for consensus statement

tags:
  - "consensus"
  - "validity"
  - "treatment"
  - "adults"

contributor: "your-github-username"
date_added: "2024-01-15"
```

---

## Code Review Checklist

Reviewers use this checklist for all PRs:

### Functionality
- [ ] Code accomplishes the stated goal
- [ ] Edge cases are handled
- [ ] Error handling is appropriate
- [ ] No security vulnerabilities introduced

### Code Quality
- [ ] Follows project style guidelines
- [ ] No code duplication
- [ ] Functions are appropriately sized
- [ ] Variable names are descriptive

### Testing
- [ ] Tests cover new functionality
- [ ] Tests cover edge cases
- [ ] All tests pass
- [ ] Coverage meets minimum threshold

### Documentation
- [ ] Public APIs are documented
- [ ] Complex logic has comments
- [ ] README updated if needed
- [ ] CHANGELOG updated for features/fixes

### Research Data (if applicable)
- [ ] DOI is valid and resolves
- [ ] Citation is complete and accurate
- [ ] Evidence level is correctly classified
- [ ] Workplace relevance is justified
- [ ] Effect sizes are correctly reported

---

## Release Process

### Version Numbering

We follow Semantic Versioning (SemVer):

```
MAJOR.MINOR.PATCH

1.0.0 -> 1.0.1  (patch: bug fixes)
1.0.1 -> 1.1.0  (minor: new features, backward compatible)
1.1.0 -> 2.0.0  (major: breaking changes)
```

### Release Workflow

1. **Feature freeze** on release branch
2. **QA testing** in staging environment
3. **Changelog** finalized
4. **Version bump** in package files
5. **Tag** release in Git
6. **Deploy** to production
7. **Announce** in project channels

### Changelog Format

```markdown
## [1.2.0] - 2024-01-20

### Added
- Bulk import endpoint for research studies (#142)
- Evidence level filtering in search (#156)

### Changed
- Improved search relevance scoring (#158)

### Fixed
- DOI validation for older formats (#160)

### Research Data
- Added 15 new studies on workplace accommodations
```

---

## Community Guidelines

### Code of Conduct

We are committed to providing a welcoming and inclusive environment. All contributors must:

- Use welcoming and inclusive language
- Respect differing viewpoints and experiences
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy toward other community members

### Communication Channels

| Channel | Purpose |
|---------|---------|
| GitHub Issues | Bug reports, feature requests |
| GitHub Discussions | Questions, ideas, general discussion |
| Pull Requests | Code and data contributions |

### Getting Help

- **Documentation:** Start with our docs
- **Search issues:** Your question may be answered
- **Ask in Discussions:** For general questions
- **Open an issue:** For bugs or features

### Recognition

Contributors are recognized in:

- CONTRIBUTORS.md file
- Release notes for significant contributions
- Annual contributor spotlight

### First-Time Contributors

Look for issues labeled `good first issue` for accessible entry points. These are:

- Well-documented with clear requirements
- Limited in scope
- Good for learning the codebase

---

## Questions?

If you have questions about contributing:

1. Check the documentation
2. Search existing issues and discussions
3. Open a new discussion if needed

We appreciate your contributions to advancing ADHD research accessibility!

---

<div align="center">
<sub>
This documentation is part of the ADHD Research Database project.<br>
Licensed under MIT. Contributions welcome.
</sub>
</div>
