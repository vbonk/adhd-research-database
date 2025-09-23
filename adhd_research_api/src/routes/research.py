from flask import Blueprint, jsonify, request
from src.database_config import prisma

research_bp = Blueprint('research', __name__)

@research_bp.route('/api/research', methods=['GET'])
def get_all_research():
    """Get all research entries with optional filtering"""
    try:
        # Get query parameters
        evidence_level = request.args.get('evidence_level')
        search = request.args.get('search')
        workplace_focus = request.args.get('workplace_focus', '').lower() == 'true'
        
        if evidence_level:
            data = prisma.get_research_by_evidence_level(evidence_level.upper())
        elif search:
            data = prisma.search_research_entries(search)
        elif workplace_focus:
            data = prisma.get_workplace_focused_research()
        else:
            data = prisma.find_many_research_entries()
        
        return jsonify({
            'success': True,
            'data': data,
            'count': len(data)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@research_bp.route('/api/research/<research_id>', methods=['GET'])
def get_research_by_id(research_id):
    """Get specific research entry by ID"""
    try:
        query = f"""
        SELECT 
            re.*,
            tp.age_range, tp.gender, tp.occupation, tp.adhd_subtype,
            m.design, m.duration, m.primary_outcomes, m.secondary_outcomes,
            kf.primary_results, kf.effect_sizes, kf.clinical_significance, kf.limitations,
            wr.productivity_impact, wr.accommodation_needs, wr.career_implications,
            qa.risk_of_bias, qa.grade_rating, qa.reviewer_notes,
            ca.diagnostic_utility, ca.treatment_recommendations, ca.monitoring_parameters
        FROM research_entries re
        LEFT JOIN target_populations tp ON re.target_population_id = tp.id
        LEFT JOIN methodologies m ON re.methodology_id = m.id
        LEFT JOIN key_findings kf ON re.key_findings_id = kf.id
        LEFT JOIN workplace_relevance wr ON re.workplace_relevance_id = wr.id
        LEFT JOIN quality_assessments qa ON re.quality_assessment_id = qa.id
        LEFT JOIN clinical_applications ca ON re.clinical_applications_id = ca.id
        WHERE re.id = '{research_id}';
        """
        
        data = prisma.query_raw(query)
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Research entry not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': data[0]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@research_bp.route('/api/research/stats', methods=['GET'])
def get_research_stats():
    """Get research database statistics"""
    try:
        stats = {}
        
        # Total counts
        stats['total_research_entries'] = len(prisma.query_raw("SELECT COUNT(*) FROM research_entries;"))
        stats['total_treatment_recommendations'] = len(prisma.query_raw("SELECT COUNT(*) FROM treatment_recommendations;"))
        stats['total_assessment_tools'] = len(prisma.query_raw("SELECT COUNT(*) FROM assessment_tools;"))
        
        # Evidence level distribution
        evidence_levels = prisma.query_raw("""
            SELECT "evidenceLevel", COUNT(*) as count 
            FROM research_entries 
            GROUP BY "evidenceLevel" 
            ORDER BY "evidenceLevel";
        """)
        stats['evidence_level_distribution'] = evidence_levels
        
        # Study type distribution
        study_types = prisma.query_raw("""
            SELECT "studyType", COUNT(*) as count 
            FROM research_entries 
            GROUP BY "studyType" 
            ORDER BY count DESC;
        """)
        stats['study_type_distribution'] = study_types
        
        # Recent additions
        recent = prisma.query_raw("""
            SELECT title, "addedDate" 
            FROM research_entries 
            ORDER BY "addedDate" DESC 
            LIMIT 5;
        """)
        stats['recent_additions'] = recent
        
        return jsonify({
            'success': True,
            'data': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@research_bp.route('/api/treatments', methods=['GET'])
def get_treatment_recommendations():
    """Get all treatment recommendations"""
    try:
        data = prisma.find_many_treatment_recommendations()
        return jsonify({
            'success': True,
            'data': data,
            'count': len(data)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@research_bp.route('/api/assessments', methods=['GET'])
def get_assessment_tools():
    """Get all assessment tools"""
    try:
        data = prisma.find_many_assessment_tools()
        return jsonify({
            'success': True,
            'data': data,
            'count': len(data)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@research_bp.route('/api/tags', methods=['GET'])
def get_all_tags():
    """Get all available tags"""
    try:
        data = prisma.query_raw("SELECT * FROM tags ORDER BY name;")
        return jsonify({
            'success': True,
            'data': data,
            'count': len(data)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

