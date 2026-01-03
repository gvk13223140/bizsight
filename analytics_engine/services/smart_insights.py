def get_smart_insights(bills):
    insights = []

    total = bills.count()
    unpaid = bills.exclude(payment_status="PAID").count()

    if total == 0:
        return ["No sales data available yet"]

    if unpaid > total * 0.3:
        insights.append("⚠ High number of unpaid bills")

    big_bills = bills.filter(total_amount__gte=5000).count()
    if big_bills:
        insights.append(f"💰 {big_bills} high-value bills above ₹5,000")

    return insights or ["Sales look healthy 👍"]
