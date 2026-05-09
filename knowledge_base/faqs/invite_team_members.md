# How to Invite Team Members

## Overview
Clouddash uses a role-based access control system to manage team permissions. Invite team members to collaborate on dashboards, manage alerts, and access billing information.

## Steps to Invite a Team Member

### Via the Web Interface
1. Navigate to **Settings** → **Team Members**
2. Click the **+ Invite Member** button
3. Enter the team member's email address
4. Select their role (see roles below)
5. Optionally add a custom message
6. Click **Send Invitation**

### Bulk Invitations
For inviting multiple team members:
1. Go to **Settings** → **Team Management** → **Bulk Invite**
2. Upload a CSV file with format: `email,role`
3. Review the list and confirm
4. Invitations will be sent to all addresses

## Available Roles

| Role | Permissions | Best For |
|------|-------------|----------|
| **Admin** | Full access, user management, billing | Team leads, account owners |
| **Manager** | Dashboard creation, team oversight, alerts | Engineering managers |
| **Developer** | View dashboards, manage own alerts | Individual developers |
| **Billing** | Invoice access, payment management | Finance team |
| **Viewer** | Read-only access | Stakeholders, auditors |

## Invitation Status

- **Pending**: Invitation sent, awaiting acceptance
- **Active**: User has accepted and logged in
- **Expired**: Invitation expired after 30 days

## Resending Invitations

If a team member hasn't responded:
1. Go to **Settings** → **Team Members**
2. Find the pending invitation
3. Click **Resend** to send another copy
4. Original invitation will expire after 30 days

## Removing Team Members

1. Navigate to **Settings** → **Team Members**
2. Find the member to remove
3. Click the **Remove** button
4. Confirm the action
5. Their access will be revoked immediately

## Troubleshooting

**Team member didn't receive invitation**
- Check spam/junk folder
- Verify email address is correct
- Resend the invitation
- Confirm your domain isn't blocking emails

**I need to change someone's role**
- Go to Team Members list
- Click the member's name
- Select new role from dropdown
- Changes take effect immediately

**How many team members can I add?**
- Starter Plan: Up to 5 members
- Professional Plan: Up to 25 members
- Enterprise Plan: Unlimited members
