# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Star History chart to encourage community engagement
- Comprehensive CONTRIBUTING.md guide
- CODE_OF_CONDUCT.md for community guidelines
- Enhanced README with Key Highlights section
- TypeScript and Black badges to showcase tech stack
- Contributors badge and recognition section

### Changed
- Improved README structure with better visual hierarchy
- Enhanced contribution guidelines with clearer steps
- Updated CI badge to reference main branch

## [1.0.0] - 2024-11-17

### Added
- 🌐 Next.js web dashboard with modern UI
- 🔍 Automatic AWS incident detection
- 💰 Free tier optimization with cost tracking
- 🔒 Production-ready security headers
- 📊 Support for EC2, Lambda, S3, and Bedrock monitoring
- ⚡ 30-second scan cooldown to prevent excessive costs
- 📱 Mobile-responsive design
- 🚀 One-click Vercel deployment
- 📖 Comprehensive documentation suite:
  - VERCEL_DEPLOYMENT.md
  - COST.md
  - SECURITY.md
  - PRODUCTION_READY.md
  - QUICKSTART.md
  - QUICKSTART_WEB.md

### Detectors
- EC2 CPU spike detection (>95% for 10+ minutes)
- Lambda error detection (5+ errors in lookback window)
- S3 access denied errors via CloudTrail
- Bedrock token usage spikes (>100K tokens/hour)

### Infrastructure
- Python CLI tool (`copilot` command)
- Vercel serverless API endpoints:
  - `/api/scan` - Real-time AWS scanning
  - `/api/test-aws` - Credential verification
  - `/api/mock-incidents` - Demo mode
- Comprehensive test suite with >80% coverage
- CI/CD pipeline with GitHub Actions
- Security scanning with Trivy

### Security
- Read-only AWS operations
- No data persistence
- Encrypted environment variables
- Security headers (CSP, X-Frame-Options, etc.)
- Error message sanitization
- Minimal IAM permissions

## [0.2.0] - 2024-10-XX

### Added
- Initial CLI implementation
- Basic incident detection
- CloudWatch integration
- CloudTrail integration

### Changed
- Improved error handling
- Better logging

## [0.1.0] - 2024-09-XX

### Added
- Initial project structure
- Basic AWS connectivity
- Mock incident generation
- Core detector framework

---

## Version History Summary

- **1.0.0** - Production-ready web dashboard with full feature set
- **0.2.0** - CLI tool with basic detection
- **0.1.0** - Initial prototype

## Release Notes

### v1.0.0 Highlights

This release marks the first production-ready version of AWS Incident Co-Pilot!

**Major Features:**
- Beautiful web dashboard built with Next.js 14
- Real-time AWS infrastructure monitoring
- Smart incident detection with actionable recommendations
- 100% free tier compatible (designed for $0/month operation)
- Production-grade security and error handling
- Comprehensive documentation for easy deployment

**Perfect For:**
- DevOps teams monitoring AWS infrastructure
- Developers wanting visibility into their AWS resources
- Startups needing cost-effective monitoring
- Anyone who wants to catch AWS issues before they become problems

**Deploy Now:** https://vercel.com/new/clone?repository-url=https://github.com/JavierHernandezVantuyl/aws-incident-copilot

---

## Upgrade Guide

### From 0.x to 1.0.0

The 1.0.0 release introduces the web dashboard. If you're upgrading from a CLI-only version:

1. **Web Dashboard (New)**
   ```bash
   npm install
   npm run dev
   ```

2. **CLI (Still Works)**
   ```bash
   pip install -e ".[dev]"
   copilot monitor
   ```

3. **Environment Variables**
   - Add `AWS_ACCESS_KEY_ID`
   - Add `AWS_SECRET_ACCESS_KEY`
   - Add `AWS_DEFAULT_REGION` (optional)

No breaking changes to the CLI interface!

---

## Future Roadmap

See [README.md](README.md#-roadmap) for planned features.

---

[Unreleased]: https://github.com/JavierHernandezVantuyl/aws-incident-copilot/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/JavierHernandezVantuyl/aws-incident-copilot/releases/tag/v1.0.0
