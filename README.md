# 🍔 Food Delivery Order & Customer Behavior Analysis

A college-level Data Analytics project built with **Python, Pandas, NumPy, Plotly,** and **Streamlit**.

---

## 📁 Project Structure

```
food_delivery_analysis/
├── app.py               ← Streamlit dashboard (run this)
├── analysis.py          ← Data loading, cleaning, enrichment & aggregations
├── requirements.txt     ← Python dependencies
└── README.md            ← This file

online food delivery dataset.csv   ← Source dataset (place in parent folder)
```

---

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the dashboard
```bash
cd food_delivery_analysis
streamlit run app.py
```
The dashboard opens automatically at `http://localhost:8501`.

---

## 📊 What's Inside

### Data Pipeline (`analysis.py`)
| Step | What happens |
|------|-------------|
| **Load** | Reads `online food delivery dataset.csv` with Pandas |
| **Clean** | Strips whitespace, removes duplicates, fills missing values, standardises binary columns |
| **Enrich** | Adds simulated order-level fields (Food Category, Restaurant, Item Price, Quantity, Payment Method, Order Date, Delivery Time, Customer Rating) using a fixed random seed for reproducibility |
| **Feature Engineering** | Computes **Order Value = Quantity × Item Price**; derives Month, Age Group |
| **Aggregations** | KPIs, monthly trends, category/restaurant/customer/city summaries, delivery performance |

### Dashboard Tabs (`app.py`)
| Tab | Visualizations |
|-----|---------------|
| 📈 **Orders & Revenue** | Monthly trend (bar + line), Revenue by category (donut), Orders by city, Payment method distribution |
| 🍽️ **Food & Restaurants** | Most popular categories, Avg price per category, Top restaurants (revenue + rating), Category × Payment heatmap |
| 👤 **Customer Behavior** | Customer type counts + avg spend, Top spending customers, Feedback breakdown, Rating distribution, Order value vs Age scatter |
| 🚴 **Delivery Performance** | Delivery time histogram, On-time vs Delayed donut, Avg delivery by city, Box plot by category |
| 📊 **Demographics** | Age group analysis, Gender distribution, Occupation analysis, Income analysis, Marital status order placement |

### KPIs Displayed
- Total Orders · Total Revenue · Total Customers
- Average Order Value · Average Delivery Time · Average Customer Rating

### Interactive Filters (Sidebar)
- 📅 Date Range
- 🍽️ Food Category
- 🏙️ City
- 👤 Customer Type
- 🏪 Restaurant
- 💳 Payment Method

---

## 🔑 Key Business Insights
1. **Biryani, Pizza, North Indian** generate the most revenue — prioritise these in promotions.
2. **UPI** is the dominant payment method — smooth UPI checkout reduces cart abandonment.
3. **Frequent customers** have the highest average order value — a loyalty programme can increase retention.
4. **Students** are the largest segment and tend to order in groups — bundle/combo deals improve conversion.
5. ~30% of orders exceed the 45-min delivery target — more delivery partners during peak hours is essential.
6. Restaurants with high ratings but lower revenue need targeted marketing support.

---

## 🛠️ Tech Stack
| Library | Version | Purpose |
|---------|---------|---------|
| Python | 3.9+ | Core language |
| Pandas | 2.x | Data loading, cleaning, aggregation |
| NumPy | 1.24+ | Numerical operations, simulation |
| Plotly | 5.x | Interactive charts & graphs |
| Streamlit | 1.31+ | Dashboard & web app framework |
