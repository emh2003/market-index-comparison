import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import date

# Title and description
st.set_page_config(page_title="Market Index Comparison", layout="wide")
st.title("Market Index Comparison Tool")
st.markdown("""
Select one or more market indices and a date range to view a normalized comparison of performance over time.
""")

# Index options (Yahoo Finance symbols)
INDEX_TICKERS = {
    'S&P 500': '^GSPC',
    'NASDAQ': '^IXIC',
    'Dow Jones': '^DJI',
    'Russell 2000': '^RUT',
    'NYSE Composite': '^NYA'
}

# Sidebar for user inputs
st.sidebar.header("User Selections")
selected_indices = st.sidebar.multiselect("Choose indices:", list(INDEX_TICKERS.keys()), default=['S&P 500', 'NASDAQ'])
start_date = st.sidebar.date_input("Start Date", value=date(2022, 1, 1))
end_date = st.sidebar.date_input("End Date", value=date.today())

@st.cache_data
def fetch_data(ticker, start, end):
    df = yf.download(ticker, start=start, end=end)

    if df.empty:
        st.warning(f"No data returned for {ticker}.")
        return pd.Series(dtype=float)

    if isinstance(df.columns, pd.MultiIndex):
        try:
            df = df[('Close', ticker)]
        except KeyError:
            st.error(f"Multi-index 'Close' not found for {ticker}. Columns: {df.columns.tolist()}")
            return pd.Series(dtype=float)
    else:
        if 'Adj Close' in df.columns:
            df = df['Adj Close']
        elif 'Close' in df.columns:
            df = df['Close']
        else:
            st.error(f"No valid price column for {ticker}. Columns: {df.columns.tolist()}")
            return pd.Series(dtype=float)

    return df.ffill().dropna()

def normalize_series(series):
    return (series / series.iloc[0]) * 100

# Fetch and display data
if selected_indices:
    st.subheader("Normalized Performance Chart")
    fig = go.Figure()
    price_data = {}

    for index in selected_indices:
        ticker = INDEX_TICKERS[index]
        data = fetch_data(ticker, start_date, end_date)
        if data.empty:
            continue
        norm_data = normalize_series(data)
        price_data[index] = data
        fig.add_trace(go.Scatter(
            x=norm_data.index,
            y=norm_data,
            mode='lines+markers',
            name=index,
            hovertemplate=f"%{{x}}<br>{index}: %{{y:.2f}}"
        ))

    fig.update_layout(
        title="Normalized Market Index Performance",
        xaxis_title="Date",
        yaxis_title="Indexed Value (Start = 100)",
        legend_title="Indices",
        hovermode="x unified",
        height=600,
        xaxis=dict(rangeslider=dict(visible=True), type="date"),
        yaxis=dict(fixedrange=False),
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Chart 2: Cumulative Returns
    st.subheader("Cumulative Returns Chart")
    fig_cum = go.Figure()
    for index, series in price_data.items():
        returns = series.pct_change().fillna(0)
        cum_returns = (1 + returns).cumprod() - 1
        fig_cum.add_trace(go.Scatter(
            x=cum_returns.index,
            y=cum_returns * 100,
            mode='lines',
            name=index,
            hovertemplate=f"%{{x}}<br>{index} Cumulative Return: %{{y:.2f}}%"
        ))
    fig_cum.update_layout(
        title="Cumulative Returns Since Start Date",
        xaxis_title="Date",
        yaxis_title="Cumulative Return (%)",
        template="plotly_white",
        hovermode="x unified",
        height=500
    )
    st.plotly_chart(fig_cum, use_container_width=True)

    # Chart 3: Rolling Volatility
    st.subheader("Rolling 20-Day Volatility")
    fig_vol = go.Figure()
    for index, series in price_data.items():
        daily_returns = series.pct_change().fillna(0)
        rolling_vol = daily_returns.rolling(window=20).std() * 100
        fig_vol.add_trace(go.Scatter(
            x=rolling_vol.index,
            y=rolling_vol,
            mode='lines',
            name=index,
            hovertemplate=f"%{{x}}<br>{index} Volatility: %{{y:.2f}}%"
        ))
    fig_vol.update_layout(
        title="20-Day Rolling Volatility",
        xaxis_title="Date",
        yaxis_title="Volatility (%)",
        template="plotly_white",
        hovermode="x unified",
        height=500
    )
    st.plotly_chart(fig_vol, use_container_width=True)

    # Summary Table
    st.subheader("Performance Summary Table")
    summary_data = []
    for index, series in price_data.items():
        start_price = series.iloc[0]
        end_price = series.iloc[-1]
        total_return = (end_price / start_price - 1) * 100
        daily_returns = series.pct_change().dropna()
        avg_daily_return = daily_returns.mean() * 100
        volatility = daily_returns.std() * 100
        summary_data.append({
            "Index": index,
            "Start Price": f"{start_price:.2f}",
            "End Price": f"{end_price:.2f}",
            "Total Return (%)": f"{total_return:.2f}",
            "Avg Daily Return (%)": f"{avg_daily_return:.3f}",
            "Volatility (%)": f"{volatility:.3f}"
        })
    summary_df = pd.DataFrame(summary_data)
    st.dataframe(summary_df)

    # Download summary as CSV
    csv_summary = summary_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Summary as CSV", data=csv_summary, file_name="performance_summary.csv", mime="text/csv")

    # Option to export raw normalized data
    if st.checkbox("Show raw data"):
        combined_df = pd.DataFrame({index: normalize_series(fetch_data(INDEX_TICKERS[index], start_date, end_date)) for index in selected_indices})
        st.dataframe(combined_df)
        csv = combined_df.to_csv().encode('utf-8')
        st.download_button("Download Normalized Data as CSV", data=csv, file_name="index_data.csv", mime="text/csv")
else:
    st.warning("Please select at least one index to display the chart.")