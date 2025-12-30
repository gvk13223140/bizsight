from django.utils import timezone
from datetime import timedelta
from billing.models import Bill
from django.db.models import Sum, Count


def get_bizmitra_insights(business):
    today = timezone.now().date()
    last_7_days = today - timedelta(days=7)
    prev_7_days = today - timedelta(days=14)

    insights = []

    # 1️⃣ Sales Trend
    recent_sales = Bill.objects.filter(
        business=business,
        created_at__date__gte=last_7_days
    ).aggregate(total=Sum("total_amount"))["total"] or 0

    previous_sales = Bill.objects.filter(
        business=business,
        created_at__date__gte=prev_7_days,
        created_at__date__lt=last_7_days
    ).aggregate(total=Sum("total_amount"))["total"] or 0

    if recent_sales < previous_sales:
        insights.append(
            "📉 Sales have dropped compared to last week."
        )

    # 2️⃣ Peak Hour
    peak_hour = (
        Bill.objects
        .filter(business=business)
        .extra(select={'hour': "strftime('%%H', created_at)"})
        .values('hour')
        .annotate(count=Count('id'))
        .order_by('-count')
        .first()
    )

    if peak_hour:
        insights.append(
            f"Most bills are generated around {peak_hour['hour']}:00 hrs."
        )

    # 3️⃣ Pay Later Risk
    pay_later_count = Bill.objects.filter(
        business=business,
        payment_status="PAY_LATER"
    ).count()

    if pay_later_count >= 3:
        insights.append(
            "⚠️ High number of Pay-Later bills detected. Cash flow risk."
        )

    if not insights:
        insights.append("✅ Business is running smoothly. No alerts.")

    return insights
