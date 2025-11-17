# ✅ Pre-Deployment Checklist

Use this checklist before deploying to Vercel to ensure everything works!

## Local Testing (Do this first!)

### Step 1: Install Dependencies

```bash
# Install Node.js dependencies
npm install

# Install Python dependencies
pip install -e .
```

**Expected output:**
- ✅ No errors
- ✅ `node_modules/` folder created
- ✅ Python package installed

---

### Step 2: Create Local Environment File

```bash
# Copy the example file
cp .env.example .env.local
```

**Edit `.env.local` and add your AWS credentials:**
```bash
AWS_ACCESS_KEY_ID=your_actual_key_here
AWS_SECRET_ACCESS_KEY=your_actual_secret_here
AWS_DEFAULT_REGION=us-east-1
```

---

### Step 3: Test Python CLI (Optional but Recommended)

```bash
# Test AWS connection
copilot test

# Try mock data
copilot diagnose
```

**Expected output:**
- ✅ "All tests passed!" for `copilot test`
- ✅ Mock incidents displayed for `copilot diagnose`

---

### Step 4: Run Web Dashboard Locally

```bash
# Start the development server
npm run dev
```

**Expected output:**
```
  ▲ Next.js 14.0.4
  - Local:        http://localhost:3000
  - ready in X seconds
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

**What to verify:**
- [ ] Page loads without errors
- [ ] You see "AWS Incident Co-Pilot" header
- [ ] Dashboard has "Scan Now" button
- [ ] Stats cards are visible (showing 0s is fine)

---

### Step 5: Test API Endpoints

**In a new terminal window:**

```bash
# Test AWS connection endpoint
curl http://localhost:3000/api/test-aws

# Expected: {"configured":true,"has_access_key":true,...}

# Test scan endpoint
curl http://localhost:3000/api/scan

# Expected: {"success":true,"incidents":[...],...}

# Test mock data endpoint
curl http://localhost:3000/api/mock-incidents

# Expected: {"success":true,"incidents":[...],"is_mock":true}
```

**All should return JSON without errors!**

---

### Step 6: Test Dashboard Functionality

In your browser at [http://localhost:3000](http://localhost:3000):

1. **Check AWS Status:**
   - [ ] Top right shows "AWS Connected" (green checkmark)
   - [ ] If not connected, verify your `.env.local` credentials

2. **Click "Scan Now":**
   - [ ] Button shows "Scanning..." with spinner
   - [ ] Stats update (might show 0 incidents, that's okay!)
   - [ ] No error messages

3. **Try Continuous Monitoring (optional):**
   - [ ] Click "Start Continuous Monitoring"
   - [ ] Button changes to "Stop Monitoring"
   - [ ] Green message appears: "Continuous monitoring active"
   - [ ] Click "Stop Monitoring" to stop

---

## GitHub Preparation

### Step 7: Verify Git Status

```bash
# Check what's changed
git status

# You should see:
# - New files (app/, api/, package.json, etc.)
# - Modified files (README.md, .gitignore, .env.example)
```

**Important checks:**
- [ ] `.env.local` is NOT listed (it should be gitignored!)
- [ ] `.env` is NOT listed (it should be gitignored!)
- [ ] `node_modules/` is NOT listed (it should be gitignored!)

---

### Step 8: Commit Everything

```bash
# Add all new files
git add .

# Commit with a good message
git commit -m "Add web dashboard with Vercel support

- Created Next.js web dashboard with modern UI
- Added Python API routes for Vercel serverless functions
- Updated documentation with Vercel deployment guide
- Made project extremely user-friendly"

# Push to GitHub
git push origin enhance-user-experience
```

**Or merge to main:**
```bash
git checkout main
git merge enhance-user-experience
git push origin main
```

---

## Vercel Deployment

### Step 9: Vercel Account Setup

- [ ] Created account at [vercel.com](https://vercel.com)
- [ ] Connected GitHub account
- [ ] Verified email (if required)

---

### Step 10: Project Import

- [ ] Logged into [vercel.com/dashboard](https://vercel.com/dashboard)
- [ ] Clicked "Add New..." → "Project"
- [ ] Found `aws-incident-copilot` repository
- [ ] Clicked "Import"

---

### Step 11: Deployment Configuration

**Verify these settings (should be auto-detected):**
- [ ] Framework: Next.js
- [ ] Root Directory: `./`
- [ ] Build Command: `npm run build`
- [ ] Output Directory: `.next`

**Click "Deploy"** (without environment variables for now)

---

### Step 12: Add Environment Variables

After first deployment completes:

1. Go to project Settings → Environment Variables

2. Add these 3 required variables:

| Variable Name | Your Value | Environments |
|--------------|------------|--------------|
| `AWS_ACCESS_KEY_ID` | Your AWS Access Key | ☑️ Production ☑️ Preview ☑️ Development |
| `AWS_SECRET_ACCESS_KEY` | Your AWS Secret Key | ☑️ Production ☑️ Preview ☑️ Development |
| `AWS_DEFAULT_REGION` | `us-east-1` (or your region) | ☑️ Production ☑️ Preview ☑️ Development |

**Checklist:**
- [ ] All 3 variables added
- [ ] All 3 environments checked for each variable
- [ ] Saved each variable

---

### Step 13: Redeploy with Credentials

- [ ] Go to "Deployments" tab
- [ ] Click "..." on latest deployment
- [ ] Click "Redeploy"
- [ ] Confirm redeploy
- [ ] Wait for deployment to complete (~2-3 minutes)

---

## Post-Deployment Testing

### Step 14: Test Production Dashboard

Visit your Vercel URL: `https://your-project.vercel.app`

**Verify:**
- [ ] Page loads without errors
- [ ] Shows "AWS Connected" (green checkmark)
- [ ] Dashboard looks correct
- [ ] Stats cards visible

---

### Step 15: Test Production Functionality

1. **Click "Scan Now":**
   - [ ] Button works
   - [ ] Shows scanning animation
   - [ ] Returns results or "No incidents detected"
   - [ ] No error messages

2. **Check Browser Console:**
   - [ ] Press F12 to open developer tools
   - [ ] Check Console tab
   - [ ] Should see no red errors

---

## Troubleshooting

### If "AWS credentials not configured" appears:

1. Verify environment variables in Vercel
2. Make sure all 3 are present
3. Make sure all 3 environments are checked
4. Redeploy again

### If deployment fails:

1. Check deployment logs in Vercel
2. Look for specific error messages
3. Common issues:
   - Missing dependencies → check `package.json` and `requirements.txt`
   - Build errors → check Next.js configuration
   - Python errors → check `api/` folder structure

### If page loads but functionality doesn't work:

1. Open browser developer tools (F12)
2. Check Console for JavaScript errors
3. Check Network tab for failed API calls
4. Verify environment variables are set

---

## Final Verification

### Everything Working? Check these:

- [ ] Local development works (`npm run dev`)
- [ ] All API endpoints respond correctly
- [ ] Code pushed to GitHub
- [ ] Deployed to Vercel
- [ ] Environment variables added
- [ ] Production site loads correctly
- [ ] "Scan Now" button works
- [ ] No console errors

---

## 🎉 Success Criteria

Your deployment is successful when:

✅ Dashboard loads at your Vercel URL
✅ Shows "AWS Connected" status
✅ Can click "Scan Now" without errors
✅ Stats display correctly (even if 0 incidents)
✅ No red error messages in console or UI

---

## What to Do After Success

1. **Bookmark your dashboard URL**
2. **Test with real AWS resources** (if you have any incidents, they'll show up!)
3. **Share with your team** (if applicable)
4. **Set up custom domain** (optional, in Vercel settings)

---

## Useful Commands Reference

```bash
# Local Development
npm install                 # Install dependencies
npm run dev                # Run locally
npm run build              # Test production build
npm start                  # Run production build locally

# Testing
curl http://localhost:3000/api/test-aws    # Test AWS API
curl http://localhost:3000/api/scan        # Test scan API

# Git
git status                 # Check changes
git add .                  # Stage all changes
git commit -m "message"    # Commit
git push                   # Push to GitHub

# Python CLI (still available!)
copilot test              # Test AWS connection
copilot monitor           # Run CLI version
copilot diagnose          # View mock data
```

---

## Need Help?

- **Deployment Guide:** [DEPLOYMENT_FOR_JAVIER.md](DEPLOYMENT_FOR_JAVIER.md)
- **Full Vercel Guide:** [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md)
- **Local Development:** [QUICKSTART_WEB.md](QUICKSTART_WEB.md)
- **Vercel Docs:** [vercel.com/docs](https://vercel.com/docs)
- **GitHub Issues:** Report bugs or request features

---

**Good luck with your deployment!** 🚀
