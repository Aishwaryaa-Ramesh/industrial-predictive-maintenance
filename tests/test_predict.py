import unittest
import pandas as pd

from src.predict import predict_machine_failure


def create_valid_sample():
    """Create a valid sample machine input."""
    return pd.DataFrame([
        {
            "Type": "M",
            "Air temperature [K]": 300.0,
            "Process temperature [K]": 310.0,
            "Rotational speed [rpm]": 1500,
            "Torque [Nm]": 40.0,
            "Tool wear [min]": 120
        }
    ])


class TestPredictionModule(unittest.TestCase):

    def test_single_machine_prediction(self):
        data = create_valid_sample()

        result = predict_machine_failure(data)

        self.assertEqual(len(result), 1)
        self.assertIn("Failure Probability", result.columns)
        self.assertIn("Predicted Failure", result.columns)
        self.assertIn("Machine Status", result.columns)

        probability = result.loc[0, "Failure Probability"]
        self.assertGreaterEqual(probability, 0)
        self.assertLessEqual(probability, 1)

        self.assertIn(result.loc[0, "Predicted Failure"], [0, 1])

    def test_multiple_machine_predictions(self):
        data = pd.concat(
            [create_valid_sample(), create_valid_sample()],
            ignore_index=True
        )

        result = predict_machine_failure(data)

        self.assertEqual(len(result), 2)

    def test_missing_feature(self):
        data = create_valid_sample().drop(
            columns=["Torque [Nm]"]
        )

        with self.assertRaises(ValueError):
            predict_machine_failure(data)

    def test_invalid_machine_type(self):
        data = create_valid_sample()
        data.loc[0, "Type"] = "X"

        with self.assertRaises(ValueError):
            predict_machine_failure(data)

    def test_non_numeric_sensor_value(self):
        data = create_valid_sample()

        data["Torque [Nm]"] = data["Torque [Nm]"].astype(object)
        data.loc[0, "Torque [Nm]"] = "invalid"

        with self.assertRaises(ValueError):
            predict_machine_failure(data)

    def test_infinite_sensor_value(self):
        data = create_valid_sample()
        data.loc[0, "Torque [Nm]"] = float("inf")

        with self.assertRaises(ValueError):
            predict_machine_failure(data)


if __name__ == "__main__":
    unittest.main()

