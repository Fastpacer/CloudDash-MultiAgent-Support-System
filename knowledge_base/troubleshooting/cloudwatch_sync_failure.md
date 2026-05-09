# CloudWatch Sync Failure

## Problem
CloudWatch metrics are not syncing to Clouddash. Dashboard shows "No Data" or metrics stop updating. Last sync shows stale timestamp or "Never".

## Root Causes

### 1. AWS Credentials Expired or Invalid
- Access keys rotated in AWS but not updated in Clouddash
- Temporary credentials expired
- Secret access key incorrect or corrupted
- IAM user/role deleted

### 2. Missing IAM Permissions
- CloudWatch:GetMetricData permission missing
- CloudWatch:ListMetrics not granted
- EC2:DescribeInstances missing (for resource discovery)
- Regional restrictions on IAM policy

### 3. Network Connectivity Issues
- Clouddash service cannot reach AWS CloudWatch API
- Firewall blocking outbound AWS API calls
- VPN connection dropped
- DNS resolution failure for cloudwatch endpoints

### 4. AWS API Rate Limiting
- CloudWatch API throttled (>400 requests/second)
- Quota exceeded
- Regional rate limits hit
- Spike in API calls from other sources

### 5. CloudWatch Region Misconfiguration
- Wrong regions selected in integration
- Data exists in region not configured
- Regional endpoint incorrect
- Cross-region sync not configured

### 6. Service Availability Issues
- AWS CloudWatch API degradation
- AWS regional service maintenance
- Clouddash sync service down
- Database connection pool exhausted

## Diagnostic Steps

### Step 1: Check Integration Status
1. Go to **Settings** → **Integrations** → **AWS CloudWatch**
2. Check **Status**:
   - **Connected**: Integration active (green)
   - **Error**: Connection failed (red)
   - **Syncing**: Currently fetching data (blue)
3. Note **Last Synced** timestamp
   - Should be recent (within 5 minutes)
   - If stale or "Never", sync is failing

### Step 2: View Error Message
1. Click **CloudWatch Integration** tile
2. Expand **Error Details** section if visible
3. Common errors:
   - "InvalidClientTokenId": Credentials invalid
   - "AccessDenied": Insufficient IAM permissions
   - "Throttling": Rate limited by AWS
   - "ServiceUnavailable": AWS API issue
4. Note exact error message

### Step 3: Test AWS Credentials
1. Go to **Settings** → **Integrations** → **AWS**
2. Click **Test Connection** button
3. Should show success within 2-5 seconds
4. If fails, shows error reason
5. Try with different regions if regional issue suspected

### Step 4: Verify IAM Permissions
In AWS Console:
1. Go to **IAM** → **Users** or **Roles**
2. Find the IAM user/role Clouddash uses
3. Check attached policies include:
   ```
   cloudwatch:GetMetricData
   cloudwatch:ListMetrics
   cloudwatch:GetMetricStatistics
   ec2:DescribeInstances (if using auto-discovery)
   ```
4. If missing, permissions need adding

### Step 5: Check Configured Regions
1. In Clouddash, go to **AWS Integration** settings
2. Look at **Regions** list
3. Compare with regions where metrics actually exist
4. Verify all needed regions are included

### Step 6: Check AWS Service Status
1. Navigate to AWS Service Health Dashboard: https://status.aws.amazon.com
2. Look for CloudWatch service status
3. Check each region you use
4. If showing issues, wait for AWS to resolve

### Step 7: Check Firewall/Network
1. Confirm outbound AWS API calls allowed
2. If behind corporate firewall:
   - Confirm AWS API endpoints whitelisted
   - Check firewall logs for blocked requests
3. Test from different network if possible

## Resolution Steps

### Quick Fix: Disconnect and Reconnect

1. **Go to AWS Integration**
   - Settings → Integrations → AWS

2. **Disconnect Current Integration**
   - Click **Disconnect**
   - Confirm action
   - Alert rules preserved, just disconnected

3. **Reconnect**
   - Click **Connect AWS Account**
   - Use AWS SSO or enter credentials
   - Authorize Clouddash to access CloudWatch
   - Select regions
   - Complete connection

4. **Monitor Sync**
   - Watch Last Synced timestamp
   - Should update within 5 minutes
   - Verify metrics appear in dashboards

### Fix Credentials

1. **Generate New AWS Credentials**
   - AWS Console → IAM → Users
   - Find Clouddash's IAM user
   - Create new Access Key (delete old if compromised)
   - Copy Access Key ID and Secret Access Key

2. **Update in Clouddash**
   - Go to **AWS Integration Settings**
   - Update Access Key ID
   - Update Secret Access Key
   - Click **Save**
   - Test connection

3. **Verify Sync Resumes**
   - Check Last Synced timestamp updates
   - Metrics should reappear in dashboards

### Fix IAM Permissions

1. **Attach Required Policy**
   - AWS Console → IAM → Users/Roles
   - Find Clouddash's user/role
   - Click **Add permissions** → **Attach policies**
   - Search and select managed policy:
     - `CloudWatchReadOnlyAccess` (includes all needed)
   - Or create custom policy:

   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": [
           "cloudwatch:GetMetricData",
           "cloudwatch:ListMetrics",
           "cloudwatch:GetMetricStatistics",
           "cloudwatch:DescribeAlarms"
         ],
         "Resource": "*"
       },
       {
         "Effect": "Allow",
         "Action": [
           "ec2:DescribeInstances",
           "ec2:DescribeTags"
         ],
         "Resource": "*"
       }
     ]
   }
   ```

2. **Allow Time for Propagation**
   - IAM changes can take 5-10 minutes
   - Wait before testing

3. **Test Connection Again**
   - Go to CloudWatch integration
   - Click **Test Connection**
   - Should succeed

### Fix Region Configuration

1. **Check What Regions Have Data**
   - AWS Console → CloudWatch → Dashboard
   - Note which regions contain metrics

2. **Update Clouddash Regions**
   - Settings → AWS Integration → Edit
   - Expand **Regions** section
   - Check all regions with data
   - Uncheck unused regions
   - Save

3. **Force Resync**
   - Click **Force Sync** (if available)
   - Or disconnect/reconnect
   - New regions should start syncing

### Handle Rate Limiting

If error is "Throttling" or "Rate Exceeded":

1. **Check CloudWatch Usage**
   - AWS Console → CloudWatch → Dashboard Metrics
   - Look for unusual API activity
   - Check if other tools also querying CloudWatch

2. **Optimize Query Frequency**
   - In Clouddash Settings → Sync Settings
   - Increase sync interval (default 5 min)
   - Reduce number of metrics fetched
   - Exclude unused metrics

3. **Request Quota Increase**
   - AWS Console → Service Quotas
   - Search "CloudWatch API Throttling"
   - Request increase if needed

### Fix Network Issues

1. **Verify AWS Endpoints Accessible**
   - Test from Clouddash server:
   ```
   ping cloudwatch.us-east-1.amazonaws.com
   telnet cloudwatch.us-east-1.amazonaws.com 443
   ```

2. **If Behind Firewall**
   - Whitelist AWS API endpoints:
     - `cloudwatch.*.amazonaws.com`
     - `ec2.*.amazonaws.com`
   - Check firewall logs for blocked requests

3. **Test Network Path**
   - Try from different network if possible
   - VPN connection stable
   - No DNS issues

## Verification

After applying fixes:

1. **Check Integration Status**
   - Green "Connected" status
   - Last Synced timestamp recent (within 5 min)
   - No error message displayed

2. **Verify Metrics Appearing**
   - Go to a dashboard with CloudWatch metrics
   - Metrics should show data
   - Not showing "No Data" or gaps
   - Charts have recent data points

3. **Monitor Ongoing Sync**
   - Return to integrations page
   - Watch Last Synced timestamp auto-update
   - Every 5 minutes (or your configured interval)

4. **Test Alert Evaluation**
   - Create temporary test alert
   - Verify alert rule evaluates
   - Check alert history shows recent evaluations
   - Confirms sync still working

## Prevention

- Monitor sync status weekly
- Set alerts for sync failures
- Rotate AWS credentials on quarterly schedule
- Update Clouddash immediately after AWS credential changes
- Review IAM permissions quarterly
- Test sync after AWS infrastructure changes

## When to Escalate

Contact support if:
- All troubleshooting steps completed but still failing
- Credentials and permissions verified correct but sync still fails
- Multiple integrations showing same issue
- Error message suggests service bug
- AWS support confirms no service issues on their end
