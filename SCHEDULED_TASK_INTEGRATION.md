# Scheduled Task Integration Guide

## Overview

This guide explains how to integrate the automation configuration into your existing scheduled ADHD research task so it can automatically push updates to GitHub without requiring user input.

## Current Scheduled Task

Your existing task runs weekly on Mondays at 9 AM and performs:
1. Research discovery and evaluation
2. Knowledge base updates
3. Framework regeneration
4. Database migration

## Integration Steps

### 1. Update the Scheduled Task Prompt

The scheduled task prompt should be enhanced to include explicit GitHub integration instructions:

```
Review the latest research on adult ADHD published in the last week, with a focus on professional men (25-55). Identify high-quality systematic reviews, meta-analyses, and RCTs. Extract key findings and update the knowledge base at /home/ubuntu/add_research_project/knowledge_base/knowledge_base.json with new entries, following the established JSON schema and quality standards. After updating, regenerate the assessment framework and treatment decision tree.

IMPORTANT: After completing all updates, automatically push changes to GitHub using the configuration in /home/ubuntu/add_research_project/AUTOMATION_CONFIG.md. Follow these specific steps:

1. READ the AUTOMATION_CONFIG.md file for complete repository details and workflow
2. Use the repository URL: https://github.com/vbonk/adhd-research-database.git
3. Create a feature branch named: research-update-YYYY-MM-DD
4. Commit ALL changes with the detailed commit message template provided
5. Push the branch and create a pull request
6. Use the GitHub PAT available in $GH_TOKEN environment variable
7. DO NOT ask for repository details - all information is in AUTOMATION_CONFIG.md

The automation configuration file contains all necessary details including:
- Repository URL and credentials
- Branch naming strategy
- Commit message templates
- File update workflow
- Error handling procedures
```

### 2. Key Integration Points

#### A. Configuration File Reference
The task should always start by reading the automation configuration:

```bash
# First step in any scheduled task
cd /home/ubuntu/add_research_project
cat AUTOMATION_CONFIG.md  # Read the full configuration
```

#### B. Git Setup Commands
Include these commands in the task workflow:

```bash
# Git configuration (from AUTOMATION_CONFIG.md)
git config user.name "ADHD Research Bot"
git config user.email "research-bot@adhddb.com"
git config credential.helper store
echo "https://vbonk:$GH_TOKEN@github.com" > ~/.git-credentials
```

#### C. Branch Creation Strategy
Use the standardized branch naming:

```bash
# Create feature branch
git checkout main
git pull origin main
BRANCH_NAME="research-update-$(date +%Y-%m-%d)"
git checkout -b $BRANCH_NAME
```

#### D. Commit and Push Workflow
Follow the established pattern:

```bash
# Stage all changes
git add knowledge_base/knowledge_base.json
git add frameworks/
git add README.md

# Use the commit message template from AUTOMATION_CONFIG.md
git commit -m "Weekly ADHD research update - $(date +%Y-%m-%d)
[Full template from config file]"

# Push and create PR
git push origin $BRANCH_NAME
gh pr create --title "Weekly ADHD Research Update - $(date +%Y-%m-%d)" --body "Automated update" --base main --head $BRANCH_NAME
```

### 3. Enhanced Task Instructions

#### Before Research Phase
```
1. Read /home/ubuntu/add_research_project/AUTOMATION_CONFIG.md completely
2. Set up git credentials using the provided commands
3. Ensure you're in the correct directory: /home/ubuntu/add_research_project
4. Verify GitHub PAT is available: echo $GH_TOKEN
```

#### After Research Updates
```
1. Follow the exact git workflow from AUTOMATION_CONFIG.md
2. Use the repository URL: https://github.com/vbonk/adhd-research-database.git
3. Create branch: research-update-YYYY-MM-DD
4. Commit with the provided template
5. Push and create PR automatically
6. Do NOT ask for any repository details or confirmation
```

#### Error Handling
```
If git operations fail:
1. Check the error handling section in AUTOMATION_CONFIG.md
2. Verify GitHub PAT is valid
3. Ensure repository permissions are correct
4. Retry with the provided troubleshooting steps
```

### 4. Updated Scheduled Task Configuration

Here's how the complete scheduled task should be configured:

```yaml
name: adhd_research_weekly_update_with_github
schedule: "0 0 9 * * 1"  # Monday 9 AM
repeat: true

prompt: |
  AUTOMATED ADHD RESEARCH UPDATE WITH GITHUB INTEGRATION
  
  CONFIGURATION: Read /home/ubuntu/add_research_project/AUTOMATION_CONFIG.md for ALL repository details, git commands, and workflow procedures. This file contains everything needed - do NOT ask for additional information.
  
  TASK: Review the latest research on adult ADHD published in the last week, with a focus on professional men (25-55). Identify high-quality systematic reviews, meta-analyses, and RCTs. Extract key findings and update the knowledge base at /home/ubuntu/add_research_project/knowledge_base/knowledge_base.json with new entries, following the established JSON schema and quality standards. After updating, regenerate the assessment framework and treatment decision tree.
  
  GITHUB INTEGRATION: After completing all research updates, automatically push changes to GitHub repository https://github.com/vbonk/adhd-research-database.git using the exact workflow specified in AUTOMATION_CONFIG.md:
  
  1. Setup git credentials (commands in config file)
  2. Create feature branch: research-update-YYYY-MM-DD  
  3. Stage and commit all changes with provided template
  4. Push branch and create pull request
  5. Use $GH_TOKEN for authentication
  
  IMPORTANT: All repository details, commands, and procedures are in AUTOMATION_CONFIG.md. Follow it exactly. Do NOT ask for repository URL, branch strategy, or commit messages - everything is pre-configured.

playbook: |
  Complete automation playbook with GitHub integration:
  
  Phase 1: Setup and Configuration
  - Read AUTOMATION_CONFIG.md for all procedures
  - Setup git credentials using provided commands
  - Verify GitHub PAT availability
  
  Phase 2: Research Discovery
  - Search for latest ADHD research (last 7 days)
  - Focus on evidence levels 1A-2B
  - Target professional men aged 25-55
  
  Phase 3: Knowledge Base Updates
  - Update knowledge_base.json with new entries
  - Follow established JSON schema
  - Validate all required fields
  
  Phase 4: Framework Regeneration
  - Run generate_framework.py
  - Run generate_decision_tree.py
  - Render decision tree diagram
  
  Phase 5: Database Migration
  - Execute migrate_data.js
  - Verify database integrity
  
  Phase 6: GitHub Integration
  - Follow exact git workflow from AUTOMATION_CONFIG.md
  - Create feature branch with date
  - Commit with detailed message template
  - Push and create pull request
  - Handle any git errors per config procedures
```

### 5. Verification Steps

To ensure the integration works correctly:

#### Test the Configuration
```bash
cd /home/ubuntu/add_research_project
python scripts/update_research_with_git.py
```

#### Verify Environment Variables
```bash
echo $GH_TOKEN  # Should show the GitHub PAT
```

#### Check Repository Access
```bash
gh repo view vbonk/adhd-research-database
```

### 6. Troubleshooting Common Issues

#### Issue: "Repository details needed"
**Solution:** The task should read AUTOMATION_CONFIG.md first and use those details

#### Issue: "Git authentication failed"  
**Solution:** Verify $GH_TOKEN is set and use the credential setup commands from config

#### Issue: "Branch already exists"
**Solution:** Use date-based branch names as specified in config

#### Issue: "No changes to commit"
**Solution:** This is normal if no new research is found - create informational commit

### 7. Success Indicators

The scheduled task is properly integrated when:
- ✅ It reads AUTOMATION_CONFIG.md automatically
- ✅ It uses the correct repository URL without asking
- ✅ It creates properly named feature branches
- ✅ It commits with the detailed message template
- ✅ It pushes and creates PRs automatically
- ✅ It handles errors according to the config procedures

### 8. Monitoring and Maintenance

#### Weekly Verification
- Check that PRs are being created automatically
- Verify commit messages follow the template
- Ensure branch naming is consistent

#### Monthly Review
- Review automation success rate
- Update configuration if needed
- Check for any recurring errors

This integration ensures your scheduled task operates completely autonomously while maintaining proper version control and documentation standards.

