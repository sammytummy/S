import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d

# 📌 Define Stock Holdings & Currency
holdings = {
    "PLTR": {"quantity": 561, "currency": "USD"},
    "SOFI": {"quantity": 300, "currency": "USD"},
    "GME": {"quantity": 30, "currency": "USD"},
    "CLSK": {"quantity": 70, "currency": "USD"},
    "BTBT": {"quantity": 300, "currency": "USD"},
    "CIFR": {"quantity": 350, "currency": "USD"},
    "NU260116C00025000": {"quantity": 10, "currency": "USD"},
    "ETHX-B.TO": {"quantity": 8, "currency": "CAD"},
    "BITF.TO": {"quantity": 521, "currency": "CAD"},
    "BTCC-B.TO": {"quantity": 220, "currency": "CAD"},
    "HUT.TO": {"quantity": 40, "currency": "CAD"},
    "SHOP.TO": {"quantity": 4, "currency": "CAD"},
    "TSLA.NE": {"quantity": 258, "currency": "CAD"}
}

# 📌 Fetch USD/CAD Exchange Rate
def get_exchange_rate():
    forex = yf.Ticker("CAD=X")  # USD to CAD exchange rate
    return forex.history(period="1d")["Close"].iloc[-1]

usd_to_cad = get_exchange_rate()

# 📌 Fetch Real-Time Prices & Convert to CAD & USD
def fetch_prices(holdings, usd_to_cad):
    data = {}
    for symbol, info in holdings.items():
        stock = yf.Ticker(symbol)
        hist = stock.history(period="1d")
        
        # Check if data is empty
        if hist.empty:
            print(f"⚠ Warning: No data for {symbol}. Skipping...")
            continue  # Skip this stock

        price = hist["Close"].iloc[-1]  # Get last available price

        value_original = info["quantity"] * price
        value_cad = value_original * usd_to_cad if info["currency"] == "USD" else value_original
        value_usd = value_original / usd_to_cad if info["currency"] == "CAD" else value_original

        data[symbol] = {
            "Currency": info["currency"],
            "Quantity": info["quantity"],
            "Value (Original)": value_original,
            "Value (CAD)": value_cad,
            "Value (USD)": value_usd,
        }
    
    return pd.DataFrame.from_dict(data, orient="index")


df = fetch_prices(holdings, usd_to_cad)
df["Percentage"] = df["Value (CAD)"] / df["Value (CAD)"].sum()

# 📌 Streamlit App
st.title("📈 Stock Portfolio Dashboard")

# 🔹 Display Exchange Rate
st.subheader("💱 Exchange Rate")
st.write(f"1 USD = {usd_to_cad:.2f} CAD")

# 🔹 Portfolio Table
st.subheader("📋 Portfolio Overview")
st.dataframe(df.style.format({
    "Value (Original)": "{:,.2f}",
    "Value (CAD)": "{:,.2f}",
    "Value (USD)": "{:,.2f}",
    "Percentage": "{:.2%}"
}))

# # 🔹 Function to Fetch Historical Portfolio Value (Only CAD)
# def fetch_historical_portfolio(holdings):
#     start_date = "2024-01-01"  # Adjust as needed
#     end_date = pd.Timestamp.today().strftime("%Y-%m-%d")

#     portfolio_value_cad = pd.DataFrame()

#     # Fetch historical exchange rates (USD to CAD)
#     forex = yf.Ticker("CAD=X").history(start=start_date, end=end_date)
#     forex["Exchange Rate"] = forex["Close"]  # USD → CAD

#     for symbol, info in holdings.items():
#         stock = yf.Ticker(symbol)
#         hist = stock.history(start=start_date, end=end_date)

#         if hist.empty:
#             print(f"⚠ Warning: No historical data for {symbol}. Skipping...")
#             continue

#         # Compute stock value over time
#         hist["Value"] = hist["Close"] * info["quantity"]

#         # Convert USD stocks to CAD
#         if info["currency"] == "USD":
#             hist["Value (CAD)"] = hist["Value"] * forex["Exchange Rate"]
#         else:
#             hist["Value (CAD)"] = hist["Value"]

#         # Merge into portfolio dataframe
#         portfolio_value_cad = pd.concat([portfolio_value_cad, hist["Value (CAD)"]], axis=1)

#     # Sum across all stocks to get total portfolio value in CAD
#     total_value_cad = portfolio_value_cad.sum(axis=1)

#     return total_value_cad

# # 🔹 Fetch Portfolio History
# df_cad = fetch_historical_portfolio(holdings)

# # 🔹 Plot Historical Portfolio Value (Only CAD)
# st.subheader("📈 Total Historical Portfolio Value (CAD)")
# fig, ax = plt.subplots(figsize=(10, 5))

# ax.plot(df_cad.index, df_cad, label="Total Portfolio in CAD", color="blue", linewidth=2)

# ax.set_title("Historical Portfolio Value Over Time")
# ax.set_ylabel("Total Portfolio Value (CAD)")
# ax.legend()
# ax.grid()

# st.pyplot(fig)

# # 🔹 Voronoi Treemap with Custom Styling
# st.subheader("🗺️ Portfolio Allocation (Voronoi Treemap)")

# # Generate Voronoi Diagram
# np.random.seed(42)
# points = np.random.rand(len(df), 2)
# vor = Voronoi(points)

# fig, ax = plt.subplots(figsize=(8, 6))
# voronoi_plot_2d(vor, ax=ax, show_vertices=False, line_colors="red", line_width=2)

# # Fill Regions with Blue & Add Black Borders
# for region in vor.regions:
#     if not -1 in region and len(region) > 0:
#         polygon = [vor.vertices[i] for i in region]
#         plt.fill(*zip(*polygon), color="blue", edgecolor="black", linewidth=2)

# # Add Stock Labels
# for i, symbol in enumerate(df.index):
#     currency = "🇺🇸" if holdings[symbol]["currency"] == "USD" else "🇨🇦"
#     ax.text(points[i, 0], points[i, 1], f"{symbol} {currency}", fontsize=12, weight="bold", ha="center", color="white")

# ax.set_title("Portfolio Allocation (Size = % Holding in CAD)")
# ax.axis("off")
# st.pyplot(fig)
