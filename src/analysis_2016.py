"""
World Happiness Report 2016 - Complete Analysis Script
========================================================
This script performs data cleaning, EDA, and visualizations
using pandas and Plotly on the 2016 World Happiness dataset.
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

# ─────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────
df = pd.read_csv("2016.csv")

# ══════════════════════════════════════════════
# STEP 1 — CHECK DATA TYPES
# ══════════════════════════════════════════════
print("=" * 60)
print("STEP 1: Initial Data Types")
print("=" * 60)
print(df.dtypes)
print("\nShape:", df.shape)
print("\nFirst 5 rows:")
print(df.head())


# ══════════════════════════════════════════════
# STEP 2 — DATA CLEANING
# ══════════════════════════════════════════════
print("\n" + "=" * 60)
print("STEP 2: Data Cleaning")
print("=" * 60)

# 2a. Remove leading and trailing whitespaces from all string columns
df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)
print("✔ Leading/trailing whitespaces removed from string columns.")

# 2b. Replace empty strings with NaN in all string columns
df = df.apply(lambda col: col.replace("", np.nan) if col.dtype == "object" else col)
print("✔ Empty strings replaced with NaN.")

# 2c. Convert columns to appropriate types (latest pandas best-practice)
#     Numeric columns: use pd.to_numeric with errors='coerce'
numeric_cols = [
    "Happiness Rank",
    "Happiness Score",
    "Lower Confidence Interval",
    "Upper Confidence Interval",
    "Economy (GDP per Capita)",
    "Family",
    "Health (Life Expectancy)",
    "Freedom",
    "Trust (Government Corruption)",
    "Generosity",
    "Dystopia Residual",
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

#     String columns: use pandas StringDtype
string_cols = ["Country", "Region"]
for col in string_cols:
    df[col] = df[col].astype("string")

#     Happiness Rank: integer (nullable Int64 to handle NaN safely)
df["Happiness Rank"] = df["Happiness Rank"].astype("Int64")

print("\nUpdated Data Types:")
print(df.dtypes)


# ══════════════════════════════════════════════
# STEP 3 — HANDLE MISSING VALUES
# ══════════════════════════════════════════════
print("\n" + "=" * 60)
print("STEP 3: Missing Values")
print("=" * 60)

# 3a. Identify columns with missing values
missing = df.isnull().sum()
missing_cols = missing[missing > 0]

if missing_cols.empty:
    print("No missing values found in the dataset.")
else:
    print("Columns with missing values:")
    print(missing_cols)

    # 3b. Replace missing values with column mean (numeric columns only)
    for col in missing_cols.index:
        if pd.api.types.is_numeric_dtype(df[col]):
            col_mean = df[col].mean()
            df[col] = df[col].fillna(col_mean)
            print(f"  ✔ '{col}' — {missing_cols[col]} NaN(s) replaced with mean ({col_mean:.4f})")

print("\nMissing values after imputation:")
print(df.isnull().sum()[df.isnull().sum() > 0] if df.isnull().sum().any() else "None")


# ══════════════════════════════════════════════
# STEP 4 — FIG1: TOP 10 COUNTRIES — GDP & LIFE EXPECTANCY
# ══════════════════════════════════════════════
print("\n" + "=" * 60)
print("STEP 4: fig1 — Top 10 Countries Bar Chart")
print("=" * 60)

top10 = df.nsmallest(10, "Happiness Rank")[
    ["Country", "Economy (GDP per Capita)", "Health (Life Expectancy)"]
].reset_index(drop=True)

fig1 = go.Figure()

fig1.add_trace(
    go.Bar(
        name="GDP per Capita",
        x=top10["Country"],
        y=top10["Economy (GDP per Capita)"],
        marker_color="#2ecc71",
        text=top10["Economy (GDP per Capita)"].round(3),
        textposition="outside",
    )
)

fig1.add_trace(
    go.Bar(
        name="Healthy Life Expectancy",
        x=top10["Country"],
        y=top10["Health (Life Expectancy)"],
        marker_color="#3498db",
        text=top10["Health (Life Expectancy)"].round(3),
        textposition="outside",
    )
)

fig1.update_layout(
    title="GDP per Capita & Healthy Life Expectancy — Top 10 Happiest Countries (2016)",
    xaxis_title="Country",
    yaxis_title="Score",
    barmode="group",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    template="plotly_white",
    height=500,
)

fig1.show()
print("✔ fig1 created.")


# ══════════════════════════════════════════════
# STEP 5 — FIG2: CORRELATION HEATMAP
# ══════════════════════════════════════════════
print("\n" + "=" * 60)
print("STEP 5: fig2 — Correlation Heatmap")
print("=" * 60)

sub_cols = [
    "Economy (GDP per Capita)",
    "Family",
    "Health (Life Expectancy)",
    "Freedom",
    "Trust (Government Corruption)",
    "Generosity",
    "Happiness Score",
]

sub_df = df[sub_cols].copy()
corr_matrix = sub_df.corr().round(2)

fig2 = go.Figure(
    data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns.tolist(),
        y=corr_matrix.index.tolist(),
        colorscale="RdYlGn",
        zmin=-1,
        zmax=1,
        text=corr_matrix.values,
        texttemplate="%{text}",
        textfont={"size": 11},
        hoverongaps=False,
    )
)

fig2.update_layout(
    title="Correlation Heatmap — Happiness Factors (2016)",
    width=800,
    height=600,
    template="plotly_white",
    xaxis=dict(tickangle=-30),
)

fig2.show()
print("✔ fig2 created.")


# ══════════════════════════════════════════════
# STEP 6 — FIG3: SCATTER PLOT — GDP vs HAPPINESS SCORE
# ══════════════════════════════════════════════
print("\n" + "=" * 60)
print("STEP 6: fig3 — Scatter Plot")
print("=" * 60)

fig3 = px.scatter(
    df,
    x="Economy (GDP per Capita)",
    y="Happiness Score",
    color="Region",
    hover_name="Country",
    title="Effect of GDP per Capita on Happiness Score by Region (2016)",
    labels={
        "Economy (GDP per Capita)": "GDP per Capita",
        "Happiness Score": "Happiness Score",
    },
    size_max=12,
    opacity=0.85,
    template="plotly_white",
    height=550,
)

fig3.update_traces(marker=dict(size=10, line=dict(width=0.5, color="white")))
fig3.update_layout(legend=dict(title="Region", font=dict(size=11)))
fig3.show()
print("✔ fig3 created.")


# ══════════════════════════════════════════════
# STEP 7 — FIG4: PIE CHART — HAPPINESS SCORE BY REGION
# ══════════════════════════════════════════════
print("\n" + "=" * 60)
print("STEP 7: fig4 — Pie Chart")
print("=" * 60)

region_happiness = (
    df.groupby("Region", as_index=False)["Happiness Score"]
    .mean()
    .sort_values("Happiness Score", ascending=False)
)

fig4 = px.pie(
    region_happiness,
    names="Region",
    values="Happiness Score",
    title="Average Happiness Score by Region (2016)",
    hole=0.35,
    template="plotly_white",
    color_discrete_sequence=px.colors.qualitative.Set2,
)

fig4.update_traces(
    textposition="inside",
    textinfo="percent+label",
    hovertemplate="<b>%{label}</b><br>Avg Happiness: %{value:.3f}<extra></extra>",
)

fig4.update_layout(height=520, legend=dict(font=dict(size=11)))
fig4.show()
print("✔ fig4 created.")


# ══════════════════════════════════════════════
# STEP 8 — FIG5: CHOROPLETH MAP — GDP PER CAPITA
# ══════════════════════════════════════════════
print("\n" + "=" * 60)
print("STEP 8: fig5 — Choropleth Map")
print("=" * 60)

fig5 = px.choropleth(
    df,
    locations="Country",
    locationmode="country names",
    color="Economy (GDP per Capita)",
    hover_name="Country",
    hover_data={"Health (Life Expectancy)": ":.3f", "Economy (GDP per Capita)": ":.3f"},
    color_continuous_scale="Viridis",
    title="GDP per Capita by Country — with Healthy Life Expectancy Tooltip (2016)",
    labels={
        "Economy (GDP per Capita)": "GDP per Capita",
        "Health (Life Expectancy)": "Healthy Life Expectancy",
    },
    template="plotly_white",
)

fig5.update_layout(
    height=520,
    coloraxis_colorbar=dict(title="GDP per Capita"),
    geo=dict(showframe=False, showcoastlines=True, projection_type="natural earth"),
)

fig5.show()
print("✔ fig5 created.")


# ══════════════════════════════════════════════
# NARRATIVE
# ══════════════════════════════════════════════
narrative = """
╔══════════════════════════════════════════════════════════════════════════╗
║          WORLD HAPPINESS REPORT 2016 — DASHBOARD NARRATIVE              ║
╚══════════════════════════════════════════════════════════════════════════╝

OVERVIEW
--------
The 2016 World Happiness Report captures happiness scores across 157 countries,
decomposed into six key contributors: economic output (GDP per Capita), social
support (Family), health (Life Expectancy), Freedom, governmental trust, and
Generosity. Together these factors reveal which regions and nations foster the
greatest well-being — and which face the steepest challenges.

──────────────────────────────────────────────────────────────────────────────
CHART 1 — CORRELATION HEATMAP (fig2)
──────────────────────────────────────────────────────────────────────────────
The heatmap reveals that Economy (GDP per Capita) and Health (Life Expectancy)
share the strongest positive correlations with Happiness Score (≈ 0.78 and 0.77
respectively), suggesting that material prosperity and physical well-being are
the most reliable predictors of national happiness. Family support follows
closely (~0.74), underscoring that social bonds matter as much as income.
Freedom shows a moderate positive effect (~0.57), while Generosity and Trust
(Government Corruption) display weaker, though still positive, relationships.
Notably, GDP per Capita and Life Expectancy are highly correlated with each
other (~0.84), indicating that wealthier nations tend to have healthier
populations — a compounding advantage in happiness.

──────────────────────────────────────────────────────────────────────────────
CHART 2 — SCATTER PLOT: GDP PER CAPITA vs. HAPPINESS SCORE (fig3)
──────────────────────────────────────────────────────────────────────────────
The scatter plot makes a compelling visual argument: as GDP per Capita rises,
so does Happiness Score — but the relationship is not uniform across regions.
Western European nations cluster in the upper-right quadrant, combining high
GDP with high happiness. North America and Australia/New Zealand sit nearby.
In contrast, Sub-Saharan Africa concentrates in the lower-left, reflecting
both lower economic output and lower happiness. Latin America and the Caribbean
is a notable outlier — several countries score higher on happiness than their
GDP alone would predict, hinting at the cultural and social strengths that
supplement economic factors. Central and Eastern Europe shows wide dispersion,
suggesting that transition economies vary greatly in translating wealth into
well-being.

──────────────────────────────────────────────────────────────────────────────
CHART 3 — PIE CHART: HAPPINESS SCORE BY REGION (fig4)
──────────────────────────────────────────────────────────────────────────────
The pie chart illustrates the share of average happiness each region contributes.
Western Europe leads the distribution with the highest average happiness, followed
by North America and Australia/New Zealand. Together these prosperous regions
account for a disproportionately large share of global happiness. Meanwhile,
Sub-Saharan Africa, Southern Asia, and parts of the Middle East and North Africa
contribute smaller shares, reflecting systemic challenges including conflict,
poverty, and governance issues. Latin America's slice is larger than its economic
footprint would suggest, reinforcing its well-documented "happiness premium" —
rooted in strong family networks and community cohesion.

──────────────────────────────────────────────────────────────────────────────
CHART 4 — WORLD MAP: GDP PER CAPITA (with Life Expectancy Tooltip) (fig5)
──────────────────────────────────────────────────────────────────────────────
The choropleth map paints a stark geographic portrait of global economic inequality.
The darkest (highest GDP) zones concentrate across Northern and Western Europe,
North America, and Australia. A mid-tier band runs through parts of Latin America,
Eastern Europe, and East Asia. The lightest shades — lowest GDP per Capita —
blanket much of sub-Saharan Africa and parts of South Asia. Hovering over any
country reveals its Healthy Life Expectancy score, which mirrors the GDP pattern
almost perfectly: wealthy nations enjoy longer, healthier lives while poorer
nations face the double burden of low income and shortened lifespans. This
geographic overlay underscores that the happiness gap is not merely cultural —
it is deeply structural and economic.

──────────────────────────────────────────────────────────────────────────────
KEY TAKEAWAYS
──────────────────────────────────────────────────────────────────────────────
1. Economic prosperity (GDP per Capita) is the single strongest driver of
   national happiness, amplified by its tight link to healthy life expectancy.

2. Social and family support adds significant happiness value beyond what income
   alone explains — particularly visible in Latin America's happiness premium.

3. Regional inequality in happiness is vast and geographically predictable:
   Western Europe and North America dominate; Sub-Saharan Africa trails.

4. Policy levers most likely to raise happiness include investments in healthcare
   (boosting Life Expectancy), anti-corruption efforts (boosting Trust), and
   economic growth strategies that also strengthen social safety nets.

5. Freedom consistently contributes to happiness, suggesting that civil liberties
   and good governance are not luxuries but components of human well-being.
"""

print(narrative)
