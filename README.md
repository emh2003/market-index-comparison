# 📊 Market Index Comparison Tool

An interactive Streamlit web app that lets users compare historical performance, cumulative returns, and volatility of major U.S. market indices.

---

## 🧠 Overview

This tool was created for an Advanced Financial Modeling group project. It enables users to:

- Select one or more market indices (e.g., S&P 500, NASDAQ, Dow Jones)
- Define a custom date range
- View normalized performance trends
- Analyze cumulative returns and rolling 20-day volatility
- Export data to CSV for further analysis

---

## 🚀 Features

- 📈 **Normalized Performance Chart**  
  Compares selected indices on a common scale starting at 100.

- 📊 **Cumulative Returns**  
  Tracks total return percentage over time since the selected start date.

- 📉 **Rolling Volatility**  
  Displays 20-day rolling standard deviation of daily returns as a volatility measure.

- 📋 **Performance Summary Table**  
  Reports total return, average daily return, and volatility for each index.

- 💾 **CSV Export**  
  Download raw normalized data and performance summaries.

- 🖱️ **Interactive Visualization**  
  Includes zooming, hovering, tooltips, and dynamic range selection with Plotly.

---

## 🛠️ Technologies Used

- [Python 3.12](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [yFinance](https://pypi.org/project/yfinance/)
- [Pandas](https://pandas.pydata.org/)
- [Plotly](https://plotly.com/python/)

---

## 📦 Installation

1. **Clone this repository:**

```bash
git clone https://github.com/yourusername/market-index-comparison.git
cd market-index-comparison

2. **(Optional) Create a virtual environment:**
python -m venv venv
Activate the environment:
On Windows:
venv\\Scripts\\activate
On macOS/Linux:
source venv/bin/activate

3. Install dependencies:
pip install -r requirements.txt

4. Run the app:
streamlit run app.py

---

👥 Team Members
Emily Huddleston

Finlay Torrance

Chandler Stults

Tanner Sweatman

