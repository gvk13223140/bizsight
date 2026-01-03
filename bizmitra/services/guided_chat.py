def get_guided_response(features, query):
    query = query.lower()

    unpaid_ratio = features["unpaid_ratio"]
    avg_bill = features["avg_bill_value"]
    total_sales = features["total_sales"]
    trend = features["sales_trend"]

    if "unpaid" in query or "risk" in query:
        if unpaid_ratio == 0:
            return (
                "All your bills are paid. "
                "There is currently no cash-flow risk."
            )
        return (
            f"{int(unpaid_ratio * 100)}% of bills are unpaid. "
            "This can impact liquidity."
        )

    if "cash" in query:
        return (
            "Cash flow is under pressure due to unpaid bills."
            if unpaid_ratio > 0.3
            else "Cash flow appears stable."
        )

    if "growth" in query:
        return (
            "Upselling and bundles can increase revenue."
            if avg_bill < 3000
            else "Your order values are already healthy."
        )

    if "trend" in query or "pattern" in query:
        return f"Sales trend is currently {trend}."

    if "this week" in query:
        return (
            "This week, focus on collecting unpaid bills "
            "and sustaining current sales momentum."
        )

    if "what if" in query:
        return (
            "If unpaid exposure continues, future liquidity risk will rise. "
            "Reducing unpaid bills stabilizes growth."
        )

    return (
        "I can help with unpaid bills, cash-flow, growth, "
        "patterns, and what-if analysis."
    )