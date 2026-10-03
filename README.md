# Telangana PDS Analytics

## Multi-Dimensional Shop Performance Clustering and Anomaly Profiling

This project analyzes Telangana Fair Price Shops (FPS) using transaction, card-status, and shop-location data.

The objective is to identify different shop behavior patterns through clustering, detect unusual shops using anomaly detection, and visualize FPS shop performance geographically through an interactive Streamlit dashboard.

---

## Project Objectives

- Integrate Telangana PDS transaction, card-status, and location data.
- Perform exploratory data analysis and feature engineering.
- Create shop-level behavioral features.
- Apply PCA for dimensionality reduction.
- Apply K-Means clustering to identify shop behavior groups.
- Apply DBSCAN to identify anomaly candidates.
- Analyze cluster characteristics and shop performance.
- Visualize FPS shops geographically.
- Provide an interactive Streamlit dashboard for analysis and filtering.

---

## Datasets

Three types of Telangana PDS datasets were integrated:

### 1. Transaction Data

Contains monthly transaction information for FPS shops, including:

- District code
- Shop number
- Month and year
- Number of registered cards
- Number of transactions
- Commodity quantities
- Transaction-related measures

### 2. Card Status Data

Contains monthly card and beneficiary information, including:

- Total ration cards
- Total units
- NFSA card information
- State card information
- Shop number
- Month and year

### 3. FPS Location Data

Contains shop-level geographical information, including:

- District code
- Shop number
- Address
- Latitude
- Longitude
- FPS status
- FPS type

---

## Data Integration

The monthly Card Status and Transaction datasets were first integrated using:

- `distCode`
- `shopNo`
- `month`
- `year`

The FPS location information was then added using:

- `distCode`
- `shopNo`

This produced an integrated shop-level dataset suitable for behavioral analysis.

---

## Feature Engineering

Several behavioral features were created from the integrated data.

### Utilization Ratio

```text
utilization_ratio =
noOfTrans / noOfRcs
