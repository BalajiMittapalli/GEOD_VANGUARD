
# import streamlit as st
# import pandas as pd
# import plotly.graph_objects as go
# from datetime import datetime

# # Page Config
# st.set_page_config(page_title="Equity Analytics Dashboard", layout="wide")

# st.title("📊 Equity Analytics Dashboard")
# st.write("Choose dataset and month-year range to begin analysis.")

# # Dataset Selection
# symbol = st.selectbox("Choose Stock Symbol:", ["MSFT", "NFLX"])

# # ----- Month-Year Selection -----
# st.subheader("🗓️ Select Month-Year Range")

# months = ["January","February","March","April","May","June","July",
#           "August","September","October","November","December"]

# years = list(range(2020, 2025))

# col1, col2 = st.columns(2)

# start_month = col1.selectbox("Start Month", months)
# start_year = col1.selectbox("Start Year", years)

# end_month = col2.selectbox("End Month", months, index=11)
# end_year = col2.selectbox("End Year", years, index=years.index(2024))

# # Convert selected Month-Year to datetime
# start_date = datetime(start_year, months.index(start_month) + 1, 1)
# end_date = datetime(end_year, months.index(end_month) + 1, 1)

# # Validation
# if start_date > end_date:
#     st.error("❌ Start Month-Year cannot be after End Month-Year.")
# else:
#     st.success(f"📅 Selected Range: {start_date.strftime('%b %Y')} → {end_date.strftime('%b %Y')}")

# # -------------------------------------------------------------------
# # Load Data
# # Load Data
# df = pd.read_csv(r"C:\Users\kondu\Downloads\dummy_data_MDD.csv")

# # Clean column names
# df.columns = df.columns.str.strip().str.replace("\ufeff", "")

# # Normalize column names
# df.rename(columns={
#     "Rebase to 100": "Rebase",  # ⭐ important fix
#     "Return": "Return",
#     "Peak": "Peak",
#     "Drawdown": "Drawdown",
#     "Date": "Date"
# }, inplace=True)

# # Convert Date column
# df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# # -------------------------------------------------------------------
# # Filter Based on Range
# df_filtered = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]

# # -------------------------------------------------------------------
# # Show All Charts Button
# if st.button("Show Analysis"):

#     if df_filtered.empty:
#         st.error("⚠ No data available for the selected period.")
#     else:
#         # -----------------------------------------------------------
#         # 1️⃣ MDD - Drawdown Chart
#         # -----------------------------------------------------------
#         st.subheader("📉 Maximum Drawdown (MDD)")

#         fig_dd = go.Figure()
#         fig_dd.add_trace(
#             go.Scatter(
#                 x=df_filtered["Date"],
#                 y=df_filtered["Drawdown"],
#                 fill="tozeroy",
#                 mode="lines",
#                 line=dict(color="red"),
#                 name="Drawdown"
#             )
#         )

#         fig_dd.update_layout(
#             title=f"{symbol} Drawdown Over Time",
#             xaxis_title="Date",
#             yaxis_title="Drawdown (%)",
#             height=400,
#             template="plotly_white"
#         )

#         st.plotly_chart(fig_dd, use_container_width=True)

#         # -----------------------------------------------------------
#         # 2️⃣ Rebase to 100 Chart
#         # -----------------------------------------------------------
#         st.subheader("📈 Rebase to 100 Chart")

#         fig_rebase = go.Figure()
#         fig_rebase.add_trace(
#             go.Scatter(
#                 x=df_filtered["Date"],
#                 y=df_filtered["Rebase"],
#                 mode="lines+markers",
#                 line=dict(color="blue"),
#                 name="Rebase Value"
#             )
#         )

#         fig_rebase.update_layout(
#             title="Rebase to 100 Over Time",
#             xaxis_title="Date",
#             yaxis_title="Rebase Value",
#             template="plotly_white",
#             height=400
#         )

#         st.plotly_chart(fig_rebase, use_container_width=True)

#         # -----------------------------------------------------------
#         # 3️⃣ Monthly Returns Bar Chart
#         # -----------------------------------------------------------
#         st.subheader("📉 Monthly Returns (%)")

#         fig_returns = go.Figure()
#         fig_returns.add_trace(
#             go.Bar(
#                 x=df_filtered["Date"],
#                 y=df_filtered["Return"] * 100,
#                 marker=dict(color="green"),
#                 name="Monthly Return"
#             )
#         )

#         fig_returns.update_layout(
#             title="Monthly Returns (%)",
#             xaxis_title="Date",
#             yaxis_title="Return (%)",
#             template="plotly_white",
#             height=400
#         )

#         st.plotly_chart(fig_returns, use_container_width=True)

#         # -----------------------------------------------------------
#         # 4️⃣ Peak vs Rebase Comparison Chart
#         # -----------------------------------------------------------
#         st.subheader("📊 Peak vs Rebase Comparison")

#         fig_peak = go.Figure()

#         fig_peak.add_trace(
#             go.Scatter(
#                 x=df_filtered["Date"],
#                 y=df_filtered["Peak"],
#                 mode="lines",
#                 line=dict(color="orange", width=3),
#                 name="Peak"
#             )
#         )

#         fig_peak.add_trace(
#             go.Scatter(
#                 x=df_filtered["Date"],
#                 y=df_filtered["Rebase"],
#                 mode="lines",
#                 line=dict(color="blue", width=3),
#                 name="Rebase"
#             )
#         )

#         fig_peak.update_layout(
#             title="Peak vs Rebase Over Time",
#             xaxis_title="Date",
#             yaxis_title="Value",
#             template="plotly_white",
#             height=400
#         )

#         st.plotly_chart(fig_peak, use_container_width=True)
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time

# Page Config
st.set_page_config(page_title="Equity Analytics Dashboard", layout="wide")

st.title("📊 Equity Analytics Dashboard")
st.write("Choose dataset and month-year range to begin analysis.")

# Dataset Selection
symbol = st.selectbox("Choose Stock Symbol:", ["MSFT", "NFLX"])

# ----- Month-Year Selection -----
st.subheader("🗓️ Select Month-Year Range")

months = ["January","February","March","April","May","June","July",
          "August","September","October","November","December"]

years = list(range(2020, 2025))

col1, col2 = st.columns(2)

start_month = col1.selectbox("Start Month", months, key="start_month")
start_year = col1.selectbox("Start Year", years, key="start_year")

end_month = col2.selectbox("End Month", months, index=11, key="end_month")
end_year = col2.selectbox("End Year", years, index=years.index(2024), key="end_year")

# Convert selected Month-Year to datetime
start_date = datetime(start_year, months.index(start_month) + 1, 1)
end_date = datetime(end_year, months.index(end_month) + 1, 1)

# Input validation animation
if start_date > end_date:
    st.error("❌ Start date must be BEFORE end date!")
    st.stop()
else:
    st.success(f"📅 Selected Range: {start_date.strftime('%b %Y')} → {end_date.strftime('%b %Y')}")


# ---------------- LOAD DATA ----------------
df = pd.read_csv(r"C:\Users\kondu\Downloads\dummy_data_MDD.csv")

df.columns = df.columns.str.strip().str.replace("\ufeff", "")
df.rename(columns={"Rebase to 100": "Rebase"}, inplace=True)
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Filter Based on Range
df_filtered = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]


# ---------------- BUTTON WITH ANIMATION ----------------
st.markdown("""
<style>
button[kind="primary"] {
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0% { box-shadow: 0 0 0px rgba(0,150,255,0.7); }
    50% { box-shadow: 0 0 20px rgba(0,150,255,0.7); }
    100% { box-shadow: 0 0 0px rgba(0,150,255,0.7); }
}
</style>
""", unsafe_allow_html=True)

if st.button("✨ Show Animated Analysis"):

    with st.spinner("⏳ Creating animated analytics..."):
        time.sleep(1.3)

    if df_filtered.empty:
        st.error("⚠ No data available for the selected period.")
        st.stop()

    # -----------------------------------------------------------
    # 1️⃣ MDD Chart (Animated)
    # -----------------------------------------------------------
    st.subheader("📉 Maximum Drawdown (Animated)")
    fig_dd = go.Figure()

    fig_dd.add_trace(go.Scatter(
        x=df_filtered["Date"],
        y=df_filtered["Drawdown"],
        fill="tozeroy",
        mode="lines",
        line=dict(color="red"),
        name="Drawdown"
    ))

    fig_dd.update_layout(
        title=f"{symbol} Drawdown Over Time",
        xaxis_title="Date",
        yaxis_title="Drawdown (%)",
        height=400,
        template="plotly_white",
        transition_duration=500
    )

    st.plotly_chart(fig_dd, use_container_width=True)


    # -----------------------------------------------------------
    # 2️⃣ Rebase Animation
    # -----------------------------------------------------------
    st.subheader("📈 Rebase to 100 (Animated)")

    fig_rebase = go.Figure(go.Scatter(
        x=df_filtered["Date"],
        y=df_filtered["Rebase"],
        mode="lines+markers",
        line=dict(color="blue"),
    ))

    fig_rebase.update_layout(
        title="Rebase to 100 Over Time",
        transition_duration=600,
        height=400,
        template="plotly_white"
    )

    st.plotly_chart(fig_rebase, use_container_width=True)


    # -----------------------------------------------------------
    # 3️⃣ Monthly Returns (Animated Bars)
    # -----------------------------------------------------------
    st.subheader("📉 Monthly Returns (Animated Bar Chart)")

    fig_returns = go.Figure(go.Bar(
        x=df_filtered["Date"],
        y=df_filtered["Return"] * 100,
        marker=dict(color="limegreen")
    ))

    fig_returns.update_layout(
        title="Monthly Returns (%)",
        xaxis_title="Date",
        yaxis_title="Return (%)",
        transition_duration=600,
        height=400,
        template="plotly_white"
    )

    st.plotly_chart(fig_returns, use_container_width=True)


    # -----------------------------------------------------------
    # 4️⃣ Peak vs Rebase (Animated Dual Line)
    # -----------------------------------------------------------
    st.subheader("📊 Peak vs Rebase (Animated)")

    fig_peak = go.Figure()

    fig_peak.add_trace(go.Scatter(
        x=df_filtered["Date"],
        y=df_filtered["Peak"],
        mode="lines",
        name="Peak",
        line=dict(color="orange", width=3)
    ))

    fig_peak.add_trace(go.Scatter(
        x=df_filtered["Date"],
        y=df_filtered["Rebase"],
        mode="lines",
        name="Rebase",
        line=dict(color="blue", width=3)
    ))

    fig_peak.update_layout(
        title="Peak vs Rebase Over Time",
        transition_duration=600,
        height=400,
        template="plotly_white"
    )

    st.plotly_chart(fig_peak, use_container_width=True)
