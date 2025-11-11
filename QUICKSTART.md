# 🚀 Quick Start Guide - AWS Incident Co-Pilot

**Welcome!** This guide will help you get started in just 5 minutes - even if you've never used AWS or command-line tools before.

## What is AWS Incident Co-Pilot?

Think of it as a "health monitor" for your AWS cloud infrastructure. It automatically checks your AWS services (like servers, databases, and storage) and alerts you when something goes wrong.

## What You'll Need

1. **A computer** with internet access (Windows, Mac, or Linux)
2. **An AWS account** ([Create one here](https://aws.amazon.com/free/) if you don't have one)
3. **5 minutes** of your time

## Step-by-Step Setup

### Step 1: Install Python (if you don't have it)

Python is a programming language that this tool needs to run.

**Check if you have Python:**
```bash
python3 --version
```

If you see something like `Python 3.9.6`, you're good! If not:

- **Mac**: Python 3 is usually pre-installed
- **Windows**: Download from [python.org](https://www.python.org/downloads/)
- **Linux**: Run `sudo apt install python3` (Ubuntu/Debian)

### Step 2: Install AWS Incident Co-Pilot

Open your terminal (Mac/Linux) or Command Prompt (Windows) and run:

```bash
pip install aws-incident-copilot
```

Wait for it to finish (usually takes 30 seconds).

### Step 3: Get Your AWS Access Keys

AWS access keys are like a username and password for the tool to access your AWS account.

1. **Log into AWS Console**: Go to [console.aws.amazon.com](https://console.aws.amazon.com)
2. **Click your name** (top right) → **Security credentials**
3. Scroll to **Access keys** section
4. Click **Create access key**
5. Choose **Command Line Interface (CLI)**
6. Click **Next** → **Create access key**
7. **⚠️ IMPORTANT**: Save both keys somewhere safe:
   - Access Key ID (looks like: `AKIAIOSFODNN7EXAMPLE`)
   - Secret Access Key (looks like: `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`)

### Step 4: Run the Setup Wizard

This is the easiest part! Just run:

```bash
copilot setup
```

The wizard will ask you a few simple questions:

1. **Paste your Access Key ID** (from Step 3)
2. **Paste your Secret Access Key** (from Step 3)
3. **Choose your AWS region** (where your resources are)
   - If unsure, choose option 1 (US East)
4. **Use recommended settings?** Type `y` (yes)

That's it! The tool is now configured. ✅

### Step 5: Test Your Connection

Make sure everything works:

```bash
copilot test
```

You should see green checkmarks (✓) for each test. If you do, you're ready!

### Step 6: Start Monitoring

Run your first scan:

```bash
copilot monitor
```

This will scan your AWS account and show any incidents it finds.

## What Happens Next?

The tool will check for common problems like:
- 🔴 **High CPU usage** on servers (EC2)
- ⚠️ **Lambda function errors**
- 📊 **Excessive API usage** (Bedrock)
- 🔒 **Permission denied errors** (S3)

If it finds issues, it will show them in a nice table with:
- What the problem is
- How serious it is (LOW, MEDIUM, HIGH, CRITICAL)
- How to fix it

## Common Commands

```bash
# Show this welcome screen
copilot

# Run setup wizard again
copilot setup

# Test your AWS connection
copilot test

# Scan once for incidents
copilot monitor

# Keep monitoring continuously (checks every 5 minutes)
copilot monitor --continuous

# Enable email alerts for serious incidents
copilot monitor --alerts

# Get help
copilot --help
```

## Troubleshooting

### "No AWS credentials found"

Run `copilot setup` again and make sure you enter the correct access keys.

### "Permission denied" errors

Your AWS user needs these permissions:
- CloudWatch (read metrics)
- CloudTrail (read events)
- EC2 (describe instances)
- Lambda (list functions)

Ask your AWS administrator to grant these, or see [Required Permissions](#required-permissions).

### "Invalid region"

Run `copilot setup` and choose a different region where your AWS resources are located.

### Still stuck?

1. Run `copilot test` to see which service is failing
2. Check the [full README](README.md) for detailed documentation
3. [Open an issue](https://github.com/JavierHernandezVantuyl/aws-incident-copilot/issues) on GitHub

## Required Permissions

If you manage your own AWS account, create an IAM policy with these permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "cloudwatch:GetMetricStatistics",
        "cloudwatch:ListMetrics",
        "cloudtrail:LookupEvents",
        "ec2:DescribeInstances",
        "lambda:ListFunctions",
        "lambda:GetFunction"
      ],
      "Resource": "*"
    }
  ]
}
```

## Advanced Usage

### Continuous Monitoring

Keep the tool running in the background:

```bash
copilot monitor --continuous
```

Press `Ctrl+C` to stop.

### Email Alerts

To receive emails when incidents are found:

1. Edit your `.env` file:
   ```bash
   COPILOT_ENABLE_ALERTING=true
   COPILOT_ALERT_EMAIL=your-email@example.com
   COPILOT_SNS_TOPIC_ARN=arn:aws:sns:us-east-1:123456789012:incident-alerts
   ```

2. Run with alerts:
   ```bash
   copilot monitor --continuous --alerts
   ```

### Custom Thresholds

Edit `.env` to change when alerts trigger:

```bash
# Alert when CPU > 90% (default: 95%)
COPILOT_EC2_CPU_THRESHOLD=90.0

# Alert after 5 Lambda errors (default: 5)
COPILOT_LAMBDA_ERROR_THRESHOLD=5

# Check last 2 hours (default: 60 minutes)
COPILOT_LOOKBACK_MINUTES=120
```

## Next Steps

- 📖 Read the [full README](README.md) for all features
- ⚙️ Customize settings in `.env` file
- 🔔 Set up email/SNS alerts
- 📊 Review incidents regularly

## Need Help?

- 📚 [Full Documentation](README.md)
- 💬 [GitHub Issues](https://github.com/JavierHernandezVantuyl/aws-incident-copilot/issues)
- 📧 Contact: [your-email@example.com]

---

**Made with ❤️ to make AWS monitoring easy for everyone!**
