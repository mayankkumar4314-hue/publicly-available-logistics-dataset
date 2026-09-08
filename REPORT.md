# Logistics Data Science Project Report

## 1. Introduction

Logistics companies must move goods to the right place, at the right time, and at a reasonable cost. This project studies freight transportation and delivery planning. The main problem is that logistics managers need to decide which routes and transportation modes should receive capacity, while also controlling cost and maintaining reliable delivery performance.

Freight demand is not the same on every route. Some routes carry much more volume than others, some are long and expensive, and some shipments may be delayed. Decisions based only on experience can miss these patterns. Data science can combine freight-flow data with shipment records to describe the current situation, predict future demand or cost, group similar routes, and support better transportation decisions.

This project has two data layers:

- **Public research dataset:** Freight Analysis Framework version 6 (FAF6), published by the U.S. Department of Transportation Bureau of Transportation Statistics (BTS), with support from the Federal Highway Administration (FHWA) and data tools hosted by Oak Ridge National Laboratory (ORNL).
- **Simulated operational sample:** `data/simulated_shipments.csv`, created for this project to demonstrate shipment-level KPIs such as delivery time and delay status. It is not copied from FAF6.

## 2. Logistics Scenario

The scenario is regional freight transportation planning. A company receives orders from different locations and must choose routes and modes such as truck, rail, air, or water. The company wants to understand which routes have high demand, how distance and mode affect cost, and where delays or inefficient use of capacity may occur.

The causes of the problem include changing demand, different route distances, different mode capacities, fuel and handling costs, seasonal activity, and limited warehouse or carrier capacity. FAF6 can show the larger freight pattern between regions, but it does not provide live GPS positions or an actual delivery timestamp for every shipment. Therefore, a realistic project combines FAF6 with operational data from a transportation management system, warehouse system, ERP, GPS devices, carrier APIs, and delivery applications.

The project questions are:

1. Which origins, destinations, commodities, and modes carry the most freight?
2. Can distance, volume, mode, and value help estimate transportation cost or freight demand?
3. Which routes or shipment groups have similar logistics characteristics?
4. How can forecast demand and route groups support a lower-cost transportation plan?

## 3. Key Performance Indicators

| KPI | What it measures | Why it matters | Calculation from available data |
|---|---|---|---|
| On-time delivery rate | The share of shipments delivered by the promised date | Shows service reliability and helps identify delay problems | `on_time_shipments / total_shipments * 100` |
| Average transportation time | The average number of days from shipping to delivery | Helps compare service speed between routes and modes | `mean(delivery_date - ship_date)` |
| Transportation cost per shipment | The average cost of moving one shipment | Makes route and mode cost comparisons possible | `total_shipping_cost / number_of_shipments` |
| Freight volume | The amount of freight moved | Supports capacity, labor, and inventory planning | Sum of tons in FAF6, or sum of `demand_units` in the simulated sample |
| Route utilization | The amount of capacity used on a route | Helps find overloaded or underused routes | `freight_assigned / route_capacity * 100` |
| Order fulfillment rate | The share of requested units delivered | Shows whether customer demand was met | `fulfilled_units / ordered_units * 100` |

The simulated file directly supports on-time delivery, delivery time, shipping cost, demand, and a simple inventory-turnover proxy. A production system should add fulfilled quantity, route capacity, actual freight weight, and beginning and ending inventory. FAF6 supports regional freight volume, shipment value, distance-related measures, and mode analysis, but not all shipment-level service KPIs.

## 4. Public Dataset and Data Research

### 4.1 FAF6 description

FAF6 provides estimated freight flows between FAF regions. The main dimensions are origin, destination, commodity, transportation mode, year, and flow measure. Common measures include tons, shipment value, and ton-miles. The public FAF6 tool provides selections for flow type, year, origin-destination geography, commodity, mode, and distance band.

FAF6 is produced by BTS with FHWA support. It integrates information from the Commodity Flow Survey, Census Bureau international trade data, and other economic sectors such as agriculture, extraction, utilities, construction, and services. The data covers freight movement in the United States and represents domestic and international trade flows entering or leaving the country. Analysts should check the current FAF6 release documentation for the exact valid historical and forecast years before downloading a file.

FAF6 is relevant because it gives a broad view of freight movement that a small company shipment table cannot provide. It can show major corridors, high-volume regions, commodity patterns, and mode shares. These results can support freight planning, regional capacity decisions, and supply-chain strategy. FAF6 values are estimates and aggregated flows, not live observations of individual vehicles.

### 4.2 Data variables and quality

Important variables include origin and destination region, commodity code, mode, year, tons, value, ton-miles, and distance information where supplied. Origin, destination, commodity, and mode are categorical variables. Tons, value, distance, and ton-miles are numerical variables. Year is a time variable.

Potential quality issues include missing or suppressed cells, rounded estimates, inconsistent codes after joining files, duplicate rows created by an incorrect merge, and very large values caused by valid aggregation. A large flow is not automatically an error. The analyst should check the official definitions and record the FAF6 release, download date, units, filters, and transformations.

### 4.3 Supporting sources

Useful supporting public resources include the Census Bureau Commodity Flow Survey, BTS National Transportation Statistics, the BTS National Transportation Atlas Database, FHWA freight planning resources, and Census international trade data. Company data can add GPS events, warehouse scans, order quantities, carrier costs, delivery dates, fuel prices, weather, and inventory information.

## 5. Data Science Methodologies

### 5.1 Data preprocessing

Raw files will be checked for missing values, duplicate rows, invalid dates, negative distances or quantities, inconsistent mode labels, and incorrect data types. Numerical missing values can be filled with a median when that is reasonable. Categorical values can be standardized and encoded. Dates can produce month, quarter, day-of-week, and seasonal features. Outliers can be flagged with an IQR rule and investigated instead of automatically deleted.

For modeling, transportation mode and commodity can be converted into indicator columns. Numerical variables may be standardized for clustering because K-Means is affected by scale. The output of preprocessing is a clean, consistently formatted table for EDA and modeling.

### 5.2 Exploratory data analysis

EDA will summarize minimum, maximum, average, total, and spread for freight volume, distance, value, cost, and delivery time. Grouped tables will compare modes and origin-destination routes. Histograms show distributions, bar charts compare modes, scatter plots show relationships, box plots show differences and outliers, and correlation heatmaps compare numerical variables.

The expected EDA outputs are a list of high-volume routes, frequently used modes, long-distance corridors, unusually expensive records, and possible seasonal patterns. These findings guide feature selection and give managers a first view of where capacity or cost problems may exist.

### 5.3 Regression

Regression will be used to predict a numerical outcome. A practical student-level target is transportation cost using distance, shipment volume, inventory, transportation mode, and commodity. Another possible target is future route freight volume. Linear Regression is a useful baseline because its results are easy to explain. Random Forest or Gradient Boosting can be compared when relationships are not linear.

The data will be divided into training and testing sets. For a true time forecast, past records should be used for training and later records for testing rather than randomly mixing time periods. Results will be evaluated with MAE, RMSE, and R-squared. A low MAE means the average prediction error is small in the target's units. RMSE gives more weight to large errors. R-squared describes the proportion of variation explained by the model.

### 5.4 Clustering

Clustering will group similar freight movements without a target variable. Route or shipment features can include distance, volume, value, ton-miles, mode, origin, and destination. After numerical features are scaled and categorical features are encoded or summarized, K-Means can create groups such as short regional routes, high-volume routes, long-distance routes, and high-cost or high-value corridors.

The analyst will compare cluster averages and use an elbow plot or silhouette score to help choose the number of clusters. Managers can use different strategies for each group. High-volume routes may need reserved capacity, long-distance routes may need rail or intermodal comparison, and high-value freight may need extra tracking or security.

### 5.5 Optimization

Optimization will use demand forecasts and route information to select a feasible transportation plan. A simple objective is to minimize total transportation cost:

```text
minimize sum(assigned_freight * cost_per_unit)
```

The constraints may require all demand to be served, prevent a route or vehicle from exceeding capacity, limit warehouse or terminal capacity, and require deliveries to meet a service deadline. Linear Programming is suitable when decisions and costs are continuous. Integer Programming is useful for whole vehicles or yes/no facility decisions. Network Optimization is suitable when freight moves through connected origins, hubs, and destinations.

FAF6 can supply regional demand, distance, commodity, and mode information. Carrier prices, vehicle availability, delivery promises, and warehouse capacity must come from company records or documented assumptions. The optimization result should be checked by logistics staff before implementation.

## 6. End-to-End Strategic Roadmap

```mermaid
flowchart LR
    A[Problem Definition] --> B[Data Collection]
    B --> C[Data Cleaning]
    C --> D[EDA]
    D --> E[Feature Engineering]
    E --> F[Predictive Modeling]
    F --> G[Model Evaluation]
    G --> H[Optimization]
    H --> I[KPI Evaluation]
    I --> J[Business Decision-Making]
```

| Stage | What will be done | Python tools | Output and next use |
|---|---|---|---|
| Problem Definition | Define freight planning questions, targets, constraints, and KPIs | Notes, project requirements | A measurable problem and success criteria |
| Data Collection | Download FAF6 and combine it with simulated or operational shipment data | Pandas, NumPy, APIs or file imports | Raw tables with documented sources |
| Data Cleaning | Check missing values, duplicates, codes, dates, units, and invalid values | Pandas, NumPy | A valid and consistent table |
| EDA | Summarize volume, cost, distance, modes, routes, and distributions | Pandas, Matplotlib, Seaborn | Charts, tables, and initial logistics findings |
| Feature Engineering | Create route totals, value per ton, seasonal fields, lagged volume, and encoded modes | Pandas, NumPy, scikit-learn | Model-ready predictors |
| Predictive Modeling | Train a cost or demand model | scikit-learn | Predictions for unseen routes or periods |
| Model Evaluation | Compare actual and predicted values and check overfitting | MAE, RMSE, R-squared, cross-validation | A model-quality report and improvement plan |
| Optimization | Allocate freight to modes and routes under capacity and service constraints | PuLP, OR-Tools, or scipy when available | A feasible cost and capacity plan |
| KPI Evaluation | Compare the recommended plan with current performance | Pandas, charts | KPI changes and trade-offs |
| Business Decision-Making | Review recommendations and monitor actual results | Reports, dashboards, APIs | Route, mode, capacity, and inventory actions |

This roadmap is feasible for a student project because the public FAF6 data and the small simulated sample are available. A full company deployment would require additional operational data, but the project does not claim to have access to private GPS or carrier systems.

## 7. Python Code Illustrations

The repository uses project-specific column names. The names in some generic examples are mapped as follows: `Distance` to `distance_miles`, `Shipment_Weight` to `demand_units`, `Freight_Value` to `shipping_cost_usd` as the available monetary proxy, `Transportation_Cost` to `shipping_cost_usd`, and `Transport_Mode` to `transportation_mode`.

### 7.1 Loading data

```python
import pandas as pd

# The repository file is used instead of a nonexistent root logistics_data.csv.
df = pd.read_csv(
    "data/simulated_shipments.csv",
    parse_dates=["ship_date", "promised_date", "delivery_date"],
)
print(df.head())
```

This reads the simulated shipment table and parses its date fields so they can be used in calculations.

### 7.2 Data cleaning

```python
print(df.isnull().sum())
df = df.drop_duplicates()
df["demand_units"] = df["demand_units"].fillna(
    df["demand_units"].median()
)
df["ship_date"] = pd.to_datetime(df["ship_date"], errors="coerce")
df = df[df["distance_miles"] > 0]
df = df[df["demand_units"] > 0]
```

This checks missing values, removes exact duplicate rows, fills missing shipment quantities with the median, converts dates, and removes invalid distance or quantity values.

### 7.3 Exploratory analysis

```python
print(df.describe())

mode_summary = df.groupby(
    "transportation_mode"
)["demand_units"].mean()

print(mode_summary)
```

The summary gives basic distributions, while the grouped result compares average shipment volume by mode.

### 7.4 Visualization

```python
import matplotlib.pyplot as plt

plt.scatter(df["distance_miles"], df["demand_units"])
plt.xlabel("Distance (miles)")
plt.ylabel("Shipment Volume (demand units)")
plt.title("Distance vs Shipment Volume")
plt.show()
```

This plot helps show whether longer routes in the sample also tend to carry more shipment volume. The relationship should not be treated as a general conclusion from only 12 simulated records.

### 7.5 Regression

```python
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

features = ["distance_miles", "demand_units", "inventory_before"]
X = df[features]
y = df["shipping_cost_usd"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)

print("MAE:", mean_absolute_error(y_test, predictions))
print("RMSE:", mean_squared_error(y_test, predictions) ** 0.5)
print("R2:", r2_score(y_test, predictions))
```

This trains a simple cost model and measures its test error. In a larger project, transportation mode and commodity would be encoded and a time-based split would be considered.

### 7.6 Clustering

```python
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

cluster_data = df[[
    "distance_miles",
    "demand_units",
    "shipping_cost_usd",
]]
scaled_data = StandardScaler().fit_transform(cluster_data)

kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df["cluster"] = kmeans.fit_predict(scaled_data)
print(df[["distance_miles", "demand_units", "cluster"]].head())
```

Standardization prevents distance, volume, or cost from dominating only because of its numeric scale. The cluster averages can then be interpreted as different transportation patterns.

## 8. Expected Results

The project is expected to produce a clear description of the main freight routes and modes, a cleaned and documented dataset, charts for volume and cost patterns, a baseline cost or demand model, and route or shipment clusters. On the current small simulated sample, the existing scripts calculate an on-time delivery rate of 66.7%, an average delivery time of 2.42 days, and total transportation cost of $8,435. These are demonstration results, not estimates for the full U.S. freight system.

The regression model is expected to improve as more real observations are added. The current 12-record sample produces an illustrative MAE of about 127.40, RMSE of about 132.21, and negative R-squared, which shows why a larger and more representative dataset is needed. Clustering can still be used as an exploratory tool, but the groups should be checked against real logistics knowledge.

## 9. Business Impact

A completed analysis can help logistics organizations reduce transportation cost by comparing modes and identifying expensive routes. Forecasts can support capacity reservations, labor planning, and inventory positioning. Clusters can help managers create different service and inventory policies for high-volume, long-distance, and high-value freight. Optimization can allocate demand to routes and modes while respecting capacity and delivery requirements.

Managers should use the results with the KPIs rather than relying on one model score. A recommended plan is valuable only if it improves cost without damaging on-time delivery, delivery time, fulfillment, or route utilization. After implementation, actual results should be compared with the predictions and the model should be retrained when demand, costs, or network conditions change.

## 10. Conclusion

This project presents a practical data science process for freight transportation and delivery planning. FAF6 provides a reliable public view of regional freight movement, while the simulated shipment table demonstrates how shipment-level operational measures can be analyzed. Pandas and NumPy support collection and cleaning, Matplotlib and Seaborn support EDA, and scikit-learn supports regression and clustering. Optimization can use the resulting forecasts and route groups to recommend feasible transportation plans.

The expected outcome is better evidence for route selection, mode selection, capacity utilization, freight-demand forecasting, cost control, and service monitoring. The project is intentionally realistic about its limits: the simulated file is small, FAF6 is aggregated, and operational decisions require current company data. Even with these limits, the workflow shows how logistics managers can move from raw freight data to measurable and data-driven decisions.

## 11. References

1. U.S. Department of Transportation, Bureau of Transportation Statistics. [Freight Analysis Framework](https://www.bts.gov/faf).
2. Oak Ridge National Laboratory National Transportation Research Center. [Freight Analysis Framework 6 data tool](https://faf.ornl.gov/faf6/dtt_total.aspx).
3. U.S. Census Bureau. [Commodity Flow Survey](https://www.census.gov/programs-surveys/cfs.html).
4. U.S. Department of Transportation, Bureau of Transportation Statistics. [National Transportation Statistics](https://www.bts.gov/topics/national-transportation-statistics).
5. Federal Highway Administration. [Freight Management and Operations](https://ops.fhwa.dot.gov/freight/).
6. U.S. Department of Transportation, Bureau of Transportation Statistics. [National Transportation Atlas Database](https://www.bts.gov/ntad).

## Running the project examples

Install dependencies and run the examples from the project folder:

```text
python -m pip install -r requirements.txt
python src/preprocess_logistics.py
python src/eda_logistics.py
python src/train_cost_model.py
python src/cluster_logistics.py
```
