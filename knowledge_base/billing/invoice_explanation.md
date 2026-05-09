# Invoice Explanation

## Overview
Understanding your Clouddash invoice helps track usage and costs. This document explains each line item, charges, and how to manage your billing.

## Invoice Basics

### Invoice Format

Each monthly invoice includes:
- Invoice number (unique identifier)
- Invoice date (when issued)
- Billing period (what dates covered)
- Due date (payment deadline)
- Total amount due
- Itemized charges
- Payment method and last 4 digits
- Account notes if any

### Where to Find Invoices

1. Log into Clouddash
2. Go to **Settings** → **Billing** → **Invoices**
3. List shows all historical invoices
4. Click invoice to view details
5. Download PDF for records

### Invoice Details

**Invoice Header Information:**
```
Invoice #: INV-2024-001234
Invoice Date: May 1, 2024
Billing Period: May 1-31, 2024
Due Date: May 15, 2024
```

## Line Items Explained

### Base Plan Charge

**What It Is:**
The monthly cost for your subscription plan

**Pricing By Plan:**
| Plan | Monthly | Annual |
|------|---------|--------|
| Starter | $50 | $500 (save $100) |
| Professional | $100 | $1,000 (save $200) |
| Enterprise | Custom | Custom |

**Example on Invoice:**
```
Clouddash Professional Plan (May 1-31, 2024)
Quantity: 1 month
Price: $100.00
Subtotal: $100.00
```

**What's Included:**
- Base features of selected plan
- Team member slots (varies by plan)
- Data retention (default)
- API rate limits
- Standard support

### Team Member Add-ons

**What It Is:**
Additional team member slots beyond plan limit

**When Charged:**
- Base plan includes 5-25 members (varies by tier)
- Each extra member costs extra
- Starter: 5 included, $5 per additional
- Professional: 25 included, $3 per additional

**Example on Invoice:**
```
Additional Team Members (May 1-31, 2024)
Quantity: 3 extra members
Price: $5.00 per member
Subtotal: $15.00
```

### Data Retention Upgrades

**What It Is:**
Extended metric and log data storage

**Default Retention:**
- Metrics: 3 months
- Logs: 1 month
- High-frequency data: Limited

**Paid Options:**
- Extended metrics: $20-50 per month
- Extended logs: $15-30 per month
- 1-year retention: $150+ per month

**Example on Invoice:**
```
1-Year Metric Retention Upgrade (May 1-31, 2024)
Quantity: 1
Price: $150.00
Subtotal: $150.00
```

### Premium Support

**What It Is:**
Enhanced support tier with faster response times

**Support Tiers:**
| Tier | Response Time | Included |
|------|---------------|----------|
| Standard | 24 hours | Starter/Professional |
| Premium | 4 hours | +$50/month |
| Enterprise | 1 hour | Enterprise plan |

**Example on Invoice:**
```
Premium Support Tier (May 1-31, 2024)
Quantity: 1 month
Price: $50.00
Subtotal: $50.00
```

### Custom Integrations

**What It Is:**
Non-standard integrations or custom configurations

**When Charged:**
- Custom API endpoints
- Specialized data sources
- Non-standard metric transformations
- Requires engineering time

**Example on Invoice:**
```
Custom Datadog Integration Development
Quantity: 10 hours
Price: $200/hour
Subtotal: $2,000.00
```

### Mid-Cycle Adjustments

**What It Is:**
Prorated charges for changes made during billing cycle

**Scenarios:**
- Upgraded plan mid-month
- Added team members mid-month
- Enabled new features mid-month
- Cancelled service before month-end

**Example on Invoice:**
```
Professional Plan Upgrade (from Starter)
May 15-31, 2024 (17 days)
Difference: $50/month = $1.67/day
Adjustment: $1.67 × 17 = $28.39
```

### Taxes and Fees

**What It Is:**
Sales tax or VAT based on location and payment method

**Tax Calculation:**
- Applies to total monthly charges
- Rate depends on billing address
- May vary by region
- Non-profit orgs may be exempt (with documentation)

**Example on Invoice:**
```
Subtotal: $100.00
Tax (10%): $10.00
Total: $110.00
```

### Payment Processing Fee (if applicable)

**What It Is:**
Fee charged by payment processor for credit card transactions

**When Applied:**
- Usually not passed to customer
- Sometimes charged for high-risk transactions
- Wire transfer or ACH rarely incur fees
- Minimum fee typically $0.50

**Example on Invoice:**
```
Payment Processing Fee: $0.35
```

## Invoice Example Breakdown

**Complete Sample Invoice:**

```
CLOUDDASH INVOICE
Invoice #: INV-2024-005678
Invoice Date: May 1, 2024
Billing Period: May 1-31, 2024
Due Date: May 15, 2024

Account: Acme Corporation
Email: billing@acme.com

CHARGES:
Professional Plan                     $100.00
Additional Team Members (2 @ $3)       $6.00
Extended Metrics Retention            $50.00
Premium Support                       $50.00

Subtotal:                            $206.00
Tax (estimated):                     $20.60
---
TOTAL DUE:                          $226.60

Payment Method: Visa ending in 4242
Auto-renewed on May 1, 2024
```

## Common Line Item Questions

**Q: Why am I seeing a charge for team members?**
A: Your plan includes a certain number of team members. Adding more incurs per-member charges.

**Q: What is the "adjustment" line item?**
A: Prorated refund or charge from a plan change mid-cycle.

**Q: Why is my tax different each month?**
A: Tax is calculated on total charges each month. Charges vary with usage and add-ons.

**Q: What are "overage charges"?**
A: Exceeding included usage limits (if applicable). Professional plan includes unlimited everything.

**Q: Why is there a credit on my invoice?**
A: Typically from:
  - Plan downgrade mid-month
  - Service credit for issues
  - Over-payment from previous month
  - Refund processed

## Pricing Tiers

### Starter Plan ($50/month)
- Up to 5 team members
- Basic integrations (AWS, GCP, Azure)
- 3-month metric retention
- Standard support
- 1,000 dashboards
- 100 alerts

### Professional Plan ($100/month)
- Up to 25 team members
- Advanced integrations
- 6-month retention (optional upgrade)
- Premium support (+$50)
- Unlimited dashboards
- Unlimited alerts
- Custom metric aggregation
- Advanced roles and permissions

### Enterprise Plan (Custom Pricing)
- Unlimited team members
- Custom integrations
- Custom data retention
- 24/7 enterprise support
- Dedicated account manager
- Custom SLAs
- On-premises deployment option

## Invoice Adjustments

### Credits Applied

Invoices may show credits for:
- Previous refunds
- Service issues/downtime
- Promotional discounts
- Partner discounts
- Volume discounts

**Example:**
```
Subtotal:          $150.00
Service Credit:    -$25.00 (previous issue)
---
Adjusted Total:    $125.00
```

### Discounts and Promotions

**Annual Billing Discount:**
- Save 15-20% by paying annually
- Invoice shows annual rate divided by 12
- Promotion codes may apply additional discounts

**Non-Profit Discount:**
- 20% discount for verified non-profits
- Requires 501(c)(3) documentation
- Applied automatically after verification

**Volume Discounts:**
- Enterprise customers may negotiate
- Larger teams or long-term commitments
- Discuss with account manager

## Payment Terms and Methods

### Due Date
- Typically 15 days from invoice date
- Can request different terms for enterprise
- Auto-renewal may occur before due date

### Accepted Payment Methods

**Automatic (Recurring):**
- Visa, Mastercard, Discover
- American Express
- PayPal

**Manual (One-time):**
- Wire transfer (ACH)
- Check (enterprise)
- Purchase order (enterprise)

### Late Payment

- Invoices typically auto-renew
- Late fees: Usually none
- After 30 days past due:
  - Service may suspend
  - Account flagged for collections
  - Access to dashboards restricted
  - Late payment notice sent

## Receipt and Tax Documentation

### Tax Receipt
- Issued for tax-exempt organizations
- Includes tax ID and documentation
- Available in invoices section

### W9 Form
- Available upon request
- Contact billing@clouddash.io
- Needed for 1099 reporting

### Proof of Payment
- Invoice serves as receipt
- Payment confirmation via email
- Detailed transaction history available

## Understanding Costs

### Cost Drivers

**Your invoice is determined by:**
1. **Selected Plan Tier**
   - Base cost: $50-$100+ per month
   - Feature set included

2. **Team Size**
   - Each extra member: $3-$5
   - Example: 30 members = 5 extra = $15-25/month

3. **Data Retention**
   - Extended retention: +$20-150/month
   - Affects storage and performance

4. **Add-ons and Features**
   - Premium support: +$50/month
   - Custom integrations: varies
   - Special configurations: varies

### Cost Optimization

**Ways to Reduce Costs:**
- Use free tier if qualifying
- Remove unused team members
- Use default data retention
- Choose monthly over add-ons
- Batch alerts to reduce evaluation

**Ways You Might See Increases:**
- Adding team members
- Extending data retention
- Enabling premium features
- Scaling usage on enterprise plan

## Quarterly and Annual Invoices

### Multi-month Billing

**Quarterly Invoice:**
- Covers 3 months
- Issued every 3 months
- Line items may be combined
- Total: Base charge × 3 (approximately)

**Annual Invoice:**
- Covers entire year
- Issued once per year
- Payment due before year starts
- Often includes discount

## Troubleshooting

### I don't recognize a charge
1. Check invoice date
2. Review what it covers
3. Note the item description
4. Contact support@clouddash.io with details
5. Provide invoice number
6. Service will investigate

### I was double-charged
1. Check both invoice numbers
2. Verify dates don't overlap
3. Contact billing@clouddash.io immediately
4. Provide both invoice numbers
5. Refund will be issued for duplicate

### My charges are different than expected
1. Review all line items
2. Check for prorated adjustments
3. Account for tax changes
4. Verify team member count
5. Ask support if line item unclear

## Support

For invoice questions:
- **Email**: billing@clouddash.io
- **Hours**: Monday-Friday, 9 AM - 5 PM EST
- **Response Time**: 24 hours
- Include invoice number in all communications
