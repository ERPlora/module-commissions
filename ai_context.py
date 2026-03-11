"""
AI context for the Commissions module.
Loaded into the assistant system prompt when this module's tools are active.
"""

CONTEXT = """
## Module Knowledge: Commissions

### Models

**CommissionsSettings** — Per-hub configuration (singleton).
- `default_commission_rate` (%, default 10.00)
- `calculation_basis`: 'gross' | 'net' | 'profit' — what percentage is applied to
- `payout_frequency`: 'weekly' | 'biweekly' | 'monthly' | 'custom'
- `payout_day`: Day of month/week for payouts (1-31)
- `minimum_payout_amount`
- `apply_tax_withholding`, `tax_withholding_rate` (%)
- `show_commission_on_receipt`, `show_pending_commission`
- Use `CommissionsSettings.get_settings(hub_id)`

**CommissionRule** — Defines how commissions are calculated.
- `name`, `description`
- `rule_type`: 'flat' | 'percentage' | 'tiered'
- `rate`: Flat amount or percentage depending on rule_type
- `staff` FK → staff.StaffMember (null = applies to all staff)
- `service` FK → services.Service (null = all services)
- `category` FK → services.ServiceCategory (null = all categories)
- `product` FK → inventory.Product (null = all products)
- `tier_thresholds` (JSONField): List of `{min_amount, max_amount, rate}` dicts for 'tiered' type
- `effective_from`, `effective_until` (DateField, optional)
- `priority`: Higher = applied first
- `is_active`

**CommissionTransaction** — Individual commission record per sale/appointment.
- `staff` FK → staff.StaffMember + `staff_name` (snapshot)
- `sale` FK → sales.Sale + `sale_reference` (snapshot)
- `appointment` FK → appointments.Appointment (optional)
- `sale_amount`: The sale value commissions are calculated on
- `commission_rate` (%): Rate applied
- `commission_amount`: Gross commission earned
- `tax_amount`: Tax withheld
- `net_commission`: commission_amount - tax_amount
- `rule` FK → CommissionRule (which rule generated this)
- `status`: 'pending' | 'approved' | 'paid' | 'cancelled' | 'adjusted'
- `payout` FK → CommissionPayout (once included in a payout batch)
- `transaction_date`, `approved_at`, `approved_by` FK → accounts.LocalUser

**CommissionPayout** — A batch payout for one staff member's commissions.
- `reference` (auto-generated: PAY-{YYYYMM}-{seq})
- `staff` FK → staff.StaffMember + `staff_name` (snapshot)
- `period_start`, `period_end`
- `gross_amount`, `tax_amount`, `adjustments_amount`, `net_amount` (= gross - tax + adjustments)
- `transaction_count`
- `status`: 'draft' | 'pending' | 'approved' | 'processing' | 'completed' | 'failed' | 'cancelled'
- `payment_method`: 'cash' | 'bank_transfer' | 'check' | 'payroll' | 'other'
- `payment_reference`, `approved_at`, `approved_by`, `paid_at`, `paid_by`

**CommissionAdjustment** — Manual correction/bonus/deduction to a payout.
- `staff` FK → staff.StaffMember + `staff_name` (snapshot)
- `adjustment_type`: 'bonus' | 'correction' | 'deduction' | 'refund_adjustment' | 'other'
- `amount`: Positive for additions, negative for deductions
- `reason`, `payout` FK → CommissionPayout (optional)
- `adjustment_date`, `created_by` FK → accounts.LocalUser

### Key Flows

1. **Record commission**: After a sale, find applicable CommissionRule (by staff/service/product/date), call `rule.calculate_commission(amount)` → create CommissionTransaction (status='pending')
2. **Approve transaction**: Manager reviews → status='approved', set approved_by/at
3. **Create payout**: Create CommissionPayout for staff+period → call `payout.recalculate_totals()` to aggregate linked transactions → link transactions via `transaction.payout = payout`
4. **Process payout**: Approve payout → status='approved' → mark paid → status='completed', paid_at set
5. **Adjustment**: Create CommissionAdjustment linked to payout; call `payout.recalculate_totals()` to reflect changes

### Relationships
- `CommissionRule.staff` → staff.StaffMember
- `CommissionTransaction.sale` → sales.Sale
- `CommissionTransaction.appointment` → appointments.Appointment
- `CommissionPayout.transactions` (reverse) → CommissionTransaction set
"""
