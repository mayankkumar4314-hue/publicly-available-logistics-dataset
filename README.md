# Logistics Data Science Project

## Reference dataset: 2022 Commodity Flow Survey

### 1. Dataset identification

The reference dataset for this project is the **2022 Commodity Flow Survey (CFS)**. It is publicly available from the **U.S. Census Bureau**, in partnership with the **Bureau of Transportation Statistics (BTS)**:

- Census Bureau CFS home: <https://www.census.gov/programs-surveys/cfs.html>
- 2022 CFS data and documentation: <https://www.census.gov/programs-surveys/cfs/data/datasets.html>
- BTS Freight Analysis Framework: <https://www.bts.gov/faf>

The CFS describes the movement of goods from U.S. establishments to their domestic and foreign destinations. It is relevant to a logistics project because it includes information about where freight starts and ends, what is shipped, how it is transported, how much it weighs, and the value of the shipment. These fields can support freight planning, mode comparison, and regional supply-chain analysis.

This project keeps an important distinction:

- **Public dataset:** the official CFS estimates and geography/commodity/mode definitions published by Census and BTS.
- **Simulated data:** `data/simulated_shipments.csv`, created only to demonstrate shipment-level delivery KPIs that the public CFS does not provide directly.

### 2. Dataset characteristics

The CFS is not a simple list of individual parcel deliveries. It is a statistical survey published in downloadable tables and files. The exact number of rows depends on the selected CFS file, geography, commodity, mode, and whether suppressed or zero cells are included. For that reason, this project does not invent one row count for the whole CFS. The official download page should be used for the row count of a chosen extract.

Important public CFS concepts include:

- **Origin and destination:** U.S. states, metropolitan areas, or other CFS geography codes.
- **Commodity:** the commodity classification and description for the goods moved.
- **Transportation mode:** for example truck, rail, water, air, pipeline, or multiple modes and mail.
- **Shipments, tons, and value:** estimated shipment count or weight, tons, and value in the published table.
- **Distance and ton-miles:** distance-related freight measures in files that include them.
- **Time period:** the 2022 survey year, with earlier benchmark surveys available for comparison.
- **Geographical coverage:** the United States, with participating in-scope establishments and their freight flows; the CFS is not a complete record of every international leg.

The main variable types are:

- **Numerical:** shipment counts or estimates, tons, value, distance, and ton-miles.
- **Categorical:** commodity code, transportation mode, and geography codes.
- **Time:** survey year and, in some files, reference-period or annual estimates. The public CFS does not normally contain an order date, promised delivery date, or actual delivery timestamp for each shipment.

Data-quality points should be considered before analysis. CFS values are estimates, not scanner-level observations. Some cells can be withheld or marked as confidential to protect businesses, and published totals can be affected by rounding. A user should check for missing or suppressed values, duplicate keys after joining files, inconsistent geography or commodity codes, and extreme values caused by aggregation. Large freight values are not automatically errors: they may represent a valid high-volume flow. Any outlier rule should therefore be checked against the CFS documentation.

### 3. Simulated data collection process

In a real logistics environment, one shipment could be assembled from several systems:

1. A customer order is created in an ERP or order-management system.
2. A warehouse management system records picking, packing, inventory level, and barcode scans.
3. A transportation management system assigns a carrier, mode, route, planned cost, and promised date.
4. A GPS device or carrier API sends location and movement events.
5. A delivery application records the actual delivery time, proof of delivery, and delay reason.
6. An integration service matches records using a shipment ID and stores validated rows in a central warehouse or data lake.

A simple simulation is: generate shipment IDs, choose realistic origins, destinations, modes, distances, quantities, and dates; calculate shipping time and cost; mark a shipment as on time when its actual delivery date is on or before its promised date; validate required fields and dates; then write the clean rows to `data/simulated_shipments.csv`. The script in `src/analyze_logistics.py` reads that file and produces summary KPIs.

### 4. Representative sample

The following 12 records are **simulated**, not copied from the public CFS. They use shipment-level fields that are useful for a later delivery analysis.

| Shipment ID | Origin | Destination | Mode | Ship Date | Promised Date | Delivery Date | Distance (mi) | Shipping Cost (USD) | Inventory Before | Demand Units | Delay Status |
|---|---|---|---|---|---|---|---:|---:|---:|---:|---|
| SIM-0001 | Chicago, IL | Detroit, MI | Truck | 2025-01-03 | 2025-01-05 | 2025-01-05 | 283 | 640 | 420 | 80 | On time |
| SIM-0002 | Dallas, TX | Atlanta, GA | Truck | 2025-01-04 | 2025-01-07 | 2025-01-08 | 781 | 1210 | 260 | 95 | Delayed |
| SIM-0003 | Seattle, WA | Portland, OR | Rail | 2025-01-05 | 2025-01-09 | 2025-01-09 | 174 | 510 | 680 | 120 | On time |
| SIM-0004 | Newark, NJ | Boston, MA | Truck | 2025-01-06 | 2025-01-07 | 2025-01-07 | 217 | 430 | 310 | 60 | On time |
| SIM-0005 | Los Angeles, CA | Phoenix, AZ | Truck | 2025-01-07 | 2025-01-09 | 2025-01-10 | 372 | 720 | 190 | 75 | Delayed |
| SIM-0006 | Memphis, TN | Nashville, TN | Air | 2025-01-08 | 2025-01-09 | 2025-01-09 | 210 | 980 | 520 | 100 | On time |
| SIM-0007 | Miami, FL | Orlando, FL | Truck | 2025-01-09 | 2025-01-10 | 2025-01-10 | 236 | 460 | 245 | 55 | On time |
| SIM-0008 | Denver, CO | Salt Lake City, UT | Rail | 2025-01-10 | 2025-01-13 | 2025-01-14 | 505 | 760 | 360 | 90 | Delayed |
| SIM-0009 | Houston, TX | New Orleans, LA | Water | 2025-01-11 | 2025-01-14 | 2025-01-13 | 348 | 390 | 800 | 140 | On time |
| SIM-0010 | Columbus, OH | Pittsburgh, PA | Truck | 2025-01-12 | 2025-01-14 | 2025-01-14 | 185 | 405 | 275 | 70 | On time |
| SIM-0011 | Minneapolis, MN | Milwaukee, WI | Truck | 2025-01-13 | 2025-01-15 | 2025-01-16 | 337 | 590 | 230 | 85 | Delayed |
| SIM-0012 | San Jose, CA | Las Vegas, NV | Air | 2025-01-14 | 2025-01-16 | 2025-01-16 | 386 | 1340 | 150 | 65 | On time |

The simulated table contains categorical variables such as origin, destination, mode, and delay status; numerical variables such as distance, cost, inventory, and demand; and date variables such as ship, promised, and delivery dates.

### 5. Data science relevance

The public CFS can be used to compare freight flows by region, commodity, and transportation mode. It can help a company study where demand is concentrated, estimate mode capacity needs, compare tonnage and freight value, and identify long-distance corridors. The simulated shipment table adds operational detail for a small demonstration.

The main KPIs are:

- **On-time delivery rate:** on-time shipments divided by all delivered shipments.
- **Average delivery time:** average number of days from ship date to delivery date.
- **Transportation cost:** average or total shipping cost, including cost per mile.
- **Inventory turnover:** demand or units shipped divided by average inventory for a defined period. This sample uses `inventory_before` as a simple demonstration, so a real project should use beginning and ending inventory.
- **Order fulfillment rate:** demand units fulfilled divided by demand units ordered. The sample assumes every listed demand quantity was fulfilled; a real system should include fulfilled quantity separately.

Future work could include exploratory analysis of cost by mode, charts of origin-destination flows, regression to estimate shipping cost or delivery time, clustering of routes, forecasting of freight demand, and optimization of carrier or mode selection. The CFS documentation and file definitions should be cited whenever a public variable is used.

## Run the example

From the project folder, run:

```text
python src/analyze_logistics.py
```

The command prints the KPI summary and checks that the sample has 12 unique shipment IDs. No third-party packages are required.
