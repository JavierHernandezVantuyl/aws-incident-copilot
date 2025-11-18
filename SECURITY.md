# Security Policy

## Overview

AWS Incident Co-Pilot is designed with security as a top priority. This document outlines our security practices, recommendations, and how to report vulnerabilities.

## Security Principles

1. **Read-Only Operations**: All AWS API calls are read-only. The application NEVER modifies your AWS infrastructure.
2. **No Data Persistence**: No incident data or AWS credentials are stored on Vercel servers. All data is processed in-memory and discarded after each request.
3. **Minimal Permissions**: The application requests only the minimum IAM permissions required for incident detection.
4. **Secure Communications**: All traffic uses HTTPS encryption.
5. **Input Validation**: All API inputs are validated and sanitized.
6. **Error Handling**: Error messages are sanitized to prevent information disclosure.

## Recommended IAM Policy

Use this least-privilege IAM policy for the AWS credentials:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "IncidentCopilotReadOnly",
      "Effect": "Allow",
      "Action": [
        "cloudwatch:GetMetricStatistics",
        "cloudwatch:ListMetrics",
        "cloudwatch:DescribeAlarms",
        "cloudtrail:LookupEvents",
        "ec2:DescribeInstances",
        "ec2:DescribeInstanceStatus",
        "lambda:ListFunctions",
        "lambda:GetFunction",
        "sts:GetCallerIdentity"
      ],
      "Resource": "*"
    }
  ]
}
```

### Alternative: AWS Managed Policies

For convenience, you can use these AWS managed policies (but they grant more permissions than necessary):
- `CloudWatchReadOnlyAccess`
- `AWSCloudTrailReadOnlyAccess`
- `AmazonEC2ReadOnlyAccess`

## Vercel Environment Variables

### Required Variables
- `AWS_ACCESS_KEY_ID` - AWS access key (encrypted by Vercel)
- `AWS_SECRET_ACCESS_KEY` - AWS secret key (encrypted by Vercel)
- `AWS_DEFAULT_REGION` - AWS region (not sensitive)

### Optional Variables
- `ALLOWED_ORIGIN` - Restrict CORS to specific domain (default: `*`)

**IMPORTANT**: Vercel encrypts all environment variables. They are only decrypted during function execution and are never logged or exposed.

## Credential Security

### DO ✅
- Use dedicated IAM user for this application
- Rotate access keys every 90 days
- Enable AWS CloudTrail to audit API calls
- Use read-only permissions only
- Set up AWS billing alerts
- Review Vercel function logs regularly
- Use Vercel's encrypted environment variables

### DON'T ❌
- Share AWS credentials in code or Git
- Use root AWS account credentials
- Grant write permissions (EC2:Terminate*, etc.)
- Commit `.env` files to version control
- Use the same credentials across multiple applications
- Store credentials in plaintext anywhere

## Security Headers

The application sets these security headers on all responses:

```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Cache-Control: no-store, no-cache, must-revalidate, private
```

## CORS Policy

By default, CORS is set to `*` (allow all origins) for ease of development.

**For production**, restrict CORS by setting the `ALLOWED_ORIGIN` environment variable:

```bash
ALLOWED_ORIGIN=https://your-dashboard.vercel.app
```

## Data Privacy

### Data NOT Collected or Stored
- AWS credentials
- Incident details
- CloudWatch metrics
- CloudTrail events
- User identifiers

### Data Temporarily Processed (in-memory only)
- AWS API responses (discarded after each request)
- Incident detection results (sent to client, not stored)

### Vercel Logs
Vercel automatically logs:
- HTTP request metadata (timestamp, status code, duration)
- Console output from serverless functions
- Error stack traces

**Note**: Vercel logs are retained for 1 hour on Free tier, 7 days on Pro tier.

## Vulnerability Disclosure

### Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly:

1. **DO NOT** create a public GitHub issue
2. Email the maintainer privately (check GitHub profile for contact)
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if applicable)

### Response Timeline

- **24 hours**: Initial acknowledgment
- **7 days**: Assessment and severity classification
- **30 days**: Fix development and testing
- **Public disclosure**: After fix is deployed and users have time to update

## Security Audit

Last security review: November 2024

### Recent Security Improvements
- Added input validation for all API endpoints
- Implemented error message sanitization
- Added security headers
- Implemented rate limiting awareness (30s cooldown)
- Added credential placeholder detection
- Removed sensitive data from error responses

## Third-Party Dependencies

### Python Dependencies
- `boto3` - Official AWS SDK (maintained by AWS)
- `typer` - CLI framework
- `rich` - Terminal formatting
- `pydantic` - Data validation

All dependencies are scanned for vulnerabilities during CI/CD.

### JavaScript Dependencies
- `next` - Next.js framework (Vercel)
- `react` - React library
- `tailwindcss` - CSS framework
- `lucide-react` - Icon library

Run `npm audit` regularly to check for vulnerabilities.

## CI/CD Security

GitHub Actions workflow includes:
- Dependency vulnerability scanning
- Static code analysis
- Linting and type checking
- Automated tests

### Security Scanning
We use Trivy for vulnerability scanning:
- Scans all dependencies
- Checks for known CVEs
- Reports to GitHub Security tab

## Incident Response

If AWS credentials are compromised:

1. **Immediate Actions**
   - Disable/delete the compromised IAM access key in AWS Console
   - Remove credentials from Vercel environment variables
   - Review AWS CloudTrail for unauthorized activity
   - Check AWS billing for unexpected charges

2. **Investigation**
   - Review Vercel function logs
   - Check Git history for exposed credentials
   - Audit all AWS API calls made with compromised credentials

3. **Recovery**
   - Create new IAM user with fresh credentials
   - Update Vercel environment variables
   - Redeploy application
   - Enable AWS CloudTrail if not already enabled
   - Set up AWS billing alerts

## Compliance

### Data Residency
- Application runs on Vercel infrastructure (US by default)
- Can be configured for other regions via Vercel settings
- No data is persisted beyond request lifetime

### Regulatory Compliance
This application:
- Does not collect PII (Personally Identifiable Information)
- Does not store data persistently
- Uses encrypted communications (HTTPS)
- Implements least-privilege access

## Best Practices for Users

1. **Use Dedicated IAM User**
   ```bash
   # Create dedicated user
   aws iam create-user --user-name incident-copilot

   # Attach read-only policy
   aws iam attach-user-policy \
     --user-name incident-copilot \
     --policy-arn arn:aws:iam::aws:policy/CloudWatchReadOnlyAccess
   ```

2. **Enable MFA on AWS Account**
   - Even with read-only permissions, enable MFA for defense in depth

3. **Monitor IAM User Activity**
   ```bash
   # Check recent activity
   aws cloudtrail lookup-events \
     --lookup-attributes AttributeKey=Username,AttributeValue=incident-copilot
   ```

4. **Set Up Billing Alerts**
   ```bash
   # Create billing alarm
   aws cloudwatch put-metric-alarm \
     --alarm-name high-billing \
     --alarm-description "Alert on high AWS bill" \
     --metric-name EstimatedCharges \
     --namespace AWS/Billing \
     --threshold 10
   ```

5. **Regular Security Audits**
   - Review IAM access keys monthly
   - Rotate credentials quarterly
   - Audit CloudTrail logs for unusual activity
   - Review Vercel function logs

## Additional Resources

- [AWS IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [Vercel Security](https://vercel.com/docs/security/secure-coding)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

## Contact

For security concerns, please contact the maintainer through GitHub.

---

**This security policy is reviewed quarterly and updated as needed.**

Last updated: November 2024
