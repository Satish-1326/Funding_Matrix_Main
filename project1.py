import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import pydeck as pdk
from io import StringIO, BytesIO
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# ------------------------------
# 🔐 MYSQL CONNECTION
# ------------------------------
import mysql.connector
import bcrypt

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",  # 🔁 CHANGE THIS
    database="auth_db"
)

cursor = conn.cursor()

# ML fallback imports
try:
    from sklearn.linear_model import LinearRegression
    from sklearn.neighbors import NearestNeighbors  # ✅ ADDED
    from sklearn.preprocessing import StandardScaler  # ✅ ADDED
    SKLEARN_OK = True
except Exception:
    SKLEARN_OK = False

WORDCLOUD_OK = False

st.set_page_config(page_title="Startup Funding — Project 1 (Advanced)", layout="wide")

# --- UI ENHANCEMENT 2: PROFESSIONAL LIGHT THEME CSS ---
CYBER_LIGHT_CSS = """
<style>
/* 1. DEFINE DYNAMIC COLORS BASED ON THEME */
:root {
    --glass-bg: rgba(255, 255, 255, 0.7);
    --glass-border: rgba(255, 255, 255, 0.4);
    --text-main: #1e293b;
    --text-muted: #64748b;
    --accent-primary: #007bff;
    --accent-secondary: #6366f1;
    --metric-bg: #ffffff;
}

/* Dark Mode detection via Streamlit's container data attribute */
[data-theme="dark"] {
    --glass-bg: rgba(15, 23, 42, 0.7);
    --glass-border: rgba(255, 255, 255, 0.1);
    --text-main: #f8fafc;
    --text-muted: #94a3b8;
    --accent-primary: #00f2fe;
    --accent-secondary: #a87ffc;
    --metric-bg: #1e293b;
}

/* 2. GLOBAL STYLES */
[data-testid="stAppViewContainer"] {
    background: transparent !important;
}

/* 3. ADAPTIVE GLASS CARDS */
.section-card {
    background: var(--glass-bg) !important;
    backdrop-filter: blur(12px) saturate(180%);
    -webkit-backdrop-filter: blur(12px) saturate(180%);
    padding: 25px;
    border-radius: 20px;
    border: 1px solid var(--glass-border) !important;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.1);
    margin-bottom: 25px;
    color: var(--text-main);
}

/* 4. DYNAMIC METRIC CARDS */
div[data-testid="stMetric"] {
    background: var(--metric-bg) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 15px !important;
    padding: 15px !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
}
div[data-testid="stMetric"] label p {
    color: var(--text-muted) !important;
}
div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: var(--accent-primary) !important;
}

/* 5. GRADIENT HEADERS */
.header-gradient {
    background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
}

/* 6. SIDEBAR FIX */
[data-testid="stSidebar"] {
    border-right: 1px solid var(--glass-border);
}

/* 7. ADAPTIVE BUTTONS */
.stButton>button {
    background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary)) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    transition: transform 0.2s ease;
}
.stButton>button:hover {
    transform: scale(1.02);
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}

/* 8. TABLE READABILITY */
.stDataFrame {
    background: var(--metric-bg);
    border-radius: 12px;
}

/* 9. CUSTOM SELECTBOX STYLING (For Sidebar Navigation) */
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background-color: var(--metric-bg);
    border-radius: 10px;
    border: 1px solid var(--glass-border);
    color: var(--text-main);
}
[data-testid="stSidebar"] [data-baseweb="select"] span {
    color: var(--text-main);
}
</style>
"""

st.markdown(CYBER_LIGHT_CSS, unsafe_allow_html=True)

# --- decorative main header ---
st.markdown("""
<div class='section-card' style='border-top: 5px solid #007bff;'>
  <div style='display:flex;align-items:center;gap:20px'>
    <div style='flex:1'>
      <div class='header-gradient'>🚀 Startup Funding Matrix </div>
      <div style='color:#64748b; margin-top:10px; font-size: 18px; font-style:italic;'>
        Advanced analytics for your funding dataset. Mode: Professional Light.
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ------------------------------
# Helper functions
# ------------------------------
def standardize_columns(df):
    rename_map = {
        "Startup Name": "startup",
        "Founded Year": "year",
        "Headquarters": "city",
        "Location (Locality)": "locality",
        "Sector/Industry": "sector",
        "Total Funding (INR)": "amount",
        "Round Type": "round_type",
        "Investor/s (Proxy)": "investors"
    }
    df = df.rename(columns={c: c.strip() for c in df.columns})
    rename_map = {k: v for k, v in rename_map.items() if k in df.columns}
    df = df.rename(columns=rename_map)
    return df


def clean_amount_series(s):
    return (
        s.astype(str)
        .str.replace("₹", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.replace("INR", "", regex=False)
        .str.strip()
    )

# ------------------------------
# AUTH FUNCTIONS
# ------------------------------
def create_user(username, password):
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, hashed_pw)
        )
        conn.commit()
        return True
    except:
        return False


def login_user(username, password):
    cursor.execute(
        "SELECT password FROM users WHERE username = %s",
        (username,)
    )
    result = cursor.fetchone()

    if result:
        stored_pw = result[0]
        if bcrypt.checkpw(password.encode(), stored_pw):
            return True
    return False


# ------------------------------
# LOGIN PAGE
# ------------------------------
def login_page():
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if login_user(username, password):
            st.session_state["logged_in"] = True
            st.session_state["user"] = username
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid credentials")


# ------------------------------
# SIGNUP PAGE
# ------------------------------
def signup_page():
    st.title("📝 Sign Up")

    new_user = st.text_input("Create Username")
    new_pass = st.text_input("Create Password", type="password")

    if st.button("Register"):
        if create_user(new_user, new_pass):
            st.success("Account created successfully")
        else:
            st.error("Username already exists")


def df_to_csv_bytes(df):
    return df.to_csv(index=False).encode("utf-8")


def extract_investor_list(df):
    inv_series = (
        df.get("investors", pd.Series([], dtype=str))
        .fillna("")
        .astype(str)
        .str.split(",")
        .explode()
        .str.strip()
    )
    inv_series = inv_series[inv_series != ""]
    return sorted(inv_series.unique())


def safe_contains(series, pat):
    pat_str = str(pat).strip()
    if not pat_str:
        return pd.Series([False] * len(series))

    def check_investors(investor_str):
        if pd.isna(investor_str) or not investor_str:
            return False
        investors = [inv.strip() for inv in investor_str.split(',')]
        return pat_str in investors

    return series.apply(check_investors)


# --- NEW: Coordinate Lookup for Indian Cities ---
def get_coordinates(city_name):
    # Dictionary of Lat/Lon for major Indian startup hubs
    # Format: "CityName": [Longitude, Latitude] (PyDeck uses Lon, Lat)
    coords = {
        "Satara": [ 74.0057, 17.6887],
        "Bengaluru": [77.5946, 12.9716],
        "Bangalore": [77.5946, 12.9716],
        "Mumbai": [72.8777, 19.0760],
        "Delhi": [77.1025, 28.7041],
        "New Delhi": [77.2090, 28.6139],
        "Gurugram": [77.0266, 28.4595],
        "Gurgaon": [77.0266, 28.4595],
        "Noida": [77.3910, 28.5355],
        "Pune": [73.8567, 18.5204],
        "Chennai": [80.2707, 13.0827],
        "Hyderabad": [78.4867, 17.3850],
        "Ahmedabad": [72.5714, 23.0225],
        "Jaipur": [75.7873, 26.9124],
        "Kolkata": [88.3639, 22.5726],
        "Chandigarh": [76.7794, 30.7333],
        "Indore": [75.8577, 22.7196],
        "Goa": [74.1240, 15.2993],
        "Vadodara": [73.1812, 22.3072],
        "Coimbatore": [76.9558, 11.0168],
        "Thiruvananthapuram": [76.9366, 8.5241],
        "Kochi": [76.2711, 9.9312],
        "Surat": [72.8311, 21.1702],
        "Nagpur": [79.0882, 21.1458]
    }
    # Return coords if found, else None
    cleaned_city = str(city_name).split("/")[0].strip()  # Handle cases like "Mumbai/Thane"
    return coords.get(cleaned_city, None)


# ------------------------------
# Load & prepare data
# ------------------------------
@st.cache_data(show_spinner=False)
def load_data(path="project.csv"):
    raw = pd.read_csv(path)
    df = standardize_columns(raw)

    if "amount" in df.columns:
        df["amount"] = clean_amount_series(df["amount"])
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)
    else:
        df["amount"] = 0

    if "year" in df.columns:
        df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    else:
        df["year"] = pd.NA

    df["startup"] = df.get("startup", pd.Series([""] * len(df))).astype(str)
    df["city"] = df.get("city", pd.Series([""] * len(df))).astype(str)
    df["sector"] = df.get("sector", pd.Series([""] * len(df))).astype(str)
    df["investors"] = df.get("investors", pd.Series([""] * len(df))).astype(str)

    df["sector"] = df["sector"].str.title().str.strip()

    def is_valid_sector(s):
        s = str(s).strip()
        if not s:
            return False
        return not s.replace(".", "", 1).isdigit()

    df = df[df["sector"].apply(is_valid_sector)]

    return df


try:
    df = load_data("project.csv")
except Exception as e:
    st.error(f"Could not load project.csv: {e}")
    st.stop()

st.session_state.setdefault("raw_df", df.copy())
st.session_state.setdefault("working_df", df.copy())
working_df = st.session_state["working_df"]

# ------------------------------
# SESSION CONTROL
# ------------------------------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# Show login/signup if not logged in
if not st.session_state["logged_in"]:
    menu = st.sidebar.selectbox("Menu", ["Login", "Sign Up"])

    if menu == "Login":
        login_page()
    else:
        signup_page()

    st.stop()  # ⛔ STOP APP HERE


# ==========================================================
# 🔥 KNN MODEL ADDITION (NEW BLOCK — DOES NOT CHANGE ANYTHING)
# ==========================================================
@st.cache_data
def build_knn_model(df):
    temp_df = df.copy()

    # Encode categorical columns
    temp_df["sector_code"] = temp_df["sector"].astype("category").cat.codes
    temp_df["city_code"] = temp_df["city"].astype("category").cat.codes

    features = temp_df[["amount", "year", "sector_code", "city_code"]].fillna(0)

    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)

    knn = NearestNeighbors(n_neighbors=5)
    knn.fit(features_scaled)

    return knn, scaler, temp_df

knn_model, knn_scaler, knn_df = build_knn_model(working_df)

def get_similar_startups(startup_name):
    try:
        idx = knn_df[knn_df["startup"] == startup_name].index[0]

        features = knn_df[["amount", "year", "sector_code", "city_code"]].fillna(0)
        features_scaled = knn_scaler.transform(features)

        distances, indices = knn_model.kneighbors([features_scaled[idx]])

        return knn_df.iloc[indices[0]]

    except:
        return pd.DataFrame()

# ------------------------------
# Aggregations for business recommendation
# ------------------------------
@st.cache_data
def sector_summary(df):
    s = (
        df.groupby("sector")["amount"]
        .agg(["sum", "mean", "min", "max", "count"])
        .rename(columns={"sum": "total_funding", "mean": "avg_funding", "count": "deals"})
        .reset_index()
    )

    uniq = df.groupby("sector")["startup"].nunique().reset_index()
    uniq = uniq.rename(columns={"startup": "unique_startups"})
    s = s.merge(uniq, on="sector", how="left")

    if "year" in df.columns and df["year"].notna().any():
        years = sorted([int(y) for y in df["year"].dropna().unique()])
        if len(years) >= 2:
            last_year = years[-1]
            recent = (
                df[df["year"] >= last_year - 1]
                .groupby("sector")["amount"]
                .sum()
                .reset_index()
                .rename(columns={"amount": "recent_funding"})
            )
            s = s.merge(recent, on="sector", how="left")
            s["recent_funding"] = s["recent_funding"].fillna(0)
        else:
            s["recent_funding"] = 0
    else:
        s["recent_funding"] = 0

    return s.fillna(0)


@st.cache_data
def sector_city_breakdown(df):
    records = {}
    for sector, grp in df.groupby("sector"):
        by_city = grp.groupby("city")["amount"].sum().reset_index().sort_values("amount", ascending=False)
        records[sector] = by_city
    return records


sector_stats = sector_summary(working_df)
sector_city = sector_city_breakdown(working_df)


# ------------------------------
# Recommendation logic
# ------------------------------
def recommend_businesses(budget, preferred_sector=None, preferred_city=None, top_n=5):
    results = []

    W_fit = 0.45
    W_demand = 0.25
    W_growth = 0.15
    W_competition = 0.15

    for _, row in sector_stats.iterrows():
        sector = row["sector"]
        avg_f = float(row["avg_funding"])
        min_f = float(row["min"])
        max_f = float(row["max"])
        total = float(row["total_funding"])
        unique = float(row["unique_startups"])
        deals = float(row["deals"])
        recent = float(row["recent_funding"])

        if budget <= 0:
            fit_score = 0
        else:
            if avg_f == 0:
                fit_score = 0.2
            else:
                ratio = min(budget / avg_f, 10)
                fit_score = np.tanh(np.log1p(ratio))
                fit_score = float(np.clip(fit_score, 0, 1))

        demand_score = np.tanh(np.log1p(unique + deals))
        growth_score = float(np.clip((recent / total) if total > 0 else 0, 0, 1))
        competition_score = float(np.clip(1 - np.tanh(np.log1p(unique)), 0, 1))

        score = (
                W_fit * fit_score
                + W_demand * demand_score
                + W_growth * growth_score
                + W_competition * competition_score
        )

        city_df = sector_city.get(sector, pd.DataFrame(columns=["city", "amount"]))
        top_cities = city_df.head(5).to_dict(orient="records")

        if preferred_sector and preferred_sector.lower() == sector.lower():
            score *= 1.08

        suggested_min = int(min_f) if min_f > 0 else int(avg_f * 0.5)
        suggested_max = int(max_f) if max_f > 0 else int(avg_f * 1.5)

        results.append({
            "sector": sector,
            "score": float(score),
            "fit_score": float(fit_score),
            "demand_score": float(demand_score),
            "growth_score": float(growth_score),
            "competition_score": float(competition_score),
            "suggested_min": suggested_min,
            "suggested_max": suggested_max,
            "unique_startups": int(unique),
            "deals": int(deals),
            "top_cities": top_cities
        })

    results = [r for r in results if r["sector"].strip() != ""]
    results = sorted(results, key=lambda x: x["score"], reverse=True)
    return results[:top_n], results


# --- Helper for custom colored badges ---
def color_for_page(page_name):
    # Map pages to hex colors for sidebar title styling
    colors = {
        "Overview": "#007bff", "Startups": "#6366f1", "Investors & Analysis": "#2d3436",
        "Sectors": "#d63031", "Geospatial Intelligence": "#00b894",
        "Investor Comparison": "#e17055", "Trends": "#6c5ce7", "Business Recommendation": "#0984e3",
        "Data & Tools": "#636e72"
    }
    return colors.get(page_name, "#007bff")


# ------------------------------
# Linear Regression Prediction Logic
# ------------------------------
@st.cache_data
def get_prediction(data_series, forecast_steps=1):
    """
    Fits a Linear Regression model on yearly time series data and predicts the next value(s).
    data_series should be a pandas Series where index is the year and values are the amount/count.
    """
    if not SKLEARN_OK or len(data_series) < 3:
        # Not enough data for prediction
        return None, None

    # Prepare data: X = years, Y = values
    X = data_series.index.values.reshape(-1, 1)
    Y = data_series.values

    # Train model
    model = LinearRegression()
    model.fit(X, Y)

    # Predict the next 'forecast_steps' years
    last_year = X.max()
    next_X = np.arange(last_year + 1, last_year + 1 + forecast_steps).reshape(-1, 1)

    # Predict values
    predictions = model.predict(next_X)

    # Create prediction Series for easy plotting/use
    predicted_series = pd.Series(predictions, index=next_X.flatten())

    return predicted_series, model.coef_[0]


# ------------------------------
# Sidebar Navigation (MODIFIED: REPLACED RADIO WITH SELECTBOX)
# ------------------------------
page_color = color_for_page(st.session_state.get('page', "Overview"))
st.sidebar.markdown(f"<h1 style='color:{page_color};'>FUNDING MATRIX</h1>",
                    unsafe_allow_html=True)

st.sidebar.write(f"👤 Logged in as: {st.session_state['user']}")

if st.sidebar.button("Logout"):
    st.session_state["logged_in"] = False
    st.session_state["user"] = None
    st.rerun()

if 'page' not in st.session_state:
    st.session_state['page'] = "Overview"

# Create a selectbox for navigation
page_options = [
    "Overview",
    "Startups",
    "Investors & Analysis",
    "Sectors",
    "Geospatial Intelligence",
    "Investor Comparison",
    "Trends",
    "Business Recommendation",
    "Data & Tools"
]

# Ensure the index matches current session state
current_index = 0
if st.session_state['page'] in page_options:
    current_index = page_options.index(st.session_state['page'])

page = st.sidebar.selectbox(
    "Navigate to Module:",
    page_options,
    index=current_index,
    key='page_select'
)

# Update session state
st.session_state['page'] = page

# ------------------------------
# PAGES
# ------------------------------

if page == "Overview":
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:#007bff;'>📊 Ecosystem Overview</h2>", unsafe_allow_html=True)

    total_funding = working_df["amount"].sum()
    total_startups = working_df["startup"].nunique()
    total_deals = len(working_df)
    unique_investors = len(extract_investor_list(working_df))
    sector_count = working_df["sector"].nunique()
    top_sector = working_df.groupby("sector")["amount"].sum().idxmax()

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Funding (INR)", f"₹{int(total_funding):,}")
    col2.metric("Total Startups", total_startups)
    col3.metric("Total Deals", total_deals)
    col4.metric("Unique Investors", unique_investors)
    col5.metric("Total Sectors", sector_count)

    st.metric("Most Funded Sector", top_sector)

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)

    trend_tab, sector_tab = st.tabs(["📈 Funding Trend (YoY)", "🏭 Top Sectors"])

    with trend_tab:
        st.subheader("Funding Growth Over Time (Year-on-Year %)")

        yearly = (
            working_df.groupby("year")
            .sum(numeric_only=True)
            .reset_index()
            .sort_values("year")
            .set_index("year")
        )
        yearly["growth_%"] = yearly["amount"].pct_change() * 100
        yearly.reset_index(inplace=True)

        pred_series, _ = get_prediction(yearly.set_index("year")["amount"], forecast_steps=1)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=yearly['year'],
            y=yearly['amount'],
            mode='lines+markers',
            name='Historical Funding',
            line=dict(color=color_for_page("Trends")),
            marker=dict(size=8, color=color_for_page("Trends"))
        ))

        if pred_series is not None and not pred_series.empty:
            last_year = yearly['year'].max()
            last_amount = yearly['amount'].iloc[-1]
            next_year = pred_series.index[0]
            next_amount = pred_series.iloc[0]

            x_pred = [last_year, next_year]
            y_pred = [last_amount, next_amount]

            fig.add_trace(go.Scatter(
                x=x_pred,
                y=y_pred,
                mode='lines+markers',
                name='Forecast',
                line=dict(color='#d63031', dash='dash'),
                marker=dict(size=8, symbol='star', color='#d63031')
            ))
            st.info(f"🔮 **Forecast for {int(next_year)}:** ₹{int(next_amount):,.0f} (Based on Linear Trend)")

        fig.update_layout(
            title="Total Funding Over Time (INR) with 1-Year Forecast",
            xaxis_title="Year",
            yaxis_title="Total Funding (INR)",
            template="plotly_white",
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
        )

        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(yearly.style.format({'amount': '₹{:,.0f}', 'growth_%': '{:.2f}%'}), use_container_width=True,
                     height=200)

    with sector_tab:
        sec = (
            working_df.groupby("sector")["amount"]
            .sum()
            .reset_index()
            .sort_values("amount", ascending=False)
            .head(15)
        )
        st.subheader("Top 15 Funded Sectors")
        st.plotly_chart(px.bar(sec, x="sector", y="amount", text="amount",
                               template="plotly_white",
                               title="Funding Distribution by Sector"), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


elif page == "Startups":
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:#6366f1;'>🚀 Startup Deep Dive</h2>", unsafe_allow_html=True)
    selected = st.selectbox("Select Startup", sorted(working_df["startup"].unique()))

    data = working_df[working_df["startup"] == selected]

    display_data = data.copy()
    if not display_data.empty and len(display_data) > 1:
        display_data = display_data.iloc[1:]

    st.markdown(f"### Funding Rounds for **{selected}**")
    st.dataframe(display_data, use_container_width=True)

    # (YOUR EXISTING COMPETITOR MAPPING CODE — NO CHANGE)

    if 'fig_comp' in locals():
        st.plotly_chart(fig_comp, use_container_width=True)

    # ==========================================================
    # 🔥 KNN UI ADDITION (ONLY THIS PART NEW)
    # ==========================================================
    st.markdown("<hr style='border-top: 2px solid #e0e0e0; margin: 30px 0;'>", unsafe_allow_html=True)
    st.subheader("🤖 Similar Startups (KNN Based)")

    if st.button("Find Similar Startups"):
        similar_df = get_similar_startups(selected)

        if not similar_df.empty:
            st.dataframe(
                similar_df[["startup", "sector", "city", "amount"]],
                use_container_width=True
            )
        else:
            st.warning("No similar startups found.")
    # ==========================================================

    st.markdown("</div>", unsafe_allow_html=True)

    if "round_type" in display_data.columns and not display_data.empty:
        st.subheader("Funding by Round Type")
        st.plotly_chart(px.bar(display_data, x="round_type", y="amount",
                               template="plotly_white",
                               title=f"Funding Amounts by Round Type for {selected}"), use_container_width=True)

    # --- INTELLIGENT COMPETITOR MAPPING SECTION ---
    st.markdown("<hr style='border-top: 2px solid #e0e0e0; margin: 30px 0;'>", unsafe_allow_html=True)

    # Check if we have sector info to proceed
    if not data.empty:
        sector_val = data["sector"].iloc[0]  # Get the sector of the selected startup

        st.subheader("🎯 Intelligent Competitor Mapping")
        st.markdown(f"Comparing **{selected}** with other startups in the **{sector_val}** sector.")

        # 1. Discover Peers
        peers = working_df[working_df["sector"] == sector_val].groupby("startup")["amount"].sum().reset_index()
        peers = peers.sort_values("amount", ascending=False).reset_index(drop=True)
        peers["Rank"] = peers.index + 1

        # 2. Metrics (Rank, Percentile)
        total_peers = len(peers)
        current_rank_row = peers[peers["startup"] == selected]

        if not current_rank_row.empty:
            current_rank = current_rank_row["Rank"].iloc[0]
            percentile = ((total_peers - current_rank + 1) / total_peers) * 100
        else:
            current_rank = "N/A"
            percentile = 0

        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("Sector Rank", f"#{current_rank} / {total_peers}")
        col_m2.metric("Market Percentile", f"{percentile:.1f}%")
        col_m3.metric("Sector Median Funding", f"₹{int(peers['amount'].median()):,}")

        # 3. Visualization (Bubble Chart)
        sector_landscape = working_df[working_df["sector"] == sector_val].copy()
        # Create a category column for color coding
        sector_landscape["Category"] = sector_landscape["startup"].apply(
            lambda x: "Selected Target" if x == selected else "Competitor"
        )

        # Generate Bubble Chart
        fig_comp = px.scatter(
            sector_landscape,
            x="year",
            y="amount",
            size="amount",
            color="Category",
            hover_name="startup",
            size_max=60,
            title=f"Competitive Landscape: {sector_val} Timeline",
            labels={"amount": "Funding Amount", "year": "Founded/Funded Year"},
            color_discrete_map={"Selected Target": "#ff4b4b", "Competitor": "#007bff"},
            # Red for target, Blue for others
            template="plotly_white"
        )

        st.plotly_chart(fig_comp, use_container_width=True)

        # 4. Peer Table
        with st.expander(f"View Top Competitors in {sector_val}"):
            st.table(peers.head(10).style.format({'amount': '₹{:,.0f}'}))

    st.markdown("</div>", unsafe_allow_html=True)


elif page == "Investors & Analysis":
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:#2d3436;'>💼 Investor Portfolio & Performance</h2>", unsafe_allow_html=True)

    investors = extract_investor_list(working_df)
    investor = st.selectbox("Select Investor for Analysis", ["-- choose --"] + investors)

    if investor != "-- choose --":
        data = working_df[safe_contains(working_df["investors"], investor)]

        st.markdown(f"### Snapshot for **{investor}**")
        col_m1, col_m2 = st.columns(2)
        col_m1.metric("Total Investment", f"₹{data['amount'].sum():,.0f}")
        col_m2.metric("Total Deals", len(data))

        tab_deals, tab_sectors = st.tabs(["🔍 Deal History", "📈 Sector Allocation"])

        with tab_deals:
            st.markdown("#### All Deals by Investor")
            st.dataframe(data, use_container_width=True)

        with tab_sectors:
            sec = data.groupby("sector")["amount"].sum().reset_index()
            st.markdown("#### Sector Allocation")
            st.plotly_chart(px.pie(sec, names="sector", values="amount",
                                   template="plotly_white",
                                   title=f"Sector Allocation for {investor}"), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


elif page == "Sectors":
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:#d63031;'>🏭 Sector Investment Breakdown</h2>", unsafe_allow_html=True)

    clean_sectors = sorted([s for s in working_df["sector"].unique() if s.strip() != ""])
    sector = st.selectbox("Select Sector", ["-- choose --"] + clean_sectors)

    if sector != "-- choose --":
        data = working_df[working_df["sector"] == sector]

        summary = (
            data.groupby("startup")
            .agg(
                total_funding=("amount", "sum"),
                years=("year", lambda x: ", ".join(sorted({str(int(y)) for y in x if pd.notna(y)})))
            )
            .reset_index()
            .sort_values("total_funding", ascending=False)
        )

        col_s1, col_s2, col_s3, col_s4 = st.columns(4)
        col_s1.metric("Total Funding in Sector", f"₹{data['amount'].sum():,.0f}")
        col_s2.metric("Total Startups in Sector", data['startup'].nunique())
        col_s3.metric("Total Deals", len(data))

        # --- SECTOR GROWTH PREDICTION ---
        yearly_sector = data.groupby("year")["amount"].sum()
        pred_series, _ = get_prediction(yearly_sector, forecast_steps=1)

        if pred_series is not None and len(yearly_sector) >= 2:
            current_funding = yearly_sector.iloc[-1]
            predicted_funding = pred_series.iloc[0]

            # Avoid division by zero
            if current_funding > 0:
                predicted_growth_rate = ((predicted_funding - current_funding) / current_funding) * 100
            else:
                predicted_growth_rate = 0

            growth_color = "green" if predicted_growth_rate >= 0 else "red"

            col_s4.markdown(
                f"<div style='border: 1px solid rgba(0,0,0,0.1); border-radius: 8px; padding: 8px;'> "
                f"<p style='color:var(--text-secondary); font-size: 14px; font-weight: 500; margin:0;'>Predicted Growth ({int(pred_series.index[0])})</p>"
                f"<p style='font-weight: 700; font-size: 20px; color:{growth_color}; margin:0;'>"
                f"{predicted_growth_rate:.2f}%"
                f"</p></div>",
                unsafe_allow_html=True
            )
        else:
            col_s4.metric("Predicted Growth", "N/A (Too few years)", delta="Requires >2 years")

        st.markdown(f"### Top Funded Startups in **{sector}**")
        st.dataframe(summary.style.format({'total_funding': '₹{:,.0f}'}), use_container_width=True)
        st.plotly_chart(px.bar(summary.head(10), x="startup", y="total_funding",
                               template="plotly_white",
                               title=f"Top 10 Startups by Funding in {sector}"), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- REPLACED CITIES PAGE WITH GEOSPATIAL INTELLIGENCE ---
elif page == "Geospatial Intelligence":
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:#00b894;'>🗺️ Geospatial Intelligence Hub</h2>", unsafe_allow_html=True)

    st.markdown("""
    Visualize funding density across India using an interactive 3D map. 
    **Tall columns** represent higher funding volume. **Color** represents deal count intensity.
    """)

    # 1. Aggregate Data by City
    city_agg = working_df.groupby("city").agg(
        total_funding=("amount", "sum"),
        deal_count=("startup", "count"),
        top_sector=("sector", lambda x: x.mode()[0] if not x.mode().empty else "Mix")
    ).reset_index()

    # 2. Get Coordinates
    # We apply the helper function to get [lon, lat]
    city_agg["coordinates"] = city_agg["city"].apply(get_coordinates)

    # 3. Filter out cities where coordinates were not found
    map_data = city_agg.dropna(subset=["coordinates"])

    if not map_data.empty:
        # 4. PyDeck Layer Configuration
        layer = pdk.Layer(
            "ColumnLayer",
            data=map_data,
            get_position="coordinates",
            get_elevation="total_funding",
            elevation_scale=50,  # Adjust scale to make bars visible but not overwhelming
            radius=4000,  # Radius of the column in meters
            get_fill_color="[255, 165, 0, 180]",  # Orange base color
            pickable=True,
            auto_highlight=True,
        )

        # 5. Tooltip Configuration
        tooltip = {
            "html": "<b>{city}</b><br/>Funding: ₹{total_funding}<br/>Deals: {deal_count}<br/>Top Sector: {top_sector}",
            "style": {"background": "grey", "color": "white", "font-family": '"Helvetica Neue", Arial',
                      "z-index": "10000"},
        }

        # 6. View State (Centered on India)
        view_state = pdk.ViewState(
            latitude=20.5937,
            longitude=78.9629,
            zoom=4,
            pitch=50,  # Tilt for 3D effect
        )

        # 7. Render Map
        r = pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip=tooltip,
            map_style=pdk.map_styles.DARK,  # Use Dark style for high contrast
        )

        st.pydeck_chart(r)

        # 8. City Stats Table (Below Map)
        st.markdown("### 🏙️ City Performance Metrics")
        st.dataframe(
            map_data[["city", "total_funding", "deal_count", "top_sector"]]
            .sort_values("total_funding", ascending=False)
            .style.format({"total_funding": "₹{:,.0f}"}),
            use_container_width=True
        )
    else:
        st.warning("Could not map city coordinates. Please check city names in dataset.")

    st.markdown("</div>", unsafe_allow_html=True)

elif page == "Investor Comparison":
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:#e17055;'>⚔️ Compare Investor Portfolios</h2>", unsafe_allow_html=True)

    inv_list = extract_investor_list(working_df)

    col_i1, col_i2 = st.columns(2)
    inv1 = col_i1.selectbox("Investor 1", ["-- choose --"] + inv_list)
    inv2 = col_i2.selectbox("Investor 2", ["-- choose --"] + inv_list)

    if inv1 != "-- choose --" and inv2 != "-- choose --":
        df1 = working_df[safe_contains(working_df["investors"], inv1)]
        df2 = working_df[safe_contains(working_df["investors"], inv2)]

        c1, c2 = st.columns(2)
        c1.metric(f"Total Funded by {inv1}", f"₹{df1['amount'].sum():,.0f}")
        c2.metric(f"Total Funded by {inv2}", f"₹{df2['amount'].sum():,.0f}")

        st.markdown("<hr style='border-top: 1px dashed rgba(0,0,0,0.1); margin: 20px 0;'>",
                    unsafe_allow_html=True)

        st.subheader("Sector Investment Comparison")
        sec1 = df1.groupby("sector")["amount"].sum().reset_index()
        sec2 = df2.groupby("sector")["amount"].sum().reset_index()

        colA, colB = st.columns(2)
        colA.markdown(f"#### **{inv1}** Sector Distribution")
        colA.plotly_chart(px.pie(sec1, names="sector", values="amount",
                                 template="plotly_white",
                                 title=inv1), use_container_width=True)

        colB.markdown(f"#### **{inv2}** Sector Distribution")
        colB.plotly_chart(px.pie(sec2, names="sector", values="amount",
                                 template="plotly_white",
                                 title=inv2), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

elif page == "Trends":
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:#6c5ce7;'>📈 Funding Trends over Years</h2>", unsafe_allow_html=True)

    yearly_df = (
        working_df.groupby("year")
        .agg(
            total_funding=("amount", "sum"),
            deal_count=("startup", "count"),
            avg_funding=("amount", "mean"),
        )
        .reset_index()
        .sort_values("year")
    )
    yearly_df.set_index("year", inplace=True)

    yearly_df["growth_%"] = yearly_df["total_funding"].pct_change() * 100

    st.dataframe(yearly_df.style.format({'total_funding': '₹{:,.0f}', 'avg_funding': '₹{:,.0f}'}),
                 use_container_width=True)

    fund_tab, deal_tab, avg_tab = st.tabs(["Total Funding", "Deal Count", "Average Funding"])

    # --- TRENDS PREDICTION ---
    fund_pred_series, _ = get_prediction(yearly_df["total_funding"], forecast_steps=1)
    deal_pred_series, _ = get_prediction(yearly_df["deal_count"], forecast_steps=1)

    with fund_tab:
        st.subheader("Total Funding by Year (with Forecast)")
        fig_fund = go.Figure()
        fig_fund.add_trace(go.Scatter(
            x=yearly_df.index,
            y=yearly_df['total_funding'],
            mode='lines+markers',
            name='Historical Funding',
            line=dict(color='orange'), marker=dict(size=8, color='orange')
        ))

        if fund_pred_series is not None and not fund_pred_series.empty:
            last_year = yearly_df.index.max()
            last_amount = yearly_df['total_funding'].iloc[-1]
            next_year = fund_pred_series.index[0]
            next_amount = fund_pred_series.iloc[0]

            x_pred = [last_year, next_year]
            y_pred = [last_amount, next_amount]

            fig_fund.add_trace(go.Scatter(
                x=x_pred,
                y=y_pred,
                mode='lines+markers',
                name='1-Year Forecast',
                line=dict(color='#d63031', dash='dash'),
                marker=dict(size=8, symbol='star', color='#d63031')
            ))
            st.info(f"🔮 **Total Funding Forecast for {int(next_year)}:** ₹{int(next_amount):,.0f}")

        fig_fund.update_layout(title="Total Funding by Year", template="plotly_white",
                               yaxis_title="Total Funding (INR)")
        st.plotly_chart(fig_fund, use_container_width=True)

    with deal_tab:
        st.subheader("Total Deals by Year (with Forecast)")
        fig_deal = go.Figure()
        fig_deal.add_trace(go.Bar(
            x=yearly_df.index,
            y=yearly_df['deal_count'],
            name='Historical Deals',
            marker_color='#6c5ce7'
        ))

        if deal_pred_series is not None and not deal_pred_series.empty:
            next_year = deal_pred_series.index[0]
            next_count = max(0, int(deal_pred_series.iloc[0]))

            fig_deal.add_trace(go.Bar(
                x=[next_year],
                y=[next_count],
                name='1-Year Forecast',
                marker_color='#d63031',
                opacity=0.7
            ))
            st.info(f"🔮 **Deal Count Forecast for {int(next_year)}:** {next_count} Deals")

        fig_deal.update_layout(title="Total Deals by Year", template="plotly_white", yaxis_title="Deal Count")
        st.plotly_chart(fig_deal, use_container_width=True)

    with avg_tab:
        st.plotly_chart(px.line(yearly_df.reset_index(), x="year", y="avg_funding", markers=True,
                                template="plotly_white",
                                title="Average Funding per Deal by Year"), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


elif page == "Business Recommendation":
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:#0984e3;'>💡 Business Recommendation Engine</h2>", unsafe_allow_html=True)

    with st.expander("🛠 Set Recommendation Parameters", expanded=True):
        col_budget, col_slider = st.columns([1, 2])
        default_budget = int(np.median(working_df["amount"]))
        budget = col_budget.number_input("Available Budget (₹)", min_value=0, value=default_budget, step=10000)
        top_k = col_slider.slider("Number of recommendations", 1, 10, 5)
        preferred_sector = None
        preferred_city = None

        if st.button("🚀 EXECUTE RECOMMENDATION"):
            st.session_state["show_recs"] = True
            st.session_state["recs_params"] = (budget, preferred_sector, preferred_city, top_k)

    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.get("show_recs", False) and "recs_params" in st.session_state:
        budget, preferred_sector, preferred_city, top_k = st.session_state["recs_params"]
        recs, all_recs = recommend_businesses(
            budget=budget,
            preferred_sector=preferred_sector,
            preferred_city=preferred_city,
            top_n=top_k
        )

        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.subheader(f"Top {top_k} Recommendations for Budget ₹{budget:,}")

        out_rows = []

        for i, r in enumerate(recs, start=1):
            st.markdown(
                f"<div style='border: 1px solid #0984e3; border-radius: 12px; padding: 20px; margin-bottom: 20px; background: rgba(9, 132, 227, 0.05);'>",
                unsafe_allow_html=True)

            col_rec1, col_rec2 = st.columns([3, 1])
            col_rec1.markdown(f"#### {i}. <span style='color:#0984e3;'>{r['sector']}</span>", unsafe_allow_html=True)
            col_rec1.markdown(
                f"<p style='color:var(--text-secondary);'>Suggested Funding Range: <span style='font-weight:700; color:#0984e3;'>₹{r['suggested_min']:,} — ₹{r['suggested_max']:,}</span></p>",
                unsafe_allow_html=True)
            col_rec1.markdown(
                f"<p style='font-size:12px; color:var(--text-secondary);'>Deals: {r['deals']} | Unique Startups: {r['unique_startups']}</p>",
                unsafe_allow_html=True)

            col_rec2.markdown(
                f"<h3 style='margin:0; border-left: none; color:#0984e3;'>Score: **{r['score']:.3f}**</h3>",
                unsafe_allow_html=True)

            with st.expander(f"Details & Top Cities for {r['sector']}"):
                score_cols = st.columns(4)
                score_cols[0].metric("Funding Fit", f"{r['fit_score']:.3f}")
                score_cols[1].metric("Market Demand", f"{r['demand_score']:.3f}")
                score_cols[2].metric("Growth Potential", f"{r['growth_score']:.3f}")
                score_cols[3].metric("Competition", f"{r['competition_score']:.3f}")

                if r["top_cities"]:
                    st.subheader("Top Investment Hubs")
                    df_city = pd.DataFrame(r["top_cities"])
                    df_city["amount"] = df_city["amount"].apply(lambda x: f"₹{int(x):,}")
                    st.table(df_city)

            st.markdown("</div>", unsafe_allow_html=True)

            out_rows.append({
                "rank": i,
                "sector": r["sector"],
                "score": r["score"],
                "suggested_min": r['suggested_min'],
                "suggested_max": r['suggested_max'],
            })

        export_df = pd.DataFrame(out_rows)
        st.download_button("Download Recommendations CSV", df_to_csv_bytes(export_df), "business_recommendations.csv")
        st.markdown("</div>", unsafe_allow_html=True)


elif page == "Data & Tools":
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:#636e72;'>🛠 Data Management & Utilities</h2>", unsafe_allow_html=True)

    preview_tab, analyzer_tab, filter_tab, export_tab = st.tabs(
        ["Preview Data", "Column Analyzer", "Data Filter", "Export CSV"])

    with preview_tab:
        st.subheader("Full Dataset Preview")
        st.dataframe(working_df, use_container_width=True)

    with analyzer_tab:
        col = st.selectbox("Choose Column to Analyze", working_df.columns)
        st.write("### Column Info")
        col_type, col_unique = st.columns(2)
        col_type.write(f"**Data Type:** `<span style='color:#0984e3;'>{working_df[col].dtype}</span>`",
                       unsafe_allow_html=True)
        col_unique.write(f"**Unique Values:** `<span style='color:#0984e3;'>{working_df[col].nunique()}</span>`",
                         unsafe_allow_html=True)

        st.subheader(f"Value Counts for {col}")
        vc = working_df[col].value_counts().reset_index()
        if len(vc.columns) >= 2:
            vc.columns = [col, "Count"]
        st.dataframe(vc, use_container_width=True)

    with filter_tab:
        start_list = ["All"] + sorted(working_df["startup"].dropna().unique())
        city_list = ["All"] + sorted(working_df["city"].dropna().unique())
        sec_list = ["All"] + sorted(working_df["sector"].dropna().unique())

        c1, c2, c3 = st.columns(3)

        s_start = c1.selectbox("Filter by Startup", start_list)
        s_city = c2.selectbox("Filter by City", city_list)
        s_sec = c3.selectbox("Filter by Sector", sec_list)

        min_amt = int(working_df["amount"].min())
        max_amt = int(working_df["amount"].max())

        amt_range = st.slider("Funding Range (INR)", min_amt, max_amt, (min_amt, max_amt))

        filtered = working_df.copy()
        if s_start != "All":
            filtered = filtered[filtered["startup"] == s_start]
        if s_city != "All":
            filtered = filtered[filtered["city"] == s_city]
        if s_sec != "All":
            filtered = filtered[filtered["sector"] == s_sec]

        filtered = filtered[(filtered["amount"] >= amt_range[0]) & (filtered["amount"] <= amt_range[1])]

        st.subheader(f"Filtered Data ({len(filtered)} rows)")
        st.dataframe(filtered, use_container_width=True)
        st.download_button("Download Filtered CSV", df_to_csv_bytes(filtered), "filtered_data.csv")

    with export_tab:
        st.subheader("Export Cleaned Dataset")
        st.write("Download the full, cleaned dataset (after normalization of sectors and numeric values).")
        st.download_button("Download Cleaned CSV", df_to_csv_bytes(working_df), "cleaned_project.csv")

    st.markdown("</div>", unsafe_allow_html=True)