"""AI tools for the Commissions module."""
from assistant.tools import AssistantTool, register_tool


@register_tool
class GetCommissionSummary(AssistantTool):
    name = "get_commission_summary"
    description = "Get commission summary for a date range: total pending, approved, paid by staff."
    module_id = "commissions"
    required_permission = "commissions.view_commissiontransaction"
    parameters = {
        "type": "object",
        "properties": {
            "date_from": {"type": "string", "description": "Start date (YYYY-MM-DD)"},
            "date_to": {"type": "string", "description": "End date (YYYY-MM-DD)"},
            "staff_id": {"type": "string", "description": "Filter by staff member ID"},
        },
        "required": [],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from datetime import date, timedelta
        from django.db.models import Sum, Count
        from commissions.models import CommissionTransaction
        date_from = args.get('date_from', str(date.today().replace(day=1)))
        date_to = args.get('date_to', str(date.today()))
        qs = CommissionTransaction.objects.filter(
            transaction_date__gte=date_from,
            transaction_date__lte=date_to,
        )
        if args.get('staff_id'):
            qs = qs.filter(staff_id=args['staff_id'])
        by_status = qs.values('status').annotate(
            total=Sum('commission_amount'),
            count=Count('id'),
        )
        return {
            "date_from": date_from,
            "date_to": date_to,
            "by_status": [
                {"status": item['status'], "total": str(item['total'] or 0), "count": item['count']}
                for item in by_status
            ],
        }


@register_tool
class ListCommissionRules(AssistantTool):
    name = "list_commission_rules"
    description = "List active commission rules."
    module_id = "commissions"
    required_permission = "commissions.view_commissionrule"
    parameters = {
        "type": "object",
        "properties": {},
        "required": [],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from commissions.models import CommissionRule
        rules = CommissionRule.objects.filter(is_active=True).order_by('priority')
        return {
            "rules": [
                {
                    "id": str(r.id),
                    "name": r.name,
                    "rule_type": r.rule_type,
                    "rate": str(r.rate) if r.rate else None,
                    "priority": r.priority,
                    "effective_from": str(r.effective_from) if r.effective_from else None,
                    "effective_until": str(r.effective_until) if r.effective_until else None,
                }
                for r in rules
            ]
        }


@register_tool
class CreateCommissionRule(AssistantTool):
    name = "create_commission_rule"
    description = "Create a commission rule (e.g., '10% on all sales', '5% on services')."
    module_id = "commissions"
    required_permission = "commissions.add_commissionrule"
    requires_confirmation = True
    parameters = {
        "type": "object",
        "properties": {
            "name": {"type": "string", "description": "Rule name"},
            "rule_type": {"type": "string", "description": "Rule type"},
            "rate": {"type": "string", "description": "Commission rate percentage"},
            "effective_from": {"type": "string", "description": "Start date (YYYY-MM-DD)"},
            "effective_until": {"type": "string", "description": "End date (YYYY-MM-DD)"},
            "priority": {"type": "integer", "description": "Priority order (lower = higher priority)"},
        },
        "required": ["name", "rate"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from decimal import Decimal
        from commissions.models import CommissionRule
        r = CommissionRule.objects.create(
            name=args['name'], rule_type=args.get('rule_type', ''),
            rate=Decimal(args['rate']),
            effective_from=args.get('effective_from'),
            effective_until=args.get('effective_until'),
            priority=args.get('priority', 10),
        )
        return {"id": str(r.id), "name": r.name, "rate": str(r.rate), "created": True}


@register_tool
class UpdateCommissionRule(AssistantTool):
    name = "update_commission_rule"
    description = "Update a commission rule's name, rate, dates, or priority."
    module_id = "commissions"
    required_permission = "commissions.change_commissionrule"
    requires_confirmation = True
    parameters = {
        "type": "object",
        "properties": {
            "rule_id": {"type": "string", "description": "Commission rule ID"},
            "name": {"type": "string"},
            "rule_type": {"type": "string", "description": "flat, percentage, tiered"},
            "rate": {"type": "string", "description": "Commission rate"},
            "effective_from": {"type": "string", "description": "Start date (YYYY-MM-DD)"},
            "effective_until": {"type": "string", "description": "End date (YYYY-MM-DD)"},
            "priority": {"type": "integer"},
            "is_active": {"type": "boolean"},
        },
        "required": ["rule_id"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from decimal import Decimal
        from commissions.models import CommissionRule
        try:
            r = CommissionRule.objects.get(id=args['rule_id'])
        except CommissionRule.DoesNotExist:
            return {"error": "Commission rule not found"}
        for field in ('name', 'rule_type', 'effective_from', 'effective_until', 'priority', 'is_active'):
            if args.get(field) is not None:
                setattr(r, field, args[field])
        if args.get('rate') is not None:
            r.rate = Decimal(args['rate'])
        r.save()
        return {"id": str(r.id), "name": r.name, "updated": True}


@register_tool
class DeleteCommissionRule(AssistantTool):
    name = "delete_commission_rule"
    description = "Delete a commission rule."
    module_id = "commissions"
    required_permission = "commissions.delete_commissionrule"
    requires_confirmation = True
    parameters = {
        "type": "object",
        "properties": {
            "rule_id": {"type": "string", "description": "Commission rule ID"},
        },
        "required": ["rule_id"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from commissions.models import CommissionRule
        try:
            r = CommissionRule.objects.get(id=args['rule_id'])
        except CommissionRule.DoesNotExist:
            return {"error": "Commission rule not found"}
        name = r.name
        r.delete()
        return {"name": name, "deleted": True}
