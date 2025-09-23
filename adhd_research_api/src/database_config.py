import os
import subprocess
import json
from typing import Dict, List, Any

class PrismaClient:
    """Simple wrapper for Prisma CLI operations"""
    
    def __init__(self, schema_path: str = None):
        self.schema_path = schema_path or "/Users/tony/Projects/adhd-research-database/prisma/schema.prisma"
        self.db_url = "postgresql://adhd_user:adhd_password@localhost:5432/adhd_research"
    
    def query_raw(self, query: str) -> List[Dict[str, Any]]:
        """Execute raw SQL query using psql"""
        try:
            cmd = [
                "/opt/homebrew/opt/postgresql@14/bin/psql", 
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
            
            # Handle simple single value results (like COUNT)
            if len(lines) == 1 and lines[0].strip() and not ',' in lines[0]:
                # Single value result (like COUNT)
                return [{'count': int(lines[0].strip())}]
            
            # Handle CSV data (no headers in psql CSV output)
            data = []
            for line in lines:
                if line.strip():
                    # Split by comma, but handle quoted fields
                    import csv
                    import io
                    csv_reader = csv.reader(io.StringIO(line))
                    values = next(csv_reader)
                    
                    # For now, return as simple dict with indexed keys
                    # This is a simplified approach - in production you'd want proper column names
                    if len(values) == 1:
                        row = {"result": values[0]}
                    else:
                        row = {f"col_{i}": value for i, value in enumerate(values)}
                    data.append(row)
            
            return data
        except subprocess.CalledProcessError as e:
            print(f"Database query error: {e}")
            print(f"Command output: {e.stdout}")
            print(f"Command error: {e.stderr}")
            return []
    
    def find_many_research_entries(self, include_relations: bool = True) -> List[Dict[str, Any]]:
        """Get all research entries with related data"""
        if include_relations:
            query = """
            SELECT 
                re.id, re.title, re.authors::text, re.journal, re."publicationDate"::text,
                re.doi, re."studyType", re."evidenceLevel", re."sampleSize"::text,
                tp."ageRange", tp.gender, tp.occupation, tp."adhdSubtype",
                m.design, m.duration,
                kf."primaryResults", kf."clinicalSignificance",
                wr."productivityImpact", wr."careerImplications",
                qa."riskOfBias", qa."gradeRating",
                ca."diagnosticUtility"
            FROM research_entries re
            LEFT JOIN target_populations tp ON re."targetPopulationId" = tp.id
            LEFT JOIN methodologies m ON re."methodologyId" = m.id
            LEFT JOIN key_findings kf ON re."keyFindingsId" = kf.id
            LEFT JOIN workplace_relevance wr ON re."workplaceRelevanceId" = wr.id
            LEFT JOIN quality_assessments qa ON re."qualityAssessmentId" = qa.id
            LEFT JOIN clinical_applications ca ON re."clinicalApplicationsId" = ca.id
            ORDER BY re."publicationDate" DESC;
            """
        else:
            query = """SELECT id, title, authors::text, journal, "publicationDate"::text, doi, "studyType", "evidenceLevel", "sampleSize"::text FROM research_entries ORDER BY "publicationDate" DESC;"""
        
        raw_data = self.query_raw(query)
        
        # Convert the generic column data to proper field names
        if include_relations:
            column_names = [
                'id', 'title', 'authors', 'journal', 'publicationDate', 'doi', 'studyType', 'evidenceLevel', 'sampleSize',
                'ageRange', 'gender', 'occupation', 'adhdSubtype', 'design', 'duration',
                'primaryResults', 'clinicalSignificance', 'productivityImpact', 'careerImplications',
                'riskOfBias', 'gradeRating', 'diagnosticUtility'
            ]
        else:
            column_names = ['id', 'title', 'authors', 'journal', 'publicationDate', 'doi', 'studyType', 'evidenceLevel', 'sampleSize']
        
        result = []
        for row in raw_data:
            if 'col_0' in row:  # Generic column names
                new_row = {}
                for i, col_name in enumerate(column_names):
                    col_key = f'col_{i}'
                    if col_key in row:
                        # Handle special cases
                        if col_name == 'authors' and row[col_key]:
                            # Convert PostgreSQL array string back to list
                            authors_str = row[col_key].strip('{}')
                            if authors_str:
                                new_row[col_name] = [a.strip('\"\'') for a in authors_str.split(',')]
                            else:
                                new_row[col_name] = []
                        elif col_name in ['sample_size'] and row[col_key]:
                            try:
                                new_row[col_name] = int(row[col_key])
                            except:
                                new_row[col_name] = row[col_key]
                        else:
                            new_row[col_name] = row[col_key]
                result.append(new_row)
            else:
                result.append(row)
        
        return result
    
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

