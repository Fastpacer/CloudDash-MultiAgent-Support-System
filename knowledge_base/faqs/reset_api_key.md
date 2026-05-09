# How to Reset Your API Key

## Overview
API keys are sensitive credentials used to authenticate requests to the Clouddash API. If you suspect your key has been compromised or need to rotate it for security purposes, you can reset it from your account settings.

## Steps to Reset Your API Key

1. Log in to your Clouddash account
2. Navigate to **Settings** → **API Keys**
3. Locate your current API key in the list
4. Click the **Reset** button next to the key you want to rotate
5. Confirm the action when prompted
6. Your new API key will be displayed immediately

## Important Notes

- **Immediate invalidation**: Your old API key becomes invalid immediately upon reset
- **Update integrations**: Any services using the old key must be updated with the new one
- **No grace period**: Requests with the old key will fail with a 401 Unauthorized error
- **Audit trail**: API key resets are logged in your account audit logs

## Impact on Integrations

After resetting your API key, update the following:
- CloudWatch integration credentials
- AWS credential configurations
- Webhook integrations
- Any custom scripts or applications

## Troubleshooting

**My applications are failing after reset**
- Verify you've updated all integrations with the new key
- Check the API key hasn't been truncated when copying
- Ensure there are no leading/trailing spaces

**I can't find my API key section**
- Confirm your account has Admin or API Manager role
- Contact support if the option remains unavailable

## Best Practices

- Rotate API keys quarterly as part of security maintenance
- Use separate API keys for different integrations
- Store keys securely (never in version control)
- Set up alerts to monitor key usage
