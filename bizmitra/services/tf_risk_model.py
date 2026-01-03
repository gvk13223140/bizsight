import tensorflow as tf
import numpy as np
import joblib
import os
from django.conf import settings

# BASE_DIR = E:/bizsight_backend/core
MODEL_PATH = os.path.join(settings.BASE_DIR, "risk_model.h5")
SCALER_PATH = os.path.join(settings.BASE_DIR, "scaler.pkl")

# Load once (important for performance)
model = tf.keras.models.load_model(MODEL_PATH)

scaler = None
if os.path.exists(SCALER_PATH):
    scaler = joblib.load(SCALER_PATH)


def predict_risk(features):
    """
    features: dict with keys
    - unpaid_ratio
    - avg_bill_value
    - bills_count
    """

    x = np.array([[
        features["unpaid_ratio"],
        features["avg_bill_value"],
        features["bills_count"],
    ]])

    if scaler:
        x = scaler.transform(x)
    else:
        # safe fallback normalization
        x = np.array([[
            features["unpaid_ratio"],
            min(features["avg_bill_value"] / 5000, 1.0),
            min(features["bills_count"] / 1000, 1.0),
        ]])

    risk_score = model(x, training=False).numpy()[0][0]
    return float(risk_score)
