# Cost Analysis & Free Tier Guide

## Overview

AWS Incident Co-Pilot is designed to be **completely free** for most users when following recommended usage patterns. This guide provides a detailed breakdown of all costs and how to stay within free tier limits.

## Executive Summary

**Estimated Monthly Cost (Typical Usage): $0.00 - $0.50**

- Vercel Hosting: **FREE** (Hobby plan)
- AWS API Calls: **FREE** (within free tier limits)
- Only cost: Occasional AWS API overages if scanning too frequently

**To stay 100% free**: Limit scans to once every 5-15 minutes.

---

## Vercel Costs

### Hobby Plan (Free)
Perfect for individual developers and small teams.

**Included:**
- ✅ Unlimited deployments
- ✅ 100 GB-hours of serverless function execution per month
- ✅ 100 GB bandwidth per month
- ✅ Automatic HTTPS
- ✅ Preview deployments for PRs
- ✅ Analytics (basic)

**What This Means:**
- **100 GB-hours** = ~10,000 function executions (assuming 10s per execution)
- **Example**: 288 scans per day (every 5 minutes) = ~8,640 scans/month
- **Verdict**: Hobby plan is MORE than enough for typical usage ✅

### Pro Plan ($20/month)
Only needed for:
- Teams with >1,000 scans per day
- Custom domains with advanced features
- Priority support

**For this application: NOT REQUIRED** ❌

### Cost Calculation Example

```
Scenario: Scan every 5 minutes, 24/7

Scans per day: 288
Scans per month: 8,640
Function execution time: ~10 seconds per scan
Total compute: 86,400 seconds = 24 GB-hours

Free tier limit: 100 GB-hours
Used: 24 GB-hours (24%)
Cost: $0.00 ✅
```

---

## AWS Costs

### Free Tier (Always Free)

These services have perpetual free tier limits:

#### 1. AWS CloudWatch
- **Free**: 10 custom metrics, 10 alarms, 1M API requests/month
- **Our Usage**: ~5-10 API requests per scan
- **Safe Rate**: Up to 100,000 scans/month
- **Verdict**: FREE for typical usage ✅

#### 2. AWS CloudTrail
- **Free**: One trail, 90-day event history
- **Our Usage**: 1 LookupEvents API call per scan
- **Cost**: FREE (no charge for first trail) ✅

#### 3. AWS STS (GetCallerIdentity)
- **Free**: Always free, unlimited usage
- **Our Usage**: 1 call per connection test
- **Cost**: $0.00 ✅

#### 4. AWS EC2 (Describe APIs)
- **Free**: All describe operations are free
- **Our Usage**: DescribeInstances calls
- **Cost**: $0.00 ✅

### Potential Costs (If Exceeding Free Tier)

#### CloudWatch API Requests
- **Free Tier**: 1,000,000 requests/month
- **After Free Tier**: $0.01 per 1,000 requests
- **Our Usage**: 5-10 requests per scan

**Example Cost Calculation:**
```
Scenario: Scan every 1 minute (aggressive)

Scans per month: 43,200
CloudWatch requests: 216,000 (5 per scan)
Free tier: 1,000,000
Billable requests: 0
Cost: $0.00 ✅

Even if you scan every 30 seconds:
Scans per month: 86,400
CloudWatch requests: 432,000
Still within free tier!
Cost: $0.00 ✅
```

#### CloudTrail Lookup Events
- **Included**: FREE with first trail
- **Additional trails**: $2.00 per 100,000 events
- **Our Usage**: 1 event per scan

**We only use the free first trail, so cost is $0.00** ✅

---

## Total Cost Breakdown

### Scenario 1: Recommended Usage (Every 5 Minutes)

| Service | Usage | Free Tier | Billable | Cost |
|---------|-------|-----------|----------|------|
| Vercel Functions | 8,640 scans/month | 100 GB-hours | 0 | $0.00 |
| CloudWatch API | 43,200 requests | 1M requests | 0 | $0.00 |
| CloudTrail | 8,640 lookups | FREE | 0 | $0.00 |
| STS | ~30 calls/month | FREE | 0 | $0.00 |
| EC2 Describe | 8,640 calls | FREE | 0 | $0.00 |
| **TOTAL** | | | | **$0.00** |

### Scenario 2: Aggressive Usage (Every 1 Minute)

| Service | Usage | Free Tier | Billable | Cost |
|---------|-------|-----------|----------|------|
| Vercel Functions | 43,200 scans/month | 100 GB-hours | 0 | $0.00 |
| CloudWatch API | 216,000 requests | 1M requests | 0 | $0.00 |
| CloudTrail | 43,200 lookups | FREE | 0 | $0.00 |
| STS | ~50 calls/month | FREE | 0 | $0.00 |
| EC2 Describe | 43,200 calls | FREE | 0 | $0.00 |
| **TOTAL** | | | | **$0.00** |

### Scenario 3: Excessive Usage (Every 10 Seconds - NOT RECOMMENDED)

| Service | Usage | Free Tier | Billable | Cost |
|---------|-------|-----------|----------|------|
| Vercel Functions | 259,200 scans/month | 100 GB-hours | ~172 GB-hours | $0.00* |
| CloudWatch API | 1,296,000 requests | 1M requests | 296,000 | $2.96 |
| CloudTrail | 259,200 lookups | FREE | 0 | $0.00 |
| **TOTAL** | | | | **~$2.96** |

*Vercel Free tier may throttle at this rate. Consider Pro plan ($20) if needed.

---

## Cost Control Features

### Built-In Cost Protections

1. **30-Second Scan Cooldown**
   - Enforced in the UI
   - Prevents accidental rapid scanning
   - Keeps you well within free tier

2. **Recommended Scan Interval: 5 Minutes**
   - Displayed in UI cost banner
   - Optimal balance of monitoring and cost
   - 100% free tier compliant

3. **Cost Information in API Responses**
   - Every scan response includes cost estimates
   - Real-time awareness of usage
   - Recommendations for optimization

### How to Monitor Your Costs

#### AWS Cost Explorer
```bash
# Enable Cost Explorer (one-time setup)
# Go to AWS Console → Billing → Cost Explorer

# View costs by service
# Filter by: CloudWatch, CloudTrail, EC2
```

#### AWS Billing Alerts
```bash
# Set up billing alarm
aws cloudwatch put-metric-alarm \
  --alarm-name aws-budget-alert \
  --alarm-description "Alert when AWS bill exceeds $1" \
  --metric-name EstimatedCharges \
  --namespace AWS/Billing \
  --statistic Maximum \
  --period 21600 \
  --threshold 1 \
  --comparison-operator GreaterThanThreshold
```

#### Vercel Analytics
- Go to Vercel Dashboard → Your Project → Analytics
- Monitor function invocations
- Check bandwidth usage
- View execution time

---

## Optimization Tips

### To Minimize Costs

1. **Use Recommended Scan Interval**
   - Scan every 5-15 minutes instead of continuously
   - Still catches most issues quickly
   - Stays well within free tier

2. **Disable Continuous Monitoring When Not Needed**
   - Use manual "Scan Now" for ad-hoc checks
   - Enable continuous monitoring only during critical periods
   - Turn off overnight if not needed

3. **Leverage Caching** (Future Enhancement)
   - Cache API responses for 1-2 minutes
   - Reduces duplicate API calls
   - No change to user experience

4. **Monitor Only Critical Resources**
   - Focus on production resources
   - Skip development/testing environments
   - Reduces CloudWatch API calls

### Free Tier Maximization

**Current Usage Estimate:**
- 8,640 scans/month (every 5 min) uses only 4.3% of CloudWatch free tier
- You have 95.7% headroom!

**Maximum Free Scans:**
```
CloudWatch free tier: 1M requests/month
Requests per scan: 5-10
Max scans: 100,000 - 200,000/month

That's one scan every 13-26 seconds!
(Not recommended, but technically free)
```

---

## Cost Comparison

### vs. Other Monitoring Solutions

| Solution | Monthly Cost | Setup Time | Features |
|----------|--------------|------------|----------|
| **AWS Incident Co-Pilot** | **$0.00** | 10 min | Automated detection, free tier |
| AWS CloudWatch Alarms | $0.10-$1.00 per alarm | 2 hours | Manual setup, per-alarm cost |
| Third-party SaaS | $50-$200/month | 30 min | More features, but expensive |
| Custom Scripts | $0.00 | 8+ hours | DIY, time-consuming |

**AWS Incident Co-Pilot offers the best value** ✅

---

## FAQ

### Q: Will I be charged for using this application?

**A:** Not if you follow recommended usage (scan every 5-15 minutes). The application is designed to stay within AWS and Vercel free tiers.

### Q: What if I exceed the free tier?

**A:** AWS will automatically start billing you, but costs are minimal:
- CloudWatch: $0.01 per 1,000 requests
- Would need 100,000+ scans/month to incur charges
- Built-in 30-second cooldown prevents this

### Q: How much does Vercel cost?

**A:** $0/month on Hobby plan (sufficient for this application)
- Pro plan ($20/month) only needed for teams or custom domains

### Q: Can I reduce costs further?

**A:** Yes! Adjust scan frequency:
- Every 5 min: FREE
- Every 10 min: FREE
- Every 15 min: FREE
- Manual only: FREE

All options stay within free tier.

### Q: What's the cost of the dashboard itself?

**A:** Zero. The Next.js frontend is static and included in Vercel's free hosting.

### Q: Are there any hidden costs?

**A:** No hidden costs. The only costs are:
1. AWS API calls (free tier eligible)
2. Vercel hosting (free tier)

Both are transparent and trackable.

### Q: What if my AWS account doesn't have a free tier?

**A:** AWS free tier is available to all accounts for 12 months after signup. After that:
- CloudWatch: $0.01 per 1,000 requests = ~$0.43/month for recommended usage
- Still very affordable!

---

## Billing Breakdown by Usage Pattern

### Conservative (Scan every 15 minutes)
```
Monthly scans: 2,880
Vercel cost: $0.00
AWS cost: $0.00
Total: $0.00 ✅
```

### Recommended (Scan every 5 minutes)
```
Monthly scans: 8,640
Vercel cost: $0.00
AWS cost: $0.00
Total: $0.00 ✅
```

### Moderate (Scan every 2 minutes)
```
Monthly scans: 21,600
Vercel cost: $0.00
AWS cost: $0.00
Total: $0.00 ✅
```

### Aggressive (Scan every 30 seconds)
```
Monthly scans: 86,400
Vercel cost: $0.00
AWS cost: $0.00
Total: $0.00 ✅

Note: Still within free tier!
```

---

## Cost Transparency Commitment

We believe in complete cost transparency:

1. **All costs shown in UI** - Dashboard displays cost info on every scan
2. **Real-time estimates** - API responses include cost calculations
3. **Recommendations** - UI suggests optimal scan frequency
4. **No surprise charges** - Built-in cooldowns prevent excess usage

## Support & Questions

If you have questions about costs or see unexpected charges:

1. Check AWS Cost Explorer
2. Review Vercel analytics
3. Verify scan frequency in dashboard
4. Check for other AWS applications using same account

---

## Conclusion

**AWS Incident Co-Pilot is designed to be FREE.**

- ✅ Vercel hosting: FREE
- ✅ AWS API calls: FREE (within generous limits)
- ✅ No hidden costs
- ✅ Transparent pricing
- ✅ Built-in cost controls

**Recommended action:** Use the default 5-minute scan interval and enjoy free, automated AWS monitoring!

---

**Last updated:** November 2024
**Next review:** February 2025

*Costs subject to change based on AWS and Vercel pricing. Always verify current pricing on respective provider websites.*
