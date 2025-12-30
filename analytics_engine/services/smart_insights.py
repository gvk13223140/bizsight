from datetime import date, timedelta
from django.db.models import Sum
from billing.models import Bill


def get_smart_insights(business):
    insights = []

    today = date.today()
    last_week = today - timedelta(days=7)
    prev_week = today - timedelta(days=14)

    last_week_sales = Bill.objects.filter(
        business=business,
        created_at__date__gte=last_week,
        payment_status="PAID"
    ).aggregate(Sum("total_amount"))["total_amount__sum"] or 0

    prev_week_sales = Bill.objects.filter(
        business=business,
        created_at__date__range=(prev_week, last_week),
        payment_status="PAID"
    ).aggregate(Sum("total_amount"))["total_amount__sum"] or 0

    if prev_week_sales > 0:
        change = ((last_week_sales - prev_week_sales) / prev_week_sales) * 100

        if change < -10:
            insights.append(
                f"⚠ Sales dropped by {abs(round(change,1))}% compared to last week"
            )
        elif change > 10:
            insights.append(
                f"📈 Sales increased by {round(change,1)}% compared to last week"
            )

    unpaid_count = Bill.objects.filter(
        business=business,
        payment_status="UNPAID"
    ).count()

    if unpaid_count >= 5:
        insights.append("⚠ High number of unpaid bills detected")

    if not insights:
        insights.append("✅ Business performance looks stable")

    return insights
