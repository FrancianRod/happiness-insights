"""
World Happiness Report 2019 - Complete Analysis Script
========================================================
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ─────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────
df = pd.read_csv("2019.csv")

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

# 2a. Remove leading and trailing whitespaces from string columns
df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)
print("✔ Leading/trailing whitespaces removed from string columns.")

# 2b. Replace empty strings with NaN
df = df.apply(lambda col: col.replace("", np.nan) if col.dtype == "object" else col)
print("✔ Empty strings replaced with NaN.")

# 2c. Convert columns to appropriate types
#     — detect automatically based on actual column names present
numeric_cols = [
    col for col in df.columns
    if col not in ["Country or region"]
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# String columns
for col in ["Country or region"]:
    if col in df.columns:
        df[col] = df[col].astype("string")

# Rank as nullable integer
if "Overall rank" in df.columns:
    df["Overall rank"] = df["Overall rank"].astype("Int64")

print("\nUpdated Data Types:")
print(df.dtypes)


# ══════════════════════════════════════════════
# STEP 3 — HANDLE MISSING VALUES
# ══════════════════════════════════════════════
print("\n" + "=" * 60)
print("STEP 3: Missing Values")
print("=" * 60)

missing = df.isnull().sum()
missing_cols = missing[missing > 0]

if missing_cols.empty:
    print("No missing values found in the dataset.")
else:
    print("Columns with missing values:")
    print(missing_cols)
    for col in missing_cols.index:
        if pd.api.types.is_numeric_dtype(df[col]):
            col_mean = df[col].mean()
            df[col] = df[col].fillna(col_mean)
            print(f"  ✔ '{col}' — {missing_cols[col]} NaN(s) replaced with mean ({col_mean:.4f})")

print("\nMissing values after imputation:", df.isnull().sum().sum())


# ══════════════════════════════════════════════
# STEP 4 — FIG1: TOP 10 COUNTRIES BAR CHART
# ══════════════════════════════════════════════
print("\n" + "=" * 60)
print("STEP 4: fig1 — Top 10 Countries Bar Chart")
print("=" * 60)

top10 = df.nsmallest(10, "Overall rank")[
    ["Country or region", "GDP per capita", "Healthy life expectancy"]
].reset_index(drop=True)

fig1 = go.Figure()

fig1.add_trace(go.Bar(
    name="GDP per Capita",
    x=top10["Country or region"],
    y=top10["GDP per capita"],
    marker_color="#2ecc71",
    text=top10["GDP per capita"].round(3),
    textposition="outside",
))

fig1.add_trace(go.Bar(
    name="Healthy Life Expectancy",
    x=top10["Country or region"],
    y=top10["Healthy life expectancy"],
    marker_color="#3498db",
    text=top10["Healthy life expectancy"].round(3),
    textposition="outside",
))

fig1.update_layout(
    title="GDP per Capita & Healthy Life Expectancy — Top 10 Happiest Countries (2019)",
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
    "GDP per capita",
    "Social support",
    "Healthy life expectancy",
    "Freedom to make life choices",
    "Perceptions of corruption",
    "Generosity",
    "Score",
]

corr_matrix = df[sub_cols].corr().round(2)

fig2 = go.Figure(data=go.Heatmap(
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
))

fig2.update_layout(
    title="Correlation Heatmap — Happiness Factors (2019)",
    width=800,
    height=600,
    template="plotly_white",
    xaxis=dict(tickangle=-30),
)

fig2.show()
print("✔ fig2 created.")


# ══════════════════════════════════════════════
# STEP 6 — FIG3: SCATTER PLOT
# Note: 2019 dataset has no Region column.
# We create income tiers from GDP per capita as a proxy.
# ══════════════════════════════════════════════
print("\n" + "=" * 60)
print("STEP 6: fig3 — Scatter Plot")
print("=" * 60)

# Create GDP tier grouping as Region substitute
df["GDP Tier"] = pd.cut(
    df["GDP per capita"],
    bins=[0, 0.6, 1.0, 1.3, float("inf")],
    labels=["Low GDP", "Lower-Middle GDP", "Upper-Middle GDP", "High GDP"],
)

fig3 = px.scatter(
    df,
    x="GDP per capita",
    y="Score",
    color="GDP Tier",
    hover_name="Country or region",
    title="Effect of GDP per Capita on Happiness Score (2019)",
    labels={"Score": "Happiness Score", "GDP per capita": "GDP per Capita"},
    opacity=0.85,
    template="plotly_white",
    height=550,
)

fig3.update_traces(marker=dict(size=10, line=dict(width=0.5, color="white")))
fig3.show()
print("✔ fig3 created.")


# ══════════════════════════════════════════════
# STEP 7 — FIG4: PIE CHART BY GDP TIER
# ══════════════════════════════════════════════
print("\n" + "=" * 60)
print("STEP 7: fig4 — Pie Chart")
print("=" * 60)

tier_happiness = (
    df.groupby("GDP Tier", as_index=False, observed=True)["Score"]
    .mean()
    .sort_values("Score", ascending=False)
)

fig4 = px.pie(
    tier_happiness,
    names="GDP Tier",
    values="Score",
    title="Average Happiness Score by GDP Tier (2019)",
    hole=0.35,
    template="plotly_white",
    color_discrete_sequence=px.colors.qualitative.Set2,
)

fig4.update_traces(
    textposition="inside",
    textinfo="percent+label",
    hovertemplate="<b>%{label}</b><br>Avg Happiness: %{value:.3f}<extra></extra>",
)

fig4.update_layout(height=520)
fig4.show()
print("✔ fig4 created.")


# ══════════════════════════════════════════════
# STEP 8 — FIG5: CHOROPLETH MAP
# ══════════════════════════════════════════════
print("\n" + "=" * 60)
print("STEP 8: fig5 — Choropleth Map")
print("=" * 60)

fig5 = px.choropleth(
    df,
    locations="Country or region",
    locationmode="country names",
    color="GDP per capita",
    hover_name="Country or region",
    hover_data={
        "Healthy life expectancy": ":.3f",
        "GDP per capita": ":.3f",
    },
    color_continuous_scale="Viridis",
    title="GDP per Capita by Country — with Healthy Life Expectancy Tooltip (2019)",
    labels={
        "GDP per capita": "GDP per Capita",
        "Healthy life expectancy": "Healthy Life Expectancy",
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
║          WORLD HAPPINESS REPORT 2019 — DASHBOARD NARRATIVE              ║
╚══════════════════════════════════════════════════════════════════════════╝

OVERVIEW
--------
The 2019 World Happiness Report ranks 156 countries by happiness score,
built from six factors: GDP per Capita, Social Support, Healthy Life
Expectancy, Freedom to Make Life Choices, Generosity, and Perceptions
of Corruption. Unlike 2016, this edition does not include a Region column,
so GDP Tiers were used as a geographic-economic proxy for grouping.

──────────────────────────────────────────────────────────────────────────
CHART 1 — CORRELATION HEATMAP (fig2)
──────────────────────────────────────────────────────────────────────────
GDP per Capita, Social Support, and Healthy Life Expectancy show the
strongest positive correlations with Happiness Score (≈ 0.79, 0.78, 0.77).
Freedom to Make Life Choices also contributes meaningfully (~0.57).
Generosity and Perceptions of Corruption have weaker relationships,
suggesting happiness is primarily driven by material and social security
rather than civic virtue alone.

──────────────────────────────────────────────────────────────────────────
CHART 2 — SCATTER PLOT: GDP vs HAPPINESS SCORE (fig3)
──────────────────────────────────────────────────────────────────────────
The scatter plot confirms a clear upward trend: higher GDP per Capita
consistently links to higher Happiness Scores. High GDP tier countries
(e.g. Finland, Denmark, Norway) cluster in the upper right. Low GDP
tier countries occupy the lower left. The spread within each tier shows
that income alone is not destiny — some countries outperform their GDP
bracket thanks to strong social support and freedoms.

──────────────────────────────────────────────────────────────────────────
CHART 3 — PIE CHART: HAPPINESS SCORE BY GDP TIER (fig4)
──────────────────────────────────────────────────────────────────────────
High GDP tier nations hold the largest share of average happiness, while
Low GDP tier nations contribute the smallest slice. The gap between tiers
is substantial, reinforcing that economic development remains the most
powerful lever for national well-being in 2019.

──────────────────────────────────────────────────────────────────────────
CHART 4 — WORLD MAP: GDP PER CAPITA (with Life Expectancy Tooltip) (fig5)
──────────────────────────────────────────────────────────────────────────
The map reveals sharp geographic inequality. Northern/Western Europe and
North America glow brightest (highest GDP). Sub-Saharan Africa and parts
of South Asia remain the darkest zones. Hovering over any country surfaces
its Healthy Life Expectancy — which mirrors the GDP map almost exactly,
confirming that wealth and health reinforce each other globally.

──────────────────────────────────────────────────────────────────────────
KEY TAKEAWAYS
──────────────────────────────────────────────────────────────────────────
1. GDP per Capita remains the #1 predictor of happiness in 2019.
2. Social Support is nearly as important — community safety nets matter.
3. Healthy Life Expectancy compounds with GDP: rich nations live longer.
4. Freedom is a meaningful happiness factor beyond pure economics.
5. Geographic inequality in happiness persists and is deeply structural.
"""

print(narrative)
