from django.db.models import Sum
from billing.models import BillItem


def get_top_items(bills, limit=5):
    return (
        BillItem.objects
        .filter(bill__in=bills)
        .values("item_name")
        .annotate(
            qty=Sum("quantity"),
            revenue=Sum("total"),
        )
        .order_by("-revenue")[:limit]
    )
