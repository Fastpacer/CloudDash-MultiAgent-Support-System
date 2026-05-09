# AWS Alerts Not Firing After Credential Update

## Problem
AWS alerts configured in Clouddash have stopped firing after updating AWS credentials or rotating API keys. Previously working alert rules no longer trigger notifications.

## Root Causes

### 1. Credentials Not Updated in Clouddash
After rotating AWS access keys or credentials:
- The old credentials remain configured in Clouddash
- CloudWatch API calls fail with 401 Unauthorized
- Metric collection stops silently
- Alerts appear "armed" but never trigger

### 2. CloudWatch Sync Failure
- Credential update breaks CloudWatch sync
- New credentials lack proper permissions
- IAM role missing CloudWatch:GetMetricData permissions
- Regional endpoint configuration mismatch

### 3. Credential Expiration
- Temporary credentials expired
- Session token not refreshed
- STS AssumeRole failing
- IAM policy expiration

## Diagnostic Steps

### Step 1: Verify Credentials in Clouddash
1. Go to **Settings** → **Integrations** → **AWS**
2. Check the **Last Synced** timestamp
3. If it says "Never" or dates before credential update, credentials are stale
4. Click **Test Connection** to validate

### Step 2: Check CloudWatch Connectivity
1. Navigate to **Integrations** → **AWS CloudWatch**
2. Look for error messages:
   - "InvalidCredentials"
   - "AccessDenied"
   - "UnauthorizedOperation"
3. Connection status should show "Connected" with recent timestamp

### Step 3: Review Alert Rule Status
1. Go to **Alerts** → **Alert Rules**
2. Filter by alert type "CloudWatch Metrics"
3. Check **Last Evaluated** column:
   - If recent: Alert engine is working
   - If stale (>15 min): Integration is failing
4. Click rule to see evaluation history

### Step 4: Check IAM Permissions
Confirm the AWS IAM user/role has these permissions:
```
cloudwatch:GetMetricData
cloudwatch:ListMetrics
cloudwatch:GetMetricStatistics
cloudwatch:DescribeAlarms
ec2:DescribeInstances (for resource discovery)
```

## Resolution Steps

### Quick Fix: Re-authenticate Credentials

1. **Go to Settings**
   - Navigate to **Settings** → **Integrations** → **AWS**

2. **Disconnect Current Integration**
   - Click **Disconnect** button
   - Confirm the action
   - This preserves alert rules but disconnects sync

3. **Reconnect with New Credentials**
   - Click **Connect AWS Account**
   - Use AWS login to authorize
   - Or provide new Access Key ID and Secret Access Key
   - Select appropriate regions

4. **Trigger CloudWatch Resync**
   - After connection, click **Force Sync** 
   - Wait 2-3 minutes for metrics to repopulate
   - Check **Last Synced** timestamp updates

5. **Verify Alert Firing**
   - Check if alert rules show recent evaluation
   - Test with manual alert trigger if available
   - Monitor alert history for new events

### Advanced Fix: Update Credentials Directly

If OAuth reconnection fails:

1. **Get New Access Credentials**
   - Log into AWS console
   - Create or rotate IAM access keys
   - Ensure proper CloudWatch permissions

2. **Update in Clouddash API**
   ```
   PATCH /api/integrations/aws
   {
     "access_key_id": "AKIA...",
     "secret_access_key": "...",
     "regions": ["us-east-1", "us-west-2"]
   }
   ```

3. **Verify Through UI**
   - Settings should show "Connected"
   - Test connection succeeds
   - CloudWatch metrics appear

### Fixing Permission Issues

If error is "AccessDenied":

1. **Verify IAM Role** in AWS Console
   - Service: EC2, Lambda, or direct user
   - Attached policy should include CloudWatch:GetMetricData
   - Check inline policies too

2. **Add Missing Permissions** if needed
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": [
           "cloudwatch:GetMetricData",
           "cloudwatch:ListMetrics",
           "cloudwatch:GetMetricStatistics"
         ],
         "Resource": "*"
       }
     ]
   }
   ```

3. **Reconnect** after permissions updated (allow 5 min for propagation)

## Verification

After applying fixes:

1. **Check Integration Status**
   - Go to Integrations
   - AWS shows "Connected"
   - Last Synced within last 5 minutes

2. **Verify Alert Evaluation**
   - Alert rules show recent **Last Evaluated** time
   - No error messages in rule details

3. **Test Alert Firing**
   - Create a test metric or threshold
   - Trigger condition manually
   - Confirm notification received

4. **Monitor Audit Log**
   - Go to **Settings** → **Audit Logs**
   - Search for "AWS" or "integration"
   - Verify successful reconnection event

## Prevention

- Rotate AWS credentials quarterly through change management
- Update Clouddash credentials immediately after AWS rotation
- Set calendar reminders for credential rotation
- Test integrations after updates before issues arise
- Configure backup notification channel (Slack + Email)

## When to Escalate

Contact support if:
- Credentials are correct but still showing errors
- CloudWatch sync fails even after reconnection
- Permission error persists after updating IAM policy
- Multiple regions affected by same issue
- Unable to restore alert functionality
