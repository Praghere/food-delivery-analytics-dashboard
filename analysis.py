"""
Food Delivery Order & Customer Behavior Analysis
=================================================
Loads the real survey CSV, cleans it, and enriches it with
deterministically simulated order-level fields so every analysis
requirement (food category, restaurant, item price, quantity,
payment method, order date, delivery time) can be fulfilled.
"""

import numpy as np
import pandas as pd
import os

# ─────────────────────────────────────────────────────────────────────────────
# PATHS
# ─────────────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, "online food delivery dataset.csv")

# ─────────────────────────────────────────────────────────────────────────────
# SEED DATA FOR SIMULATION
# ─────────────────────────────────────────────────────────────────────────────
FOOD_CATEGORIES = ["Biryani", "Pizza", "Burger", "South Indian", "Chinese",
                   "North Indian", "Desserts", "Beverages", "Sandwich", "Rolls"]

CATEGORY_PRICES = {
    "Biryani":      (180, 350),
    "Pizza":        (200, 450),
    "Burger":       (80,  200),
    "South Indian": (60,  180),
    "Chinese":      (120, 300),
    "North Indian": (150, 350),
    "Desserts":     (50,  150),
    "Beverages":    (30,  120),
    "Sandwich":     (60,  160),
    "Rolls":        (80,  180),
}

RESTAURANTS = [
    "Spice Garden", "Pizza Palace", "Burger Barn", "Dosa Hub",
    "Dragon Wok", "Curry House", "Sweet Treats", "Café Sip",
    "Sub Station", "Roll Fiesta", "Biryani Bros", "The Pizza Co",
    "Grill Nation", "Mumbai Masala", "Wok Express",
]

PAYMENT_METHODS = ["UPI", "Cash on Delivery", "Credit Card", "Debit Card", "Net Banking"]

CITIES = ["Bangalore", "Mumbai", "Delhi", "Hyderabad", "Chennai",
          "Pune", "Kolkata", "Ahmedabad"]

# ─────────────────────────────────────────────────────────────────────────────
# STEP 1 — LOAD & CLEAN
# ─────────────────────────────────────────────────────────────────────────────

def load_and_clean(path: str = CSV_PATH) -> pd.DataFrame:
    """Load CSV, fix column names, drop duplicates, handle missing values."""
    df = pd.read_csv(path)

    # Strip whitespace from column names and string values
    df.columns = df.columns.str.strip()
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip()

    # Rename the trailing unnamed column if present
    df = df.loc[:, ~df.columns.str.startswith("Unnamed")]

    # Drop full-duplicate rows
    before = len(df)
    df.drop_duplicates(inplace=True)
    dupes_removed = before - len(df)

    # Fill missing numeric with median
    for col in df.select_dtypes(include=[np.number]).columns:
        df[col] = df[col].fillna(df[col].median())

    # Fill missing categoricals with mode
    for col in df.select_dtypes(include="object").columns:
        if df[col].isna().any():
            df[col] = df[col].fillna(df[col].mode()[0])

    # Standardise binary columns
    df["Output"] = df["Output"].map({"Yes": 1, "No": 0}).fillna(0).astype(int)
    df["Feedback"] = df["Feedback"].str.strip().str.lower()
    df["Feedback"] = df["Feedback"].map({"positive": "Positive", "negative": "Negative"}).fillna("Positive")

    df["_dupes_removed"] = dupes_removed  # carry for reporting
    df.reset_index(drop=True, inplace=True)
    return df


# ─────────────────────────────────────────────────────────────────────────────
# STEP 2 — SIMULATE ORDER-LEVEL FIELDS
# ─────────────────────────────────────────────────────────────────────────────

def simulate_orders(df: pd.DataFrame) -> pd.DataFrame:
    """
    Attach realistic simulated order fields to each row.
    Uses a fixed seed so results are reproducible.
    """
    n = len(df)
    rng = np.random.default_rng(42)

    # --- Food category (weighted by Customer Type)
    freq_weights = [0.18, 0.14, 0.12, 0.10, 0.10, 0.10, 0.07, 0.07, 0.06, 0.06]
    cat_idx = rng.choice(len(FOOD_CATEGORIES), size=n, p=freq_weights)
    df["Food Category"] = [FOOD_CATEGORIES[i] for i in cat_idx]

    # --- Item price within category range
    prices = []
    for cat in df["Food Category"]:
        lo, hi = CATEGORY_PRICES[cat]
        prices.append(round(rng.integers(lo, hi + 1), -1))  # nearest 10
    df["Item Price"] = prices

    # --- Quantity (1–4, family-size influenced)
    base_qty = rng.integers(1, 4, size=n)
    large_family = (df["Family size"] >= 4).astype(int)
    df["Quantity"] = np.clip(base_qty + large_family, 1, 5)

    # --- Order Value
    df["Order Value"] = df["Quantity"] * df["Item Price"]

    # --- Restaurant (assigned per category for realism)
    cat_to_rest = {
        "Biryani":      ["Biryani Bros", "Spice Garden", "Curry House"],
        "Pizza":        ["Pizza Palace", "The Pizza Co"],
        "Burger":       ["Burger Barn", "Grill Nation"],
        "South Indian": ["Dosa Hub", "Mumbai Masala"],
        "Chinese":      ["Dragon Wok", "Wok Express"],
        "North Indian": ["Curry House", "Mumbai Masala", "Spice Garden"],
        "Desserts":     ["Sweet Treats", "Café Sip"],
        "Beverages":    ["Café Sip", "Sweet Treats"],
        "Sandwich":     ["Sub Station", "Grill Nation"],
        "Rolls":        ["Roll Fiesta", "Sub Station"],
    }
    restaurants = []
    for cat in df["Food Category"]:
        options = cat_to_rest[cat]
        restaurants.append(options[rng.integers(0, len(options))])
    df["Restaurant"] = restaurants

    # --- Payment method
    pay_weights = [0.38, 0.28, 0.15, 0.12, 0.07]
    pay_idx = rng.choice(len(PAYMENT_METHODS), size=n, p=pay_weights)
    df["Payment Method"] = [PAYMENT_METHODS[i] for i in pay_idx]

    # --- City (mapped roughly from Pin code prefix)
    pin_city = {
        "5600": "Bangalore", "5601": "Bangalore", "5602": "Bangalore",
    }
    city_pool = CITIES
    city_idx = rng.integers(0, len(city_pool), size=n)
    df["City"] = [city_pool[i] for i in city_idx]
    # Override based on pin code prefix for plausibility
    mask_blr = df["Pin code"].astype(str).str.startswith("560")
    df.loc[mask_blr, "City"] = "Bangalore"

    # --- Order date (spread over 12 months of 2024)
    start = pd.Timestamp("2024-01-01")
    days_offset = rng.integers(0, 366, size=n)
    df["Order Date"] = [start + pd.Timedelta(days=int(d)) for d in days_offset]
    df["Month"] = df["Order Date"].dt.strftime("%b %Y")
    df["Month Num"] = df["Order Date"].dt.to_period("M")

    # --- Delivery time (minutes): base 25–55 min; longer for large orders
    base_delivery = rng.integers(25, 56, size=n)
    delay_flag = (df["Order Value"] > 600).astype(int) * rng.integers(0, 20, size=n)
    df["Delivery Time (min)"] = base_delivery + delay_flag

    # --- Customer rating (1–5), correlated with Feedback
    ratings = []
    for fb in df["Feedback"]:
        if fb == "Positive":
            ratings.append(rng.choice([3, 4, 4, 5, 5]))
        else:
            ratings.append(rng.choice([1, 2, 2, 3]))
    df["Customer Rating"] = ratings

    # --- Customer ID (anonymised)
    df["Customer ID"] = ["CUST" + str(i + 1).zfill(4) for i in df.index]

    return df


# ─────────────────────────────────────────────────────────────────────────────
# STEP 3 — AGGREGATIONS & INSIGHTS
# ─────────────────────────────────────────────────────────────────────────────

def compute_kpis(df: pd.DataFrame) -> dict:
    ordered = df[df["Output"] == 1]
    return {
        "total_orders":       len(ordered),
        "total_revenue":      ordered["Order Value"].sum(),
        "total_customers":    df["Customer ID"].nunique(),
        "avg_order_value":    ordered["Order Value"].mean(),
        "avg_delivery_time":  ordered["Delivery Time (min)"].mean(),
        "avg_rating":         ordered["Customer Rating"].mean(),
        "positive_feedback_pct": (
            (ordered["Feedback"] == "Positive").sum() / len(ordered) * 100
            if len(ordered) > 0 else 0
        ),
    }


def orders_by_month(df: pd.DataFrame) -> pd.DataFrame:
    ordered = df[df["Output"] == 1].copy()
    ordered["Month Label"] = ordered["Order Date"].dt.strftime("%b %Y")
    ordered["Period"] = ordered["Order Date"].dt.to_period("M")
    grp = (ordered.groupby("Period", observed=True)
           .agg(Orders=("Order Value", "count"),
                Revenue=("Order Value", "sum"))
           .reset_index())
    grp["Month Label"] = grp["Period"].dt.strftime("%b %Y")
    grp = grp.sort_values("Period")
    return grp


def revenue_by_category(df: pd.DataFrame) -> pd.DataFrame:
    ordered = df[df["Output"] == 1]
    return (ordered.groupby("Food Category", observed=True)
            .agg(Revenue=("Order Value", "sum"),
                 Orders=("Order Value", "count"))
            .sort_values("Revenue", ascending=False)
            .reset_index())


def top_restaurants(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    ordered = df[df["Output"] == 1]
    return (ordered.groupby("Restaurant", observed=True)
            .agg(Revenue=("Order Value", "sum"),
                 Orders=("Order Value", "count"),
                 Avg_Rating=("Customer Rating", "mean"))
            .sort_values("Revenue", ascending=False)
            .head(n)
            .reset_index())


def popular_food_items(df: pd.DataFrame) -> pd.DataFrame:
    ordered = df[df["Output"] == 1]
    return (ordered.groupby("Food Category", observed=True)
            .agg(Total_Orders=("Quantity", "sum"),
                 Avg_Price=("Item Price", "mean"))
            .sort_values("Total_Orders", ascending=False)
            .reset_index())


def customer_spending(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    ordered = df[df["Output"] == 1]
    return (ordered.groupby("Customer ID", observed=True)
            .agg(Total_Spent=("Order Value", "sum"),
                 Orders=("Order Value", "count"),
                 Avg_Order=("Order Value", "mean"))
            .sort_values("Total_Spent", ascending=False)
            .head(n)
            .reset_index())


def payment_method_analysis(df: pd.DataFrame) -> pd.DataFrame:
    ordered = df[df["Output"] == 1]
    total = len(ordered)
    grp = (ordered.groupby("Payment Method", observed=True)
           .agg(Count=("Order Value", "count"),
                Revenue=("Order Value", "sum"))
           .reset_index())
    grp["Share (%)"] = (grp["Count"] / total * 100).round(1)
    return grp.sort_values("Count", ascending=False)


def customer_type_analysis(df: pd.DataFrame) -> pd.DataFrame:
    ordered = df[df["Output"] == 1]
    return (ordered.groupby("Customer Type", observed=True)
            .agg(Count=("Customer ID", "count"),
                 Avg_Spend=("Order Value", "mean"),
                 Avg_Rating=("Customer Rating", "mean"))
            .reset_index())


def delivery_performance(df: pd.DataFrame) -> dict:
    ordered = df[df["Output"] == 1]
    threshold = 45  # minutes
    delayed = ordered[ordered["Delivery Time (min)"] > threshold]
    return {
        "avg_delivery_time": ordered["Delivery Time (min)"].mean(),
        "min_delivery_time": ordered["Delivery Time (min)"].min(),
        "max_delivery_time": ordered["Delivery Time (min)"].max(),
        "delayed_orders":    len(delayed),
        "delayed_pct":       len(delayed) / len(ordered) * 100 if len(ordered) > 0 else 0,
        "on_time_pct":       (1 - len(delayed) / len(ordered)) * 100 if len(ordered) > 0 else 0,
    }


def age_group_analysis(df: pd.DataFrame) -> pd.DataFrame:
    ordered = df[df["Output"] == 1].copy()
    bins = [0, 20, 25, 30, 35, 100]
    labels = ["<20", "20–24", "25–29", "30–34", "35+"]
    ordered["Age Group"] = pd.cut(ordered["Age"], bins=bins, labels=labels, right=False)
    return (ordered.groupby("Age Group", observed=True)
            .agg(Orders=("Order Value", "count"),
                 Avg_Spend=("Order Value", "mean"),
                 Avg_Rating=("Customer Rating", "mean"))
            .reset_index())


def occupation_analysis(df: pd.DataFrame) -> pd.DataFrame:
    ordered = df[df["Output"] == 1]
    return (ordered.groupby("Occupation", observed=True)
            .agg(Orders=("Order Value", "count"),
                 Avg_Spend=("Order Value", "mean"))
            .sort_values("Orders", ascending=False)
            .reset_index())


def income_analysis(df: pd.DataFrame) -> pd.DataFrame:
    ordered = df[df["Output"] == 1]
    income_order = [
        "No Income", "Below Rs.10000", "10001 to 25000",
        "25001 to 50000", "More than 50000"
    ]
    grp = (ordered.groupby("Monthly Income", observed=True)
           .agg(Orders=("Order Value", "count"),
                Avg_Spend=("Order Value", "mean"))
           .reset_index())
    grp["Monthly Income"] = pd.Categorical(
        grp["Monthly Income"], categories=income_order, ordered=True
    )
    return grp.sort_values("Monthly Income")


def delivery_by_city(df: pd.DataFrame) -> pd.DataFrame:
    ordered = df[df["Output"] == 1]
    return (ordered.groupby("City", observed=True)
            .agg(Orders=("Order Value", "count"),
                 Revenue=("Order Value", "sum"),
                 Avg_Delivery=("Delivery Time (min)", "mean"))
            .sort_values("Revenue", ascending=False)
            .reset_index())


# ─────────────────────────────────────────────────────────────────────────────
# MAIN — build full enriched dataframe
# ─────────────────────────────────────────────────────────────────────────────

def build_dataframe(path: str = CSV_PATH) -> pd.DataFrame:
    df = load_and_clean(path)
    df = simulate_orders(df)
    return df


if __name__ == "__main__":
    df = build_dataframe()
    print(f"Dataset shape  : {df.shape}")
    print(f"Duplicates removed: {df['_dupes_removed'].iloc[0]}")
    print(f"\nColumns: {df.columns.tolist()}")
    print(f"\nKPIs:\n{compute_kpis(df)}")
    print(f"\nTop 5 food categories:\n{revenue_by_category(df).head()}")
    print(f"\nDelivery performance:\n{delivery_performance(df)}")
