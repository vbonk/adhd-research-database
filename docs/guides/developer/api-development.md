---
title: API Development Guide
description: Complete guide to developing and extending the ADHD Research Database REST API using Flask 3.1 with Blueprints
audience: developer
difficulty: intermediate
---

# API Development Guide

This guide covers everything you need to know to develop, extend, and maintain the ADHD Research Database REST API. Built on Flask 3.1 with Blueprints, the API provides a clean, modular architecture for serving research data.

## Architecture Overview

The API follows a layered architecture:

```
┌─────────────────────────────────────────────────────────┐
│                    Client Request                        │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                 Flask Application                        │
│  ┌─────────────────────────────────────────────────┐   │
│  │              CORS Middleware                     │   │
│  └─────────────────────────────────────────────────┘   │
│                         │                               │
│  ┌─────────────────────────────────────────────────┐   │
│  │           Blueprint Router (/api)                │   │
│  └─────────────────────────────────────────────────┘   │
│                         │                               │
│  ┌─────────────────────────────────────────────────┐   │
│  │              Route Handlers                      │   │
│  │   research.py | treatments.py | assessments.py  │   │
│  └─────────────────────────────────────────────────┘   │
│                         │                               │
│  ┌─────────────────────────────────────────────────┐   │
│  │              PrismaClient                        │   │
│  │         (Raw SQL Query Execution)               │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                  PostgreSQL Database                     │
└─────────────────────────────────────────────────────────┘
```

## Flask Blueprint Structure

Blueprints provide modular organization for routes. The main routes file is located at:

```
adhd_research_api/src/routes/research.py
```

### Blueprint Registration

```python
# adhd_research_api/src/routes/research.py
from flask import Blueprint, jsonify, request

research_bp = Blueprint('research', __name__, url_prefix='/api')

@research_bp.route('/research', methods=['GET'])
def get_research():
    # Route implementation
    pass
```

### Registering Blueprints in the Application

```python
# adhd_research_api/src/app.py
from flask import Flask
from flask_cors import CORS
from routes.research import research_bp

def create_app():
    app = Flask(__name__)

    # Enable CORS for all routes
    CORS(app)

    # Register blueprints
    app.register_blueprint(research_bp)

    return app
```

## Standard Response Format

All API responses must follow this consistent format:

```python
{
    "success": True,           # Boolean indicating request success
    "data": [...],             # Response payload (array or object)
    "count": 42,               # Total count for paginated results
    "error": None              # Error message if success is False
}
```

### Response Helper Functions

Create consistent responses with helper functions:

```python
def success_response(data, count=None):
    """Generate a successful API response."""
    response = {
        "success": True,
        "data": data,
        "error": None
    }
    if count is not None:
        response["count"] = count
    return jsonify(response)

def error_response(message, status_code=400):
    """Generate an error API response."""
    return jsonify({
        "success": False,
        "data": None,
        "error": message
    }), status_code
```

### Usage Examples

```python
@research_bp.route('/research', methods=['GET'])
def get_research():
    try:
        results = prisma.query("SELECT * FROM research LIMIT 100")
        return success_response(results, count=len(results))
    except Exception as e:
        return error_response(str(e), 500)
```

## Adding New Endpoints

Follow this step-by-step process when adding new endpoints:

### Step 1: Define the Route

```python
@research_bp.route('/research/categories', methods=['GET'])
def get_categories():
    """
    Get all research categories.

    Query Parameters:
        - active_only (bool): Filter to active categories only

    Returns:
        JSON response with category list
    """
    pass
```

### Step 2: Parse Query Parameters

```python
@research_bp.route('/research/categories', methods=['GET'])
def get_categories():
    # Parse boolean parameter with default
    active_only = request.args.get('active_only', 'false').lower() == 'true'

    # Parse integer parameter with validation
    limit = request.args.get('limit', 50, type=int)
    if limit > 100:
        return error_response("Limit cannot exceed 100", 400)

    # Parse string parameter
    sort_by = request.args.get('sort', 'name')
    allowed_sorts = ['name', 'created_at', 'count']
    if sort_by not in allowed_sorts:
        return error_response(f"Invalid sort field. Allowed: {allowed_sorts}", 400)
```

### Step 3: Build and Execute Query

```python
    # Build query with parameters
    query = "SELECT * FROM categories WHERE 1=1"
    params = []

    if active_only:
        query += " AND active = %s"
        params.append(True)

    query += f" ORDER BY {sort_by} LIMIT %s"
    params.append(limit)

    results = prisma.query(query, params)
```

### Step 4: Return Response

```python
    return success_response(results, count=len(results))
```

### Complete Example

```python
@research_bp.route('/research/categories', methods=['GET'])
def get_categories():
    """
    Get all research categories.

    Query Parameters:
        - active_only (bool): Filter to active categories only
        - limit (int): Maximum results (default: 50, max: 100)
        - sort (str): Sort field (name, created_at, count)

    Returns:
        JSON response with category list
    """
    try:
        # Parse parameters
        active_only = request.args.get('active_only', 'false').lower() == 'true'
        limit = min(request.args.get('limit', 50, type=int), 100)
        sort_by = request.args.get('sort', 'name')

        # Validate sort field
        allowed_sorts = ['name', 'created_at', 'count']
        if sort_by not in allowed_sorts:
            return error_response(f"Invalid sort. Allowed: {allowed_sorts}", 400)

        # Build query
        query = "SELECT * FROM categories WHERE 1=1"
        params = []

        if active_only:
            query += " AND active = %s"
            params.append(True)

        query += f" ORDER BY {sort_by} LIMIT %s"
        params.append(limit)

        # Execute and return
        results = prisma.query(query, params)
        return success_response(results, count=len(results))

    except Exception as e:
        return error_response(str(e), 500)
```

## Query Parameter Handling

### Common Parameter Patterns

```python
# Boolean parameters
include_archived = request.args.get('include_archived', 'false').lower() == 'true'

# Integer parameters with defaults
page = request.args.get('page', 1, type=int)
per_page = request.args.get('per_page', 20, type=int)

# String parameters with validation
status = request.args.get('status', 'all')
valid_statuses = ['all', 'active', 'archived', 'draft']
if status not in valid_statuses:
    return error_response(f"Invalid status: {status}", 400)

# Date parameters
from datetime import datetime
date_from = request.args.get('from')
if date_from:
    try:
        date_from = datetime.fromisoformat(date_from)
    except ValueError:
        return error_response("Invalid date format. Use ISO 8601.", 400)

# List parameters (comma-separated)
tags = request.args.get('tags', '')
tag_list = [t.strip() for t in tags.split(',') if t.strip()]
```

### Pagination Pattern

```python
@research_bp.route('/research', methods=['GET'])
def get_research():
    # Parse pagination params
    page = max(1, request.args.get('page', 1, type=int))
    per_page = min(100, max(1, request.args.get('per_page', 20, type=int)))
    offset = (page - 1) * per_page

    # Get total count
    count_result = prisma.query("SELECT COUNT(*) as total FROM research")
    total = count_result[0]['total']

    # Get paginated results
    results = prisma.query(
        "SELECT * FROM research ORDER BY created_at DESC LIMIT %s OFFSET %s",
        [per_page, offset]
    )

    return jsonify({
        "success": True,
        "data": results,
        "count": total,
        "page": page,
        "per_page": per_page,
        "total_pages": (total + per_page - 1) // per_page,
        "error": None
    })
```

## Error Handling Patterns

### Exception Handling Decorator

```python
from functools import wraps

def handle_exceptions(f):
    """Decorator to handle exceptions consistently."""
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            return error_response(f"Invalid input: {str(e)}", 400)
        except PermissionError as e:
            return error_response(f"Permission denied: {str(e)}", 403)
        except FileNotFoundError as e:
            return error_response(f"Resource not found: {str(e)}", 404)
        except Exception as e:
            # Log the full error for debugging
            app.logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
            return error_response("Internal server error", 500)
    return decorated

# Usage
@research_bp.route('/research/<int:id>', methods=['GET'])
@handle_exceptions
def get_research_by_id(id):
    result = prisma.query("SELECT * FROM research WHERE id = %s", [id])
    if not result:
        raise FileNotFoundError(f"Research item {id} not found")
    return success_response(result[0])
```

### Validation Pattern

```python
def validate_research_input(data):
    """Validate research item input data."""
    errors = []

    if not data.get('title'):
        errors.append("Title is required")
    elif len(data['title']) > 255:
        errors.append("Title must be 255 characters or less")

    if not data.get('category_id'):
        errors.append("Category ID is required")

    if data.get('year'):
        try:
            year = int(data['year'])
            if year < 1900 or year > 2100:
                errors.append("Year must be between 1900 and 2100")
        except ValueError:
            errors.append("Year must be a valid integer")

    return errors

@research_bp.route('/research', methods=['POST'])
@handle_exceptions
def create_research():
    data = request.get_json()

    errors = validate_research_input(data)
    if errors:
        return error_response("; ".join(errors), 400)

    # Proceed with creation
    ...
```

## Using PrismaClient for Database Queries

The PrismaClient wrapper provides a clean interface for executing raw SQL queries.

### Basic Queries

```python
from prisma_client import prisma

# Simple SELECT
results = prisma.query("SELECT * FROM research WHERE active = true")

# SELECT with parameters (prevents SQL injection)
results = prisma.query(
    "SELECT * FROM research WHERE category_id = %s AND year >= %s",
    [category_id, min_year]
)

# Single record
result = prisma.query_one(
    "SELECT * FROM research WHERE id = %s",
    [research_id]
)
```

### Insert Operations

```python
# Insert with returning
new_id = prisma.execute(
    """
    INSERT INTO research (title, description, category_id, year)
    VALUES (%s, %s, %s, %s)
    RETURNING id
    """,
    [title, description, category_id, year]
)
```

### Update Operations

```python
# Update with row count
rows_affected = prisma.execute(
    """
    UPDATE research
    SET title = %s, updated_at = NOW()
    WHERE id = %s
    """,
    [new_title, research_id]
)

if rows_affected == 0:
    return error_response("Research item not found", 404)
```

### Complex Queries

```python
# Join query
results = prisma.query("""
    SELECT
        r.id,
        r.title,
        r.year,
        c.name as category_name,
        array_agg(t.name) as tags
    FROM research r
    LEFT JOIN categories c ON r.category_id = c.id
    LEFT JOIN research_tags rt ON r.id = rt.research_id
    LEFT JOIN tags t ON rt.tag_id = t.id
    WHERE r.active = true
    GROUP BY r.id, r.title, r.year, c.name
    ORDER BY r.created_at DESC
    LIMIT %s
""", [limit])

# Aggregation query
stats = prisma.query_one("""
    SELECT
        COUNT(*) as total,
        COUNT(DISTINCT category_id) as categories,
        MIN(year) as earliest_year,
        MAX(year) as latest_year
    FROM research
    WHERE active = true
""")
```

## Testing API Endpoints

### Unit Testing with pytest

```python
# tests/test_research_api.py
import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_research_returns_success(client):
    """Test that GET /api/research returns success response."""
    response = client.get('/api/research')
    data = response.get_json()

    assert response.status_code == 200
    assert data['success'] is True
    assert 'data' in data
    assert 'count' in data
    assert data['error'] is None

def test_get_research_with_pagination(client):
    """Test pagination parameters."""
    response = client.get('/api/research?page=2&per_page=10')
    data = response.get_json()

    assert response.status_code == 200
    assert data['page'] == 2
    assert data['per_page'] == 10

def test_get_research_by_id_not_found(client):
    """Test 404 response for non-existent resource."""
    response = client.get('/api/research/99999')
    data = response.get_json()

    assert response.status_code == 404
    assert data['success'] is False
    assert 'not found' in data['error'].lower()

def test_invalid_query_parameter(client):
    """Test validation of query parameters."""
    response = client.get('/api/research?sort=invalid_field')
    data = response.get_json()

    assert response.status_code == 400
    assert data['success'] is False
```

### Integration Testing

```python
# tests/test_integration.py
import pytest

@pytest.fixture(scope='module')
def test_db():
    """Set up test database."""
    # Create test database and seed data
    yield
    # Cleanup after tests

def test_create_and_retrieve_research(client, test_db):
    """Test full create-retrieve cycle."""
    # Create
    create_response = client.post('/api/research', json={
        'title': 'Test Research Item',
        'category_id': 1,
        'year': 2024
    })
    assert create_response.status_code == 201
    created_id = create_response.get_json()['data']['id']

    # Retrieve
    get_response = client.get(f'/api/research/{created_id}')
    assert get_response.status_code == 200
    assert get_response.get_json()['data']['title'] == 'Test Research Item'
```

### Manual Testing with curl

```bash
# GET all research
curl -X GET "http://localhost:5000/api/research" | jq

# GET with query parameters
curl -X GET "http://localhost:5000/api/research?page=1&per_page=10&sort=year" | jq

# GET single item
curl -X GET "http://localhost:5000/api/research/1" | jq

# GET stats
curl -X GET "http://localhost:5000/api/research/stats" | jq

# POST new research (if implemented)
curl -X POST "http://localhost:5000/api/research" \
  -H "Content-Type: application/json" \
  -d '{"title": "New Study", "category_id": 1, "year": 2024}' | jq
```

## API Versioning Considerations

### URL-Based Versioning (Recommended)

```python
# Version 1 blueprint
v1_bp = Blueprint('v1', __name__, url_prefix='/api/v1')

@v1_bp.route('/research', methods=['GET'])
def get_research_v1():
    # Original implementation
    pass

# Version 2 blueprint with changes
v2_bp = Blueprint('v2', __name__, url_prefix='/api/v2')

@v2_bp.route('/research', methods=['GET'])
def get_research_v2():
    # New implementation with breaking changes
    pass

# Register both versions
app.register_blueprint(v1_bp)
app.register_blueprint(v2_bp)
```

### Deprecation Headers

```python
@v1_bp.route('/research', methods=['GET'])
def get_research_v1():
    response = success_response(data)
    response.headers['Deprecation'] = 'true'
    response.headers['Sunset'] = 'Sat, 01 Jan 2025 00:00:00 GMT'
    response.headers['Link'] = '</api/v2/research>; rel="successor-version"'
    return response
```

### Version Detection Middleware

```python
@app.before_request
def log_api_version():
    """Log which API version is being used."""
    if request.path.startswith('/api/v1'):
        app.logger.info(f"v1 API call: {request.path}")
    elif request.path.startswith('/api/v2'):
        app.logger.info(f"v2 API call: {request.path}")
```

## Documentation Requirements for New Endpoints

Every new endpoint must include:

### 1. Docstring Documentation

```python
@research_bp.route('/research/search', methods=['GET'])
def search_research():
    """
    Search research items by keyword.

    Performs full-text search across title, description, and abstract fields.

    Query Parameters:
        q (str): Search query (required, min 2 characters)
        category (int): Filter by category ID (optional)
        year_from (int): Minimum year filter (optional)
        year_to (int): Maximum year filter (optional)
        limit (int): Maximum results, default 20, max 100 (optional)

    Returns:
        200: Success response with matching research items
        400: Invalid query parameters
        500: Server error

    Example:
        GET /api/research/search?q=medication&category=1&limit=10

    Response:
        {
            "success": true,
            "data": [...],
            "count": 42,
            "error": null
        }
    """
```

### 2. OpenAPI Specification

```yaml
# docs/openapi.yaml
paths:
  /api/research/search:
    get:
      summary: Search research items
      description: Full-text search across research database
      parameters:
        - name: q
          in: query
          required: true
          schema:
            type: string
            minLength: 2
          description: Search query
        - name: category
          in: query
          required: false
          schema:
            type: integer
          description: Filter by category ID
      responses:
        '200':
          description: Successful search
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ResearchResponse'
```

### 3. Changelog Entry

```markdown
## [1.2.0] - 2024-03-15

### Added
- GET /api/research/search - Full-text search endpoint
  - Supports filtering by category, year range
  - Returns relevance-scored results
```

## Current API Endpoints Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/research` | GET | List all research items with pagination |
| `/api/research/{id}` | GET | Get single research item by ID |
| `/api/research/stats` | GET | Get aggregate statistics |
| `/api/treatments` | GET | List all treatments |
| `/api/assessments` | GET | List all assessments |
| `/api/tags` | GET | List all tags |

## Best Practices Summary

1. **Always use parameterized queries** - Never concatenate user input into SQL
2. **Validate all input** - Check types, ranges, and allowed values
3. **Return consistent responses** - Use the standard response format
4. **Handle errors gracefully** - Catch exceptions and return meaningful messages
5. **Document everything** - Docstrings, OpenAPI specs, and changelogs
6. **Write tests first** - Test-driven development catches issues early
7. **Log appropriately** - Info for normal operations, error for exceptions
8. **Consider backwards compatibility** - Use versioning for breaking changes

---

*This documentation is part of the ADHD Research Database project. For questions or contributions, please refer to the project repository.*
