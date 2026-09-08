"""Group simulated logistics records with K-Means clustering."""

from pathlib import Path

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


DATA_FILE = Path(__file__).parents[1] / "data" / "simulated_shipments.csv"


def main() -> None:
    df = pd.read_csv(DATA_FILE)

    # shipping_cost_usd is the available monetary proxy for freight value.
    cluster_columns = [
        "distance_miles",
        "demand_units",
        "shipping_cost_usd",
    ]
    cluster_data = df[cluster_columns]

    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(cluster_data)

    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    df["cluster"] = kmeans.fit_predict(scaled_data)

    print(df[["shipment_id", "distance_miles", "demand_units", "cluster"]].head())
    print("\nRecords per cluster:")
    print(df["cluster"].value_counts().sort_index())
    print("\nCluster averages:")
    print(df.groupby("cluster")[cluster_columns].mean().round(2))


if __name__ == "__main__":
    main()
