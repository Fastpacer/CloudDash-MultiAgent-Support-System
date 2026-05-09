# Metric Ingestion Delay

## Problem
Metrics are arriving in Clouddash with significant delay. Real-time dashboards show data from 5-10 minutes ago instead of current values. Alert evaluation using delayed metrics causes false negatives.

## Root Causes

### 1. CloudWatch Data Latency
- AWS CloudWatch itself has inherent latency (typically 1-2 minutes)
- Detailed monitoring enabled (1-minute granularity) adds latency
- Custom metrics sent to CloudWatch have delays
- Regional differences in metric availability

### 2. Clouddash Sync Interval Too Long
- Metrics fetched every 15-30 minutes instead of 1-5 minutes
- Configured interval too conservative
- Sync configuration not updated after scaling

### 3. Query Aggregation Issues
- Metrics aggregated over long time windows
- Using 5-minute aggregation when 1-minute needed
- Collecting historical data causes slow ingestion of fresh data
- Query execution time too long

### 4. API Rate Limiting
- Clouddash hitting CloudWatch API rate limits
- Too many simultaneous requests
- Throttled requests retried later
- Rate limit quota exhausted

### 5. Processing Bottleneck
- Database ingestion pipeline slow
- Data queue building up
- Insufficient processing capacity
- Resource contention on Clouddash servers

### 6. Network Latency
- Slow connection between Clouddash and AWS
- Routing issue causing high latency
- VPN latency if using private connection
- ISP or regional network issues

### 7. Metric Transformation Issues
- Custom metric mapping or calculations slow
- Data enrichment adds processing time
- Complex aggregation rules running
- Third-party integrations adding delay

## Diagnostic Steps

### Step 1: Measure Actual Delay
1. Create a metric with known, real-time update pattern
   - Example: Count of API requests (updates every second)
2. Note timestamp when metric is generated at source
3. Check when same metric appears in Clouddash dashboard
4. Calculate difference in time

Typical latency:
- **<2 minutes**: Normal (AWS + Clouddash)
- **2-5 minutes**: Acceptable for most use cases
- **5-10 minutes**: Noticeable delay, investigate
- **>10 minutes**: Significant issue, needs fixing

### Step 2: Identify Source of Delay
1. Check CloudWatch metric publication lag:
   - AWS Console → CloudWatch
   - Look at metric timestamp vs current time
   - If CloudWatch shows old data, AWS is lagging

2. Compare Clouddash with AWS Console:
   - Open AWS CloudWatch dashboard
   - Open Clouddash dashboard showing same metric
   - See if Clouddash is further behind than AWS Console
   - If Clouddash is 5min behind AWS, Clouddash is the bottleneck

### Step 3: Check Sync Interval
1. Go to **Settings** → **Integrations** → **AWS**
2. Look for **Sync Interval** or **Polling Frequency** setting
3. Note configured interval:
   - 1 minute: Most frequent (may hit rate limits)
   - 5 minutes: Standard default
   - 15 minutes: Conservative (causes delay)

### Step 4: Monitor Sync Performance
1. Go to **Settings** → **Observability** → **Metrics**
2. Look for:
   - API latency: How long each sync takes
   - Queue depth: How many metrics waiting
   - Throughput: Metrics ingested per second
3. If API latency >2 min or queue building, processing is bottleneck

### Step 5: Review Aggregation Settings
1. Go to dashboard with delayed metric
2. Click on metric/widget
3. Check **Aggregation Interval**:
   - 1 minute: Most granular, freshest data
   - 5 minutes: Standard trade-off
   - Higher: Older data aggregated together
4. Compare with ingestion interval

### Step 6: Check API Metrics
1. AWS Console → CloudWatch → Metrics
2. Search for "Clouddash" or "ThrottledRequests"
3. Look for spikes in API throttling
4. Check if quota exceeded errors

### Step 7: Test Network Path
1. Test latency from Clouddash to AWS:
   ```bash
   ping cloudwatch.us-east-1.amazonaws.com
   # Latency should be <100ms
   ```
2. If >200ms, network issue
3. Check VPN latency if using private connection

## Resolution Steps

### Quick Fix: Reduce Sync Interval

1. **Access Sync Settings**
   - Go to **Settings** → **Integrations** → **AWS CloudWatch**
   - Find **Sync Interval** or **Polling Frequency**

2. **Decrease Interval**
   - Current: 15 minutes → Change to 5 minutes
   - Current: 5 minutes → Change to 1-2 minutes
   - Shorter interval = fresher data

3. **Test and Monitor**
   - Save settings
   - Wait 2-3 sync cycles
   - Observe metric freshness
   - Check if more responsive

### Fix: Adjust Aggregation

1. **Review Aggregation Settings**
   - Dashboard settings
   - Individual widget settings
   - Current aggregation interval

2. **Use Finer Granularity**
   - Change from 5-minute to 1-minute aggregation
   - Means each data point represents 1 minute
   - More fresh data points available
   - Updates more frequently

3. **Trade-off Considerations**
   - 1-minute granularity: More fresh, more storage
   - 5-minute granularity: Smoother, less storage
   - Choose based on monitoring need

### Fix: Implement Query Caching

1. **Enable Result Caching**
   - Settings → Performance → Query Caching
   - Set cache TTL to 30-60 seconds
   - Repeated queries reuse recent results
   - Reduces API calls

2. **Balance Freshness**
   - Cache TTL = 30 sec: Fresh data, some cache hits
   - Cache TTL = 60 sec: More cache reuse, slightly stale
   - Choose based on needs

### Fix: Reduce Metric Volume

If ingesting thousands of metrics:

1. **Identify Unnecessary Metrics**
   - Go to metric catalog
   - Review all ingested metrics
   - Identify unused or low-value metrics

2. **Exclude Unneeded Metrics**
   - AWS Integration settings
   - Configure metric filters/exclusions
   - Don't ingest irrelevant metrics
   - Reduces processing load

3. **Use Aggregates Instead**
   - Instead of ingesting 100 individual metrics
   - Use CloudWatch aggregation to create composite metrics
   - Ingest fewer but more useful metrics

### Fix: Upgrade Processing Capacity

If bottleneck is Clouddash processing:

1. **Check Service Load**
   - Settings → System Metrics
   - CPU usage: Should be <70%
   - Memory usage: Should be <80%
   - Database connections: Should have headroom

2. **Upgrade if Needed**
   - If resources near capacity
   - Upgrade to higher tier plan
   - Allocates more compute resources
   - Improves ingestion throughput

### Fix: Handle Rate Limiting

If AWS is throttling requests:

1. **Check Rate Limit Status**
   - CloudWatch API limit: 400 requests/second
   - Verify not approaching limit
   - Check if other tools also querying CloudWatch

2. **Request Higher Limit**
   - AWS Console → Service Quotas
   - Search for CloudWatch
   - Request increase if applicable
   - AWS reviews request (usually approves for legitimate use)

3. **Optimize Request Patterns**
   - Batch metric queries when possible
   - Use metric statistics API efficiently
   - Reduce redundant queries

### Fix: Optimize Network Path

If network latency is cause:

1. **Check Latency**
   ```bash
   ping -c 5 cloudwatch.us-east-1.amazonaws.com
   # Check average latency
   ```

2. **If Using VPN**
   - Test latency without VPN
   - VPN adds overhead
   - Consider direct AWS connection if critical
   - AWS Direct Connect for low-latency access

3. **Regional Optimization**
   - Use regional endpoints close to data
   - If metrics in us-west-2, query us-west-2 endpoint
   - Reduces data transfer overhead

### Fix: Implement Intelligent Caching

For improved real-time feel:

1. **Cache Local Recent Values**
   - Dashboards cache last known value
   - Display with visual indicator (stale, cached)
   - Updates as fresh data arrives
   - Feels more responsive to users

2. **Predictive Display**
   - Show trend of last point
   - Indicate data is updating
   - Reduces perceived lag

## Verification

After applying fixes:

1. **Measure New Latency**
   - Use same test metric from Step 1
   - Measure time from generation to display
   - Should see improvement
   - Target: <5 minutes

2. **Monitor Dashboard Freshness**
   - Compare Clouddash with AWS Console
   - Should be similar latency
   - Charts updating regularly
   - Timestamps recent

3. **Verify Alert Responsiveness**
   - Create test alert condition
   - Trigger manually
   - Alert should fire quickly
   - Check alert history for timestamp

4. **Check Ongoing Performance**
   - Monitor metrics over 24 hours
   - Latency should be consistent
   - No degradation over time
   - Queue depths normal

## Prevention

- Monitor ingestion latency weekly
- Review sync intervals quarterly
- Adjust aggregation based on use case
- Keep metric volume reasonable
- Monitor AWS service health
- Set alerts for ingestion delays >5 min

## When to Escalate

Contact support if:
- Latency still >10 minutes after optimization
- Specific metrics have high latency but others normal
- AWS confirms no CloudWatch issues
- Need custom metric aggregation strategies
- Requires dedicated ingestion pipeline
- Performance requirements <1 minute latency
