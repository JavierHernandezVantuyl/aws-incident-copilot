# AWS Incident Co-Pilot 🚀

<div align="center">

![AWS Incident Co-Pilot Logo](https://img.shields.io/badge/AWS-Incident_Co--Pilot-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white)

**Monitor your AWS infrastructure and respond to incidents automatically - no DevOps experience required!**

[![CI Status](https://img.shields.io/github/actions/workflow/status/JavierHernandezVantuyl/aws-incident-copilot/ci.yml?branch=main&style=flat-square&label=CI)](https://github.com/JavierHernandezVantuyl/aws-incident-copilot/actions)
[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org)
[![Next.js](https://img.shields.io/badge/Next.js-14-black?style=flat-square&logo=next.js)](https://nextjs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue?style=flat-square&logo=typescript&logoColor=white)](https://www.typescriptlang.org)
[![Vercel](https://img.shields.io/badge/Deploy-Vercel-black?style=flat-square&logo=vercel)](https://vercel.com)
[![Cost](https://img.shields.io/badge/Cost-FREE-success?style=flat-square&logo=aws-lambda)](COST.md)
[![Security](https://img.shields.io/badge/Security-Production_Ready-green?style=flat-square&logo=security)](SECURITY.md)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)

[Quick Start](#-quick-start) •
[Features](#-features) •
[Deploy](#-deployment-options) •
[Documentation](#-documentation) •
[Security](#-security) •
[Contributing](#-contributing) •
[Changelog](CHANGELOG.md)

</div>

---

<div align="center">

### 🎉 Get Started in 2 Minutes

```bash
# Option 1: Deploy to Vercel (Recommended)
# Click the button above ↑

# Option 2: Run Locally
pip install -e . && copilot setup && copilot monitor
```

**No credit card required** • **100% Free Tier** • **Production Ready**

</div>

---

## 🎯 What Does This Do?

AWS Incident Co-Pilot is like having a **24/7 DevOps assistant** for your AWS infrastructure. It automatically:

- 🔍 **Scans** your AWS account for problems (EC2, Lambda, S3, Bedrock)
- 🚨 **Alerts** you when something goes wrong
- 📝 **Collects evidence** to help you fix issues faster
- 💡 **Suggests fixes** with actionable recommendations
- 💰 **Stays FREE** - designed for AWS free tier

> **Perfect for:** Developers, DevOps teams, startups, and anyone managing AWS infrastructure!

### ⚡ Key Highlights

| Feature | Benefit |
|---------|---------|
| **🚀 5-Minute Setup** | Deploy to Vercel with one click - no complex configuration |
| **💰 100% Free** | Stays within AWS & Vercel free tiers - $0/month for typical usage |
| **🔒 Production Security** | Read-only operations, encrypted credentials, security headers |
| **📊 Beautiful UI** | Modern Next.js dashboard - monitor from anywhere |
| **🤖 Smart Detection** | AI-powered incident detection with actionable recommendations |
| **📚 Complete Docs** | Step-by-step guides for every deployment scenario |

---

## ✨ Features

### 🌐 Web Dashboard (Production-Ready!)
- **Beautiful, Modern UI** - Built with Next.js and Tailwind CSS
- **Real-Time Monitoring** - See incidents as they happen
- **Cost Awareness** - Built-in cost controls and warnings
- **Mobile Responsive** - Monitor from anywhere
- **30-Second Cooldown** - Prevents excessive AWS API costs
- **Professional Security** - Production-grade security headers

### 🔍 Smart Detection
Automatically finds common AWS issues:
- **EC2 CPU Spikes** - High CPU usage for 10+ minutes
- **Lambda Errors** - Function failures and timeouts
- **S3 Access Denied** - Permission errors
- **Bedrock Token Spikes** - Excessive API usage ($$ warning!)
- **DynamoDB Throttling** - Coming soon!

### 💰 Cost Optimized
- **$0.00/month** for typical usage (stays within free tiers)
- **Vercel Free Tier** - 100GB-hours/month included
- **AWS Free Tier** - 1M CloudWatch requests/month
- **Built-in Rate Limiting** - 30-second scan cooldown
- **Transparent Pricing** - Cost estimates in every response

### 🔒 Production Security
- **Read-Only Operations** - Never modifies your AWS infrastructure
- **No Data Persistence** - Nothing stored on servers
- **Security Headers** - X-Frame-Options, CSP, etc.
- **Error Sanitization** - No sensitive data in error messages
- **IAM Best Practices** - Minimal permissions required

[📖 Read Full Security Policy](SECURITY.md)

---

## 🚀 Quick Start

### Option 1: Web Dashboard (Recommended)

**Deploy to Vercel in 5 minutes:**

1. **Click to Deploy**

   [![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/JavierHernandezVantuyl/aws-incident-copilot&project-name=aws-incident-copilot&env=AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY,AWS_DEFAULT_REGION)

2. **Add Environment Variables** (in Vercel dashboard):
   ```bash
   AWS_ACCESS_KEY_ID=your_aws_key
   AWS_SECRET_ACCESS_KEY=your_aws_secret
   AWS_DEFAULT_REGION=us-east-1
   ```

3. **Deploy and Access** your dashboard!

**[📖 Detailed Deployment Guide](VERCEL_DEPLOYMENT.md)** | **[🔐 Get AWS Credentials](SECURITY.md#recommended-iam-policy)**

### Option 2: Command Line

```bash
# 1. Install (requires Python 3.9+)
pip install -e .

# 2. Configure AWS credentials
copilot setup

# 3. Start monitoring!
copilot monitor
```

---

## 📊 Dashboard Preview

```
┌─────────────────────────────────────────────────────────────┐
│  AWS Incident Co-Pilot        ✓ AWS Connected              │
├─────────────────────────────────────────────────────────────┤
│  💵 Cost: $0.00/month (Free Tier) | Limit: 5-min intervals │
│  ────────────────────────────────────────────────────────── │
│  [⚡ Scan Now]  [▶ Start Monitoring]  [🔍 Test Connection] │
│  ────────────────────────────────────────────────────────── │
│  📊 Stats:  0 Total  |  0 Critical  |  0 High  |  0 Medium │
│  ────────────────────────────────────────────────────────── │
│  ✓ No incidents detected                                   │
│    Your AWS infrastructure is running smoothly!             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎨 Features in Detail

### Incident Detection

| Incident Type | Detection Logic | Severity | Cost Impact |
|--------------|----------------|----------|-------------|
| **EC2 CPU Spike** | CPU > 95% for 10+ min | MEDIUM-HIGH | Minimal |
| **Lambda Errors** | 5+ errors in lookback window | MEDIUM-HIGH | Minimal |
| **S3 Access Denied** | AccessDenied in CloudTrail | HIGH | None |
| **Bedrock Token Spike** | >100K tokens/hour | HIGH | ⚠️ **$2-5/hour** |

### Smart Recommendations

Each incident includes actionable recommendations:

```json
{
  "title": "EC2 CPU Spike Detected",
  "recommendations": [
    "Check application logs for unusual activity",
    "Consider scaling up instance size",
    "Review recent deployments"
  ],
  "cost_impact": null
}
```

---

## 💰 Cost Transparency

### Monthly Cost Breakdown

| Service | Free Tier | Typical Usage | Cost |
|---------|-----------|---------------|------|
| Vercel Hosting | 100GB-hours | ~24GB-hours | **$0.00** |
| AWS CloudWatch | 1M requests | ~43K requests | **$0.00** |
| AWS CloudTrail | 1 trail free | 1 trail | **$0.00** |
| **TOTAL** | | | **$0.00** ✅ |

**Recommended:** Scan every 5-15 minutes to stay 100% free.

**[📊 Detailed Cost Analysis](COST.md)**

---

## 📚 Documentation

### Quick Links
- **[🌐 Vercel Deployment](VERCEL_DEPLOYMENT.md)** - Step-by-step deployment guide
- **[💰 Cost Analysis](COST.md)** - Complete cost breakdown
- **[🔐 Security Policy](SECURITY.md)** - Security best practices
- **[✅ Production Checklist](PRODUCTION_READY.md)** - Deployment verification
- **[📖 Quick Start (Web)](QUICKSTART_WEB.md)** - Local development
- **[📖 Quick Start (CLI)](QUICKSTART.md)** - Command-line usage

### Architecture

```
aws-incident-copilot/
├── app/                    # Next.js web dashboard
│   ├── page.tsx           # Main dashboard component
│   ├── types.ts           # TypeScript definitions
│   └── globals.css        # Tailwind styles
├── api/                   # Python serverless functions
│   ├── scan.py           # Scan AWS for incidents
│   ├── test-aws.py       # Test AWS connectivity
│   └── mock-incidents.py # Demo data
├── copilot/               # Python CLI package
│   ├── sources/          # CloudWatch, CloudTrail
│   ├── detectors/        # Incident detection logic
│   ├── evidence.py       # Evidence collection
│   └── alerts.py         # Alerting system
└── tests/                 # Comprehensive test suite
```

---

## 🔒 Security

### Security Highlights
✅ **Read-Only AWS Operations** - Never modifies your infrastructure
✅ **No Data Persistence** - Nothing stored on servers
✅ **Encrypted Credentials** - Vercel encrypts environment variables
✅ **Security Headers** - Production-grade HTTP headers
✅ **Minimal IAM Permissions** - Least-privilege access
✅ **Error Sanitization** - No sensitive data exposure

### Recommended IAM Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": [
      "cloudwatch:GetMetricStatistics",
      "cloudwatch:ListMetrics",
      "cloudtrail:LookupEvents",
      "ec2:DescribeInstances",
      "sts:GetCallerIdentity"
    ],
    "Resource": "*"
  }]
}
```

**[🔐 Full Security Documentation](SECURITY.md)**

---

## 🚀 Deployment Options

### 🌐 Option 1: Vercel (Recommended for Teams)

**Best for:** Web dashboard, teams, visual monitoring

```bash
# One-click deploy
vercel --prod
```

**Pros:**
- Beautiful web UI
- Free hosting
- Automatic HTTPS
- No server management
- Mobile friendly

**[📖 Deploy to Vercel](VERCEL_DEPLOYMENT.md)**

### 💻 Option 2: CLI (Recommended for Automation)

**Best for:** Scripts, CI/CD, automation

```bash
# Install
pip install -e .

# Run once
copilot monitor

# Continuous monitoring
copilot monitor --continuous

# With alerts
copilot monitor --continuous --alerts
```

**Pros:**
- Works in scripts
- No web UI needed
- Direct AWS access
- Full CLI control

**[📖 CLI Quick Start](QUICKSTART.md)**

---

## 🧪 Development

### Local Setup

```bash
# Clone repository
git clone https://github.com/JavierHernandezVantuyl/aws-incident-copilot.git
cd aws-incident-copilot

# Install Python dependencies
pip install -e ".[dev]"

# Install Node.js dependencies
npm install

# Run web dashboard locally
npm run dev
# Visit http://localhost:3000

# Run Python tests
pytest -v --cov=copilot

# Run Next.js build
npm run build
```

### Testing

```bash
# Python tests with coverage
pytest -v --cov=copilot --cov-report=html

# Lint Python code
ruff check .
black --check .

# Lint Next.js code
npm run lint

# Type checking
npx tsc --noEmit
```

---

## 🤝 Contributing

We love contributions! Here's how you can help make this project even better:

[![Code of Conduct](https://img.shields.io/badge/Code%20of%20Conduct-Contributor%20Covenant-purple.svg?style=flat-square)](CODE_OF_CONDUCT.md)

**Please read our [Contributing Guide](CONTRIBUTING.md) and [Code of Conduct](CODE_OF_CONDUCT.md) before getting started.**

### 🌟 Ways to Contribute

- **⭐ Star this repo** - Show your support and help others discover it!
- **🐛 Report bugs** - Found an issue? [Open a bug report](https://github.com/JavierHernandezVantuyl/aws-incident-copilot/issues/new)
- **💡 Suggest features** - Have an idea? [Share it with us](https://github.com/JavierHernandezVantuyl/aws-incident-copilot/issues/new)
- **📖 Improve docs** - Help make our documentation even better
- **🔧 Submit PRs** - Fix bugs or add new features

### 🚀 Quick Contribution Guide

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Add** tests for new functionality
4. **Run** tests (`pytest`, `npm run build`)
5. **Format** code (`black .`, `npm run lint`)
6. **Commit** with clear messages (`git commit -m 'Add amazing feature'`)
7. **Push** to your branch (`git push origin feature/amazing-feature`)
8. **Open** a Pull Request

### 📋 Development Guidelines

- **Python:** Follow PEP 8, use type hints
- **TypeScript:** Strict mode, full type safety
- **Security:** Never expose credentials
- **Tests:** Maintain >80% coverage
- **Documentation:** Update docs for new features

### 🏅 Contributors

Thank you to all our contributors! Every contribution, no matter how small, is valued and appreciated.

[![Contributors](https://img.shields.io/github/contributors/JavierHernandezVantuyl/aws-incident-copilot?style=for-the-badge)](https://github.com/JavierHernandezVantuyl/aws-incident-copilot/graphs/contributors)

---

## 📝 Roadmap

- [x] ✅ Web UI dashboard
- [x] ✅ Vercel deployment support
- [x] ✅ Production-ready security
- [x] ✅ Cost optimization features
- [x] ✅ TypeScript types
- [x] ✅ Comprehensive documentation
- [ ] DynamoDB throttling detection
- [ ] RDS connection monitoring
- [ ] API Gateway error tracking
- [ ] Slack/Teams integration
- [ ] Custom detection rules
- [ ] Historical incident tracking
- [ ] Multi-account support
- [ ] Automated remediation

---

## 🏆 Why Choose AWS Incident Co-Pilot?

| Feature | AWS Incident Co-Pilot | CloudWatch Alarms | Third-Party SaaS |
|---------|----------------------|-------------------|------------------|
| **Cost** | **FREE** | $0.10+ per alarm | $50-200/month |
| **Setup Time** | 5 minutes | 2+ hours | 30 minutes |
| **Web Dashboard** | ✅ Included | ❌ Manual | ✅ Included |
| **Smart Recommendations** | ✅ Yes | ❌ No | ✅ Yes |
| **Open Source** | ✅ MIT License | ❌ Proprietary | ❌ Proprietary |
| **Self-Hosted** | ✅ Optional | N/A | ❌ No |

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built with [Next.js](https://nextjs.org/), [React](https://react.dev/), and [Tailwind CSS](https://tailwindcss.com/)
- Powered by [AWS SDK (boto3)](https://aws.amazon.com/sdk-for-python/)
- Deployed on [Vercel](https://vercel.com)
- CLI framework: [Typer](https://typer.tiangolo.com/)

---

## 💬 Support & Questions

- **📖 Documentation:** Check the [docs folder](.)
- **🐛 Bug Reports:** [Open an issue](https://github.com/JavierHernandezVantuyl/aws-incident-copilot/issues)
- **💡 Feature Requests:** [Open an issue](https://github.com/JavierHernandezVantuyl/aws-incident-copilot/issues)
- **🔒 Security Issues:** See [SECURITY.md](SECURITY.md)

---

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/JavierHernandezVantuyl/aws-incident-copilot?style=social)
![GitHub forks](https://img.shields.io/github/forks/JavierHernandezVantuyl/aws-incident-copilot?style=social)
![GitHub issues](https://img.shields.io/github/issues/JavierHernandezVantuyl/aws-incident-copilot)
![GitHub pull requests](https://img.shields.io/github/issues-pr/JavierHernandezVantuyl/aws-incident-copilot)

---

## ⭐ Show Your Support

If you find AWS Incident Co-Pilot useful, please consider:

<div align="center">

### ⭐ **Star this repository** ⭐

Starring helps others discover this project and motivates us to keep improving it!

[![Star History Chart](https://api.star-history.com/svg?repos=JavierHernandezVantuyl/aws-incident-copilot&type=Date)](https://star-history.com/#JavierHernandezVantuyl/aws-incident-copilot&Date)

</div>

### 🎉 Other Ways to Support

- **Share** this project with colleagues and on social media
- **Contribute** by submitting pull requests
- **Sponsor** future development (coming soon)
- **Provide feedback** to help us improve

---

<div align="center">

**Made with ❤️ for the DevOps community**

**Free • Open Source • Production Ready**

<br />

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/JavierHernandezVantuyl/aws-incident-copilot)

<br />

[🚀 Deploy Now](https://vercel.com/new/clone?repository-url=https://github.com/JavierHernandezVantuyl/aws-incident-copilot) • [📖 Documentation](VERCEL_DEPLOYMENT.md) • [🐛 Report Bug](https://github.com/JavierHernandezVantuyl/aws-incident-copilot/issues) • [💡 Request Feature](https://github.com/JavierHernandezVantuyl/aws-incident-copilot/issues)

<br />

**Copyright © 2024 AWS Incident Co-Pilot Contributors**

Licensed under [MIT License](LICENSE)

</div>
