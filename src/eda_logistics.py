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

    # Keep plotting available for interactive EDA without forcing a display.
    sns.set_theme(style="whitegrid")
    df[numeric_columns].hist(figsize=(10, 7))
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
