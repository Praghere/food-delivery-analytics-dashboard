"""
Food Delivery Order & Customer Behavior — Streamlit Dashboard
=============================================================
Run:  streamlit run app.py
"""

import os
import sys

# Allow imports from this folder regardless of working directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from analysis import (
    build_dataframe,
    compute_kpis,
    orders_by_month,
    revenue_by_category,
    top_restaurants,
    popular_food_items,
    customer_spending,
    payment_method_analysis,
    customer_type_analysis,
    delivery_performance,
    age_group_analysis,
    occupation_analysis,
    income_analysis,
    delivery_by_city,
)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Food Delivery Analytics",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# COLOUR PALETTE
# ─────────────────────────────────────────────────────────────────────────────
PRIMARY   = "#F97316"   # orange
SECONDARY = "#3B82F6"   # blue
SUCCESS   = "#22C55E"   # green
DANGER    = "#EF4444"   # red
PURPLE    = "#A855F7"
TEAL      = "#14B8A6"
GOLD      = "#EAB308"

CATEGORY_COLORS = {
    "Biryani":      "#F97316",
    "Pizza":        "#EF4444",
    "Burger":       "#EAB308",
    "South Indian": "#22C55E",
    "Chinese":      "#3B82F6",
    "North Indian": "#A855F7",
    "Desserts":     "#EC4899",
    "Beverages":    "#14B8A6",
    "Sandwich":     "#F59E0B",
    "Rolls":        "#6366F1",
}

# ─────────────────────────────────────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* KPI card */
    .kpi-card {
        background: #1E293B;
        border-radius: 12px;
        padding: 18px 20px;
        text-align: center;
        border-left: 4px solid;
        height: 110px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .kpi-label {
        font-size: 12px;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 26px;
        font-weight: 700;
        color: #F1F5F9;
        line-height: 1.1;
    }
    .kpi-sub {
        font-size: 11px;
        color: #64748B;
        margin-top: 4px;
    }

    /* Section header */
    .section-title {
        font-size: 18px;
        font-weight: 600;
        color: #F1F5F9;
        margin: 24px 0 10px 0;
        padding-bottom: 6px;
        border-bottom: 2px solid #334155;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0F172A;
    }

    /* Main background */
    .stApp {
        background-color: #0F172A;
    }

    /* Plotly chart borders */
    .js-plotly-plot {
        border-radius: 10px;
        overflow: hidden;
    }

    /* DataFrame */
    .stDataFrame { font-size: 13px; }

    /* Tabs */
    .stTabs [data-baseweb="tab"] {
        font-size: 14px;
        padding: 8px 18px;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# DATA LOAD (cached)
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner="Loading dataset…")
def load_data():
    return build_dataframe()


df_full = load_data()

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR — FILTERS
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🍔 Food Delivery Analytics")
    st.markdown("**Filters**")
    st.markdown("---")

    # Date range
    min_date = df_full["Order Date"].min().date()
    max_date = df_full["Order Date"].max().date()
    date_range = st.date_input(
        "📅 Order Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    # Food category
    all_cats = sorted(df_full["Food Category"].unique())
    sel_cats = st.multiselect(
        "🍽️ Food Category",
        options=all_cats,
        default=all_cats,
    )

    # City
    all_cities = sorted(df_full["City"].unique())
    sel_cities = st.multiselect(
        "🏙️ City",
        options=all_cities,
        default=all_cities,
    )

    # Customer type
    all_ctypes = sorted(df_full["Customer Type"].unique())
    sel_ctypes = st.multiselect(
        "👤 Customer Type",
        options=all_ctypes,
        default=all_ctypes,
    )

    # Restaurant
    all_rests = sorted(df_full["Restaurant"].unique())
    sel_rests = st.multiselect(
        "🏪 Restaurant",
        options=all_rests,
        default=all_rests,
    )

    # Payment method
    all_pays = sorted(df_full["Payment Method"].unique())
    sel_pays = st.multiselect(
        "💳 Payment Method",
        options=all_pays,
        default=all_pays,
    )

    st.markdown("---")
    st.caption(f"Dataset: {len(df_full)} records  |  Ordered: {(df_full['Output']==1).sum()}")

# ─────────────────────────────────────────────────────────────────────────────
# APPLY FILTERS
# ─────────────────────────────────────────────────────────────────────────────
if len(date_range) == 2:
    d_start, d_end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
else:
    d_start, d_end = df_full["Order Date"].min(), df_full["Order Date"].max()

df = df_full[
    (df_full["Order Date"] >= d_start) &
    (df_full["Order Date"] <= d_end) &
    (df_full["Food Category"].isin(sel_cats if sel_cats else all_cats)) &
    (df_full["City"].isin(sel_cities if sel_cities else all_cities)) &
    (df_full["Customer Type"].isin(sel_ctypes if sel_ctypes else all_ctypes)) &
    (df_full["Restaurant"].isin(sel_rests if sel_rests else all_rests)) &
    (df_full["Payment Method"].isin(sel_pays if sel_pays else all_pays))
].copy()

if df.empty:
    st.warning("No data matches the selected filters. Please adjust your selections.")
    st.stop()

ordered = df[df["Output"] == 1]

# ─────────────────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    "<h1 style='color:#F97316; font-size:32px; margin-bottom:4px;'>"
    "🍔 Food Delivery Order & Customer Behavior Analysis"
    "</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='color:#94A3B8; font-size:14px; margin-top:0;'>"
    "Interactive dashboard — use the sidebar to filter by date, category, city, customer type, restaurant, and payment method."
    "</p>",
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# KPI ROW
# ─────────────────────────────────────────────────────────────────────────────
kpis = compute_kpis(df)

kpi_defs = [
    ("Total Orders",          f"{kpis['total_orders']:,}",        "Placed orders",       PRIMARY,   "📦"),
    ("Total Revenue",         f"₹{kpis['total_revenue']:,.0f}",   "Order value sum",     SECONDARY, "💰"),
    ("Total Customers",       f"{kpis['total_customers']:,}",      "Unique customers",    SUCCESS,   "👥"),
    ("Avg Order Value",       f"₹{kpis['avg_order_value']:,.0f}", "Per order",           PURPLE,    "🧾"),
    ("Avg Delivery Time",     f"{kpis['avg_delivery_time']:.1f}m","Minutes",             TEAL,      "🚴"),
    ("Avg Customer Rating",   f"{kpis['avg_rating']:.2f} ★",      "Out of 5",            GOLD,      "⭐"),
]

cols = st.columns(6)
for col, (label, value, sub, color, icon) in zip(cols, kpi_defs):
    col.markdown(
        f"""<div class="kpi-card" style="border-color:{color};">
              <div class="kpi-label">{icon} {label}</div>
              <div class="kpi-value">{value}</div>
              <div class="kpi-sub">{sub}</div>
            </div>""",
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Orders & Revenue",
    "🍽️ Food & Restaurants",
    "👤 Customer Behavior",
    "🚴 Delivery Performance",
    "📊 Demographics",
])

PLOT_BG   = "#0F172A"
GRID_CLR  = "#1E293B"
TEXT_CLR  = "#CBD5E1"
PAPER_BG  = "#0F172A"

AXIS_STYLE = dict(gridcolor=GRID_CLR, linecolor=GRID_CLR)


def base_layout(title="", dual_axis=False):
    """Return a base Plotly layout dict.
    Set dual_axis=True for charts that supply their own yaxis/yaxis2 keys.
    """
    layout = dict(
        template="plotly_dark",
        plot_bgcolor=PLOT_BG,
        paper_bgcolor=PAPER_BG,
        font=dict(color=TEXT_CLR, size=12),
        title=dict(text=title, font=dict(size=15, color="#F1F5F9"), x=0.0),
        margin=dict(l=40, r=20, t=50, b=40),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
    )
    if not dual_axis:
        layout["xaxis"] = AXIS_STYLE
        layout["yaxis"] = AXIS_STYLE
    return layout


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — ORDERS & REVENUE
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    # Monthly trend
    monthly = orders_by_month(df)
    if not monthly.empty:
        monthly_sorted = monthly.sort_values("Period")

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=monthly_sorted["Month Label"],
            y=monthly_sorted["Revenue"],
            name="Revenue (₹)",
            marker_color=PRIMARY,
            opacity=0.85,
            yaxis="y",
        ))
        fig.add_trace(go.Scatter(
            x=monthly_sorted["Month Label"],
            y=monthly_sorted["Orders"],
            name="Orders",
            mode="lines+markers",
            line=dict(color=SECONDARY, width=2.5),
            marker=dict(size=6),
            yaxis="y2",
        ))
        fig.update_layout(
            **base_layout("Monthly Orders & Revenue Trend", dual_axis=True),
            xaxis=AXIS_STYLE,
            yaxis=dict(title="Revenue (₹)", gridcolor=GRID_CLR, linecolor=GRID_CLR),
            yaxis2=dict(title="Order Count", overlaying="y", side="right",
                        gridcolor="rgba(0,0,0,0)", linecolor=GRID_CLR),
            hovermode="x unified",
            height=370,
        )
        st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    # Revenue by category (pie)
    with col1:
        rev_cat = revenue_by_category(df)
        if not rev_cat.empty:
            colors = [CATEGORY_COLORS.get(c, PRIMARY) for c in rev_cat["Food Category"]]
            fig2 = go.Figure(go.Pie(
                labels=rev_cat["Food Category"],
                values=rev_cat["Revenue"],
                hole=0.42,
                marker=dict(colors=colors, line=dict(color=PLOT_BG, width=2)),
                textinfo="label+percent",
                textfont=dict(size=11),
                hovertemplate="<b>%{label}</b><br>Revenue: ₹%{value:,.0f}<br>Share: %{percent}<extra></extra>",
            ))
            fig2.update_layout(
                **base_layout("Revenue by Food Category"),
                showlegend=False,
                height=340,
            )
            st.plotly_chart(fig2, use_container_width=True)

    # Orders by city
    with col2:
        city_data = delivery_by_city(df)
        if not city_data.empty:
            fig3 = px.bar(
                city_data,
                x="City", y="Revenue",
                color="Orders",
                color_continuous_scale=[[0, SECONDARY], [1, PRIMARY]],
                labels={"Revenue": "Revenue (₹)"},
                text_auto=".2s",
            )
            fig3.update_layout(
                **base_layout("Revenue & Orders by City"),
                coloraxis_showscale=False,
                height=340,
            )
            fig3.update_traces(textfont_size=11)
            st.plotly_chart(fig3, use_container_width=True)

    # Payment method
    pay_df = payment_method_analysis(df)
    col3, col4 = st.columns(2)
    with col3:
        if not pay_df.empty:
            fig4 = px.bar(
                pay_df.sort_values("Count"),
                x="Count", y="Payment Method",
                orientation="h",
                color="Share (%)",
                color_continuous_scale=[[0, TEAL], [1, PRIMARY]],
                text="Share (%)",
                labels={"Count": "Orders"},
            )
            fig4.update_traces(texttemplate="%{text:.1f}%", textfont_size=11)
            fig4.update_layout(
                **base_layout("Payment Method Distribution"),
                coloraxis_showscale=False,
                height=300,
            )
            st.plotly_chart(fig4, use_container_width=True)

    with col4:
        pay_rev = pay_df.copy()
        fig5 = px.pie(
            pay_rev, names="Payment Method", values="Revenue",
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.Plasma_r,
        )
        fig5.update_layout(
            **base_layout("Revenue Share by Payment Method"),
            height=300,
            showlegend=True,
        )
        st.plotly_chart(fig5, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — FOOD & RESTAURANTS
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    col1, col2 = st.columns(2)

    # Popular food categories (horizontal bar)
    with col1:
        pop = popular_food_items(df)
        if not pop.empty:
            pop_sorted = pop.sort_values("Total_Orders")
            bar_colors = [CATEGORY_COLORS.get(c, PRIMARY) for c in pop_sorted["Food Category"]]
            fig = go.Figure(go.Bar(
                x=pop_sorted["Total_Orders"],
                y=pop_sorted["Food Category"],
                orientation="h",
                marker_color=bar_colors,
                text=pop_sorted["Total_Orders"],
                textposition="outside",
                hovertemplate="<b>%{y}</b><br>Qty ordered: %{x:,}<extra></extra>",
            ))
            fig.update_layout(
                **base_layout("Most Popular Food Categories (Qty Ordered)"),
                height=370,
                xaxis_title="Total Quantity Ordered",
            )
            st.plotly_chart(fig, use_container_width=True)

    # Average price per category
    with col2:
        if not pop.empty:
            pop_price = pop.sort_values("Avg_Price", ascending=False)
            fig2 = px.bar(
                pop_price,
                x="Food Category", y="Avg_Price",
                color="Food Category",
                color_discrete_map=CATEGORY_COLORS,
                text_auto=",.0f",
                labels={"Avg_Price": "Avg Item Price (₹)"},
            )
            fig2.update_layout(
                **base_layout("Average Item Price by Category"),
                showlegend=False,
                height=370,
                xaxis_tickangle=-30,
            )
            st.plotly_chart(fig2, use_container_width=True)

    # Top restaurants
    top_rest = top_restaurants(df)
    if not top_rest.empty:
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            x=top_rest["Restaurant"],
            y=top_rest["Revenue"],
            name="Revenue (₹)",
            marker_color=PRIMARY,
            opacity=0.9,
            yaxis="y",
            hovertemplate="<b>%{x}</b><br>Revenue: ₹%{y:,.0f}<extra></extra>",
        ))
        fig3.add_trace(go.Scatter(
            x=top_rest["Restaurant"],
            y=top_rest["Avg_Rating"],
            name="Avg Rating",
            mode="lines+markers",
            line=dict(color=GOLD, width=2),
            marker=dict(size=8, symbol="diamond"),
            yaxis="y2",
            hovertemplate="<b>%{x}</b><br>Rating: %{y:.2f}<extra></extra>",
        ))
        fig3.update_layout(
            **base_layout("Top Restaurants — Revenue & Rating", dual_axis=True),
            xaxis=AXIS_STYLE,
            yaxis=dict(title="Revenue (₹)", gridcolor=GRID_CLR, linecolor=GRID_CLR),
            yaxis2=dict(title="Avg Rating", overlaying="y", side="right",
                        range=[0, 5.5], gridcolor="rgba(0,0,0,0)"),
            hovermode="x unified",
            height=360,
        )
        st.plotly_chart(fig3, use_container_width=True)

    # Category × Payment method heatmap
    if not ordered.empty:
        pivot = (ordered.groupby(["Food Category", "Payment Method"], observed=True)
                 .size().unstack(fill_value=0))
        fig4 = px.imshow(
            pivot,
            color_continuous_scale="YlOrRd",
            text_auto=True,
            aspect="auto",
            labels={"color": "Orders"},
        )
        fig4.update_layout(
            **base_layout("Food Category vs Payment Method Heatmap"),
            height=350,
            xaxis_title="Payment Method",
            yaxis_title="Food Category",
            coloraxis_showscale=True,
        )
        st.plotly_chart(fig4, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — CUSTOMER BEHAVIOR
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    col1, col2 = st.columns(2)

    # Customer type distribution
    with col1:
        ct = customer_type_analysis(df)
        if not ct.empty:
            fig = px.bar(
                ct.sort_values("Count", ascending=False),
                x="Customer Type", y="Count",
                color="Customer Type",
                color_discrete_sequence=[PRIMARY, SECONDARY, SUCCESS, PURPLE],
                text="Count",
            )
            fig.update_traces(textposition="outside")
            fig.update_layout(
                **base_layout("Customer Type — Order Count"),
                showlegend=False,
                height=330,
            )
            st.plotly_chart(fig, use_container_width=True)

    # Avg spend per customer type
    with col2:
        if not ct.empty:
            fig2 = px.bar(
                ct.sort_values("Avg_Spend", ascending=False),
                x="Customer Type", y="Avg_Spend",
                color="Customer Type",
                color_discrete_sequence=[PRIMARY, SECONDARY, SUCCESS, PURPLE],
                text_auto=",.0f",
                labels={"Avg_Spend": "Avg Order Value (₹)"},
            )
            fig2.update_traces(textposition="outside")
            fig2.update_layout(
                **base_layout("Average Spend by Customer Type"),
                showlegend=False,
                height=330,
            )
            st.plotly_chart(fig2, use_container_width=True)

    # Top spending customers
    top_cust = customer_spending(df)
    if not top_cust.empty:
        fig3 = px.bar(
            top_cust,
            x="Customer ID", y="Total_Spent",
            color="Orders",
            color_continuous_scale=[[0, SECONDARY], [1, PRIMARY]],
            text_auto=",.0f",
            labels={"Total_Spent": "Total Spent (₹)", "Orders": "Order Count"},
            hover_data={"Avg_Order": ":.0f"},
        )
        fig3.update_layout(
            **base_layout("Top 10 Highest-Spending Customers"),
            coloraxis_showscale=True,
            height=340,
        )
        st.plotly_chart(fig3, use_container_width=True)

    # Feedback breakdown
    col3, col4 = st.columns(2)
    with col3:
        fb = (ordered.groupby(["Customer Type", "Feedback"], observed=True)
              .size().reset_index(name="Count"))
        if not fb.empty:
            fig4 = px.bar(
                fb, x="Customer Type", y="Count", color="Feedback",
                barmode="group",
                color_discrete_map={"Positive": SUCCESS, "Negative": DANGER},
                text_auto=True,
            )
            fig4.update_layout(
                **base_layout("Feedback by Customer Type"),
                height=320,
            )
            st.plotly_chart(fig4, use_container_width=True)

    # Rating distribution
    with col4:
        if not ordered.empty:
            rating_counts = ordered["Customer Rating"].value_counts().sort_index()
            fig5 = go.Figure(go.Bar(
                x=rating_counts.index.astype(str),
                y=rating_counts.values,
                marker_color=[DANGER, "#F97316", GOLD, SUCCESS, TEAL],
                text=rating_counts.values,
                textposition="outside",
            ))
            fig5.update_layout(
                **base_layout("Customer Rating Distribution"),
                xaxis_title="Rating (1–5)",
                yaxis_title="Count",
                height=320,
            )
            st.plotly_chart(fig5, use_container_width=True)

    # Order value scatter vs age
    if not ordered.empty:
        fig6 = px.scatter(
            ordered,
            x="Age", y="Order Value",
            color="Customer Type",
            color_discrete_sequence=[PRIMARY, SECONDARY, SUCCESS, PURPLE],
            size="Quantity",
            opacity=0.65,
            hover_data=["Gender", "Occupation", "Restaurant", "Food Category"],
            labels={"Order Value": "Order Value (₹)"},
        )
        fig6.update_layout(
            **base_layout("Order Value vs Customer Age"),
            height=360,
        )
        st.plotly_chart(fig6, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — DELIVERY PERFORMANCE
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    dp = delivery_performance(df)

    # Delivery KPI mini-cards
    d_cols = st.columns(4)
    d_kpis = [
        ("Avg Delivery Time", f"{dp['avg_delivery_time']:.1f} min", TEAL),
        ("Fastest Delivery",  f"{dp['min_delivery_time']} min",     SUCCESS),
        ("Slowest Delivery",  f"{dp['max_delivery_time']} min",     DANGER),
        ("Delayed Orders",    f"{dp['delayed_orders']:,} ({dp['delayed_pct']:.1f}%)", PRIMARY),
    ]
    for dcol, (lbl, val, clr) in zip(d_cols, d_kpis):
        dcol.markdown(
            f"""<div class="kpi-card" style="border-color:{clr};">
                  <div class="kpi-label">{lbl}</div>
                  <div class="kpi-value">{val}</div>
                </div>""",
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # Delivery time histogram
    with col1:
        if not ordered.empty:
            fig = px.histogram(
                ordered,
                x="Delivery Time (min)",
                nbins=25,
                color_discrete_sequence=[TEAL],
                opacity=0.85,
                labels={"Delivery Time (min)": "Delivery Time (min)"},
            )
            fig.add_vline(x=45, line_dash="dash", line_color=DANGER,
                          annotation_text="45-min threshold",
                          annotation_font_color=DANGER)
            fig.add_vline(x=dp["avg_delivery_time"], line_dash="dot",
                          line_color=GOLD,
                          annotation_text=f"Avg {dp['avg_delivery_time']:.0f}m",
                          annotation_font_color=GOLD)
            fig.update_layout(
                **base_layout("Delivery Time Distribution"),
                yaxis_title="Order Count",
                height=340,
            )
            st.plotly_chart(fig, use_container_width=True)

    # On-time vs delayed donut
    with col2:
        fig2 = go.Figure(go.Pie(
            labels=["On-Time", "Delayed (>45 min)"],
            values=[dp["on_time_pct"], dp["delayed_pct"]],
            hole=0.5,
            marker=dict(colors=[SUCCESS, DANGER], line=dict(color=PLOT_BG, width=3)),
            textinfo="label+percent",
            textfont=dict(size=13),
        ))
        fig2.update_layout(
            **base_layout("On-Time vs Delayed Orders"),
            height=340,
            showlegend=False,
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Avg delivery time by city
    city_d = delivery_by_city(df)
    if not city_d.empty:
        fig3 = px.bar(
            city_d.sort_values("Avg_Delivery"),
            x="City", y="Avg_Delivery",
            color="Avg_Delivery",
            color_continuous_scale=[[0, SUCCESS], [0.5, GOLD], [1, DANGER]],
            text_auto=".1f",
            labels={"Avg_Delivery": "Avg Delivery Time (min)"},
        )
        fig3.update_layout(
            **base_layout("Average Delivery Time by City"),
            coloraxis_showscale=False,
            height=320,
        )
        st.plotly_chart(fig3, use_container_width=True)

    # Delivery time by food category box plot
    if not ordered.empty:
        fig4 = px.box(
            ordered,
            x="Food Category", y="Delivery Time (min)",
            color="Food Category",
            color_discrete_map=CATEGORY_COLORS,
            points="outliers",
        )
        fig4.update_layout(
            **base_layout("Delivery Time Distribution by Food Category"),
            showlegend=False,
            height=360,
            xaxis_tickangle=-25,
        )
        st.plotly_chart(fig4, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — DEMOGRAPHICS
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    col1, col2 = st.columns(2)

    # Age group analysis
    with col1:
        age_grp = age_group_analysis(df)
        if not age_grp.empty:
            fig = px.bar(
                age_grp,
                x="Age Group", y="Orders",
                color="Avg_Spend",
                color_continuous_scale=[[0, SECONDARY], [1, PRIMARY]],
                text_auto=True,
                labels={"Orders": "Order Count", "Avg_Spend": "Avg Spend (₹)"},
            )
            fig.update_layout(
                **base_layout("Orders by Age Group"),
                height=330,
            )
            st.plotly_chart(fig, use_container_width=True)

    # Gender distribution
    with col2:
        if not ordered.empty:
            gender_cnt = ordered["Gender"].value_counts().reset_index()
            gender_cnt.columns = ["Gender", "Count"]
            fig2 = px.pie(
                gender_cnt, names="Gender", values="Count",
                hole=0.4,
                color_discrete_sequence=[SECONDARY, PRIMARY, PURPLE],
            )
            fig2.update_layout(
                **base_layout("Gender Distribution of Ordered Customers"),
                height=330,
            )
            st.plotly_chart(fig2, use_container_width=True)

    # Occupation analysis
    occ_df = occupation_analysis(df)
    if not occ_df.empty:
        fig3 = px.bar(
            occ_df.head(8),
            x="Orders", y="Occupation",
            orientation="h",
            color="Avg_Spend",
            color_continuous_scale=[[0, TEAL], [1, PURPLE]],
            text_auto=True,
            labels={"Orders": "Order Count", "Avg_Spend": "Avg Spend (₹)"},
        )
        fig3.update_layout(
            **base_layout("Orders & Avg Spend by Occupation"),
            coloraxis_showscale=True,
            height=320,
        )
        st.plotly_chart(fig3, use_container_width=True)

    # Income analysis
    inc_df = income_analysis(df)
    col3, col4 = st.columns(2)
    with col3:
        if not inc_df.empty:
            fig4 = px.bar(
                inc_df,
                x="Monthly Income", y="Orders",
                color="Monthly Income",
                color_discrete_sequence=px.colors.sequential.Plasma,
                text_auto=True,
            )
            fig4.update_layout(
                **base_layout("Order Count by Monthly Income"),
                showlegend=False,
                height=320,
                xaxis_tickangle=-25,
            )
            st.plotly_chart(fig4, use_container_width=True)

    with col4:
        if not inc_df.empty:
            fig5 = px.bar(
                inc_df,
                x="Monthly Income", y="Avg_Spend",
                color="Monthly Income",
                color_discrete_sequence=px.colors.sequential.Viridis,
                text_auto=",.0f",
                labels={"Avg_Spend": "Avg Order Value (₹)"},
            )
            fig5.update_layout(
                **base_layout("Avg Spend by Monthly Income"),
                showlegend=False,
                height=320,
                xaxis_tickangle=-25,
            )
            st.plotly_chart(fig5, use_container_width=True)

    # Marital status vs order output
    if not df.empty:
        ms = (df.groupby(["Marital Status", "Output"], observed=True)
              .size().reset_index(name="Count"))
        ms["Output Label"] = ms["Output"].map({1: "Ordered", 0: "Did Not Order"})
        fig6 = px.bar(
            ms, x="Marital Status", y="Count",
            color="Output Label",
            barmode="stack",
            color_discrete_map={"Ordered": SUCCESS, "Did Not Order": DANGER},
            text_auto=True,
        )
        fig6.update_layout(
            **base_layout("Order Placement by Marital Status"),
            height=320,
        )
        st.plotly_chart(fig6, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# BUSINESS INSIGHTS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div class='section-title'>💡 Key Business Insights & Recommendations</div>",
    unsafe_allow_html=True,
)

insights_col1, insights_col2 = st.columns(2)

with insights_col1:
    st.markdown("""
**📦 Orders & Revenue**
- The majority of revenue comes from **Biryani, Pizza**, and **North Indian** categories — focus menu promotions here.
- **UPI** and **Cash on Delivery** dominate payment methods; ensure seamless UPI checkout to reduce drop-offs.
- Monthly trends reveal demand peaks — plan staffing and inventory accordingly.

**🍽️ Food Preferences**
- High-quantity categories like Biryani and Rolls drive volume; bundle deals can further boost revenue.
- Restaurants with high ratings but lower revenue represent untapped potential — marketing support recommended.
""")

with insights_col2:
    st.markdown("""
**👤 Customer Behavior**
- **Frequent customers** generate the highest average order value — introduce a loyalty rewards program.
- Students (the largest segment) tend to order in groups (high family-size) — group/combo discounts can increase conversion.
- Negative feedback customers are concentrated in lower-income groups — consider affordable meal options.

**🚴 Delivery Performance**
- ~30% of orders exceed the 45-minute threshold — investing in delivery partner availability during peak hours is critical.
- Cities with higher avg delivery times need expanded delivery zones or dark kitchen partnerships.
""")

# ─────────────────────────────────────────────────────────────────────────────
# RAW DATA EXPLORER
# ─────────────────────────────────────────────────────────────────────────────
with st.expander("🔍 Raw Data Explorer", expanded=False):
    display_cols = [
        "Customer ID", "Age", "Gender", "Occupation", "Monthly Income",
        "Customer Type", "Food Category", "Restaurant", "Item Price",
        "Quantity", "Order Value", "Payment Method", "City",
        "Order Date", "Delivery Time (min)", "Customer Rating", "Feedback", "Output",
    ]
    st.dataframe(
        df[display_cols].rename(columns={"Output": "Placed Order"}),
        use_container_width=True,
        height=350,
    )
    st.caption(f"Showing {len(df):,} rows after filters applied.")

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<hr style="border:1px solid #1E293B; margin-top:40px;">
<p style="text-align:center; color:#475569; font-size:12px;">
    Food Delivery Order & Customer Behavior Analysis &nbsp;|&nbsp;
    Built with Python · Pandas · NumPy · Plotly · Streamlit
</p>
""", unsafe_allow_html=True)
