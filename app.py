# ============================================================
# TELANGANA PDS ANALYTICS DASHBOARD
# ============================================================

import streamlit as st
import pandas as pd
import folium

from folium.plugins import MarkerCluster
from streamlit_folium import st_folium


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Telangana PDS Analytics",
    page_icon="🏪",
    layout="wide"
)


# ============================================================
# LOAD MAIN DATA
# ============================================================

@st.cache_data
def load_data():

    data = pd.read_csv(
        "final_shop_data.csv"
    )

    return data


df = load_data()


# ============================================================
# TITLE
# ============================================================

st.title("🏪 Telangana PDS Analytics")

st.subheader(
    "Multi-Dimensional Shop Performance "
    "Clustering and Anomaly Profiling"
)

st.markdown(
    """
    This dashboard analyzes Telangana Fair Price Shops (FPS)
    using transaction, card-status, and location data.

    **Methods used:**
    - PCA for dimensionality reduction
    - K-Means for behavioral clustering
    - DBSCAN for anomaly identification
    - Geospatial visualization for FPS locations
    """
)


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.header("🔎 Dashboard Filters")


# ------------------------------------------------------------
# K-MEANS CLUSTER FILTER
# ------------------------------------------------------------

cluster_options = sorted(
    df["cluster"].dropna().unique()
)

selected_clusters = st.sidebar.multiselect(
    "Select K-Means Cluster",
    options=cluster_options,
    default=cluster_options,
    key="cluster_filter"
)


# ------------------------------------------------------------
# DISTRICT FILTER
# ------------------------------------------------------------

district_options = sorted(
    df["distCode"].dropna().unique()
)

selected_districts = st.sidebar.multiselect(
    "Select District",
    options=district_options,
    default=district_options,
    key="district_filter"
)


# ------------------------------------------------------------
# SHOP TYPE FILTER
# ------------------------------------------------------------

anomaly_option = st.sidebar.selectbox(
    "Shop Type",
    [
        "All Shops",
        "Normal Shops",
        "Anomaly Candidates"
    ],
    key="shop_type_filter"
)


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df[
    df["cluster"].isin(selected_clusters)
    & df["distCode"].isin(selected_districts)
].copy()


if anomaly_option == "Normal Shops":

    filtered_df = filtered_df[
        filtered_df["is_anomaly"] == False
    ]


elif anomaly_option == "Anomaly Candidates":

    filtered_df = filtered_df[
        filtered_df["is_anomaly"] == True
    ]


# ============================================================
# DASHBOARD SUMMARY
# ============================================================

st.success(
    f"Displaying {len(filtered_df):,} shops"
)


# ============================================================
# KEY METRICS
# ============================================================

total_shops = len(filtered_df)

total_clusters = filtered_df["cluster"].nunique()

total_anomalies = filtered_df["is_anomaly"].sum()


if total_shops > 0:

    anomaly_percentage = (
        total_anomalies
        / total_shops
        * 100
    )

else:

    anomaly_percentage = 0


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Filtered FPS Shops",
        f"{total_shops:,}"
    )


with col2:

    st.metric(
        "K-Means Clusters",
        total_clusters
    )


with col3:

    st.metric(
        "Anomaly Candidates",
        f"{total_anomalies:,}"
    )


with col4:

    st.metric(
        "Anomaly %",
        f"{anomaly_percentage:.2f}%"
    )


# ============================================================
# SHOP SEARCH & CLUSTER COMPARISON
# ============================================================

st.header("🔎 Shop Search & Cluster Comparison")

st.write(
    "Enter a shop number to compare its performance "
    "with the average performance of its K-Means cluster."
)


shop_search = st.text_input(
    "Enter Shop Number",
    placeholder="Example: 1901001",
    key="shop_search"
)


if shop_search.strip() != "":

    try:

        search_shop_no = int(
            shop_search.strip()
        )

        # Search in complete dataset
        shop_result = df[
            df["shopNo"] == search_shop_no
        ].copy()


        if len(shop_result) == 0:

            st.warning(
                f"Shop number {search_shop_no} "
                "was not found."
            )

        else:

            shop_row = shop_result.iloc[0]

            shop_cluster = int(
                shop_row["cluster"]
            )


            # ------------------------------------------------
            # Cluster average from complete dataset
            # ------------------------------------------------

            cluster_data = df[
                df["cluster"] == shop_cluster
            ].copy()


            cluster_avg_transactions = (
                cluster_data[
                    "avg_transactions"
                ].mean()
            )


            cluster_avg_units = (
                cluster_data[
                    "avg_total_units"
                ].mean()
            )


            cluster_avg_commodity = (
                cluster_data[
                    "avg_commodity_quantity"
                ].mean()
            )


            cluster_avg_transaction_volatility = (
                cluster_data[
                    "transaction_volatility"
                ].mean()
            )


            cluster_avg_commodity_volatility = (
                cluster_data[
                    "commodity_volatility"
                ].mean()
            )


            # =================================================
            # SHOP INFORMATION
            # =================================================

            st.subheader(
                f"🏪 Shop {search_shop_no} "
                "Performance Profile"
            )


            col1, col2, col3, col4 = st.columns(4)


            with col1:

                st.metric(
                    "K-Means Cluster",
                    shop_cluster
                )


            with col2:

                anomaly_status = (
                    "Yes"
                    if bool(shop_row["is_anomaly"])
                    else "No"
                )

                st.metric(
                    "Anomaly",
                    anomaly_status
                )


            with col3:

                st.metric(
                    "District",
                    int(shop_row["distCode"])
                )


            with col4:

                st.metric(
                    "DBSCAN Cluster",
                    int(shop_row["dbscan_cluster"])
                )


            # =================================================
            # PERFORMANCE COMPARISON
            # =================================================

            st.subheader(
                "📊 Shop Performance vs Cluster Average"
            )


            comparison_data = pd.DataFrame({

                "Metric": [

                    "Average Transactions",

                    "Average Total Units",

                    "Average Commodity Quantity",

                    "Transaction Volatility",

                    "Commodity Volatility"

                ],

                "Shop Value": [

                    shop_row[
                        "avg_transactions"
                    ],

                    shop_row[
                        "avg_total_units"
                    ],

                    shop_row[
                        "avg_commodity_quantity"
                    ],

                    shop_row[
                        "transaction_volatility"
                    ],

                    shop_row[
                        "commodity_volatility"
                    ]

                ],

                "Cluster Average": [

                    cluster_avg_transactions,

                    cluster_avg_units,

                    cluster_avg_commodity,

                    cluster_avg_transaction_volatility,

                    cluster_avg_commodity_volatility

                ]

            })


            comparison_data["Difference"] = (
                comparison_data["Shop Value"]
                - comparison_data["Cluster Average"]
            )


            st.dataframe(
                comparison_data.style.format({
                    "Shop Value": "{:.2f}",
                    "Cluster Average": "{:.2f}",
                    "Difference": "{:.2f}"
                }),
                use_container_width=True
            )


            # =================================================
            # SHOP INTERPRETATION
            # =================================================

            st.subheader(
                "📌 Shop Interpretation"
            )


            transaction_difference = (
                shop_row["avg_transactions"]
                - cluster_avg_transactions
            )


            commodity_difference = (
                shop_row["avg_commodity_quantity"]
                - cluster_avg_commodity
            )


            if transaction_difference > 0:

                st.write(
                    f"• This shop has higher average "
                    f"transactions than the average of "
                    f"Cluster {shop_cluster}."
                )

            else:

                st.write(
                    f"• This shop has lower average "
                    f"transactions than the average of "
                    f"Cluster {shop_cluster}."
                )


            if commodity_difference > 0:

                st.write(
                    f"• Commodity quantity is higher "
                    f"than the Cluster {shop_cluster} "
                    f"average."
                )

            else:

                st.write(
                    f"• Commodity quantity is lower "
                    f"than the Cluster {shop_cluster} "
                    f"average."
                )


            if bool(shop_row["is_anomaly"]):

                st.error(
                    "⚠️ This shop has been identified "
                    "as a DBSCAN anomaly candidate."
                )

            else:

                st.success(
                    "✅ This shop has not been identified "
                    "as a DBSCAN anomaly candidate."
                )


    except ValueError:

        st.warning(
            "Please enter a valid numeric shop number."
        )


# ============================================================
# CLUSTER DISTRIBUTION
# ============================================================

st.header("📊 K-Means Cluster Distribution")


cluster_counts = (
    filtered_df["cluster"]
    .value_counts()
    .sort_index()
)


st.bar_chart(
    cluster_counts
)


# ============================================================
# CLUSTER PROFILE ANALYSIS
# ============================================================

st.header("📋 Cluster Profile Analysis")


cluster_profile = (
    filtered_df
    .groupby("cluster")
    .agg(
        Shop_Count=("shopNo", "count"),
        Avg_Transactions=(
            "avg_transactions",
            "mean"
        ),
        Avg_Total_Units=(
            "avg_total_units",
            "mean"
        ),
        Avg_Commodity_Quantity=(
            "avg_commodity_quantity",
            "mean"
        ),
        Transaction_Volatility=(
            "transaction_volatility",
            "mean"
        ),
        Commodity_Volatility=(
            "commodity_volatility",
            "mean"
        ),
        Avg_Transaction_Intensity=(
            "avg_transaction_intensity",
            "mean"
        )
    )
    .round(2)
)


st.dataframe(
    cluster_profile,
    use_container_width=True
)


# ============================================================
# CLUSTER ACTIVITY COMPARISON
# ============================================================

st.header("📊 Average Shop Activity by Cluster")


activity_chart = (
    filtered_df
    .groupby("cluster")[
        [
            "avg_transactions",
            "avg_total_units",
            "avg_commodity_quantity"
        ]
    ]
    .mean()
)


st.bar_chart(
    activity_chart
)


# ============================================================
# VOLATILITY COMPARISON
# ============================================================

st.header("📈 Shop Volatility by Cluster")


volatility_chart = (
    filtered_df
    .groupby("cluster")[
        [
            "transaction_volatility",
            "commodity_volatility"
        ]
    ]
    .mean()
)


st.bar_chart(
    volatility_chart
)


# ============================================================
# SHOP DATA
# ============================================================

st.header("🏪 Shop Data")


display_columns = [

    "distCode",

    "shopNo",

    "cluster",

    "dbscan_cluster",

    "is_anomaly",

    "avg_transactions",

    "avg_total_units",

    "avg_commodity_quantity",

    "transaction_volatility",

    "commodity_volatility"

]


st.dataframe(
    filtered_df[display_columns],
    use_container_width=True,
    height=500
)


# ============================================================
# INTERACTIVE FPS SHOP MAP
# ============================================================

st.header(
    "🗺️ FPS Shop Cluster & Anomaly Map"
)


# ============================================================
# LOAD LOCATION DATA
# ============================================================

@st.cache_data
def load_location_data():

    location_data = pd.read_csv(
        "location/shop-status-details_6_2025.csv"
    )

    return location_data


location_data = load_location_data()


# ============================================================
# SELECT LOCATION COLUMNS
# ============================================================

location_data = location_data[
    [
        "distCode",
        "shopNo",
        "address",
        "longitude",
        "latitude",
        "fpsStatus",
        "fpsType"
    ]
].copy()


# ============================================================
# MERGE SHOP + LOCATION DATA
# ============================================================

map_data = pd.merge(
    filtered_df,
    location_data,
    on=[
        "distCode",
        "shopNo"
    ],
    how="left"
)


# ============================================================
# KEEP VALID COORDINATES
# ============================================================

map_data = map_data[
    map_data["latitude"].notna()
    & map_data["longitude"].notna()
    & (map_data["latitude"] != 0)
    & (map_data["longitude"] != 0)
].copy()


st.write(
    f"Total shops with valid coordinates: "
    f"{len(map_data):,}"
)


# ============================================================
# OPTIMIZE MAP DATA
# ============================================================

# Keep all anomaly shops
anomaly_map_data = map_data[
    map_data["is_anomaly"] == True
].copy()


# Keep normal shops
normal_map_data = map_data[
    map_data["is_anomaly"] == False
].copy()


normal_sample_size = min(
    3000,
    len(normal_map_data)
)


if normal_sample_size > 0:

    normal_map_data = normal_map_data.sample(
        n=normal_sample_size,
        random_state=42
    )


# Combine anomaly shops + normal sample

display_map_data = pd.concat(
    [
        anomaly_map_data,
        normal_map_data
    ],
    ignore_index=True
)


st.write(
    f"Displaying {len(display_map_data):,} shops "
    f"on the map "
    f"({len(anomaly_map_data):,} anomalies + "
    f"{len(normal_map_data):,} normal shops)."
)


# ============================================================
# CREATE MAP
# ============================================================

if len(display_map_data) > 0:

    map_center = [

        display_map_data[
            "latitude"
        ].mean(),

        display_map_data[
            "longitude"
        ].mean()

    ]


    dashboard_map = folium.Map(

        location=map_center,

        zoom_start=7,

        tiles="OpenStreetMap"

    )


    # ========================================================
    # MARKER CLUSTER
    # ========================================================

    marker_cluster = MarkerCluster(
        name="FPS Shops"
    )


    marker_cluster.add_to(
        dashboard_map
    )


    # ========================================================
    # K-MEANS CLUSTER COLORS
    # ========================================================

    cluster_colors = {

        0: "blue",

        1: "orange",

        2: "green",

        3: "purple"

    }


    # ========================================================
    # ADD MAP MARKERS
    # ========================================================

    for _, row in display_map_data.iterrows():

        if row["is_anomaly"]:

            marker_color = "red"

        else:

            marker_color = cluster_colors.get(

                int(row["cluster"]),

                "gray"

            )


        popup_text = f"""

        <b>FPS Shop:</b>
        {row['shopNo']}<br>

        <b>District Code:</b>
        {row['distCode']}<br>

        <b>K-Means Cluster:</b>
        {row['cluster']}<br>

        <b>DBSCAN Cluster:</b>
        {row['dbscan_cluster']}<br>

        <b>Anomaly:</b>
        {row['is_anomaly']}<br>

        <b>Average Transactions:</b>
        {row['avg_transactions']:.2f}<br>

        <b>Average Total Units:</b>
        {row['avg_total_units']:.2f}<br>

        <b>Average Commodity Quantity:</b>
        {row['avg_commodity_quantity']:.2f}<br>

        <b>Transaction Volatility:</b>
        {row['transaction_volatility']:.2f}<br>

        <b>Commodity Volatility:</b>
        {row['commodity_volatility']:.2f}<br>

        <b>FPS Status:</b>
        {row['fpsStatus']}<br>

        <b>FPS Type:</b>
        {row['fpsType']}

        """


        folium.CircleMarker(

            location=[

                row["latitude"],

                row["longitude"]

            ],

            radius=(
                5
                if row["is_anomaly"]
                else 3
            ),

            color=marker_color,

            fill=True,

            fill_color=marker_color,

            fill_opacity=0.75,

            popup=folium.Popup(

                popup_text,

                max_width=300

            )

        ).add_to(

            marker_cluster

        )


    # ========================================================
    # MAP LEGEND
    # ========================================================

    legend_html = """

    <div style="

        position: fixed;

        bottom: 30px;

        left: 30px;

        width: 180px;

        background-color: white;

        border: 2px solid grey;

        z-index: 9999;

        padding: 10px;

        font-size: 13px;

        ">

        <b>FPS Map Legend</b>
        <br><br>

        <span style="color:blue;">
        ●
        </span>
        Cluster 0
        <br>

        <span style="color:orange;">
        ●
        </span>
        Cluster 1
        <br>

        <span style="color:green;">
        ●
        </span>
        Cluster 2
        <br>

        <span style="color:purple;">
        ●
        </span>
        Cluster 3
        <br>

        <span style="color:red;">
        ●
        </span>
        Anomaly

    </div>

    """


    dashboard_map.get_root().html.add_child(

        folium.Element(
            legend_html
        )

    )


    # ========================================================
    # DISPLAY MAP
    # ========================================================

    st_folium(

        dashboard_map,

        height=700,

        width=None,

        returned_objects=[]

    )


else:

    st.warning(

        "No shops with valid coordinates "
        "are available for the selected filters."

    )