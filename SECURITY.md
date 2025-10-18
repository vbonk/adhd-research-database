# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it responsibly:

1. **DO NOT** create a public GitHub issue
2. Email the maintainer directly or use GitHub's private vulnerability reporting
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We aim to respond to security reports within 48 hours.

## Security Best Practices

### Environment Variables

This project uses environment variables for sensitive configuration:

1. **NEVER** commit `.env` files to version control
2. Use `.env.example` as a template (contains no real credentials)
3. Store production credentials securely (e.g., using a secrets manager)

### Database Security

1. **Always use strong passwords** for database accounts
2. **Rotate credentials regularly** (at least every 90 days)
3. **Use parameterized queries** for all user input (implemented in this codebase)
4. **Limit database user permissions** to only what's necessary

### API Security

1. **Validate all user input** before processing
2. **Use HTTPS** in production
3. **Implement rate limiting** to prevent abuse
4. **Keep dependencies up to date** (run `pip list --outdated` regularly)

## Recent Security Fixes

### October 2025 - Critical Security Update

**Fixed Issues:**
1. **Hardcoded database credentials** - Now uses environment variables
2. **SQL injection vulnerabilities** - Implemented parameterized queries

**Action Required:**
- If upgrading from an earlier version, you MUST:
  1. Create a `.env` file based on `.env.example`
  2. Set `DATABASE_URL` with your database credentials
  3. **Rotate your database password** (the old hardcoded password `adhd_password` was publicly visible)
  4. Update your deployment configuration to use environment variables

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| Latest  | :white_check_mark: |
| < 1.0   | :x:                |

## Security Update History

- **2025-10-17**: Fixed hardcoded credentials and SQL injection vulnerabilities
- Project maintains security best practices going forward
