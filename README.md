<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=28&pause=1000&color=F97316&center=true&vCenter=true&width=700&lines=🍔+Food+Delivery+Analytics;Order+%26+Customer+Behavior+Analysis" alt="Typing SVG" />

<br/>

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-3.0-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-2.5-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-7.1-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.64-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

<br/>

> **A college-level Data Analytics project** that explores online food delivery ordering patterns and customer behavior through an interactive Streamlit dashboard with 25 Plotly visualizations.

</div>

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Live Dashboard Preview](#-live-dashboard-preview)
- [Dataset](#-dataset)https://www.kaggle.com/datasets/srisyra02/online-food-ordering-dataset
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [Dashboard Features](#-dashboard-features)
- [Key Findings](#-key-findings)
- [Tech Stack](#-tech-stack)
- [Business Insights](#-business-insights)

---

## 🔍 Overview

This project performs end-to-end data analysis on a real-world online food delivery survey dataset of **388 respondents** from Bangalore, India. Since the original dataset is a customer survey (no transactional records), the pipeline **enriches it** with deterministically simulated order-level fields — food category, restaurant, item price, quantity, payment method, order date, and delivery time — using a **fixed random seed (42)** for full reproducibility.

The result is a production-quality analytics dashboard that answers:
- 🛒 Who is ordering, and how much are they spending?
- 🍽️ Which food categories and restaurants generate the most revenue?
- 🚴 How is delivery performance, and where are the bottlenecks?
- 💡 What actionable steps can improve the business?

---

## 🖥️ Live Dashboard Preview

| Section | Highlights |
|---------|-----------|
| 📈 **Orders & Revenue** | Monthly trend, revenue by category, city breakdown, payment methods |
| 🍽️ **Food & Restaurants** | Popular items, top restaurants, price analysis, heatmap |
| 👤 **Customer Behavior** | Customer types, top spenders, ratings, feedback, age scatter |
| 🚴 **Delivery Performance** | Delivery time histogram, on-time vs delayed, city & category breakdown |
| 📊 **Demographics** | Age groups, gender, occupation, income, marital status |

**KPIs shown on every page:**

| 📦 Total Orders | 💰 Total Revenue | 👥 Total Customers | 🧾 Avg Order Value | 🚴 Avg Delivery Time | ⭐ Avg Rating |
|:-:|:-:|:-:|:-:|:-:|:-:|
| 217 | ₹1,04,950 | 285 | ₹484 | 43.4 min | 4.10 ★ |

---

## 📂 Dataset

**Source:** `online food delivery dataset.csv` — customer survey (388 rows, 13 columns)

| Column | Type | Description |
|--------|------|-------------|
| `Age` | Integer | Customer age (18–33) |
| `Gender` | Categorical | Male / Female |
| `Marital Status` | Categorical | Single / Married / Prefer not to say |
| `Occupation` | Categorical | Student / Employee / Self Employed / House wife |
| `Monthly Income` | Categorical | No Income → More than ₹50,000 |
| `Educational Qualifications` | Categorical | School → Ph.D |
| `Family size` | Integer | 1–6 members |
| `Customer Type` | Categorical | **New / Regular / Frequent** |
| `latitude` / `longitude` | Float | Bangalore geo-coordinates |
| `Pin code` | Integer | 560001 – 560109 |
| `Output` | Binary | Whether order was placed (Yes/No → 1/0) |
| `Feedback` | Categorical | Positive / Negative |

**Engineered / Simulated Fields** added by `analysis.py`:

| Field | Method |
|-------|--------|
| `Food Category` | Weighted random from 10 categories |
| `Restaurant` | Category-specific pool of 15 restaurants |
| `Item Price` | Uniform random within category price range |
| `Quantity` | Random 1–4, +1 bonus if Family size ≥ 4 |
| **`Order Value`** | **`Quantity × Item Price`** ← key feature |
| `Payment Method` | Weighted (UPI 38%, COD 28%, Card 27%, Net Banking 7%) |
| `City` | Pin code prefix → Bangalore; others from 8 Indian cities |
| `Order Date` | Random day in 2024 (Jan–Dec) |
| `Delivery Time` | Base 25–55 min + delay for high-value orders |
| `Customer Rating` | 1–5 stars, correlated with Feedback |

---

## 📁 Project Structure

```
📦 Data Analytics/
├── 📄 online food delivery dataset.csv     ← Source dataset
│
└── 📁 food_delivery_analysis/
    ├── 🐍 analysis.py          ← Data pipeline: load → clean → enrich → aggregate
    ├── 🎛️  app.py               ← Streamlit dashboard (25 charts, 6 KPIs, 6 filters)
    ├── 📋 requirements.txt     ← Python dependencies
    └── 📖 README.md            ← You are here
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- pip package manager

### 1 — Clone the repository
```bash
git clone https://github.com/your-username/food-delivery-analytics.git
cd food-delivery-analytics
```

### 2 — Install dependencies
```bash
pip install -r food_delivery_analysis/requirements.txt
```

### 3 — Run the dashboard
```bash
cd food_delivery_analysis
streamlit run app.py
```

### 4 — Open in browser
```
http://localhost:8501
```

> 💡 The dashboard loads in ~5 seconds on first run. Keep the terminal open while using it.

---

## 📊 Dashboard Features

### 🎛️ Interactive Sidebar Filters
All charts and KPIs update **live** when you change any filter:

| Filter | Options |
|--------|---------|
| 📅 Order Date Range | Jan 2024 – Dec 2024 (slider) |
| 🍽️ Food Category | Biryani, Pizza, Burger, South Indian, Chinese, North Indian, Desserts, Beverages, Sandwich, Rolls |
| 🏙️ City | Bangalore, Mumbai, Delhi, Hyderabad, Chennai, Pune, Kolkata, Ahmedabad |
| 👤 Customer Type | New, Regular, Frequent |
| 🏪 Restaurant | 15 restaurants |
| 💳 Payment Method | UPI, Cash on Delivery, Credit Card, Debit Card, Net Banking |

### 📈 Charts & Visualizations (25 total)

<details>
<summary><b>📈 Tab 1 — Orders & Revenue</b></summary>

- **Monthly Orders & Revenue Trend** — Dual-axis bar + line chart
- **Revenue by Food Category** — Donut pie chart
- **Revenue & Orders by City** — Colour-graded bar chart
- **Payment Method Distribution** — Horizontal bar + donut pie

</details>

<details>
<summary><b>🍽️ Tab 2 — Food & Restaurants</b></summary>

- **Most Popular Food Categories** — Horizontal bar (by quantity ordered)
- **Average Item Price by Category** — Grouped bar chart
- **Top Restaurants — Revenue & Rating** — Dual-axis bar + line
- **Food Category × Payment Method** — Heatmap

</details>

<details>
<summary><b>👤 Tab 3 — Customer Behavior</b></summary>

- **Customer Type — Order Count** — Bar chart
- **Average Spend by Customer Type** — Bar chart
- **Top 10 Highest-Spending Customers** — Colour-graded bar
- **Feedback by Customer Type** — Grouped bar
- **Customer Rating Distribution** — Bar chart
- **Order Value vs Customer Age** — Bubble scatter plot

</details>

<details>
<summary><b>🚴 Tab 4 — Delivery Performance</b></summary>

- **Delivery Time Distribution** — Histogram with threshold markers
- **On-Time vs Delayed Orders** — Donut pie (45-min threshold)
- **Average Delivery Time by City** — Colour-graded bar
- **Delivery Time by Food Category** — Box plot

</details>

<details>
<summary><b>📊 Tab 5 — Demographics</b></summary>

- **Orders by Age Group** — Bar chart
- **Gender Distribution** — Donut pie
- **Orders & Avg Spend by Occupation** — Horizontal bar
- **Order Count by Monthly Income** — Bar chart
- **Average Spend by Monthly Income** — Bar chart
- **Order Placement by Marital Status** — Stacked bar

</details>

---

## 🔑 Key Findings

```
📦  76% of surveyed customers placed an order
💰  Biryani, Pizza & North Indian = highest revenue categories
💳  UPI is used in 38% of all transactions
👤  Frequent customers generate the highest average order value
🎓  Students (20–24) are the dominant ordering demographic
🚴  ~30% of orders exceed the 45-minute delivery threshold
⭐  76% of ordering customers gave Positive feedback
```

---

## 💡 Business Insights

| # | Insight | Recommendation |
|---|---------|---------------|
| 1 | Frequent customers = highest AOV | Launch a loyalty/rewards programme |
| 2 | UPI dominates payments | Enable one-tap UPI checkout |
| 3 | Students order for large families | Introduce group/combo meal deals |
| 4 | Biryani & Pizza drive most revenue | Run category-specific promotions |
| 5 | 30% orders are delayed | Deploy more riders during peak hours (12–2 PM, 7–10 PM) |
| 6 | High-rated restaurants have low orders | Boost visibility through featured listings |
| 7 | Negative feedback in low-income segment | Create a budget meal category (under ₹100) |

---

## 🛠️ Tech Stack

| Library | Version | Purpose |
|---------|---------|---------|
| ![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white&style=flat) **Python** | 3.12.10 | Core language |
| ![Pandas](https://img.shields.io/badge/-Pandas-150458?logo=pandas&logoColor=white&style=flat) **Pandas** | 3.0.6 | Data loading, cleaning, aggregation |
| ![NumPy](https://img.shields.io/badge/-NumPy-013243?logo=numpy&logoColor=white&style=flat) **NumPy** | 2.5.3 | Numerical operations, reproducible simulation |
| ![Plotly](https://img.shields.io/badge/-Plotly-3F4F75?logo=plotly&logoColor=white&style=flat) **Plotly** | 7.1.0 | 25 interactive charts |
| ![Streamlit](https://img.shields.io/badge/-Streamlit-FF4B4B?logo=streamlit&logoColor=white&style=flat) **Streamlit** | 1.64.0 | Web dashboard framework |

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---

<div align="center">

Made with ❤️ for a Data Analytics college project

⭐ **Star this repo if you found it helpful!**

</div>
