---
title: Friction Log
description: Known limitations, workarounds, and areas for improvement in the ADHD Research Database
audience: all
difficulty: reference
---

# Friction Log

This document tracks known limitations, friction points, and areas where the ADHD Research Database could be improved. We believe in transparency about what works well and what doesn't.

## Current Limitations

### Dataset Size

**Status:** Expanding

The database currently contains 281 research entries. While this covers significant ADHD research, it represents a fraction of the total literature available.

**Workarounds:**
- Use specific search terms to find the most relevant entries
- Check the "Related Research" suggestions for connected studies
- Submit missing research via GitHub issues for inclusion

**Planned Improvements:**
- Automated PubMed integration for continuous updates
- Community submission pipeline for new research
- Target: 1,000+ entries by end of 2026

---

### No Authentication System

**Status:** By Design (for now)

The API and database are completely open with no user accounts or authentication.

**Implications:**
- Anyone can access all research data
- No personalized features (saved searches, bookmarks)
- No user-specific history tracking
- Cannot implement user preferences

**Workarounds:**
- Bookmark search URLs in your browser for quick access
- Use browser extensions to save favorite entries
- Export results to local files for personal organization

**Planned Improvements:**
- Optional user accounts (Q3 2026)
- Saved searches and bookmarks
- Personal research collections

---

### No Rate Limiting

**Status:** Monitoring

The API has no rate limiting, which means:
- Heavy usage could impact performance for all users
- No protection against accidental infinite loops
- Potential for abuse (though none observed)

**Workarounds:**
- Add reasonable delays between programmatic requests
- Cache API responses locally when building applications
- Use batch endpoints when available

**Planned Improvements:**
- Implement rate limiting (100 requests/minute per IP)
- Add API keys for higher limits
- Request queuing for heavy operations

---

### No Pagination on Results

**Status:** Open

Search results return all matches without pagination. With the current dataset size (281 entries), this is manageable but will become problematic as the database grows.

**Implications:**
- Large result sets load slowly
- Browser may lag with many results
- Mobile devices particularly affected

**Workarounds:**
- Use more specific search terms to reduce result count
- Filter by category or year to narrow results
- Use browser's find function (Ctrl+F) within results

**Planned Improvements:**
- Server-side pagination (20 results per page)
- Infinite scroll option
- Result count limits with "load more" functionality

---

### Limited Search Operators

**Status:** Open

The search functionality supports basic text matching but lacks advanced operators.

**Not Supported:**
- Boolean operators (AND, OR, NOT)
- Phrase matching ("exact phrase")
- Wildcard searches (neuro*)
- Field-specific searches (author:Smith)
- Date range filtering

**Workarounds:**
- Perform multiple searches and compare results manually
- Use category filters to narrow scope
- Browse by year for date-based exploration

**Planned Improvements:**
- Full-text search with PostgreSQL ts_vector
- Boolean operator support
- Advanced search interface

---

### No Offline Support

**Status:** Won't Fix (near-term)

The application requires an internet connection. There is no service worker, offline cache, or Progressive Web App (PWA) functionality.

**Implications:**
- Cannot access research while offline
- No background sync for saved items
- Mobile users on spotty connections affected

**Workarounds:**
- Export search results before going offline
- Use browser's "Save Page" feature for important entries
- Download PDFs of original research papers when available

**Planned Improvements:**
- PWA implementation is on the roadmap but not prioritized
- Focus remains on core functionality first

---

### No Mobile App

**Status:** Won't Fix

There are no native iOS or Android applications planned.

**Rationale:**
- Web application works on mobile browsers
- Limited development resources
- PWA would provide app-like experience when implemented

**Workarounds:**
- Add website to home screen for app-like access
- Use mobile browser's reading mode for better readability
- Landscape orientation may improve table viewing

---

## Known Issues

### Open Issues

| Issue | Description | Severity | Reported |
|-------|-------------|----------|----------|
| Search delay on first query | Initial search takes 2-3 seconds due to cold database connection | Low | 2026-01 |
| Long titles truncate on mobile | Research titles over 80 characters clip without ellipsis | Low | 2026-01 |
| Category filter resets on back button | Browser back navigation clears active filters | Medium | 2026-01 |

### In Progress

| Issue | Description | ETA |
|-------|-------------|-----|
| Inconsistent date formats | Some entries show YYYY-MM-DD, others show Month YYYY | Q1 2026 |
| Missing abstracts | ~15% of entries lack abstracts | Ongoing data entry |

### Won't Fix

| Issue | Reason |
|-------|--------|
| IE11 support | Browser is deprecated; use modern browsers |
| Print stylesheet | Low demand; use browser print preview |

---

## Performance Limitations

### Response Times

| Operation | Expected Time | Notes |
|-----------|---------------|-------|
| Page load | < 2 seconds | First visit may be slower |
| Search query | < 500ms | After initial connection |
| Filter application | < 100ms | Client-side filtering |
| Full database export | 5-10 seconds | Depends on connection speed |

### Factors That Impact Performance

1. **Cold starts:** First request after idle period is slower
2. **Network latency:** Users far from server experience delays
3. **Large result sets:** Rendering 100+ results causes browser lag
4. **Concurrent users:** No load balancing implemented

### Optimization Tips

- Use specific search terms to reduce result volume
- Avoid refreshing during peak hours (9 AM - 5 PM EST)
- Clear browser cache if experiencing persistent slowness

---

## Browser Compatibility

### Fully Supported

| Browser | Minimum Version |
|---------|-----------------|
| Chrome | 90+ |
| Firefox | 88+ |
| Safari | 14+ |
| Edge | 90+ |

### Partial Support

| Browser | Issues |
|---------|--------|
| Safari < 14 | Flexbox layout issues |
| Firefox < 88 | Some CSS features degraded |

### Not Supported

| Browser | Reason |
|---------|--------|
| Internet Explorer | Deprecated; uses unsupported JavaScript features |
| Opera Mini | Extreme mode disables required JavaScript |

### Required Browser Features

- JavaScript ES6+ (const, let, arrow functions, fetch API)
- CSS Grid and Flexbox
- LocalStorage (for preferences)
- Modern DOM APIs

---

## Mobile Experience

### Current State

The application is responsive but not mobile-optimized.

### Known Mobile Issues

| Issue | Devices Affected | Workaround |
|-------|------------------|------------|
| Table horizontal scroll | All phones | Rotate to landscape |
| Touch targets too small | Older phones | Zoom in on buttons |
| Keyboard covers search | iOS Safari | Scroll up after typing |
| Results text too small | Small screens | Use browser zoom |

### Recommended Mobile Usage

1. Use landscape orientation for data tables
2. Enable "Desktop Site" for full functionality
3. Use browser's built-in zoom for readability
4. Consider tablet for extended research sessions

---

## Data Freshness

### Update Schedule

| Data Type | Update Frequency | Last Updated |
|-----------|------------------|--------------|
| Research entries | Weekly | 2026-02-01 |
| Categories | As needed | 2026-01-15 |
| Metadata corrections | Daily | 2026-02-02 |

### Data Sources

- Manual curation from peer-reviewed journals
- PubMed abstracts (with attribution)
- Community submissions (verified before inclusion)

### Staleness Indicators

- Entries show "Added" date in metadata
- Search results prioritize recent additions
- Homepage displays "Last updated" timestamp

### Requesting Updates

If you notice outdated or incorrect information:

1. Open a GitHub issue with the entry ID
2. Provide the correct information with source
3. Updates typically processed within 48 hours

---

## Feature Gaps

### Compared to Similar Tools

| Feature | ADHD Research DB | PubMed | Google Scholar |
|---------|------------------|--------|----------------|
| ADHD-specific curation | Yes | No | No |
| Plain language summaries | Yes | No | No |
| Full-text search | Limited | Yes | Yes |
| Citation export | No | Yes | Yes |
| Alerts/notifications | No | Yes | Yes |
| API access | Yes | Yes | No |

### Planned Features (Roadmap)

**Q1 2026:**
- Citation export (BibTeX, RIS)
- Improved search operators

**Q2 2026:**
- Email alerts for new research
- Related research recommendations

**Q3 2026:**
- User accounts (optional)
- Saved searches and collections

**Q4 2026:**
- API rate limiting and keys
- Pagination

**2027:**
- Mobile PWA
- Offline support
- Community annotations

---

## Reporting Issues

### How to Report

1. **GitHub Issues (Preferred)**
   - Visit: [GitHub Repository Issues](https://github.com/your-org/adhd-research-database/issues)
   - Use issue templates when available
   - Include browser/device information

2. **Email**
   - Contact: [maintainer email from repository]
   - Subject line: "ADHD Research DB Issue: [brief description]"

### What to Include

```markdown
**Description:**
[Clear description of the issue]

**Steps to Reproduce:**
1. Go to...
2. Click on...
3. Observe...

**Expected Behavior:**
[What should happen]

**Actual Behavior:**
[What actually happens]

**Environment:**
- Browser: Chrome 120
- OS: Windows 11
- Device: Desktop
- Screen size: 1920x1080
```

### Issue Priority Guidelines

| Priority | Criteria | Response Time |
|----------|----------|---------------|
| Critical | Data loss, security issue, complete breakage | 24 hours |
| High | Major feature broken, affects many users | 1 week |
| Medium | Feature partially broken, workaround exists | 2 weeks |
| Low | Minor inconvenience, cosmetic issues | Best effort |

---

## Contributing Improvements

We welcome contributions to address items in this friction log.

### How to Contribute

1. Check GitHub issues for existing discussions
2. Comment on issues you'd like to work on
3. Submit pull requests with improvements
4. Follow the contribution guidelines in CONTRIBUTING.md

### Priority Areas for Contributors

- Search functionality improvements
- Mobile responsiveness fixes
- Performance optimizations
- Documentation improvements
- Data entry and verification

---

*This friction log is updated regularly. Last review: 2026-02-02*

*Built with transparency in mind. Your feedback helps improve this resource for the ADHD research community.*
