"""Basic exploratory analysis for the simulated logistics dataset."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


DATA_FILE = Path(__file__).parents[1] / "data" / "simulated_shipments.csv"


def main() -> None:
    # Parse dates so the initial inspection shows useful dtypes.
    df = pd.read_csv(
        DATA_FILE,
        parse_dates=["ship_date", "promised_date", "delivery_date"],
    )

    print("First five records:")
    print(df.head())
    print("\nDataset information:")
    df.info()
    print("\nDescriptive statistics:")
    print(df.describe(include="all"))

    numeric_columns = df.select_dtypes(include=np.number).columns
    print("\nNumeric columns:")
    print(list(numeric_columns))

    # Use project column names: demand_units is the shipment-volume proxy,
    # and shipping_cost_usd is the available monetary measure.
    mode_summary = df.groupby("transportation_mode")["demand_units"].mean()
    print("\nAverage shipment volume by transportation mode:")
    print(mode_summary)

    correlation_columns = [
        "distance_miles",
        "demand_units",
        "shipping_cost_usd",
    ]
    correlation = df[correlation_columns].corr()
    print("\nCorrelation between logistics variables:")
    print(correlation)

    # Keep plotting available for interactive EDA without forcing a display.
    sns.set_theme(style="whitegrid")
    sns.heatmap(correlation, annot=True, cmap="Blues", vmin=-1, vmax=1)
    plt.title("Correlation Between Logistics Variables")
    plt.tight_layout()
    plt.show()

    df[numeric_columns].hist(figsize=(10, 7))
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
