# User Authentication & Configuration

AWS Incident Co-Pilot now features per-user authentication and credential management, ensuring that each user can monitor their own AWS account without sharing credentials.

## Overview

The application uses **NextAuth.js** for authentication and stores AWS credentials securely in encrypted JWT session cookies. Each user manages their own AWS credentials through a dedicated Settings page.

## Key Features

- **Per-User Isolation**: Each user logs in with their own username/password
- **Personal AWS Credentials**: Users configure their own AWS Access Keys in Settings
- **Session-Based Storage**: Credentials stored in encrypted browser session (24-hour expiry)
- **No Database Required**: All authentication handled via JWT tokens
- **Easy Configuration**: Simple Settings UI for updating AWS credentials anytime

## How It Works

### 1. First Time Setup

1. Visit the application URL
2. You'll be redirected to the login page
3. Create an account by entering:
   - Username (any username you choose)
   - Password (keep it secure)
   - Optionally configure AWS credentials now, or skip and do it later

### 2. Configuring AWS Credentials

After logging in:

1. Click the **Settings** button in the header
2. Enter your AWS credentials:
   - **AWS Access Key ID**: Your personal AWS access key
   - **AWS Secret Access Key**: Your AWS secret key
   - **AWS Region**: The primary region to monitor (e.g., us-east-1)
3. Click **Save Changes**
4. Return to the dashboard

Your credentials are now active and will be used for all AWS API calls.

### 3. Using the Dashboard

- The dashboard only shows incidents from **your** AWS account
- All scans use **your** credentials
- Your credentials are never shared with other users
- Each user sees only their own AWS resources

## Security

### Credential Storage

- **Browser Session Only**: Credentials stored in encrypted JWT session cookie
- **No Server Storage**: No database, no credential persistence on server
- **24-Hour Expiry**: Sessions automatically expire after 24 hours
- **HTTPS Required**: Always use HTTPS in production to protect credentials in transit

### Session Management

- **Automatic Logout**: Session expires after 24 hours of inactivity
- **Manual Logout**: Click your username → Sign Out to end session immediately
- **Credential Updates**: Change AWS credentials anytime in Settings

### Best Practices

1. **Use IAM Read-Only Credentials**: Configure an IAM user with read-only permissions:
   - `CloudWatchReadOnlyAccess`
   - `AWSCloudTrailReadOnlyAccess`
   - `AmazonEC2ReadOnlyAccess`

2. **Rotate Credentials Regularly**: Update your AWS credentials every 90 days

3. **Use Strong Passwords**: Choose a strong password for your Co-Pilot account

4. **Don't Share Accounts**: Each team member should have their own account

## Environment Variables (Deployment)

When deploying to Vercel or other platforms, configure:

### Required

```bash
# NextAuth Configuration
NEXTAUTH_SECRET=<generate-with-openssl-rand-base64-32>
NEXTAUTH_URL=https://your-deployed-url.com
```

### Optional (Legacy Fallback)

```bash
# Optional: Fallback AWS credentials if user hasn't configured their own
AWS_ACCESS_KEY_ID=<your-aws-key>
AWS_SECRET_ACCESS_KEY=<your-aws-secret>
AWS_DEFAULT_REGION=us-east-1
```

## Generating NEXTAUTH_SECRET

For production deployments, generate a secure secret:

```bash
openssl rand -base64 32
```

Add this value to your Vercel environment variables as `NEXTAUTH_SECRET`.

## Migration from Environment-Based Auth

If you previously used environment variable-based AWS credentials:

### What Changed

- **Before**: All users shared single AWS credentials from Vercel env vars
- **After**: Each user configures their own AWS credentials in Settings

### Migration Steps

1. **Update Environment Variables**:
   - Add `NEXTAUTH_SECRET` to Vercel (required)
   - Add `NEXTAUTH_URL` to Vercel (required)
   - Keep existing `AWS_*` vars as fallback (optional)

2. **Redeploy Application**:
   - Deploy latest code to Vercel
   - Application now has login page

3. **User Onboarding**:
   - Have each user create an account
   - Each user configures their AWS credentials in Settings
   - Users can now monitor their own AWS accounts independently

### Fallback Behavior

- If user hasn't configured AWS credentials, system falls back to environment variables
- This allows gradual migration and backward compatibility
- Eventually remove fallback env vars once all users have configured credentials

## Troubleshooting

### "AWS credentials not configured"

**Solution**: Go to Settings and enter your AWS Access Key ID and Secret Access Key

### "Invalid AWS Access Key ID"

**Solution**:
1. Verify credentials are correct in AWS IAM Console
2. Ensure Access Key is active (not deleted or deactivated)
3. Check for typos when copying credentials

### "Access denied" errors

**Solution**:
1. Verify your IAM user has required permissions
2. Attach read-only policies: CloudWatch, CloudTrail, EC2
3. Test credentials using AWS CLI: `aws sts get-caller-identity`

### Session expired

**Solution**: Log out and log back in to refresh your 24-hour session

### Credentials not updating

**Solution**:
1. Sign out completely
2. Sign back in
3. Go to Settings and reconfigure credentials
4. Click Save Changes

## API Changes

### Frontend → Backend Communication

The frontend now sends AWS credentials with each API request:

```typescript
// Example: Testing AWS connection
const response = await fetch('/api/test-aws', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    awsAccessKeyId: session.user.awsAccessKeyId,
    awsSecretAccessKey: session.user.awsSecretAccessKey,
    awsRegion: session.user.awsRegion
  })
})
```

### Backend Handlers

API handlers accept credentials from request body:

```python
# Python API handler
def do_POST(self):
    request_data = json.loads(request_body)
    credentials = self._get_credentials(request_data)
    # Use user-specific credentials for AWS API calls
```

## Future Enhancements

Potential improvements for consideration:

- **Database Storage**: Store encrypted credentials in database for persistence
- **Multi-Account Support**: Allow users to configure multiple AWS accounts
- **Role-Based Access**: Add admin/user roles with different permissions
- **Audit Logging**: Track user actions and AWS API calls
- **SSO Integration**: Support enterprise SSO providers (SAML, OAuth)
- **MFA Support**: Add two-factor authentication for enhanced security

## Support

For issues or questions:

1. Check this documentation first
2. Review logs in browser console (F12 → Console)
3. Check Vercel function logs for server-side errors
4. Open an issue on GitHub with details

---

**Important**: Your AWS credentials are sensitive. Never share them, commit them to git, or expose them in screenshots. Treat them like passwords.
