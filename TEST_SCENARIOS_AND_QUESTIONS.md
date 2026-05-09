# Test Scenarios and Sample Questions
## Multi-Agent Customer Support System Assessment

This document provides a comprehensive set of test questions mapped to the four assessment scenarios and the available knowledge base.

---

## Knowledge Base Coverage Summary

### Available Categories (20+ Articles)

**API Documentation:**
- Authentication (API keys, Bearer tokens)
- Rate Limits (Starter, Pro, Enterprise tiers)
- SDK Usage (Python, JavaScript, Go, Java)
- Webhook Configuration (event types, authentication methods)

**Troubleshooting Guides:**
- AWS Alerts Not Firing (credential updates, CloudWatch sync)
- CloudWatch Sync Failure (credentials, IAM permissions, network, rate limiting)
- Dashboard Loading Slowly (widget count, time ranges, data sources)
- Metric Ingestion Delay (CloudWatch latency, sync intervals, aggregation)
- SSO Login Failure (IdP misconfiguration, user provisioning, SAML issues)
- Webhook Delivery Failures (URL issues, authentication, network)

**Billing & Subscription:**
- Invoice Explanation (plan charges, team members, data retention add-ons)
- Refund Policy (eligibility criteria, calculation examples)
- Payment Failure Resolution (expired cards, fraud prevention)
- Upgrade/Downgrade Policy (prorated pricing, feature changes)

**FAQs & Getting Started:**
- Alert Frequency Configuration
- Dashboard Customization
- Invite Team Members
- Reset API Key
- Supported Cloud Providers (AWS, GCP, Azure; NO Datadog)

**Account & Access Management:**
- SSO Setup Guide (Okta, Azure AD, Google Workspace)
- RBAC Roles and Permissions (Admin, Manager, Developer, Viewer, Billing)
- Team Management
- Audit Logs (tracking all activities)

---

# Test Scenarios

## SCENARIO 1: Single-Agent Resolution
**Flow**: Triage → Technical Support Agent → KB Retrieval → Resolution

### Expected Behavior
- Triage agent classifies as **technical issue**
- Routes to **Technical Support Agent**
- Agent retrieves relevant KB article
- Provides **step-by-step resolution with source citation**

---

## TEST QUESTIONS FOR SCENARIO 1

### Question 1.1 (Core Scenario)
**Customer Query:**
```
"My CloudDash alerts stopped firing after I updated my AWS integration 
credentials yesterday. I'm on the Pro plan and this is affecting our 
production monitoring."
```

**Expected Agent Flow:**
1. **Triage Agent**: Classifies as technical support, extracts entities (AWS, alerts, credentials)
2. **Technical Support Agent**: Should retrieve from `aws_alerts_not_firing.md` + `cloudwatch_sync_failure.md`
3. **Suggested Response Elements**:
   - Acknowledge AWS credential update as likely root cause
   - Guide to Settings → Integrations → AWS
   - Reference "Last Synced" timestamp check
   - Provide "Test Connection" button location
   - Include step-by-step reconnection process
   - **Citation**: Link to KB articles on AWS credential updates

**KB Articles Used**: 
- `troubleshooting/aws_alerts_not_firing.md`
- `troubleshooting/cloudwatch_sync_failure.md`

---

### Question 1.2 (Technical Depth - Alert Configuration)
**Customer Query:**
```
"My dashboard shows metrics from AWS CloudWatch but they're updating 
very slowly - about 15 minutes behind real-time. How can I speed this up?"
```

**Expected Agent Flow:**
1. **Triage Agent**: Classifies as technical issue, identifies metric delay concern
2. **Technical Support Agent**: Retrieves from `metric_ingestion_delay.md`
3. **Suggested Response Elements**:
   - Explain AWS CloudWatch inherent latency (1-2 minutes typical)
   - Check current sync interval (recommend 1-5 minutes)
   - Suggest reducing dashboard time range if querying months of data
   - Recommend reducing widget count
   - Provide steps to check aggregation interval
   - **Citation**: Reference KB article on metric ingestion

**KB Articles Used**:
- `troubleshooting/metric_ingestion_delay.md`
- `troubleshooting/dashboard_loading_slowly.md`

---

### Question 1.3 (Technical - Dashboard Performance)
**Customer Query:**
```
"Our production dashboard takes almost 10 seconds to load. We have about 
30 widgets showing various metrics across AWS and GCP. Any tips?"
```

**Expected Agent Flow:**
1. **Triage Agent**: Classifies as technical performance issue
2. **Technical Support Agent**: Retrieves from `dashboard_loading_slowly.md`
3. **Suggested Response Elements**:
   - Identify 30 widgets as likely cause
   - Recommend reducing to 15-20 widgets maximum
   - Suggest removing duplicate metrics
   - Recommend combining similar charts
   - Provide steps for removing widgets
   - **Citation**: KB article on dashboard optimization

**KB Articles Used**:
- `troubleshooting/dashboard_loading_slowly.md`
- `faqs/dashboard_customization.md`

---

### Question 1.4 (Technical - API/Webhooks)
**Customer Query:**
```
"I configured a webhook to send our alerts to Slack, but we're not 
receiving any notifications. The webhook was working last month."
```

**Expected Agent Flow:**
1. **Triage Agent**: Classifies as technical issue with webhooks
2. **Technical Support Agent**: Retrieves from `webhook_delivery_failures.md`
3. **Suggested Response Elements**:
   - Guide to check webhook configuration
   - Check if endpoint URL is still valid and accessible
   - Test webhook connectivity
   - Verify authentication headers if using API key
   - Check webhook delivery history/logs
   - **Citation**: Reference webhook troubleshooting KB

**KB Articles Used**:
- `troubleshooting/webhook_delivery_failures.md`
- `api_docs/webhook_configuration.md`

---

### Question 1.5 (Technical - Account Access)
**Customer Query:**
```
"I need to reset my API key because I think it was accidentally exposed 
in a GitHub commit. How do I do this without breaking my integrations?"
```

**Expected Agent Flow:**
1. **Triage Agent**: Classifies as account security issue
2. **Technical Support Agent**: Routes to account access KB
3. **Suggested Response Elements**:
   - Provide steps to reset API key (immediate invalidation)
   - Emphasize need to update all integrations immediately
   - List integration types to update (CloudWatch, webhooks, scripts)
   - Provide link to reset instructions
   - Recommend rotating quarterly for security
   - **Citation**: KB article on API key management

**KB Articles Used**:
- `faqs/reset_api_key.md`
- `api_docs/authentication.md`

---

## SCENARIO 2: Cross-Agent Handover
**Flow**: Triage → Technical Agent → Billing Agent → Resolution with context preservation

### Expected Behavior
- Triage identifies **two distinct intents**
- Routes to Technical Support first
- **Seamlessly hands over to Billing Agent** with full context
- Billing Agent has access to prior discussion
- No information needs to be repeated
- Handover is **logged with context snapshot**

---

## TEST QUESTIONS FOR SCENARIO 2

### Question 2.1 (Core Cross-Agent Scenario)
**Customer Query:**
```
"I want to upgrade from Pro to Enterprise, but first can you check if 
the SSO integration issue I reported last week has been resolved? My team 
is having trouble logging in."
```

**Expected Agent Flow:**
1. **Triage Agent**: Identifies TWO intents:
   - Intent #1: Technical (SSO login failure)
   - Intent #2: Billing (upgrade plan)
   
2. **Technical Support Agent** (First):
   - Retrieves from `sso_login_failure.md`
   - Provides diagnostics for SSO issue
   - Guides through verification steps
   - Resolves or escalates SSO problem
   
3. **Handover to Billing Agent**:
   - **Context preserved**: SSO issue resolved/status, customer plan info, customer ID
   - **Entities transferred**: Customer ID, current plan (Pro), desired plan (Enterprise)
   - Billing Agent acknowledges received context
   
4. **Billing Agent** (Second):
   - Provides upgrade process from `upgrade_downgrade_policy.md`
   - Explains prorated charges
   - Confirms Enterprise features available
   - Shows no downtime during upgrade
   
5. **Audit Trail**: Handover logged with:
   - Timestamp
   - Source: Technical Support Agent
   - Target: Billing Agent
   - Reason: Cross-domain intent
   - Context snapshot: SSO status, plan upgrade request

**KB Articles Used**:
- `troubleshooting/sso_login_failure.md`
- `account_access/sso_setup.md`
- `billing/upgrade_downgrade_policy.md`

---

### Question 2.2 (Cross-Agent - Technical then Billing)
**Customer Query:**
```
"My dashboard is unusable - it's loading in 45 seconds. This started 
happening after we added 10 more team members last week. Also, I'm 
considering upgrading to Enterprise because we're hitting the 25-member 
limit on Professional."
```

**Expected Agent Flow:**
1. **Triage Agent**: Identifies TWO intents:
   - Intent #1: Technical (dashboard performance, team member count)
   - Intent #2: Billing (plan upgrade for more team slots)
   
2. **Technical Support Agent** (First):
   - Acknowledges dashboard slowness
   - Notes correlation with 10 new team members
   - Retrieves from `dashboard_loading_slowly.md`
   - Suggests checking widget count, time ranges
   - May recommend Dashboard optimization (reduce widgets)
   
3. **Handover to Billing Agent**:
   - **Context**: Dashboard performance issue, current team size (25), desire to add more members
   - **Entities**: Current plan (Professional), team size (25)
   
4. **Billing Agent** (Second):
   - Confirms Professional allows 25 members (at limit)
   - Shows Enterprise includes unlimited members
   - Explains prorated upgrade cost if mid-cycle
   - No re-explanation needed of dashboard issue

**KB Articles Used**:
- `troubleshooting/dashboard_loading_slowly.md`
- `billing/upgrade_downgrade_policy.md`
- `faqs/invite_team_members.md`

---

### Question 2.3 (Cross-Agent - Billing then Technical)
**Customer Query:**
```
"I just upgraded from Starter to Professional to enable our webhooks 
integration with our incident management system. But now the webhooks 
aren't delivering. Can you help?"
```

**Expected Agent Flow:**
1. **Triage Agent**: Identifies potential TWO intents:
   - Intent #1: Billing (plan upgrade confirmation)
   - Intent #2: Technical (webhook delivery failure)
   
2. **Billing Agent** (First - Optional):
   - Confirms upgrade from Starter to Professional successful
   - References `upgrade_downgrade_policy.md`
   - Shows new features now available
   
3. **Handover to Technical Support Agent**:
   - **Context**: Just upgraded, webhooks now enabled/expected to work
   - Customer likely doesn't know webhook setup
   
4. **Technical Support Agent** (Second):
   - Guides through webhook configuration
   - Checks delivery logs
   - Verifies endpoint URL, authentication
   - References `webhook_configuration.md` and troubleshooting

**KB Articles Used**:
- `billing/upgrade_downgrade_policy.md`
- `api_docs/webhook_configuration.md`
- `troubleshooting/webhook_delivery_failures.md`

---

## SCENARIO 3: Escalation to Human
**Flow**: Triage → Specialist Agent → Escalation Agent → Human Handover

### Expected Behavior
- Triage routes to specialist
- Specialist **attempts resolution** but identifies need for human intervention
- Routes to **Escalation Agent**
- Escalation Agent **packages context** (customer ID, issue, urgency, sentiment)
- **Human handover triggered** with complete information
- No context loss

---

## TEST QUESTIONS FOR SCENARIO 3

### Question 3.1 (Core Escalation - Billing/Refund)
**Customer Query:**
```
"I've been charged TWICE for April. I need an immediate refund and I want 
to speak to a manager. This is completely unacceptable. Your system 
clearly has a billing bug."
```

**Expected Agent Flow:**
1. **Triage Agent**: Identifies as urgent billing issue
   
2. **Billing Agent** (Attempts Resolution):
   - Retrieves from `refund_policy.md` and `invoice_explanation.md`
   - Acknowledges duplicate charge
   - Recognizes this as "Billing Error" (eligible for refund)
   - Explains: "This qualifies for a full refund per our policy"
   - BUT recognizes: Customer demand for manager + high emotion
   - Recognizes refund authority may be limited for AI
   
3. **Escalation to Escalation Agent**:
   - Reason: High priority billing error + customer explicitly wants manager
   - **Context Package includes**:
     - Customer ID
     - Issue: Duplicate charge for April
     - Amount affected: $100+ (assuming Professional plan)
     - Urgency: HIGH (explicit demand for manager)
     - Sentiment: FRUSTRATED/ANGRY (language: "unacceptable", "completely")
     - Refund eligibility: YES (Billing Error category)
     - Recommended action: Process refund + manager contact
   
4. **Escalation Agent**:
   - Acknowledges urgency and frustration
   - Validates customer concern
   - Indicates human support team will contact within 1 hour
   - Preserves all prior conversation
   - **Log entry**: Priority=HIGH, Type=BILLING_ERROR, Action=REFUND_REQUIRED
   
5. **Human Support** (Simulated):
   - Receives complete context
   - Processes refund
   - Manager provides personal contact

**KB Articles Used**:
- `billing/refund_policy.md`
- `billing/invoice_explanation.md`
- `handover/context_builder.md` (internal)

---

### Question 3.2 (Escalation - Payment Failure)
**Customer Query:**
```
"My payment was declined and now I'm getting warnings that my service 
will be suspended in 24 hours. I need this resolved immediately but your 
payment form is confusing and I've tried 5 times. I want to talk to 
someone directly."
```

**Expected Agent Flow:**
1. **Triage Agent**: Identifies as urgent billing + payment issue
   
2. **Billing Agent** (Attempts Resolution):
   - Retrieves from `payment_failure_resolution.md`
   - Attempts to troubleshoot:
     - Expired card? Fraud block? Address mismatch?
     - Offers solutions (update payment method, use different card)
   - BUT recognizes: Customer frustrated after 5 attempts, wants human
   
3. **Escalation to Escalation Agent**:
   - Reason: Customer explicitly wants human agent + high frustration + service at risk
   - **Context Package**:
     - Customer ID
     - Issue: Payment declined 5 times
     - Urgency: CRITICAL (service suspension imminent)
     - Sentiment: FRUSTRATED/LOSING PATIENCE
     - Troubleshooting attempts: 5 failed
     - Account status: At risk of suspension
     - Note: May need payment method reset or special handling
   
4. **Escalation Agent**:
   - Validates frustration
   - Commits to human agent assistance
   - Indicates will prioritize resolution within 30 minutes
   - Prevents immediate suspension if possible
   
5. **Human Support** (Simulated):
   - May reset payment method
   - May manually process payment
   - Extends grace period if needed

**KB Articles Used**:
- `billing/payment_failure_resolution.md`

---

### Question 3.3 (Escalation - Complex Technical Issue)
**Customer Query:**
```
"Our CloudWatch integration stopped syncing 3 days ago and our entire 
monitoring is blind. We're Enterprise customers and this is a huge problem. 
I need someone from your technical team to investigate urgently."
```

**Expected Agent Flow:**
1. **Triage Agent**: Identifies as urgent technical issue
   
2. **Technical Support Agent** (Attempts Resolution):
   - Retrieves from `cloudwatch_sync_failure.md`
   - Runs through diagnostics:
     - Check credentials
     - Verify IAM permissions
     - Check AWS API status
   - But after 30+ minutes of troubleshooting with no resolution
   - Recognizes: Enterprise customer + 3-day outage + needs specialist
   
3. **Escalation to Escalation Agent**:
   - Reason: Enterprise SLA violation + extended outage + requires specialist investigation
   - **Context Package**:
     - Customer ID & Plan: ENTERPRISE
     - Issue: CloudWatch sync failure for 3 days
     - Impact: Complete monitoring blind (CRITICAL)
     - Urgency: CRITICAL
     - Sentiment: URGENT/DEMANDING
     - Troubleshooting attempted: Credentials verified, IAM OK, AWS API OK
     - Root cause: UNKNOWN (needs deeper investigation)
     - SLA: Enterprise 4-hour response
   
4. **Escalation Agent**:
   - Acknowledges Enterprise status and SLA violation
   - Commits to engineer investigation
   - Provides support ticket number
   - Updates customer on progress timeline
   
5. **Human Support / Engineering** (Simulated):
   - Investigates logs for sync failures
   - Checks for service issues
   - May involve AWS support if needed

**KB Articles Used**:
- `troubleshooting/cloudwatch_sync_failure.md`

---

## SCENARIO 4: KB Retrieval Failure
**Flow**: Triage → Agent → KB Search → No Results → Graceful Escalation

### Expected Behavior
- Agent searches KB
- **Finds NO relevant article**
- Agent **transparently acknowledges limitation**
- Agent offers alternative: escalate or feature request
- Never fabricates information

---

## TEST QUESTIONS FOR SCENARIO 4

### Question 4.1 (Core KB Failure Scenario)
**Customer Query:**
```
"Does CloudDash support integration with Datadog for cross-platform 
alerting? We use Datadog for APM and want to correlate alerts with 
Clouddash metrics."
```

**Expected Agent Flow:**
1. **Triage Agent**: Classifies as feature/integration inquiry
   
2. **Technical Support Agent**:
   - Searches KB for "Datadog integration"
   - Searches KB for "Datadog support"
   - Retrieves `faqs/supported_cloud_providers.md`
   - Finds: "Not Currently Supported: Proprietary monitoring tools (we do not provide Datadog integration)"
   
3. **Response**:
   - **Transparent acknowledgment**: "Datadog integration is not currently supported by CloudDash"
   - **Why**: "We currently integrate with AWS, GCP, and Azure cloud native monitoring"
   - **Alternatives offered**:
     - Use Datadog's AWS integration to send metrics to CloudWatch, then monitor in CloudDash
     - Or use Datadog's webhook capabilities to send alerts to Clouddash
   - **Path forward**: 
     - Contact sales/feature request for Datadog integration
     - Would require Engineering review and roadmap prioritization
   - **Never say**: "Datadog is integrated but you need to set it up differently" (fabrication)

**KB Articles Used**:
- `faqs/supported_cloud_providers.md`

**Response Pattern**:
```
We don't currently provide a native Datadog integration in CloudDash. 
However, here are your options:

1. Use Datadog's AWS integration to sync metrics to CloudWatch, which 
   we fully support
2. Use Datadog webhooks to send alerts to CloudDash webhooks
3. Interested in native Datadog integration? I can escalate your 
   request to our product team for consideration

Would you like me to help set up workaround #1 or #2, or escalate 
a feature request?
```

---

### Question 4.2 (KB Failure - Unsupported Feature)
**Customer Query:**
```
"Can I use CloudDash with our on-premises Kubernetes cluster that runs 
on our private data center? We don't want to migrate to EKS/GKE."
```

**Expected Agent Flow:**
1. **Triage Agent**: Classifies as infrastructure question
   
2. **Technical Support Agent**:
   - Searches KB for "on-premises", "on-prem", "Kubernetes", "private"
   - Retrieves `faqs/supported_cloud_providers.md`
   - Finds: "On-Premises: Limited support through API endpoints and custom integrations"
   
3. **Response** (Transparent about Limitations):
   - "On-premises Kubernetes is not natively supported by CloudDash"
   - "We support cloud-based Kubernetes (EKS, GKE, AKS) through cloud provider integrations"
   - "Limited support available through custom API integrations"
   - **Path forward**:
     - Contact sales for custom integration assessment
     - Might require professional services engagement
     - Timeline and feasibility: unknown without assessment

**KB Articles Used**:
- `faqs/supported_cloud_providers.md`

---

### Question 4.3 (KB Failure - Unknown Feature)
**Customer Query:**
```
"I heard that Clouddash can predict when my metrics will breach thresholds 
using machine learning. How do I enable that feature? I want to get alerts 
before issues happen, not after."
```

**Expected Agent Flow:**
1. **Triage Agent**: Classifies as feature inquiry
   
2. **Technical Support Agent**:
   - Searches KB for "ML", "machine learning", "predictive", "forecasting"
   - Searches for "anomaly detection"
   - **Result**: NO relevant articles found
   
3. **Response** (Graceful Degradation):
   - "I couldn't find documentation on predictive alerting or machine learning features in our knowledge base"
   - "Based on our current documentation, CloudDash focuses on threshold-based alerting"
   - **Options**:
     - Let me escalate this to our product team to clarify if this feature exists
     - Suggest current solution: Configure threshold-based alerts at conservative thresholds
     - Schedule demo/consultation with solutions engineer
   
4. **Escalation Path**:
   - If customer is interested, escalate to Sales/Product
   - Feature may exist but not documented
   - Or feature may be roadmap item only

**Response Pattern**:
```
Great question! I don't have documentation on predictive alerting 
in our knowledge base. Let me clarify this for you:

1. I can escalate this to our product team to verify if we offer 
   this capability
2. In the meantime, I'd recommend setting up threshold-based alerts 
   at conservative thresholds to catch issues early
3. For advanced use cases, our Enterprise tier includes consulting

Which would be most helpful?
```

---

### Question 4.4 (KB Failure - Configuration Question)
**Customer Query:**
```
"I need to configure custom authentication headers on my webhooks. 
The standard API key and Bearer token options won't work with our system. 
Can I use OAuth 2.0 instead?"
```

**Expected Agent Flow:**
1. **Triage Agent**: Classifies as technical/API question
   
2. **Technical Support Agent**:
   - Searches KB for "OAuth", "custom headers", "advanced auth"
   - Retrieves `api_docs/webhook_configuration.md`
   - Finds: "Custom Headers: Add custom headers to request"
   - BUT: No mention of OAuth 2.0 support
   - Limited to: No Auth, API Key, Bearer Token, Custom Headers
   
3. **Response** (Accurate about Limitations):
   - "CloudDash webhooks support the following auth methods:" [lists 4 options]
   - "OAuth 2.0 is not currently supported as a webhook auth method"
   - **Possible workarounds**:
     - Use Custom Headers to add your OAuth token manually
     - Or use Bearer Token if your system supports it
     - Or contact support for custom development
   - **Never say**: "Yes, we support OAuth" if we don't

**KB Articles Used**:
- `api_docs/webhook_configuration.md`

---

## ADDITIONAL VARIATIONS FOR ROBUSTNESS

### Variation 4.1: Multi-step Technical with Escalation
**Customer Query:**
```
"I've followed all the troubleshooting steps for AWS alerts not firing - 
tested connection, verified IAM permissions, re-authenticated credentials, 
forced sync - but alerts STILL aren't firing after 2 hours. What else?"
```

**Expected Flow**:
- Technical Agent exhausts troubleshooting steps
- Recognizes need for deeper investigation
- Escalates to Technical Escalation (or human engineer)
- Preserves all troubleshooting context and results

### Variation 4.2: Handover Back to Previous Agent
**Customer Query** (Continuation):
```
"So the billing upgrade is processing. But I'm worried the dashboard 
performance issue won't be fixed just by upgrading. Should I also 
optimize the dashboard?"
```

**Expected Flow**:
- Billing Agent completes upgrade
- Customer has follow-up technical question
- Can hand back to Technical Agent with context
- OR both agents know from session context

### Variation 4.3: Incorrect Routing Recovery
**Customer Query**:
```
"I keep getting errors when trying to export my dashboards as PDF. 
Is this a known issue?"
```

**Expected Flow**:
- Triage may route incorrectly initially
- If wrong agent receives query, should:
  - Recognize it's not their domain
  - Route to correct agent with context
  - Not try to answer outside expertise

### Variation 4.4: Sentiment-Based Escalation
**Customer Query** (Same technical issue, different tone):
```
"Alerts aren't firing. Not working. Fix this now. Enterprise customer 
here. SLA violation."
```

**Expected Flow**:
- Triage recognizes: Enterprise status + urgent tone + immediate escalation needed
- May escalate to Escalation Agent directly
- Don't try to walk through troubleshooting if customer is already escalated

---

## EVALUATION CHECKLIST

### For Each Test Question, Verify:

#### System Design (25%)
- [ ] Correct agent routing logic
- [ ] Clean separation of concerns
- [ ] State management across turns
- [ ] Extensibility (easy to add new agents)

#### KB Integration (25%)
- [ ] Accurate KB retrieval
- [ ] Proper source citation
- [ ] Chunking works for complex topics
- [ ] Hybrid retrieval finds obscure info
- [ ] Context rewriting improves accuracy

#### Agent Handover (20%)
- [ ] Full context preserved
- [ ] Entities transferred without loss
- [ ] Receiving agent acknowledges handover
- [ ] Graceful failure handling
- [ ] Handover logged with metadata

#### Code Quality (15%)
- [ ] Typed data models
- [ ] Meaningful error handling
- [ ] Structured logging
- [ ] Trace ID across conversation
- [ ] Clean code organization

#### Guardrails (15%)
- [ ] Never fabricates KB info
- [ ] Transparently acknowledges limitations
- [ ] Handles off-topic gracefully
- [ ] Identifies high-priority issues
- [ ] Sentiment/urgency analysis

---

## SCORING GUIDE

### Expected Agent Response Quality

**Excellent (90-100%)**
- Correct KB retrieval with exact citations
- Empathetic tone matching customer sentiment
- Provides 3+ actionable steps
- Acknowledges limitations transparently
- Correct handover with full context
- No hallucinations

**Good (75-89%)**
- Relevant KB articles retrieved
- Addresses customer concern
- Provides helpful guidance
- Mostly correct handovers
- Minor context loss acceptable

**Acceptable (60-74%)**
- Some relevant KB info
- Attempts to resolve issue
- Partial context preservation
- Basic handover capability

**Poor (<60%)**
- Hallucinated information
- Wrong KB articles
- Context loss
- Failed handovers
- Incorrect routing

---

## NEXT STEPS FOR IMPLEMENTATION

1. **Implement Question Generator**: Create variations of these questions
2. **Add Metric Tracking**: Track success rate for each scenario
3. **Create Test Harness**: Automated testing framework
4. **Collect Baseline Metrics**: Establish expected performance
5. **Iteration**: Refine based on results

