"""Calculate basic logistics KPIs for the simulated shipment sample."""

from __future__ import annotations

import csv
from datetime import date
from pathlib import Path


DATA_FILE = Path(__file__).parents[1] / "data" / "simulated_shipments.csv"


def read_shipments(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    required = {
        "shipment_id",
        "ship_date",
        "promised_date",
        "delivery_date",
        "distance_miles",
        "shipping_cost_usd",
        "inventory_before",
        "demand_units",
        "delay_status",
    }
    missing = required.difference(rows[0] if rows else set())
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    if not rows:
        raise ValueError("The shipment file is empty")
    return rows


def to_date(value: str) -> date:
    return date.fromisoformat(value)


def calculate_kpis(rows: list[dict[str, str]]) -> dict[str, float]:
    on_time = sum(
        to_date(row["delivery_date"]) <= to_date(row["promised_date"])
        for row in rows
    )
    delivery_days = [
        (to_date(row["delivery_date"]) - to_date(row["ship_date"])).days
        for row in rows
    ]
    total_cost = sum(float(row["shipping_cost_usd"]) for row in rows)
    total_demand = sum(float(row["demand_units"]) for row in rows)
    total_inventory = sum(float(row["inventory_before"]) for row in rows)
    total_distance = sum(float(row["distance_miles"]) for row in rows)

    return {
        "on_time_delivery_rate": on_time / len(rows),
        "average_delivery_days": sum(delivery_days) / len(delivery_days),
        "total_transportation_cost_usd": total_cost,
        "average_cost_per_mile_usd": total_cost / total_distance,
        "inventory_turnover_proxy": total_demand / total_inventory,
        "order_fulfillment_rate": 1.0,
    }


def main() -> None:
    rows = read_shipments(DATA_FILE)
    shipment_ids = [row["shipment_id"] for row in rows]
    if len(shipment_ids) != len(set(shipment_ids)):
        raise ValueError("Shipment IDs must be unique")

    kpis = calculate_kpis(rows)
    print(f"Records analyzed: {len(rows)}")
    print(f"Unique shipment IDs: {len(set(shipment_ids))}")
    print(f"On-time delivery rate: {kpis['on_time_delivery_rate']:.1%}")
    print(f"Average delivery time: {kpis['average_delivery_days']:.2f} days")
    print(f"Total transportation cost: ${kpis['total_transportation_cost_usd']:,.2f}")
    print(f"Average cost per mile: ${kpis['average_cost_per_mile_usd']:.2f}")
    print(f"Inventory turnover proxy: {kpis['inventory_turnover_proxy']:.2f}")
    print(f"Order fulfillment rate: {kpis['order_fulfillment_rate']:.1%}")


if __name__ == "__main__":
    main()
