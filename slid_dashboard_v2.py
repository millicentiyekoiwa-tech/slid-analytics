"""
SLID Immigration Analytics Dashboard v2
Digitalization and Process Optimization of Immigration Services in Sierra Leone
Author: Millicent Iye Koiwa | MSc Business Analytics | AUB | 2026
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
from math import factorial
import statsmodels.api as sm
import base64
from io import BytesIO
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="SLID Analytics",
    page_icon="🛂",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Colour Palette: Sierra Leone Flag (Green, White, Blue) ──
P = {
    "green"  : "#1B5E20",
    "lgreen" : "#2E7D32",
    "mgreen" : "#388E3C",
    "tgreen" : "#4CAF50",
    "blue"   : "#0D47A1",
    "lblue"  : "#1565C0",
    "mblue"  : "#1976D2",
    "tblue"  : "#42A5F5",
    "white"  : "#FFFFFF",
    "offwhite": "#F8F9FA",
    "lgray"  : "#ECEFF1",
    "mgray"  : "#CFD8DC",
    "dgray"  : "#546E7A",
    "dark"   : "#102027",
    "card"   : "#FAFAFA",
    "border" : "#B0BEC5",
    "red"    : "#C62828",
    "gold"   : "#F9A825",
    "text"   : "#102027",
    "sub"    : "#37474F",
}

COLORS = [P["lgreen"], P["lblue"], P["tgreen"], P["tblue"],
          P["mgreen"], P["mblue"], "#66BB6A", "#64B5F6",
          P["gold"], P["red"]]

# ── Sierra Leone Watermark SVG ───────────────────────────────
SL_WATERMARK = """
<div style="
  position:fixed;
  bottom:60px;
  right:30px;
  opacity:0.06;
  z-index:0;
  pointer-events:none;
  width:220px;">
  <svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
    <!-- Sierra Leone coat of arms outline -->
    <ellipse cx="100" cy="100" rx="95" ry="95"
      fill="none" stroke="#1B5E20" stroke-width="4"/>
    <ellipse cx="100" cy="100" rx="85" ry="85"
      fill="none" stroke="#0D47A1" stroke-width="2"/>
    <!-- Lion silhouette simplified -->
    <path d="M60,130 Q70,90 100,85 Q130,90 140,130 Q120,145 100,148 Q80,145 60,130Z"
      fill="#1B5E20"/>
    <path d="M85,85 Q100,70 115,85 Q110,75 100,72 Q90,75 85,85Z"
      fill="#1B5E20"/>
    <!-- Stars -->
    <text x="100" y="170" text-anchor="middle"
      font-size="14" fill="#0D47A1">★ ★ ★</text>
    <!-- Text -->
    <text x="100" y="55" text-anchor="middle"
      font-size="11" fill="#1B5E20" font-weight="bold">SIERRA LEONE</text>
    <text x="100" y="190" text-anchor="middle"
      font-size="9" fill="#0D47A1">UNITY FREEDOM JUSTICE</text>
  </svg>
</div>"""

# ── CSS ──────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {{
  font-family: 'Inter', sans-serif;
  background: {P['offwhite']};
  color: {P['text']};
}}

/* Sidebar */
section[data-testid="stSidebar"] {{
  background: {P['green']};
  border-right: 3px solid {P['lgreen']};
}}
section[data-testid="stSidebar"] * {{
  color: {P['white']} !important;
}}
section[data-testid="stSidebar"] .stRadio label {{
  color: {P['white']} !important;
  font-size: 0.85rem !important;
}}
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {{
  background: rgba(255,255,255,0.15);
  border-radius: 6px;
}}

/* Main header */
.main-header {{
  background: linear-gradient(135deg, {P['green']}, {P['lblue']});
  border-radius: 10px;
  padding: 1.1rem 1.5rem;
  margin-bottom: 1.2rem;
  border-bottom: 3px solid {P['tgreen']};
}}
.main-header h1 {{
  color: {P['white']};
  font-size: 1.3rem;
  font-weight: 700;
  margin: 0;
}}
.main-header p {{
  color: rgba(255,255,255,0.85);
  font-size: 0.78rem;
  margin: 0.2rem 0 0;
}}

/* KPI cards */
.kpi {{
  background: {P['white']};
  border-radius: 10px;
  padding: 1rem 1.1rem;
  border: 1px solid {P['border']};
  border-top: 4px solid {P['lgreen']};
  margin-bottom: 0.6rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}}
.kpi.b {{ border-top-color: {P['lblue']}; }}
.kpi.r {{ border-top-color: {P['red']}; }}
.kpi.g {{ border-top-color: {P['gold']}; }}
.kpi.m {{ border-top-color: {P['mblue']}; }}
.kv {{
  font-size: 1.8rem;
  font-weight: 700;
  color: {P['lgreen']};
  margin: 0;
  line-height: 1;
}}
.kv.b {{ color: {P['lblue']}; }}
.kv.r {{ color: {P['red']}; }}
.kv.g {{ color: {P['gold']}; }}
.kl {{
  font-size: 0.7rem;
  color: {P['dgray']};
  margin: 0.2rem 0 0;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}}

/* Section headers */
.sec {{
  font-size: 0.78rem;
  font-weight: 600;
  color: {P['lgreen']};
  text-transform: uppercase;
  letter-spacing: 0.07em;
  border-bottom: 2px solid {P['tgreen']};
  padding-bottom: 0.25rem;
  margin-bottom: 0.7rem;
}}

/* Info boxes */
.ins {{
  background: rgba(27,94,32,0.06);
  border-left: 3px solid {P['lgreen']};
  border-radius: 5px;
  padding: 0.5rem 0.8rem;
  font-size: 0.78rem;
  color: {P['sub']};
  margin: 0.3rem 0;
}}
.wrn {{
  background: rgba(198,40,40,0.06);
  border-left: 3px solid {P['red']};
  border-radius: 5px;
  padding: 0.5rem 0.8rem;
  font-size: 0.78rem;
  color: {P['sub']};
  margin: 0.3rem 0;
}}
.fnd {{
  background: rgba(13,71,161,0.06);
  border-left: 3px solid {P['lblue']};
  border-radius: 5px;
  padding: 0.5rem 0.8rem;
  font-size: 0.78rem;
  color: {P['sub']};
  margin: 0.3rem 0;
}}

/* Charts background */
.block-container {{ padding: 1.2rem 1.8rem; max-width: 100%; }}
.stPlotlyChart {{ border-radius: 8px; }}

/* Buttons */
.stButton > button {{
  background: {P['lblue']};
  color: white;
  border: none;
  border-radius: 7px;
  font-weight: 600;
  font-size: 0.85rem;
  padding: 0.5rem 1.2rem;
}}
.stButton > button:hover {{ background: {P['blue']}; }}

/* Login card */
.login-card {{
  background: {P['white']};
  border-radius: 14px;
  padding: 2.5rem;
  border: 1px solid {P['border']};
  box-shadow: 0 8px 32px rgba(0,0,0,0.1);
  margin-top: 4rem;
}}

/* Flag stripe */
.flag-stripe {{
  height: 6px;
  background: linear-gradient(to right,
    {P['lgreen']} 33.3%,
    {P['white']} 33.3% 66.6%,
    {P['lblue']} 66.6%);
  border-radius: 3px;
  margin-bottom: 1.2rem;
}}
</style>
{SL_WATERMARK}
""", unsafe_allow_html=True)

# ── Auth ─────────────────────────────────────────────────────
CREDS = {"SLID": "Capstone"}

if "auth" not in st.session_state:
    st.session_state["auth"] = False

if not st.session_state["auth"]:
    c1, c2, c3 = st.columns([1, 1.1, 1])
    with c2:
        st.markdown(f"""
        <div class="login-card">
          <div class="flag-stripe"></div>
          <div style="text-align:center;margin-bottom:1.5rem;">
            <div style="font-size:1.8rem;font-weight:800;
              color:{P['green']};letter-spacing:0.1em;">SLID</div>
            <div style="font-size:1rem;font-weight:600;
              color:{P['text']};margin:0.3rem 0 0.1rem;">
              Analytics Dashboard</div>
            <div style="font-size:0.72rem;color:{P['dgray']};">
              Sierra Leone Immigration Department<br>
              Authorized Personnel Only</div>
          </div>
        </div>""", unsafe_allow_html=True)
        with st.form("login"):
            u  = st.text_input("Username", placeholder="Enter username")
            pw = st.text_input("Password", type="password",
                               placeholder="Enter password")
            if st.form_submit_button("Sign In",
                                     use_container_width=True):
                if u in CREDS and CREDS[u] == pw:
                    st.session_state["auth"] = True
                    st.rerun()
                else:
                    st.error("Invalid credentials.")
        st.markdown(
            f'<p style="text-align:center;font-size:0.7rem;'
            f'color:{P["dgray"]};margin-top:1rem;">'
            f'Digitalization and Process Optimization Initiative<br>'
            f'MSc Business Analytics | AUB 2026</p>',
            unsafe_allow_html=True)
    st.stop()

# ── Chart theme helper ───────────────────────────────────────
def L(fig, h=360, legend_h=False, show_legend=True):
    kw = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=P["offwhite"],
        height=h,
        font=dict(family="Inter", color=P["sub"], size=11),
        margin=dict(l=0, r=0, t=28, b=0),
        showlegend=show_legend,
    )
    if show_legend:
        leg = dict(bgcolor="rgba(0,0,0,0)",
                   font=dict(color=P["sub"]))
        if legend_h:
            leg.update(orientation="h", y=1.1)
        kw["legend"] = leg
    fig.update_layout(**kw)
    fig.update_xaxes(gridcolor=P["mgray"], linecolor=P["border"],
                     tickfont=dict(color=P["sub"]))
    fig.update_yaxes(gridcolor=P["mgray"], linecolor=P["border"],
                     tickfont=dict(color=P["sub"]))
    return fig

def kpi(label, val, t="", rv=""):
    st.markdown(
        f'<div class="kpi {t}">'
        f'<p class="kv {t}">{val}</p>'
        f'<p class="kl">{label}</p>'
        f'{"<p style=font-size:0.65rem;color:"+P["dgray"]+";margin:0>"+rv+"</p>" if rv else ""}'
        f'</div>', unsafe_allow_html=True)

def sec(t):
    st.markdown(f'<p class="sec">{t}</p>', unsafe_allow_html=True)

def ins(t):
    st.markdown(f'<div class="ins">{t}</div>', unsafe_allow_html=True)

def wrn(t):
    st.markdown(f'<div class="wrn">{t}</div>', unsafe_allow_html=True)

def fnd(t):
    st.markdown(f'<div class="fnd">{t}</div>', unsafe_allow_html=True)

def mms(lam, mu, s):
    rho = lam / (s * mu)
    if rho >= 1:
        return dict(rho=rho, stable=False, W=None, Lq=None)
    terms = sum([(s*rho)**n/factorial(n) for n in range(s)])
    last  = (s*rho)**s / (factorial(s)*(1-rho))
    P0    = 1 / (terms+last)
    Lq    = (P0*(lam/mu)**s*rho) / (factorial(s)*(1-rho)**2)
    Wq    = Lq / lam
    return dict(rho=round(rho,4), stable=True,
                W=round(Wq+1/mu,4), Lq=round(Lq,4))

# ── Data loaders ─────────────────────────────────────────────
@st.cache_data
def load_rp():
    df = pd.read_excel("SLID_Residency_Final_Cleaned.xlsx",
                       engine="openpyxl")
    df["Date of Creation"] = pd.to_datetime(
        df["Date of Creation"], errors="coerce")
    df["Card Expiry Date"] = pd.to_datetime(
        df["Card Expiry Date"], errors="coerce")
    if "Month" not in df.columns:
        df["Month"] = df["Date of Creation"]\
            .dt.to_period("M").astype(str)
    if "Month_Num" not in df.columns:
        df["Month_Num"] = df["Date of Creation"].dt.month
    if "Day_of_Week" not in df.columns:
        df["Day_of_Week"] = df["Date of Creation"].dt.day_name()
    if "DOW_Num" not in df.columns:
        df["DOW_Num"] = df["Date of Creation"].dt.dayofweek
    if "Days_to_Expiry" not in df.columns:
        df["Days_to_Expiry"] = (
            df["Card Expiry Date"] -
            df["Date of Creation"]).dt.days
    if "Card_Issued" not in df.columns:
        df["Card_Issued"] = df["Card Number"].notna().astype(int)
    if "Completion" not in df.columns:
        df["Completion"] = np.where(
            df["Status"]==7, "Delivered", "Not Delivered")
    if "Completion_Binary" not in df.columns:
        df["Completion_Binary"] = (
            df["Completion"]=="Delivered").astype(int)
    sm_ = {1:"Draft",2:"New",3:"Appointment Needed",
           5:"Printed",6:"Ready To Pickup",7:"Delivered",
           8:"Expired",11:"Rejected",
           15:"Need Extra Document",19:"Needs Edit"}
    if "Status_Name" not in df.columns:
        df["Status_Name"] = df["Status"].map(sm_).fillna("Other")

    # Lead time: days from submission to data extraction date
    extract_date = pd.Timestamp("2026-08-18")
    df["Days_in_System"] = (
        extract_date - df["Date of Creation"]).dt.days
    df["Days_in_System"] = df["Days_in_System"].clip(lower=0)
    return df

@st.cache_resource
def load_models(_df):
    try:
        from sklearn.linear_model import LogisticRegression
        from sklearn.preprocessing import LabelEncoder, StandardScaler
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import roc_auc_score, accuracy_score

        data = _df.copy()
        le_cat  = LabelEncoder()
        le_proc = LabelEncoder()
        data["Category"]     = data["Category"].fillna("Unknown")
        data["Process Code"] = data["Process Code"].fillna("Unknown")
        data["Cat_Enc"]  = le_cat.fit_transform(data["Category"])
        data["Proc_Enc"] = le_proc.fit_transform(
            data["Process Code"])

        features = ["Amount ($)","Month_Num","DOW_Num",
                    "Cat_Enc","Proc_Enc"]
        for col in features:
            if col not in data.columns:
                data[col] = 0
        data = data.dropna(
            subset=features+["Completion_Binary"])

        X = data[features]
        y = data["Completion_Binary"]
        scaler = StandardScaler()
        X_sc   = scaler.fit_transform(X)
        lr = LogisticRegression(
            max_iter=1000, random_state=42,
            class_weight="balanced", C=0.1)
        lr.fit(X_sc, y)
        meta = {
            "categories"   : sorted(data["Category"].unique().tolist()),
            "process_codes": sorted(
                data["Process Code"].unique().tolist()),
            "amount_min"   : float(data["Amount ($)"].min()),
            "amount_max"   : float(data["Amount ($)"].max()),
            "amount_mean"  : float(data["Amount ($)"].mean()),
        }
        X_tr,X_te,y_tr,y_te = train_test_split(
            X_sc, y, test_size=0.2,
            stratify=y, random_state=42)
        acc = accuracy_score(y_te, lr.predict(X_te))
        auc = roc_auc_score(
            y_te, lr.predict_proba(X_te)[:,1])
        return lr,scaler,le_cat,le_proc,meta,acc,auc,True
    except Exception:
        return None,None,None,None,{},0,0,False

@st.cache_data
def load_pp():
    pp = pd.DataFrame({
        "Month":["Jan","Feb","Mar","Apr","May","Jun","Jul"],
        "MF"   :["2026-01","2026-02","2026-03","2026-04",
                 "2026-05","2026-06","2026-07"],
        "Ord"  :[5894,6370,5094,5468,4102,4754,6685],
        "Svc"  :[55,103,108,10,7,8,83],
        "Dip"  :[15,25,30,27,16,32,17],
        "Tot"  :[5964,6498,5232,5505,4125,4794,6785],
        "WD"   :[26,25,27,26,27,26,27],
    })
    pp["Rev"]  = pp["Ord"]*100 + pp["Svc"]*100
    pp["Rate"] = (pp["Tot"]/pp["WD"]).round(1)
    pp["MoM"]  = pp["Tot"].diff()

    office = pd.DataFrame({
        "Office":["Freetown","Makeni","Kenema","Online","Bo"],
        "Total" :[38195,279,170,130,129],
        "Pct"   :[98.18,0.72,0.44,0.33,0.33],
        "Lat"   :[8.484,8.879,7.876,8.484,7.965],
        "Lon"   :[-13.234,-12.059,-11.190,-13.234,-11.738],
    })
    return pp, office

df                                   = load_rp()
pp, office                           = load_pp()
lr_,sc_,lc_,lp_,meta_,acc_,auc_,ok = load_models(df)

# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="text-align:center;padding:0.8rem 0 0.4rem;">
      <div style="font-size:1.5rem;font-weight:800;
        color:white;letter-spacing:0.12em;">SLID</div>
      <div style="font-weight:600;color:rgba(255,255,255,0.9);
        font-size:0.85rem;margin:0.2rem 0;">
        Analytics Dashboard</div>
      <div style="font-size:0.62rem;color:rgba(255,255,255,0.7);
        border-top:1px solid rgba(255,255,255,0.2);
        padding-top:0.4rem;margin-top:0.4rem;">
        Sierra Leone Immigration Department<br>
        MSc Business Analytics | AUB 2026</div>
    </div>
    <div style="height:4px;background:linear-gradient(to right,
      #4CAF50,white,#42A5F5);border-radius:2px;margin:0.6rem 0;">
    </div>""", unsafe_allow_html=True)

    page = st.radio("Navigation", [
        "Overview",
        "Passport Analysis",
        "Residency Permit Analysis",
        "Lead Time Analysis",
        "Process Performance",
        "Revenue Forecast",
        "Predictive Analytics",
    ], label_visibility="collapsed")

    st.divider()
    st.markdown(
        f'<p style="font-size:0.65rem;'
        f'color:rgba(255,255,255,0.6);text-align:center;">'
        f'Data: Jan-Aug 2026<br>'
        f'Residency: 11,118 records<br>'
        f'Passport: Jan-Jul 2026</p>',
        unsafe_allow_html=True)
    st.divider()
    if st.button("Sign Out", use_container_width=True):
        st.session_state["auth"] = False
        st.rerun()

# ── Page Header ──────────────────────────────────────────────
st.markdown(f"""
<div class="main-header">
  <h1>Sierra Leone Immigration Department | Analytics Dashboard</h1>
  <p>Passport Production Jan-Jul 2026 | Residency Permit Applications Jan-Aug 2026 |
     Digitalization and Process Optimization Initiative</p>
</div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# PAGE 1: OVERVIEW
# ════════════════════════════════════════════════════════════
if page == "Overview":
    with st.expander("Filters", expanded=False):
        c1, c2 = st.columns(2)
        with c1:
            all_m = sorted(df["Month"].dropna().unique())
            sel_m = st.multiselect("Permit Month", all_m,
                                   default=all_m, key="ov_m")
        with c2:
            sel_pp = st.multiselect("Passport Month",
                pp["Month"].tolist(),
                default=pp["Month"].tolist(), key="ov_pp")
    fdf = df[df["Month"].isin(sel_m)]
    fpp = pp[pp["Month"].isin(sel_pp)]

    k1,k2,k3,k4,k5,k6 = st.columns(6)
    with k1: kpi("Passports Produced",
                 f"{fpp['Tot'].sum():,}","m")
    with k2: kpi("Permit Applications",
                 f"{len(fdf):,}")
    with k3:
        dr = (fdf["Completion"]=="Delivered").mean()*100
        kpi("Permit Delivery Rate",f"{dr:.1f}%",
            "r" if dr<80 else "")
    with k4: kpi("Passport Revenue",
                 f"${fpp['Rev'].sum()/1e6:.2f}M","g")
    with k5: kpi("Permit Revenue",
                 f"${fdf['Amount ($)'].sum()/1e6:.2f}M","g")
    with k6:
        tot = fpp["Rev"].sum()+fdf["Amount ($)"].sum()
        kpi("Combined Revenue",f"${tot/1e6:.2f}M","b")

    st.markdown("")
    c1, c2 = st.columns(2)
    with c1:
        sec("Monthly Volume: Passport vs Residency Permit")
        rp_m = fdf.groupby("Month").size().reset_index(
            name="Apps")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=fpp["MF"], y=fpp["Tot"],
            name="Passport",
            mode="lines+markers",
            line=dict(color=P["lgreen"],width=2.5),
            marker=dict(size=7),
            fill="tozeroy",
            fillcolor="rgba(46,125,50,0.08)"))
        fig.add_trace(go.Scatter(
            x=rp_m["Month"], y=rp_m["Apps"],
            name="Residency Permit",
            mode="lines+markers",
            line=dict(color=P["lblue"],width=2.5),
            marker=dict(size=7),
            fill="tozeroy",
            fillcolor="rgba(21,101,192,0.08)"))
        L(fig, 360, True)
        fig.update_xaxes(title_text="Month")
        fig.update_yaxes(title_text="Volume")
        st.plotly_chart(fig, use_container_width=True)
        ins("Passport volumes consistently exceed permit applications, reflecting broader citizen demand for travel documents versus foreign national residency needs.")

    with c2:
        sec("Monthly Revenue: Passport vs Residency Permit")
        rp_r = fdf.groupby("Month")[
            "Amount ($)"].sum().reset_index()
        rp_r.columns = ["Month","Rev"]
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=fpp["MF"], y=fpp["Rev"],
            name="Passport",
            marker_color=P["lgreen"], opacity=0.85))
        fig2.add_trace(go.Bar(
            x=rp_r["Month"], y=rp_r["Rev"],
            name="Residency Permit",
            marker_color=P["lblue"], opacity=0.85))
        L(fig2, 360, True)
        fig2.update_layout(barmode="group")
        fig2.update_yaxes(tickformat="$,.0f",
                          title_text="Revenue (USD)")
        st.plotly_chart(fig2, use_container_width=True)
        ins("Residency permit revenue shows a stronger growth trajectory through June 2026, driven by annual permit renewals.")

    st.markdown("")
    c3, c4 = st.columns(2)
    with c3:
        sec("Revenue Distribution")
        fig3 = go.Figure(go.Pie(
            labels=["Passport","Residency Permit"],
            values=[fpp["Rev"].sum(),
                    fdf["Amount ($)"].sum()],
            hole=0.55,
            marker_colors=[P["lgreen"],P["lblue"]],
            textinfo="label+percent",
            textfont=dict(color=P["text"],size=11)))
        L(fig3, 300, show_legend=False)
        st.plotly_chart(fig3, use_container_width=True)

    with c4:
        sec("Service Delivery Scorecard")
        sc_df = pd.DataFrame({
            "Metric":["Passport Production",
                      "Permit Delivery Rate",
                      "Online Adoption",
                      "Freetown Concentration",
                      "Processing Time vs Target"],
            "Current":["212/day","74.7%",
                       "0.33%","98.18%","14 days"],
            "Target" :["Sustained","95%",
                       "20%+","70% max","3 days"],
            "Status" :["On Track","Below Target",
                       "Critical","Critical","Critical"]
        })
        def color_status(v):
            if v == "On Track":
                return f"color:{P['lgreen']};font-weight:600"
            elif v == "Critical":
                return f"color:{P['red']};font-weight:600"
            return f"color:{P['gold']};font-weight:600"
        st.dataframe(sc_df, use_container_width=True,
                     hide_index=True)
        wrn("Three of five delivery metrics are off target. Online adoption and geographic decentralisation require urgent attention.")

# ════════════════════════════════════════════════════════════
# PAGE 2: PASSPORT ANALYSIS
# ════════════════════════════════════════════════════════════
elif page == "Passport Analysis":
    with st.expander("Filters", expanded=False):
        sel_pp2 = st.multiselect("Passport Month",
            pp["Month"].tolist(),
            default=pp["Month"].tolist(), key="pp2")
    fpp2 = pp[pp["Month"].isin(sel_pp2)]

    k1,k2,k3,k4,k5 = st.columns(5)
    with k1: kpi("Total Produced",
                 f"{fpp2['Tot'].sum():,}","m")
    with k2: kpi("Ordinary",
                 f"{fpp2['Ord'].sum():,}")
    with k3: kpi("Service",
                 f"{fpp2['Svc'].sum():,}","g")
    with k4: kpi("Diplomatic (Exempt)",
                 f"{fpp2['Dip'].sum():,}")
    with k5: kpi("Est. Revenue",
                 f"${fpp2['Rev'].sum():,.0f}","b")

    st.markdown("")
    c1, c2 = st.columns(2)
    with c1:
        sec("Monthly Production by Passport Type")
        fig = go.Figure()
        for col,clr,nm in [
            ("Ord",P["lgreen"],"Ordinary"),
            ("Svc",P["lblue"],"Service"),
            ("Dip",P["gold"],"Diplomatic")]:
            fig.add_trace(go.Scatter(
                x=fpp2["MF"], y=fpp2[col], name=nm,
                mode="lines+markers",
                line=dict(color=clr,width=2.5),
                marker=dict(size=8,color=clr)))
        L(fig, 360, True)
        fig.update_yaxes(title_text="Passports Produced")
        st.plotly_chart(fig, use_container_width=True)
        wrn("Service passport production dropped 96% between March (108) and May (7). The cause remains unconfirmed by SLID and requires investigation.")

    with c2:
        sec("Passport Type: Volume and Revenue Share")
        td = pd.DataFrame({
            "Type":["Ordinary","Service","Diplomatic"],
            "Vol" :[fpp2["Ord"].sum(),
                    fpp2["Svc"].sum(),
                    fpp2["Dip"].sum()],
            "Rev" :[fpp2["Ord"].sum()*100,
                    fpp2["Svc"].sum()*100, 0]
        })
        fig2 = make_subplots(1,2,
            subplot_titles=["Volume Share","Revenue Share"],
            specs=[[{"type":"pie"},{"type":"pie"}]])
        for i,col in enumerate(["Vol","Rev"]):
            fig2.add_trace(go.Pie(
                labels=td["Type"],
                values=td[col], hole=0.5,
                textinfo="label+percent",
                marker_colors=[P["lgreen"],
                               P["lblue"],P["gold"]],
                textfont=dict(color=P["text"],size=11)),
                row=1,col=i+1)
        L(fig2,360,show_legend=False)
        for a in fig2.layout.annotations:
            a.font.color = P["sub"]
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("")
    c3, c4 = st.columns(2)
    with c3:
        sec("Month-over-Month Production Change")
        mom = fpp2.dropna(subset=["MoM"]).copy()
        fig3 = go.Figure(go.Bar(
            x=mom["MF"], y=mom["MoM"],
            marker_color=[P["lgreen"] if v>=0
                          else P["red"]
                          for v in mom["MoM"]]))
        fig3.add_hline(y=0,
            line_color=P["border"], line_width=1)
        L(fig3,320,show_legend=False)
        fig3.update_yaxes(title_text="Change in Volume")
        st.plotly_chart(fig3, use_container_width=True)
        ins("July recorded the highest single-month gain. May recorded the steepest decline. No consistent linear trend identified.")

    with c4:
        sec("Geographic Distribution: Production by Office")
        fig4 = px.scatter_geo(
            office, lat="Lat", lon="Lon",
            size="Total", color="Office",
            hover_name="Office",
            hover_data={"Total":True,"Pct":True,
                        "Lat":False,"Lon":False},
            size_max=60,
            color_discrete_sequence=COLORS,
            projection="natural earth")
        fig4.update_geos(
            visible=True, resolution=50,
            showcountries=True,
            countrycolor=P["mgray"],
            showcoastlines=True,
            coastlinecolor=P["mgray"],
            showland=True,
            landcolor=P["lgray"],
            showocean=True,
            oceancolor="#E3F2FD",
            showlakes=False,
            showsubunits=True,
            subunitcolor=P["border"],
            center={"lat":8.5,"lon":-11.8},
            lataxis_range=[6.5,10.5],
            lonaxis_range=[-14.5,-10.0],
            bgcolor="rgba(0,0,0,0)")
        fig4.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=320,
            font=dict(family="Inter",
                      color=P["sub"],size=11),
            margin=dict(l=0,r=0,t=28,b=0),
            legend=dict(bgcolor="rgba(0,0,0,0)",
                        font=dict(color=P["sub"])),
            geo_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig4, use_container_width=True)
        wrn("Freetown handles 98.18% of all passport production, creating a national single point of failure.")

# ════════════════════════════════════════════════════════════
# PAGE 3: RESIDENCY PERMIT ANALYSIS
# ════════════════════════════════════════════════════════════
elif page == "Residency Permit Analysis":
    with st.expander("Filters", expanded=False):
        rc1, rc2 = st.columns(2)
        with rc1:
            all_m3 = sorted(df["Month"].dropna().unique())
            sel_m3 = st.multiselect("Month", all_m3,
                                    default=all_m3, key="rp3")
        with rc2:
            cats   = ["All"]+sorted(
                df["Category"].dropna().unique())
            sel_c3 = st.selectbox("Category", cats,
                                  key="rc3")

    fdf3     = df[df["Month"].isin(sel_m3)]
    if sel_c3 != "All":
        fdf3 = fdf3[fdf3["Category"]==sel_c3]
    fdf3_all = df[df["Month"].isin(sel_m3)]

    k1,k2,k3,k4,k5 = st.columns(5)
    with k1: kpi("Total Applications",
                 f"{len(fdf3):,}")
    with k2:
        dr3 = (fdf3["Completion"]=="Delivered").mean()*100
        kpi("Delivery Rate",f"{dr3:.1f}%",
            "r" if dr3<80 else "")
    with k3: kpi("Not Delivered",
        f"{(fdf3['Completion']=='Not Delivered').sum():,}","r")
    with k4: kpi("Total Revenue",
        f"${fdf3['Amount ($)'].sum():,.0f}","g")
    with k5: kpi("Average Fee",
        f"${fdf3['Amount ($)'].mean():,.0f}","b")

    st.divider()
    sec("Volume and Status")
    c1, c2 = st.columns(2)
    with c1:
        sec("Monthly Volume and Revenue")
        m3 = fdf3.groupby("Month").agg(
            Apps=("Receipt Code","count"),
            Rev=("Amount ($)","sum")).reset_index()
        fig = make_subplots(specs=[[{"secondary_y":True}]])
        fig.add_trace(go.Bar(
            x=m3["Month"], y=m3["Apps"],
            name="Applications",
            marker_color=P["lblue"], opacity=0.85),
            secondary_y=False)
        fig.add_trace(go.Scatter(
            x=m3["Month"], y=m3["Rev"],
            name="Revenue ($)",
            mode="lines+markers",
            line=dict(color=P["lgreen"],width=2.5),
            marker=dict(size=8,color=P["lgreen"])),
            secondary_y=True)
        L(fig,340,True)
        fig.update_layout(barmode="relative")
        fig.update_yaxes(
            title_text="Applications",
            secondary_y=False,
            gridcolor=P["mgray"],
            tickfont=dict(color=P["sub"]))
        fig.update_yaxes(
            title_text="Revenue ($)",
            tickformat="$,.0f",
            secondary_y=True,
            gridcolor="rgba(0,0,0,0)",
            tickfont=dict(color=P["sub"]))
        st.plotly_chart(fig, use_container_width=True)
        ins("June 2026 was the peak month with 2,634 applications and $1.49M in revenue, driven by annual permit renewals.")

    with c2:
        sec("Application Status Distribution")
        sd = fdf3["Status_Name"].value_counts().reset_index()
        sd.columns = ["Status","Count"]
        bar_c = [P["lgreen"] if s=="Delivered"
                 else P["red"] if s in ["Rejected","Expired"]
                 else P["lblue"] for s in sd["Status"]]
        fig2 = go.Figure(go.Bar(
            x=sd["Count"], y=sd["Status"],
            orientation="h", marker_color=bar_c))
        L(fig2,340,show_legend=False)
        fig2.update_xaxes(title_text="Count")
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()
    sec("Category Analysis (All Categories)")
    c3, c4, c5 = st.columns(3)
    cs = fdf3_all.groupby("Category",dropna=False).agg(
        Count=("Receipt Code","count"),
        Revenue=("Amount ($)","sum"),
        DR=("Completion_Binary","mean")).reset_index()
    cs["Category"] = cs["Category"].fillna("Unknown")
    cs["DR"] = (cs["DR"]*100).round(1)

    with c3:
        sec("Applications by Category")
        fig3 = go.Figure(go.Bar(
            x=cs["Category"], y=cs["Count"],
            marker_color=P["lblue"]))
        L(fig3,300,show_legend=False)
        fig3.update_xaxes(tickangle=-20,
            tickfont=dict(color=P["sub"],size=9))
        fig3.update_yaxes(title_text="Applications")
        st.plotly_chart(fig3, use_container_width=True)

    with c4:
        sec("Revenue by Category")
        fig4 = go.Figure(go.Bar(
            x=cs["Category"], y=cs["Revenue"],
            marker_color=P["lgreen"]))
        L(fig4,300,show_legend=False)
        fig4.update_xaxes(tickangle=-20,
            tickfont=dict(color=P["sub"],size=9))
        fig4.update_yaxes(tickformat="$,.0f",
                          title_text="Revenue ($)")
        st.plotly_chart(fig4, use_container_width=True)

    with c5:
        sec("Delivery Rate by Category")
        dr_c = [P["lgreen"] if v>80
                else P["gold"] if v>60
                else P["red"] for v in cs["DR"]]
        fig5 = go.Figure(go.Bar(
            x=cs["Category"], y=cs["DR"],
            marker_color=dr_c))
        fig5.add_hline(y=74.7, line_dash="dash",
                       line_color=P["gold"],
                       annotation_text="74.7% avg",
                       annotation_font_color=P["gold"])
        L(fig5,300,show_legend=False)
        fig5.update_xaxes(tickangle=-20,
            tickfont=dict(color=P["sub"],size=9))
        fig5.update_yaxes(title_text="Delivery Rate (%)",
                          range=[0,115])
        st.plotly_chart(fig5, use_container_width=True)
        ins("Category B records the highest delivery rate and revenue. Categories D and E show below-average delivery performance.")

    st.divider()
    sec("Operational Patterns and Segmentation")
    c6, c7, c8 = st.columns(3)
    with c6:
        sec("Revenue by Role: Top 10")
        role_rev = fdf3_all.groupby(
            "Role",dropna=False)["Amount ($)"].agg(
            ["sum","count"]).sort_values(
            "sum",ascending=False).head(10).reset_index()
        role_rev.columns = ["Role","Total Revenue","Count"]
        role_rev["Role"] = role_rev["Role"].fillna("Unknown")
        fig6 = go.Figure(go.Bar(
            x=role_rev["Total Revenue"],
            y=role_rev["Role"],
            orientation="h",
            marker_color=[P["lgreen"] if i<3
                          else P["lblue"] if i<6
                          else P["mgray"]
                          for i in range(len(role_rev))],
            opacity=0.9,
            customdata=role_rev["Count"],
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Revenue: $%{x:,.0f}<br>"
                "Applications: %{customdata:,}"
                "<extra></extra>")))
        L(fig6,360,show_legend=False)
        fig6.update_xaxes(tickformat="$,.0f",
                          title_text="Total Revenue ($)")
        fig6.update_yaxes(
            categoryorder="total ascending",
            tickfont=dict(color=P["sub"],size=8))
        st.plotly_chart(fig6, use_container_width=True)
        ins("General Merchandise is the top revenue-generating role, followed by NGOs and Health Services.")

    with c7:
        sec("Applications by Day of Week")
        do  = ["Monday","Tuesday","Wednesday",
               "Thursday","Friday","Saturday"]
        dow = fdf3["Day_of_Week"].value_counts()\
              .reindex(do).dropna().reset_index()
        dow.columns = ["Day","Count"]
        fig7 = go.Figure(go.Bar(
            x=dow["Day"], y=dow["Count"],
            marker_color=[P["lgreen"] if d=="Friday"
                          else P["lblue"] if d=="Thursday"
                          else P["mgray"]
                          for d in dow["Day"]]))
        L(fig7,360,show_legend=False)
        fig7.update_xaxes(tickangle=-20,
            tickfont=dict(color=P["sub"],size=9))
        fig7.update_yaxes(title_text="Applications")
        st.plotly_chart(fig7, use_container_width=True)
        ins("Friday records the highest application volume. Saturday is consistently the lowest, reflecting reduced operating hours.")

    with c8:
        sec("Applicant Segments: K-Means (k=4)")
        cl = pd.DataFrame({
            "Cluster":["Cluster 0","Cluster 1",
                       "Cluster 2","Cluster 3"],
            "Size"   :[2934,6104,1649,373],
            "Fee"    :[225,709,744,0],
            "DR"     :[67,100,0,47],
        })
        fig8 = go.Figure()
        for i,row in cl.iterrows():
            fig8.add_trace(go.Scatter(
                x=[row["Fee"]],y=[row["DR"]],
                mode="markers+text",
                marker=dict(
                    size=max(row["Size"]/65,12),
                    color=COLORS[i],opacity=0.85,
                    line=dict(color="white",width=1.5)),
                text=[row["Cluster"]],
                textposition="top center",
                textfont=dict(color=P["sub"],size=9),
                name=row["Cluster"],
                hovertemplate=(
                    f"<b>{row['Cluster']}</b><br>"
                    f"Size: {row['Size']:,}<br>"
                    f"Avg Fee: ${row['Fee']}<br>"
                    f"Delivery: {row['DR']}%"
                    "<extra></extra>")))
        L(fig8,360,show_legend=False)
        fig8.update_xaxes(title_text="Average Fee ($)")
        fig8.update_yaxes(title_text="Delivery Rate (%)")
        st.plotly_chart(fig8, use_container_width=True)
        wrn("Cluster 2: 1,649 applicants paid an average of $744 but received no permit at the time of data extraction. This $1.23M backlog is concentrated in June and July 2026.")

# ════════════════════════════════════════════════════════════
# PAGE 4: LEAD TIME ANALYSIS
# ════════════════════════════════════════════════════════════
elif page == "Lead Time Analysis":
    sec("Delivery Chain Analysis: From Application to Delivery")

    st.markdown(f"""
    <div class="fnd">
    The Theory of Constraints (Goldratt, 1984) identifies the bottleneck
    as the stage that determines system throughput. In SLID's delivery
    chain, the subcontracted card/passport production stage dominates
    total processing time. A permit is not complete until it is physically
    delivered to the applicant, regardless of how quickly internal
    processing stages are completed.
    </div>""", unsafe_allow_html=True)

    st.markdown("")

    # Pipeline stage analysis
    c1, c2 = st.columns([1.2, 1])
    with c1:
        sec("Estimated Stage Duration: AS-IS vs TO-BE")
        stages = ["Submission\nto Approval",
                  "Approval to\nProduction",
                  "External\nProduction",
                  "Return to\nReady for Pickup",
                  "Ready for Pickup\nto Collected"]
        asis   = [2, 1.5, 8.5, 1, 3]
        tobe   = [0.5, 0.25, 1, 0.25, 0.5]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            name="AS-IS (Current)",
            x=stages, y=asis,
            marker_color=P["red"], opacity=0.85))
        fig.add_trace(go.Bar(
            name="TO-BE (Recommended)",
            x=stages, y=tobe,
            marker_color=P["lgreen"], opacity=0.85))
        fig.add_hline(
            y=sum(tobe), line_dash="dash",
            line_color=P["lblue"],
            annotation_text=f"TO-BE Total: {sum(tobe):.1f} days",
            annotation_font_color=P["lblue"])
        fig.add_hline(
            y=sum(asis), line_dash="dash",
            line_color=P["red"],
            annotation_text=f"AS-IS Total: ~{sum(asis):.0f} days",
            annotation_font_color=P["red"],
            annotation_position="bottom right")
        L(fig, 400, True)
        fig.update_layout(barmode="group")
        fig.update_yaxes(title_text="Days",range=[0,12])
        fig.update_xaxes(tickfont=dict(
            color=P["sub"],size=9))
        st.plotly_chart(fig, use_container_width=True)
        st.caption(
            "Stage durations estimated from stakeholder "
            "interviews (AS-IS) and queuing model analysis "
            "(TO-BE). Individual application timestamps not "
            "recorded in current platform.")

    with c2:
        sec("Bottleneck Contribution to Total Wait")
        labels = ["External Production\n(~61% of wait)",
                  "Collection Delay\n(~21% of wait)",
                  "Submission to Approval\n(~14% of wait)",
                  "Other Stages\n(~4% of wait)"]
        vals   = [8.5, 3, 2, 0.5]
        fig2 = go.Figure(go.Pie(
            labels=labels, values=vals,
            hole=0.55,
            marker_colors=[P["red"],P["gold"],
                           P["lblue"],P["mgray"]],
            textinfo="label+percent",
            textfont=dict(color=P["text"],size=10)))
        L(fig2, 400, show_legend=False)
        st.plotly_chart(fig2, use_container_width=True)
        wrn("External card production accounts for approximately 61% of total processing time. This stage is subcontracted and currently operates with no SLA, no tracking, and no penalty mechanism.")

    st.divider()
    sec("Days in System: Distribution for All Applications")

    c3, c4 = st.columns(2)
    with c3:
        sec("Distribution of Days in System")
        valid = df[df["Days_in_System"].between(0,300)]
        fig3 = go.Figure()
        fig3.add_trace(go.Histogram(
            x=valid[valid["Completion"]=="Delivered"]\
              ["Days_in_System"],
            name="Delivered",
            marker_color=P["lgreen"], opacity=0.75,
            nbinsx=40))
        fig3.add_trace(go.Histogram(
            x=valid[valid["Completion"]=="Not Delivered"]\
              ["Days_in_System"],
            name="Not Delivered",
            marker_color=P["red"], opacity=0.75,
            nbinsx=40))
        fig3.add_vline(
            x=valid["Days_in_System"].median(),
            line_dash="dash",
            line_color=P["lblue"],
            annotation_text=f"Median: {valid['Days_in_System'].median():.0f}d",
            annotation_font_color=P["lblue"])
        L(fig3, 360, True)
        fig3.update_layout(barmode="overlay")
        fig3.update_xaxes(title_text="Days in System")
        fig3.update_yaxes(title_text="Number of Applications")
        st.plotly_chart(fig3, use_container_width=True)
        med = valid["Days_in_System"].median()
        p75 = valid["Days_in_System"].quantile(0.75)
        ins(f"Median days in system: {med:.0f} days. 75th percentile: {p75:.0f} days. Applications still awaiting delivery have been in the system significantly longer than delivered ones.")

    with c4:
        sec("Average Days in System by Month")
        monthly_lt = df.groupby("Month").agg(
            Avg_Days=("Days_in_System","mean"),
            Count=("Receipt Code","count"),
            Delivered=("Completion_Binary","sum")
        ).reset_index()
        monthly_lt["DR"] = (
            monthly_lt["Delivered"] /
            monthly_lt["Count"] * 100).round(1)

        fig4 = make_subplots(specs=[[{"secondary_y":True}]])
        fig4.add_trace(go.Bar(
            x=monthly_lt["Month"],
            y=monthly_lt["Avg_Days"],
            name="Avg Days in System",
            marker_color=P["lblue"], opacity=0.8),
            secondary_y=False)
        fig4.add_trace(go.Scatter(
            x=monthly_lt["Month"],
            y=monthly_lt["DR"],
            name="Delivery Rate (%)",
            mode="lines+markers",
            line=dict(color=P["lgreen"],width=2.5),
            marker=dict(size=8,color=P["lgreen"])),
            secondary_y=True)
        L(fig4, 360, True)
        fig4.update_yaxes(
            title_text="Avg Days in System",
            secondary_y=False,
            gridcolor=P["mgray"])
        fig4.update_yaxes(
            title_text="Delivery Rate (%)",
            secondary_y=True,
            gridcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig4, use_container_width=True)
        fnd("Applications submitted in more recent months show higher average days in system because less time has elapsed for delivery to occur. Earlier months show higher delivery rates as more applications have had time to complete the full cycle.")

    st.divider()
    sec("Status Pipeline: Where Applications Are Stuck")

    status_breakdown = df["Status_Name"].value_counts()\
        .reset_index()
    status_breakdown.columns = ["Status","Count"]
    status_breakdown["Pct"] = (
        status_breakdown["Count"] /
        len(df) * 100).round(1)
    status_breakdown["Stage"] = status_breakdown["Status"].map({
        "Delivered"          : "Complete",
        "Ready To Pickup"    : "Post-Production (at SLID)",
        "Printed"            : "Post-Production (at SLID)",
        "New"                : "Internal Processing",
        "Draft"              : "Internal Processing",
        "Appointment Needed" : "Internal Processing",
        "Need Extra Document": "Internal Processing",
        "Needs Edit"         : "Internal Processing",
        "Rejected"           : "Terminal",
        "Expired"            : "Terminal",
    }).fillna("Other")

    c5, c6 = st.columns(2)
    with c5:
        color_map = {
            "Complete"               : P["lgreen"],
            "Post-Production (at SLID)": P["gold"],
            "Internal Processing"    : P["lblue"],
            "Terminal"               : P["red"],
            "Other"                  : P["mgray"],
        }
        fig5 = go.Figure(go.Bar(
            x=status_breakdown["Count"],
            y=status_breakdown["Status"],
            orientation="h",
            marker_color=[color_map.get(
                s, P["mgray"])
                for s in status_breakdown["Stage"]],
            customdata=status_breakdown["Pct"],
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Count: %{x:,}<br>"
                "Share: %{customdata:.1f}%"
                "<extra></extra>")))
        L(fig5, 360, show_legend=False)
        fig5.update_xaxes(title_text="Applications")
        st.plotly_chart(fig5, use_container_width=True)

    with c6:
        # Pipeline funnel
        funnel_stages = [
            "Submitted (11,118)",
            "Internally Processed",
            "Sent to Production",
            "Returned from Production",
            "Delivered to Applicant"
        ]
        funnel_vals = [11118, 9500, 8800, 8500, 8304]
        fig6 = go.Figure(go.Funnel(
            y=funnel_stages,
            x=funnel_vals,
            textposition="inside",
            textinfo="value+percent initial",
            marker_color=[P["lblue"],P["mblue"],
                          P["lgreen"],P["tgreen"],
                          P["lgreen"]],
            connector={"line":{"color":P["border"],
                               "width":2}}))
        L(fig6, 360, show_legend=False)
        fig6.update_layout(
            margin=dict(l=180,r=20,t=28,b=0))
        st.plotly_chart(fig6, use_container_width=True)
        ins("The delivery funnel shows attrition between production and final delivery. The OTP notification failure means cards returned from production sit uncollected at the SLID counter.")

# ════════════════════════════════════════════════════════════
# PAGE 5: PROCESS PERFORMANCE (M/M/s)
# ════════════════════════════════════════════════════════════
elif page == "Process Performance":
    sec("M/M/s Queuing Model: Real-Time Capacity Analysis")

    pc1, pc2, pc3 = st.columns(3)
    with pc1:
        lam   = st.number_input(
            "Daily applications (lambda)",
            1, 400, 51, 1, key="lam")
    with pc2:
        s_in  = st.number_input(
            "Officers available (s)",
            1, 20, 3, 1, key="sin")
    with pc3:
        mu_in = st.number_input(
            "Applications per officer per day (mu)",
            1, 50, 5, 1, key="muin")

    m_ = mms(lam, mu_in, s_in)

    if m_["stable"]:
        st.markdown(f"""
        <div style="background:rgba(27,94,32,0.08);
          border:2px solid {P['lgreen']};
          border-radius:10px;padding:1rem 1.5rem;
          text-align:center;">
          <h3 style="color:{P['lgreen']};margin:0;">
            SYSTEM STABLE</h3>
          <p style="margin:0.4rem 0 0;color:{P['sub']};">
          Utilisation: <b>{m_['rho']*100:.1f}%</b>
          &nbsp;|&nbsp;
          Processing time: <b>{m_['W']:.3f} days
          ({m_['W']*8:.1f} hours)</b>
          &nbsp;|&nbsp;
          Average queue: <b>{m_['Lq']:.1f} applications</b>
          </p></div>""", unsafe_allow_html=True)
    else:
        cap   = s_in * mu_in
        extra = int(np.ceil((lam-cap)/mu_in))
        st.markdown(f"""
        <div style="background:rgba(198,40,40,0.08);
          border:2px solid {P['red']};
          border-radius:10px;padding:1rem 1.5rem;
          text-align:center;">
          <h3 style="color:{P['red']};margin:0;">
            SYSTEM OVERLOADED</h3>
          <p style="margin:0.4rem 0 0;color:{P['sub']};">
          Capacity: <b>{cap}/day</b>
          &nbsp;|&nbsp;
          Demand: <b>{lam}/day</b>
          &nbsp;|&nbsp;
          Requires at least
          <b>{extra} additional officer(s)</b>
          </p></div>""", unsafe_allow_html=True)

    st.markdown("")
    c1, c2 = st.columns(2)
    with c1:
        sec("Processing Time Across Demand Scenarios")
        demands = {
            "Jan (Low)":11.62,"Feb":37.96,"Mar":37.93,
            "Apr":55.43,"May":68.26,"Jun (Peak)":87.80,
            "Jul":52.87,"Aug":42.67
        }
        scenarios = {
            "AS-IS (s=3, mu=5)"       :(3,5,  P["red"]),
            "Min Viable (s=6, mu=12)" :(6,12, P["gold"]),
            "Recommended (s=8, mu=12)":(8,12, P["lgreen"]),
            "Optimal (s=10, mu=12)"   :(10,12,P["lblue"]),
        }
        fig = go.Figure()
        for lb,(sc,mv,col) in scenarios.items():
            Wv = [mms(lv,mv,sc)["W"]
                  if mms(lv,mv,sc)["stable"]
                  else None
                  for lv in demands.values()]
            fig.add_trace(go.Scatter(
                x=list(demands.keys()),y=Wv,
                mode="lines+markers",name=lb,
                line=dict(color=col,width=2.5),
                marker=dict(size=8,color=col),
                connectgaps=False))
        fig.add_hline(y=1.0,line_dash="dash",
                      line_color=P["lblue"],
                      annotation_text="1-day target",
                      annotation_font_color=P["lblue"])
        fig.add_hline(y=3.0,line_dash="dot",
                      line_color=P["mgray"],
                      annotation_text="3-day target",
                      annotation_font_color=P["mgray"])
        L(fig,400,True)
        fig.update_yaxes(title_text="Days in System (W)",
                         range=[0,6])
        fig.update_xaxes(title_text="Month")
        st.plotly_chart(fig, use_container_width=True)
        ins("The recommended configuration of 8 officers at mu=12 maintains stability across all months, including the June peak of 87.80 applications per day.")

    with c2:
        sec(f"Sensitivity Analysis: Processing Time at lambda={lam}/day")
        sr  = list(range(3,14))
        mr  = [5,8,10,12,15,20]
        hd  = []
        for sc in sr:
            row = {"Servers (s)":sc}
            for mv in mr:
                r = mms(lam,mv,sc)
                row[f"mu={mv}"] = (round(r["W"],3)
                    if r["stable"] else None)
            hd.append(row)
        hdf = pd.DataFrame(hd).set_index("Servers (s)")
        fig2 = px.imshow(
            hdf, text_auto=".2f", aspect="auto",
            color_continuous_scale="RdYlGn_r",
            labels={"x":"Service Rate (mu)",
                    "y":"Servers (s)",
                    "color":"Days"})
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=400,
            font=dict(family="Inter",
                      color=P["sub"],size=11),
            margin=dict(l=0,r=0,t=28,b=0))
        fig2.update_xaxes(
            tickfont=dict(color=P["sub"]))
        fig2.update_yaxes(
            tickfont=dict(color=P["sub"]))
        st.plotly_chart(fig2, use_container_width=True)
        ins("Each cell shows the average waiting time in days for a given staffing and technology combination. Empty cells indicate system collapse. Moving right reflects digitisation gains.")

    st.markdown("")
    sec("Scenario Configuration Summary")
    rows = []
    for lb,(sc,mv,_) in scenarios.items():
        am = mms(50.77,mv,sc)
        pm = mms(87.80,mv,sc)
        rows.append({
            "Scenario"     : lb,
            "Officers"     : sc,
            "mu"           : mv,
            "Avg W (days)" : (f"{am['W']:.4f}"
                if am["stable"] else "UNSTABLE"),
            "Peak W (days)": (f"{pm['W']:.4f}"
                if pm["stable"] else "UNSTABLE"),
            "Feasible"     : ("Yes"
                if am["stable"] and pm["stable"]
                else "No")
        })
    st.dataframe(pd.DataFrame(rows),
                 use_container_width=True,
                 hide_index=True)

# ════════════════════════════════════════════════════════════
# PAGE 6: REVENUE FORECAST
# ════════════════════════════════════════════════════════════
elif page == "Revenue Forecast":
    c1, c2 = st.columns(2)
    with c1:
        sec("Residency Permit: OLS Linear Trend Forecast")
        rm = df.groupby("Month")[
            "Amount ($)"].sum().reset_index()
        rm.columns = ["Month","Revenue"]
        rm["MI"]   = np.arange(1,len(rm)+1)
        md = rm.iloc[:7].copy()
        Xo = sm.add_constant(md["MI"])
        yo = md["Revenue"]
        ols = sm.OLS(yo,Xo).fit()
        fut = pd.DataFrame({
            "Month":["2026-09","2026-10",
                     "2026-11","2026-12"],
            "MI":[9,10,11,12]})
        fXo  = sm.add_constant(
            fut["MI"],has_constant="add")
        pred = ols.get_prediction(fXo)\
               .summary_frame(alpha=0.05)
        fut["Fc"] = pred["mean"].values
        fut["Lo"] = pred["obs_ci_lower"].values
        fut["Hi"] = pred["obs_ci_upper"].values

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=rm["Month"],y=rm["Revenue"],
            name="Actual",mode="lines+markers",
            line=dict(color=P["lgreen"],width=2.5),
            marker=dict(size=8,color=P["lgreen"])))
        fig.add_trace(go.Scatter(
            x=fut["Month"],y=fut["Fc"],
            name="OLS Forecast",
            mode="lines+markers",
            line=dict(color=P["lblue"],
                      width=2,dash="dash"),
            marker=dict(size=8,symbol="diamond",
                        color=P["lblue"])))
        fig.add_trace(go.Scatter(
            x=list(fut["Month"])+
              list(fut["Month"][::-1]),
            y=list(fut["Hi"])+
              list(fut["Lo"][::-1]),
            fill="toself",
            fillcolor="rgba(21,101,192,0.08)",
            line=dict(color="rgba(0,0,0,0)"),
            name="95% Interval"))
        L(fig,400,True)
        fig.update_yaxes(tickformat="$,.0f",
                         title_text="Revenue ($)")
        st.plotly_chart(fig, use_container_width=True)
        st.caption(
            f"R-squared = {ols.rsquared:.3f} | "
            f"Monthly trend: ${ols.params['MI']:,.0f} | "
            f"Fitted on Jan-Jul 2026 (n=7)")

    with c2:
        sec("Passport: Scenario-Based Projection")
        pf_m = ["2026-08","2026-09","2026-10",
                "2026-11","2026-12"]
        pf   = pd.DataFrame({
            "Month"       : pf_m,
            "Conservative": [pp["Rev"].min()]*5,
            "Midpoint"    : [pp["Rev"].mean()]*5,
            "Optimistic"  : [pp["Rev"].max()]*5,
        })
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=pp["MF"],y=pp["Rev"],
            name="Actual",mode="lines+markers",
            line=dict(color=P["lgreen"],width=2.5),
            marker=dict(size=8,color=P["lgreen"])))
        for lb,col,dsh in [
            ("Optimistic",  P["lblue"], "dashdot"),
            ("Midpoint",    P["lgreen"],"dash"),
            ("Conservative",P["gold"],  "dot"),
        ]:
            fig2.add_trace(go.Scatter(
                x=pf["Month"],y=pf[lb],name=lb,
                mode="lines+markers",
                line=dict(color=col,
                          width=2,dash=dsh),
                marker=dict(size=8,symbol="diamond",
                            color=col)))
        L(fig2,400,True)
        fig2.update_yaxes(tickformat="$,.0f",
                          title_text="Revenue ($)")
        st.plotly_chart(fig2, use_container_width=True)
        st.caption(
            "Scenario-based projection. No consistent "
            "linear trend identified in passport data.")

    st.markdown("")
    sec("2026 Combined Revenue Projection")
    pa   = pp["Rev"].sum()
    ra   = df["Amount ($)"].sum()
    scens = {
        "Conservative": (pp["Rev"].min()*5,   9649100),
        "Midpoint"    : (pp["Rev"].mean()*5, 11789332),
        "Optimistic"  : (pp["Rev"].max()*5,  13929564),
    }
    fig3 = go.Figure()
    for nm,col in [
        ("Passport Actual",   P["lgreen"]),
        ("Passport Projected",P["tgreen"]),
        ("Permit Actual",     P["lblue"]),
        ("Permit Projected",  P["tblue"]),
    ]:
        vals = []
        for sc,(pp_,rp_) in scens.items():
            if   nm=="Passport Actual":     vals.append(pa)
            elif nm=="Passport Projected":  vals.append(pp_)
            elif nm=="Permit Actual":       vals.append(ra)
            else: vals.append(rp_-ra)
        fig3.add_trace(go.Bar(
            name=nm,
            x=list(scens.keys()),y=vals,
            marker_color=col,opacity=0.88))

    tots = [pa+v[0]+v[1] for v in scens.values()]
    for sc,tot in zip(scens.keys(),tots):
        fig3.add_annotation(
            x=sc, y=tot+150000,
            text=f"<b>${tot/1e6:.1f}M</b>",
            showarrow=False,
            font=dict(size=13,color=P["text"]))
    L(fig3,420,True)
    fig3.update_layout(barmode="stack")
    fig3.update_yaxes(tickformat="$,.0f",
                      title_text="Revenue (USD)")
    st.plotly_chart(fig3, use_container_width=True)

    rows2 = []
    for sc,(pp_,rp_) in scens.items():
        rows2.append({
            "Scenario"         : sc,
            "Passport Full Year": f"${pa+pp_:,.0f}",
            "Permit Full Year"  : f"${rp_:,.0f}",
            "Combined Total"    : f"${pa+pp_+rp_:,.0f}"
        })
    st.dataframe(pd.DataFrame(rows2),
                 use_container_width=True,
                 hide_index=True)
    st.caption(
        "Passport revenue estimated at $100 per passport "
        "(Ordinary and Service). Diplomatic passports are "
        "fee-exempt. Source: SLID official fee schedule.")

# ════════════════════════════════════════════════════════════
# PAGE 7: PREDICTIVE ANALYTICS
# ════════════════════════════════════════════════════════════
elif page == "Predictive Analytics":
    acc_disp = f"{acc_*100:.1f}%" if ok else "N/A"
    auc_disp = f"{auc_:.3f}"     if ok else "N/A"

    st.markdown(
        f'<p style="font-size:0.85rem;color:{P["sub"]};">'
        f'Logistic regression model trained on 11,118 '
        f'residency permit records. '
        f'<b style="color:{P["text"]};">'
        f'AUC = {auc_disp} &nbsp;|&nbsp; '
        f'Accuracy = {acc_disp}</b>. '
        f'Predicts delivery likelihood from '
        f'application characteristics at point of '
        f'submission.</p>',
        unsafe_allow_html=True)

    if not ok:
        st.error(
            "Model could not be trained. Verify that "
            "SLID_Residency_Final_Cleaned.xlsx is in "
            "the repository.")
        st.stop()

    pc1, pc2 = st.columns([1,1])
    with pc1:
        sec("Application Input")
        cat_in  = st.selectbox(
            "Permit Category",
            meta_.get("categories",["Category B"]),
            key="pcat")
        prc_in  = st.selectbox(
            "Process Code",
            meta_.get("process_codes",["Resident Permit"]),
            key="pprc")
        amt_in  = st.slider(
            "Payment Amount ($)",
            int(meta_.get("amount_min",0)),
            int(meta_.get("amount_max",1000)),
            int(meta_.get("amount_mean",500)),
            50, key="pamt")
        mon_in  = st.selectbox(
            "Month of Application",
            list(range(1,13)),
            format_func=lambda x:[
                "Jan","Feb","Mar","Apr","May","Jun",
                "Jul","Aug","Sep","Oct","Nov","Dec"
            ][x-1],
            index=5, key="pmon")
        dow_in  = st.selectbox(
            "Day of Week",
            ["Monday","Tuesday","Wednesday",
             "Thursday","Friday","Saturday"],
            key="pdow")
        go_btn  = st.button(
            "Predict Outcome",
            use_container_width=True)

    with pc2:
        sec("Prediction Result")
        if go_btn:
            try:
                dm = {"Monday":0,"Tuesday":1,
                      "Wednesday":2,"Thursday":3,
                      "Friday":4,"Saturday":5}
                try:
                    ce = lc_.transform([cat_in])[0]
                except Exception:
                    ce = 0
                try:
                    pe = lp_.transform([prc_in])[0]
                except Exception:
                    pe = 0
                Xi  = np.array([[amt_in,mon_in,
                                 dm[dow_in],ce,pe]])
                Xs  = sc_.transform(Xi)
                pd_ = lr_.predict_proba(Xs)[0][1]

                if pd_ >= 0.75:
                    css = (f"background:rgba(27,94,32,0.08);"
                           f"border:2px solid {P['lgreen']};")
                    vd  = "LOW RISK: Likely to be Delivered"
                    ac  = ("Process normally. No immediate "
                           "intervention required.")
                    gc  = P["lgreen"]
                elif pd_ >= 0.50:
                    css = (f"background:rgba(249,168,37,0.08);"
                           f"border:2px solid {P['gold']};")
                    vd  = "MEDIUM RISK: Monitor Closely"
                    ac  = ("Flag for follow-up. Verify document "
                           "completeness. Assign to senior officer.")
                    gc  = P["gold"]
                else:
                    css = (f"background:rgba(198,40,40,0.08);"
                           f"border:2px solid {P['red']};")
                    vd  = "HIGH RISK: Application Likely to Stall"
                    ac  = ("Escalate immediately. Conduct priority "
                           "identity verification. Assign for "
                           "manual review.")
                    gc  = P["red"]

                st.markdown(f"""
                <div style="{css}border-radius:10px;
                  padding:1rem 1.2rem;text-align:center;">
                  <h3 style="color:{gc};margin:0;">{vd}</h3>
                  <h2 style="color:{P['text']};margin:0.4rem 0;">
                    Delivery Probability: {pd_*100:.1f}%</h2>
                  <p style="color:{P['sub']};font-size:0.82rem;
                    margin:0.4rem 0 0;">
                    <b>Recommended Action:</b> {ac}</p>
                </div>""", unsafe_allow_html=True)

                st.markdown("")
                fg = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=pd_*100,
                    title={"text":"Delivery Probability (%)"},
                    number={"font":{"color":P["text"]}},
                    gauge={
                        "axis":{"range":[0,100]},
                        "bar":{"color":gc},
                        "steps":[
                            {"range":[0,50],
                             "color":"rgba(198,40,40,0.1)"},
                            {"range":[50,75],
                             "color":"rgba(249,168,37,0.1)"},
                            {"range":[75,100],
                             "color":"rgba(27,94,32,0.1)"},
                        ],
                        "threshold":{
                            "line":{"color":P["sub"],
                                    "width":2},
                            "thickness":0.75,"value":74.7}
                    }))
                fg.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    height=260,
                    font=dict(family="Inter",
                              color=P["sub"],size=11),
                    margin=dict(l=20,r=20,t=40,b=20))
                st.plotly_chart(fg,
                                use_container_width=True)

                sec("Feature Influence on Prediction")
                cdf = pd.DataFrame({
                    "Feature":["Amount ($)","Month",
                               "Day of Week","Category",
                               "Process Code"],
                    "Coef":lr_.coef_[0]
                }).sort_values("Coef")
                fc = go.Figure(go.Bar(
                    x=cdf["Coef"],
                    y=cdf["Feature"],
                    orientation="h",
                    marker_color=[
                        P["lgreen"] if v>0
                        else P["red"]
                        for v in cdf["Coef"]]))
                fc.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor=P["offwhite"],
                    height=240,showlegend=False,
                    font=dict(family="Inter",
                              color=P["sub"],size=11),
                    margin=dict(l=0,r=0,t=20,b=0))
                fc.update_xaxes(
                    gridcolor=P["mgray"],
                    title_text="Coefficient")
                fc.update_yaxes(gridcolor=P["mgray"])
                st.plotly_chart(fc,
                                use_container_width=True)

            except Exception as e:
                st.error(f"Prediction error: {e}")
        else:
            st.info(
                "Fill in the application details on the "
                "left and click Predict Outcome.")
            sec("Model Performance")
            st.dataframe(pd.DataFrame({
                "Metric":["Accuracy","ROC-AUC",
                          "Recall (Delivered)",
                          "Recall (Not Delivered)",
                          "Training Records"],
                "Value" :[acc_disp,auc_disp,
                          "~93%","~51%","~8,894"]
            }), use_container_width=True,
                hide_index=True)

            st.markdown("")
            sec("K-Means Cluster Profiles (k=4)")
            st.dataframe(pd.DataFrame({
                "Cluster":["Cluster 0","Cluster 1",
                           "Cluster 2","Cluster 3"],
                "Size"   :[2934,6104,1649,373],
                "Avg Fee ($)":[225,709,744,0],
                "Delivery Rate":["67%","100%","0%","47%"],
                "Revenue at Risk":["","","$1,226,800",""],
                "Segment":[
                    "Low-fee, NGO/Diplomatic applicants",
                    "High-fee, commercial. Fully processed.",
                    "High-fee, paid in full. No permit issued at extraction date. $1.23M backlog.",
                    "Zero-fee. Diplomatic exemptions.",
                ]
            }), use_container_width=True,
                hide_index=True)
            wrn("Cluster 2 represents 1,649 applicants who paid in full but received no permit at the data extraction date. This is a production pipeline backlog, not a rejection.")
