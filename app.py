import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d

# 📌 Define Stock Holdings & Currency
holdings = {
    "PLTR": {"quantity": 561, "cost_basis": 20.6602, "currency": "USD"},
    "SOFI": {"quantity": 300, "cost_basis": 8.22, "currency": "USD"},
    "GME": {"quantity": 30, "cost_basis": 28.39, "currency": "USD"},
    "CLSK": {"quantity": 70, "cost_basis": 16.56, "currency": "USD"},
    "BTBT": {"quantity": 300, "cost_basis": 4.07, "currency": "USD"},
    "CIFR": {"quantity": 350, "cost_basis": 4.04, "currency": "USD"},
    "NU260116C00025000": {"quantity": 10, "cost_basis": 0.29, "currency": "USD"},
    "ETHX-B.TO": {"quantity": 8, "cost_basis": 19.97, "currency": "CAD"},
    "BITF.TO": {"quantity": 521, "cost_basis": 3.39, "currency": "CAD"},
    "BTCC-B.TO": {"quantity": 220.5312, "cost_basis": 7.96, "currency": "CAD"},
    "HUT.TO": {"quantity": 40, "cost_basis": 13.52, "currency": "CAD"},
    "SHOP.TO": {"quantity": 4, "cost_basis": 96.58, "currency": "CAD"},
    "TSLA.NE": {"quantity": 258, "cost_basis": 22.01, "currency": "CAD"}
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
        hist = stock.history(period="2d")  # Fetch last two days for % change calc
        
        # Check if data is empty
        if hist.empty:
            print(f"⚠ Warning: No data for {symbol}. Skipping...")
            continue  # Skip this stock

        price = hist["Close"].iloc[-1]  # Get last available price
        prev_price = hist["Close"].iloc[-2] if len(hist) > 1 else price

        value_original = info["quantity"] * price
        value_cad = value_original * usd_to_cad if info["currency"] == "USD" else value_original
        value_usd = value_original / usd_to_cad if info["currency"] == "CAD" else value_original
        
        book_value = info["quantity"] * info["cost_basis"]
        percent_change_cost_basis = ((price - info["cost_basis"]) / info["cost_basis"]) * 100
        percent_change_last_day = ((price - prev_price) / prev_price) * 100

        data[symbol] = {
            "Last Price": price,
            "Cost Basis": info["cost_basis"],
            "Quantity": info["quantity"],
            "Book Value": book_value,
            ##"Value (Original)": value_original,
            "Value (CAD)": value_cad,
            "Value (USD)": value_usd,
            "% Change from Cost Basis": percent_change_cost_basis,
            "% Change from Last Trading Day": percent_change_last_day
        }
    
    return pd.DataFrame.from_dict(data, orient="index")

df = fetch_prices(holdings, usd_to_cad)
df["Percentage of Portfolio"] = df["Value (CAD)"] / df["Value (CAD)"].sum()

# 📌 Portfolio Total Values
total_value_cad = df["Value (CAD)"].sum()
total_value_usd = df["Value (USD)"].sum()

# 📌 Streamlit App
st.title("📈 Stock Portfolio Dashboard")

# 🔹 Display Exchange Rate
st.subheader("💱 Exchange Rate")
st.write(f"1 USD = {usd_to_cad:.2f} CAD")

# 🔹 Portfolio Table
st.subheader("📋 Portfolio Overview")
def highlight_percentage(val):
    color = "green" if val > 0 else "red"
    return f'color: {color}'

st.dataframe(
    df.style.format({
        "Last Price": "{:,.2f}",
        "Cost Basis": "{:,.2f}",
        ##"Value (Original)": "{:,.2f}",
        "Book Value": "{:,.2f}",
        "Value (CAD)": "{:,.2f}",
        "Value (USD)": "{:,.2f}",
        "% Change from Cost Basis": "{:+.2f}%",
        "% Change from Last Trading Day": "{:+.2f}%",
        "Percentage of Portfolio": "{:.2%}"
    }).applymap(highlight_percentage, subset=["% Change from Cost Basis", "% Change from Last Trading Day"])
)

# 🔹 Portfolio Total Values
st.subheader("📊 Portfolio Total Value")
st.write(f"💰 Total Value: {total_value_cad:,.2f} CAD | {total_value_usd:,.2f} USD")

# 🔹 Second Portfolio Placeholder
st.subheader("📋 Second Portfolio Overview")
# 📌 Define Stock Holdings & Currency
holdings2 = {
    "ETHX-B.TO": {"quantity": 21, "cost_basis": 14.14, "currency": "CAD"},
    "BITF.TO": {"quantity": 2079, "cost_basis": 2.47, "currency": "CAD"},
    "FBTC.TO": {"quantity": 11, "cost_basis": 21.87, "currency": "CAD"},
    "SHOP.TO": {"quantity": 29, "cost_basis": 96.84, "currency": "CAD"},
}


# 📌 Fetch Real-Time Prices & Convert to CAD & USD
def fetch_prices(holdings2, usd_to_cad):
    data = {}
    for symbol, info in holdings2.items():
        stock = yf.Ticker(symbol)
        hist = stock.history(period="2d")  # Fetch last two days for % change calc
        
        # Check if data is empty
        if hist.empty:
            print(f"⚠ Warning: No data for {symbol}. Skipping...")
            continue  # Skip this stock

        price = hist["Close"].iloc[-1]  # Get last available price
        prev_price = hist["Close"].iloc[-2] if len(hist) > 1 else price

        value_original = info["quantity"] * price
        value_cad = value_original * usd_to_cad if info["currency"] == "USD" else value_original
        value_usd = value_original / usd_to_cad if info["currency"] == "CAD" else value_original
        
        book_value = info["quantity"] * info["cost_basis"]
        percent_change_cost_basis = ((price - info["cost_basis"]) / info["cost_basis"]) * 100
        percent_change_last_day = ((price - prev_price) / prev_price) * 100

        data[symbol] = {
            "Last Price": price,
            "Cost Basis": info["cost_basis"],
            "Quantity": info["quantity"],
            "Book Value": book_value,
            ##"Value (Original)": value_original,
            "Value (CAD)": value_cad,
            "Value (USD)": value_usd,
            "% Change from Cost Basis": percent_change_cost_basis,
            "% Change from Last Trading Day": percent_change_last_day
        }
    
    return pd.DataFrame.from_dict(data, orient="index")

df = fetch_prices(holdings2, usd_to_cad)
df["Percentage of Portfolio"] = df["Value (CAD)"] / df["Value (CAD)"].sum()

# 📌 Portfolio Total Values
total_value_cad = df["Value (CAD)"].sum()
total_value_usd = df["Value (USD)"].sum()


def highlight_percentage(val):
    color = "green" if val > 0 else "red"
    return f'color: {color}'

st.dataframe(
    df.style.format({
        "Last Price": "{:,.2f}",
        "Cost Basis": "{:,.2f}",
        ##"Value (Original)": "{:,.2f}",
        "Book Value": "{:,.2f}",
        "Value (CAD)": "{:,.2f}",
        "Value (USD)": "{:,.2f}",
        "% Change from Cost Basis": "{:+.2f}%",
        "% Change from Last Trading Day": "{:+.2f}%",
        "Percentage of Portfolio": "{:.2%}"
    }).applymap(highlight_percentage, subset=["% Change from Cost Basis", "% Change from Last Trading Day"])
)

# 🔹 Portfolio Total Values
st.subheader("📊 FHSA Portfolio Total Value")
st.write(f"💰 Total Value: {total_value_cad:,.2f} CAD | {total_value_usd:,.2f} USD")

# Expand table size
st.markdown(
    """
    <style>
    .dataframe-container { max-height: 800px !important; width: 100% !important; }
    </style>
    """,
    unsafe_allow_html=True
)


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
#         if info["cost_basis": ,"currency"] == "USD":
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
#     currency = "🇺🇸" if holdings[symbol]["cost_basis": ,"currency"] == "USD" else "🇨🇦"
#     ax.text(points[i, 0], points[i, 1], f"{symbol} {currency}", fontsize=12, weight="bold", ha="center", color="white")

# ax.set_title("Portfolio Allocation (Size = % Holding in CAD)")
# ax.axis("off")
# st.pyplot(fig)
