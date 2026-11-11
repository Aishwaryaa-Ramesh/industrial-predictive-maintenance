import os
import json
import joblib
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "predictive_maintenance_model.pkl"
)

THRESHOLD_PATH = os.path.join(
    BASE_DIR,
    "models",
    "decision_threshold.json"
)


def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Model file not found: {MODEL_PATH}"
        )

    model = joblib.load(MODEL_PATH)

    return model


def load_threshold():
    if not os.path.exists(THRESHOLD_PATH):
        raise FileNotFoundError(
            f"Threshold file not found: {THRESHOLD_PATH}"
        )

    with open(THRESHOLD_PATH, "r") as file:
        config = json.load(file)

    threshold = float(config["decision_threshold"])

    if not 0 < threshold < 1:
        raise ValueError("Decision threshold must be between 0 and 1.")

    return threshold

EXPECTED_FEATURES = [
    "Type",
    "Air temperature [K]",
    "Process temperature [K]",
    "Rotational speed [rpm]",
    "Torque [Nm]",
    "Tool wear [min]"
]


def validate_input(data):
    if not isinstance(data, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")

    if data.empty:
        raise ValueError("Input data cannot be empty.")

    missing_features = [
        feature for feature in EXPECTED_FEATURES
        if feature not in data.columns
    ]

    if missing_features:
        raise ValueError(
            f"Missing required features: {missing_features}"
        )

    # Keep only the expected model features in the correct order
    data = data[EXPECTED_FEATURES].copy()

    # Validate machine type
    if not data["Type"].isin(["L", "M", "H"]).all():
        raise ValueError("Type must be L, M or H.")

    # Convert sensor columns to numeric values
    numeric_features = EXPECTED_FEATURES[1:]

    for feature in numeric_features:
        data[feature] = pd.to_numeric(
            data[feature],
            errors="coerce"
        )

    # Check for missing or invalid numeric values
    if data[numeric_features].isnull().any().any():
        raise ValueError(
            "Sensor values must be valid numeric values."
        )

    # Check for infinite values
    if not np.isfinite(
            data[numeric_features].to_numpy(dtype=float)
    ).all():
        raise ValueError(
            "Sensor values cannot contain infinity."
        )

    return data


def predict_machine_failure(data):
    model = load_model()
    threshold = load_threshold()

    data = validate_input(data)

    probabilities = model.predict_proba(data)[:, 1]

    predictions = (probabilities >= threshold).astype(int)

    results = data.copy()

    results["Failure Probability"] = probabilities
    results["Predicted Failure"] = predictions

    results["Machine Status"] = [
        "Potential Failure" if prediction == 1
        else "Normal"
        for prediction in predictions
    ]

    return results

## test block
if __name__ == "__main__":
    sample_data = pd.DataFrame([{
        "Type": "M",
        "Air temperature [K]": 300.0,
        "Process temperature [K]": 310.0,
        "Rotational speed [rpm]": 1500,
        "Torque [Nm]": 40.0,
        "Tool wear [min]": 120
    }])

    prediction_result = predict_machine_failure(sample_data)

    print("\nMachine Prediction Result:")
    print(prediction_result.to_string(index=False))