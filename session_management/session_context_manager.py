#!/usr/bin/env python3
"""
Session Context Management Agent for ADD Professional Research & Application Development Project

This agent maintains comprehensive session state, tracks progress across phases,
and ensures seamless migration between chat sessions when context limits are reached.

Author: Manus AI Agent
Created: 2025-09-12
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class TaskProgress:
    """Represents progress on a specific task or subtask"""
    task_id: str
    description: str
    status: str  # "not_started", "in_progress", "completed", "blocked"
    progress_percentage: float
    last_updated: str
    notes: str = ""
    dependencies: List[str] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []

@dataclass
class PhaseStatus:
    """Represents the status of a project phase"""
    phase_id: int
    title: str
    status: str  # "not_started", "in_progress", "completed"
    progress_percentage: float
    tasks: List[TaskProgress]
    start_date: Optional[str] = None
    completion_date: Optional[str] = None
    required_capabilities: Dict[str, bool] = None
    
    def __post_init__(self):
        if self.required_capabilities is None:
            self.required_capabilities = {}

@dataclass
class SessionContext:
    """Complete session context for the ADD research project"""
    project_name: str
    project_goal: str
    current_phase_id: int
    session_start_time: str
    last_updated: str
    phases: List[PhaseStatus]
    key_files: Dict[str, str]  # filename -> description
    knowledge_base_stats: Dict[str, Any]
    next_actions: List[str]
    technical_notes: List[str]
    user_requirements: List[str]
    quality_targets: Dict[str, str]
    migration_instructions: str

class SessionContextManager:
    """Manages session context, progress tracking, and migration support"""
    
    def __init__(self, project_dir: str = "/home/ubuntu/add_research_project"):
        self.project_dir = Path(project_dir)
        self.context_file = self.project_dir / "session_context.json"
        self.context: Optional[SessionContext] = None
        self.load_context()
    
    def initialize_context(self) -> SessionContext:
        """Initialize a new session context"""
        phases = [
            PhaseStatus(
                phase_id=1,
                title="Package Analysis and Research Setup",
                status="completed",
                progress_percentage=100.0,
                tasks=[
                    TaskProgress("1.1", "Examine package files and methodology", "completed", 100.0, "2025-09-12"),
                    TaskProgress("1.2", "Review JSON schemas and data structures", "completed", 100.0, "2025-09-12"),
                    TaskProgress("1.3", "Set up project directory structure", "completed", 100.0, "2025-09-12"),
                ]
            ),
            PhaseStatus(
                phase_id=2,
                title="Systematic Literature Search and Evidence Collection",
                status="completed",
                progress_percentage=100.0,
                tasks=[
                    TaskProgress("2.1", "Execute comprehensive search strategy", "completed", 100.0, "2025-09-12"),
                    TaskProgress("2.2", "Collect systematic reviews and meta-analyses", "completed", 100.0, "2025-09-12"),
                    TaskProgress("2.3", "Document search methodology using PRISMA", "completed", 100.0, "2025-09-12"),
                ],
                required_capabilities={"deep_research": True, "search_use": True}
            ),
            PhaseStatus(
                phase_id=3,
                title="Knowledge Base Development and Data Structuring",
                status="in_progress",
                progress_percentage=29.7,  # 89/300 entries
                tasks=[
                    TaskProgress("3.1", "Extract and structure research findings (89/300+)", "in_progress", 29.7, "2025-09-12", 
                               "Completed 2 batches of parallel processing, 89 valid entries extracted"),
                    TaskProgress("3.2", "Apply strict JSON schema compliance", "in_progress", 90.0, "2025-09-12"),
                    TaskProgress("3.3", "Focus on 5 key domains", "in_progress", 80.0, "2025-09-12"),
                    TaskProgress("3.4", "Ensure 90%+ avatar relevance", "in_progress", 85.0, "2025-09-12"),
                    TaskProgress("3.5", "Maintain 70%+ high-quality evidence", "in_progress", 85.0, "2025-09-12"),
                ],
                required_capabilities={"data_analysis": True, "parallel_processing": True}
            ),
            PhaseStatus(
                phase_id=4,
                title="Assessment Framework and Treatment Decision Tree Creation",
                status="not_started",
                progress_percentage=0.0,
                tasks=[
                    TaskProgress("4.1", "Develop self-assessment tools", "not_started", 0.0, "2025-09-12"),
                    TaskProgress("4.2", "Create workplace impact assessment", "not_started", 0.0, "2025-09-12"),
                    TaskProgress("4.3", "Build evidence-based decision trees", "not_started", 0.0, "2025-09-12"),
                ],
                required_capabilities={"data_analysis": True}
            ),
            PhaseStatus(
                phase_id=5,
                title="Web Application Architecture and Development",
                status="not_started",
                progress_percentage=0.0,
                tasks=[
                    TaskProgress("5.1", "Set up React application structure", "not_started", 0.0, "2025-09-12"),
                    TaskProgress("5.2", "Implement core components", "not_started", 0.0, "2025-09-12"),
                    TaskProgress("5.3", "Develop scoring algorithms", "not_started", 0.0, "2025-09-12"),
                ],
                required_capabilities={"frontend_development": True, "web_design": True}
            ),
            PhaseStatus(
                phase_id=6,
                title="Application Integration and Testing",
                status="not_started",
                progress_percentage=0.0,
                tasks=[
                    TaskProgress("6.1", "Test application functionality", "not_started", 0.0, "2025-09-12"),
                    TaskProgress("6.2", "Ensure responsive design", "not_started", 0.0, "2025-09-12"),
                ],
                required_capabilities={"browser_use": True, "frontend_development": True}
            ),
            PhaseStatus(
                phase_id=7,
                title="Deployment and Documentation",
                status="not_started",
                progress_percentage=0.0,
                tasks=[
                    TaskProgress("7.1", "Deploy application to public URL", "not_started", 0.0, "2025-09-12"),
                    TaskProgress("7.2", "Create user documentation", "not_started", 0.0, "2025-09-12"),
                ],
                required_capabilities={"document_generation": True, "frontend_development": True}
            ),
            PhaseStatus(
                phase_id=8,
                title="Final Delivery and User Guidance",
                status="not_started",
                progress_percentage=0.0,
                tasks=[
                    TaskProgress("8.1", "Present completed application", "not_started", 0.0, "2025-09-12"),
                    TaskProgress("8.2", "Provide comprehensive documentation", "not_started", 0.0, "2025-09-12"),
                ]
            )
        ]
        
        context = SessionContext(
            project_name="ADD Professional Research & Application Development",
            project_goal="Complete comprehensive knowledge base of 300+ research findings and develop web application for professional adult males with ADHD",
            current_phase_id=3,
            session_start_time=datetime.now().isoformat(),
            last_updated=datetime.now().isoformat(),
            phases=phases,
            key_files={
                "/home/ubuntu/todo.md": "Project task tracker and progress overview",
                "/home/ubuntu/add_research_project/knowledge_base/knowledge_base.json": "Main knowledge base with research findings",
                "/home/ubuntu/add_research_project/research/search_results_phase1.md": "Systematic literature search results",
                "/home/ubuntu/add_research_project/research/PRISMA_documentation.md": "PRISMA methodology documentation",
                "/home/ubuntu/add_research_project/documentation/research_methodology.md": "Research methodology documentation",
                "/home/ubuntu/add_research_project/package/": "Original research package and templates",
                "/home/ubuntu/extract_adhd_research_findings.json": "Batch 1 parallel processing results",
                "/home/ubuntu/extract_adhd_research_findings_batch2.json": "Batch 2 parallel processing results"
            },
            knowledge_base_stats={
                "total_entries": 89,
                "target_entries": 300,
                "completion_percentage": 29.7,
                "domains_covered": ["Workplace & Career Impact", "Treatments", "Clinical", "Management", "Foundational"],
                "last_batch_processed": 2,
                "valid_entries_batch1": 42,
                "valid_entries_batch2": 42,
                "initial_entries": 5
            },
            next_actions=[
                "Continue parallel processing of research topics to reach 300+ knowledge base entries",
                "Process remaining research topics from the comprehensive list",
                "Validate knowledge base entries for schema compliance and quality",
                "Begin Phase 4: Assessment Framework development once knowledge base is complete"
            ],
            technical_notes=[
                "Using parallel processing with agent_map_subtasks for efficient knowledge extraction",
                "JSON schema compliance maintained across all entries",
                "Focus on professional adult males (25-55) with ADHD",
                "Evidence-based approach with systematic reviews and meta-analyses prioritized",
                "Session context manager implemented for continuity across sessions"
            ],
            user_requirements=[
                "300+ research findings in knowledge base",
                "90%+ avatar relevance (professional adult men)",
                "70%+ high-quality evidence standards",
                "Complete web application for ADHD assessment and resources",
                "Professional UI/UX design",
                "Deployment to public URL"
            ],
            quality_targets={
                "avatar_relevance": "≥90% professional adult male applicability",
                "evidence_quality": "≥70% high-quality evidence (systematic reviews, RCTs, large cohorts)",
                "schema_compliance": "100% schema compliance for all data entries",
                "prisma_documentation": "Complete PRISMA methodology documentation",
                "application_functionality": "Functional web application with professional design"
            },
            migration_instructions="""
SESSION MIGRATION INSTRUCTIONS:

When migrating to a new session due to context limits:

1. PRIORITY FILES TO TRANSFER:
   - /home/ubuntu/add_research_project/session_context.json (THIS FILE - CRITICAL)
   - /home/ubuntu/todo.md (Updated task tracker)
   - /home/ubuntu/add_research_project/knowledge_base/knowledge_base.json (Main knowledge base)
   - /home/ubuntu/add_research_project/research/research_topics.txt (Remaining topics to process)

2. CURRENT STATE SUMMARY:
   - Project: ADD Professional Research & Application Development
   - Current Phase: 3 (Knowledge Base Development) - 29.7% complete
   - Knowledge Base: 89/300+ entries completed
   - Next Action: Continue parallel processing of research topics

3. CONTEXT INHERITANCE:
   - Load session_context.json to restore full project state
   - Review todo.md for current task status
   - Continue from current_phase_id in the context
   - Use remaining research topics for next parallel processing batch

4. AGENT CONTINUITY:
   - Session Context Manager must be reinitialized in new session
   - Update context after each significant progress milestone
   - Maintain this migration instruction format for future sessions

5. QUALITY ASSURANCE:
   - Verify knowledge base integrity after migration
   - Ensure all parallel processing results are properly integrated
   - Validate that no progress is lost during transition
"""
        )
        
        return context
    
    def load_context(self):
        """Load existing context or initialize new one"""
        if self.context_file.exists():
            try:
                with open(self.context_file, 'r') as f:
                    data = json.load(f)
                    # Convert dict back to dataclass instances
                    phases = [PhaseStatus(**phase_data) for phase_data in data['phases']]
                    for phase in phases:
                        phase.tasks = [TaskProgress(**task_data) for task_data in phase.tasks]
                    
                    data['phases'] = phases
                    self.context = SessionContext(**data)
            except Exception as e:
                print(f"Error loading context: {e}")
                self.context = self.initialize_context()
        else:
            self.context = self.initialize_context()
    
    def save_context(self):
        """Save current context to file"""
        if self.context:
            self.context.last_updated = datetime.now().isoformat()
            
            # Convert dataclasses to dict for JSON serialization
            context_dict = asdict(self.context)
            
            with open(self.context_file, 'w') as f:
                json.dump(context_dict, f, indent=2)
    
    def update_task_progress(self, task_id: str, status: str, progress: float, notes: str = ""):
        """Update progress for a specific task"""
        if not self.context:
            return
            
        for phase in self.context.phases:
            for task in phase.tasks:
                if task.task_id == task_id:
                    task.status = status
                    task.progress_percentage = progress
                    task.last_updated = datetime.now().isoformat()
                    if notes:
                        task.notes = notes
                    break
        
        self.save_context()
    
    def update_phase_progress(self, phase_id: int):
        """Update phase progress based on task completion"""
        if not self.context:
            return
            
        phase = next((p for p in self.context.phases if p.phase_id == phase_id), None)
        if not phase:
            return
        
        if phase.tasks:
            total_progress = sum(task.progress_percentage for task in phase.tasks)
            phase.progress_percentage = total_progress / len(phase.tasks)
            
            completed_tasks = sum(1 for task in phase.tasks if task.status == "completed")
            if completed_tasks == len(phase.tasks):
                phase.status = "completed"
                phase.completion_date = datetime.now().isoformat()
            elif any(task.status == "in_progress" for task in phase.tasks):
                phase.status = "in_progress"
        
        self.save_context()
    
    def update_knowledge_base_stats(self, total_entries: int, last_batch: int = None):
        """Update knowledge base statistics"""
        if not self.context:
            return
            
        self.context.knowledge_base_stats["total_entries"] = total_entries
        self.context.knowledge_base_stats["completion_percentage"] = (total_entries / 300) * 100
        
        if last_batch:
            self.context.knowledge_base_stats["last_batch_processed"] = last_batch
        
        # Update task 3.1 progress
        self.update_task_progress(
            "3.1", 
            "in_progress", 
            (total_entries / 300) * 100,
            f"Completed {last_batch or 'multiple'} batches of parallel processing, {total_entries} valid entries extracted"
        )
        
        self.save_context()
    
    def get_migration_summary(self) -> str:
        """Generate a summary for session migration"""
        if not self.context:
            return "No context available"
        
        current_phase = next((p for p in self.context.phases if p.phase_id == self.context.current_phase_id), None)
        
        summary = f"""
SESSION MIGRATION SUMMARY
========================

Project: {self.context.project_name}
Current Phase: {self.context.current_phase_id} - {current_phase.title if current_phase else 'Unknown'}
Overall Progress: {current_phase.progress_percentage if current_phase else 0:.1f}%

Knowledge Base Status:
- Entries: {self.context.knowledge_base_stats['total_entries']}/300+ ({self.context.knowledge_base_stats['completion_percentage']:.1f}%)
- Last Batch: {self.context.knowledge_base_stats.get('last_batch_processed', 'N/A')}

Next Actions:
{chr(10).join(f'- {action}' for action in self.context.next_actions)}

Critical Files:
{chr(10).join(f'- {file}: {desc}' for file, desc in self.context.key_files.items())}

Migration Instructions:
{self.context.migration_instructions}
"""
        return summary
    
    def add_technical_note(self, note: str):
        """Add a technical note to the context"""
        if self.context:
            self.context.technical_notes.append(f"{datetime.now().isoformat()}: {note}")
            self.save_context()
    
    def update_next_actions(self, actions: List[str]):
        """Update the list of next actions"""
        if self.context:
            self.context.next_actions = actions
            self.save_context()

# Initialize the session context manager
if __name__ == "__main__":
    manager = SessionContextManager()
    manager.save_context()
    print("Session Context Manager initialized and saved.")
    print(f"Context file: {manager.context_file}")
    print(f"Current phase: {manager.context.current_phase_id}")
    print(f"Knowledge base entries: {manager.context.knowledge_base_stats['total_entries']}")

