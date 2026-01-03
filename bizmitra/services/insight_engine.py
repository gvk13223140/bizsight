from .tf_risk_model import predict_risk

def generate_insights(features):
    insights = []

    risk_score = float(predict_risk(features))
    unpaid_ratio = features["unpaid_ratio"]
    avg_bill = features["avg_bill_value"]

    # 1️⃣ ML risk insight (ALWAYS shown)
    insights.append({
        "level": "risk" if risk_score > 0.6 else "success",
        "title": "ML Cash-Flow Risk Forecast",
        "risk_score": risk_score,
        "message": f"Predicted cash-flow risk is {int(risk_score * 100)}%.",
        "recommendation": (
            "Reduce unpaid exposure immediately."
            if risk_score > 0.6
            else "Risk levels are stable."
        ),
    })

    # 2️⃣ Unpaid exposure (ONLY if real)
    if unpaid_ratio > 0.3:
        insights.append({
            "level": "warning",
            "title": "Unpaid Exposure Pattern",
            "unpaid_ratio": unpaid_ratio,
            "message": f"{int(unpaid_ratio * 100)}% of bills are unpaid.",
            "recommendation": "Enable reminders or advance payments.",
        })

    # 3️⃣ Average bill value
    if avg_bill < 1000:
        insights.append({
            "level": "warning",
            "title": "Low Order Value",
            "avg_bill_value": avg_bill,
            "message": f"Average bill value is ₹{int(avg_bill)}.",
            "recommendation": "Bundle products or upsell.",
        })

    return insights