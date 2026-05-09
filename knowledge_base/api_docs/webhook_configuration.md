# Webhook Configuration

## Overview
Webhooks allow Clouddash to send real-time notifications to your systems when events occur (alerts firing, metrics changing, etc.). Configure webhooks to integrate with your incident management, monitoring, or custom workflows.

## Webhook Basics

### What Are Webhooks?

Webhooks are HTTP POST requests Clouddash sends to your endpoint when events happen:

1. Event occurs in Clouddash (e.g., alert fires)
2. Clouddash sends HTTP POST to your URL
3. Your server receives event payload
4. Your system processes the event
5. Webhook delivery confirmed

### When to Use Webhooks

**Good for:**
- Real-time alerts to external systems
- Integration with incident management platforms
- Triggering automated responses
- Logging events to external services
- Updating issue tracking systems

**Not good for:**
- Frequent polling (use REST API instead)
- Large data transfers
- Long-running operations
- Query-based data retrieval

## Creating a Webhook

### Step 1: Navigate to Webhooks

1. Go to **Settings** → **Webhooks**
2. Click **+ Create Webhook**
3. Form appears with required fields

### Step 2: Configure Basic Settings

**Webhook Name:**
- Descriptive name (e.g., "Slack Alert Notifier")
- Used for organization and logging
- Visible only to you

**Endpoint URL:**
- Full HTTPS URL where events sent
- Example: `https://your-api.example.com/clouddash/alerts`
- Must be publicly accessible
- HTTPS required (not HTTP)

**Method:**
- POST (most common)
- PUT (if API requires)
- Typically POST for events

**Description (Optional):**
- Notes about webhook purpose
- Visible in webhook list

### Step 3: Configure Event Filters

**Select Event Types:**
- **Alert Fired**: When alert triggers
- **Alert Resolved**: When alert clears
- **Metric Updated**: When metric data changes
- **Threshold Exceeded**: When metric crosses threshold
- **Integration Changed**: When integration updated

Check which events to send to this webhook

**Filter by Alert Rules (Optional):**
- All alerts (default)
- Specific alert rules
- By alert severity
- By alert category

### Step 4: Configure Authentication

**No Authentication:**
- Webhook endpoint is public
- Anyone can send requests (not secure)
- Use only for testing

**API Key Authentication:**
- Header: `X-API-Key: your_secret_key`
- Endpoint verifies key matches expected value
- Simple authentication

**Bearer Token:**
- Header: `Authorization: Bearer your_token`
- Standard OAuth-style authentication
- More secure than API key

**Custom Headers:**
- Add custom headers to request
- Example: `X-Custom-Header: value`
- Useful for routing or identification

### Step 5: Configure Payload

**Payload Format:**
- JSON (standard)
- XML (if supported)
- Form data (if needed)

**Payload Content:**
- Full alert details
- Metric values
- Event timestamp
- Account information

### Step 6: Test and Enable

**Test Webhook:**
1. Click **Test Webhook**
2. Sends test payload to endpoint
3. Response shows success/failure
4. Check endpoint logs to verify receipt

**Enable Webhook:**
1. Toggle **Enabled** to ON
2. Webhook now active
3. Events sent as they occur
4. Can disable anytime

## Webhook Payload

### Example Alert Fired Payload

```json
{
  "event": "alert_fired",
  "timestamp": "2024-05-08T14:30:00Z",
  "alert_id": "alert_123",
  "alert_name": "AWS Alerts Not Firing",
  "severity": "critical",
  "account_id": "acc_456",
  "metric_name": "cloudwatch.sync.status",
  "metric_value": 0,
  "threshold": 1,
  "threshold_type": "less_than",
  "dashboard_id": "dash_789",
  "description": "CloudWatch integration sync failed",
  "runbook_url": "https://docs.company.com/alerts/cloudwatch",
  "tags": {
    "service": "monitoring",
    "env": "production"
  }
}
```

### Payload Fields

| Field | Description |
|-------|-------------|
| `event` | Type of event (alert_fired, alert_resolved, metric_updated) |
| `timestamp` | ISO 8601 timestamp when event occurred |
| `alert_id` | Unique alert identifier |
| `alert_name` | Human-readable alert name |
| `severity` | Critical, Warning, Info |
| `account_id` | Your Clouddash account ID |
| `metric_name` | Name of metric triggering alert |
| `metric_value` | Current metric value |
| `threshold` | Alert threshold value |
| `threshold_type` | Comparison type (greater_than, less_than, equals) |
| `dashboard_id` | Dashboard containing metric |
| `description` | Alert description |
| `runbook_url` | Link to incident runbook |
| `tags` | Custom tags for routing/filtering |

## Webhook Implementation

### Receiving Webhooks

**Node.js/Express:**
```javascript
const express = require('express');
const app = express();

app.post('/clouddash/alerts', express.json(), (req, res) => {
  const event = req.body;
  
  console.log('Alert received:', event.alert_name);
  console.log('Severity:', event.severity);
  console.log('Metric:', event.metric_name);
  
  // Process event
  handleAlert(event);
  
  // Send success response
  res.status(200).json({ received: true });
});

app.listen(3000);
```

**Python/Flask:**
```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/clouddash/alerts', methods=['POST'])
def handle_alert():
    event = request.json
    
    print(f"Alert: {event['alert_name']}")
    print(f"Severity: {event['severity']}")
    
    # Process event
    process_alert(event)
    
    return jsonify({'received': True})

if __name__ == '__main__':
    app.run(port=3000)
```

**Python/Django:**
```python
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json

@require_http_methods(['POST'])
def clouddash_webhook(request):
    event = json.loads(request.body)
    
    print(f"Alert: {event['alert_name']}")
    process_alert(event)
    
    return JsonResponse({'received': True})
```

### Webhook Verification

**Verify Webhook Origin (Optional but Recommended):**

1. Clouddash sends X-Webhook-Signature header
2. Calculate HMAC-SHA256 of payload
3. Compare with provided signature

```python
import hmac
import hashlib

def verify_webhook(payload, signature, secret):
    expected = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(expected, signature)

@app.route('/clouddash/alerts', methods=['POST'])
def handle_alert():
    signature = request.headers.get('X-Webhook-Signature')
    payload = request.get_data()
    
    if not verify_webhook(payload, signature, 'your_secret'):
        return jsonify({'error': 'Invalid signature'}), 401
    
    event = request.json
    process_alert(event)
    return jsonify({'received': True})
```

## Webhook Delivery

### Delivery Guarantees

**At-Least-Once Delivery:**
- Webhook sent when event occurs
- Retried if endpoint unavailable
- May be sent multiple times
- Your endpoint should handle duplicates

**Retry Policy:**
- Initial attempt: Immediate
- 1st retry: 1 minute later
- 2nd retry: 5 minutes later
- 3rd retry: 15 minutes later
- 4th retry: 30 minutes later
- Final retry: After 1 hour
- Max attempts: 5 total

### Success Response

Webhook considered successful if:
- Endpoint returns HTTP 200-299
- Response within 30 seconds
- Content-type: application/json

**Example Success:**
```json
{
  "status": "processed",
  "id": "webhook_123"
}
```

### Failure Handling

Webhook fails if:
- Endpoint returns 4xx or 5xx
- Timeout (>30 seconds)
- Network unreachable
- Invalid SSL certificate

After 5 failed attempts:
- Webhook marked as failed
- Alert sent to account owner
- Can be manually retried from settings
- Check webhook delivery logs for details

## Managing Webhooks

### View Webhook History

1. Go to **Settings** → **Webhooks**
2. Click on webhook name
3. View **Recent Deliveries**
4. Shows:
   - Delivery timestamp
   - Event type
   - Response status
   - Response time
   - Any error messages

### Edit Webhook

1. Click webhook name
2. Modify any setting:
   - Endpoint URL
   - Event types
   - Authentication
   - Custom headers
3. Click **Save**
4. Changes take effect immediately

### Disable/Enable Webhook

1. Find webhook in list
2. Toggle **Enabled** switch
3. Disabled webhooks don't fire
4. Re-enable anytime

### Delete Webhook

1. Click webhook name
2. Click **Delete**
3. Confirm deletion
4. Webhook permanently removed
5. Cannot recover deleted webhooks

### Test Webhook Again

1. Click on webhook
2. Click **Send Test Event**
3. Test alert fires webhook
4. Response shown immediately
5. Check endpoint logs

## Troubleshooting Webhooks

### Webhook Not Firing

**Causes:**
- Webhook disabled
- Event type not selected
- Wrong event type
- Alert rule not matching filter

**Resolution:**
1. Check webhook is **Enabled**
2. Verify event types selected
3. Trigger test event manually
4. Check Clouddash logs for errors

### Endpoint Not Receiving

**Causes:**
- Endpoint URL incorrect
- Firewall blocking requests
- Endpoint not accessible
- DNS resolution failure

**Resolution:**
1. Click **Test Webhook**
2. Check for connection error
3. Verify URL is correct
4. Ensure endpoint publicly accessible
5. Check firewall logs

### Slow Webhook Delivery

**Causes:**
- Endpoint processing slowly
- Network latency
- High load on endpoint
- Rate limiting

**Resolution:**
1. Optimize endpoint code
2. Move heavy processing to background job
3. Return response quickly
4. Implement queuing

### Authentication Failures

**Causes:**
- Wrong API key/token
- Header name incorrect
- Timing issues
- Credential expired

**Resolution:**
1. Verify credential in webhook settings
2. Check header name matches endpoint
3. Regenerate credential if expired
4. Test with simple curl command

## Best Practices

### Endpoint Design
- Return response quickly (< 1 second)
- Process heavy work asynchronously
- Use message queue if needed
- Validate webhook signature

### Error Handling
- Log all webhook events
- Catch and handle exceptions
- Implement idempotency (handle duplicates)
- Don't re-throw errors to Clouddash

### Scaling
- Use webhook for events, not polling
- Implement message queue for high volume
- Scale endpoint horizontally
- Monitor endpoint availability

### Security
- Always use HTTPS
- Verify webhook signature
- Rotate credentials regularly
- Limit webhook permissions
- Monitor for suspicious activity

## Support

For webhook help:
- **Documentation**: https://docs.clouddash.io/webhooks
- **Email**: support@clouddash.io
- **Response Time**: 24 hours
