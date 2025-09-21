const { PrismaClient } = require('@prisma/client');
const fs = require('fs');
const path = require('path');

const prisma = new PrismaClient();

async function migrateData() {
  try {
    // Read the JSON knowledge base
    const jsonPath = path.join(__dirname, 'knowledge_base', 'knowledge_base.json');
    const jsonData = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));
    
    console.log('Starting data migration...');
    
    // Migrate research entries
    for (const entry of jsonData.research_entries) {
      console.log(`Migrating: ${entry.title}`);
      
      // Create target population
      const targetPopulation = await prisma.targetPopulation.create({
        data: {
          ageRange: entry.target_population.age_range,
          gender: entry.target_population.gender,
          occupation: entry.target_population.occupation,
          adhdSubtype: entry.target_population.adhd_subtype
        }
      });
      
      // Create methodology
      const methodology = await prisma.methodology.create({
        data: {
          design: entry.methodology.design,
          duration: entry.methodology.duration,
          primaryOutcomes: entry.methodology.primary_outcomes,
          secondaryOutcomes: entry.methodology.secondary_outcomes
        }
      });
      
      // Create key findings
      const keyFindings = await prisma.keyFindings.create({
        data: {
          primaryResults: entry.key_findings.primary_results,
          effectSizes: entry.key_findings.effect_sizes,
          clinicalSignificance: entry.key_findings.clinical_significance,
          limitations: entry.key_findings.limitations
        }
      });
      
      // Create workplace relevance
      const workplaceRelevance = await prisma.workplaceRelevance.create({
        data: {
          productivityImpact: entry.workplace_relevance.productivity_impact,
          accommodationNeeds: entry.workplace_relevance.accommodation_needs,
          careerImplications: entry.workplace_relevance.career_implications
        }
      });
      
      // Create quality assessment
      const qualityAssessment = await prisma.qualityAssessment.create({
        data: {
          riskOfBias: entry.quality_assessment.risk_of_bias.toUpperCase(),
          gradeRating: entry.quality_assessment.grade_rating.toUpperCase(),
          reviewerNotes: entry.quality_assessment.reviewer_notes
        }
      });
      
      // Create clinical applications
      const clinicalApplications = await prisma.clinicalApplications.create({
        data: {
          diagnosticUtility: entry.clinical_applications.diagnostic_utility,
          treatmentRecommendations: entry.clinical_applications.treatment_recommendations,
          monitoringParameters: entry.clinical_applications.monitoring_parameters
        }
      });
      
      // Create or find tags
      const tagRecords = [];
      for (const tagName of entry.tags) {
        let tag = await prisma.tag.findUnique({
          where: { name: tagName }
        });
        
        if (!tag) {
          tag = await prisma.tag.create({
            data: { name: tagName }
          });
        }
        tagRecords.push(tag);
      }
      
      // Map study type and evidence level
      const studyTypeMap = {
        'systematic_review': 'SYSTEMATIC_REVIEW',
        'meta_analysis': 'META_ANALYSIS',
        'rct': 'RCT',
        'cohort': 'COHORT',
        'case_control': 'CASE_CONTROL'
      };
      
      const evidenceLevelMap = {
        '1a': 'LEVEL_1A',
        '1b': 'LEVEL_1B',
        '2a': 'LEVEL_2A',
        '2b': 'LEVEL_2B',
        '3a': 'LEVEL_3A',
        '3b': 'LEVEL_3B',
        '4': 'LEVEL_4',
        '5': 'LEVEL_5'
      };
      
      // Create research entry
      const researchEntry = await prisma.researchEntry.create({
        data: {
          title: entry.title,
          authors: entry.authors,
          journal: entry.journal,
          publicationDate: new Date(entry.publication_date),
          doi: entry.doi,
          studyType: studyTypeMap[entry.study_type] || 'RCT',
          evidenceLevel: evidenceLevelMap[entry.evidence_level] || 'LEVEL_2B',
          sampleSize: entry.sample_size,
          addedDate: new Date(entry.added_date),
          lastReviewed: new Date(entry.last_reviewed),
          targetPopulationId: targetPopulation.id,
          methodologyId: methodology.id,
          keyFindingsId: keyFindings.id,
          workplaceRelevanceId: workplaceRelevance.id,
          qualityAssessmentId: qualityAssessment.id,
          clinicalApplicationsId: clinicalApplications.id,
          tags: {
            connect: tagRecords.map(tag => ({ id: tag.id }))
          }
        }
      });
      
      console.log(`✓ Migrated: ${entry.title}`);
    }
    
    // Add some assessment tools
    const assessmentTools = [
      {
        name: "Adult ADHD Self-Report Scale",
        acronym: "ASRS",
        purpose: "Screening for adult ADHD symptoms",
        targetPopulation: "Adults 18+ years",
        administrationTime: 5,
        domains: ["Inattention", "Hyperactivity", "Impulsivity"],
        psychometricProperties: {
          reliability: "Good internal consistency (α = 0.88)",
          validity: "Good sensitivity and specificity for ADHD diagnosis"
        },
        clinicalUtility: "Brief screening tool suitable for primary care settings",
        limitations: ["Self-report bias", "May not capture functional impairment"]
      },
      {
        name: "Adult ADHD Quality of Life Scale",
        acronym: "AAQoL",
        purpose: "Assess quality of life impact of ADHD",
        targetPopulation: "Adults with ADHD",
        administrationTime: 10,
        domains: ["Life productivity", "Psychological health", "Life outlook", "Relationships"],
        psychometricProperties: {
          reliability: "Excellent internal consistency (α = 0.93)",
          validity: "Strong construct validity with ADHD symptom measures"
        },
        clinicalUtility: "Comprehensive assessment of ADHD impact on quality of life",
        limitations: ["ADHD-specific", "May not be sensitive to change"]
      }
    ];
    
    for (const tool of assessmentTools) {
      await prisma.assessmentTool.create({
        data: tool
      });
    }
    
    // Add treatment recommendations
    const treatmentRecommendations = [
      {
        condition: "Adult ADHD",
        treatmentType: "PHARMACOLOGICAL",
        interventionName: "Stimulant medications",
        evidenceLevel: "LEVEL_1A",
        effectSize: 0.5,
        recommendationStrength: "STRONG_FOR",
        targetPopulation: "Professional men aged 25-55",
        contraindications: ["Cardiovascular disease", "Substance abuse history"],
        sideEffects: ["Appetite suppression", "Sleep difficulties", "Increased heart rate"],
        monitoringRequirements: ["Blood pressure", "Heart rate", "Weight", "Sleep patterns"]
      },
      {
        condition: "Adult ADHD with comorbid anxiety/depression",
        treatmentType: "PSYCHOLOGICAL",
        interventionName: "Cognitive Behavioral Therapy",
        evidenceLevel: "LEVEL_1A",
        effectSize: 4.43,
        recommendationStrength: "STRONG_FOR",
        targetPopulation: "Professional men aged 25-55",
        contraindications: ["Severe cognitive impairment"],
        sideEffects: ["Temporary increase in anxiety during initial sessions"],
        monitoringRequirements: ["ADHD symptom scales", "Depression measures", "Anxiety measures"]
      }
    ];
    
    for (const recommendation of treatmentRecommendations) {
      await prisma.treatmentRecommendation.create({
        data: recommendation
      });
    }
    
    console.log('✓ Data migration completed successfully!');
    
    // Print summary
    const counts = await Promise.all([
      prisma.researchEntry.count(),
      prisma.tag.count(),
      prisma.assessmentTool.count(),
      prisma.treatmentRecommendation.count()
    ]);
    
    console.log('\nMigration Summary:');
    console.log(`- Research Entries: ${counts[0]}`);
    console.log(`- Tags: ${counts[1]}`);
    console.log(`- Assessment Tools: ${counts[2]}`);
    console.log(`- Treatment Recommendations: ${counts[3]}`);
    
  } catch (error) {
    console.error('Migration failed:', error);
  } finally {
    await prisma.$disconnect();
  }
}

migrateData();

