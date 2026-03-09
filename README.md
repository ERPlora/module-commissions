# Commissions

## Overview

| Property | Value |
|----------|-------|
| **Module ID** | `commissions` |
| **Version** | `1.0.0` |
| **Dependencies** | `staff`, `services`, `inventory`, `sales`, `appointments` |

## Dependencies

This module requires the following modules to be installed:

- `staff`
- `services`
- `inventory`
- `sales`
- `appointments`

## Models

### `CommissionsSettings`

Per-hub commissions settings.

| Field | Type | Details |
|-------|------|---------|
| `default_commission_rate` | DecimalField |  |
| `calculation_basis` | CharField | max_length=20, choices: gross, net, profit |
| `payout_frequency` | CharField | max_length=20, choices: weekly, biweekly, monthly, custom |
| `payout_day` | PositiveSmallIntegerField |  |
| `minimum_payout_amount` | DecimalField |  |
| `apply_tax_withholding` | BooleanField |  |
| `tax_withholding_rate` | DecimalField |  |
| `show_commission_on_receipt` | BooleanField |  |
| `show_pending_commission` | BooleanField |  |

**Methods:**

- `get_settings()`
- `calculate_tax()` — Calculate tax withholding on a commission amount.

### `CommissionRule`

Commission rules for different scenarios.

| Field | Type | Details |
|-------|------|---------|
| `name` | CharField | max_length=100 |
| `description` | TextField | optional |
| `rule_type` | CharField | max_length=20, choices: flat, percentage, tiered |
| `rate` | DecimalField |  |
| `staff` | ForeignKey | → `staff.StaffMember`, on_delete=SET_NULL, optional |
| `service` | ForeignKey | → `services.Service`, on_delete=SET_NULL, optional |
| `category` | ForeignKey | → `services.ServiceCategory`, on_delete=SET_NULL, optional |
| `product` | ForeignKey | → `inventory.Product`, on_delete=SET_NULL, optional |
| `tier_thresholds` | JSONField | optional |
| `effective_from` | DateField | optional |
| `effective_until` | DateField | optional |
| `priority` | PositiveIntegerField |  |
| `is_active` | BooleanField |  |

**Methods:**

- `is_applicable_on()`
- `calculate_commission()` — Calculate commission for given amount.

### `CommissionTransaction`

Individual commission transaction record.

| Field | Type | Details |
|-------|------|---------|
| `staff` | ForeignKey | → `staff.StaffMember`, on_delete=SET_NULL, optional |
| `staff_name` | CharField | max_length=200 |
| `sale` | ForeignKey | → `sales.Sale`, on_delete=SET_NULL, optional |
| `sale_reference` | CharField | max_length=100, optional |
| `appointment` | ForeignKey | → `appointments.Appointment`, on_delete=SET_NULL, optional |
| `sale_amount` | DecimalField |  |
| `commission_rate` | DecimalField |  |
| `commission_amount` | DecimalField |  |
| `tax_amount` | DecimalField |  |
| `net_commission` | DecimalField |  |
| `rule` | ForeignKey | → `commissions.CommissionRule`, on_delete=SET_NULL, optional |
| `status` | CharField | max_length=20, choices: pending, approved, paid, cancelled, adjusted |
| `payout` | ForeignKey | → `commissions.CommissionPayout`, on_delete=SET_NULL, optional |
| `transaction_date` | DateField |  |
| `approved_at` | DateTimeField | optional |
| `approved_by` | ForeignKey | → `accounts.LocalUser`, on_delete=SET_NULL, optional |
| `description` | TextField | optional |
| `notes` | TextField | optional |

### `CommissionPayout`

Commission payout batch.

| Field | Type | Details |
|-------|------|---------|
| `reference` | CharField | max_length=50 |
| `staff` | ForeignKey | → `staff.StaffMember`, on_delete=SET_NULL, optional |
| `staff_name` | CharField | max_length=200 |
| `period_start` | DateField |  |
| `period_end` | DateField |  |
| `gross_amount` | DecimalField |  |
| `tax_amount` | DecimalField |  |
| `adjustments_amount` | DecimalField |  |
| `net_amount` | DecimalField |  |
| `transaction_count` | PositiveIntegerField |  |
| `status` | CharField | max_length=20, choices: draft, pending, approved, processing, completed, failed, ... |
| `payment_method` | CharField | max_length=20, choices: cash, bank_transfer, check, payroll, other, optional |
| `payment_reference` | CharField | max_length=100, optional |
| `approved_at` | DateTimeField | optional |
| `approved_by` | ForeignKey | → `accounts.LocalUser`, on_delete=SET_NULL, optional |
| `paid_at` | DateTimeField | optional |
| `paid_by` | ForeignKey | → `accounts.LocalUser`, on_delete=SET_NULL, optional |
| `notes` | TextField | optional |

**Methods:**

- `recalculate_totals()`

**Properties:**

- `can_be_modified`

### `CommissionAdjustment`

Manual commission adjustments.

| Field | Type | Details |
|-------|------|---------|
| `staff` | ForeignKey | → `staff.StaffMember`, on_delete=SET_NULL, optional |
| `staff_name` | CharField | max_length=200 |
| `adjustment_type` | CharField | max_length=20, choices: bonus, correction, deduction, refund_adjustment, other |
| `amount` | DecimalField |  |
| `reason` | TextField |  |
| `payout` | ForeignKey | → `commissions.CommissionPayout`, on_delete=SET_NULL, optional |
| `adjustment_date` | DateField |  |

## Cross-Module Relationships

| From | Field | To | on_delete | Nullable |
|------|-------|----|-----------|----------|
| `CommissionRule` | `staff` | `staff.StaffMember` | SET_NULL | Yes |
| `CommissionRule` | `service` | `services.Service` | SET_NULL | Yes |
| `CommissionRule` | `category` | `services.ServiceCategory` | SET_NULL | Yes |
| `CommissionRule` | `product` | `inventory.Product` | SET_NULL | Yes |
| `CommissionTransaction` | `staff` | `staff.StaffMember` | SET_NULL | Yes |
| `CommissionTransaction` | `sale` | `sales.Sale` | SET_NULL | Yes |
| `CommissionTransaction` | `appointment` | `appointments.Appointment` | SET_NULL | Yes |
| `CommissionTransaction` | `rule` | `commissions.CommissionRule` | SET_NULL | Yes |
| `CommissionTransaction` | `payout` | `commissions.CommissionPayout` | SET_NULL | Yes |
| `CommissionTransaction` | `approved_by` | `accounts.LocalUser` | SET_NULL | Yes |
| `CommissionPayout` | `staff` | `staff.StaffMember` | SET_NULL | Yes |
| `CommissionPayout` | `approved_by` | `accounts.LocalUser` | SET_NULL | Yes |
| `CommissionPayout` | `paid_by` | `accounts.LocalUser` | SET_NULL | Yes |
| `CommissionAdjustment` | `staff` | `staff.StaffMember` | SET_NULL | Yes |
| `CommissionAdjustment` | `payout` | `commissions.CommissionPayout` | SET_NULL | Yes |
| `CommissionAdjustment` | `created_by` | `accounts.LocalUser` | SET_NULL | Yes |

## URL Endpoints

Base path: `/m/commissions/`

| Path | Name | Method |
|------|------|--------|
| `(root)` | `index` | GET |
| `dashboard/` | `dashboard` | GET |
| `transactions/` | `transaction_list` | GET |
| `transactions/<uuid:pk>/` | `transaction_detail` | GET |
| `transactions/<uuid:pk>/approve/` | `transaction_approve` | GET |
| `transactions/<uuid:pk>/reject/` | `transaction_reject` | GET |
| `payouts/` | `payout_list` | GET |
| `payouts/create/` | `payout_create` | GET/POST |
| `payouts/<uuid:pk>/` | `payout_detail` | GET |
| `payouts/<uuid:pk>/approve/` | `payout_approve` | GET |
| `payouts/<uuid:pk>/process/` | `payout_process` | GET |
| `payouts/<uuid:pk>/cancel/` | `payout_cancel` | GET |
| `rules/` | `rule_list` | GET |
| `rules/add/` | `rule_add` | GET/POST |
| `rules/<uuid:pk>/` | `rule_detail` | GET |
| `rules/<uuid:pk>/edit/` | `rule_edit` | GET |
| `rules/<uuid:pk>/delete/` | `rule_delete` | GET/POST |
| `rules/<uuid:pk>/toggle/` | `rule_toggle` | GET |
| `adjustments/` | `adjustment_list` | GET |
| `adjustments/add/` | `adjustment_add` | GET/POST |
| `adjustments/<uuid:pk>/` | `adjustment_detail` | GET |
| `adjustments/<uuid:pk>/delete/` | `adjustment_delete` | GET/POST |
| `settings/` | `settings` | GET |
| `settings/save/` | `settings_save` | GET/POST |
| `settings/toggle/` | `settings_toggle` | GET |
| `settings/input/` | `settings_input` | GET |
| `settings/reset/` | `settings_reset` | GET |
| `api/calculate/` | `api_calculate` | GET |
| `api/staff/<uuid:staff_pk>/summary/` | `api_staff_summary` | GET |

## Permissions

| Permission | Description |
|------------|-------------|
| `commissions.manage_settings` | Manage Settings |

**Role assignments:**

- **admin**: All permissions
- **manager**: 
- **employee**: 

## Navigation

| View | Icon | ID | Fullpage |
|------|------|----|----------|
| Overview | `stats-chart-outline` | `dashboard` | No |
| Transactions | `receipt-outline` | `transactions` | No |
| Payouts | `cash-outline` | `payouts` | No |
| Rules | `options-outline` | `rules` | No |
| Adjustments | `swap-horizontal-outline` | `adjustments` | No |
| Settings | `settings-outline` | `settings` | No |

## AI Tools

Tools available for the AI assistant:

### `get_commission_summary`

Get commission summary for a date range: total pending, approved, paid by staff.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `date_from` | string | No | Start date (YYYY-MM-DD) |
| `date_to` | string | No | End date (YYYY-MM-DD) |
| `staff_id` | string | No | Filter by staff member ID |

### `list_commission_rules`

List active commission rules.

### `create_commission_rule`

Create a commission rule (e.g., '10% on all sales', '5% on services').

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | Yes | Rule name |
| `rule_type` | string | No | Rule type |
| `rate` | string | Yes | Commission rate percentage |
| `effective_from` | string | No | Start date (YYYY-MM-DD) |
| `effective_until` | string | No | End date (YYYY-MM-DD) |
| `priority` | integer | No | Priority order (lower = higher priority) |

## File Structure

```
CHANGELOG.md
README.md
TODO.md
__init__.py
ai_tools.py
apps.py
forms.py
locale/
  es/
    LC_MESSAGES/
      django.po
migrations/
  0001_initial.py
  __init__.py
models.py
module.py
static/
  icons/
    ion/
templates/
  commissions/
    pages/
      adjustment_detail.html
      adjustments.html
      index.html
      payout_detail.html
      payouts.html
      rule_detail.html
      rules.html
      settings.html
      transaction_detail.html
      transactions.html
    partials/
      adjustment_detail.html
      adjustments.html
      dashboard.html
      payout_detail.html
      payouts.html
      rule_detail.html
      rules.html
      settings.html
      transaction_detail.html
      transactions.html
tests/
  __init__.py
  conftest.py
  test_models.py
  test_services.py
  test_views.py
urls.py
views.py
```
