"""Prepare predictors and target for a transportation-cost model."""

from pathlib import Path

import pandas as pd


DATA_FILE = Path(__file__).parents[1] / "data" / "simulated_shipments.csv"


def load_model_data(path: Path = DATA_FILE) -> tuple[pd.DataFrame, pd.Series]:
    df = pd.read_csv(path)

    # Freight_Value is not present in this sample; use available operational fields.
    features = [
        "distance_miles",
        "demand_units",
        "inventory_before",
        "transportation_mode",
    ]
    target = "shipping_cost_usd"

    model_data = df[features + [target]].dropna()
    X = pd.get_dummies(
        model_data[features],
        columns=["transportation_mode"],
        drop_first=True,
    )
    y = model_data[target]
    return X, y


def main() -> None:
    X, y = load_model_data()
    print("Feature columns:", list(X.columns))
    print("Target column: shipping_cost_usd")
    print("Feature shape:", X.shape)
    print("Target shape:", y.shape)
    print(X.head())
    print(y.head())


if __name__ == "__main__":
    main()
