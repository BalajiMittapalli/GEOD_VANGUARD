
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
import requests
import glob
import time
import glob

# Page Config
st.set_page_config(page_title="Equity Analytics Dashboard", layout="wide")

st.title("📊 Equity Analytics Dashboard")
st.write("Choose dataset and month-year range to begin analysis.")

# Dataset Selection
symbol = st.selectbox("Choose Stock Symbol:", ["MSFT", "NFLX", "NVDA"])

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

# Validation
if start_date > end_date:
    st.error("❌ Start Month-Year cannot be after End Month-Year.")
else:
    st.success(f"📅 Selected Range: {start_date.strftime('%b %Y')} → {end_date.strftime('%b %Y')}")

# -------------------------------------------------------------------
# API call function
@st.cache_data(ttl=300)
def call_analytics_api(ticker, start_date, end_date):
    """Call the analytics API to generate enhanced data"""
    try:
        response = requests.post(
            "http://localhost:8000/analytics/run",
            json={
                "ticker": ticker,
                "start_date": start_date,
                "end_date": end_date
            },
            timeout=60
        )
        if response.status_code == 200:
            return True
        else:
            st.error(f"API Error: {response.status_code}")
            return False
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return False

# Load Enhanced Data
def load_enhanced_csv(ticker, start_date, end_date):
    """Load the most recent enhanced CSV file, generate if not exists"""
    try:
        csv_files = glob.glob(f"{ticker}_enhanced_analytics_*.csv")
        if not csv_files:
            # Generate enhanced data using API
            st.info(f"📊 Generating enhanced analytics for {ticker}...")
            with st.spinner("Running financial calculations..."):
                success = call_analytics_api(ticker, start_date, end_date)
            
            if success:
                st.success(f"✅ Enhanced analytics generated for {ticker}")
                # Try to find the file again
                csv_files = glob.glob(f"{ticker}_enhanced_analytics_*.csv")
            else:
                st.error("❌ Failed to generate analytics")
                return None
        
        if csv_files:
            latest_file = max(csv_files)
            df = pd.read_csv(latest_file)
            df['datetime'] = pd.to_datetime(df['datetime'])
            
            # Map to expected column names for compatibility
            df = df.rename(columns={
                'datetime': 'Date',
                'rebase_100': 'Rebase', 
                'monthly_return': 'Return',
                'rolling_max': 'Peak',
                'drawdown': 'Drawdown'
            })
            
            return df
        else:
            st.error(f"❌ Could not generate or find enhanced data for {ticker}")
            return None
            
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

# Load the enhanced data (this will auto-generate if missing)
df = load_enhanced_csv(symbol, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))


# -------------------------------------------------------------------
# Filter Based on Range
if df is not None:
    df_filtered = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]
else:
    df_filtered = None

# -------------------------------------------------------------------
# Show All Charts Button - ORIGINAL VISUALIZATIONS
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

    if df_filtered is None or df_filtered.empty:
        st.error("⚠ No enhanced data available for the selected period.")
        st.info("💡 Make sure to run the API first to generate enhanced CSV files.")
    else:
        # -----------------------------------------------------------
        # 1️⃣ MDD - Drawdown Chart (Original)
        # -----------------------------------------------------------
        st.subheader("📉 Maximum Drawdown (MDD)")

        fig_dd = go.Figure()
        fig_dd.add_trace(
            go.Scatter(
                x=df_filtered["Date"],
                y=df_filtered["Drawdown"] * 100,  # Convert to percentage for display
                fill="tozeroy",
                mode="lines",
                line=dict(color="red"),
                name="Drawdown"
            )
        )

        fig_dd.update_layout(
            title=f"{symbol} Drawdown Over Time",
            xaxis_title="Date",
            yaxis_title="Drawdown (%)",
            height=400,
            template="plotly_white"
        )

        st.plotly_chart(fig_dd, use_container_width=True)

        # -----------------------------------------------------------
        # 2️⃣ Rebase to 100 Chart (Original)
        # -----------------------------------------------------------
        st.subheader("📈 Rebase to 100 Chart")

        fig_rebase = go.Figure()
        fig_rebase.add_trace(
            go.Scatter(
                x=df_filtered["Date"],
                y=df_filtered["Rebase"],
                mode="lines+markers",
                line=dict(color="blue"),
                name="Rebase Value"
            )
        )

        fig_rebase.update_layout(
            title="Rebase to 100 Over Time",
            xaxis_title="Date",
            yaxis_title="Rebase Value",
            template="plotly_white",
            height=400
        )

        st.plotly_chart(fig_rebase, use_container_width=True)

        # -----------------------------------------------------------
        # 3️⃣ Monthly Returns Bar Chart (Original)
        # -----------------------------------------------------------
        st.subheader("📉 Monthly Returns (%)")

        # Remove NaN values from returns
        valid_returns = df_filtered["Return"].dropna()
        valid_dates = df_filtered["Date"][df_filtered["Return"].notna()]

        fig_returns = go.Figure()
        
        # Color bars based on positive/negative returns
        colors = ["green" if x >= 0 else "red" for x in valid_returns]
        
        fig_returns.add_trace(
            go.Bar(
                x=valid_dates,
                y=valid_returns * 100,  # Convert to percentage
                marker=dict(color=colors),
                name="Monthly Return"
            )
        )

        fig_returns.update_layout(
            title="Monthly Returns (%)",
            xaxis_title="Date",
            yaxis_title="Return (%)",
            template="plotly_white",
            height=400
        )

        st.plotly_chart(fig_returns, use_container_width=True)

        # -----------------------------------------------------------
        # 4️⃣ Peak vs Rebase Comparison Chart (Original)
        # -----------------------------------------------------------
        st.subheader("📊 Peak vs Rebase Comparison")

        fig_peak = go.Figure()

        fig_peak.add_trace(
            go.Scatter(
                x=df_filtered["Date"],
                y=df_filtered["Peak"],
                mode="lines",
                line=dict(color="orange", width=3),
                name="Peak"
            )
        )

        fig_peak.add_trace(
            go.Scatter(
                x=df_filtered["Date"],
                y=df_filtered["Rebase"],
                mode="lines",
                line=dict(color="blue", width=3),
                name="Rebase"
            )
        )

        fig_peak.update_layout(
            title="Peak vs Rebase Over Time",
            xaxis_title="Date",
            yaxis_title="Value",
            template="plotly_white",
            height=400
        )

        st.plotly_chart(fig_peak, use_container_width=True)
        
        # -----------------------------------------------------------
        # 5️⃣ Key Metrics Summary
        # -----------------------------------------------------------
        if 'beta' in df_filtered.columns and 'unlevered_beta' in df_filtered.columns:
            st.subheader("📊 Financial Metrics Summary")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                max_dd = df_filtered["Drawdown"].min() * 100
                st.metric("Max Drawdown", f"{abs(max_dd):.6f}%")
            
            with col2:
                beta_val = df_filtered["beta"].iloc[0] if not df_filtered["beta"].isna().all() else 0
                st.metric("Beta", f"{beta_val:.9f}")
            
            with col3:
                unbeta_val = df_filtered["unlevered_beta"].iloc[0] if not df_filtered["unlevered_beta"].isna().all() else 0
                st.metric("Unlevered Beta", f"{unbeta_val:.9f}")
            
            with col4:
                avg_return = df_filtered["Return"].mean() * 100 if not df_filtered["Return"].isna().all() else 0
                st.metric("Avg Monthly Return", f"{avg_return:.2f}%")
        
        # -----------------------------------------------------------
        # 6️⃣ WACC Optimization Visualization
        # -----------------------------------------------------------
        st.subheader("💰 WACC vs Debt Ratio Analysis")
        
        # Make API call to get WACC curve data
        with st.spinner("📊 Calculating WACC optimization..."):
            try:
                response = requests.post(
                    "http://localhost:8000/analytics/run",
                    json={
                        "ticker": symbol,
                        "start_date": start_date.strftime('%Y-%m-%d'),
                        "end_date": end_date.strftime('%Y-%m-%d')
                    },
                    timeout=60
                )
                
                if response.status_code == 200:
                    api_data = response.json()
                    wacc_curve = api_data['wacc_curve']
                    
                    # Extract data for visualization
                    debt_ratios = [point['debt_ratio'] * 100 for point in wacc_curve]  # Convert to %
                    wacc_values = [point['wacc']  for point in wacc_curve]  # Convert to % for Y-axis
                    
                    # Find minimum WACC point
                    min_wacc_idx = wacc_values.index(min(wacc_values))
                    optimal_debt = debt_ratios[min_wacc_idx]
                    optimal_wacc = wacc_values[min_wacc_idx]
                    
                    # Create WACC curve plot
                    fig_wacc = go.Figure()
                    
                    # Main curve
                    fig_wacc.add_trace(go.Scatter(
                        x=debt_ratios,
                        y=wacc_values,
                        mode='lines+markers',
                        line=dict(color='purple', width=3),
                        marker=dict(size=4, color='purple'),
                        name='WACC Curve',
                        hovertemplate='<b>Debt:</b> %{x:.1f}%<br><b>WACC:</b> %{y:.2f}%<extra></extra>'
                    ))
                    
                    # Highlight optimal point
                    fig_wacc.add_trace(go.Scatter(
                        x=[optimal_debt],
                        y=[optimal_wacc],
                        mode='markers',
                        marker=dict(color='red', size=15, symbol='star', line=dict(color='darkred', width=2)),
                        name=f'Minimum WACC at {optimal_debt:.1f}% Debt',
                        hovertemplate='<b>OPTIMAL POINT</b><br><b>Debt:</b> %{x:.1f}%<br><b>Min WACC:</b> %{y:.2f}%<extra></extra>'
                    ))
                    
                    # Add annotation pointing to minimum
                    fig_wacc.add_annotation(
                        x=optimal_debt,
                        y=optimal_wacc,
                        text=f"🎯 Minimum WACC<br>Debt: {optimal_debt:.1f}%<br>WACC: {optimal_wacc:.2f}%",
                        showarrow=True,
                        arrowhead=2,
                        arrowcolor="red",
                        arrowwidth=2,
                        bgcolor="rgba(255,255,255,0.9)",
                        bordercolor="red",
                        borderwidth=2,
                        font=dict(size=12, color="darkred")
                    )
                    
                    fig_wacc.update_layout(
                        title=f"{symbol} WACC Optimization Curve (0% - 99% Debt Range)",
                        xaxis_title="Debt Ratio (%)",
                        yaxis_title="WACC (%)",
                        height=500,
                        template="plotly_white",
                        showlegend=True,
                        xaxis=dict(
                            dtick=4,  # Scale of 4 for debt %
                            tick0=1,  # Start from 1%
                            tickmode='linear',
                            range=[1, 99]  # Start from 1% instead of 0%
                        ),
                        yaxis=dict(
                            dtick=2.0,  # Scale of 2.000000 for WACC %
                            tick0=0.00,  # Start from 0.00%
                            tickmode='linear',
                            tickformat='.2f'  # Show 2 decimal places
                        )
                    )
                    
                    st.plotly_chart(fig_wacc, use_container_width=True)
                    
                    # -----------------------------------------------------------
                    # 7️⃣ Enhanced Summary Table
                    # -----------------------------------------------------------
                    st.subheader("📋 Complete Financial Metrics Summary Table")
                    
                    # Create comprehensive summary data
                    summary_data = {
                        "Financial Metric": [
                            f"{symbol} Beta (Levered)",
                            f"{symbol} Beta (Unlevered)", 
                            "Optimal WACC (%)",
                            "Debt % at Optimal WACC",
                            "Equity % at Optimal WACC",
                            "Maximum Drawdown (%)"
                        ],
                        "Value": [
                            f"{api_data['beta']:.9f}",
                            f"{api_data['unlevered_beta']:.9f}",
                            f"{optimal_wacc:.2f}%",
                            f"{optimal_debt:.2f}%",
                            f"{100-optimal_debt:.2f}%",
                            f"{api_data['max_drawdown']:.6f}%"
                        ]
                    }
                    
                    # Display as styled table
                    summary_df = pd.DataFrame(summary_data)
                    
                    # Create attractive table layout
                    col1, col2, col3 = st.columns([1, 3, 1])
                    
                    with col2:
                        st.dataframe(
                            summary_df,
                            use_container_width=True,
                            hide_index=True,
                            column_config={
                                "Financial Metric": st.column_config.TextColumn(
                                    "📊 Financial Metric", 
                                    width="large"
                                ),
                                "Value": st.column_config.TextColumn(
                                    "📈 Value", 
                                    width="medium"
                                )
                            }
                        )
                    
                    # Highlight optimal capital structure in success box
                    st.success(
                        f"🎯 **Optimal Capital Structure for {symbol}:** "
                        f"{optimal_debt:.2f}% Debt + {100-optimal_debt:.2f}% Equity "
                        f"→ **Minimum WACC: {optimal_wacc:.2f}%**"
                    )
                    
                else:
                    st.error(f"❌ API Error: {response.status_code}")
                    
            except Exception as e:
                st.error(f"❌ Error calculating WACC: {str(e)}")
