# ADHD Research Database Documentation

## Executive Summary

This document provides comprehensive documentation for the ADHD Research Database system, a PostgreSQL-based solution with Prisma ORM that stores and manages evidence-based research data specifically focused on professional men aged 25-55 with ADHD. The system includes a complete web API and frontend interface for accessing and analyzing research findings.

## System Architecture

### Technology Stack
- **Database**: PostgreSQL 14
- **ORM**: Prisma 6.16.2
- **Backend**: Flask 3.1.1 with Python 3.11
- **Frontend**: HTML5/CSS3/JavaScript (Vanilla)
- **Environment**: Ubuntu 22.04 with Node.js 22.13.0

### Database Schema Overview

The database is designed with a normalized structure that separates research entries into logical components:

#### Core Tables
1. **research_entries** - Main research entry records
2. **target_populations** - Demographics and population characteristics
3. **methodologies** - Study design and methodology details
4. **key_findings** - Primary results and effect sizes
5. **workplace_relevance** - Professional and workplace-specific impacts
6. **quality_assessments** - Evidence quality and bias assessments
7. **clinical_applications** - Diagnostic and treatment applications
8. **tags** - Categorization and tagging system

#### Supporting Tables
- **treatment_recommendations** - Evidence-based treatment guidelines
- **assessment_tools** - Validated assessment instruments
- **outcome_measures** - Standardized outcome measurement tools

### Data Model Relationships

```
research_entries (1:1) → target_populations
research_entries (1:1) → methodologies
research_entries (1:1) → key_findings
research_entries (1:1) → workplace_relevance
research_entries (1:1) → quality_assessments
research_entries (1:1) → clinical_applications
research_entries (M:N) → tags
```

## Database Setup Instructions

### Prerequisites
- Ubuntu 22.04 or compatible Linux distribution
- PostgreSQL 14+
- Node.js 22.13.0+
- Python 3.11+

### Installation Steps

1. **Install PostgreSQL**
```bash
sudo apt update
sudo apt install -y postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

2. **Create Database and User**
```bash
sudo -u postgres psql -c "CREATE DATABASE adhd_research;"
sudo -u postgres psql -c "CREATE USER adhd_user WITH PASSWORD 'adhd_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE adhd_research TO adhd_user;"
sudo -u postgres psql -c "ALTER USER adhd_user CREATEDB;"
```

3. **Initialize Node.js Project**
```bash
npm init -y
npm install prisma @prisma/client pg
npm install -D @types/pg
```

4. **Configure Environment**
```bash
echo 'DATABASE_URL="postgresql://adhd_user:adhd_password@localhost:5432/adhd_research?schema=public"' > .env
```

5. **Initialize and Run Prisma Migrations**
```bash
npx prisma init
# Copy the provided schema.prisma file
npx prisma migrate dev --name init
npx prisma generate
```

6. **Migrate Data**
```bash
node migrate_data.js
```

## API Documentation

### Base URL
```
http://localhost:5000
```

### Authentication
Currently, the API does not require authentication. All endpoints are publicly accessible.

### Endpoints

#### Research Entries

**GET /api/research**
- Description: Retrieve all research entries with optional filtering
- Query Parameters:
  - `evidence_level`: Filter by evidence level (LEVEL_1A, LEVEL_1B, etc.)
  - `search`: Search by title, authors, or journal
  - `workplace_focus`: Boolean to filter workplace-focused research
- Response: JSON array of research entries

**GET /api/research/{id}**
- Description: Retrieve specific research entry with full details
- Parameters: Research entry ID
- Response: Complete research entry with all related data

**GET /api/research/stats**
- Description: Get database statistics and summary information
- Response: Statistics including counts, distributions, and recent additions

#### Treatment Recommendations

**GET /api/treatments**
- Description: Retrieve all treatment recommendations
- Response: JSON array of treatment recommendations

#### Assessment Tools

**GET /api/assessments**
- Description: Retrieve all assessment tools
- Response: JSON array of assessment tools

#### Tags

**GET /api/tags**
- Description: Retrieve all available tags
- Response: JSON array of tags

### Response Format

All API responses follow this structure:
```json
{
  "success": true|false,
  "data": <response_data>,
  "count": <number_of_items>,
  "error": "<error_message_if_applicable>"
}
```

## Frontend Interface

### Features
- **Search and Filter**: Full-text search across research entries with evidence level filtering
- **Statistics Dashboard**: Real-time database statistics and metrics
- **Responsive Design**: Mobile-friendly interface with modern CSS Grid layout
- **Evidence-Based Display**: Color-coded evidence levels and structured research presentation

### Usage
1. Navigate to `http://localhost:5000` when the Flask server is running
2. Use the search bar to find specific research
3. Apply filters for evidence levels or workplace-focused research
4. View statistics and browse all research entries

## Data Migration

### Current Data
The database contains:
- **3 Research Entries**: High-quality studies from 2025
- **15 Tags**: Categorization system for research types
- **2 Assessment Tools**: ASRS and AAQoL instruments
- **2 Treatment Recommendations**: Evidence-based treatment guidelines

### Migration Process
The `migrate_data.js` script handles:
1. Reading JSON knowledge base data
2. Creating normalized database records
3. Establishing relationships between entities
4. Adding supplementary assessment tools and treatment recommendations

## Development Workflow

### Starting the Application

1. **Start PostgreSQL** (if not running)
```bash
sudo systemctl start postgresql
```

2. **Start Flask API Server**
```bash
cd adhd_research_api
source venv/bin/activate
python src/main.py
```

3. **Access the Application**
- Frontend: http://localhost:5000
- API: http://localhost:5000/api/

### Making Schema Changes

1. **Update Prisma Schema**
```bash
# Edit prisma/schema.prisma
npx prisma migrate dev --name <migration_name>
npx prisma generate
```

2. **Update Migration Scripts**
```bash
# Modify migrate_data.js if needed
node migrate_data.js
```

## Security Considerations

### Current Security Status
- **Database**: Local PostgreSQL with basic authentication
- **API**: No authentication required (development setup)
- **CORS**: Enabled for all origins

### Production Recommendations
1. Implement API authentication (JWT tokens)
2. Add rate limiting and request validation
3. Use environment variables for sensitive configuration
4. Enable HTTPS/TLS encryption
5. Implement database connection pooling
6. Add input sanitization and SQL injection protection

## Performance Optimization

### Database Indexes
The current schema includes basic indexes. Consider adding:
- Full-text search indexes on title and authors
- Composite indexes for common query patterns
- Partial indexes for filtered queries

### Caching Strategy
For production deployment:
- Implement Redis caching for frequently accessed data
- Add API response caching
- Consider database query result caching

## Monitoring and Maintenance

### Health Checks
- Database connectivity: `SELECT 1;`
- API health: `GET /api/research/stats`
- Data integrity: Regular count validations

### Backup Strategy
```bash
# Database backup
pg_dump adhd_research > backup_$(date +%Y%m%d).sql

# Restore from backup
psql adhd_research < backup_file.sql
```

### Log Monitoring
- Flask application logs
- PostgreSQL query logs
- System resource monitoring

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Verify PostgreSQL is running
   - Check DATABASE_URL configuration
   - Confirm user permissions

2. **Migration Failures**
   - Ensure database user has CREATEDB permission
   - Check for existing data conflicts
   - Verify Prisma schema syntax

3. **API Errors**
   - Check Flask server logs
   - Verify database connectivity
   - Confirm all dependencies are installed

### Debug Commands
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Test database connection
psql "postgresql://adhd_user:adhd_password@localhost:5432/adhd_research"

# View Prisma schema status
npx prisma db pull
npx prisma validate
```

## Future Enhancements

### Planned Features
1. **User Authentication**: Role-based access control
2. **Advanced Search**: Semantic search capabilities
3. **Data Visualization**: Charts and graphs for research trends
4. **Export Functionality**: PDF and CSV export options
5. **API Versioning**: Structured API versioning strategy

### Scalability Considerations
1. **Database Sharding**: For large-scale data growth
2. **Microservices**: Split into specialized services
3. **CDN Integration**: For static asset delivery
4. **Load Balancing**: Multiple application instances

## Contact and Support

For technical questions or issues:
- Review this documentation
- Check the troubleshooting section
- Examine application logs
- Verify database connectivity and permissions

This documentation provides a comprehensive guide for understanding, deploying, and maintaining the ADHD Research Database system.

