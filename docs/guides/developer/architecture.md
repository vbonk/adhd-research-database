---
title: System Architecture
description: Technical architecture overview for the ADHD Research Database, covering the Flask backend, PostgreSQL database layer, Prisma schema management, and vanilla JavaScript frontend.
audience: developer
difficulty: intermediate
---

# System Architecture

This document provides a comprehensive overview of the ADHD Research Database system architecture. It covers the technology stack, component interactions, request flow, database design, and key architectural decisions.

## Table of Contents

1. [Technology Stack](#technology-stack)
2. [High-Level Architecture](#high-level-architecture)
3. [Component Overview](#component-overview)
4. [Request Flow](#request-flow)
5. [Directory Structure](#directory-structure)
6. [Database Layer](#database-layer)
7. [API Design](#api-design)
8. [Frontend Architecture](#frontend-architecture)
9. [Security Considerations](#security-considerations)
10. [Key Design Decisions](#key-design-decisions)

---

## Technology Stack

| Layer | Technology | Version | Purpose |
|-------|------------|---------|---------|
| **Runtime** | Python | 3.11 | Backend language |
| **Framework** | Flask | 3.1 | Web framework |
| **Database** | PostgreSQL | 14 | Primary data store |
| **Schema Management** | Prisma | 6.16 | Schema definition and migrations |
| **Frontend** | Vanilla JS | ES6+ | Client-side interactivity |
| **Styling** | CSS3 | - | Presentation layer |

### Why This Stack?

- **Flask**: Lightweight, unopinionated framework ideal for API-first applications
- **PostgreSQL**: Robust relational database with excellent JSON support for flexible research data
- **Prisma**: Type-safe schema management without the overhead of a full ORM
- **Vanilla JS**: Zero dependencies, fast load times, full control over behavior

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              CLIENT LAYER                                    │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                         Browser (Vanilla JS SPA)                       │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────┐ │ │
│  │  │   Research   │  │   Category   │  │    Source    │  │   Search   │ │ │
│  │  │    Views     │  │   Browser    │  │   Manager    │  │   Module   │ │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  └────────────┘ │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ HTTP/HTTPS (JSON)
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              SERVER LAYER                                    │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                         Flask Application                              │ │
│  │  ┌──────────────────────────────────────────────────────────────────┐ │ │
│  │  │                    CORS Middleware                                │ │ │
│  │  └──────────────────────────────────────────────────────────────────┘ │ │
│  │  ┌──────────────────────────────────────────────────────────────────┐ │ │
│  │  │                    Static File Server                            │ │ │
│  │  │                    (/static/ -> HTML/CSS/JS)                     │ │ │
│  │  └──────────────────────────────────────────────────────────────────┘ │ │
│  │  ┌──────────────────────────────────────────────────────────────────┐ │ │
│  │  │                    research_bp Blueprint                          │ │ │
│  │  │  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐ │ │ │
│  │  │  │   /api/    │  │   /api/    │  │   /api/    │  │   /api/    │ │ │ │
│  │  │  │  research  │  │ categories │  │  sources   │  │   search   │ │ │ │
│  │  │  └────────────┘  └────────────┘  └────────────┘  └────────────┘ │ │ │
│  │  └──────────────────────────────────────────────────────────────────┘ │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ psql subprocess (SQL)
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              DATA LAYER                                      │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                    PrismaClient Wrapper                                │ │
│  │                    (database_config.py)                                │ │
│  │  ┌──────────────────────────────────────────────────────────────────┐ │ │
│  │  │  execute_query()  │  Subprocess-based SQL execution              │ │ │
│  │  └──────────────────────────────────────────────────────────────────┘ │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                        PostgreSQL 14                                   │ │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐        │ │
│  │  │Research │ │Category │ │ Source  │ │  Tag    │ │ Author  │  ...   │ │
│  │  │ Papers  │ │         │ │         │ │         │ │         │        │ │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘        │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                      Prisma Schema                                     │ │
│  │                      (schema.prisma)                                   │ │
│  │  • Schema definition  • Migrations  • Type generation                 │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Component Overview

### Flask Application (`main.py`)

The Flask application serves as the central orchestrator:

```python
# Simplified structure
app = Flask(__name__)
CORS(app)  # Enable cross-origin requests

# Register blueprints
app.register_blueprint(research_bp, url_prefix='/api')

# Serve static files
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')
```

**Responsibilities:**
- Application initialization and configuration
- Blueprint registration for modular routing
- Static file serving for the frontend
- CORS configuration for API access

### Research Blueprint (`routes/research.py`)

Contains all API endpoint definitions organized by resource:

| Endpoint Group | Purpose |
|----------------|---------|
| `/api/research` | CRUD operations for research papers |
| `/api/categories` | Category management |
| `/api/sources` | Source/publication management |
| `/api/tags` | Tag management |
| `/api/authors` | Author management |
| `/api/search` | Full-text and filtered search |

### Database Configuration (`database_config.py`)

The `PrismaClient` wrapper provides database access:

```python
class PrismaClient:
    def __init__(self):
        self.database_url = os.environ.get('DATABASE_URL')

    def execute_query(self, sql, params=None):
        """Execute raw SQL via psql subprocess"""
        # Constructs psql command
        # Executes via subprocess
        # Returns parsed JSON results
```

**Key characteristics:**
- No ORM query builder - all queries are raw SQL
- Uses psql subprocess for execution
- JSON output parsing for structured results
- Connection string managed via environment variable

### Static Frontend (`static/`)

Single-page application built with vanilla JavaScript:

- **index.html**: Application shell and structure
- **app.js**: Main application logic and routing
- **api.js**: API client for backend communication
- **styles.css**: Application styling

---

## Request Flow

### API Request Lifecycle

```
┌──────────┐    ┌─────────┐    ┌───────────┐    ┌────────────┐    ┌──────────┐
│  Browser │───▶│  Flask  │───▶│ Blueprint │───▶│ PrismaClient│───▶│PostgreSQL│
│          │    │  CORS   │    │  Handler  │    │  execute() │    │          │
└──────────┘    └─────────┘    └───────────┘    └────────────┘    └──────────┘
     │               │               │                │                 │
     │   HTTP GET    │               │                │                 │
     │──────────────▶│               │                │                 │
     │               │  route match  │                │                 │
     │               │──────────────▶│                │                 │
     │               │               │  build query   │                 │
     │               │               │───────────────▶│                 │
     │               │               │                │   psql -c SQL   │
     │               │               │                │────────────────▶│
     │               │               │                │                 │
     │               │               │                │   JSON result   │
     │               │               │                │◀────────────────│
     │               │               │   parsed data  │                 │
     │               │               │◀───────────────│                 │
     │               │  JSON response│                │                 │
     │               │◀──────────────│                │                 │
     │  HTTP 200 JSON│               │                │                 │
     │◀──────────────│               │                │                 │
     │               │               │                │                 │
```

### Example: Fetching Research Papers

1. **Client Request**: `GET /api/research?category=neuroscience`
2. **CORS Middleware**: Validates origin, adds headers
3. **Blueprint Router**: Matches route to handler function
4. **Handler Logic**:
   - Validates query parameters
   - Constructs SQL query with filters
   - Calls `PrismaClient.execute_query()`
5. **Database Execution**:
   - PrismaClient spawns psql subprocess
   - SQL executed against PostgreSQL
   - Results returned as JSON
6. **Response**: JSON array of research papers

---

## Directory Structure

```
adhd-research-database/
├── prisma/
│   ├── schema.prisma          # Database schema definition
│   └── migrations/            # Migration history
│       └── YYYYMMDDHHMMSS_*/  # Timestamped migrations
│
├── adhd_research_api/
│   └── src/
│       ├── main.py            # Flask application entry point
│       ├── database_config.py # PrismaClient wrapper
│       │
│       ├── routes/
│       │   └── research.py    # API endpoint definitions
│       │
│       └── static/            # Frontend assets
│           ├── index.html     # SPA shell
│           ├── app.js         # Application logic
│           ├── api.js         # API client
│           └── styles.css     # Styling
│
├── tests/                     # Test suite
│   ├── test_api.py           # API endpoint tests
│   └── test_database.py      # Database layer tests
│
├── docs-new/                  # Documentation
│   └── guides/
│       └── developer/
│           └── architecture.md  # This file
│
├── requirements.txt           # Python dependencies
├── .env                       # Environment configuration
└── README.md                  # Project overview
```

### Key Files Explained

| File | Purpose |
|------|---------|
| `schema.prisma` | Single source of truth for database structure |
| `main.py` | Application bootstrap, configuration, and routing setup |
| `database_config.py` | Database abstraction layer with raw SQL execution |
| `research.py` | All API endpoint handlers organized by resource |
| `index.html` | SPA entry point with minimal HTML structure |
| `app.js` | Client-side routing, state management, view rendering |
| `api.js` | Fetch wrapper for backend API communication |

---

## Database Layer

### Prisma Schema (`schema.prisma`)

Prisma serves as the schema definition and migration tool:

```prisma
// Example schema structure (simplified)
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model ResearchPaper {
  id          Int       @id @default(autoincrement())
  title       String
  abstract    String?
  publishedAt DateTime?
  categoryId  Int?
  sourceId    Int?

  category    Category? @relation(fields: [categoryId], references: [id])
  source      Source?   @relation(fields: [sourceId], references: [id])
  tags        TagsOnPapers[]
  authors     AuthorsOnPapers[]

  createdAt   DateTime  @default(now())
  updatedAt   DateTime  @updatedAt
}

model Category {
  id          Int             @id @default(autoincrement())
  name        String          @unique
  description String?
  papers      ResearchPaper[]
}

// Additional models: Source, Tag, Author, etc.
```

### Database Tables (11 Total)

| Table | Purpose | Key Relationships |
|-------|---------|-------------------|
| `ResearchPaper` | Core research paper data | category, source, tags, authors |
| `Category` | Topic categories | papers |
| `Source` | Publication sources (journals, etc.) | papers |
| `Tag` | Flexible tagging | papers (many-to-many) |
| `Author` | Researcher information | papers (many-to-many) |
| `TagsOnPapers` | Tag-paper junction | tag, paper |
| `AuthorsOnPapers` | Author-paper junction | author, paper |
| `Citation` | Paper citations | citing paper, cited paper |
| `Note` | User notes on papers | paper |
| `Bookmark` | Saved papers | paper |
| `SearchHistory` | Search query logging | - |

### SQL Execution Pattern

The `PrismaClient` wrapper executes raw SQL rather than using an ORM:

```python
class PrismaClient:
    def execute_query(self, sql, params=None):
        """
        Execute SQL via psql subprocess.

        Args:
            sql: Raw SQL query string
            params: Query parameters (for sanitization)

        Returns:
            Parsed JSON results from psql output
        """
        # Build psql command
        cmd = [
            'psql',
            self.database_url,
            '-c', sql,
            '-t',  # Tuples only
            '-A',  # Unaligned output
            '-F', ','  # Field separator
        ]

        # Execute subprocess
        result = subprocess.run(cmd, capture_output=True, text=True)

        # Parse and return results
        return self._parse_output(result.stdout)
```

### Why Raw SQL?

1. **Full Control**: Complex queries, window functions, CTEs without abstraction leakage
2. **Performance**: No ORM overhead, query can be optimized directly
3. **Transparency**: What you write is what executes
4. **Prisma for Schema**: Get migration benefits without query builder complexity

---

## API Design

### RESTful Principles

The API follows REST conventions:

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/api/research` | List papers (with filters) |
| `GET` | `/api/research/:id` | Get single paper |
| `POST` | `/api/research` | Create paper |
| `PUT` | `/api/research/:id` | Update paper |
| `DELETE` | `/api/research/:id` | Delete paper |

### Response Format

All API responses follow a consistent structure:

```json
// Success response
{
  "success": true,
  "data": { ... },
  "meta": {
    "total": 100,
    "page": 1,
    "limit": 20
  }
}

// Error response
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Title is required",
    "details": { ... }
  }
}
```

### Query Parameters

List endpoints support filtering and pagination:

| Parameter | Type | Description |
|-----------|------|-------------|
| `page` | int | Page number (1-indexed) |
| `limit` | int | Items per page (default: 20, max: 100) |
| `category` | string | Filter by category name |
| `source` | string | Filter by source |
| `tag` | string | Filter by tag (multiple allowed) |
| `q` | string | Full-text search query |
| `sort` | string | Sort field (e.g., `publishedAt`) |
| `order` | string | Sort order (`asc` or `desc`) |

### CORS Configuration

CORS is enabled for all routes to support frontend development:

```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allows all origins in development
```

For production, restrict to specific origins:

```python
CORS(app, origins=['https://yourdomain.com'])
```

---

## Frontend Architecture

### Vanilla JavaScript SPA

The frontend is a single-page application without frameworks:

```
┌─────────────────────────────────────────────────────────────────┐
│                         index.html                               │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                      <div id="app">                       │  │
│  │  ┌─────────────┐  ┌────────────────────────────────────┐ │  │
│  │  │   Sidebar   │  │           Main Content             │ │  │
│  │  │  Navigation │  │  ┌──────────────────────────────┐  │ │  │
│  │  │             │  │  │        View Container        │  │ │  │
│  │  │  - Home     │  │  │   (dynamically rendered)     │  │ │  │
│  │  │  - Browse   │  │  │                              │  │ │  │
│  │  │  - Search   │  │  │                              │  │ │  │
│  │  │  - Add      │  │  └──────────────────────────────┘  │ │  │
│  │  └─────────────┘  └────────────────────────────────────┘ │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Module Structure

```javascript
// api.js - API Client
const API = {
  baseUrl: '/api',

  async getResearch(params = {}) {
    const query = new URLSearchParams(params);
    const response = await fetch(`${this.baseUrl}/research?${query}`);
    return response.json();
  },

  async createResearch(data) {
    const response = await fetch(`${this.baseUrl}/research`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return response.json();
  }

  // Additional methods for other resources
};
```

```javascript
// app.js - Application Logic
const App = {
  state: {
    currentView: 'home',
    papers: [],
    categories: [],
    filters: {}
  },

  init() {
    this.bindEvents();
    this.loadInitialData();
    this.render();
  },

  async loadInitialData() {
    this.state.papers = await API.getResearch();
    this.state.categories = await API.getCategories();
    this.render();
  },

  render() {
    const container = document.getElementById('app');
    container.innerHTML = this.views[this.state.currentView]();
  }

  // View rendering methods
};
```

### Client-Side Routing

Hash-based routing for SPA navigation:

```javascript
// Simple hash router
window.addEventListener('hashchange', () => {
  const route = window.location.hash.slice(1) || 'home';
  App.navigate(route);
});

// Navigation
App.navigate = function(route) {
  this.state.currentView = route;
  this.render();
};
```

### State Management

Simple object-based state with render triggers:

```javascript
// State update pattern
App.updateState = function(updates) {
  Object.assign(this.state, updates);
  this.render();
};

// Usage
App.updateState({
  papers: newPapers,
  filters: { category: 'neuroscience' }
});
```

---

## Security Considerations

### Input Validation

All user input is validated at multiple levels:

1. **Client-side**: Form validation for immediate feedback
2. **Server-side**: Parameter validation in route handlers
3. **Database**: Parameterized queries prevent SQL injection

```python
# Example validation in route handler
@research_bp.route('/research', methods=['POST'])
def create_research():
    data = request.get_json()

    # Validate required fields
    if not data.get('title'):
        return jsonify({'error': 'Title is required'}), 400

    # Sanitize and validate types
    title = str(data['title'])[:500]  # Limit length

    # Use parameterized query
    sql = "INSERT INTO research_paper (title) VALUES (%s) RETURNING id"
    result = db.execute_query(sql, [title])
```

### SQL Injection Prevention

Even with raw SQL, parameterized queries are used:

```python
# UNSAFE - Never do this
sql = f"SELECT * FROM papers WHERE title = '{user_input}'"

# SAFE - Parameterized query
sql = "SELECT * FROM papers WHERE title = %s"
result = db.execute_query(sql, [user_input])
```

### CORS Security

In production, restrict CORS to known origins:

```python
CORS(app, origins=[
    'https://adhd-research.example.com',
    'https://admin.adhd-research.example.com'
])
```

### Environment Variables

Sensitive configuration stored in environment:

```bash
# .env file (never commit to git)
DATABASE_URL=postgresql://user:password@localhost:5432/adhd_research
SECRET_KEY=your-secret-key-here
FLASK_ENV=production
```

### Additional Recommendations

- [ ] Implement rate limiting for API endpoints
- [ ] Add authentication for write operations
- [ ] Enable HTTPS in production
- [ ] Implement request logging for audit trails
- [ ] Add CSRF protection for form submissions

---

## Key Design Decisions

### Decision 1: Prisma for Schema, Raw SQL for Queries

**Context**: Need database schema management without full ORM complexity.

**Decision**: Use Prisma for schema definition and migrations, but execute raw SQL queries.

**Rationale**:
- Schema changes are tracked and versioned via Prisma migrations
- Complex queries (joins, aggregations, window functions) are written directly
- No ORM magic or abstraction leakage
- Full PostgreSQL feature access

**Trade-offs**:
- (+) Complete query control
- (+) No ORM learning curve
- (-) More verbose query code
- (-) Manual result mapping

### Decision 2: Vanilla JavaScript Frontend

**Context**: Need interactive frontend without build complexity.

**Decision**: Use vanilla JavaScript without frameworks or build tools.

**Rationale**:
- Zero dependencies to maintain
- Fast initial load (no framework bundle)
- Full control over behavior
- Easy to understand and modify

**Trade-offs**:
- (+) No build step required
- (+) Smaller bundle size
- (-) More boilerplate code
- (-) No component reusability patterns

### Decision 3: Flask Blueprints for Organization

**Context**: API routes need organization as the application grows.

**Decision**: Use Flask blueprints to group related endpoints.

**Rationale**:
- Logical grouping of routes by resource
- Easy to add new resource groups
- Supports URL prefixes for versioning

### Decision 4: Subprocess-Based SQL Execution

**Context**: Need to execute SQL without a full database driver.

**Decision**: Use psql subprocess calls through PrismaClient wrapper.

**Rationale**:
- Leverages existing psql tool
- Consistent with Prisma CLI approach
- Simple implementation

**Trade-offs**:
- (+) No additional database driver dependency
- (-) Subprocess overhead per query
- (-) Connection pooling not available

**Future Consideration**: For high-traffic scenarios, consider switching to psycopg2 or asyncpg for connection pooling.

### Decision 5: Normalized Database Schema

**Context**: Research data has complex relationships.

**Decision**: Fully normalized schema with junction tables for many-to-many relationships.

**Rationale**:
- Data integrity through foreign keys
- Flexible querying across relationships
- No data duplication

---

## Conclusion

The ADHD Research Database architecture prioritizes simplicity and control:

- **Flask** provides a minimal, well-understood foundation
- **Prisma** manages schema evolution without ORM complexity
- **Raw SQL** enables full database feature access
- **Vanilla JS** delivers a responsive frontend without framework overhead

This architecture is well-suited for a focused research database application where query flexibility and development simplicity are more important than high-concurrency scaling.

---

*Documentation generated for ADHD Research Database*
*Last updated: 2026-02-02*

---

> **Attribution**: This documentation was generated with assistance from Claude, Anthropic's AI assistant.
