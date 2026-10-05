import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from difflib import get_close_matches
from pathlib import Path

# ============================================================
# TANGY STITCH — RETAIL INTELLIGENCE SYSTEM
# ============================================================

st.set_page_config(
    page_title="Tangy Stitch | Retail Intelligence",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------- Palette ---------------------------
CREAM = "#F5F0E8"
PAPER = "#FFFDF9"
INK = "#174D42"
INK_DARK = "#0F3D34"
ROSE = "#B8736B"
ROSE_DARK = "#89534D"
ROSE_PALE = "#EBD7D2"
SAGE = "#A8B8A7"
SAGE_PALE = "#DDE7DD"
OCHRE = "#B48A4A"
STONE = "#D9D0C4"
STONE_DARK = "#625F59"
CHARCOAL = "#343633"
GRID = "#DDD5CA"
WHITE = "#FFFFFF"

FONT_SERIF = "Georgia, 'Times New Roman', serif"
FONT_SANS = "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"

# ------------------------- CSS -------------------------------
st.markdown(
    f"""
<style>
:root {{
    --cream:{CREAM}; --paper:{PAPER}; --ink:{INK}; --ink-dark:{INK_DARK};
    --rose:{ROSE}; --stone:{STONE}; --charcoal:{CHARCOAL};
}}

html, body {{
    font-family:{FONT_SANS};
}}
[data-testid="stIconMaterial"] {{
    font-family: "Material Symbols Rounded" !important;
    font-style: normal !important;
    font-weight: normal !important;
}}
.stApp {{ background:{CREAM} !important; color:{CHARCOAL} !important; }}
header[data-testid="stHeader"] {{ background:{CREAM} !important; border-bottom:1px solid {STONE} !important; }}
.block-container {{ max-width:1500px; padding:2.0rem 2.8rem 4rem 2.8rem; }}

/* Main typography */
h1, h2, h3 {{
    color:{INK} !important;
    font-family:{FONT_SERIF} !important;
    font-weight:600 !important;
}}
h1 {{ font-size:48px !important; letter-spacing:-1.8px; line-height:1.05 !important; }}
h2 {{ font-size:31px !important; letter-spacing:-.6px; margin-top:0 !important; }}
h3 {{ font-size:22px !important; }}
p, label, .stCaption {{ color:{CHARCOAL} !important; }}

/* Sidebar */
section[data-testid="stSidebar"] {{ background:{INK_DARK} !important; border-right:0 !important; }}
section[data-testid="stSidebar"] > div {{ padding:0.8rem 1.15rem 1.5rem 1.15rem; justify-content:flex-start !important; }}
section[data-testid="stSidebar"] * {{ font-family:{FONT_SANS}; }}
section[data-testid="stSidebar"] .brand-name {{ color:#F8F3EA !important; font-family:{FONT_SERIF} !important; font-size:27px; font-weight:600; margin-top:-6px; }}
section[data-testid="stSidebar"] .sidebar-logo {{ width:40px; height:70px; margin:0 0 1px 0; padding:0; display:block; overflow:hidden; line-height:0; }}
section[data-testid="stSidebar"] .sidebar-logo img {{ display:block; width:40px; height:auto; max-height:70px; object-fit:contain; object-position:left top; pointer-events:none; user-select:none; }}
section[data-testid="stSidebar"] .brand-name {{ color:#F8F3EA !important; font-family:{FONT_SERIF} !important; font-size:27px; font-weight:600; margin-top:0 !important; line-height:1.05 !important; }}
section[data-testid="stSidebar"] .brand-sub {{ color:#C9D5D0 !important; font-size:10px; letter-spacing:2.2px; margin-top:5px; }}
section[data-testid="stSidebar"] hr {{ border-color:rgba(255,255,255,.18) !important; }}
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{ color:#F8F3EA !important; }}
section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {{ color:#BFCBC6 !important; }}
section[data-testid="stSidebar"] .nav-heading {{
    color:#F8F3EA !important; font-size:13px; font-weight:700;
    margin:0 0 10px 2px; letter-spacing:.2px;
}}
section[data-testid="stSidebar"] .ts-nav {{ display:flex; flex-direction:column; gap:3px; }}
section[data-testid="stSidebar"] .ts-nav-link {{
    display:flex; align-items:center; gap:10px; padding:9px 8px;
    border-radius:7px; text-decoration:none !important;
    color:#F8F3EA !important; background:transparent;
    font-size:15px; line-height:1.2;
}}
section[data-testid="stSidebar"] .ts-nav-link:hover {{
    background:rgba(255,255,255,.07); color:#F8F3EA !important;
}}
section[data-testid="stSidebar"] .ts-nav-link.active {{
    background:rgba(255,255,255,.10);
}}
section[data-testid="stSidebar"] .ts-nav-dot {{
    width:14px; height:14px; border:1.5px solid rgba(255,255,255,.35);
    border-radius:50%; flex:0 0 14px; box-sizing:border-box;
}}
section[data-testid="stSidebar"] .ts-nav-link.active .ts-nav-dot {{
    background:#FF6B63; border-color:#FF6B63;
    box-shadow:inset 0 0 0 3px #F8F3EA;
}}

/* Inputs */
div[data-baseweb="select"] > div {{
    background:{PAPER} !important; border:1px solid {STONE} !important; border-radius:7px !important;
}}
div[data-baseweb="select"] span, div[data-baseweb="select"] input, div[data-baseweb="select"] div {{ color:{CHARCOAL} !important; }}
[data-testid="stSelectbox"] label, [data-testid="stSlider"] label, [data-testid="stNumberInput"] label {{
    color:{STONE_DARK} !important; font-size:12px !important; font-weight:600 !important;
}}
[data-testid="stSlider"] [data-baseweb="slider"] {{ padding-top:8px; }}
.stSlider [data-baseweb="slider"] [role="slider"] {{ background:{ROSE} !important; border-color:{ROSE} !important; }}
.stSlider [data-baseweb="slider"] > div > div > div {{ background:{ROSE} !important; }}

/* Metrics */
div[data-testid="stMetric"] {{
    background:{PAPER} !important; border:1px solid {STONE} !important; border-radius:9px !important;
    padding:17px 19px !important; box-shadow:none !important;
}}
div[data-testid="stMetricLabel"] p {{ color:{STONE_DARK} !important; font-size:10px !important; text-transform:uppercase; letter-spacing:1.25px; }}
div[data-testid="stMetricValue"] {{ color:{INK} !important; font-family:{FONT_SERIF} !important; font-size:31px !important; }}

/* Editorial */
.eyebrow {{ color:{ROSE}; font-size:10px; font-weight:800; letter-spacing:2.5px; text-transform:uppercase; margin-bottom:7px; }}
.subline {{ color:{STONE_DARK}; font-size:14px; margin-top:-12px; margin-bottom:26px; }}
.section-head {{ margin-top:12px; margin-bottom:10px; }}
.section-title {{ color:{INK}; font-family:{FONT_SERIF}; font-size:27px; font-weight:600; line-height:1.1; }}
.section-sub {{ color:{STONE_DARK}; font-size:12px; margin-top:4px; }}
.kicker {{ display:inline-block; color:{ROSE}; font-size:9px; font-weight:800; letter-spacing:2px; text-transform:uppercase; margin-bottom:5px; }}

/* Cards that contain only HTML content */
.info-card {{
    background:{PAPER}; border:1px solid {STONE}; border-radius:9px; padding:16px 18px;
}}
.info-title {{ color:{INK}; font-family:{FONT_SERIF}; font-size:21px; font-weight:600; margin-bottom:3px; }}
.info-copy {{ color:{STONE_DARK}; font-size:11px; line-height:1.5; }}

.badge {{ display:inline-block; padding:5px 9px; border-radius:999px; font-size:9px; font-weight:800; letter-spacing:1.1px; text-transform:uppercase; }}
.badge-real {{ background:{SAGE_PALE}; color:{INK}; }}
.badge-demo {{ background:{ROSE_PALE}; color:{ROSE_DARK}; }}

.callout {{ border-radius:8px; padding:12px 14px; font-size:11px; line-height:1.55; }}
.callout-real {{ background:{SAGE_PALE}; border:1px solid #C5D4C3; color:{INK}; }}
.callout-demo {{ background:#F0DDD9; border:1px solid #DFC2BD; color:#744B47; }}

.insight {{ background:{PAPER}; border:1px solid {STONE}; border-left:3px solid {ROSE}; border-radius:8px; padding:14px 16px; }}
.insight-label {{ color:{ROSE}; font-size:9px; font-weight:800; letter-spacing:1.5px; text-transform:uppercase; }}
.insight-title {{ color:{INK}; font-family:{FONT_SERIF}; font-size:19px; margin-top:4px; }}
.insight-copy {{ color:{STONE_DARK}; font-size:11px; line-height:1.5; margin-top:3px; }}

/* Real HTML table. Never use Streamlit dataframe styling. */
.clean-table {{ width:100%; border-collapse:collapse; background:{PAPER}; border:1px solid {STONE}; border-radius:8px; overflow:hidden; font-size:12px; }}
.clean-table th {{ text-align:left; padding:11px 13px; background:#EEE8DE; color:{INK}; font-weight:700; border-bottom:1px solid {STONE}; }}
.clean-table td {{ padding:10px 13px; color:{CHARCOAL}; border-bottom:1px solid #E6DED3; }}
.clean-table tr:last-child td {{ border-bottom:0; }}
.clean-table td.num {{ text-align:right; font-variant-numeric:tabular-nums; }}

/* Remove accidental Streamlit dataframe/table visuals if any remain. */
div[data-testid="stDataFrame"] {{ display:none !important; }}

/* Plotly: never recolour SVG text from CSS. */
.js-plotly-plot .modebar {{ opacity:0 !important; }}
.js-plotly-plot:hover .modebar {{ opacity:.35 !important; }}

/* System rail */
.system-rail {{ display:flex; align-items:center; gap:0; margin:18px 0 28px 0; padding:0; }}
.system-node {{ position:relative; flex:0 0 auto; min-width:132px; padding:12px 15px 11px 15px; background:{PAPER}; border:1px solid {STONE}; border-radius:8px; opacity:0; transform:translateY(7px); animation:railIn .55s ease-out forwards; }}
.system-node:nth-child(1) {{ animation-delay:.05s; }}
.system-node:nth-child(3) {{ animation-delay:.18s; }}
.system-node:nth-child(5) {{ animation-delay:.31s; }}
.system-node:nth-child(7) {{ animation-delay:.44s; }}
.system-node:nth-child(9) {{ animation-delay:.57s; }}
.system-node .node-index {{ color:{ROSE}; font-size:8px; font-weight:800; letter-spacing:1.5px; }}
.system-node .node-name {{ color:{INK}; font-family:{FONT_SERIF}; font-size:16px; margin-top:3px; }}
.system-node .node-copy {{ color:{STONE_DARK}; font-size:9px; margin-top:3px; }}
.system-link {{ height:1px; flex:1 1 28px; min-width:18px; background:{STONE}; position:relative; overflow:hidden; }}
.system-link:after {{ content:""; position:absolute; left:-30%; top:0; width:30%; height:1px; background:{ROSE}; animation:railDraw .75s ease-out forwards; }}
.system-link:nth-child(2):after {{ animation-delay:.12s; }}
.system-link:nth-child(4):after {{ animation-delay:.25s; }}
.system-link:nth-child(6):after {{ animation-delay:.38s; }}
.system-link:nth-child(8):after {{ animation-delay:.51s; }}
@keyframes railIn {{ to {{ opacity:1; transform:translateY(0); }} }}
@keyframes railDraw {{ to {{ left:100%; }} }}
.explorer {{ background:{PAPER}; border:1px solid {STONE}; border-radius:9px; padding:18px 20px; }}
.explorer-label {{ color:{ROSE}; font-size:9px; font-weight:800; letter-spacing:1.7px; text-transform:uppercase; }}
.explorer-title {{ color:{INK}; font-family:{FONT_SERIF}; font-size:23px; margin-top:3px; }}
.explorer-copy {{ color:{STONE_DARK}; font-size:11px; line-height:1.5; margin-top:3px; }}
.explorer-stat {{ border-top:1px solid {STONE}; margin-top:12px; padding-top:11px; }}
.explorer-stat-label {{ color:{STONE_DARK}; font-size:9px; text-transform:uppercase; letter-spacing:1px; }}
.explorer-stat-value {{ color:{INK}; font-family:{FONT_SERIF}; font-size:19px; margin-top:2px; }}
.status-pill {{ display:inline-block; margin-top:10px; padding:5px 8px; border-radius:999px; font-size:8px; font-weight:800; letter-spacing:1px; text-transform:uppercase; }}
.status-ok {{ background:{SAGE_PALE}; color:{INK}; }}
.status-watch {{ background:{ROSE_PALE}; color:{ROSE_DARK}; }}
.footer {{ color:{STONE_DARK}; font-size:10px; letter-spacing:.2px; padding-top:4px; }}

/* Mobile refinement */
@media (max-width: 768px) {{
    .block-container {{ padding: 1.15rem 1rem 2.5rem 1rem !important; }}
    h1 {{ font-size: 34px !important; letter-spacing:-1px; }}
    h2 {{ font-size: 25px !important; }}
    h3 {{ font-size: 19px !important; }}
    .subline {{ font-size: 12px; margin-bottom: 18px; }}
    .system-rail {{ overflow-x:auto; padding-bottom:8px; }}
    .system-node {{ min-width:118px; }}
    .system-link {{ min-width:12px; }}
    div[data-testid="stMetric"] {{ padding:12px 13px !important; }}
    div[data-testid="stMetricValue"] {{ font-size:24px !important; }}
    div[data-testid="stMetricLabel"] p {{ font-size:9px !important; }}
    .section-title {{ font-size:23px; }}
    .section-sub {{ font-size:11px; }}
    .clean-table {{ font-size:10px; }}
    .clean-table th, .clean-table td {{ padding:8px 9px; }}
}}

</style>
""",
    unsafe_allow_html=True,
)

# ============================================================
# DATA
# ============================================================

FILE = "tangy_stitch_data.xlsx"

@st.cache_data
def load_data(path):
    sheets = {
        "fabric": "Fabric Inventory",
        "trims": "Trims and Accessories",
        "consumption": "Consumption",
        "costing": "Product Costing",
        "designs": "Design Tracker",
        "suppliers": "Suppliers",
    }
    data = {k: pd.read_excel(path, sheet_name=v) for k, v in sheets.items()}
    for df in data.values():
        df.columns = df.columns.astype(str).str.strip()
    return data

try:
    data = load_data(FILE)
except Exception as exc:
    st.error(f"Could not load {FILE}. Keep the Excel file beside app.py.\n\n{exc}")
    st.stop()

fabric = data["fabric"].copy()
trims = data["trims"].copy()
consumption = data["consumption"].copy()
costing = data["costing"].copy()
designs = data["designs"].copy()
suppliers = data["suppliers"].copy()

# Numeric cleaning
for c in ["Price per Meter", "Discount %", "Net Price/m", "Meters Purchased", "Current Stock", "Minimum Stock", "Inventory Value"]:
    if c in fabric.columns:
        fabric[c] = pd.to_numeric(fabric[c], errors="coerce")
for c in ["Cost per Piece/m  (₹)", "Price per Unit", "Quantity Purchased", "Current Stock", "Inventory Value"]:
    if c in trims.columns:
        trims[c] = pd.to_numeric(trims[c], errors="coerce")
for c in ["Qty Produced", "Fabric Used (m)"]:
    if c in consumption.columns:
        consumption[c] = pd.to_numeric(consumption[c], errors="coerce")
for c in ["Fabric Cost", "Stitching", "Trims/ Lace/ Embroidery", "Packaging", "Total Cost", "Selling Price", "Profit", "Margin %"]:
    if c in costing.columns:
        costing[c] = pd.to_numeric(costing[c], errors="coerce")

fabric["Fabric ID Clean"] = fabric["Fabric ID"].astype(str).str.strip()
fabric["Fabric Name Clean"] = fabric["Fabric Name"].fillna("Unnamed fabric").astype(str).str.strip()
fabric["Fabric Category Clean"] = fabric["Fabric Category"].fillna("Uncategorised").astype(str).str.strip().str.replace(r"\s+", " ", regex=True)
fabric["Colour Clean"] = fabric["Colour"].fillna("—").astype(str).str.strip()
consumption["Fabric ID Clean"] = consumption["Fabric ID"].astype(str).str.strip()
consumption["Product Clean"] = consumption["Product"].fillna("Unknown product").astype(str).str.strip()
costing["Product Name Clean"] = costing["Product Name"].fillna("Unnamed product").astype(str).str.strip()

usage = consumption.groupby("Fabric ID Clean", as_index=False).agg(
    Fabric_Used_m=("Fabric Used (m)", "sum"),
    Units_Produced=("Qty Produced", "sum"),
    Products_Using_Fabric=("Product Clean", "nunique"),
)
material = fabric.merge(usage, on="Fabric ID Clean", how="left")
for c in ["Fabric_Used_m", "Units_Produced", "Products_Using_Fabric"]:
    material[c] = material[c].fillna(0)
material["Utilisation %"] = np.where(
    material["Meters Purchased"].fillna(0) > 0,
    material["Fabric_Used_m"] / material["Meters Purchased"] * 100,
    0,
)
material["Remaining m"] = (material["Meters Purchased"] - material["Fabric_Used_m"]).clip(lower=0)

fabric_value = float(fabric["Inventory Value"].sum())
trims_value = float(trims["Inventory Value"].sum())
total_purchased = float(material["Meters Purchased"].sum())
total_used = float(material["Fabric_Used_m"].sum())
overall_utilisation = total_used / total_purchased * 100 if total_purchased else 0

# Material → product relationship table used by the Collection relationship explorer
# and the recorded-relationships section. Build it once before any page renders.
flow = consumption.merge(
    fabric[["Fabric ID Clean", "Fabric Name Clean"]],
    on="Fabric ID Clean",
    how="left",
)
flow = flow.dropna(subset=["Fabric Name Clean", "Product Clean", "Fabric Used (m)"]).copy()
flow = (
    flow.groupby(["Fabric Name Clean", "Product Clean"], as_index=False)["Fabric Used (m)"]
    .sum()
)
flow = flow[flow["Fabric Used (m)"] > 0].copy()

# ============================================================
# HELPERS
# ============================================================

def money(v):
    if pd.isna(v):
        return "—"
    return f"₹{float(v):,.0f}"


def normalise(s):
    return "".join(ch.lower() for ch in str(s) if ch.isalnum())


def find_consumption_name(product_name):
    target = normalise(product_name)
    names = consumption["Product Clean"].dropna().unique().tolist()
    norm_map = {normalise(x): x for x in names}
    if target in norm_map:
        return norm_map[target]
    for n, original in norm_map.items():
        if target in n or n in target:
            return original
    matches = get_close_matches(target, list(norm_map.keys()), n=1, cutoff=0.55)
    return norm_map[matches[0]] if matches else None


def unit_fabric_for_product(product_name):
    match = find_consumption_name(product_name)
    if not match:
        return None
    rows = consumption[consumption["Product Clean"] == match]
    units = rows["Qty Produced"].sum()
    used = rows["Fabric Used (m)"].sum()
    return used / units if units and used else None


def primary_fabric_for_product(product_name):
    match = find_consumption_name(product_name)
    if not match:
        return None
    rows = consumption[consumption["Product Clean"] == match].copy()
    if rows.empty:
        return None
    primary_id = rows.groupby("Fabric ID Clean")["Fabric Used (m)"].sum().idxmax()
    fm = fabric[fabric["Fabric ID Clean"] == primary_id]
    return fm.iloc[0] if not fm.empty else None


def chart(fig, height=380, legend=False, margins=None):
    """One styling function for every Plotly chart. All text is explicitly dark."""
    if margins is None:
        margins = dict(l=60, r=30, t=24, b=52)
    fig.update_layout(
        template="simple_white",
        height=height,
        paper_bgcolor=PAPER,
        plot_bgcolor=PAPER,
        font=dict(family=FONT_SANS, color=CHARCOAL, size=11),
        margin=margins,
        showlegend=legend,
        hoverlabel=dict(bgcolor=INK_DARK, font=dict(color=WHITE, family=FONT_SANS, size=11)),
        dragmode=False,
    )
    fig.update_xaxes(
        showline=False,
        zeroline=False,
        showgrid=False,
        gridcolor=GRID,
        gridwidth=1,
        tickfont=dict(color=CHARCOAL, size=11),
        title_font=dict(color=INK_DARK, size=12, family=FONT_SANS),
    )
    fig.update_yaxes(
        showline=False,
        zeroline=False,
        gridcolor=GRID,
        gridwidth=1,
        tickfont=dict(color=CHARCOAL, size=11),
        title_font=dict(color=INK_DARK, size=12, family=FONT_SANS),
        automargin=True,
    )
    return fig


def section(title, subtitle=None, kicker=None):
    k = f'<div class="kicker">{kicker}</div>' if kicker else ""
    s = f'<div class="section-head">{k}<div class="section-title">{title}</div>'
    if subtitle:
        s += f'<div class="section-sub">{subtitle}</div>'
    s += '</div>'
    st.markdown(s, unsafe_allow_html=True)


def callout(kind, title, text):
    cls = "callout-real" if kind == "real" else "callout-demo"
    st.markdown(f'<div class="callout {cls}"><b>{title}</b> {text}</div>', unsafe_allow_html=True)


def badge(kind, text):
    cls = "badge-real" if kind == "real" else "badge-demo"
    st.markdown(f'<span class="badge {cls}">{text}</span>', unsafe_allow_html=True)


def insight(label, title, copy):
    st.markdown(
        f'<div class="insight"><div class="insight-label">{label}</div>'
        f'<div class="insight-title">{title}</div><div class="insight-copy">{copy}</div></div>',
        unsafe_allow_html=True,
    )


def system_rail():
    html = f"""
    <div class="system-rail">
        <div class="system-node"><div class="node-index">01</div><div class="node-name">Collection</div><div class="node-copy">Products &amp; assortment</div></div>
        <div class="system-link"></div>
        <div class="system-node"><div class="node-index">02</div><div class="node-name">Materials</div><div class="node-copy">Inventory &amp; usage</div></div>
        <div class="system-link"></div>
        <div class="system-node"><div class="node-index">03</div><div class="node-name">Economics</div><div class="node-copy">Cost &amp; structure</div></div>
        <div class="system-link"></div>
        <div class="system-node"><div class="node-index">04</div><div class="node-name">Forecast</div><div class="node-copy">Demand signal</div></div>
        <div class="system-link"></div>
        <div class="system-node"><div class="node-index">05</div><div class="node-name">Decision</div><div class="node-copy">Plan &amp; test</div></div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def html_table(df, columns, formats=None):
    formats = formats or {}
    headers = "".join(f"<th>{c}</th>" for c in columns)
    rows = []
    for _, r in df.iterrows():
        cells = []
        for c in columns:
            v = r[c]
            if c in formats:
                v = formats[c](v)
            is_num = isinstance(v, str) and (v.startswith("₹") or v.endswith("%") or v.replace(".", "", 1).replace("-", "", 1).isdigit())
            cells.append(f'<td class="{"num" if is_num else ""}">{v}</td>')
        rows.append("<tr>" + "".join(cells) + "</tr>")
    st.markdown(
        '<table class="clean-table"><thead><tr>' + headers + '</tr></thead><tbody>' + ''.join(rows) + '</tbody></table>',
        unsafe_allow_html=True,
    )


# ============================================================
# DEMO FORECASTING
# ============================================================

@st.cache_data
def make_demo_demand(product_name):
    seed = sum(ord(c) for c in product_name) % 997
    rng = np.random.default_rng(seed)
    dates = pd.date_range("2026-01-01", periods=10, freq="MS")
    base = 3 + (seed % 4)
    trend = np.linspace(0, 1.2 + (seed % 3) * 0.25, len(dates))
    season = np.array([0.4, -0.3, 0.5, 1.0, -0.7, -0.1, 0.4, 1.0, 0.7, 1.2])
    noise = rng.normal(0, 0.35, len(dates))
    demand = np.maximum(0, np.rint(base + trend + season + noise)).astype(int)
    return pd.DataFrame({"Month": dates, "Units": demand})


def forecast_series(history, horizon, model):
    y = history["Units"].astype(float).to_numpy()
    n = len(y)
    if model == "Moving average":
        window = min(3, n)
        pred = np.repeat(float(np.mean(y[-window:])), horizon)
    elif model == "Linear trend":
        x = np.arange(n)
        coef = np.polyfit(x, y, 1)
        future_x = np.arange(n, n + horizon)
        pred = np.maximum(np.polyval(coef, future_x), 0)
    else:
        alpha = 0.45
        level = y[0]
        trend = 0.0
        for value in y[1:]:
            prev = level
            level = alpha * value + (1 - alpha) * (level + trend)
            trend = 0.35 * (level - prev) + 0.65 * trend
        pred = np.maximum(level + np.arange(1, horizon + 1) * trend, 0)
    return pred


# ------------------------------------------------------------
# Illustrative retail sales layer
# ------------------------------------------------------------
# The workbook does not contain order-level sales, returns, sizes or
# colour-level sell-through history. These deterministic demo records
# let the retail analytics layer demonstrate the calculations without
# presenting simulated values as historical Tangy Stitch performance.
product_names = costing["Product Name Clean"].dropna().tolist()
_demo_rows = []
_sizes = ["XS", "S", "M", "L", "XL"]
_size_factor = {"XS": 0.70, "S": 0.90, "M": 1.18, "L": 1.12, "XL": 0.78}

for i, product_name in enumerate(product_names):
    crow = costing[costing["Product Name Clean"] == product_name].iloc[0]
    base_received = 24 + (i % 5) * 6
    # Costing cells can be blank/NaN in the public demo workbook. Treat
    # missing values as unavailable rather than allowing NaN to propagate
    # into the illustrative sales calculations.
    cost_raw = pd.to_numeric(pd.Series([crow.get("Total Cost", 0)]), errors="coerce").iloc[0]
    sell_raw = pd.to_numeric(pd.Series([crow.get("Selling Price", 0)]), errors="coerce").iloc[0]
    cost = float(cost_raw) if pd.notna(cost_raw) else 0.0
    sell_price = float(sell_raw) if pd.notna(sell_raw) else 0.0

    # Deterministic variation creates a useful demo range while keeping
    # the dataset stable across runs and deployments.
    base_str = 0.42 + ((i * 7) % 27) / 100
    if sell_price > 0 and np.isfinite(sell_price) and np.isfinite(cost):
        margin_signal = (sell_price - cost) / sell_price
        if np.isfinite(margin_signal):
            base_str += min(max(margin_signal, 0), 0.18)
    base_str = float(np.clip(base_str, 0.38, 0.78))

    pf = primary_fabric_for_product(product_name)
    primary_colour = str(pf.get("Colour Clean", "Core") if pf is not None else "Core")
    secondary_colour = "Core Ivory" if "ivory" not in primary_colour.lower() else "Natural"
    colours = [primary_colour, secondary_colour]

    for colour_index, colour in enumerate(colours):
        colour_share = 0.58 if colour_index == 0 else 0.42
        received_colour = max(1, round(base_received * colour_share))
        for size in _sizes:
            received = max(1, round(received_colour * _size_factor[size] / sum(_size_factor.values()) * 5))
            size_adjust = 0.92 + (0.04 * (i % 3))
            sold_estimate = received * base_str * _size_factor[size] * size_adjust
            sold = min(received, max(0, round(sold_estimate))) if np.isfinite(sold_estimate) else 0
            _demo_rows.append({
                "Product": product_name,
                "Size": size,
                "Colour": colour,
                "Units Received": received,
                "Units Sold": sold,
            })

demo_sales = pd.DataFrame(_demo_rows)

# SKU-level retail metrics
sku_sales = demo_sales.groupby("Product", as_index=False).agg(
    Units_Received=("Units Received", "sum"),
    Units_Sold=("Units Sold", "sum"),
)
sku_sales["Sell-through %"] = np.where(
    sku_sales["Units_Received"] > 0,
    sku_sales["Units_Sold"] / sku_sales["Units_Received"] * 100,
    0,
)

sku_sales = sku_sales.merge(
    costing[["Product Name Clean", "Total Cost"]].rename(columns={"Product Name Clean": "Product"}),
    on="Product", how="left"
)
# Use the same illustrative 2.75× retail assumption as Product Lab.
sku_sales["Scenario Retail"] = sku_sales["Total Cost"] * 2.75
sku_sales["Gross Margin"] = sku_sales["Units_Sold"] * (sku_sales["Scenario Retail"] - sku_sales["Total Cost"])
sku_sales["Average Inventory Cost"] = ((sku_sales["Units_Received"] - sku_sales["Units_Sold"] / 2).clip(lower=0) * sku_sales["Total Cost"])
sku_sales["GMROI"] = np.where(
    sku_sales["Average Inventory Cost"] > 0,
    sku_sales["Gross Margin"] / sku_sales["Average Inventory Cost"],
    np.nan,
)

# Size × colour sell-through matrix
curve = demo_sales.groupby(["Colour", "Size"], as_index=False).agg(
    Units_Received=("Units Received", "sum"),
    Units_Sold=("Units Sold", "sum"),
)
curve["Sell-through %"] = np.where(
    curve["Units_Received"] > 0,
    curve["Units_Sold"] / curve["Units_Received"] * 100,
    0,
)


# ============================================================
# SIDEBAR
# ============================================================

LOGO_PATH = Path(__file__).parent / "assets" / "tangy_stitch_logo_sidebar_tight.png"
if LOGO_PATH.exists():
    import base64
    logo_b64 = base64.b64encode(LOGO_PATH.read_bytes()).decode("ascii")
    st.sidebar.markdown(
        f'<div class="sidebar-logo"><img src="data:image/png;base64,{logo_b64}" alt="Tangy Stitch logo"></div>',
        unsafe_allow_html=True,
    )
st.sidebar.markdown('<div class="brand-name">Tangy Stitch</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="brand-sub">RETAIL INTELLIGENCE</div>', unsafe_allow_html=True)
st.sidebar.divider()

PAGES = [
    ("01", "Collection", "01  Collection"),
    ("02", "Product Lab", "02  Product Lab"),
    ("03", "Material Lab", "03  Material Lab"),
    ("04", "Forecast Lab", "04  Forecast Lab"),
    ("05", "Decision Lab", "05  Decision Lab"),
]

# Keep navigation inside the Streamlit app. Do NOT use query parameters:
# changing this control reruns the same URL and preserves the five-page IA.
_page_labels = [p[2] for p in PAGES]
_page_default = st.session_state.get("active_page", "01  Collection")
if _page_default not in _page_labels:
    _page_default = "01  Collection"
_page_index = _page_labels.index(_page_default)

def _navigation_changed():
    st.session_state["reset_page_scroll"] = True

page = st.sidebar.radio(
    "NAVIGATION",
    _page_labels,
    index=_page_index,
    key="active_page",
    on_change=_navigation_changed,
    label_visibility="visible",
)

# Remember the navigation event. The actual scroll script is rendered after
# the selected page has finished rendering, so the top anchor definitely exists.
reset_page_scroll = st.session_state.pop("reset_page_scroll", False)

# This stays on the same app URL; only the selected page body changes.

st.sidebar.divider()
st.sidebar.markdown("**DATA STATUS**")
st.sidebar.markdown(f"• {len(costing)} products")
st.sidebar.markdown(f"• {len(fabric)} fabric records")
st.sidebar.markdown(f"• {len(trims)} trims / accessories")
st.sidebar.caption("Real workbook data is kept separate from simulated planning scenarios.")

# ============================================================
# GLOBAL HEADER
# ============================================================

st.markdown('<div id="page-top-anchor"></div>', unsafe_allow_html=True)
st.markdown('<div class="eyebrow">TANGY STITCH / RETAIL INTELLIGENCE SYSTEM</div>', unsafe_allow_html=True)
st.markdown("# TANGY STITCH")
st.markdown('<div class="subline">A product, material and planning system built around the collection.</div>', unsafe_allow_html=True)

# ============================================================
# 01 COLLECTION
# ============================================================

if page.startswith("01"):
    badge("real", "REAL WORKBOOK DATA")
    section("Collection Intelligence", "A compact view of the current product, material and production footprint.")

    # Executive strip: real workbook KPIs + clearly labelled illustrative retail metrics.
    a, b, c, d = st.columns(4)
    a.metric("Products", len(costing))
    b.metric("Fabric inventory", money(fabric_value))
    c.metric("Sell-through", f"{sku_sales['Sell-through %'].mean():.1f}%")
    gmroi_mean = sku_sales["GMROI"].replace([np.inf, -np.inf], np.nan).mean()
    d.metric("GMROI", f"{gmroi_mean:.2f}×" if pd.notna(gmroi_mean) else "—")

    st.caption("Collection-level retail KPIs are illustrative until order-level sales are connected.")

    system_rail()

    section("Relationship explorer", "Follow a recorded material into the products that use it. This is the data layer behind the collection view.")
    exp_left, exp_right = st.columns([1, 1.35])
    with exp_left:
        material_options = sorted(material["Fabric Name Clean"].dropna().unique().tolist())
        selected_material = st.selectbox("Explore material", material_options, key="collection_material_explorer")
        material_rows = material[material["Fabric Name Clean"] == selected_material]
        stock = float(material_rows["Current Stock"].sum())
        purchased = float(material_rows["Meters Purchased"].sum())
        used = float(material_rows["Fabric_Used_m"].sum())
        util = used / purchased * 100 if purchased else 0
        status_cls = "status-ok" if stock > 0 else "status-watch"
        status_text = "RECORDED STOCK AVAILABLE" if stock > 0 else "REVIEW STOCK"
        st.markdown(
            f"""<div class="explorer">
                <div class="explorer-label">Material selected</div>
                <div class="explorer-title">{selected_material}</div>
                <div class="explorer-copy">Recorded material position across the current collection.</div>
                <div class="explorer-stat"><div class="explorer-stat-label">Current stock</div><div class="explorer-stat-value">{stock:.1f} m</div></div>
                <div class="explorer-stat"><div class="explorer-stat-label">Recorded utilisation</div><div class="explorer-stat-value">{util:.1f}%</div></div>
                <span class="status-pill {status_cls}">{status_text}</span>
            </div>""",
            unsafe_allow_html=True,
        )
    with exp_right:
        linked = flow[flow["Fabric Name Clean"] == selected_material].sort_values("Fabric Used (m)", ascending=False).copy()
        if linked.empty:
            st.markdown(f'''<div class="explorer"><div class="explorer-label">Recorded relationships</div><div class="explorer-title">No product link recorded</div><div class="explorer-copy">This material exists in inventory, but no production-consumption relationship is currently recorded.</div></div>''', unsafe_allow_html=True)
        else:
            st.markdown(f'''<div class="explorer"><div class="explorer-label">Recorded relationships</div><div class="explorer-title">{len(linked)} product connection(s)</div><div class="explorer-copy">The material is currently linked to these recorded products.</div>''', unsafe_allow_html=True)
            for _, rr in linked.head(5).iterrows():
                st.markdown(
                    f'<div style="display:flex;justify-content:space-between;gap:20px;border-top:1px solid {STONE};padding:10px 0 0 0;margin-top:10px;">'
                    f'<span style="color:{INK};font-weight:700;font-size:12px;">{rr["Product Clean"]}</span>'
                    f'<span style="color:{STONE_DARK};font-size:11px;">{rr["Fabric Used (m)"]:.2f} m recorded</span></div>',
                    unsafe_allow_html=True,
                )
            st.markdown('</div>', unsafe_allow_html=True)

    st.write("")
    left, right = st.columns([1.35, 1])

    with left:
        section("Product cost landscape", "Actual production cost by product.")
        dfx = costing[["Product Name Clean", "Total Cost"]].dropna().sort_values("Total Cost", ascending=True)
        fig = go.Figure(go.Bar(
            x=dfx["Total Cost"], y=dfx["Product Name Clean"], orientation="h",
            marker_color=ROSE,
            text=[money(v) for v in dfx["Total Cost"]], textposition="outside", cliponaxis=False,
            hovertemplate="<b>%{y}</b><br>Production cost: ₹%{x:,.0f}<extra></extra>",
        ))
        fig = chart(fig, 540, margins=dict(l=10, r=78, t=8, b=45))
        fig.update_layout(showlegend=False, xaxis_title="Production cost (₹)", yaxis_title="", bargap=.28)
        # Re-apply axis typography after all layout changes.
        fig.update_xaxes(tickfont=dict(color=CHARCOAL, size=10), title_font=dict(color=INK_DARK, size=12))
        fig.update_yaxes(tickfont=dict(color=CHARCOAL, size=10), title_font=dict(color=INK_DARK, size=12))
        st.plotly_chart(fig, width="stretch", config={"displaylogo": False})

    with right:
        section("Where the inventory sits", "Recorded inventory value by material category.")
        cat = fabric.groupby("Fabric Category Clean", as_index=False)["Inventory Value"].sum().sort_values("Inventory Value").tail(10)
        fig = go.Figure(go.Bar(
            x=cat["Inventory Value"], y=cat["Fabric Category Clean"], orientation="h",
            marker_color=INK,
            text=[money(v) for v in cat["Inventory Value"]], textposition="outside", cliponaxis=False,
            hovertemplate="<b>%{y}</b><br>Inventory value: ₹%{x:,.0f}<extra></extra>",
        ))
        fig = chart(fig, 540, margins=dict(l=8, r=72, t=8, b=45))
        fig.update_layout(showlegend=False, xaxis_title="Inventory value (₹)", yaxis_title="", bargap=.3)
        fig.update_xaxes(tickfont=dict(color=CHARCOAL, size=10), title_font=dict(color=INK_DARK, size=12))
        fig.update_yaxes(tickfont=dict(color=CHARCOAL, size=10), title_font=dict(color=INK_DARK, size=12))
        st.plotly_chart(fig, width="stretch", config={"displaylogo": False})

    st.write("")
    section("Collection architecture", "A compact cost-to-material map. Hover a point for product detail; the visual stays intentionally label-free so the collection remains readable.")
    prod = costing[["Product Name Clean", "Total Cost"]].copy()
    prod["Fabric per unit"] = prod["Product Name Clean"].map(unit_fabric_for_product)
    prod = prod.dropna(subset=["Fabric per unit", "Total Cost"])
    if not prod.empty:
        fig = go.Figure(go.Scatter(
            x=prod["Fabric per unit"], y=prod["Total Cost"], mode="markers",
            marker=dict(size=13, color=INK, line=dict(color=PAPER, width=2)),
            customdata=prod["Product Name Clean"],
            hovertemplate="<b>%{customdata}</b><br>Fabric per unit: %{x:.2f} m<br>Production cost: ₹%{y:,.0f}<extra></extra>",
        ))
        fig = chart(fig, 430, margins=dict(l=70, r=30, t=20, b=62))
        fig.update_layout(showlegend=False, xaxis_title="Recorded fabric required per unit (m)", yaxis_title="Production cost (₹)")
        fig.update_xaxes(tickfont=dict(color=CHARCOAL, size=10), title_font=dict(color=INK_DARK, size=12))
        fig.update_yaxes(tickfont=dict(color=CHARCOAL, size=10), title_font=dict(color=INK_DARK, size=12))
        st.plotly_chart(fig, width="stretch", config={"displaylogo": False})

    st.write("")
    badge("real", "RECORDED RELATIONSHIPS")
    section("Material → product flow", "The strongest recorded material relationships, shown as a compact trace rather than a dense Sankey.")
    flow = consumption.merge(fabric[["Fabric ID Clean", "Fabric Name Clean"]], on="Fabric ID Clean", how="left")
    flow = flow.dropna(subset=["Fabric Name Clean", "Product Clean", "Fabric Used (m)"])
    flow = flow.groupby(["Fabric Name Clean", "Product Clean"], as_index=False)["Fabric Used (m)"].sum()
    flow = flow[flow["Fabric Used (m)"] > 0].sort_values("Fabric Used (m)", ascending=False).head(8)
    if not flow.empty:
        cols = st.columns(2)
        for i, (_, r) in enumerate(flow.iterrows()):
            with cols[i % 2]:
                st.markdown(
                    f'<div style="display:flex;justify-content:space-between;border-bottom:1px solid {STONE};padding:10px 2px;gap:20px;">'
                    f'<span style="color:{INK};font-weight:700;">{r["Fabric Name Clean"]}</span>'
                    f'<span style="color:{STONE_DARK};text-align:right;">→ {r["Product Clean"]} · {r["Fabric Used (m)"]:.2f} m</span></div>',
                    unsafe_allow_html=True,
                )

    # ------------------------------------------------------------
    # Retail performance layer
    # ------------------------------------------------------------
    st.write("")
    badge("demo", "ILLUSTRATIVE RETAIL DATA")
    section("Retail Performance", "A demonstration of the metrics the system can support once order-level sales are connected.")

    ra, rb, rc = st.columns(3)
    ra.metric("Average sell-through", f"{sku_sales['Sell-through %'].mean():.1f}%")
    rb.metric("Average GMROI", f"{sku_sales['GMROI'].replace([np.inf, -np.inf], np.nan).mean():.2f}×")
    rc.metric("Demo units sold", f"{int(sku_sales['Units_Sold'].sum()):,}")

    left, right = st.columns([1.15, 1])
    with left:
        section("Sell-through by SKU", "Percentage of illustrative received inventory sold in the scenario.")
        str_plot = sku_sales.sort_values("Sell-through %", ascending=True)
        fig = go.Figure(go.Bar(
            x=str_plot["Sell-through %"], y=str_plot["Product"], orientation="h",
            marker_color=INK,
            text=[f"{v:.0f}%" for v in str_plot["Sell-through %"]], textposition="outside", cliponaxis=False,
            hovertemplate="<b>%{y}</b><br>Sell-through: %{x:.1f}%<extra></extra>",
        ))
        fig = chart(fig, max(430, 22 * len(str_plot) + 110), margins=dict(l=10, r=55, t=10, b=45))
        fig.update_layout(showlegend=False, xaxis_title="Sell-through (%)", yaxis_title="", bargap=.28)
        fig.update_xaxes(range=[0, max(85, float(str_plot["Sell-through %"].max()) + 12)])
        fig.update_yaxes(tickfont=dict(color=CHARCOAL, size=9))
        st.plotly_chart(fig, width="stretch", config={"displaylogo": False})

    with right:
        section("Size × colour curve", "Where illustrative demand is concentrating across the assortment.")
        heat = curve.pivot(index="Colour", columns="Size", values="Sell-through %").reindex(columns=_sizes).fillna(0)
        fig = go.Figure(go.Heatmap(
            z=heat.values, x=heat.columns, y=heat.index,
            zmin=30, zmax=80, colorscale=[[0, ROSE_PALE], [0.55, OCHRE], [1, INK]],
            text=[[f"{v:.0f}%" for v in row] for row in heat.values], texttemplate="%{text}",
            hovertemplate="<b>%{y}</b> · %{x}<br>Sell-through: %{z:.1f}%<extra></extra>",
            colorbar=dict(title=dict(text="STR", font=dict(color=CHARCOAL)), tickfont=dict(color=CHARCOAL)),
        ))
        fig = chart(fig, 430, margins=dict(l=10, r=35, t=15, b=45))
        fig.update_layout(showlegend=False, xaxis_title="Size", yaxis_title="Colour")
        st.plotly_chart(fig, width="stretch", config={"displaylogo": False})

    callout("demo", "IMPORTANT:", "Sell-through, size/colour performance and GMROI are illustrative planning data. They are not historical Tangy Stitch sales results. Replace this demo layer with order-level data when available.")


# ============================================================
# 02 PRODUCT LAB
# ============================================================

elif page.startswith("02"):
    badge("real", "REAL COST DATA")
    section("Product Economics", "Understand how each product is built, then test the commercial layer without confusing it with actual sales.")

    products = costing["Product Name Clean"].tolist()
    product = st.selectbox("Select product", products, key="product_lab_product")
    multiplier = st.slider("Illustrative retail multiplier", 1.5, 4.0, 2.75, 0.25, key="product_multiplier")

    row = costing[costing["Product Name Clean"] == product].iloc[0]
    cost = float(row["Total Cost"])
    scenario_retail = cost * multiplier
    scenario_profit = scenario_retail - cost
    scenario_margin = scenario_profit / scenario_retail * 100 if scenario_retail else 0

    a, b, c, d = st.columns(4)
    a.metric("Production cost", money(cost))
    b.metric("Scenario retail", money(scenario_retail))
    c.metric("Scenario gross profit", money(scenario_profit))
    d.metric("Scenario margin", f"{scenario_margin:.1f}%")

    selected_retail = sku_sales[sku_sales["Product"] == product]
    selected_gmroi = float(selected_retail["GMROI"].iloc[0]) if not selected_retail.empty and pd.notna(selected_retail["GMROI"].iloc[0]) else np.nan
    st.metric("Illustrative GMROI", f"{selected_gmroi:.2f}×" if pd.notna(selected_gmroi) else "—")

    callout("demo", "SCENARIO:", "The workbook currently contains no actual selling prices or order-level sales. Retail, profit, sell-through and GMROI here are illustrative planning values and should be replaced with real sales data when available.")
    st.write("")

    left, right = st.columns(2)
    with left:
        section("Cost anatomy", "Actual populated cost components for the selected product.")
        components = pd.DataFrame({
            "Component": ["Fabric", "Stitching", "Trims / embroidery", "Packaging"],
            "Cost": [row.get("Fabric Cost", 0), row.get("Stitching", 0), row.get("Trims/ Lace/ Embroidery", 0), row.get("Packaging", 0)],
        })
        components["Cost"] = pd.to_numeric(components["Cost"], errors="coerce").fillna(0)
        components = components[components["Cost"] > 0]
        palette = [ROSE, INK, OCHRE, SAGE]
        fig = go.Figure(go.Bar(
            x=components["Cost"], y=components["Component"], orientation="h",
            marker_color=palette[:len(components)],
            text=[money(v) for v in components["Cost"]], textposition="outside", cliponaxis=False,
            hovertemplate="<b>%{y}</b><br>₹%{x:,.0f}<extra></extra>",
        ))
        fig = chart(fig, 350, margins=dict(l=15, r=75, t=10, b=48))
        fig.update_layout(showlegend=False, xaxis_title="Cost (₹)", yaxis_title="", bargap=.32)
        fig.update_xaxes(tickfont=dict(color=CHARCOAL, size=10), title_font=dict(color=INK_DARK, size=12))
        fig.update_yaxes(tickfont=dict(color=CHARCOAL, size=10))
        st.plotly_chart(fig, width="stretch", config={"displaylogo": False})

    with right:
        section("Scenario bridge", "How production cost translates into an illustrative retail value.")
        fig = go.Figure(go.Waterfall(
            x=["Production cost", "Gross profit", "Scenario retail"],
            measure=["absolute", "relative", "total"],
            y=[cost, scenario_profit, scenario_retail],
            connector=dict(line=dict(color=STONE, width=1)),
            increasing=dict(marker=dict(color=INK)),
            totals=dict(marker=dict(color=OCHRE)),
            text=[money(cost), money(scenario_profit), money(scenario_retail)],
            textposition="outside",
            hovertemplate="%{x}: ₹%{y:,.0f}<extra></extra>",
        ))
        fig = chart(fig, 350, margins=dict(l=55, r=35, t=30, b=48))
        fig.update_layout(showlegend=False, yaxis_title="₹")
        fig.update_yaxes(tickfont=dict(color=CHARCOAL, size=10), title_font=dict(color=INK_DARK, size=12))
        st.plotly_chart(fig, width="stretch", config={"displaylogo": False})

    st.write("")
    section("Collection cost map", "A clean ranked view of production cost. Product names stay on the axis instead of being stacked inside a scatter plot.")
    pos = costing[["Product Name Clean", "Total Cost"]].copy().sort_values("Total Cost", ascending=True)
    fig = go.Figure(go.Bar(
        x=pos["Total Cost"], y=pos["Product Name Clean"], orientation="h",
        marker_color=INK,
        text=[money(v) for v in pos["Total Cost"]], textposition="outside", cliponaxis=False,
        hovertemplate="<b>%{y}</b><br>Production cost: ₹%{x:,.0f}<extra></extra>",
    ))
    fig = chart(fig, 560, margins=dict(l=10, r=75, t=10, b=48))
    fig.update_layout(showlegend=False, xaxis_title="Production cost (₹)", yaxis_title="", bargap=.28)
    fig.update_xaxes(tickfont=dict(color=CHARCOAL, size=10), title_font=dict(color=INK_DARK, size=12))
    fig.update_yaxes(tickfont=dict(color=CHARCOAL, size=10))
    st.plotly_chart(fig, width="stretch", config={"displaylogo": False})

# ============================================================
# 03 MATERIAL LAB
# ============================================================

elif page.startswith("03"):
    badge("real", "REAL WORKBOOK DATA")
    section("Material Intelligence", "See what has been purchased, what has been used and where inventory value is concentrated.")

    a, b, c, d = st.columns(4)
    a.metric("Purchased", f"{total_purchased:.1f} m")
    b.metric("Recorded used", f"{total_used:.1f} m")
    c.metric("Utilisation", f"{overall_utilisation:.1f}%")
    d.metric("Fabric inventory", money(fabric_value))

    st.write("")
    left, right = st.columns([1.25, 1])
    with left:
        section("Utilisation by material", "Purchased metres versus recorded production consumption.")
        m = material.groupby("Fabric Category Clean", as_index=False).agg(Purchased=("Meters Purchased", "sum"), Used=("Fabric_Used_m", "sum")).sort_values("Purchased", ascending=True).tail(12)
        fig = go.Figure()
        fig.add_trace(go.Bar(y=m["Fabric Category Clean"], x=m["Purchased"], orientation="h", name="Purchased", marker_color=STONE, text=[f"{v:.1f} m" for v in m["Purchased"]], textposition="outside", cliponaxis=False))
        fig.add_trace(go.Bar(y=m["Fabric Category Clean"], x=m["Used"], orientation="h", name="Used", marker_color=INK, text=[f"{v:.1f} m" if v > 0 else "" for v in m["Used"]], textposition="inside", insidetextanchor="end"))
        fig = chart(fig, 520, legend=True, margins=dict(l=10, r=75, t=28, b=48))
        fig.update_layout(barmode="overlay", xaxis_title="Metres", yaxis_title="", legend=dict(orientation="h", y=1.06, x=0, font=dict(color=CHARCOAL, size=10)))
        fig.update_xaxes(tickfont=dict(color=CHARCOAL, size=10), title_font=dict(color=INK_DARK, size=12))
        fig.update_yaxes(tickfont=dict(color=CHARCOAL, size=10))
        st.plotly_chart(fig, width="stretch", config={"displaylogo": False})

    with right:
        section("Inventory concentration", "Material categories ranked by recorded inventory value.")
        inv = fabric.groupby("Fabric Category Clean", as_index=False)["Inventory Value"].sum().sort_values("Inventory Value").tail(12)
        fig = go.Figure(go.Bar(
            x=inv["Inventory Value"], y=inv["Fabric Category Clean"], orientation="h", marker_color=ROSE,
            text=[money(v) for v in inv["Inventory Value"]], textposition="outside", cliponaxis=False,
            hovertemplate="<b>%{y}</b><br>Inventory value: ₹%{x:,.0f}<extra></extra>",
        ))
        fig = chart(fig, 520, margins=dict(l=15, r=75, t=12, b=48))
        fig.update_layout(showlegend=False, xaxis_title="Inventory value (₹)", yaxis_title="")
        fig.update_xaxes(tickfont=dict(color=CHARCOAL, size=10), title_font=dict(color=INK_DARK, size=12))
        fig.update_yaxes(tickfont=dict(color=CHARCOAL, size=10))
        st.plotly_chart(fig, width="stretch", config={"displaylogo": False})

    most_valuable = material.sort_values("Inventory Value", ascending=False).iloc[0]
    lowest_util = material[material["Meters Purchased"] > 0].sort_values("Utilisation %").iloc[0]
    st.write("")
    x, y = st.columns(2)
    with x:
        insight("INVENTORY CONCENTRATION", most_valuable["Fabric Name Clean"], f"Recorded inventory value is {money(most_valuable['Inventory Value'])}. This is useful context for assortment and production planning.")
    with y:
        insight("LOWEST RECORDED UTILISATION", lowest_util["Fabric Name Clean"], f"Only {lowest_util['Utilisation %']:.1f}% of the purchased quantity is represented in recorded consumption. This is a signal to investigate before buying more of the same material.")

    st.write("")
    section("Material register", "The underlying inventory view, kept deliberately simple and readable.")
    register = material[["Fabric Name Clean", "Fabric Category Clean", "Colour Clean", "Meters Purchased", "Fabric_Used_m", "Remaining m", "Utilisation %", "Inventory Value"]].copy()
    register.columns = ["Fabric", "Category", "Colour", "Purchased", "Used", "Remaining", "Utilisation", "Inventory value"]
    html_table(
        register.head(20), list(register.columns),
        formats={"Purchased": lambda x: f"{x:.1f} m", "Used": lambda x: f"{x:.1f} m", "Remaining": lambda x: f"{x:.1f} m", "Utilisation": lambda x: f"{x:.1f}%", "Inventory value": money},
    )

# ============================================================
# 04 FORECAST LAB
# ============================================================

elif page.startswith("04"):
    badge("demo", "DEMO DEMAND MODE")
    section("Forecast Lab", "A transparent forecasting sandbox. The current history is synthetic because the workbook contains no dated sales records.")

    products = costing["Product Name Clean"].tolist()
    product = st.selectbox("Product", products, key="forecast_product")
    model = st.selectbox("Forecast method", ["Moving average", "Linear trend", "Exponential smoothing"], key="forecast_model")
    horizon = st.slider("Forecast horizon", 2, 6, 4, key="forecast_horizon")
    growth = st.slider("Scenario demand adjustment", -20, 30, 0, 5, key="forecast_growth")

    hist = make_demo_demand(product)
    pred = forecast_series(hist, horizon, model) * (1 + growth / 100)
    future_dates = pd.date_range(hist["Month"].iloc[-1] + pd.offsets.MonthBegin(1), periods=horizon, freq="MS")
    residual = hist["Units"] - hist["Units"].rolling(3, min_periods=1).mean()
    sigma = max(float(residual.std(ddof=0)), 0.7)
    lower = np.maximum(pred - 1.28 * sigma, 0)
    upper = pred + 1.28 * sigma

    avg_demand = hist["Units"].mean()
    next_month = pred[0]
    horizon_total = pred.sum()
    peak_month = future_dates[int(np.argmax(pred))]

    a, b, c, d = st.columns(4)
    a.metric("Avg monthly demand", f"{avg_demand:.1f} units")
    b.metric("Next month", f"{next_month:.0f} units")
    c.metric(f"Next {horizon} months", f"{horizon_total:.0f} units")
    d.metric("Peak forecast month", peak_month.strftime("%b %Y"))

    callout("demo", "DEMO DATA:", "This history is synthetic and deterministic so the forecasting workflow can be demonstrated without inventing real Tangy Stitch sales. Replace it with actual dated sales records before using the forecast operationally.")
    st.write("")

    section("Demand trajectory", "Historical demo demand, forecast signal and a restrained uncertainty band.")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=hist["Month"], y=hist["Units"], mode="lines+markers", name="Demo history", line=dict(color=ROSE, width=2.5), marker=dict(size=6)))
    fig.add_trace(go.Scatter(x=future_dates, y=upper, mode="lines", line=dict(width=0), showlegend=False, hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=future_dates, y=lower, mode="lines", fill="tonexty", fillcolor="rgba(168,184,167,.24)", line=dict(width=0), name="Uncertainty band", hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=future_dates, y=pred, mode="lines+markers", name="Forecast", line=dict(color=INK, width=2.8), marker=dict(size=6)))
    fig.add_vline(x=hist["Month"].iloc[-1].timestamp() * 1000, line_dash="dot", line_color=OCHRE, line_width=1.5)
    fig.add_annotation(x=future_dates[0], y=max(max(hist["Units"]), max(upper)), text="FORECAST START", showarrow=False, font=dict(size=9, color=OCHRE), xanchor="left", yshift=8)
    fig = chart(fig, 470, legend=True, margins=dict(l=55, r=30, t=45, b=52))
    fig.update_layout(xaxis_title="", yaxis_title="Units", legend=dict(orientation="h", y=1.07, x=0, font=dict(color=CHARCOAL, size=10)))
    fig.update_xaxes(tickfont=dict(color=CHARCOAL, size=10), title_font=dict(color=INK_DARK, size=12))
    fig.update_yaxes(tickfont=dict(color=CHARCOAL, size=10), title_font=dict(color=INK_DARK, size=12))
    st.plotly_chart(fig, width="stretch", config={"displaylogo": False})

    st.write("")
    left, right = st.columns(2)
    with left:
        section("Method comparison", "Total forecast across the selected horizon.")
        comparison = []
        for m in ["Moving average", "Linear trend", "Exponential smoothing"]:
            p = forecast_series(hist, horizon, m) * (1 + growth / 100)
            comparison.append({"Method": m, "Forecast units": p.sum()})
        comp = pd.DataFrame(comparison)
        html_table(comp, ["Method", "Forecast units"], {"Forecast units": lambda x: f"{x:.1f}"})

    with right:
        section("Forecast → material requirement", "Turn a demand signal into a material planning question.")
        unit_fabric = unit_fabric_for_product(product)
        current = primary_fabric_for_product(product)
        if unit_fabric is not None and current is not None:
            required = horizon_total * unit_fabric
            available = float(current["Current Stock"])
            gap = available - required
            status = "Within recorded stock" if gap >= 0 else "Additional material indicated"
            status_colour = INK if gap >= 0 else ROSE_DARK
            st.markdown(
                f'<div style="padding:8px 0 12px 0;">'
                f'<div style="font-family:{FONT_SERIF};font-size:22px;color:{INK};">{current["Fabric Name Clean"]}</div>'
                f'<div style="color:{STONE_DARK};font-size:11px;margin-top:2px;">{unit_fabric:.2f} m per unit · {horizon_total:.0f} forecast units</div></div>',
                unsafe_allow_html=True,
            )
            q1, q2 = st.columns(2)
            q1.metric("Material required", f"{required:.1f} m")
            q2.metric("Recorded stock", f"{available:.1f} m")
            st.markdown(f'<div style="color:{status_colour};font-weight:700;font-size:12px;margin-top:9px;">{status}</div>', unsafe_allow_html=True)
            st.caption("This is a planning calculation, not a purchase recommendation. It becomes operational once actual sales data is connected.")
        else:
            st.caption("No reliable product-to-material match is available for this product.")

# ============================================================
# 05 DECISION LAB
# ============================================================

else:
    badge("demo", "PLANNING SCENARIO")
    section("Decision Lab", "Test a production decision before it becomes a production commitment. Change the assumptions and watch the material position respond.")

    products = costing["Product Name Clean"].tolist()
    product = st.selectbox("Product", products, key="decision_product")
    forecast_units = st.number_input("Expected demand / production units", min_value=1, max_value=250, value=20, step=1, key="decision_units")
    safety = st.slider("Safety-stock buffer", 0, 30, 10, 5, key="decision_safety")
    multiplier = st.slider("Illustrative retail multiplier", 1.5, 4.0, 2.75, 0.25, key="decision_multiplier")

    row = costing[costing["Product Name Clean"] == product].iloc[0]
    unit_fabric = unit_fabric_for_product(product)
    planned_units = int(np.ceil(forecast_units * (1 + safety / 100)))
    material_required = unit_fabric * planned_units if unit_fabric is not None else None
    scenario_revenue = float(row["Total Cost"]) * multiplier * planned_units
    scenario_cost = float(row["Total Cost"]) * planned_units
    scenario_profit = scenario_revenue - scenario_cost

    a, b, c, d = st.columns(4)
    a.metric("Planning quantity", f"{planned_units} units")
    b.metric("Material required", f"{material_required:.1f} m" if material_required is not None else "No match")
    c.metric("Scenario revenue", money(scenario_revenue))
    d.metric("Scenario gross profit", money(scenario_profit))

    callout("demo", "SCENARIO MODE:", "Demand, safety stock and retail multiplier are assumptions. Production cost and material-consumption inputs come from the workbook where available.")
    st.write("")

    current = primary_fabric_for_product(product)
    if material_required is not None and current is not None:
        available = float(current["Current Stock"])
        gap = available - material_required
        if gap >= 0:
            title = "MATERIAL AVAILABLE"
            copy = f'{current["Fabric Name Clean"]}: {available:.2f} m recorded stock versus {material_required:.2f} m required.'
            bg = SAGE_PALE
            fg = INK
        else:
            title = "MATERIAL CONSTRAINED"
            copy = f'{current["Fabric Name Clean"]}: {available:.2f} m available versus {material_required:.2f} m required. Shortfall: {abs(gap):.2f} m.'
            bg = "#F0DDD9"
            fg = ROSE_DARK
        st.markdown(
            f'<div style="background:{bg};border:1px solid {STONE};border-radius:8px;padding:16px 18px;margin-bottom:18px;">'
            f'<div style="color:{ROSE};font-size:9px;letter-spacing:1.6px;font-weight:800;">MATERIAL FEASIBILITY</div>'
            f'<div style="color:{fg};font-family:{FONT_SERIF};font-size:24px;margin-top:4px;">{title}</div>'
            f'<div style="color:{fg};font-size:11px;margin-top:4px;">{copy}</div></div>',
            unsafe_allow_html=True,
        )

    if material_required is not None and current is not None:
        available_for_readiness = float(current["Current Stock"])
        coverage = (available_for_readiness / material_required * 100) if material_required else 0
        if coverage >= 100:
            readiness_label = "READY ON RECORDED MATERIAL"
            readiness_copy = f"{current['Fabric Name Clean']} covers the planned quantity with {available_for_readiness - material_required:.1f} m remaining."
            readiness_cls = "status-ok"
        else:
            readiness_label = "MATERIAL CONSTRAINED"
            readiness_copy = f"{current['Fabric Name Clean']} covers {coverage:.0f}% of the planned requirement; {material_required - available_for_readiness:.1f} m is not covered by recorded stock."
            readiness_cls = "status-watch"
        st.markdown(
            f"""<div class="explorer" style="margin-top:4px; margin-bottom:20px;">
                <div class="explorer-label">Production readiness</div>
                <div style="display:flex;align-items:center;justify-content:space-between;gap:20px;flex-wrap:wrap;">
                    <div><div class="explorer-title">{product}</div><div class="explorer-copy">{readiness_copy}</div></div>
                    <span class="status-pill {readiness_cls}">{readiness_label}</span>
                </div>
            </div>""",
            unsafe_allow_html=True,
        )

    section("What-if matrix", "Gross profit across production quantity and illustrative retail multiplier.")
    multipliers = [2.0, 2.5, 3.0, 3.5]
    quantities = [10, 20, 30, 40]
    z = []
    for q in quantities:
        row_z = []
        for mult in multipliers:
            revenue = float(row["Total Cost"]) * mult * q
            profit = revenue - float(row["Total Cost"]) * q
            row_z.append(profit)
        z.append(row_z)
    fig = go.Figure(go.Heatmap(
        z=z,
        x=[f"{m:.1f}×" for m in multipliers],
        y=[f"{q} units" for q in quantities],
        colorscale=[[0, ROSE_PALE], [0.5, "#D5C9BA"], [1, INK]],
        text=[[money(v) for v in r] for r in z],
        texttemplate="%{text}",
        textfont=dict(color=CHARCOAL, size=11),
        hovertemplate="Quantity: %{y}<br>Retail multiplier: %{x}<br>Gross profit: ₹%{z:,.0f}<extra></extra>",
        colorbar=dict(
            title=dict(text="Gross profit", font=dict(color=INK_DARK, size=11)),
            tickfont=dict(color=CHARCOAL, size=10),
            outlinecolor=STONE,
        ),
    ))
    fig = chart(fig, 390, margins=dict(l=85, r=80, t=20, b=58))
    fig.update_layout(showlegend=False, xaxis_title="Illustrative retail multiplier", yaxis_title="Planned quantity")
    fig.update_xaxes(tickfont=dict(color=CHARCOAL, size=11), title_font=dict(color=INK_DARK, size=12))
    fig.update_yaxes(tickfont=dict(color=CHARCOAL, size=11), title_font=dict(color=INK_DARK, size=12))
    st.plotly_chart(fig, width="stretch", config={"displaylogo": False})

    st.write("")
    left, right = st.columns(2)
    with left:
        insight("DECISION BRIDGE", "Forecast → production → material", "The useful part of the system is the connection between a demand assumption, production quantity and the recorded material base.")
    with right:
        insight("COMMERCIAL LAYER", "Scenario, not fact", "The workbook has production costs but no actual selling prices. Keeping this layer explicitly simulated prevents invented business results from entering the project.")

# ============================================================
# FOOTER
# ============================================================

st.divider()
st.markdown('<div class="footer">TANGY STITCH / Retail Intelligence System · Real inventory + transparent simulation layer</div>', unsafe_allow_html=True)


# ============================================================
# NAVIGATION SCROLL RESET
# ============================================================
if reset_page_scroll:
    st.html(
        """<script>
        (() => {
            const goTop = () => {
                const anchor = document.getElementById('page-top-anchor');
                const main = document.querySelector('[data-testid="stMain"]');
                const candidates = [
                    main,
                    document.querySelector('section.main'),
                    document.querySelector('main'),
                    document.querySelector('[data-testid="stAppViewContainer"]'),
                    document.scrollingElement,
                    document.documentElement,
                    document.body
                ].filter(Boolean);

                // The anchor is at the very beginning of the page body.
                if (anchor) {
                    anchor.scrollIntoView({block: 'start', inline: 'nearest', behavior: 'auto'});
                }

                for (const el of candidates) {
                    try {
                        el.scrollTop = 0;
                        el.scrollLeft = 0;
                        if (typeof el.scrollTo === 'function') el.scrollTo(0, 0);
                    } catch (e) {}
                }

                try { window.scrollTo(0, 0); } catch (e) {}
            };

            // Streamlit may finish its DOM update a moment after the script
            // is inserted, so retry across a few frames.
            requestAnimationFrame(goTop);
            setTimeout(goTop, 50);
            setTimeout(goTop, 150);
            setTimeout(goTop, 300);
            setTimeout(goTop, 600);
        })();
        </script>""",
        width="stretch",
        unsafe_allow_javascript=True,
    )
