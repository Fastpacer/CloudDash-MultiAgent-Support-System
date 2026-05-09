# Rate Limits

## Overview
The Clouddash API implements rate limiting to ensure fair usage and system stability. All API requests are subject to rate limits based on your subscription plan.

## Rate Limit Tiers

### Starter Plan
- **10 requests per second**
- **600 requests per minute**
- **36,000 requests per hour**
- **864,000 requests per day**

### Professional Plan
- **50 requests per second**
- **3,000 requests per minute**
- **180,000 requests per hour**
- **2,000,000 requests per day**

### Enterprise Plan
- **Custom limits**
- Contact sales for details
- Negotiable based on use case
- Typically 100+ requests per second

## Understanding Rate Limits

### How Limits Work

Rate limits are enforced at multiple levels:

**Per-Second Limit:**
- Maximum requests in single second
- Prevents traffic spikes
- Enforced at API gateway level

**Per-Minute Limit:**
- Smooths out burst traffic
- Detects sustained overuse
- Most commonly hit by automation

**Per-Hour and Per-Day Limits:**
- Long-term usage tracking
- Prevents quota exhaustion
- Applies to all requests

### Shared vs Individual Limits

- Limits apply to your entire API key
- All applications using same key share limits
- Create separate keys to isolate limits
- Exceeded limits affect all requests

## Rate Limit Headers

### Response Headers

Every API response includes rate limit information:

```
X-RateLimit-Limit: 3000
X-RateLimit-Remaining: 2998
X-RateLimit-Reset: 1609459200
X-RateLimit-Retry-After: 60
```

**Header Explanation:**

| Header | Meaning |
|--------|---------|
| `X-RateLimit-Limit` | Maximum requests allowed in period |
| `X-RateLimit-Remaining` | Requests left before rate limited |
| `X-RateLimit-Reset` | Unix timestamp when counter resets |
| `X-RateLimit-Retry-After` | Seconds to wait before retrying (if limited) |

### Checking Rate Limit Status

```bash
curl -i https://api.clouddash.io/v1/metrics \
  -H "Authorization: Bearer YOUR_API_KEY"

# Look for X-RateLimit headers in response
HTTP/1.1 200 OK
X-RateLimit-Limit: 3000
X-RateLimit-Remaining: 2998
X-RateLimit-Reset: 1609459200
```

## Handling Rate Limits

### 429 Too Many Requests

**Error Response:**
```json
{
  "error": "too_many_requests",
  "message": "Rate limit exceeded",
  "retry_after": 60
}
```

**HTTP Status:** 429

**Indicates:**
- All rate limit windows exceeded
- Must wait before retrying
- Check `Retry-After` header

### Response When Limited

When you hit rate limit:
1. Request rejected
2. HTTP 429 returned
3. `Retry-After` header specifies wait time
4. Subsequent requests also rejected until window resets

### Retry Strategy

**Exponential Backoff:**
```python
import time
import requests

max_retries = 5
retry_delay = 1

for attempt in range(max_retries):
    response = requests.get(
        'https://api.clouddash.io/v1/metrics',
        headers={'Authorization': f'Bearer {api_key}'}
    )
    
    if response.status_code == 429:
        wait_time = int(response.headers.get('Retry-After', retry_delay))
        print(f"Rate limited. Waiting {wait_time} seconds...")
        time.sleep(wait_time)
        retry_delay *= 2  # Exponential backoff
    else:
        break
```

## Optimizing API Usage

### Reduce Request Frequency

**Problem:** Too many status check requests

**Solution:** Increase polling interval
```python
# Before: Check every 10 seconds
for i in range(100):
    response = check_metrics()
    time.sleep(10)

# After: Check every 60 seconds
for i in range(100):
    response = check_metrics()
    time.sleep(60)
```

### Batch Operations

**Problem:** One request per metric

**Solution:** Batch multiple metrics
```python
# Before: 100 individual requests
for metric_id in metric_ids:
    response = get_metric(metric_id)

# After: Single batch request (if supported)
response = get_metrics_batch(metric_ids)
```

### Implement Caching

**Problem:** Repeated identical requests

**Solution:** Cache results locally
```python
import time

cache = {}
cache_ttl = 300  # 5 minutes

def get_cached_metrics():
    now = time.time()
    if 'metrics' in cache:
        if now - cache['metrics']['timestamp'] < cache_ttl:
            return cache['metrics']['data']
    
    data = fetch_metrics_from_api()
    cache['metrics'] = {'data': data, 'timestamp': now}
    return data
```

### Use Webhooks Instead of Polling

**Problem:** Continuous polling for alerts

**Solution:** Subscribe to webhooks
```
Polling: 1 request/minute × 1440 minutes = 1,440 requests/day
Webhooks: Only when alert fires (example: 10 times/day)

Savings: 1,430 requests/day
```

### Pagination for Large Results

**Problem:** Requesting all metrics at once

**Solution:** Use pagination
```python
# Before: Get all in one request
response = get_metrics(limit=10000)

# After: Paginate through results
page = 1
all_metrics = []
while True:
    response = get_metrics(page=page, limit=100)
    all_metrics.extend(response['data'])
    if not response.get('has_next'):
        break
    page += 1
```

## Monitoring Rate Limit Usage

### Check Current Usage

```bash
# Option 1: Check via API
curl https://api.clouddash.io/v1/account/rate-limit-status \
  -H "Authorization: Bearer YOUR_API_KEY"

# Response:
# {
#   "limit": 3000,
#   "remaining": 2850,
#   "reset_timestamp": 1609459200,
#   "percentage_used": 5
# }
```

### Set Up Alerts

1. Go to **Settings** → **API** → **Rate Limit Alerts**
2. Configure thresholds:
   - Alert at 75% usage
   - Alert at 90% usage
   - Alert at 100% usage
3. Choose notification channel (Email, Slack, Webhook)
4. Enable alerts

### Track Usage Over Time

- Monitor `X-RateLimit-Remaining` header
- Log requests by endpoint
- Identify high-traffic endpoints
- Plan optimization

## Common Rate Limit Issues

### "Rate limit exceeded" but usage looks low

**Causes:**
- Multiple API keys or applications counted together
- Burst traffic at specific times
- Background jobs running simultaneously
- Shared key across team members

**Solution:**
- Create separate keys for different services
- Stagger requests to avoid bursts
- Review access logs for unexpected traffic
- Check for runaway automation

### Unexpectedly hitting limits

**Causes:**
- Third-party integrations consuming quota
- Scheduled jobs running simultaneously
- Inefficient script with redundant requests
- Rate limit calculation differs from expected

**Solution:**
- Audit all API consumers
- Implement request caching
- Optimize API queries
- Contact support for limit adjustment

### Inconsistent rate limiting

**Causes:**
- Different services sharing same key
- Testing consuming production quota
- Pagination or retries amplifying requests
- Rate limit windows not synchronized

**Solution:**
- Use separate keys for test/production
- Verify pagination working correctly
- Check for retry loops
- Monitor rate limit headers

## Requesting Higher Limits

### When to Request Increase

- Approaching limits consistently
- Legitimate high-volume use case
- Plan to scale API usage
- Integrating many third-party services

### How to Request

1. **Log your current usage**
   - Provide data for last 7 days
   - Include average and peak requests/minute
   - Document use case

2. **Contact Clouddash**
   - Email: support@clouddash.io
   - Include account ID and use case
   - Provide usage metrics
   - Request specific new limit

3. **Provide Context**
   - What integrations require higher limits?
   - Expected usage growth?
   - Budget constraints?
   - Timeline for increase needed?

4. **Approval Process**
   - Support team reviews request
   - Typically approved within 24-48 hours
   - May require plan upgrade
   - Enterprise customers: Custom negotiation

## Best Practices

### API Design
- Batch related requests
- Use pagination for large datasets
- Implement caching for frequently accessed data
- Consider webhooks for event-driven updates

### Error Handling
- Implement exponential backoff
- Check rate limit headers
- Respect Retry-After header
- Log rate limit events

### Monitoring
- Track API usage trends
- Set alerts before limits exceeded
- Monitor error rates
- Review inefficient queries

### Planning
- Estimate API requirements upfront
- Plan for growth and spikes
- Create separate keys for different needs
- Consider plan upgrade if approaching limits

## Support

For rate limit questions:
- **Documentation**: https://docs.clouddash.io/api/rate-limits
- **Email**: support@clouddash.io
- **Response Time**: 24 hours
- Include API usage metrics when contacting
