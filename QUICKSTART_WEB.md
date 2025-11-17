# 🚀 Quick Start: Web Dashboard

Get your AWS Incident Co-Pilot web dashboard running in 5 minutes!

## Prerequisites

- Node.js 18+ installed ([download here](https://nodejs.org/))
- AWS credentials (Access Key ID and Secret Access Key)
- Git installed

## Local Development Setup

### 1. Clone or Navigate to the Project

```bash
cd aws-incident-copilot
```

### 2. Install Dependencies

```bash
# Install Node.js dependencies
npm install

# Install Python dependencies
pip install -e .
```

### 3. Configure Environment Variables

Create a `.env.local` file for local development:

```bash
# Copy the example file
cp .env.example .env.local
```

Edit `.env.local` and add your AWS credentials:

```bash
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_DEFAULT_REGION=us-east-1
```

**Important:** Never commit `.env.local` to Git! It's already in `.gitignore`.

### 4. Run the Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser!

## What You'll See

- **Dashboard:** Real-time view of AWS incidents
- **Scan Button:** Manually trigger a scan
- **Continuous Monitoring:** Enable automatic scanning every 5 minutes
- **Incident Cards:** Detailed information about each incident

## Next Steps

### Deploy to Production (Recommended)

For production use, deploy to Vercel:

1. **Read the deployment guide:** [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md)
2. **Push to GitHub:** Commit and push your code
3. **Import to Vercel:** Connect your GitHub repository
4. **Add environment variables:** Configure AWS credentials in Vercel
5. **Deploy!** Your dashboard will be live at `https://your-project.vercel.app`

### Test the API Endpoints

The web dashboard uses these API endpoints:

- `/api/test-aws` - Test AWS connectivity
- `/api/scan` - Scan for incidents
- `/api/mock-incidents` - Get demo incidents

You can test them directly:

```bash
# Test AWS connection
curl http://localhost:3000/api/test-aws

# Scan for incidents
curl http://localhost:3000/api/scan

# Get mock incidents
curl http://localhost:3000/api/mock-incidents
```

## Troubleshooting

### "Module not found" errors

```bash
# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

### Python import errors

```bash
# Reinstall Python package
pip install -e .
```

### AWS credential errors

1. Verify your credentials are in `.env.local`
2. Check that the file is in the project root
3. Restart the dev server (`npm run dev`)

### Port already in use

```bash
# Use a different port
npm run dev -- -p 3001
```

## Building for Production

To create a production build locally:

```bash
# Build the application
npm run build

# Start the production server
npm start
```

## Project Structure

```
aws-incident-copilot/
├── app/                    # Next.js app directory
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Main dashboard page
│   └── globals.css        # Global styles
├── api/                   # Python serverless functions
│   ├── scan.py           # Scan for incidents
│   ├── test-aws.py       # Test AWS connection
│   └── mock-incidents.py # Get demo data
├── copilot/               # Python package (CLI)
│   ├── sources/          # AWS data sources
│   ├── detectors/        # Incident detection
│   └── ...
├── package.json          # Node.js dependencies
├── requirements.txt      # Python dependencies
└── vercel.json          # Vercel configuration
```

## Available Scripts

```bash
# Development
npm run dev              # Start development server

# Production
npm run build           # Build for production
npm start               # Start production server

# Linting
npm run lint            # Run ESLint

# Python CLI (still available!)
copilot monitor         # Run CLI version
copilot setup           # Setup wizard
copilot test            # Test AWS connection
```

## Learn More

- **Vercel Deployment:** [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md)
- **CLI Usage:** [QUICKSTART.md](QUICKSTART.md)
- **Full Documentation:** [README.md](README.md)
- **Next.js Docs:** [nextjs.org/docs](https://nextjs.org/docs)

## Getting Help

- **GitHub Issues:** [Report a bug or request a feature](https://github.com/JavierHernandezVantuyl/aws-incident-copilot/issues)
- **Next.js Help:** [nextjs.org/docs](https://nextjs.org/docs)
- **Vercel Help:** [vercel.com/docs](https://vercel.com/docs)

---

**Happy Monitoring! 🎉**
