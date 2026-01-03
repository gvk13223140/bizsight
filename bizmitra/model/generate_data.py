import pandas as pd
import numpy as np

np.random.seed(42)
N = 10000

data = []

for _ in range(N):
    unpaid_ratio = round(np.random.beta(2, 5), 2)   # realistic skew
    avg_bill_value = np.random.randint(500, 20000)
    bills_count = np.random.randint(10, 5000)

    # Risk logic
    risk = 0
    if unpaid_ratio > 0.4:
        risk = 1
    if unpaid_ratio > 0.25 and avg_bill_value < 3000:
        risk = 1
    if unpaid_ratio > 0.3 and bills_count < 200:
        risk = 1

    data.append([
        unpaid_ratio,
        avg_bill_value,
        bills_count,
        risk
    ])

df = pd.DataFrame(
    data,
    columns=[
        "unpaid_ratio",
        "avg_bill_value",
        "bills_count",
        "risk_label"
    ]
)

df.to_csv("risk_data.csv", index=False)
print("10,000-row risk_data.csv generated successfully")