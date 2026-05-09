# Team Management Guide

## Overview
Manage your Clouddash team members, assign roles, organize teams, and maintain access control. This guide covers adding members, organizing teams, and managing permissions.

## Team Fundamentals

### What is a Team?

In Clouddash, a "team" consists of:
- Team members (users with account access)
- Their assigned roles (Admin, Manager, Developer, Viewer)
- Shared dashboards and alerts
- Combined resource usage

### Team Limits by Plan

| Limit | Starter | Professional | Enterprise |
|-------|---------|--------------|-----------|
| Team Members | 5 | 25 | Unlimited |
| Additional Members | $5 each | $3 each | Included |
| Shared Dashboards | 50 | Unlimited | Unlimited |
| Shared Alerts | 25 | Unlimited | Unlimited |

## Adding Team Members

### Send Invitation

**Step 1: Go to Team Settings**
1. Navigate to **Settings**
2. Select **Team Members**
3. Click **+ Invite Member**

**Step 2: Enter Member Information**
- **Email Address**: New member's email
- **Role**: Select appropriate role
  - Admin: Full access
  - Manager: Dashboard & alert management
  - Developer: Create and modify own dashboards/alerts
  - Viewer: Read-only access
- **Message (Optional)**: Custom invitation message

**Step 3: Send Invitation**
1. Click **Send Invitation**
2. Email sent to new member
3. Link in email directs to account creation
4. Member creates password and joins

### Bulk Invitations

**Import Multiple Members:**

1. Go to **Settings** → **Team Members**
2. Click **Bulk Import**
3. Download CSV template (includes email, role columns)
4. Fill in member information:
   ```
   email,role
   john@company.com,developer
   sarah@company.com,manager
   finance@company.com,billing
   ```
5. Upload completed CSV
6. Review list and confirm
7. Invitations sent to all addresses

## Managing Team Members

### View Team Members

1. Go to **Settings** → **Team Members**
2. List shows all team members:
   - Name/email
   - Role assigned
   - Invitation status (pending, active, expired)
   - Last activity date
   - Join date

### Update Member Role

**Change a Member's Role:**

1. Find member in list
2. Click member name or settings icon
3. Select new role from dropdown
4. Click **Save** or **Update**
5. Changes take effect immediately
6. Member notified of role change

**Promotion Example:**
- Current: Developer
- New: Manager
- Change requires no additional action
- Manager permissions activate immediately

**Demotion Example:**
- Current: Admin
- New: Developer
- Ensure another Admin available first
- Developer loses access to settings/billing

### Remove Team Member

**Revoke Access:**

1. Go to **Settings** → **Team Members**
2. Find member to remove
3. Click **Remove** button
4. Confirm action (cannot be undone)
5. Member immediately loses access
6. Dashboards and alerts remain (not deleted)

**What Happens When Removed:**
- Email access revoked
- Cannot log in
- Cannot access dashboards
- Data preserved (30-day recovery window)
- Can be re-invited within 30 days

### Re-invite Removed Member

**If Removed Recently:**

1. Go to **Settings** → **Team Members**
2. View removed members (30-day window)
3. Click **Re-invite**
4. Select role
5. New invitation sent
6. Member can rejoin with same email

**After 30 Days:**
- Member no longer visible in team
- Must invite as new member
- Will appear as new user
- Previous data cannot be recovered

## Organizing Multiple Teams

### Team Hierarchies (Enterprise)

Create sub-teams for organizational structure:

**Example Structure:**
```
Company
├── Engineering
│   ├── Backend Team
│   ├── Frontend Team
│   └── DevOps Team
├── Operations
│   ├── Infrastructure
│   └── Support
└── Finance
    └── Billing
```

**Benefits:**
- Organize large organizations
- Delegate management to sub-team leads
- Segment dashboards by team
- Control access at team level

### Assigning Members to Teams

1. Go to **Settings** → **Team Organization**
2. Create teams matching organizational structure
3. Assign members to teams
4. Set team-level permissions
5. Members see only their team's dashboards

### Team-Level Permissions

Control access at team level:

**Example: Support Team Read-Only Access**
1. Create "Support" team
2. Assign support members
3. Set team permissions: "View dashboards only"
4. Assign specific dashboards to team
5. Team members can view but not modify

## Working with Groups (Advanced)

### Create Groups

Organize members by function or project:

**Group Examples:**
- **On-Call Team**: Rotate responsibilities
- **Project Team**: Members working on specific project
- **Geographic Team**: Team in specific region
- **Skill-Based**: By expertise (database, networking, etc.)

**Create Group:**
1. Go to **Settings** → **Groups**
2. Click **+ Create Group**
3. Name: Descriptive group name
4. Add members
5. Assign group permissions
6. Save

### Group Permissions

**What Groups Can Control:**
- Access to specific dashboards
- Alert management
- Integration visibility
- Resource quotas

**Example: Night Shift On-Call**
1. Create group "Night Shift"
2. Assign night shift team members
3. Give group access to critical alerts
4. Permission to acknowledge/manage alerts
5. Restrict other group activities

### Dynamic Group Membership

**Rotate Group Membership:**
1. Go to group settings
2. Update members list
3. Add new on-call member
4. Remove previous on-call member
5. Save changes (automatic)

**On-Call Rotation:**
- Create "Current On-Call" group
- Update membership weekly
- Grant temporary elevated permissions
- Automatically revoked after rotation

## Access Control Patterns

### Principle of Least Privilege

Assign only needed permissions:

**Good Practice:**
- Contractor: Viewer role
- New developer: Developer role (not Admin)
- Intern: Limited Viewer role
- Manager: Manager role (not Admin)

**Bad Practice:**
- Everyone: Admin (security risk)
- New employee: Full access immediately
- Contractors: Developer+ access

### Temporary Access

**Grant Temporary Access:**
1. Add member with limited role
2. Set calendar reminder for removal
3. On expiration date, remove member
4. Can re-invite if needed again

**Example: Vendor Support**
1. Invite vendor with Viewer role
2. Grant access to specific dashboard
3. Note removal date: 2 weeks
4. After 2 weeks, remove member
5. Data audit trail remains

### Cross-Functional Access

**Allow engineers to see finance dashboards:**
1. Create shared dashboard accessible to multiple roles
2. Assign specific members (not entire role group)
3. Control what different users see
4. Finance team maintains dashboard

## Delegation of Responsibilities

### Designating Sub-Admins

Empower team leads with Admin rights:

1. Identify reliable team members
2. Change their role to Admin
3. Document their responsibilities:
   - Manage team members
   - Approve integrations
   - Handle billing questions
4. Maintain audit trail of their actions
5. Review monthly for compliance

### Backup Admin Coverage

Ensure continuity:

1. Designate 2+ admins minimum
2. Different time zones if distributed team
3. Cross-training on critical functions
4. Regular review of backup procedures
5. Documented handoff procedures

### Delegating Specific Responsibilities

**Dashboard Management:**
- Assign Manager role
- Responsible for dashboard quality
- Review and approve new dashboards
- Archive old dashboards

**Alert Management:**
- Assign Manager role
- Maintain alert rules
- Review alert tuning
- Prevent alert fatigue

**Billing Management:**
- Assign Billing role (if available)
- Or Admin with billing focus
- Monitor costs
- Approve upgrades

## Communication and Workflow

### Announcing Role Changes

**Notify Team When:**
- Major role promotion/demotion
- Team member leaving
- New team leads assigned
- Permission changes affecting workflow

**Communication Template:**
```
Hi team,

Please join me in welcoming [name] to the [role] team!
[Name] will be supporting us with [responsibilities].

If you have questions, reach out to me directly.

- [Admin name]
```

### Onboarding New Members

**First Day Tasks:**
1. Send welcome email with Clouddash info
2. Invite to Clouddash team
3. Provide getting started guide
4. Assign team mentor if applicable
5. Grant initial dashboards access

**First Week:**
1. Check member can access dashboards
2. Review alert notifications
3. Answer questions about workflows
4. Verify appropriate access level

**First Month:**
1. Quarterly review of permission level
2. Feedback on role fit
3. Adjust permissions if needed
4. Training on critical dashboards

### Offboarding Members

**Leaving Company:**

1. **Notice Period** (2 weeks before departure):
   - Plan knowledge transfer
   - Document their dashboards/alerts
   - Identify coverage for responsibilities

2. **Last Day**:
   - Remove from all teams
   - Revoke API keys
   - Note their dashboards (don't delete)
   - Document in audit trail

3. **After Departure**:
   - Reassign their dashboards
   - Update alert ownership
   - Keep audit trail (1 year minimum)
   - Archive their work if needed

**Changing Roles:**

1. Identify overlap period needed (1 week typical)
2. Add new person, keep old person temporarily
3. Provide training and knowledge transfer
4. New person takes full responsibility
5. Remove old person from role

## Team Monitoring

### Activity Review

**Monthly Team Review:**

1. Go to **Settings** → **Audit Logs**
2. Filter by time period (last month)
3. Review key activities:
   - New members added
   - Role changes
   - Dashboard/alert modifications
   - Integration changes
4. Note unusual patterns
5. Address concerns

### Inactive Members

**Identify Unused Accounts:**

1. Go to **Team Members**
2. Check "Last Activity" column
3. Members with 90+ day inactivity
4. Consider:
   - Are they still needed?
   - Should we remove to save licenses?
   - Did they leave without notice?

**Options:**
- Contact to verify still active
- Remove if departed
- Keep if on extended leave (documented)

### Usage by Member

**Track Member Contribution:**

1. Go to **Audit Logs**
2. Filter by user
3. See what they've created/modified
4. Review frequency of activity
5. Useful for performance reviews

## Team Size Management

### Staying Within License Limits

**Starter Plan (5 members included):**
- If adding 6th member:
  - Additional charge: $5/month
  - Consider upgrade to Professional

**Professional Plan (25 members included):**
- If exceeding 25:
  - Each additional member: $3/month
  - Or upgrade to Enterprise

### Optimizing Costs

**Reduce Member Count:**
1. Remove inactive members
2. Use Viewer role for read-only access
3. Remove contractors when not needed
4. Consolidate overlapping roles

**Optimize Plan:**
1. Review current plan vs. needs
2. If adding many members, upgrade may be cheaper
3. Calculate breakeven point
4. Switch plans if cost-effective

## Team Security

### Access Control Best Practices

- **Minimum Access**: Everyone starts with least privilege
- **Regular Audits**: Monthly review of team permissions
- **Immediate Removal**: Remove access when departing
- **Two Admins**: Minimum for account security
- **Segregation**: Sensitive dashboards restricted

### Credential Management

**API Keys:**
- One key per application/person
- Rotate keys quarterly
- Revoke unused keys
- Never share keys
- Document key purpose

**Passwords:**
- Encourage strong passwords
- Use SSO if available
- Disable password reset after departures
- Implement MFA for admins

### Suspicious Activity

**Red Flags:**
- Unusual logins (off-hours, odd locations)
- Bulk downloads or data access
- Rapid dashboard/alert creation
- API key generation spike
- Failed access attempts (brute force)

**Response:**
1. Investigate audit logs
2. Contact user to verify
3. Revoke access if unauthorized
4. Review account security
5. Document incident

## Team Communication

### Team-Wide Announcements

**For Important Changes:**
1. Prepare announcement
2. Choose communication method:
   - Email to team
   - In-app notification
   - Slack integration
   - All-hands meeting
3. Explain changes
4. Answer questions

### Feedback and Support

**Getting Help:**
- Encourage questions
- Create internal wiki/documentation
- Regular training sessions
- Slack channel for Clouddash topics
- Buddy system for new members

## Support and Training

### Internal Training

**Getting Team Productive:**

1. **Basic Training**: Dashboard navigation
2. **Intermediate**: Creating dashboards, alerts
3. **Advanced**: API usage, automation
4. **Specialized**: SSO setup, RBAC configuration

**Resources:**
- Internal wiki/documentation
- Video tutorials (record your workflows)
- Lunch-and-learn sessions
- Mentoring from experienced members

### External Support

Contact Clouddash for:
- Technical issues
- Complex RBAC scenarios
- Team structure consultation
- Enterprise setup guidance

**Support Channels:**
- Email: support@clouddash.io
- Chat: In-app support
- Docs: https://docs.clouddash.io

## Best Practices Summary

✓ Start with least privilege principle  
✓ Maintain 2+ admins minimum  
✓ Review team access monthly  
✓ Document role responsibilities  
✓ Use SSO for easier management  
✓ Implement proper onboarding  
✓ Track member activity  
✓ Remove inactive members promptly  
✓ Keep audit logs for compliance  
✓ Plan for succession/coverage  

## Troubleshooting

**"I can't invite new members"**
- Check if at team limit for your plan
- Upgrade plan to add more slots
- Remove inactive members
- Contact support for limit increase

**"Member says they can't access dashboard"**
- Check member's role permits access
- Verify dashboard is shared with their team
- Check for permission override (mark private)
- Restart app or clear cache

**"Removed member can still access"**
- May be cached session (log them out)
- Check they were actually removed
- Verify API keys revoked if used
- Clear browser cache and try again

**"Permission changes not taking effect"**
- Restart browser
- Log user out and back in
- Clear all cached data
- Verify change actually saved
