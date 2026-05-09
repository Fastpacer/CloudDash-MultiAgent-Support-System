# Audit Logs

## Overview
Audit logs track all account activities including user access, configuration changes, and data modifications. Use audit logs for compliance, troubleshooting, and security monitoring.

## Accessing Audit Logs

### View Audit Logs

1. Go to **Settings** → **Audit Logs**
2. List shows recent activities (newest first)
3. Each entry includes:
   - Timestamp
   - User who performed action
   - Action/event type
   - Resource affected
   - Result (success/failure)
   - Additional details

### Audit Log Columns

| Column | What It Shows |
|--------|---------------|
| **Timestamp** | Exact date and time (UTC) |
| **User** | Email of user who performed action |
| **Event** | Type of activity (login, create, modify, delete) |
| **Resource** | Dashboard, alert, integration, etc. |
| **Status** | Success, Failed, or Pending |
| **IP Address** | Source IP if applicable |
| **Details** | Additional context or error message |

## Event Types

### Authentication Events

**login_success**
- User successfully logged in
- Includes IP address and browser/device
- Timestamp of login

**login_failed**
- Failed login attempt
- Reason: Invalid password, user not found, etc.
- IP address for tracking

**login_mfa**
- Multi-factor authentication completed
- MFA method used (TOTP, SMS, etc.)

**logout**
- User logged out
- Normal or forced logout

**sso_login**
- User logged in via SSO/SAML
- IdP name and user attributes
- Successful or failed

**password_change**
- User changed their password
- Timestamp of change

**password_reset**
- Password reset request processed
- Reset email sent or completed

### Account Management

**user_created**
- New team member added
- Email and role assigned
- By whom and when

**user_invited**
- Team member invitation sent
- Email address invited
- Invitation status (pending, accepted, expired)

**user_removed**
- Team member access revoked
- Reason if documented
- Timestamp of removal

**role_changed**
- User's role modified
- Old role → New role
- Who made the change

**role_granted**
- Additional role or permission granted
- Specific permission changed

### Dashboard Activities

**dashboard_created**
- New dashboard created
- Dashboard name and ID
- Creator email
- Creation time

**dashboard_modified**
- Dashboard configuration changed
- What was modified (widgets, settings, etc.)
- Who made change and when

**dashboard_deleted**
- Dashboard permanently deleted
- Dashboard name and ID
- Who deleted it
- Timestamp

**dashboard_shared**
- Dashboard shared with user/team
- Permission level (view, edit)
- Shared by whom

**dashboard_unshared**
- Dashboard sharing removed
- User access revoked
- Reason if documented

### Alert Activities

**alert_created**
- Alert rule created
- Alert name, metric, threshold
- Creator and timestamp

**alert_modified**
- Alert configuration changed
- What changed (threshold, frequency, etc.)
- Before and after values if available

**alert_deleted**
- Alert rule deleted
- Alert name and ID
- Who deleted and when

**alert_triggered**
- Alert fired/activated
- Trigger reason (metric value, condition)
- Timestamp

**alert_acknowledged**
- User acknowledged alert
- Who acknowledged
- Acknowledgment time

**alert_resolved**
- Alert condition cleared
- Metric returned to normal
- Resolution time

### Integration Events

**integration_created**
- New data source integration added
- Provider (AWS, GCP, Azure, etc.)
- Creation timestamp

**integration_connected**
- Integration successfully tested/connected
- Connection status and details
- Timestamp

**integration_disconnected**
- Integration connection lost or disabled
- Reason if known
- Disconnection time

**integration_modified**
- Integration settings changed
- Credentials updated, regions changed, etc.
- Who made change

**integration_deleted**
- Integration permanently removed
- Integration name and ID
- Who deleted and when

**sync_failed**
- Metric sync from data source failed
- Error message
- Provider and timestamp

### Security Events

**api_key_created**
- API key generated
- Scopes assigned
- Key ID (last 4 characters shown)

**api_key_regenerated**
- API key rotated
- Old key invalidated
- New key issued

**api_key_revoked**
- API key permanently disabled
- Revocation timestamp
- Reason if documented

**mfa_enabled**
- Multi-factor authentication activated
- MFA method used
- User and timestamp

**mfa_disabled**
- MFA turned off
- Who disabled it
- Timestamp

**settings_changed**
- Account settings modified
- What changed
- Before and after values

**permission_denied**
- Access attempt blocked
- User, resource, reason
- Timestamp

### Subscription Events

**subscription_created**
- New subscription started
- Plan tier and date
- Billing information

**subscription_upgraded**
- Plan upgraded to higher tier
- From plan → To plan
- Effective date and charge

**subscription_downgraded**
- Plan downgraded to lower tier
- From plan → To plan
- Effective date and credit

**invoice_issued**
- Invoice generated and sent
- Invoice number and amount
- Invoice date

**payment_processed**
- Payment received
- Amount and date
- Payment method

**payment_failed**
- Payment processing failed
- Reason (insufficient funds, expired card, etc.)
- Retry timestamp

## Filtering and Searching

### Quick Filters

**By Time Range:**
- Last 24 hours (default)
- Last 7 days
- Last 30 days
- Last 90 days
- Custom date range

**By Event Type:**
- Authentication
- User Management
- Dashboards
- Alerts
- Integrations
- Billing
- Security

**By User:**
- Specific team member
- Service accounts
- All users

**By Status:**
- Successful
- Failed
- Pending
- All

### Advanced Search

**Search by Keywords:**
1. Click **Advanced Search**
2. Enter search terms:
   - Event name: `dashboard_created`
   - Resource name: `Production Overview`
   - User email: `john@company.com`
   - IP address: `192.168.1.100`

**Search Operators:**
- `event:login_failed` - Only failed logins
- `user:admin@company.com` - Specific user
- `resource:dashboard` - Dashboard events only
- `status:failed` - Only failed events

### Exporting Logs

**Export to CSV:**
1. Go to Audit Logs
2. Click **Export**
3. Select date range
4. Click **Download CSV**
5. Opens in spreadsheet application
6. Contains all columns for analysis

**Filtered Export:**
1. Apply filters (time, user, event type, etc.)
2. Click **Export**
3. Only filtered logs included
4. Useful for compliance reports

## Common Use Cases

### Investigation: User Unauthorized Access

**Scenario:** Suspicious activity detected

**Steps:**
1. Search logs for the suspicious user
2. Filter by date range around suspicious activity
3. Look for `login_success` events
4. Check IP address and browser/device
5. Look at what they accessed:
   - `dashboard_viewed`
   - `metrics_queried`
6. Determine if authorized
7. If unauthorized, remove user and review security

**Query Example:**
```
user:suspicious@company.com
event:login_success
after:2024-05-01 before:2024-05-08
```

### Audit: Compliance Verification

**Scenario:** Need to verify access controls

**Steps:**
1. Export audit logs for date range
2. Filter by `role_changed` events
3. Verify all role changes authorized
4. Check `user_created` events
5. Verify all new users are valid employees
6. Check `user_removed` for departing employees
7. Export report for auditors

### Troubleshooting: Dashboard Deleted

**Scenario:** Dashboard disappeared

**Steps:**
1. Go to Audit Logs
2. Search for dashboard name: `resource:Dashboard_Name`
3. Look for `dashboard_deleted` event
4. Note who deleted it and when
5. If accidental, contact Admin to restore
6. For future prevention, review dashboard permissions

### Security: Unauthorized API Access

**Scenario:** High API usage from unknown source

**Steps:**
1. Search logs for `api_key` events
2. Filter by `api_key_created`
3. Identify keys created recently
4. Check who created and when
5. Look for unusual `login_success` from new IPs
6. If unauthorized:
   - Revoke key: `api_key_revoked`
   - Lock account temporarily
   - Notify security team

## Data Retention

### Log Retention Policy

**Standard Plans (Starter/Professional):**
- Logs retained for 90 days
- After 90 days, automatically archived
- Can request extension (contact support)

**Enterprise Plans:**
- Logs retained for 1 year
- Extended retention available
- Custom retention on request

**Archived Logs:**
- Accessible for compliance via backup
- Not visible in UI after retention expires
- Available through support request

### Exporting for Long-Term Storage

To keep logs beyond retention period:

1. Monthly: Go to **Audit Logs** → **Export**
2. Download all logs for month
3. Store in:
   - Cloud storage (S3, GCS, Azure Blob)
   - Archive system
   - Compliance management platform
4. Keep copies for audit trail

## Performance and Monitoring

### High-Volume Activity

If logs show unusual volume:

1. Identify source:
   - Specific user?
   - Specific event type?
   - Specific time range?

2. Investigate:
   - Scheduled job running?
   - Runaway script?
   - Attack/brute force?

3. Take action:
   - If legitimate, whitelist/document
   - If not, block/disable
   - Update security rules

### Alert on Suspicious Activity

**Set Up Monitoring:**
1. Export logs regularly (daily)
2. Filter for:
   - Multiple failed logins (same user)
   - Bulk user deletions
   - API key creation spikes
   - Permission escalations
3. Alert if thresholds exceeded
4. Investigate quickly

## Compliance and Auditing

### SOC 2 / ISO 27001 Compliance

Audit logs support compliance by providing:
- Access trail for authentication
- Change history for configurations
- User action tracking
- Security event logging

**For Compliance:**
1. Enable audit log review monthly
2. Export and store for required period
3. Monitor for unauthorized access
4. Document remediation actions
5. Provide logs to auditors on request

### GDPR Right to Access

**User Data Subject Access Request:**

1. User requests access to their data
2. Go to Audit Logs
3. Filter by user email: `user:request@company.com`
4. Export all activities
5. Provide user their data
6. Keep documentation of response

### Data Retention for Legal Hold

**During Investigation:**
1. Go to Audit Logs
2. Export all logs for relevant period
3. Do not delete or auto-purge
4. Store securely with restricted access
5. Notify support of legal hold to suspend archival

## Troubleshooting

### "No events found"
- Expand date range
- Check filters aren't too restrictive
- Verify event actually occurred
- Check user has access to logs

### "Can't export logs"
- Check user has Admin role
- Verify date range valid
- Try smaller date range
- Contact support if issue persists

### "Logs not showing recent activity"
- There may be delay (usually <1 minute)
- Refresh page
- Check user has logs permission
- Verify action actually executed

## Best Practices

### Regular Review
- Review logs weekly as routine
- Check for suspicious patterns
- Monitor key metrics (logins, changes)
- Export monthly for archival

### Security Monitoring
- Alert on repeated failed logins
- Track API key creation
- Monitor permission changes
- Track integration credential updates

### Compliance
- Export audit logs periodically
- Maintain retention policy
- Document security incidents
- Keep audit trail intact

### Investigation Protocol
1. Identify suspicious activity
2. Search relevant logs
3. Determine scope and impact
4. Document findings
5. Take corrective action
6. Update security practices

## Support

For audit log questions:
- **Documentation**: https://docs.clouddash.io/audit-logs
- **Email**: support@clouddash.io
- **Compliance Support**: compliance@clouddash.io
- **Response Time**: 24 hours
- For legal holds, contact support immediately
