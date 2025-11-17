# 🚀 Quick Start Guide - AWS Incident Co-Pilot

**Welcome!** This guide will help you get started in just 5 minutes - even if you've never used AWS or command-line tools before.

## What is AWS Incident Co-Pilot?

Think of it as a "health monitor" for your AWS cloud infrastructure. It automatically checks your AWS services (like servers, databases, and storage) and alerts you when something goes wrong.

## ⚠️ Important Notes Before Starting

- 📊 **Read-only monitoring**: This tool only reads data from your AWS account - it doesn't modify anything
- 💰 **AWS costs**: Using AWS services may incur small charges (CloudWatch/CloudTrail API calls)
- 🔐 **Security**: Keep your AWS access keys private - never share them or commit them to Git!
- 👤 **Permissions**: You'll need IAM permissions to read CloudWatch, CloudTrail, EC2, and Lambda data

## What You'll Need

1. **A computer** with internet access (macOS, Windows, or Linux)
2. **An AWS account** ([Create one free here](https://aws.amazon.com/free/) if you don't have one)
3. **5-10 minutes** of your time

## Step-by-Step Setup

### Step 1: Install Python (if you don't have it)

Python is a programming language that this tool needs to run. **You need Python 3.9 or higher.**

#### Check if you have Python:

Open Terminal (Mac/Linux) or Command Prompt (Windows) and type:

```bash
python3 --version
```

If you see `Python 3.9.x` or higher, you're good! Skip to Step 2.

#### If Python is not installed or too old:

**🍎 macOS:**

The easiest way is using Homebrew (a package manager for Mac):

1. **Install Homebrew** (if you don't have it):
   - Open Terminal (press `Cmd + Space`, type "Terminal")
   - Paste this command:
     ```bash
     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
     ```
   - Follow the prompts (you may need to enter your Mac password)

2. **Install Python 3**:
   ```bash
   brew install python@3.11
   ```

3. **Verify installation**:
   ```bash
   python3 --version
   ```

**Alternative for Mac (without Homebrew):**
- Download the official installer from [python.org](https://www.python.org/downloads/macos/)
- Download the latest Python 3.11+ macOS installer
- Open the `.pkg` file and follow the installer

**🪟 Windows:**

1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Download "Python 3.11" (or newer)
3. **⚠️ IMPORTANT**: Check "Add Python to PATH" during installation
4. Run the installer
5. Verify by opening Command Prompt and typing: `python --version`

**🐧 Linux (Ubuntu/Debian):**

```bash
sudo apt update
sudo apt install python3.11 python3-pip
```

**Linux (Fedora/RHEL):**

```bash
sudo dnf install python3.11 python3-pip
```

### Step 2: Install AWS Incident Co-Pilot

#### For macOS/Linux:

Open Terminal and run:

```bash
# Install using pip (Python's package installer)
pip3 install aws-incident-copilot

# If that doesn't work, try:
python3 -m pip install --user aws-incident-copilot
```

#### For Windows:

Open Command Prompt and run:

```bash
pip install aws-incident-copilot

# If that doesn't work, try:
python -m pip install --user aws-incident-copilot
```

⏳ Wait for it to finish (usually takes 30-60 seconds).

#### Verify installation:

```bash
copilot --help
```

If you see the help menu, you're all set! If you get "command not found":

**macOS/Linux fix:**
```bash
# Add Python's bin directory to your PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc  # For macOS
# Or for older Macs:
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bash_profile
source ~/.zshrc  # Reload your shell
```

**Windows fix:**
- The installer should have added Python to PATH. If not, search for "Edit system environment variables" and add `C:\Users\YourName\AppData\Local\Programs\Python\Python311\Scripts` to your PATH.

### Step 3: Get Your AWS Access Keys

AWS access keys are like a username and password for the tool to access your AWS account.

> ⚠️ **SECURITY WARNING**: Your AWS access keys give full access to your AWS account.
> - **Never share them** with anyone
> - **Never commit them** to Git/GitHub
> - **Never post them** in forums or chat
> - Store them securely (like in a password manager)
> - If accidentally exposed, delete them immediately in AWS Console

#### Create Access Keys:

1. **Log into AWS Console**: Go to [console.aws.amazon.com](https://console.aws.amazon.com)

2. **Navigate to IAM**:
   - Click your username (top right)
   - Click **"Security credentials"**
   - Or go directly to IAM → Users → Your User

3. **Create access key**:
   - Scroll to **"Access keys"** section
   - Click **"Create access key"**
   - Choose **"Command Line Interface (CLI)"**
   - Check the confirmation box
   - Click **"Next"** → **"Create access key"**

4. **⚠️ SAVE YOUR KEYS IMMEDIATELY**:

   Copy and save both keys somewhere safe (like a password manager):

   - **Access Key ID**: Looks like `AKIAIOSFODNN7EXAMPLE`
   - **Secret Access Key**: Looks like `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`

   > ⚠️ **CRITICAL**: You can only see the Secret Access Key once! If you lose it, you'll need to create new keys.

5. **Click "Download .csv file"** as a backup (store it securely!)

### Step 4: Run the Setup Wizard

This is the easiest part! The interactive wizard will guide you through everything.

```bash
copilot setup
```

The wizard will ask you a few simple questions:

#### Question 1: AWS Credentials

If AWS CLI is installed and configured, it will auto-detect your credentials. If not:

- Choose **"Yes, I have my access keys ready"**
- Paste your **Access Key ID** (from Step 3)
- Paste your **Secret Access Key** (from Step 3)

> 💡 **Tip**: When pasting the Secret Access Key, you won't see the text (for security). Just paste and press Enter.

#### Question 2: AWS Region

Choose where your AWS resources are located:

- **Option 1**: US East (N. Virginia) - `us-east-1` (most common)
- **Option 2**: US West (Oregon) - `us-west-2`
- **Option 3**: EU (Ireland) - `eu-west-1`
- **Option 4**: Asia Pacific (Singapore) - `ap-southeast-1`
- **Option 5**: Enter a custom region

> 💡 **Don't know your region?** Choose Option 1 (us-east-1). You can change it later in the `.env` file.

#### Question 3: Detection Settings

For beginners, just type **`y`** (yes) to use recommended defaults.

Advanced users can customize:
- CPU threshold (default: 95%)
- Lambda error count (default: 5 errors)
- How far back to check (default: 60 minutes)

#### Question 4: Test Connection

Type **`y`** (yes) to test your AWS connection.

If tests pass, you'll see green checkmarks ✓ and you're ready!

### Step 5: Start Monitoring!

Run your first scan:

```bash
copilot monitor
```

This will:
1. Connect to your AWS account
2. Scan for incidents across EC2, Lambda, S3, and Bedrock
3. Display any issues found in a nice table
4. Suggest fixes for each issue

**That's it!** You're now monitoring your AWS infrastructure! 🎉

## What Happens Next?

The tool scans your AWS account for common problems:

- 🔴 **EC2 High CPU**: Servers running at >95% CPU for 10+ minutes
- ⚠️ **Lambda Errors**: Functions with 5+ errors in the last hour
- 📊 **Bedrock Token Spikes**: Excessive API usage (>100K tokens/hour)
- 🔒 **S3 Access Denied**: Permission errors on S3 buckets

### Understanding the Output

If incidents are found, you'll see a table with:

| Column | Meaning |
|--------|---------|
| **ID** | Unique identifier for the incident |
| **Title** | Short description of the problem |
| **Severity** | LOW, MEDIUM, HIGH, or CRITICAL |
| **Resource** | Which AWS resource has the issue |
| **Description** | Details about what's wrong |

For each incident, you'll also get **suggested fixes**!

## Common Commands

```bash
# Show welcome screen with command list
copilot

# Run setup wizard again
copilot setup

# Test your AWS connection
copilot test

# Scan once for incidents
copilot monitor

# Keep monitoring continuously (checks every 5 minutes)
copilot monitor --continuous

# Monitor with alerts (emails/SNS for HIGH/CRITICAL)
copilot monitor --alerts

# Monitor without saving evidence files (faster)
copilot monitor --no-evidence

# Use a specific AWS region
copilot monitor --region us-west-2

# Use a specific AWS profile
copilot monitor --profile production

# Get help for any command
copilot monitor --help
```

## Troubleshooting

### "Command not found: copilot"

**On Mac/Linux:**
```bash
# Check where Python installs packages
python3 -m site --user-base

# Add to PATH (for macOS with zsh - default on modern Macs)
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Or for older Macs with bash:
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bash_profile
source ~/.bash_profile

# Try running with full path:
python3 -m copilot.cli --help
```

**On Windows:**
- Restart your Command Prompt
- Make sure Python is in PATH during installation
- Try: `python -m copilot.cli --help`

### "No AWS credentials found"

Your AWS keys aren't configured. Run:
```bash
copilot setup
```

Or manually configure AWS CLI:
```bash
aws configure
```

### "Permission denied" or "Access denied" errors

Your AWS user needs these permissions:
- `cloudwatch:GetMetricStatistics`
- `cloudwatch:ListMetrics`
- `cloudtrail:LookupEvents`
- `ec2:DescribeInstances`
- `lambda:ListFunctions`
- `lambda:GetFunction`

Ask your AWS administrator to grant these, or create an IAM policy (see [Required Permissions](#required-permissions) below).

### "Invalid region" or "Region not found"

The region you specified doesn't exist. Common regions:
- `us-east-1` (N. Virginia)
- `us-west-2` (Oregon)
- `eu-west-1` (Ireland)
- `ap-southeast-1` (Singapore)

See [full list of regions](https://docs.aws.amazon.com/general/latest/gr/rande.html).

### Tests are slow or timing out

This is normal! AWS API calls can take 5-10 seconds each. If it's taking longer:
- Check your internet connection
- Try a different AWS region
- AWS might be experiencing issues - check [AWS Status Page](https://status.aws.amazon.com/)

### On Mac: "command not found: brew"

Homebrew isn't installed. You have two options:

1. **Install Homebrew** (recommended):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Or download Python directly** from [python.org](https://www.python.org/downloads/macos/)

### Still stuck?

1. **Run the test command** to see what's failing:
   ```bash
   copilot test
   ```

2. **Check the full README** for detailed documentation:
   [README.md](README.md)

3. **Open an issue** on GitHub:
   [github.com/JavierHernandezVantuyl/aws-incident-copilot/issues](https://github.com/JavierHernandezVantuyl/aws-incident-copilot/issues)

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
        "lambda:GetFunction",
        "sts:GetCallerIdentity"
      ],
      "Resource": "*"
    }
  ]
}
```

### How to create an IAM policy:

1. Go to [IAM Console](https://console.aws.amazon.com/iam/)
2. Click **Policies** → **Create policy**
3. Click **JSON** tab
4. Paste the policy above
5. Click **Review policy**
6. Name it: `IncidentCopilot-ReadOnly`
7. Click **Create policy**
8. Go to **Users** → Your User → **Add permissions** → **Attach policies directly**
9. Search for `IncidentCopilot-ReadOnly` and attach it

## Advanced Usage

### Continuous Monitoring

Keep the tool running 24/7:

```bash
# Run continuously (Ctrl+C to stop)
copilot monitor --continuous

# With alerts enabled
copilot monitor --continuous --alerts
```

> 💡 **Tip**: Run this in a screen/tmux session or as a system service to keep it running in the background.

### Email/SNS Alerts

To receive emails when incidents are found:

1. **Create an SNS topic** in AWS Console
2. **Subscribe your email** to the SNS topic
3. **Edit your `.env` file**:
   ```bash
   COPILOT_ENABLE_ALERTING=true
   COPILOT_SNS_TOPIC_ARN=arn:aws:sns:us-east-1:123456789012:incident-alerts
   COPILOT_ALERT_EMAIL=your-email@example.com
   ```

4. **Run with alerts**:
   ```bash
   copilot monitor --continuous --alerts
   ```

### Custom Thresholds

Edit the `.env` file in your project directory:

```bash
# Alert when CPU > 90% (default: 95%)
COPILOT_EC2_CPU_THRESHOLD=90.0

# Alert after 10 Lambda errors (default: 5)
COPILOT_LAMBDA_ERROR_THRESHOLD=10

# Check last 2 hours instead of 1 hour (default: 60)
COPILOT_LOOKBACK_MINUTES=120

# Check every 10 minutes instead of 5 (default: 300)
COPILOT_POLL_INTERVAL_SECONDS=600
```

### Multiple AWS Accounts/Profiles

If you have multiple AWS accounts:

```bash
# Use a specific profile
copilot monitor --profile production

# Or set it in .env:
COPILOT_AWS_PROFILE=production
```

## Security Best Practices

🔐 **Protect your AWS credentials:**

1. **Use IAM users** with minimal permissions (not root account)
2. **Enable MFA** (Multi-Factor Authentication) on your AWS account
3. **Rotate access keys** regularly (every 90 days)
4. **Use AWS SSO** or temporary credentials if possible
5. **Never commit `.env` to Git** (it's in `.gitignore` by default)
6. **Monitor CloudTrail** for unusual activity
7. **Delete old access keys** you're not using

If you suspect your keys are compromised:
1. Go to AWS Console → IAM → Security Credentials
2. **Deactivate** the compromised key immediately
3. Create new keys
4. Run `copilot setup` again with new keys

## Cost Considerations

💰 **This tool makes AWS API calls**, which may incur small charges:

- **CloudWatch** `GetMetricStatistics`: ~$0.01 per 1,000 requests
- **CloudTrail** `LookupEvents`: Usually covered by free tier
- **EC2/Lambda** `Describe/List` calls: Free

**Typical costs**: Less than $1-2/month for hourly monitoring

To minimize costs:
- Use longer `COPILOT_POLL_INTERVAL_SECONDS` (check less frequently)
- Reduce `COPILOT_LOOKBACK_MINUTES` (check shorter time periods)
- Run scans manually instead of continuously

## Next Steps

- 📖 Read the [full README](README.md) for all features
- ⚙️ Customize settings in `.env` file
- 🔔 Set up email/SNS alerts for critical incidents
- 📊 Review incidents regularly to improve your infrastructure
- 🤖 Automate with cron jobs or systemd services

## Need Help?

- 📚 [Full Documentation](README.md)
- 💬 [GitHub Issues](https://github.com/JavierHernandezVantuyl/aws-incident-copilot/issues)
- 🐛 [Report a Bug](https://github.com/JavierHernandezVantuyl/aws-incident-copilot/issues/new)

---

**Made with ❤️ to make AWS monitoring easy for everyone!**

*Questions? Found this helpful? Give us a ⭐ on [GitHub](https://github.com/JavierHernandezVantuyl/aws-incident-copilot)!*
