"""Clean the simulated logistics dataset for later analysis."""

from pathlib import Path

import pandas as pd


DATA_FILE = Path(__file__).parents[1] / "data" / "simulated_shipments.csv"


def clean_logistics_data(path: Path = DATA_FILE) -> pd.DataFrame:
    df = pd.read_csv(
        path,
        parse_dates=["ship_date", "promised_date", "delivery_date"],
    )

    print("Missing values before cleaning:")
    print(df.isnull().sum())

    # Remove exact duplicate records before applying field-level rules.
    df = df.drop_duplicates().copy()

    # This sample has demand_units rather than Shipment_Weight.
    df["demand_units"] = df["demand_units"].fillna(
        df["demand_units"].median()
    )

    # Dates are parsed during import; this is safe if the input changes later.
    df["ship_date"] = pd.to_datetime(df["ship_date"], errors="coerce")

    # Keep only physically meaningful distance and quantity values.
    df = df[df["distance_miles"] > 0]
    df = df[df["demand_units"] > 0]

    return df.reset_index(drop=True)


def main() -> None:
    cleaned = clean_logistics_data()
    print(f"Clean records: {len(cleaned)}")
    print("Missing values after cleaning:")
    print(cleaned.isnull().sum())
    print(cleaned.head())


if __name__ == "__main__":
    main()
