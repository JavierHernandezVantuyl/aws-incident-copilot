# 🚀 Deploying AWS Incident Co-Pilot to Vercel

This guide will walk you through deploying AWS Incident Co-Pilot to Vercel, even if you've never used Vercel before!

## What is Vercel?

Vercel is a cloud platform that makes it incredibly easy to deploy web applications. It's free to get started and handles all the infrastructure for you - no server management needed!

## Prerequisites

Before you begin, make sure you have:

1. **AWS Account** with credentials (Access Key ID and Secret Access Key)
2. **GitHub Account** (free at [github.com](https://github.com))
3. **Vercel Account** (free at [vercel.com](https://vercel.com))

## Step-by-Step Deployment Guide

### Step 1: Create a Vercel Account

1. Go to [vercel.com](https://vercel.com)
2. Click **"Sign Up"**
3. Choose **"Continue with GitHub"** (easiest option)
4. Authorize Vercel to access your GitHub account

**That's it!** You now have a Vercel account.

---

### Step 2: Push Your Code to GitHub

If you haven't already pushed this project to GitHub:

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit your changes
git commit -m "Initial commit: AWS Incident Co-Pilot"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR-USERNAME/aws-incident-copilot.git
git push -u origin main
```

**Note:** Replace `YOUR-USERNAME` with your GitHub username.

---

### Step 3: Import Your Project to Vercel

1. **Log in to Vercel** at [vercel.com](https://vercel.com)

2. **Click "Add New..."** in the top right corner

3. **Select "Project"**

4. **Import from GitHub:**
   - You'll see a list of your GitHub repositories
   - Find `aws-incident-copilot` and click **"Import"**

5. **Configure Your Project:**
   - **Project Name:** `aws-incident-copilot` (or whatever you prefer)
   - **Framework Preset:** Next.js (should auto-detect)
   - **Root Directory:** `./` (leave as default)
   - **Build Command:** `npm run build` (should be auto-filled)
   - **Output Directory:** `.next` (should be auto-filled)

6. **Click "Deploy"** (don't worry about environment variables yet!)

**Your app will deploy in about 2-3 minutes!** ⏱️

---

### Step 4: Add AWS Credentials (Environment Variables)

After your first deployment completes:

1. **Go to your project dashboard** on Vercel

2. **Click "Settings"** tab at the top

3. **Click "Environment Variables"** in the left sidebar

4. **Add these required variables:**

   | Name | Value | Environment |
   |------|-------|-------------|
   | `AWS_ACCESS_KEY_ID` | Your AWS Access Key | Production, Preview, Development |
   | `AWS_SECRET_ACCESS_KEY` | Your AWS Secret Key | Production, Preview, Development |
   | `AWS_DEFAULT_REGION` | `us-east-1` (or your preferred region) | Production, Preview, Development |

   **How to add each variable:**
   - Type the **Name** (e.g., `AWS_ACCESS_KEY_ID`)
   - Type the **Value** (your actual AWS credential)
   - Check all boxes: **Production**, **Preview**, **Development**
   - Click **"Save"**

5. **Optional: Add configuration variables** (recommended defaults are already set):

   | Name | Value | Description |
   |------|-------|-------------|
   | `COPILOT_LOOKBACK_MINUTES` | `60` | How far back to check for incidents |
   | `COPILOT_EC2_CPU_THRESHOLD` | `95.0` | CPU percentage to trigger alert |
   | `COPILOT_LAMBDA_ERROR_THRESHOLD` | `5` | Number of errors to trigger alert |

---

### Step 5: Redeploy with Environment Variables

After adding environment variables:

1. **Go to the "Deployments"** tab
2. **Click the three dots (•••)** on the latest deployment
3. **Click "Redeploy"**
4. **Click "Redeploy"** again to confirm

**Wait 2-3 minutes** for the redeployment to complete.

---

### Step 6: Access Your Application! 🎉

1. Once deployment is complete, you'll see a **"Visit"** button
2. Click it to open your AWS Incident Co-Pilot dashboard!

Your app will be available at: `https://your-project-name.vercel.app`

---

## Getting Your AWS Credentials

If you don't have AWS credentials yet:

### Option 1: Using AWS IAM Console (Recommended)

1. **Log in to AWS Console:** [console.aws.amazon.com](https://console.aws.amazon.com)

2. **Navigate to IAM:**
   - Search for "IAM" in the top search bar
   - Click "IAM" (Identity and Access Management)

3. **Create a New User:**
   - Click "Users" in the left sidebar
   - Click "Create user"
   - Username: `incident-copilot-user`
   - Click "Next"

4. **Set Permissions:**
   - Select "Attach policies directly"
   - Search for and select:
     - `CloudWatchReadOnlyAccess`
     - `AWSCloudTrailReadOnlyAccess`
     - `AmazonEC2ReadOnlyAccess`
   - Click "Next"
   - Click "Create user"

5. **Create Access Key:**
   - Click on the user you just created
   - Click "Security credentials" tab
   - Scroll to "Access keys"
   - Click "Create access key"
   - Select "Application running outside AWS"
   - Click "Next"
   - (Optional) Add description: "Vercel Deployment"
   - Click "Create access key"

6. **Save Your Credentials:**
   - ⚠️ **IMPORTANT:** Copy both the **Access Key ID** and **Secret Access Key**
   - You won't be able to see the Secret Access Key again!
   - Consider downloading the CSV file as a backup

### Option 2: Using AWS CLI (For Advanced Users)

If you already have AWS CLI configured:

```bash
# View your credentials
cat ~/.aws/credentials

# Or use AWS CLI to get caller identity
aws sts get-caller-identity
```

---

## Troubleshooting

### "AWS credentials not configured" error

**Solution:**
- Make sure you added the environment variables in Vercel
- Redeploy after adding them
- Check that you selected all three environments (Production, Preview, Development)

### "Access Denied" errors

**Solution:**
- Verify your IAM user has the required permissions:
  - CloudWatch read access
  - CloudTrail read access
  - EC2 read access

### Deployment failed

**Solution:**
1. Check the deployment logs in Vercel
2. Make sure all files are committed to GitHub
3. Verify `package.json` and `requirements.txt` are present

### Python API routes not working

**Solution:**
- Vercel automatically detects Python files in the `/api` folder
- Make sure `requirements.txt` is in the root directory
- Check deployment logs for Python-specific errors

---

## Updating Your Deployment

Whenever you make changes to your code:

```bash
# Commit your changes
git add .
git commit -m "Your change description"

# Push to GitHub
git push
```

**Vercel will automatically redeploy!** 🚀

You'll get a notification when the deployment is complete.

---

## Advanced Configuration

### Custom Domain

Want to use your own domain (e.g., `incidents.yourcompany.com`)?

1. Go to **Settings** > **Domains**
2. Click **"Add"**
3. Enter your domain name
4. Follow the DNS configuration instructions

### Automatic Monitoring

To enable continuous monitoring:

1. The web UI has a "Start Continuous Monitoring" button
2. This will scan every 5 minutes while the page is open
3. For true background monitoring, consider using:
   - AWS Lambda with scheduled CloudWatch Events
   - A dedicated monitoring server
   - Vercel Cron Jobs (available on Pro plan)

### Alerts

To enable email/SNS alerts, add these environment variables:

```
COPILOT_ENABLE_ALERTING=true
COPILOT_SNS_TOPIC_ARN=arn:aws:sns:us-east-1:123456789012:incident-alerts
COPILOT_ALERT_EMAIL=alerts@example.com
```

---

## Security Best Practices

1. **Never commit AWS credentials to Git**
   - Always use environment variables
   - The `.gitignore` file is already configured to prevent this

2. **Use IAM permissions wisely**
   - Only grant read-only access
   - Follow the principle of least privilege

3. **Rotate credentials regularly**
   - Update your AWS access keys every 90 days
   - Update them in Vercel environment variables

4. **Monitor Vercel usage**
   - Check your Vercel dashboard for unusual activity
   - Set up billing alerts

---

## Cost Information

### Vercel Costs

- **Hobby Plan (Free):**
  - Unlimited deployments
  - 100 GB bandwidth/month
  - Serverless function execution limits
  - **Perfect for personal use or small teams!**

- **Pro Plan ($20/month):**
  - Higher limits
  - Advanced features
  - Custom domains

### AWS Costs

- **CloudWatch:** ~$0.30/month for basic monitoring
- **CloudTrail:** Usually free for single trail
- **API calls:** Minimal cost (fractions of a penny)

**Estimated total:** Less than $1/month for typical usage! 💰

---

## Need Help?

- **Vercel Documentation:** [vercel.com/docs](https://vercel.com/docs)
- **AWS IAM Guide:** [docs.aws.amazon.com/iam](https://docs.aws.amazon.com/iam)
- **Project Issues:** [GitHub Issues](https://github.com/JavierHernandezVantuyl/aws-incident-copilot/issues)

---

## Quick Reference: Environment Variables

Copy this template for easy reference:

```bash
# Required
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
AWS_DEFAULT_REGION=us-east-1

# Optional - Thresholds
COPILOT_EC2_CPU_THRESHOLD=95.0
COPILOT_LAMBDA_ERROR_THRESHOLD=5
COPILOT_LOOKBACK_MINUTES=60

# Optional - Alerting
COPILOT_ENABLE_ALERTING=true
COPILOT_SNS_TOPIC_ARN=arn:aws:sns:us-east-1:123456789012:alerts
COPILOT_ALERT_EMAIL=you@example.com
```

---

**Congratulations! 🎉** Your AWS Incident Co-Pilot is now running on Vercel!

Visit your dashboard and start monitoring your AWS infrastructure with ease!
