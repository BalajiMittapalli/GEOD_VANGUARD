import streamlit as st

# Page Config
st.set_page_config(page_title="Equity Analytics Dashboard", layout="wide")

st.title("📊 Equity Analytics Dashboard")
st.write("Choose dataset and month-year range to begin analysis.")

# Dataset Selection
symbol = st.selectbox("Choose Stock Symbol:", ["MSFT", "NFLX"])

# ----- Month-Year Selection -----
st.subheader("🗓️ Select Month-Year Range")

months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

years = list(range(2020, 2025))  # 2020 → 2024

col1, col2 = st.columns(2)

# Start Month-Year Picker
start_month = col1.selectbox("Start Month", months, index=0)
start_year = col1.selectbox("Start Year", years, index=0)

# End Month-Year Picker
end_month = col2.selectbox("End Month", months, index=11)
end_year = col2.selectbox("End Year", years, index=len(years)-1)

# Convert to month-year string or tuple
start_period = f"{start_month} {start_year}"
end_period = f"{end_month} {end_year}"

# Validation
if (start_year > end_year) or (start_year == end_year and months.index(start_month) > months.index(end_month)):
    st.error("❌ Start Month-Year cannot be after End Month-Year.")
else:
    st.success(f"📅 Selected Range: {start_period} → {end_period}")
