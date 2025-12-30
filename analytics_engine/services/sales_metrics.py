from django.db.models import Sum, Count
from datetime import date, timedelta
from billing.models import Bill


def get_sales_overview(business):
    bills = Bill.objects.filter(business=business)

    return {
        "total_revenue": bills.filter(payment_status="PAID")
                              .aggregate(Sum("total_amount"))["total_amount__sum"] or 0,

        "total_bills": bills.count(),

        "paid_bills": bills.filter(payment_status="PAID").count(),
        "unpaid_bills": bills.filter(payment_status="UNPAID").count(),
        "pay_later_bills": bills.filter(payment_status="PAY_LATER").count(),
    }


def get_sales_by_day(business, days=7):
    today = date.today()
    start_date = today - timedelta(days=days)

    bills = (
        Bill.objects.filter(
            business=business,
            created_at__date__gte=start_date
        )
        .values("created_at__date")
        .annotate(total=Sum("total_amount"))
        .order_by("created_at__date")
    )

    return list(bills)
