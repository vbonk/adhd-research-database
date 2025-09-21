import os
import subprocess
import json
from typing import Dict, List, Any

class PrismaClient:
    """Simple wrapper for Prisma CLI operations"""
    
    def __init__(self, schema_path: str = None):
        self.schema_path = schema_path or "/home/ubuntu/add_research_project/prisma/schema.prisma"
        self.db_url = "postgresql://adhd_user:adhd_password@localhost:5432/adhd_research?schema=public"
    
    def query_raw(self, query: str) -> List[Dict[str, Any]]:
        """Execute raw SQL query using psql"""
        try:
            cmd = [
                "psql", 
                self.db_url,
                "-c", query,
                "-t",  # tuples only
                "--csv"  # CSV output
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            # Parse CSV output
            lines = result.stdout.strip().split('\n')
            if not lines or not lines[0]:
                return []
            
            # Simple CSV parsing (assuming no commas in data)
            headers = lines[0].split(',') if len(lines) > 1 else []
            data = []
            
            for line in lines[1:] if len(lines) > 1 else lines:
                if line.strip():
                    values = line.split(',')
                    if headers:
                        row = dict(zip(headers, values))
                    else:
                        row = {"result": line}
                    data.append(row)
            
            return data
        except subprocess.CalledProcessError as e:
            print(f"Database query error: {e}")
            return []
    
    def find_many_research_entries(self, include_relations: bool = True) -> List[Dict[str, Any]]:
        """Get all research entries with related data"""
        if include_relations:
            query = """
            SELECT 
                re.id, re.title, re.authors, re.journal, re.publication_date,
                re.doi, re.study_type, re.evidence_level, re.sample_size,
                tp.age_range, tp.gender, tp.occupation, tp.adhd_subtype,
                m.design, m.duration,
                kf.primary_results, kf.clinical_significance,
                wr.productivity_impact, wr.career_implications,
                qa.risk_of_bias, qa.grade_rating,
                ca.diagnostic_utility
            FROM research_entries re
            LEFT JOIN target_populations tp ON re.target_population_id = tp.id
            LEFT JOIN methodologies m ON re.methodology_id = m.id
            LEFT JOIN key_findings kf ON re.key_findings_id = kf.id
            LEFT JOIN workplace_relevance wr ON re.workplace_relevance_id = wr.id
            LEFT JOIN quality_assessments qa ON re.quality_assessment_id = qa.id
            LEFT JOIN clinical_applications ca ON re.clinical_applications_id = ca.id
            ORDER BY re.publication_date DESC;
            """
        else:
            query = "SELECT * FROM research_entries ORDER BY publication_date DESC;"
        
        return self.query_raw(query)
    
    def find_many_treatment_recommendations(self) -> List[Dict[str, Any]]:
        """Get all treatment recommendations"""
        query = "SELECT * FROM treatment_recommendations ORDER BY recommendation_strength, evidence_level;"
        return self.query_raw(query)
    
    def find_many_assessment_tools(self) -> List[Dict[str, Any]]:
        """Get all assessment tools"""
        query = "SELECT * FROM assessment_tools ORDER BY name;"
        return self.query_raw(query)
    
    def search_research_entries(self, search_term: str) -> List[Dict[str, Any]]:
        """Search research entries by title, authors, or journal"""
        query = f"""
        SELECT * FROM research_entries 
        WHERE title ILIKE '%{search_term}%' 
           OR array_to_string(authors, ', ') ILIKE '%{search_term}%'
           OR journal ILIKE '%{search_term}%'
        ORDER BY publication_date DESC;
        """
        return self.query_raw(query)
    
    def get_research_by_evidence_level(self, evidence_level: str) -> List[Dict[str, Any]]:
        """Get research entries by evidence level"""
        query = f"SELECT * FROM research_entries WHERE evidence_level = '{evidence_level}' ORDER BY publication_date DESC;"
        return self.query_raw(query)
    
    def get_workplace_focused_research(self) -> List[Dict[str, Any]]:
        """Get research entries with workplace relevance"""
        query = """
        SELECT re.*, wr.productivity_impact, wr.accommodation_needs, wr.career_implications
        FROM research_entries re
        JOIN workplace_relevance wr ON re.workplace_relevance_id = wr.id
        WHERE wr.productivity_impact IS NOT NULL AND wr.productivity_impact != ''
        ORDER BY re.publication_date DESC;
        """
        return self.query_raw(query)

# Global instance
prisma = PrismaClient()

