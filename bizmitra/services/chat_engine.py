def respond(query, features):
    q = query.lower()

    if "risk" in q:
        return (
            f"Your current unpaid ratio is "
            f"{int(features['unpaid_ratio']*100)}%. "
            "This directly increases predicted risk."
        )

    if "increase sales" in q:
        return (
            "Based on billing patterns, increasing average bill value "
            "has the strongest impact on growth."
        )

    if "why" in q:
        return (
            "BizMitra analyzes unpaid behavior, bill frequency, "
            "and sales trends using ML patterns."
        )

    return (
        "I can help with risk, growth, unpaid bills, "
        "or forecasting questions."
    )
