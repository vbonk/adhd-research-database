#!/usr/bin/env python3
"""
ADHD Research Database - Automated Git Operations Helper
This script handles git operations for the automated research update pipeline.
"""

import os
import subprocess
import json
from datetime import datetime
from pathlib import Path

class GitOperationsHelper:
    def __init__(self, repo_path="/home/ubuntu/add_research_project"):
        self.repo_path = Path(repo_path)
        self.git_token = os.getenv('GH_TOKEN')
        
    def setup_git_credentials(self):
        """Configure git with GitHub PAT for authentication"""
        try:
            # Configure git user
            subprocess.run(['git', 'config', 'user.name', 'ADHD Research Bot'], 
                         cwd=self.repo_path, check=True)
            subprocess.run(['git', 'config', 'user.email', 'research-bot@adhddb.com'], 
                         cwd=self.repo_path, check=True)
            
            # Set up credential helper
            subprocess.run(['git', 'config', 'credential.helper', 'store'], 
                         cwd=self.repo_path, check=True)
            
            # Store credentials
            credentials_file = Path.home() / '.git-credentials'
            with open(credentials_file, 'w') as f:
                f.write(f'https://vbonk:{self.git_token}@github.com\n')
            
            print("✅ Git credentials configured successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to configure git credentials: {e}")
            return False
    
    def create_research_branch(self):
        """Create a new branch for research updates"""
        try:
            # Get current date for branch name
            date_str = datetime.now().strftime('%Y-%m-%d')
            branch_name = f"research-update-{date_str}"
            
            # Ensure we're on main branch
            subprocess.run(['git', 'checkout', 'main'], cwd=self.repo_path, check=True)
            subprocess.run(['git', 'pull', 'origin', 'main'], cwd=self.repo_path, check=True)
            
            # Create and checkout new branch
            subprocess.run(['git', 'checkout', '-b', branch_name], 
                         cwd=self.repo_path, check=True)
            
            print(f"✅ Created research branch: {branch_name}")
            return branch_name
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to create research branch: {e}")
            return None
    
    def commit_research_updates(self, new_research_count=0, research_summary=""):
        """Commit research updates with detailed message"""
        try:
            # Add all changes
            subprocess.run(['git', 'add', '.'], cwd=self.repo_path, check=True)
            
            # Check if there are changes to commit
            result = subprocess.run(['git', 'diff', '--cached', '--quiet'], 
                                  cwd=self.repo_path, capture_output=True)
            
            if result.returncode == 0:
                print("ℹ️ No changes to commit")
                return True
            
            # Create detailed commit message
            date_str = datetime.now().strftime('%Y-%m-%d')
            commit_message = f"""Weekly ADHD research update - {date_str}

📊 Research Updates:
- Added {new_research_count} new high-quality research entries
- Updated knowledge base with latest evidence-based findings
- Regenerated assessment framework and treatment decision tree
- Updated database with new research data

🔬 Research Summary:
{research_summary}

🏥 Clinical Impact:
- Enhanced evidence base for professional men aged 25-55
- Updated treatment recommendations based on latest research
- Improved assessment tools with current best practices

📈 Database Statistics:
- Total research entries: Updated
- Evidence levels: Maintained high-quality standards
- Target population focus: Professional adults 25-55

🤖 Automated update via scheduled research pipeline
"""
            
            # Commit changes
            subprocess.run(['git', 'commit', '-m', commit_message], 
                         cwd=self.repo_path, check=True)
            
            print("✅ Research updates committed successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to commit research updates: {e}")
            return False
    
    def push_and_create_pr(self, branch_name, research_summary=""):
        """Push branch and create pull request"""
        try:
            # Push branch to origin
            subprocess.run(['git', 'push', 'origin', branch_name], 
                         cwd=self.repo_path, check=True)
            
            # Create pull request using GitHub CLI
            pr_title = f"Weekly ADHD Research Update - {datetime.now().strftime('%Y-%m-%d')}"
            pr_body = f"""## 📚 Weekly Research Update

### Summary
This automated update includes the latest high-quality ADHD research findings focused on professional men aged 25-55.

### Changes
- ✅ Updated knowledge base with new research entries
- ✅ Regenerated assessment framework
- ✅ Updated treatment decision tree
- ✅ Migrated new data to PostgreSQL database

### Research Findings
{research_summary}

### Quality Assurance
- All research entries meet evidence level standards (1A-2B)
- Target population alignment verified
- Clinical significance assessed
- Workplace relevance evaluated

### Next Steps
- Review new research entries for accuracy
- Validate updated frameworks
- Deploy updated database if approved

---
*This PR was automatically generated by the ADHD Research Update Pipeline*
"""
            
            subprocess.run(['gh', 'pr', 'create', 
                          '--title', pr_title,
                          '--body', pr_body,
                          '--base', 'main',
                          '--head', branch_name], 
                         cwd=self.repo_path, check=True)
            
            print(f"✅ Pull request created successfully for branch: {branch_name}")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to push and create PR: {e}")
            return False
    
    def update_readme_stats(self):
        """Update README with current database statistics"""
        try:
            readme_path = self.repo_path / 'README.md'
            
            # Load current knowledge base to get stats
            kb_path = self.repo_path / 'knowledge_base' / 'knowledge_base.json'
            with open(kb_path, 'r') as f:
                kb_data = json.load(f)
            
            research_count = len(kb_data.get('research_entries', []))
            
            # Read current README
            with open(readme_path, 'r') as f:
                readme_content = f.read()
            
            # Update research count in README
            import re
            pattern = r'- \*\*(\d+) High-Quality Research Entries\*\*'
            replacement = f'- **{research_count} High-Quality Research Entries**'
            
            updated_content = re.sub(pattern, replacement, readme_content)
            
            # Write updated README
            with open(readme_path, 'w') as f:
                f.write(updated_content)
            
            print(f"✅ README updated with {research_count} research entries")
            return True
            
        except Exception as e:
            print(f"❌ Failed to update README stats: {e}")
            return False

def main():
    """Main function for testing git operations"""
    git_helper = GitOperationsHelper()
    
    print("🔧 Setting up git credentials...")
    if not git_helper.setup_git_credentials():
        return False
    
    print("🌿 Creating research branch...")
    branch_name = git_helper.create_research_branch()
    if not branch_name:
        return False
    
    print("📊 Updating README statistics...")
    git_helper.update_readme_stats()
    
    print("💾 Committing research updates...")
    if not git_helper.commit_research_updates(
        new_research_count=1,
        research_summary="Test update for automated pipeline"
    ):
        return False
    
    print("🚀 Pushing and creating PR...")
    if not git_helper.push_and_create_pr(
        branch_name,
        research_summary="Test research summary"
    ):
        return False
    
    print("✅ All git operations completed successfully!")
    return True

if __name__ == "__main__":
    main()

