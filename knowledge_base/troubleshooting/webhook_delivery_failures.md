# Webhook Delivery Failures

## Problem
Webhooks configured in Clouddash are not being delivered to external systems. Alert notifications aren't reaching webhook endpoints. Webhook shows as "Failed" or logs show delivery errors.

## Root Causes

### 1. Incorrect Webhook URL
- URL has typo or incorrect format
- Endpoint moved to different domain
- Port number changed
- Path incorrect or stale

### 2. Endpoint Not Accepting Requests
- Server behind webhook URL is down
- Service restarted and not accepting connections
- Load balancer or proxy misconfigured
- Firewall blocking incoming requests

### 3. Authentication Failures
- API key or token expired
- Authentication header format incorrect
- Bearer token not included
- API credentials changed in target system

### 4. Network/Firewall Issues
- Clouddash IP not whitelisted in firewall
- Outbound HTTPS blocked
- DNS resolution failing
- Proxy authentication required

### 5. Webhook Payload Issues
- Request body malformed or too large
- Content-Type header incorrect
- Special characters not properly encoded
- Payload schema doesn't match endpoint expectations

### 6. Rate Limiting at Endpoint
- Endpoint rejecting requests due to frequency
- HTTP 429 Too Many Requests errors
- Throttling threshold exceeded
- Backoff not implemented

### 7. TLS/Certificate Issues
- Endpoint certificate expired
- Self-signed certificate not trusted
- Certificate chain incomplete
- TLS version mismatch

## Diagnostic Steps

### Step 1: Verify Webhook Configuration
1. Go to **Settings** → **Webhooks**
2. Find the webhook in question
3. Check these fields:
   - **URL**: Appears correctly formatted
   - **Method**: GET, POST, or PUT selected
   - **Enabled**: Toggle is ON
   - **Headers**: Any custom headers configured
   - **Authentication**: Credentials/tokens if needed

### Step 2: Check Recent Delivery Attempts
1. In webhook settings, click **View History** or **Logs**
2. Look at recent delivery attempts (last hour)
3. Note status of each:
   - **Success** (green): Delivered successfully
   - **Failed** (red): Delivery attempt failed
   - **Pending** (yellow): Waiting to be delivered
4. Click failed entry to see error details

### Step 3: Test Webhook Connectivity
1. In Clouddash, click **Test Webhook**
2. Should send test payload to endpoint
3. Results show:
   - **Success**: Endpoint received request
   - **Failed**: Shows error reason
   - **Timeout**: Endpoint not responding
4. Error details help diagnose issue

### Step 4: Verify Endpoint Health
If endpoint URL is accessible:
1. Open command prompt/terminal
2. Test endpoint directly:
   ```bash
   curl -X POST https://your-endpoint.com/webhook \
     -H "Content-Type: application/json" \
     -d '{"test": "data"}'
   ```
3. Or use online tool: https://webhook.site
4. Check response status (should be 200, 201, or 202)

### Step 5: Check Endpoint Authentication
1. Determine auth method required:
   - API key in header
   - Bearer token
   - Basic auth (username:password)
   - OAuth
2. Verify credentials are current
3. Test authentication outside Clouddash if possible

### Step 6: Review Firewall Rules
1. Ask endpoint owner about:
   - IP whitelisting requirement
   - Clouddash IP address range whitelisted?
   - Rate limiting configured?
   - Proxy or WAF in front?
2. Check if Clouddash IPs are on whitelist

## Resolution Steps

### Fix 1: Correct Webhook URL

1. **Verify Correct URL**
   - Contact endpoint owner/team
   - Confirm current webhook endpoint URL
   - Ensure URL is publicly accessible
   - Verify protocol (https, not http)

2. **Update in Clouddash**
   - Go to **Settings** → **Webhooks**
   - Click webhook to edit
   - Update URL field with correct address
   - Save changes

3. **Test Updated URL**
   - Click **Test Webhook** button
   - Should show success
   - Check endpoint logs to verify reception

### Fix 2: Update Authentication

1. **Get New Credentials**
   - Contact endpoint service
   - Request new API key or token
   - Note exact format expected (Bearer token, API-Key header, etc.)
   - Check for any special characters or encoding

2. **Configure Authentication in Clouddash**
   - Edit webhook settings
   - Under **Authentication** section:
     - Select auth type (API Key, Bearer Token, etc.)
     - Enter exact credentials provided
     - Include correct header name
   - Save

3. **Test with New Credentials**
   - Click **Test Webhook**
   - Error should now include successful authentication
   - If still failing, verify credentials again

### Fix 3: Fix TLS/Certificate Issues

For self-signed certificates or certificate errors:

1. **If Endpoint Uses Self-Signed Certificate**
   - In webhook settings, look for **Verify SSL Certificate** toggle
   - If it fails, you can temporarily:
     - Disable SSL verification (less secure)
     - Or obtain proper certificate from CA
   - Note: Production should use valid certificates

2. **If Certificate Expired**
   - Contact endpoint owner
   - Request certificate renewal
   - Wait for update to propagate
   - Retry webhook after certificate is renewed

3. **Test Connection**
   - After certificate fix
   - Click **Test Webhook**
   - Should succeed

### Fix 4: Whitelist Clouddash IPs

1. **Get Clouddash IP Address**
   - Contact Clouddash support for IP range
   - Typically provided in docs or account settings

2. **Update Endpoint Firewall**
   - Contact endpoint owner
   - Provide Clouddash IP address/range
   - Request whitelisting in firewall
   - Request WAF/proxy rule update if needed

3. **Wait for Changes**
   - Firewall changes can take 5-15 minutes
   - Retry webhook after update applied

### Fix 5: Handle Rate Limiting

If error indicates "429 Too Many Requests":

1. **Reduce Webhook Frequency**
   - Go to alert that triggers webhook
   - Increase alert frequency/throttling
   - Reduce from "Every 5 minutes" to "Every 15 minutes"
   - Prevents duplicate webhook calls

2. **Implement Backoff at Endpoint**
   - Ask endpoint team to implement retry logic with backoff
   - Clouddash will retry failed deliveries
   - Standard: 1min, 5min, 15min, 30min delays

3. **Coordinate with Endpoint Owner**
   - Discuss expected webhook volume
   - May need to upgrade endpoint capacity
   - Batch webhooks if possible

### Fix 6: Verify Webhook Payload Format

1. **Check Webhook Headers**
   - In webhook edit, view required headers
   - Ensure Content-Type is: `application/json`
   - Verify any custom headers are correct

2. **Review Payload Structure**
   - Test webhook sends example payload
   - Compare to endpoint documentation
   - Verify all required fields present
   - Check data types match expectations

3. **Adjust if Needed**
   - Some endpoints require specific format
   - Contact Clouddash support if custom format needed
   - May require field mapping or transformation

### Fix 7: Test in Isolated Environment

1. **Create Test Webhook Service**
   - Use https://webhook.site for free testing
   - Creates unique URL that logs all requests
   - No authentication needed
   - Useful for debugging

2. **Configure Temporary Test Webhook**
   - In Clouddash, add webhook pointing to webhook.site
   - Trigger an alert
   - Check webhook.site to verify payload received
   - Review exact format and headers

3. **Identify Issue**
   - If webhook.site receives it: endpoint issue
   - If webhook.site doesn't receive it: Clouddash issue
   - Helps narrow down root cause

## Verification

After applying fixes:

1. **Test Webhook Delivery**
   - In webhook settings, click **Test Webhook**
   - Should show success response
   - Check endpoint logs confirm receipt

2. **Trigger Real Alert**
   - Create test condition that triggers alert
   - Alert should fire
   - Webhook should deliver
   - Monitor endpoint logs for incoming webhook

3. **Check Webhook History**
   - Go to webhook history/logs
   - Most recent entry should show **Success**
   - Timestamp should be recent

4. **Monitor for Ongoing Success**
   - Return to webhook settings
   - Watch delivery history
   - Should show consistent successes
   - No new error entries

## Prevention

- Test webhooks weekly
- Monitor webhook delivery logs
- Update webhook URLs when services migrate
- Rotate API keys/tokens annually
- Implement monitoring on webhook endpoints
- Set up alerts if webhook deliveries fail

## When to Escalate

Contact support if:
- Test webhook succeeds but real alerts still fail
- Endpoint confirms correctly formatted requests received but can't process
- Need custom webhook payload format
- Require webhook signature verification
- TLS/certificate issues persist after verification
- Multiple webhooks failing simultaneously
