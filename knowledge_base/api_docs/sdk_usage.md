# SDK Usage Guide

## Overview
Clouddash provides SDKs for popular programming languages to simplify API integration. SDKs handle authentication, error handling, and payload formatting automatically.

## Available SDKs

### Official SDKs

| Language | Package | Repository |
|----------|---------|------------|
| Python | `clouddash-sdk` | https://github.com/clouddash/sdk-python |
| JavaScript/Node.js | `@clouddash/sdk` | https://github.com/clouddash/sdk-js |
| Go | `github.com/clouddash/sdk-go` | https://github.com/clouddash/sdk-go |
| Java | `com.clouddash:sdk` | https://github.com/clouddash/sdk-java |

### Community SDKs

- Ruby: `clouddash-rb` (community maintained)
- PHP: `clouddash/php-sdk` (community maintained)
- .NET: `Clouddash.Sdk` (community maintained)

## Python SDK

### Installation

```bash
pip install clouddash-sdk
```

### Basic Usage

```python
from clouddash import ClouddashClient

# Initialize client
client = ClouddashClient(api_key='sk_live_your_api_key')

# List metrics
metrics = client.metrics.list()
for metric in metrics:
    print(metric.name, metric.value)

# Get specific metric
metric = client.metrics.get('metric_id')
print(metric.value)
```

### Working with Alerts

```python
from clouddash import ClouddashClient

client = ClouddashClient(api_key='sk_live_your_api_key')

# List all alerts
alerts = client.alerts.list()

# Get alert by ID
alert = client.alerts.get('alert_123')

# Create alert
new_alert = client.alerts.create(
    name='High CPU Usage',
    metric_id='cpu_metric',
    threshold=80,
    comparison='greater_than'
)

# Update alert
alert.threshold = 85
alert.save()

# Delete alert
client.alerts.delete('alert_123')
```

### Working with Dashboards

```python
# Create dashboard
dashboard = client.dashboards.create(
    name='Production Overview',
    description='Main production metrics'
)

# Add widget to dashboard
widget = dashboard.add_widget(
    title='CPU Usage',
    metric_id='cpu_metric',
    type='line_chart'
)

# Update dashboard
dashboard.refresh_interval = 300  # 5 minutes
dashboard.save()

# List dashboards
dashboards = client.dashboards.list()
```

### Error Handling

```python
from clouddash import ClouddashClient
from clouddash.exceptions import ClouddashError, RateLimitError

client = ClouddashClient(api_key='sk_live_your_api_key')

try:
    metric = client.metrics.get('invalid_id')
except RateLimitError as e:
    print(f"Rate limited. Wait {e.retry_after} seconds")
except ClouddashError as e:
    print(f"Error: {e.message}")
```

## JavaScript/Node.js SDK

### Installation

```bash
npm install @clouddash/sdk
```

### Basic Usage

```javascript
const { ClouddashClient } = require('@clouddash/sdk');

// Initialize client
const client = new ClouddashClient({
  apiKey: 'sk_live_your_api_key'
});

// List metrics
const metrics = await client.metrics.list();
metrics.forEach(metric => {
  console.log(metric.name, metric.value);
});

// Get specific metric
const metric = await client.metrics.get('metric_id');
console.log(metric.value);
```

### Working with Alerts

```javascript
// Create alert
const alert = await client.alerts.create({
  name: 'High CPU Usage',
  metricId: 'cpu_metric',
  threshold: 80,
  comparison: 'greater_than'
});

// Update alert
alert.threshold = 85;
await alert.save();

// List alerts
const alerts = await client.alerts.list();

// Delete alert
await client.alerts.delete('alert_123');
```

### Working with Webhooks

```javascript
// Create webhook
const webhook = await client.webhooks.create({
  name: 'Alert Notifier',
  url: 'https://your-api.example.com/alerts',
  events: ['alert_fired', 'alert_resolved'],
  authentication: {
    type: 'bearer_token',
    token: 'your_token'
  }
});

// Test webhook
const result = await client.webhooks.test('webhook_id');
if (result.success) {
  console.log('Webhook delivery successful');
}

// List webhooks
const webhooks = await client.webhooks.list();
```

### Error Handling

```javascript
const { ClouddashClient, RateLimitError } = require('@clouddash/sdk');

const client = new ClouddashClient({
  apiKey: 'sk_live_your_api_key'
});

try {
  const metric = await client.metrics.get('invalid_id');
} catch (error) {
  if (error instanceof RateLimitError) {
    console.log(`Rate limited. Wait ${error.retryAfter} seconds`);
  } else {
    console.log(`Error: ${error.message}`);
  }
}
```

## Go SDK

### Installation

```bash
go get github.com/clouddash/sdk-go
```

### Basic Usage

```go
package main

import (
    "fmt"
    "github.com/clouddash/sdk-go"
)

func main() {
    client := clouddash.NewClient("sk_live_your_api_key")
    
    // List metrics
    metrics, err := client.Metrics.List()
    if err != nil {
        fmt.Println("Error:", err)
        return
    }
    
    for _, metric := range metrics {
        fmt.Println(metric.Name, metric.Value)
    }
}
```

### Working with Alerts

```go
// Create alert
alert, err := client.Alerts.Create(&clouddash.CreateAlertRequest{
    Name:       "High CPU",
    MetricID:   "cpu_metric",
    Threshold:  80,
    Comparison: "greater_than",
})

// Update alert
alert.Threshold = 85
err = alert.Save()

// Delete alert
err = client.Alerts.Delete("alert_123")
```

## Java SDK

### Installation

Add to Maven `pom.xml`:
```xml
<dependency>
    <groupId>com.clouddash</groupId>
    <artifactId>sdk</artifactId>
    <version>1.0.0</version>
</dependency>
```

Or Gradle `build.gradle`:
```gradle
dependencies {
    implementation 'com.clouddash:sdk:1.0.0'
}
```

### Basic Usage

```java
import com.clouddash.ClouddashClient;
import com.clouddash.models.Metric;

public class Example {
    public static void main(String[] args) {
        ClouddashClient client = new ClouddashClient("sk_live_your_api_key");
        
        // List metrics
        List<Metric> metrics = client.getMetrics().list();
        for (Metric metric : metrics) {
            System.out.println(metric.getName() + ": " + metric.getValue());
        }
    }
}
```

### Working with Alerts

```java
import com.clouddash.models.Alert;

// Create alert
Alert alert = client.getAlerts().create(new CreateAlertRequest()
    .setName("High CPU")
    .setMetricId("cpu_metric")
    .setThreshold(80)
    .setComparison("greater_than"));

// Update alert
alert.setThreshold(85);
alert.save();

// Delete alert
client.getAlerts().delete("alert_123");
```

## Common Patterns

### Polling Metrics

```python
import time
from clouddash import ClouddashClient

client = ClouddashClient(api_key='your_key')

while True:
    metric = client.metrics.get('cpu_metric')
    print(f"CPU: {metric.value}%")
    time.sleep(60)  # Poll every minute
```

### Batch Processing

```python
# Efficient: Fetch multiple metrics at once
metrics = client.metrics.list(
    filter={'tag': 'production'},
    limit=100
)

for metric in metrics:
    process_metric(metric)
```

### Pagination

```python
# Get all metrics with pagination
page = 1
all_metrics = []

while True:
    metrics = client.metrics.list(page=page, per_page=50)
    all_metrics.extend(metrics)
    if len(metrics) < 50:
        break
    page += 1
```

### Error Retry Logic

```python
import time
from clouddash.exceptions import ClouddashError

def retry_operation(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except ClouddashError as e:
            if attempt == max_retries - 1:
                raise
            wait_time = 2 ** attempt  # Exponential backoff
            print(f"Attempt {attempt + 1} failed, retrying in {wait_time}s")
            time.sleep(wait_time)

# Usage
result = retry_operation(lambda: client.metrics.get('metric_123'))
```

### Working with Webhooks

```python
# Create webhook that posts to endpoint
webhook = client.webhooks.create(
    name='Slack Alerts',
    url='https://hooks.slack.com/services/YOUR/WEBHOOK/URL',
    events=['alert_fired', 'alert_resolved'],
    authentication={'type': 'custom'},
    headers={'X-Custom': 'value'}
)

# Test webhook
result = client.webhooks.test(webhook.id)
if result.success:
    print("Webhook working!")
```

## SDK Configuration

### Setting Base URL

```python
# Use self-hosted instance
client = ClouddashClient(
    api_key='sk_live_your_api_key',
    base_url='https://clouddash.internal.company.com'
)
```

### Setting Timeout

```python
# Custom timeout
client = ClouddashClient(
    api_key='sk_live_your_api_key',
    timeout=30  # 30 seconds
)
```

### Logging

```python
import logging
from clouddash import ClouddashClient

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

client = ClouddashClient(api_key='sk_live_your_api_key')
```

## Best Practices

### API Key Management
- Never hardcode API keys
- Use environment variables
- Use secrets management for production
- Rotate keys regularly

### Error Handling
- Always handle rate limit errors
- Implement exponential backoff
- Log errors for debugging
- Use try-except blocks

### Performance
- Use pagination for large result sets
- Cache results when appropriate
- Implement request batching
- Consider webhook for real-time updates

### Testing
- Use mock responses for unit tests
- Test error handling paths
- Mock rate limit scenarios
- Test authentication

## Troubleshooting

### "Invalid API Key" Error
```python
# Check API key is correct and not expired
# Verify key is included in environment or constructor
# Regenerate key if suspected compromise
```

### "Connection Timeout"
```python
# Check internet connectivity
# Verify endpoint URL is correct
# Increase timeout setting
# Check firewall rules
```

### "Rate Limited"
```python
# Implement retry with backoff
# Reduce request frequency
# Check rate limit headers
# Request higher limit if needed
```

## Documentation

- **Full API Reference**: https://docs.clouddash.io/api
- **SDK GitHub**: https://github.com/clouddash
- **Community Forum**: https://community.clouddash.io

## Support

For SDK issues:
- **GitHub Issues**: Report bugs on SDK repository
- **Email**: sdk-support@clouddash.io
- **Response Time**: 24-48 hours
