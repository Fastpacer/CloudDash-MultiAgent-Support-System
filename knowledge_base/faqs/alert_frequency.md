# Alert Frequency Configuration

## Overview
Alert frequency controls how often Clouddash will notify you about the same condition. This helps prevent alert fatigue while ensuring you stay informed of critical issues.

## Alert Frequency Options

### Real-Time
- **Trigger**: Immediately upon condition detection
- **Best for**: Critical, page-worthy incidents
- **Example**: Database connection failures, authentication service down

### Every 5 Minutes
- **Trigger**: Once per 5-minute window if condition persists
- **Best for**: Active incidents requiring frequent updates
- **Example**: High CPU usage, memory pressure

### Every 15 Minutes
- **Trigger**: Once per 15-minute window
- **Best for**: Standard operational alerts
- **Example**: Slow response times, elevated error rates

### Hourly
- **Trigger**: Once per hour if condition continues
- **Best for**: Non-critical but monitored conditions
- **Example**: Minor performance degradation

### Daily Digest
- **Trigger**: Single summary email at specified time
- **Best for**: Informational alerts
- **Example**: Daily capacity reports, trend summaries

## How to Set Alert Frequency

1. Navigate to **Alerts** → **Alert Rules**
2. Select the alert you want to configure
3. Click **Edit**
4. Find the **Notification Frequency** section
5. Select your preferred frequency
6. Choose delivery method (Email, Slack, Webhook)
7. Click **Save**

## Escalation Frequency

For critical alerts, enable escalation:
1. After initial alert at selected frequency
2. Escalate to manager after 30 minutes
3. Page on-call team after 1 hour
4. Contact security team for security alerts after 2 hours

## Suppress Window

Prevent duplicate alerts during maintenance:
1. Go to alert settings
2. Enable **Suppress Duplicates for X minutes**
3. Set duration (5-120 minutes)
4. Alerts matching same conditions won't repeat during window

## Best Practices

- **Critical**: Real-time or 5-minute frequency
- **Warning**: 15-minute frequency
- **Info**: Hourly or daily digest
- **Test alerts**: Quiet hours to reduce noise
- **Review monthly**: Tune frequency based on actual incidents

## Dynamic Frequency

For variable workloads, use intelligent frequency:
- Increase frequency during business hours
- Reduce frequency during off-hours
- Escalate quickly during on-call rotations

## Troubleshooting

**Not receiving alerts**
- Verify notification channel is configured
- Check alert rule is enabled
- Confirm frequency isn't set to "Disabled"

**Too many alerts**
- Increase frequency interval
- Apply more specific conditions
- Use alert grouping/correlation
