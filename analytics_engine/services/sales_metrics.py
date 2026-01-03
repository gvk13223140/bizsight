from django.db.models import Sum
from django.db.models.functions import TruncDate, TruncMonth


def get_sales_overview(bills):
    return {
        "total_sales": bills.aggregate(Sum("total_amount"))["total_amount__sum"] or 0,
        "bill_count": bills.count(),
        "paid": bills.filter(payment_status="PAID").count(),
        "unpaid": bills.exclude(payment_status="PAID").count(),
    }


def get_sales_by_day(bills):
    return (
        bills
        .annotate(label=TruncDate("created_at"))
        .values("label")
        .annotate(total=Sum("total_amount"))
        .order_by("label")
    )


def get_sales_by_month(bills):
    return (
        bills
        .annotate(label=TruncMonth("created_at"))
        .values("label")
        .annotate(total=Sum("total_amount"))
        .order_by("label")
    )
