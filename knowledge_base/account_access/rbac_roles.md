# RBAC Roles and Permissions

## Overview
Clouddash uses Role-Based Access Control (RBAC) to manage permissions. Assign roles to team members to control what they can access and modify.

## Available Roles

### Admin
**What They Can Do:**
- Full account access and control
- Manage team members and roles
- Access billing and subscription settings
- View and modify all dashboards and alerts
- Configure integrations and API keys
- Access audit logs
- Delete account or data

**When to Use:**
- Account owner
- Team lead or manager
- Senior operations engineers

**Permissions:**
- `account:read`, `account:write`, `account:delete`
- `team:manage`
- `billing:read`, `billing:write`
- `dashboards:*` (all operations)
- `alerts:*` (all operations)
- `integrations:*` (all operations)
- `settings:*` (all operations)

### Manager
**What They Can Do:**
- Create and manage dashboards
- Create and manage alerts
- View team members
- Cannot manage integrations or billing
- Cannot delete account
- Can moderate team activity

**When to Use:**
- Team leads
- Engineering managers
- Project leads

**Permissions:**
- `dashboards:read`, `dashboards:write`, `dashboards:delete`
- `alerts:read`, `alerts:write`, `alerts:delete`
- `team:read`
- `metrics:read`
- `integrations:read` (view only)
- Cannot access billing or account settings

### Developer
**What They Can Do:**
- Create and modify dashboards
- View and manage own alerts
- View metrics data
- Cannot modify other users' dashboards
- Cannot manage team or integrations

**When to Use:**
- Individual developers
- Engineers
- Analysts

**Permissions:**
- `dashboards:read`, `dashboards:write` (own dashboards)
- `alerts:read`, `alerts:write` (own alerts)
- `metrics:read`
- Limited cross-team visibility

### Viewer
**What They Can Do:**
- View dashboards
- View alerts (read-only)
- View metrics
- Cannot create or modify anything
- Cannot access settings

**When to Use:**
- Stakeholders
- Non-technical team members
- Auditors
- Executives (briefing dashboards)

**Permissions:**
- `dashboards:read`
- `alerts:read`
- `metrics:read`
- No write permissions

### Billing
**What They Can Do:**
- View and pay invoices
- View subscription details
- Manage payment methods
- Cannot access technical settings
- Cannot view dashboards or metrics

**When to Use:**
- Finance team
- Accounts payable
- Billing administrators

**Permissions:**
- `billing:read`, `billing:write`
- `invoices:read`, `invoices:write`
- Cannot access technical features

### Custom Roles (Enterprise Only)

Create custom roles with specific permissions:

**Example: Compliance Officer**
- View all dashboards (compliance checking)
- Access audit logs (compliance verification)
- View integrations (no modification)
- Cannot modify dashboards or alerts
- Cannot access billing

**Example: Data Analyst**
- View metrics and reports
- Create analysis dashboards
- Cannot create alerts
- Cannot manage team or integrations

## Managing Roles

### Assigning Roles

**When Inviting New Member:**
1. Go to **Settings** → **Team Members**
2. Click **+ Invite Member**
3. Enter email address
4. Select role from dropdown
5. Click **Send Invitation**

**Changing Existing Member's Role:**
1. Go to **Settings** → **Team Members**
2. Find member in list
3. Click member name or settings icon
4. Change role from dropdown
5. Click **Save** or **Update**
6. Changes take effect immediately

### Revoking Access

**Remove Team Member:**
1. Go to **Settings** → **Team Members**
2. Find member to remove
3. Click **Remove** button
4. Confirm action
5. Member immediately loses access
6. Can reinvite later within 30 days

**Suspend Temporarily:**
- There is no suspend feature
- Must remove member to revoke access
- Can re-invite when access needed

## Permission Details

### Dashboard Permissions

| Action | Viewer | Developer | Manager | Admin |
|--------|--------|-----------|---------|-------|
| View | ✓ | ✓ | ✓ | ✓ |
| Create | ✗ | ✓ | ✓ | ✓ |
| Edit Own | ✗ | ✓ | ✓ | ✓ |
| Edit Others' | ✗ | ✗ | ✓ | ✓ |
| Delete | ✗ | ✗ | ✓ | ✓ |
| Share | ✓ | ✓ | ✓ | ✓ |

**Dashboard Sharing:**
- Viewer role can share dashboards (read-only link)
- Developer can share created dashboards
- Manager can share any dashboard
- Admin can share and manage permissions

### Alert Permissions

| Action | Viewer | Developer | Manager | Admin |
|--------|--------|-----------|---------|-------|
| View | ✓ | ✓ | ✓ | ✓ |
| Create | ✗ | ✓ | ✓ | ✓ |
| Edit Own | ✗ | ✓ | ✓ | ✓ |
| Edit Others' | ✗ | ✗ | ✓ | ✓ |
| Delete | ✗ | ✗ | ✓ | ✓ |
| Acknowledge | ✓ | ✓ | ✓ | ✓ |

### Integration Permissions

| Action | Viewer | Developer | Manager | Admin |
|--------|--------|-----------|---------|-------|
| View | ✗ | ✗ | View Only | ✓ |
| Create | ✗ | ✗ | ✗ | ✓ |
| Configure | ✗ | ✗ | ✗ | ✓ |
| Test | ✗ | ✗ | ✗ | ✓ |
| Delete | ✗ | ✗ | ✗ | ✓ |

### API & Settings Permissions

| Action | Viewer | Developer | Manager | Admin |
|--------|--------|-----------|---------|-------|
| View API Keys | ✗ | ✗ | ✗ | ✓ |
| Create API Keys | ✗ | ✗ | ✗ | ✓ |
| Manage Users | ✗ | ✗ | ✗ | ✓ |
| Edit Settings | ✗ | ✗ | ✗ | ✓ |
| Access Billing | ✗ | ✗ | ✗ | ✓ |

## Granular Permissions (Advanced)

### Permission Format

Permissions use dot notation: `resource:action`

**Examples:**
- `dashboards:read` - Read dashboards
- `alerts:write` - Create/modify alerts
- `metrics:read` - View metrics
- `account:delete` - Delete account
- `team:manage` - Manage team members

### Wildcard Permissions

- `dashboards:*` - All dashboard operations
- `alerts:*` - All alert operations
- `*:read` - Read all resources
- `*:*` - Full access (Admin)

## Team Structure Best Practices

### Small Teams (1-5 members)
- 1 Admin (account owner)
- Others: Developers
- Simple, flat structure
- All can create dashboards

### Medium Teams (5-20 members)
- 2-3 Admins (ensure coverage)
- Some Managers (team leads)
- Most as Developers
- Few Viewers (stakeholders)

### Large Teams (20+ members)
- 3-5 Admins (distributed by region/team)
- 10-15 Managers (multiple per department)
- Developers by department
- Viewers for read-only access
- Billing role for finance team

### By Department

**Engineering:**
- Developers and Managers
- Create technical dashboards
- Manage operational alerts

**Operations:**
- Admins (on-call lead)
- Managers (team lead)
- Some Developers (junior ops)
- Viewers (stakeholders)

**Finance/Billing:**
- Billing role
- View-only access to cost dashboards
- Not in technical operations

**Executives:**
- Viewer role
- Executive dashboard only
- No modification access

## Role Transition Scenarios

### Promoting to Manager

1. Remove as Developer
2. Re-invite as Manager
3. Assign any dashboards they own
4. Brief on new responsibilities

**Or:** Update existing member's role directly (preferred)

### Demoting from Admin

1. Ensure other Admins available
2. Change role to Manager or Developer
3. Verify access restrictions working
4. Confirm in audit log

### Offboarding User

1. Change role to Viewer (temporarily)
2. Export their dashboards if needed
3. Remove team member completely
4. 30-day recovery window (if needed)

## Special Cases

### External Contractors
- Use Viewer role for report access
- Use Developer if creating dashboards
- Limited dashboard sharing capability
- Recommend separate account if sensitive

### Audit/Compliance
- Create audit user with:
  - Viewer dashboard access
  - Audit log read access
  - No modification permissions
- Use email address for compliance records

### On-Call Rotations
- Primary: Admin or Manager
- Secondary: Manager or Developer
- Rotate role based on schedule
- Maintain coverage in audit trail

## API Permissions

### Scoped API Keys

Create API keys with specific permissions:

1. Go to **Settings** → **API Keys**
2. Click **+ Create Key**
3. Select scopes:
   - `read:metrics` (read only)
   - `write:alerts` (create alerts)
   - `read:dashboards` (view dashboards)
   - etc.
4. Limited to scoped permissions

**Best Practice:**
- Separate key per application
- Grant only needed scopes
- Different key for dev vs production
- Rotate regularly

## Audit and Monitoring

### Permission Changes

All role changes tracked in audit log:

1. Go to **Settings** → **Audit Logs**
2. Filter by "role_change" or "user_management"
3. See:
   - Who changed it
   - When changed
   - Old and new role
   - Reason (if documented)

### Unusual Access

Monitor for:
- Viewer accessing sensitive dashboards
- Developer creating alerts excessively
- After-hours access from new users
- Failed authentication attempts

### Permission Audit

Regular review:
- Monthly: Check role assignments
- Quarterly: Review inactive users
- After departures: Verify removal
- Before promotions: Verify appropriate

## Troubleshooting

### "Access Denied" Error
- Check user's role
- Verify role has required permission
- Check dashboard/alert sharing settings
- Confirm not a suspended user

### User Can't See Dashboard
- Confirm user has Viewer+ role
- Check dashboard is shared with user's team
- Verify dashboard not marked private
- Check user's role has dashboard:read

### User Can't Modify Alert
- Confirm user created alert (or Manager+)
- Check user role has alerts:write
- Verify not inherited/system alert
- Check user's role allows alert modification

## Support

For RBAC questions:
- **Documentation**: https://docs.clouddash.io/rbac
- **Email**: support@clouddash.io
- **Response Time**: 24 hours
