# Payment Failure Resolution

## Problem
Payment for your Clouddash subscription has failed. Service may be suspended or at risk if payment is not resolved. Common reasons include expired card, insufficient funds, or billing address mismatch.

## Why Payments Fail

### Expired or Invalid Card
- Credit card expired
- Card number incorrect
- CVV code wrong
- Card cancelled by issuer

### Insufficient Funds
- Account balance too low
- Card limit exceeded
- Daily transaction limit reached
- Insufficient credit available

### Billing Address Mismatch
- Address doesn't match card issuer records
- ZIP code incorrect
- State/province mismatch
- Street number mistyped

### Card Fraud Prevention
- Transaction flagged as suspicious
- Unusual spending pattern detected
- Velocity check failed (too many transactions)
- Geographic inconsistency

### Technical Issues
- Payment gateway down
- Temporary connectivity issue
- Timeout during processing
- Banking system issue

### Account Restrictions
- Account flagged for dispute
- High-risk designation
- Payment processor restriction
- Region/country restrictions

## Diagnostic Steps

### Step 1: Check Payment Status
1. Log into Clouddash account
2. Go to **Settings** → **Billing** → **Payment Method**
3. Look for error message or notification
4. Check **Recent Transactions** for failed attempt
5. Note the exact error message

### Step 2: Review Billing Information
1. Go to **Settings** → **Billing** → **Billing Address**
2. Verify address matches payment card:
   - Street address correct
   - City/State/ZIP accurate
   - Country correct
   - No extra spaces or characters
3. Compare with card statement

### Step 3: Check Card Details
1. Verify credit card not expired:
   - Expiration date on card
   - Current date before expiration
   - Check MM/YY format
2. Confirm card is active:
   - Not cancelled by issuer
   - Not reported lost or stolen
   - Not flagged for fraud

### Step 4: Monitor Account Status
1. Go to **Settings** → **Account** → **Status**
2. Look for:
   - **Active**: Service running normally
   - **Suspended**: Payment failed, service limited
   - **Pending Verification**: Account review in progress
   - **Flagged**: Potential issue detected
3. Note any suspension message

### Step 5: Check Email Notifications
1. Check email (including spam folder) for:
   - "Payment Failed" notification
   - "Billing Issue" alert
   - "Action Required" message
   - "Service Suspension Notice"
2. Note exact error mentioned
3. Check for payment deadline

## Resolution Steps

### Quick Fix: Update Payment Method

1. **Go to Payment Settings**
   - Settings → Billing → Payment Method
   - Click **Update Payment Method**

2. **Enter Valid Card**
   - Card number (no spaces)
   - Expiration date (MM/YY)
   - CVV/CVC code (3-4 digits)
   - Cardholder name

3. **Verify Billing Address**
   - Street address (no abbreviations)
   - City name
   - State/Province
   - ZIP/Postal code
   - Country

4. **Save and Retry**
   - Click **Save**
   - System automatically retries payment
   - May take 2-5 minutes
   - Check for confirmation email

5. **Verify Success**
   - Billing page should show "Active"
   - No error messages
   - Confirmation email received
   - Service fully accessible

### Fix: Correct Billing Address

1. **Get Current Card Information**
   - Check your credit card statement
   - Note exact billing address as shown
   - Include all address details

2. **Update Address in Clouddash**
   - Settings → Billing → Billing Address
   - Street Address (Line 1 and 2 if needed)
   - City (spell out completely, no abbreviations)
   - State/Province (full name, not abbreviation)
   - ZIP/Postal Code (exact format on card)
   - Country

3. **Save Changes**
   - Click **Save Address**
   - System validates address format
   - Address should be saved

4. **Retry Payment**
   - Go back to payment method
   - Click **Retry Payment** if visible
   - Or update card to trigger retry
   - Check email for result

### Fix: Use Different Card

If current card continues failing:

1. **Add Alternative Payment Method**
   - Settings → Billing → Payment Methods
   - Click **+ Add Payment Method**
   - Choose different card or account

2. **Use Valid Card**
   - Ensure card is active and not expired
   - Sufficient available balance
   - Not previously declined by Clouddash

3. **Set as Primary**
   - New card should be marked default
   - Used for next billing cycle
   - Previous failed card can be removed

4. **Test Payment**
   - Optional: Make small one-time charge to test
   - Confirms card is accepted
   - Then proceed with subscription

### Fix: Address Specific Error Messages

**"Card Declined"**
- Contact your bank/credit card issuer
- Verify card not cancelled or suspended
- Ask about fraud alerts
- May need to authorize Clouddash transactions
- Try different card if available

**"Invalid Card Number"**
- Re-enter card number carefully
- Check for typos
- Verify all digits included
- Try formatting without spaces
- Check card statement for exact number

**"Expired Card"**
- Card expiration date passed
- Only option: Use different valid card
- Or renew card with issuer and update

**"Insufficient Funds"**
- Account balance too low
- Available credit insufficient
- Wait for deposits to post
- Use card with higher balance
- Consider payment plan options

**"Billing Address Mismatch"**
- Update billing address exactly as on card
- No abbreviations (Avenue not Ave)
- Check ZIP code carefully
- Try card without apartment/suite number
- Contact card issuer if address differs from records

**"Transaction Declined by Bank"**
- Contact your bank/issuer
- May need to authorize Clouddash
- Geographic blocks (traveling)?
- Large transaction flagged?
- Request they whitelist Clouddash

**"Security Check Failed"**
- Card locked for security
- Contact card issuer to unlock
- May require verification call
- Some cards need activation after issue

### Fix: Resolve Account Restrictions

If account shows "Flagged" or "Suspended":

1. **Contact Support**
   - Email: support@clouddash.io
   - Reference your account
   - Explain payment failure
   - Provide screenshot of error

2. **Provide Information**
   - Account email address
   - Invoice number
   - Billing address
   - Last 4 of payment card
   - Payment failure date/time

3. **Resolution**
   - Support may require identity verification
   - May lift restrictions after verification
   - Flag may be removed to retry payment
   - Service restored after successful payment

4. **Prevent Future Issues**
   - Follow up on payment reminders
   - Keep billing information current
   - Update payment method before expiration
   - Monitor for payment failures

## Prevention

### Keep Billing Information Current
- Update payment method 30 days before expiration
- Update billing address when you move
- Verify information annually
- Notify of any address changes

### Enable Payment Notifications
- Settings → Notifications → Billing
- Enable payment failure alerts
- Quick notification when issues occur
- Time to fix before service suspended

### Set Up Auto-Renewal
- Automatic payments ensure no gaps
- Failures are handled immediately
- Service continuity assured
- One-time payment options available

### Monitor Invoice Due Dates
- Calendar reminder for payment due dates
- Check email for billing notifications
- Review invoices within 24 hours of receipt
- Report discrepancies immediately

## Temporary Solutions

### If Payment Can't Be Resolved Immediately

**Contact Support for:**
- Payment plan options
- Extended grace period
- Temporary service continuation
- Enterprise customer accommodations

**Alternative Options:**
- Switch to lower plan tier (temporarily)
- Remove add-ons to reduce cost
- Request billing date change
- Pause service temporarily (for annual plans)

## When Account is Suspended

### What Happens
- Access to dashboards removed
- Alerts stop firing
- Metric ingestion pauses
- API calls rejected
- Data retained for 30 days

### How to Restore
1. Update payment method
2. Retry failed payment
3. Payment processes successfully
4. Service restored within 5-10 minutes
5. Data and settings intact

### Grace Period
- Service suspended for 30 days
- Data not deleted immediately
- If payment made within 30 days: Full restoration
- After 30 days: Account deleted, data lost

## Special Situations

### Business/Enterprise Accounts
- May have custom payment terms
- Invoice-based billing option
- NET-30, NET-60 terms possible
- Contact Account Manager

### Dispute or Chargeback
- If you dispute charge: Service suspended
- Cannot re-enable until resolved
- Payment processor investigates
- Account permanently closed if chargebacked
- Future accounts may be rejected

### Payment for Multiple Accounts
- If managing multiple accounts
- Each has separate payment method
- One failed payment affects only that account
- Other accounts continue normally

## Support Resources

**For Payment Help:**
- Email: billing@clouddash.io
- Response time: 24 hours
- Include invoice number
- Provide error details

**For Technical Issues:**
- Email: support@clouddash.io
- Chat: In-app support
- Help Center: FAQs and guides

**For Account Questions:**
- Email: support@clouddash.io
- Phone: Available for enterprise
- Hours: Monday-Friday, 9 AM - 5 PM EST

## FAQ

**Q: How long before my service is suspended after failed payment?**
A: Immediately upon failure. You have 30 days grace period to resolve before permanent deletion.

**Q: Can I get a refund if my service was suspended due to payment failure?**
A: Typically no. Service was available and suspended due to non-payment. Refund only if service unavailable on your end.

**Q: What happens to my data during suspension?**
A: Data retained for 30 days. If payment resolved within 30 days, restored. After 30 days, permanently deleted.

**Q: Can I downgrade to avoid payment failure?**
A: Yes. Downgrading reduces monthly charge. Prorated credit applied to next invoice.

**Q: How do I prevent this from happening again?**
A: Enable auto-renewal, set billing alerts, update card 30 days before expiration, and verify billing address annually.
