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

## Research section: FAF6 and data science methods

### 1. Dataset and data sources

For the wider research part of this project, the main public logistics dataset is the **Freight Analysis Framework, version 6 (FAF6)**. FAF6 is published by the **U.S. Department of Transportation's Bureau of Transportation Statistics (BTS)**. The Federal Highway Administration (FHWA) supports the FAF program, and the National Transportation Research Center at Oak Ridge National Laboratory (ORNL) hosts the public FAF6 data tools and documentation. The FAF is built from several sources, including Commodity Flow Survey data, Census Bureau international trade data, and information about agriculture, extraction, utilities, construction, services, and other economic sectors [1][2].

FAF6 estimates freight flows between FAF regions in the United States. A flow can be described by its origin, destination, commodity, transportation mode, year, and measure. Common measures include tons, value, and ton-miles. The FAF6 online tool provides selections such as the 2022 year, total flows, origin-destination geography, commodity, mode, and distance band [2]. These are **modeled and estimated flows**, not a live list of individual truck or parcel movements. This distinction matters when interpreting results.

The dataset is useful for this logistics scenario because it helps describe where freight is produced, where it is consumed, which commodities move between regions, and which modes carry the freight. It can support transportation planning, freight corridor studies, capacity planning, mode comparisons, and supply-chain decisions. FAF6 covers domestic freight flows and also represents international trade flows as they enter or leave the United States. The available years and forecast years should be checked in the current FAF6 download documentation before analysis because the published release controls which year selections are valid.

Important FAF6 variables include:

- **Origin and destination region:** the FAF zone or region where the flow begins and ends.
- **Commodity:** a commodity classification code and description.
- **Mode:** such as truck, rail, water, air, multiple modes and mail, pipeline, or other published FAF categories.
- **Year and flow type:** the selected historical, base, or forecast year and the type of flow being viewed.
- **Tons, value, and ton-miles:** measures of freight weight, economic value, and movement work.
- **Distance information:** where supplied by the FAF release or selected distance band.

Other useful public resources include the BTS Transportation Statistics Annual Reports and National Transportation Statistics, FHWA freight planning resources, the Census Bureau Commodity Flow Survey, the Bureau of Transportation Statistics National Transportation Atlas Database, and the U.S. Census Bureau international trade data. These sources can be joined carefully with geography and commodity definitions, but they do not necessarily use the same units, years, or observation level. A research dataset should record the source, download date, release version, unit, and any filters used.

### 2. Application of regression

Regression can estimate a numeric logistics outcome from one or more explanatory variables. For example, a project could predict freight volume in tons using distance, commodity type, transportation mode, shipment value, and origin and destination characteristics. It could also predict transportation cost when a separate cost field is available, or forecast future freight demand after creating time-based features. FAF6 itself is mainly a flow-estimation dataset, so a cost or delivery-time model may need additional carrier, fuel-price, GPS, or delivery-system data.

Categorical fields such as mode and commodity cannot be entered directly into most regression models. They can be encoded as indicator variables, while numeric fields such as tons, value, distance, and ton-miles can be scaled or transformed when their distributions are highly skewed. A simple train-test split or time-based split can be used to evaluate the model. Useful measures are **R²**, which describes explained variation; **MAE**, which gives the average absolute error in the outcome's units; and **RMSE**, which penalizes large errors more strongly.

Illustrative Python code for a flow file with these columns is:

```python
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder

flows = pd.read_csv("faf6_flows.csv")
features = ["distance_miles", "shipment_value", "commodity", "mode"]
X = flows[features]
y = flows["tons"]

preprocess = ColumnTransformer([
	("categorical", OneHotEncoder(handle_unknown="ignore"), ["commodity", "mode"]),
	("numeric", "passthrough", ["distance_miles", "shipment_value"]),
])
model = make_pipeline(preprocess, LinearRegression())
X_train, X_test, y_train, y_test = train_test_split(
	X, y, test_size=0.2, random_state=42
)
model.fit(X_train, y_train)
prediction = model.predict(X_test)
print("R2:", r2_score(y_test, prediction))
print("MAE:", mean_absolute_error(y_test, prediction))
print("RMSE:", mean_squared_error(y_test, prediction) ** 0.5)
```

This is an example of a method, not a result from the public FAF6 files. A real study should compare a baseline with more than one model, avoid leakage between training and test data, and explain that aggregated flows may hide differences between individual shipments.

### 3. Application of clustering

Clustering groups observations that are similar without requiring a target variable. A logistics analyst could create route-level or region-level features such as total tons, shipment value, distance, ton-miles, number of commodities, and the share moved by each mode. Origin, destination, commodity, and mode are categorical, so they need a suitable encoding or a summary such as mode shares before K-Means is used.

K-Means could produce groups such as high-volume short-distance routes, lower-volume regional routes, long-distance corridors, or high-value freight corridors. The number of groups should be tested with a method such as the elbow plot or silhouette score, and the results should be checked against logistics knowledge. Since K-Means is affected by scale, numeric features should normally be standardized. A cluster is a planning aid, not a label that is automatically meaningful.

The groups could support different decisions. High-volume routes may need larger contracted capacity and frequent departures. Long-distance routes may benefit from rail or intermodal comparisons. High-value routes may require stronger tracking and security. Lower-volume regions may be served by consolidation or less frequent shipments. Inventory policies can also differ by cluster when transit time and demand variability are different.

### 4. Application of optimization

Optimization can choose a feasible logistics plan from many alternatives. For example, a model can decide how much freight to assign to truck, rail, water, or another mode on each route while minimizing total cost. The objective could be:

```text
minimize total cost = sum(flow assigned to route and mode * unit cost)
```

Typical constraints require every shipment demand to be met, prevent a vehicle or route from exceeding capacity, enforce warehouse or terminal capacity, and require delivery within an allowed time. Other terms can represent emissions, handling charges, service penalties, or risk. A linear program is appropriate when quantities and costs are continuous and relationships are linear. Integer programming is useful when the decision includes whole vehicles, facilities, or yes/no choices. Network optimization is useful when freight moves through connected origins, hubs, and destinations.

FAF6 can provide demand, geography, commodity, mode, and distance inputs for the planning model. It does not by itself provide every operational input, such as a carrier contract rate, vehicle availability, warehouse stock, or a guaranteed delivery time. Those constraints should come from company systems or clearly documented assumptions.

### 5. Integrated data science approach

The three methods can be used in one workflow:

**Data collection -> Data cleaning -> Exploratory data analysis -> Regression -> Clustering -> Optimization -> Logistics decision-making**

First, analysts download FAF6 data and combine it with supporting public data or company records. They check units, missing or suppressed values, duplicate keys, geography codes, commodity codes, and differences between historical and forecast years. Exploratory analysis then shows the largest flows, important corridors, mode shares, unusual values, and changes over time.

Regression can forecast freight demand or estimate cost and transit-related outcomes. Clustering can group similar routes, regions, or commodities so that the organization does not use one policy for every flow. Optimization can then use the forecast demand and cluster-specific costs, capacities, and service requirements to recommend a transportation plan. The final plan should be reviewed by logistics staff and monitored with actual performance data.

### 6. Expected business impact

Used carefully, these methods can help logistics organizations:

- reduce transportation cost by comparing modes and assigning freight more efficiently;
- improve route and mode selection using distance, volume, value, and service requirements;
- forecast freight demand to support capacity, labor, and inventory planning;
- improve vehicle, terminal, and warehouse utilization;
- identify inefficient or unusually expensive logistics routes; and
- support supply-chain decisions with measurable evidence rather than informal estimates.

The expected benefit depends on data quality and implementation. FAF6 is valuable for strategic and regional planning, while operational decisions should be checked against current company data. Forecasts should be measured against later observations, clusters should be interpreted rather than accepted blindly, and optimization outputs should be tested for practical feasibility.

### Sources

1. U.S. Department of Transportation, Bureau of Transportation Statistics, [Freight Analysis Framework](https://www.bts.gov/faf).
2. Oak Ridge National Laboratory National Transportation Research Center, [Freight Analysis Framework 6 data tool](https://faf.ornl.gov/faf6/dtt_total.aspx).
3. U.S. Census Bureau, [Commodity Flow Survey](https://www.census.gov/programs-surveys/cfs.html).
4. U.S. Department of Transportation, Bureau of Transportation Statistics, [National Transportation Statistics](https://www.bts.gov/topics/national-transportation-statistics).
5. U.S. Federal Highway Administration, [Freight Management and Operations](https://ops.fhwa.dot.gov/freight/).
