import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Cricket Analysis Dashboard",
    page_icon="🏏",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

.main {
    background-color: #f5f7fa;
}

.block-container {
    padding-top: 1.5rem;
}

h1 {
    color: #1f2937;
}

h2 {
    color: #374151;
}

.metric-card {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("cleaned file.csv")

    # Remove unnecessary index column
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    return df


df = load_data()


# --------------------------------------------------
# NAVIGATION
# --------------------------------------------------

st.markdown(
    "<h2 style='margin-bottom: 10px;'>🏏 Cricket Dashboard</h2>",
    unsafe_allow_html=True
)

selected = option_menu(
    menu_title=None,
    options=[
        "Home",
        "Player Analysis",
        "Country Insight",
        "Comparison",
        "Data Explorer",
        "Project Insight"
    ],
    icons=[
        "house",
        "person",
        "globe",
        "bar-chart",
        "table",
        "info-circle"
    ],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal"
)


# ==================================================
# HOME
# ==================================================

if selected == "Home":

    st.title("Cricket Analysis Dashboard")

    st.markdown(
        "### Explore Test Cricket Players, Countries and Performance Statistics"
    )

    st.write(
        "This dashboard provides an interactive analysis of cricket "
        "players using career statistics such as matches, runs, averages, "
        "strike rates, centuries, fifties and boundaries."
    )

    st.divider()

    # -----------------------------
    # KPI CARDS
    # -----------------------------

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "👤 Total Players",
        df["Player"].nunique()
    )

    col2.metric(
        "🌍 Countries",
        df["country"].nunique()
    )

    col3.metric(
        "🏏 Total Matches",
        f"{df['Matches'].sum():,}"
    )

    col4.metric(
        "🏃 Total Runs",
        f"{df['Runs'].sum():,}"
    )

    col5.metric(
        "💥 Total Sixes",
        f"{df['6s'].sum():,}"
    )

    st.divider()

    # -----------------------------
    # TOP PLAYERS
    # -----------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🏃 Top 10 Run Scorers")

        top_runs = df.nlargest(10, "Runs")

        fig = px.bar(
            top_runs,
            x="Runs",
            y="Player",
            orientation="h",
            title="Top Players by Runs",
            text="Runs"
        )

        fig.update_layout(
            yaxis=dict(autorange="reversed")
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        st.subheader("⭐ Top Batting Averages")

        top_avg = df.nlargest(10, "Average")

        fig = px.bar(
            top_avg,
            x="Average",
            y="Player",
            orientation="h",
            title="Top Players by Average",
            text="Average"
        )

        fig.update_layout(
            yaxis=dict(autorange="reversed")
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ==================================================
# PLAYER ANALYSIS
# ==================================================

elif selected == "Player Analysis":

    st.title(" Player Analysis")

    st.write(
        "Select a player to explore their complete career performance."
    )

    player = st.selectbox(
        "Select Player",
        sorted(df["Player"].unique())
    )

    pdata = df[df["Player"] == player].iloc[0]

    st.divider()

    # -----------------------------
    # PLAYER KPIs
    # -----------------------------

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "🏏 Matches",
        int(pdata["Matches"])
    )

    col2.metric(
        "🏃 Runs",
        f"{int(pdata['Runs']):,}"
    )

    col3.metric(
        "⭐ Average",
        pdata["Average"]
    )

    col4.metric(
        "💯 Centuries",
        int(pdata["100"])
    )

    st.divider()

    # -----------------------------
    # SECOND ROW
    # -----------------------------

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "50s",
        int(pdata["50"])
    )

    col2.metric(
        "4s",
        int(pdata["4s"])
    )

    col3.metric(
        "6s",
        int(pdata["6s"])
    )

    col4.metric(
        "Strike Rate",
        pdata["Strike_Rate"]
    )

    st.divider()

    # -----------------------------
    # PLAYER DETAILS
    # -----------------------------

    st.subheader(" Player Career Details")

    details = pd.DataFrame({
        "Metric": [
            "Country",
            "Career Period",
            "Career Duration",
            "Matches",
            "Innings",
            "Not Outs",
            "Runs",
            "Highest Score",
            "Average",
            "Balls Faced",
            "Strike Rate",
            "Centuries",
            "Fifties",
            "Ducks",
            "Fours",
            "Sixes"
        ],
        "Value": [
            pdata["country"],
            pdata["Duration(year)"],
            pdata["Duration"],
            pdata["Matches"],
            pdata["Inns"],
            pdata["NO"],
            pdata["Runs"],
            pdata["Highest_Score"],
            pdata["Average"],
            pdata["Balls_Faced"],
            pdata["Strike_Rate"],
            pdata["100"],
            pdata["50"],
            pdata["0"],
            pdata["4s"],
            pdata["6s"]
        ]
    })

    st.dataframe(
        details,
        use_container_width=True,
        hide_index=True
    )

    # -----------------------------
    # PERFORMANCE CHART
    # -----------------------------

    st.subheader(" Player Performance")

    chart_data = pd.DataFrame({
        "Metric": [
            "Matches",
            "Runs",
            "Highest Score",
            "100s",
            "50s",
            "4s",
            "6s"
        ],
        "Value": [
            pdata["Matches"],
            pdata["Runs"],
            pdata["Highest_Score"],
            pdata["100"],
            pdata["50"],
            pdata["4s"],
            pdata["6s"]
        ]
    })

    fig = px.bar(
        chart_data,
        x="Metric",
        y="Value",
        text="Value",
        title=f"{player} - Career Performance"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ==================================================
# COUNTRY INSIGHT
# ==================================================

elif selected == "Country Insight":

    st.title(" Country Insight")

    st.write(
        "Explore player performance and cricket statistics by country."
    )

    countries = sorted(df["country"].unique())

    country = st.selectbox(
        "Select Country",
        countries
    )

    cdata = df[df["country"] == country]

    st.divider()

    # -----------------------------
    # COUNTRY KPIs
    # -----------------------------

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Players",
        cdata["Player"].nunique()
    )

    col2.metric(
        "Total Runs",
        f"{cdata['Runs'].sum():,}"
    )

    col3.metric(
        "Total Matches",
        f"{cdata['Matches'].sum():,}"
    )

    col4.metric(
        "Total Centuries",
        int(cdata["100"].sum())
    )

    st.divider()

    # -----------------------------
    # COUNTRY CHARTS
    # -----------------------------

    col1, col2 = st.columns(2)

    with col1:

        fig = px.bar(
            cdata.nlargest(10, "Runs"),
            x="Runs",
            y="Player",
            orientation="h",
            title=f"Top Run Scorers - {country}",
            text="Runs"
        )

        fig.update_layout(
            yaxis=dict(autorange="reversed")
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        fig = px.scatter(
            cdata,
            x="Average",
            y="Strike_Rate",
            size="Runs",
            hover_name="Player",
            title=f"Average vs Strike Rate - {country}"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # -----------------------------
    # COUNTRY TABLE
    # -----------------------------

    st.subheader(f" Players from {country}")

    st.dataframe(
        cdata.sort_values(
            "Runs",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )


# ==================================================
# COMPARISON
# ==================================================

elif selected == "Comparison":

    st.title(" Player Comparison")

    st.write(
        "Select two players and compare their career statistics."
    )

    col1, col2 = st.columns(2)

    with col1:

        player1 = st.selectbox(
            "Select Player 1",
            sorted(df["Player"].unique()),
            key="player1"
        )

    with col2:

        player2 = st.selectbox(
            "Select Player 2",
            sorted(df["Player"].unique()),
            index=1 if len(df) > 1 else 0,
            key="player2"
        )

    p1 = df[df["Player"] == player1].iloc[0]
    p2 = df[df["Player"] == player2].iloc[0]

    st.divider()

    # -----------------------------
    # COMPARISON TABLE
    # -----------------------------

    comparison = pd.DataFrame({
        "Metric": [
            "Matches",
            "Innings",
            "Runs",
            "Highest Score",
            "Average",
            "Strike Rate",
            "100s",
            "50s",
            "4s",
            "6s"
        ],
        player1: [
            p1["Matches"],
            p1["Inns"],
            p1["Runs"],
            p1["Highest_Score"],
            p1["Average"],
            p1["Strike_Rate"],
            p1["100"],
            p1["50"],
            p1["4s"],
            p1["6s"]
        ],
        player2: [
            p2["Matches"],
            p2["Inns"],
            p2["Runs"],
            p2["Highest_Score"],
            p2["Average"],
            p2["Strike_Rate"],
            p2["100"],
            p2["50"],
            p2["4s"],
            p2["6s"]
        ]
    })

    st.dataframe(
        comparison,
        use_container_width=True,
        hide_index=True
    )

    # -----------------------------
    # BAR CHART
    # -----------------------------

    chart = pd.DataFrame({
        "Metric": [
            "Matches",
            "Runs",
            "Average",
            "Strike Rate",
            "100s",
            "50s",
            "4s",
            "6s"
        ],
        player1: [
            p1["Matches"],
            p1["Runs"],
            p1["Average"],
            p1["Strike_Rate"],
            p1["100"],
            p1["50"],
            p1["4s"],
            p1["6s"]
        ],
        player2: [
            p2["Matches"],
            p2["Runs"],
            p2["Average"],
            p2["Strike_Rate"],
            p2["100"],
            p2["50"],
            p2["4s"],
            p2["6s"]
        ]
    })

    melted = chart.melt(
        id_vars="Metric",
        var_name="Player",
        value_name="Value"
    )

    fig = px.bar(
        melted,
        x="Metric",
        y="Value",
        color="Player",
        barmode="group",
        text="Value",
        title="Player Comparison"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ==================================================
# DATA EXPLORER
# ==================================================

elif selected == "Data Explorer":

    st.title(" Data Explorer")

    st.write(
        "Use the filters below to explore the cricket dataset."
    )

    # -----------------------------
    # FILTERS
    # -----------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        selected_country = st.multiselect(
            "Filter by Country",
            sorted(df["country"].unique()),
            default=sorted(df["country"].unique())
        )

    with col2:

        min_runs = st.number_input(
            "Minimum Runs",
            min_value=0,
            max_value=int(df["Runs"].max()),
            value=0
        )

    with col3:

        min_average = st.number_input(
            "Minimum Average",
            min_value=0.0,
            max_value=float(df["Average"].max()),
            value=0.0
        )

    filtered_df = df[
        (df["country"].isin(selected_country)) &
        (df["Runs"] >= min_runs) &
        (df["Average"] >= min_average)
    ]

    st.divider()

    st.subheader(" Filtered Dataset")

    st.write(
        f"Showing **{len(filtered_df)}** players"
    )

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )

    # -----------------------------
    # DOWNLOAD
    # -----------------------------

    csv = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download Filtered Data",
        data=csv,
        file_name="filtered_cricket_data.csv",
        mime="text/csv"
    )


# ==================================================
# PROJECT INSIGHT
# ==================================================

elif selected == "Project Insight":

    st.title("📌 Project Overview")

    st.markdown("""
    ### 🏏 Cricket Analysis Dashboard

    This project focuses on analyzing cricket player career
    statistics using Python, Pandas, Plotly and Streamlit.

    ### 🎯 Project Objectives

    - Analyze player career performance
    - Compare different cricket players
    - Explore country-wise statistics
    - Identify high-performing players
    - Create interactive visualizations
    - Make cricket data easier to understand

    ### 🛠️ Technologies Used

    - Python
    - Pandas
    - Plotly
    - Streamlit
    - Streamlit Option Menu

    ### 📊 Dataset Features

    The dataset contains information about:

    - Players
    - Countries
    - Matches
    - Innings
    - Runs
    - Highest Score
    - Batting Average
    - Strike Rate
    - Centuries
    - Fifties
    - Fours
    - Sixes
    - Career Duration

    ###  Project By

    **Rabbia Mehtab**

    Data Analysis & Visualization Project
    """)

    st.success(
        "The dashboard converts raw cricket statistics into "
        "interactive and easy-to-understand insights."
    )