# SSO Setup Guide

## Overview
Single Sign-On (SSO) allows your team to log into Clouddash using your organization's identity provider. Supported providers include Okta, Azure AD (Entra ID), Google Workspace, and SAML 2.0 compatible systems.

## Supported Identity Providers

### Enterprise Providers
- **Okta**: Full SAML 2.0 support
- **Azure AD/Entra ID**: OAuth 2.0 and SAML
- **Google Workspace**: SAML 2.0
- **Ping Identity**: SAML 2.0
- **OneLogin**: SAML 2.0
- **JumpCloud**: SAML 2.0

### Protocol Support
- **SAML 2.0**: Most common, recommended
- **OpenID Connect (OIDC)**: Modern alternative
- **OAuth 2.0**: For select providers

## Before You Start

### Prerequisites
- Administrator access to Clouddash account
- Administrator access to Identity Provider
- Verified domain in Clouddash
- Users already created in IdP or auto-provisioning enabled

### Information You'll Need

From your Identity Provider:
- Entity ID (Issuer)
- SAML Login Endpoint (SSO URL)
- SAML Logout Endpoint (SLO URL)
- X.509 Certificate (public key)
- Metadata XML URL (optional but helpful)

## Setting Up SSO in Clouddash

### Step 1: Navigate to SSO Settings

1. Log into Clouddash as administrator
2. Go to **Settings** → **Security** → **Single Sign-On**
3. Click **+ Add SSO Provider**
4. Select provider type:
   - SAML 2.0
   - OpenID Connect
   - Or search for specific provider (Okta, Azure, Google, etc.)

### Step 2: Configure Provider

**For SAML 2.0:**
1. Name: Select "Custom SAML 2.0" or specific provider
2. Issuer/Entity ID: Paste the issuer from IdP metadata
3. SSO Login URL: Paste SAML endpoint for login
4. SLO Logout URL: Paste SAML endpoint for logout
5. X.509 Certificate: Paste public certificate (PEM format)
6. Click **Continue**

**For OpenID Connect:**
1. Provider: Select or enter provider name
2. Client ID: From IdP OIDC configuration
3. Client Secret: From IdP OIDC configuration
4. Discovery URL: Usually https://provider/.well-known/openid-configuration
5. Scopes: email, profile (minimum)
6. Click **Continue**

### Step 3: Configure Attribute Mapping

Clouddash needs to map IdP attributes to user information:

**Required Mappings:**
- **Email Attribute**: Which IdP attribute contains user email
  - Common names: `mail`, `email`, `emailAddress`, `http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress`
  - Must be unique identifier

- **Name Attribute**: Which IdP attribute contains user name
  - Common names: `name`, `displayName`, `givenName`
  - Used for user display

**Optional Mappings:**
- **Department**: For organizational tracking
- **Group**: For role mapping (see RBAC section)

**How to Find Attributes:**
1. Check IdP attribute mapping documentation
2. Use saml-tracer or similar tool to inspect SAML assertion
3. Ask IdP administrator for attribute list
4. Test with sample user assertion

### Step 4: Configure User Provisioning

**Just-In-Time (JIT) Provisioning:**
- User created in Clouddash on first SSO login
- Automatically added to default group
- Requires email attribute mapping
- Recommended for most organizations

**Enable JIT:**
1. In SSO config, find **Provisioning** section
2. Toggle **Auto-provision users** to ON
3. Select default role for new users:
   - Viewer (read-only)
   - Developer
   - Manager
4. Save

**Manual Provisioning:**
- Administrator creates users in Clouddash first
- Users then use SSO to log in
- Requires email matching between systems
- More control but more overhead

### Step 5: Test Configuration

1. Click **Test Connection**
2. Clouddash attempts to fetch metadata and validate
3. Should show "✓ Configuration valid"
4. If errors, review configuration against IdP settings

**Common Test Errors:**
- "Invalid certificate": Certificate format incorrect (must be PEM)
- "Cannot reach endpoint": URL incorrect or network blocked
- "Invalid Entity ID": Issuer doesn't match IdP configuration

### Step 6: Enable SSO

1. After successful test, toggle **Enable SSO** to ON
2. Configuration is now live
3. Users can access SSO login option
4. Email domain users can sign in via SSO

## Provider-Specific Setup

### Okta Setup

**In Okta Admin Console:**

1. Go to **Applications** → **Applications** → **Browse App Catalog**
2. Search for "Clouddash"
3. If found:
   - Click app
   - Click **Add**
   - Follow prompts
4. If not found:
   - Create SAML app
   - Continue with manual setup below

**Manual Okta SAML Setup:**
1. **General Settings**
   - App name: Clouddash
   - Skip optional settings

2. **SAML Settings**
   - Single Sign On URL: `https://yourdomain.clouddash.io/auth/saml/acs`
   - Audience Restriction: `https://yourdomain.clouddash.io`
   - Name ID Format: Email
   - Application username: Okta username

3. **Attribute Statements**
   - Name: `email` → Value: `user.email`
   - Name: `name` → Value: `user.displayName`

4. **Click Done**

**In Clouddash:**
1. Go to SSO Settings
2. Select "Okta" provider
3. Enter information from Okta metadata:
   - Issuer: `https://your-domain.okta.com`
   - SSO URL: From Okta SAML metadata
   - Certificate: From Okta app details
4. Test and enable

### Azure AD / Entra ID Setup

**In Azure Portal:**

1. Go to **Azure Active Directory** → **Enterprise applications** → **New application**
2. Search for "Clouddash" or create custom app
3. If custom app:
   - Name: Clouddash
   - Click **Create**

4. Go to **Single sign-on**
5. Select **SAML**
6. Configure:
   - Identifier (Entity ID): `https://yourdomain.clouddash.io`
   - Reply URL (Assertion Consumer Service URL): `https://yourdomain.clouddash.io/auth/saml/acs`
   - Sign on URL: `https://yourdomain.clouddash.io`

7. Under **Attributes & Claims**:
   - Add `email` claim (if not present)
   - Add `name` claim (if not present)

**In Clouddash:**
1. Go to SSO Settings
2. Select "Azure AD" or SAML 2.0
3. Use metadata URL or manual entry:
   - Issuer: `https://sts.windows.net/{tenant-id}/`
   - SSO URL: `https://login.microsoftonline.com/{tenant-id}/saml2`
   - Certificate: From Azure AD
4. Test and enable

### Google Workspace Setup

**In Google Admin Console:**

1. Go to **Apps** → **Web and mobile apps** → **Custom SAML apps**
2. Click **Create new custom SAML app**
3. App name: Clouddash

**Step 1: Google IdP Information**
- Download metadata or note Entity ID and SSO URL

**Step 2: Service Provider Details**
- ACS URL: `https://yourdomain.clouddash.io/auth/saml/acs`
- Entity ID: `https://yourdash.io`
- Start URL: `https://yourdomain.clouddash.io`
- Signed response: ON
- Name ID Format: Email

**Step 3: Attribute Mapping**
- Primary email → `email`
- First name / Last name → `name`

**In Clouddash:**
1. Go to SSO Settings
2. Select "Google Workspace" or SAML 2.0
3. Enter Google metadata:
   - Issuer: `https://accounts.google.com/o/saml2/idp?idpid={idpid}`
   - SSO URL: From Google metadata
   - Certificate: From Google metadata
4. Test and enable

## Verifying SSO Setup

### Test Login

1. Log out of Clouddash
2. Go to login page
3. Look for "Login with SSO" or company name button
4. Click SSO option
5. Redirected to IdP login
6. Enter credentials
7. Redirected back to Clouddash
8. Should be logged in

### Verify User Information

1. After SSO login, go to **Settings** → **Account**
2. Check that email and name are correct
3. Should match IdP user attributes
4. If incorrect, check attribute mapping

### Check Audit Log

1. Go to **Settings** → **Audit Logs**
2. Search for "SSO" or "authentication"
3. Should show successful login event
4. Entry includes timestamp, user, and status

## Troubleshooting SSO

### "Invalid SAML response"
- Check certificate is current (not expired)
- Verify clock sync between IdP and Clouddash
- Check attribute mapping is correct
- Test with different user

### "User not found / Create failed"
- If auto-provisioning enabled:
  - Check email attribute mapped correctly
  - Verify user's email in IdP
- If manual provisioning:
  - Create user in Clouddash first
  - Email must match exactly

### "Certificate expired"
- Download new certificate from IdP
- Update certificate in Clouddash settings
- Test connection
- Enable

### "Cannot find test event"
- Check IdP has Clouddash app assigned to test user
- If using groups: User must be in assigned group
- Try different test user
- Check IdP logs for errors

## Managing SSO

### Disable SSO Temporarily

1. Go to **Settings** → **Security** → **SSO**
2. Toggle SSO provider to OFF
3. Users must use email/password login
4. Toggle back ON to re-enable

### Change Provider

1. Create new SSO provider configuration
2. Test thoroughly
3. Once working, disable old provider
4. Delete old provider if no longer needed

### Add Second SSO Provider

1. Go to SSO settings
2. Click **+ Add Provider**
3. Configure different provider
4. Both will appear as login options
5. Users choose appropriate provider

## User Assignment

### Auto Assignment
- All organization domain users get access
- User auto-created on first login
- Group assignment based on SAML group claim

### Manual Assignment
- IdP users not automatically assigned
- Clouddash admin must create users
- Users log in via SSO with same email

### Group-Based Assignment
- SAML groups claim mapped to Clouddash roles
- Groups in IdP → Roles in Clouddash
- User roles automatically updated based on IdP group membership

## Best Practices

### Security
- Use SAML 2.0 or OIDC (not older protocols)
- Require HTTPS for all endpoints
- Rotate certificates annually
- Monitor for unusual SSO activity
- Use MFA in IdP for additional security

### User Management
- Keep IdP user list current
- Remove users from IdP when leaving organization
- Use group-based assignment when possible
- Regularly audit Clouddash user roster

### Maintenance
- Test SSO monthly
- Keep metadata up to date
- Monitor certificate expiration dates
- Plan certificate rotation in advance
- Document your SSO setup

## Support

For SSO setup help:
- **Documentation**: https://docs.clouddash.io/sso
- **Setup Wizard**: Guided setup in UI
- **Email**: support@clouddash.io
- **Response Time**: 24 hours
- Include IdP provider and error messages when contacting support
