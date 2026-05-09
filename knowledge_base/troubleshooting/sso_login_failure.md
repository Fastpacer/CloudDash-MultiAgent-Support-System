# SSO Login Failure

## Problem
Users cannot log in using Single Sign-On (SSO). Login attempts fail with error messages or redirect to error page. Users may see "Authentication Failed", "Invalid Credentials", or "Unauthorized" errors.

## Root Causes

### 1. SSO Configuration Not Enabled
- SSO not configured in Clouddash account
- SSO connector not properly set up
- Configuration changed or deleted
- Feature not available on current plan

### 2. Identity Provider (IdP) Misconfiguration
- IdP settings don't match Clouddash configuration
- Metadata URLs pointing to wrong endpoints
- Certificate or signing credentials expired
- SAML assertion format incorrect

### 3. User Not Provisioned in IdP
- User account doesn't exist in IdP
- User not assigned to Clouddash application
- Group membership incorrect
- User account disabled or suspended

### 4. Redirect URI Mismatch
- Redirect URI in IdP doesn't match Clouddash URL
- Application URL changed but IdP not updated
- Using HTTP instead of HTTPS or vice versa
- Domain/subdomain mismatch

### 5. SAML/OAuth Token Issues
- SAML assertion expired
- OAuth token invalid or revoked
- Clock skew between servers
- Encryption/signing issues

### 6. Email Domain Mismatch
- Email address used doesn't match verified domain
- IdP using different email domain than Clouddash
- User has multiple email addresses configured

## Diagnostic Steps

### Step 1: Verify SSO is Configured
1. Navigate to **Settings** → **Security** → **Single Sign-On**
2. Check if SSO is **Enabled** (toggle or status should indicate "Active")
3. If not enabled, SSO configuration missing
4. Verify SSO provider is selected (Okta, Azure AD, Google Workspace, etc.)

### Step 2: Check SSO Configuration
1. Go to **Settings** → **SSO Configuration**
2. Verify these fields are filled:
   - **Entity ID** (Issuer)
   - **Single Sign-On URL** (SAML endpoint)
   - **Single Logout URL**
   - **Certificate** (X.509, currently valid)
3. Values should match your IdP's metadata
4. Check certificate expiration date

### Step 3: Test SSO Connection
1. In SSO Settings, click **Test Connection**
2. Should show:
   - "Connection successful" (green)
   - IdP responding normally
   - Metadata retrieved successfully
3. If fails, connection issue with IdP

### Step 4: Check User Provisioning
1. Log into your Identity Provider (Okta, Azure AD, etc.)
2. Verify the user exists:
   - Account enabled and active
   - Not suspended or deprovisioned
3. Verify user assigned to Clouddash application
4. Check group memberships if group-based assignment used

### Step 5: Verify Redirect URI
1. In IdP admin console
2. Find Clouddash application configuration
3. Check **Authorized redirect URIs** or **Reply URLs**
4. Should include:
   - `https://yourdomain.clouddash.io/auth/callback`
   - `https://yourdomain.clouddash.io/auth/oidc/callback` (if using OIDC)
5. Must be HTTPS (not HTTP)
6. Must include correct domain

### Step 6: Check Logs
1. Go to **Settings** → **Audit Logs**
2. Search for "SSO" or "authentication"
3. Recent failed login attempts show:
   - Exact error message
   - Timestamp
   - User email
   - Error details

## Resolution Steps

### Fix 1: Enable SSO (If Not Configured)

1. **Prepare SSO Information**
   - Get IdP metadata URL or XML
   - Note Entity ID (Issuer)
   - Get SAML endpoint URL
   - Download X.509 certificate

2. **Configure in Clouddash**
   - Go to **Settings** → **Security** → **SSO**
   - Click **+ Add SSO Provider**
   - Select provider type (SAML 2.0, OpenID Connect, SAML)
   - Enter configuration details

3. **Enter IdP Details**
   - Entity ID: (from IdP metadata)
   - SAML Endpoint URL: (login URL from IdP)
   - Certificate: (X.509 public cert)
   - Email Attribute: (usually "email" or "mail")
   - Name Attribute: (usually "givenName familyName")

4. **Test and Enable**
   - Click **Test Configuration**
   - Should succeed
   - Toggle **Enable SSO** to on
   - Save settings

### Fix 2: Update IdP Configuration

1. **Access IdP Admin Console**
   - Okta: Admin console → Applications → Clouddash
   - Azure AD: Azure Portal → Enterprise Applications → Clouddash
   - Google Workspace: Admin console → Apps → SAML apps → Clouddash

2. **Verify Redirect URIs**
   - Check each configured return URL
   - Must match exactly: `https://yourdomain.clouddash.io/auth/callback`
   - Remove any test or old URLs
   - Ensure HTTPS (not HTTP)

3. **Update SAML Configuration if Needed**
   - Verify Entity ID matches Clouddash configuration
   - Check Single Sign-On URL is current
   - Upload latest certificate if expired

4. **Save and Test**
   - Save IdP changes
   - Wait 2-5 minutes for changes to propagate
   - Try SSO login again

### Fix 3: Provision User in IdP

1. **Check User Exists in IdP**
   - Okta: Go to Directory → People
   - Azure AD: Go to Users
   - Google Workspace: Go to Users
   - Search for user by email

2. **If User Not Found**
   - Create new user account
   - Set email address
   - Set password (temporary if IdP managed)

3. **Assign to Clouddash Application**
   - Find Clouddash app in IdP
   - Assign user to app
   - If group-based: Ensure user in correct group
   - Save assignment

4. **Wait for Provisioning**
   - Allow 5-10 minutes for changes
   - User should receive email notification
   - Try logging in again

### Fix 4: Fix Email Domain Mismatch

1. **Check Verified Domains**
   - Go to **Settings** → **Organization** → **Verified Domains**
   - List should include your email domain
   - If missing: Add and verify domain ownership

2. **Update IdP Email Domain**
   - Ensure IdP uses same domain for user emails
   - If using subdomains, add all to verified list
   - Example: `user@company.com` and `user@dept.company.com` both need domain

3. **Verify User Email Matches**
   - Clouddash user email: `john@company.com`
   - IdP SAML assertion email: `john@company.com`
   - Must match exactly (case-insensitive)

### Fix 5: Update SSO Certificate

If certificate expired:

1. **Get New Certificate from IdP**
   - Download latest X.509 certificate
   - Many IdPs auto-rotate certificates
   - Check IdP metadata endpoint for current cert

2. **Update in Clouddash**
   - Go to **Settings** → **SSO Configuration**
   - Paste new certificate in Certificate field
   - Click **Test Configuration**
   - Should show success

3. **Keep Old Certificate**
   - During transition, some IdPs accept both
   - New certificate should be active
   - Old certificate can remain temporarily

## Verification

After applying fixes:

1. **Test SSO Login**
   - Go to login page
   - Click "Login with SSO" or company name
   - Should redirect to IdP
   - After entering credentials, redirect back to Clouddash
   - Should be logged in

2. **Check Audit Log**
   - Go to **Audit Logs**
   - Search for user or "successful login"
   - Recent successful SSO event should appear

3. **Test with Different User**
   - Ask team member to log in via SSO
   - Verify multiple users can authenticate
   - Confirms not user-specific issue

4. **Verify Logout Works**
   - Test logout
   - Should redirect to IdP logout or back to login
   - Confirm no lingering sessions

## Prevention

- Renew SSO certificates 30 days before expiration
- Review SSO configuration quarterly
- Monitor IdP for metadata changes
- Keep redirect URIs documented
- Test SSO before making user-facing changes
- Have backup login method (email/password) for emergencies

## When to Escalate

Contact support if:
- SSO test connection fails consistently
- Configuration appears correct but users still can't log in
- Certificate issues after renewal
- Multiple users affected by same error
- Need help migrating to new IdP
- Require custom SAML attribute mapping
