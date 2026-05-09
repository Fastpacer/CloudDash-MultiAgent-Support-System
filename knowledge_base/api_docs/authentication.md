# API Authentication

## Overview
The Clouddash API uses API keys for authentication. Requests must include your API key in the Authorization header to access protected endpoints.

## Authentication Methods

### API Key Authentication (Recommended)

**What It Is:**
An alphanumeric token that identifies your account and permissions

**When to Use:**
- Server-to-server integrations
- Automated scripts and monitoring
- Custom applications
- Most common authentication method

**How It Works:**
1. Generate API key from account settings
2. Include key in request header
3. Server validates key and grants access
4. Request processed with your permissions

### Bearer Token Format

All API requests should include:
```
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

**Example Request:**
```bash
curl -H "Authorization: Bearer sk_live_abc123def456" \
  https://api.clouddash.io/v1/metrics
```

## Getting Your API Key

### Generate API Key

1. **Log Into Clouddash**
   - Navigate to web application
   - Log in with your credentials

2. **Go to Settings**
   - Click **Settings** in top right
   - Select **API Keys** or **Developer** section

3. **Create New Key**
   - Click **+ Generate New Key**
   - Give key a name (e.g., "Production Integration", "Dev Server")
   - Select scopes (permissions) needed:
     - **read:metrics** - Read metric data
     - **read:alerts** - Read alert rules
     - **write:alerts** - Create/modify alerts
     - **read:dashboards** - Access dashboards
     - **write:dashboards** - Create/modify dashboards
     - **admin:account** - Full account access (use with care)

4. **Copy Key**
   - Display shows full API key once
   - Copy immediately to secure location
   - Will not be shown again

5. **Store Securely**
   - Environment variable: `CLOUDDASH_API_KEY`
   - Secrets manager (AWS Secrets Manager, HashiCorp Vault)
   - Never in version control
   - Never in logs or error messages

## Key Management

### Viewing Existing Keys

1. Go to **Settings** → **API Keys**
2. List shows all generated keys
3. Last 4 characters visible for verification
4. Creation date and last used timestamp shown
5. Scopes displayed for each key

### Regenerating Keys

If you suspect compromise:

1. Go to API key settings
2. Find key to regenerate
3. Click **Regenerate**
4. Confirm action
5. Old key immediately invalidated
6. New key generated
7. Update integrations with new key

### Revoking Keys

To permanently disable a key:

1. Go to **Settings** → **API Keys**
2. Find key to revoke
3. Click **Revoke**
4. Confirm action
5. Key immediately invalid
6. Requests using key will fail
7. Cannot be restored

### Key Expiration

**Automatic Expiration:**
- Keys do not auto-expire by default
- Can set optional expiration when creating
- Recommended: 90 days for development, 1 year for production

**Manual Renewal:**
- Before expiration, generate new key
- Update applications to use new key
- Revoke old key after verification

## Using API Keys

### In Code Examples

**Python:**
```python
import requests

headers = {
    "Authorization": "Bearer sk_live_your_api_key_here",
    "Content-Type": "application/json"
}

response = requests.get(
    "https://api.clouddash.io/v1/metrics",
    headers=headers
)
```

**JavaScript/Node.js:**
```javascript
const response = await fetch('https://api.clouddash.io/v1/metrics', {
  method: 'GET',
  headers: {
    'Authorization': 'Bearer sk_live_your_api_key_here',
    'Content-Type': 'application/json'
  }
});
```

**cURL:**
```bash
curl -X GET https://api.clouddash.io/v1/metrics \
  -H "Authorization: Bearer sk_live_your_api_key_here" \
  -H "Content-Type: application/json"
```

### In Environment Variables

**Store Key Securely:**
```bash
export CLOUDDASH_API_KEY="sk_live_your_api_key_here"
```

**Access in Code:**
```python
import os
api_key = os.getenv('CLOUDDASH_API_KEY')
```

### In Configuration Files

**Never store in version control. Use:**
- `.env` file (add to `.gitignore`)
- Secrets manager
- Configuration service
- Environment-specific config

## API Key Scopes

### Available Scopes

| Scope | Permission | Use Case |
|-------|-----------|----------|
| `read:metrics` | Read metric data | Dashboards, reports |
| `read:alerts` | Read alert rules | Monitoring, audits |
| `write:alerts` | Create/modify alerts | Alert automation |
| `read:dashboards` | View dashboards | Embed views |
| `write:dashboards` | Create/modify dashboards | Programmatic dashboards |
| `read:integrations` | View integrations | Status checks |
| `write:integrations` | Configure integrations | Setup automation |
| `read:team` | View team members | Auditing |
| `admin:account` | Full account access | Administrative tasks |

### Principle of Least Privilege

- Grant only needed scopes
- Development key: Limited scopes
- Production key: Specific scopes only
- Separate keys for different purposes

## Authentication Errors

### 401 Unauthorized

**Causes:**
- Missing Authorization header
- Invalid or expired API key
- Key revoked or regenerated
- Typo in key

**Resolution:**
- Verify header included in request
- Check API key is correct
- Regenerate key if expired
- Check for hidden characters

**Example Error:**
```json
{
  "error": "unauthorized",
  "message": "Invalid or missing API key"
}
```

### 403 Forbidden

**Causes:**
- Key lacks required scope
- Insufficient permissions
- Account restricted or suspended

**Resolution:**
- Verify key has needed scopes
- Regenerate with additional scopes
- Contact support if account suspended

**Example Error:**
```json
{
  "error": "forbidden",
  "message": "API key lacks required scope: write:alerts"
}
```

## Security Best Practices

### Key Protection
- Treat API keys like passwords
- Never commit to version control
- Never share publicly
- Rotate regularly (annually minimum)
- Use environment variables

### Access Control
- Create separate keys for different applications
- Different key for development vs production
- Revoke keys from departed team members
- Audit key usage regularly

### Monitoring
- Check "Last Used" timestamp
- Alert on new key generation
- Monitor for unusual API activity
- Review access logs periodically

### Incident Response
- If key compromised:
  1. Immediately regenerate/revoke key
  2. Update all integrations
  3. Review API logs for misuse
  4. Contact support if suspicious activity
  5. Consider account security review

## Rate Limits by Auth Method

API keys have rate limit allowances:

**Default Limits:**
- 100 requests per minute per key
- 1,000 requests per hour per key
- 10,000 requests per day per key

**Upgrading Limits:**
- Contact support for increases
- Enterprise customers: Custom limits
- Documented in rate_limits.md

## Rotating Keys

### Scheduled Rotation Process

1. **Generate New Key**
   - Settings → API Keys → + Generate
   - Use same scopes as old key
   - Copy new key

2. **Update Integrations**
   - Update each application with new key
   - Test updated integrations
   - Verify functionality

3. **Revoke Old Key**
   - After all systems updated
   - Settings → API Keys → Revoke
   - Confirm no services still use old key

4. **Document Rotation**
   - Record date of rotation
   - Note which systems updated
   - Keep audit trail

## Troubleshooting

**Q: I lost my API key, what do I do?**
A: Generate a new key immediately. The old key cannot be recovered. Update all applications to use new key and revoke the old one.

**Q: Can I have multiple API keys?**
A: Yes. Create separate keys for different purposes (development, production, integrations, etc.).

**Q: How often should I rotate keys?**
A: Annually for production, more frequently if compromised. Development keys can be rotated less frequently.

**Q: What if my key is exposed in logs?**
A: Immediately regenerate/revoke the key. Review logs for misuse. Contact support to check for unauthorized access.

**Q: Can I use the same key across multiple applications?**
A: Possible but not recommended. Use separate keys to isolate access and simplify revocation.

## Support

For authentication help:
- **Documentation**: https://docs.clouddash.io/api/auth
- **Email**: support@clouddash.io
- **Response Time**: 24 hours
