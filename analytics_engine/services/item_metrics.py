from django.db.models import Sum
from billing.models import BillItem


def get_top_items(business, limit=5):
    return (
        BillItem.objects
        .filter(bill__business=business)
        .values("item_name")
        .annotate(
            total_qty=Sum("quantity"),
            revenue=Sum("total")
        )
        .order_by("-revenue")[:limit]
    )
