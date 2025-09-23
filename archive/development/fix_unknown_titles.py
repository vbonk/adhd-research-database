#!/usr/bin/env python3
"""
MINIMAL FIX: Replace "Unknown" titles with proper research finding titles
Following Quality Assurance Protocol - minimal change to fix specific issue
"""

import json
import re

def fix_unknown_titles():
    """Fix Unknown titles in enhanced_findings.json with proper research titles"""
    
    # Load the enhanced findings
    with open('public/enhanced_findings.json', 'r') as f:
        findings = json.load(f)
    
    print(f"Loaded {len(findings)} enhanced research findings")
    
    # Count unknown titles before fix
    unknown_count_before = sum(1 for f in findings if f.get('title') == 'Unknown')
    print(f"Found {unknown_count_before} entries with 'Unknown' titles")
    
    # Fix unknown titles by generating proper titles from domain and summary
    fixed_count = 0
    for i, finding in enumerate(findings):
        if finding.get('title') == 'Unknown':
            # Generate title from domain and summary
            domain = finding.get('domain', 'ADHD Research')
            summary = finding.get('summary', '')
            
            # Extract key concepts from summary for title
            if 'workplace' in summary.lower():
                title = f"ADHD Workplace Strategies for Professional Adults"
            elif 'medication' in summary.lower():
                title = f"ADHD Medication Management for Working Professionals"
            elif 'executive function' in summary.lower():
                title = f"Executive Function Enhancement for ADHD Professionals"
            elif 'stress' in summary.lower():
                title = f"ADHD Stress Management in Professional Settings"
            elif 'productivity' in summary.lower():
                title = f"ADHD Productivity Optimization for Working Adults"
            elif 'communication' in summary.lower():
                title = f"ADHD Communication Skills for Professional Success"
            elif 'time management' in summary.lower():
                title = f"ADHD Time Management Strategies for Professionals"
            elif 'focus' in summary.lower() or 'attention' in summary.lower():
                title = f"ADHD Focus Enhancement for Working Professionals"
            elif 'organization' in summary.lower():
                title = f"ADHD Organization Systems for Professional Adults"
            elif 'career' in summary.lower():
                title = f"ADHD Career Development and Professional Growth"
            else:
                # Fallback: use domain + professional context
                title = f"{domain} for Professional Adult Males (25-65)"
            
            # Update the title
            finding['title'] = title
            
            # Also update content library titles to match
            if 'contentLibrary' in finding and 'blogPost' in finding['contentLibrary']:
                finding['contentLibrary']['blogPost']['title'] = f"Complete Guide to {title}"
            
            if 'contentLibrary' in finding and 'ebookChapter' in finding['contentLibrary']:
                finding['contentLibrary']['ebookChapter']['title'] = f"Chapter {i+1}: {title}"
            
            fixed_count += 1
    
    print(f"Fixed {fixed_count} unknown titles")
    
    # Verify no unknown titles remain
    unknown_count_after = sum(1 for f in findings if f.get('title') == 'Unknown')
    print(f"Unknown titles remaining: {unknown_count_after}")
    
    # Save the fixed data
    with open('public/enhanced_findings.json', 'w') as f:
        json.dump(findings, f, indent=2)
    
    print(f"✅ Successfully fixed enhanced_findings.json")
    print(f"✅ All {len(findings)} entries now have proper titles")
    
    return len(findings), fixed_count

if __name__ == "__main__":
    total, fixed = fix_unknown_titles()
    print(f"\n🎯 MINIMAL FIX COMPLETE:")
    print(f"   Total entries: {total}")
    print(f"   Titles fixed: {fixed}")
    print(f"   Ready for local testing")

