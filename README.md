# ADHD Research Database

A comprehensive PostgreSQL database with Prisma ORM for storing and managing evidence-based ADHD research data, specifically focused on professional men aged 25-55. The system includes a complete web API and frontend interface for accessing and analyzing research findings.

![ADHD Research Database](https://img.shields.io/badge/Evidence--Based-Research-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-blue)
![Flask](https://img.shields.io/badge/Flask-3.1.1-green)
![Prisma](https://img.shields.io/badge/Prisma-6.16.2-purple)

## 🎯 Features

- **Comprehensive Research Database**: Structured storage of ADHD research with normalized schema
- **Evidence-Based Classification**: Research categorized by evidence levels (1A-5) following medical standards
- **Advanced Search & Filtering**: Full-text search across titles, authors, journals with evidence level filtering
- **Workplace-Focused Research**: Special filtering for professional men aged 25-55
- **Real-Time Statistics**: Live dashboard showing research counts, distributions, and trends
- **RESTful API**: Complete API for programmatic access to research data
- **Responsive Web Interface**: Modern, mobile-friendly interface for browsing research
- **Treatment Recommendations**: Evidence-based treatment guidelines and protocols
- **Assessment Tools**: Validated ADHD assessment instruments and outcome measures

## 📊 Current Database Content

- **3 High-Quality Research Entries** (2025 studies)
- **15 Research Tags** for categorization
- **2 Assessment Tools** (ASRS, AAQoL)
- **2 Treatment Recommendations** (Pharmacological & Psychological)
- **Multiple Evidence Levels** (1A systematic reviews to 2B cohort studies)

## 🚀 Quick Start

### Prerequisites

- PostgreSQL 14+
- Node.js 22.13.0+
- Python 3.11+
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/adhd-research-database.git
cd adhd-research-database
```

2. **Set up PostgreSQL**
```bash
sudo apt update && sudo apt install -y postgresql postgresql-contrib
sudo systemctl start postgresql && sudo systemctl enable postgresql

# Create database and user
sudo -u postgres psql -c "CREATE DATABASE adhd_research;"
sudo -u postgres psql -c "CREATE USER adhd_user WITH PASSWORD 'adhd_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE adhd_research TO adhd_user;"
sudo -u postgres psql -c "ALTER USER adhd_user CREATEDB;"
```

3. **Install dependencies**
```bash
# Node.js dependencies
npm install

# Python dependencies
cd adhd_research_api
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cd ..
```

4. **Configure environment**
```bash
echo 'DATABASE_URL="postgresql://adhd_user:adhd_password@localhost:5432/adhd_research?schema=public"' > .env
```

5. **Run database migrations**
```bash
npx prisma migrate dev --name init
npx prisma generate
```

6. **Migrate initial data**
```bash
node migrate_data.js
```

7. **Start the application**
```bash
cd adhd_research_api
source venv/bin/activate
python src/main.py
```

8. **Access the application**
- Frontend: http://localhost:5000
- API: http://localhost:5000/api/research

## 🏗️ Architecture

### Database Schema

The database uses a normalized structure with the following core tables:

- **research_entries**: Main research records
- **target_populations**: Demographics and population data
- **methodologies**: Study design and methodology details
- **key_findings**: Primary results and effect sizes
- **workplace_relevance**: Professional impact assessments
- **quality_assessments**: Evidence quality ratings
- **clinical_applications**: Treatment and diagnostic applications
- **tags**: Research categorization system

### Technology Stack

- **Database**: PostgreSQL 14 with Prisma ORM
- **Backend**: Flask 3.1.1 (Python 3.11)
- **Frontend**: HTML5/CSS3/JavaScript (Vanilla)
- **Environment**: Ubuntu 22.04, Node.js 22.13.0

## 📡 API Documentation

### Base URL
```
http://localhost:5000/api
```

### Endpoints

#### Research Entries
- `GET /research` - Get all research entries with optional filtering
- `GET /research/{id}` - Get specific research entry with full details
- `GET /research/stats` - Get database statistics

#### Treatment & Assessment
- `GET /treatments` - Get all treatment recommendations
- `GET /assessments` - Get all assessment tools
- `GET /tags` - Get all available tags

### Query Parameters
- `evidence_level`: Filter by evidence level (LEVEL_1A, LEVEL_1B, etc.)
- `search`: Search by title, authors, or journal
- `workplace_focus`: Boolean to filter workplace-focused research

### Response Format
```json
{
  "success": true,
  "data": [...],
  "count": 3,
  "error": null
}
```

## 🔍 Research Focus Areas

### Evidence Levels Supported
- **Level 1A**: Systematic reviews of RCTs (highest quality)
- **Level 1B**: Individual RCTs with narrow confidence intervals
- **Level 2A**: Systematic reviews of cohort studies
- **Level 2B**: Individual cohort studies
- **Level 3A-5**: Case-control studies to expert opinion

### Target Population
- **Primary Focus**: Professional men aged 25-55
- **Workplace Relevance**: Career impact, productivity, stress management
- **Comorbidities**: Anxiety, depression, executive function deficits

### Treatment Modalities
- **Pharmacological**: Stimulants, non-stimulants, combination therapies
- **Psychological**: CBT, mindfulness, stress management
- **Workplace Interventions**: Web-based programs, accommodation strategies

## 🚢 Deployment

### Docker Deployment
```bash
# Using Docker Compose
docker-compose up -d

# Run migrations
docker-compose exec app npx prisma migrate deploy
docker-compose exec app node migrate_data.js
```

### Cloud Deployment
The application is ready for deployment on:
- Railway
- Heroku
- AWS
- Google Cloud Platform
- Azure

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.

## 📚 Documentation

- [Database Documentation](DATABASE_DOCUMENTATION.md) - Comprehensive database guide
- [Deployment Guide](DEPLOYMENT_GUIDE.md) - Production deployment instructions
- [API Documentation](DATABASE_DOCUMENTATION.md#api-documentation) - Complete API reference

## 🧪 Research Data Sources

Current research entries include:

1. **Lancet Psychiatry 2025** - Network meta-analysis of ADHD treatments (Level 1A)
2. **Frontiers in Psychiatry 2025** - Non-pharmacological interventions review (Level 1A)
3. **JMIR Formative Research 2025** - Workplace stress management pilot (Level 2B)

All research is peer-reviewed and follows evidence-based medicine standards.

## 🤝 Contributing

We welcome contributions to expand the research database and improve the system:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-research`)
3. Add research data following the established schema
4. Commit changes (`git commit -am 'Add new research entry'`)
5. Push to branch (`git push origin feature/new-research`)
6. Create a Pull Request

### Research Contribution Guidelines
- Include DOI and full citation
- Provide evidence level classification
- Add workplace relevance assessment
- Include effect sizes where available
- Follow the established data schema

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔬 Research Ethics

This database is designed for:
- Evidence-based clinical decision making
- Research synthesis and meta-analysis
- Educational purposes
- Healthcare provider reference

**Not intended for**:
- Self-diagnosis
- Replacement of professional medical advice
- Commercial diagnostic tools without validation

## 📞 Support

For technical support or research contributions:
- Create an issue in this repository
- Review the documentation in `/docs`
- Check the troubleshooting section in [DATABASE_DOCUMENTATION.md](DATABASE_DOCUMENTATION.md)

## 🏆 Acknowledgments

- Research data sourced from peer-reviewed journals
- Built with modern web technologies and best practices
- Designed for healthcare professionals and researchers
- Focused on evidence-based ADHD treatment for working adults

---

**Disclaimer**: This database is for informational and research purposes only. Always consult with qualified healthcare professionals for medical advice and treatment decisions.

