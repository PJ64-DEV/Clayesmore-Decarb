import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy_financial as npf
from io import StringIO

# =================================================================================================
# PAGE CONFIGURATION
# =================================================================================================
st.set_page_config(
    page_title="Clayesmore School LED Proposal",
    page_icon="💡",
    layout="wide"
)

# =================================================================================================
# --- DATA LOADING AND PROCESSING ---
# This section parses the raw text data you provided.
# =================================================================================================

RAW_DATA = """
EXISTING FITTINGS
Area,Existing Lamp,Quantity,Wattage,kW/Hour,Hours per Day,Days,Total kWh Per annum,Existing Running Cost,CO2 Tns
CIRCULATION,28W,45,31,1.40,7,220,2148,£537.08,0.50
CIRCULATION,125W,1,138,0.14,7,220,213,£53.13,0.05
CIRCULATION,58W,5,64,0.32,7,220,493,£123.20,0.11
CIRCULATION,2X58W,4,128,0.51,7,220,788,£197.12,0.18
CIRCULATION,4X18W,16,79,1.26,7,220,1947,£486.64,0.45
CIRCULATION,2X55W,50,121,6.05,7,220,9317,"£2,329.25",2.17
CIRCULATION,32W,36,36,1.30,7,220,1996,£498.96,0.47
CIRCULATION,38W,13,42,0.55,7,220,841,£210.21,0.20
CIRCULATION,36W,12,40,0.48,7,220,739,£184.80,0.17
CIRCULATION,2X18W,25,40,1.00,7,220,1540,£385.00,0.36
CIRCULATION,2X26W,19,58,1.10,7,220,1697,£424.27,0.40
CIRCULATION,70W ,1,78,0.08,7,220,120,£30.03,0.03
CIRCULATION,16W,1,18,0.02,7,220,28,£6.93,0.01
CIRCULATION,3X18W,1,60,0.06,7,220,92,£23.10,0.02
CIRCULATION,3X55W,7,182,1.27,7,220,1962,£490.49,0.46
BEDROOM,2X58W,19,128,2.43,5,220,2675,£668.80,0.62
BEDROOM,28W,41,31,1.27,5,220,1398,£349.53,0.33
BEDROOM,16W,31,18,0.56,5,220,614,£153.45,0.14
BEDROOM,70W,1,77,0.08,5,220,85,£21.18,0.02
BEDROOM,36W,3,40,0.12,5,220,132,£33.00,0.03
BEDROOM,58W,1,64,0.06,5,220,70,£17.60,0.02
CHANGING ROOM,58W,13,64,0.83,6,220,1098,£274.56,0.26
CHANGING ROOM,28W,13,31,0.40,6,220,532,£132.99,0.12
CHANGING ROOM,4X18W,35,79,2.77,6,220,3650,£912.45,0.85
CHANGING ROOM,70W,7,77,0.54,6,220,711,£177.87,0.17
CHANGING ROOM,2X58W,8,128,1.02,6,220,1352,£337.92,0.31
CHANGING ROOM,2X70W,4,154,0.62,6,220,813,£203.28,0.19
CLASSROOM,2X58W,59,128,7.55,7,220,11630,"£2,907.52",2.71
CLASSROOM,4X18W,90,79,7.11,7,220,10949,"£2,737.35",2.55
CLASSROOM,70W,18,77,1.39,7,220,2134,£533.61,0.50
CLASSROOM,2X55W,457,121,55.30,7,220,85157,"£21,289.35",19.84
CLASSROOM,58W,25,64,1.60,7,220,2464,£616.00,0.57
CLASSROOM,2X70W,9,154,1.39,7,220,2134,£533.61,0.50
CLASSROOM,36W,4,40,0.16,7,220,246,£61.60,0.06
COMMUNAL,2X58W,9,128,1.15,5,220,1267,£316.80,0.30
COMMUNAL,32W,32,36,1.15,5,220,1267,£316.80,0.30
COMMUNAL,58W,1,64,0.06,5,220,70,£17.60,0.02
COMMUNAL,2X32W,16,72,1.15,5,220,1267,£316.80,0.30
COMMUNAL,70W,8,77,0.62,5,220,678,£169.40,0.16
COMMUNAL,2X70W,6,154,0.92,5,220,1016,£254.10,0.24
COMMUNAL,28W,25,31,0.78,5,220,853,£213.13,0.20
KITCHEN,4X18W,12,79,0.95,8,220,1668,£417.12,0.39
KITCHEN,2X58W,3,128,0.38,8,220,676,£168.96,0.16
KITCHEN,58W,5,64,0.32,8,220,563,£140.80,0.13
KITCHEN,4X36W,6,158,0.95,8,220,1668,£417.12,0.39
KITCHEN,2X70W,3,154,0.46,8,220,813,£203.28,0.19
KITCHEN,70W,3,77,0.23,8,220,407,£101.64,0.09
KITCHEN,100W,2,110,0.22,8,220,387,£96.80,0.09
KITCHEN,2X36W,1,79,0.08,8,220,139,£34.76,0.03
KITCHEN,28W,2,31,0.06,8,220,109,£27.28,0.03
OFFICE,58W,4,64,0.26,7,220,394,£98.56,0.09
OFFICE,2X58W,37,128,4.74,7,220,7293,"£1,823.36",1.70
OFFICE,2X55W,12,121,1.45,7,220,2236,£559.02,0.52
OFFICE,4X18W,19,79,1.50,7,220,2312,£577.89,0.54
OFFICE,70W,2,77,0.15,7,220,237,£59.29,0.06
OFFICE,36W,8,40,0.32,7,220,493,£123.20,0.11
PLANT,2X58W,7,128,0.90,2,220,394,£98.56,0.09
PLANT,28W,2,31,0.06,2,220,27,£6.82,0.01
SPORTS HALL,4X80W,27,352,9.50,5,220,10454,"£2,613.60",2.44
SPORTS HALL,2X70W,18,154,2.77,5,220,3049,£762.30,0.71
STORE,28W,13,31,0.40,3,220,266,£66.50,0.06
STORE,58W,13,64,0.83,3,220,549,£137.28,0.13
STORE,70W,6,77,0.46,3,220,305,£76.23,0.07
STORE,2X18W,1,40,0.04,3,220,26,£6.60,0.01
STORE,16W,1,18,0.02,3,220,12,£2.97,0.00
STORE,2X58W,2,128,0.26,3,220,169,£42.24,0.04
STORE,36W,1,40,0.04,3,220,26,£6.60,0.01
STORE,2X36W,1,79,0.08,3,220,52,£13.04,0.01
WC,4X18W,10,79,0.79,8,220,1390,£347.60,0.32
WC,28W,29,31,0.90,8,220,1582,£395.56,0.37
WC,2X58W,5,128,0.64,8,220,1126,£281.60,0.26
WC,16W,7,18,0.13,8,220,222,£55.44,0.05
WC,2X18W,32,40,1.28,8,220,2253,£563.20,0.52
WC,58W,1,64,0.06,8,220,113,£28.16,0.03
PROPOSED FITTINGS
Area,Lamp replacement,Quantity,Wattage,kW/Hour,Hours per Day,Days,Total kWh Per Annum,Proposed Running Cost,CO2 Tns
CIRCULATION,70W PENDANT,7,70,0.49,4,220,431,£107.80,0.10
CIRCULATION,16W PANEL,67,16,1.07,4,220,943,£235.84,0.22
CIRCULATION,10W BULKHEAD,46,10,0.46,4,220,405,£101.20,0.09
CIRCULATION,31W BATTEN,9,31,0.28,4,220,246,£61.38,0.06
CIRCULATION,18W DOWNLIGHT,80,18,1.44,4,220,1267,£316.80,0.30
CIRCULATION,21W BATTEN,12,21,0.25,4,220,222,£55.44,0.05
CIRCULATION,37W BATTEN,2,37,0.07,4,220,65,£16.28,0.02
CIRCULATION,16W BULKHEAD,13,16,0.21,4,220,183,£45.76,0.04
BEDROOM,31W BATTEN,20,31,0.62,5,220,682,£170.50,0.16
BEDROOM,10W BULKHEAD,41,10,0.41,5,220,451,£112.75,0.11
BEDROOM,8W BULKHEAD,31,8,0.25,5,220,273,£68.20,0.06
BEDROOM,21W BATTEN,3,21,0.06,5,220,69,£17.33,0.02
BEDROOM,31W BATTEN,1,31,0.03,5,220,34,£8.53,0.01
CHANGING ROOM,16W PANEL,35,16,0.56,3,220,370,£92.40,0.09
CHANGING ROOM,27W BATTEN,21,27,0.57,3,220,374,£93.56,0.09
CHANGING ROOM,10W BULKHEAD,13,10,0.13,3,220,86,£21.45,0.02
CHANGING ROOM,31W BATTEN,11,31,0.34,3,220,225,£56.27,0.05
CLASSROOM,16W PANEL,547,16,8.75,7,220,13478,"£3,369.52",3.14
CLASSROOM,31W BATTEN,115,31,3.57,7,220,5490,"£1,372.53",1.28
COMMUNAL,31W BATTEN,10,31,0.31,5,220,341,£85.25,0.08
COMMUNAL,18W DOWNLIGHT,48,18,0.86,5,220,950,£237.60,0.22
COMMUNAL,10W BULKHEAD,25,10,0.25,5,220,275,£68.75,0.06
COMMUNAL,37W BATTEN,14,37,0.52,5,220,570,£142.45,0.13
KITCHEN,31W BATTEN,8,31,0.25,8,220,436,£109.12,0.10
KITCHEN,1200X600 PANEL,6,54,0.32,8,220,570,£142.56,0.13
KITCHEN,16W PANEL,12,16,0.19,8,220,338,£84.48,0.08
KITCHEN,37W BATTEN,8,37,0.30,8,220,521,£130.24,0.12
KITCHEN,10W BULKHEAD,2,10,0.02,8,220,35,£8.80,0.01
KITCHEN,21W BATTEN,1,21,0.02,8,220,37,£9.24,0.01
OFFICE,31W BATTEN,51,31,1.58,7,220,2435,£608.69,0.57
OFFICE,16W PANEL,31,16,0.50,7,220,764,£190.96,0.18
PLANT,10W BULKHEAD,2,10,0.02,2,220,9,£2.20,0.00
PLANT,31W BATTEN,7,31,0.22,2,220,95,£23.87,0.02
SPORTS HALL,150W LOW BAY,27,27,0.73,5,220,802,£200.48,0.19
SPORTS HALL,57W LINEAR,18,57,1.03,5,220,1129,£282.15,0.26
STORE,10W BULKHEAD,14,10,0.14,1,220,31,£7.70,0.01
STORE,31W BATTEN,15,31,0.47,1,220,102,£25.58,0.02
STORE,37W BATTEN,6,37,0.22,1,220,49,£12.21,0.01
STORE,21W BATTEN,2,21,0.04,1,220,9,£2.31,0.00
STORE,18W DOWNLIGHT,1,18,0.02,1,220,4,£0.99,0.00
WC,16W PANEL,10,16,0.16,4,220,141,£35.20,0.03
WC,10W BULKHEAD,29,10,0.29,4,220,255,£63.80,0.06
WC,31W BATTEN,6,31,0.19,4,220,164,£40.92,0.04
WC,8W BULKHEAD,7,8,0.06,4,220,49,£12.32,0.01
WC,18W DOWNLIGHT,32,18,0.58,4,220,507,£126.72,0.12
"""

@st.cache_data
def load_and_process_data():
    lines = RAW_DATA.strip().split('\n')
    split_index = lines.index("PROPOSED FITTINGS")
    existing_data = "\n".join(lines[1:split_index])
    proposed_data = "\n".join(lines[split_index+1:])
    df_existing = pd.read_csv(StringIO(existing_data))
    df_proposed = pd.read_csv(StringIO(proposed_data))
    
    for df in [df_existing, df_proposed]:
        df.columns = [col.strip().replace('"', '') for col in df.columns]
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].str.strip().str.replace('"', '')
        cost_col = [col for col in df.columns if 'Running Cost' in col][0]
        df[cost_col] = df[cost_col].replace({r'[£,]': ''}, regex=True).astype(float)
        numeric_cols = ['Quantity', 'Wattage', 'Hours per Day', 'Days']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
    return df_existing, df_proposed

df_existing_base, df_proposed_base = load_and_process_data()

PROJECT_NAME = "Clayesmore School"
COST_PER_KWH = 0.25
KG_CO2_PER_KWH = 0.233
PROJECT_INSTALL_COST = 155915.00
ANNUAL_MAINTENANCE_OLD = 0 
ANNUAL_MAINTENANCE_LED = 0

DEFAULT_HOURS_MAP = df_proposed_base.groupby('Area')['Hours per Day'].first().to_dict()

DEFAULT_PARAMS = {
    "hours_per_day_map": DEFAULT_HOURS_MAP.copy(),
    "days_per_year": 220.0,
    "interest_rate": 5.0,
    "lease_term": 5,
    "deposit": 0,
}

if 'params' not in st.session_state:
    st.session_state.params = DEFAULT_PARAMS.copy()

st.sidebar.title("🎛️ Scenario Planner")
st.sidebar.markdown("Use the controls below to model different scenarios.")

# --- General Assumptions using Number Input for better control ---
st.session_state.params['days_per_year'] = st.sidebar.number_input(
    "🗓️ Days of Use per Year (All Areas)",
    min_value=1.0, max_value=365.0,
    value=float(st.session_state.params['days_per_year']),
    step=0.5,
    format="%.1f"
)

with st.sidebar.expander("💡 Detailed Operational Assumptions", expanded=True):
    st.markdown("Adjust the average hours of use per day for each area.")
    unique_areas = sorted(df_proposed_base['Area'].unique())
    for area in unique_areas:
        default_hour = float(DEFAULT_HOURS_MAP.get(area, 8))
        current_hour = float(st.session_state.params['hours_per_day_map'].get(area, default_hour))
        st.session_state.params['hours_per_day_map'][area] = st.number_input(
            f"{area}",
            min_value=1.0, max_value=24.0,
            value=current_hour,
            step=0.5,
            format="%.1f"
        )

st.sidebar.divider()
st.sidebar.markdown("### Funding Assumptions")
st.session_state.params['lease_term'] = st.sidebar.number_input("Lease Term (Years)", min_value=1, max_value=20, value=st.session_state.params['lease_term'], step=1)
st.session_state.params['interest_rate'] = st.sidebar.number_input("Interest Rate (%)", min_value=0.0, max_value=25.0, value=st.session_state.params['interest_rate'], step=0.1, format="%.1f")
st.session_state.params['deposit'] = st.sidebar.number_input(f"Upfront Deposit (£)", min_value=0, max_value=int(PROJECT_INSTALL_COST), value=st.session_state.params['deposit'], step=1000)

if st.sidebar.button("Reset to Defaults", use_container_width=True):
    st.session_state.params = DEFAULT_PARAMS.copy()
    st.experimental_rerun()

def calculate_metrics(df, annual_maintenance, hours_map, days):
    df_calc = df.copy()
    df_calc['Hours per Day'] = df_calc['Area'].map(hours_map).fillna(8.0)
    df_calc['Days'] = days
    df_calc['kWh'] = (df_calc['Quantity'] * df_calc['Wattage'] * df_calc['Hours per Day'] * df_calc['Days']) / 1000
    df_calc['Cost'] = df_calc['kWh'] * COST_PER_KWH
    total_cost = df_calc['Cost'].sum() + annual_maintenance
    total_kwh = df_calc['kWh'].sum()
    total_co2 = (total_kwh * KG_CO2_PER_KWH) / 1000
    return total_cost, total_kwh, total_co2, df_calc

p = st.session_state.params
current_cost, current_kwh, current_co2, df_existing_calc = calculate_metrics(df_existing_base, ANNUAL_MAINTENANCE_OLD, p['hours_per_day_map'], p['days_per_year'])
led_cost, led_kwh, led_co2, df_proposed_calc = calculate_metrics(df_proposed_base, ANNUAL_MAINTENANCE_LED, p['hours_per_day_map'], p['days_per_year'])

annual_savings = current_cost - led_cost
co2_savings = current_co2 - led_co2
payback_period = PROJECT_INSTALL_COST / annual_savings if annual_savings > 0 else 0

loan_amount = PROJECT_INSTALL_COST - p['deposit']
if p['interest_rate'] == 0:
    monthly_payment = loan_amount / (p['lease_term'] * 12) if p['lease_term'] > 0 else 0
else:
    monthly_rate = (p['interest_rate'] / 100) / 12
    n_periods = p['lease_term'] * 12
    monthly_payment = npf.pmt(monthly_rate, n_periods, -loan_amount) if n_periods > 0 else 0

annual_funding_cost = monthly_payment * 12
net_cash_flow = annual_savings - annual_funding_cost

st.title(f"💡 {PROJECT_NAME} Energy & Cost Savings Proposal")
st.markdown("An interactive proposal for a full-site LED lighting upgrade. All values update live based on your selections in the sidebar.")

st.header("Executive Summary: The Opportunity")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Projected Annual Savings", f"£{annual_savings:,.0f}", f"{((annual_savings/current_cost)*100):.0f}% Reduction" if current_cost > 0 else "N/A")
kpi2.metric("Positive Annual Cashflow", f"£{net_cash_flow:,.0f}", "After funding costs")
kpi3.metric("Carbon Reduction (CO₂e)", f"{co2_savings:.1f} Tonnes/Year", f"{((co2_savings/current_co2)*100):.0f}% Reduction" if current_co2 > 0 else "N/A")
kpi4.metric("Project Payback Period", f"{payback_period:.1f} Years" if payback_period > 0 else "N/A")

st.divider()
st.header("Analysis & Financial Breakdown")
col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader("⚡ Annual Consumption & Costs")
    df_compare = pd.DataFrame({
        "Metric": ["Running Costs (£)", "Energy Use (kWh)", "CO₂ Emissions (Tonnes)"],
        "Current System": [current_cost, current_kwh, current_co2],
        "Proposed LED System": [led_cost, led_kwh, led_co2]
    })
    # --- FIX: Added width parameter to make bars thicker ---
    fig_compare = go.Figure(data=[
        go.Bar(name='Current System', x=df_compare['Metric'], y=df_compare['Current System'], marker_color='#A9A9A9', width=0.4),
        go.Bar(name='Proposed LED System', x=df_compare['Metric'], y=df_compare['Proposed LED System'], marker_color='#00B050', width=0.4)
    ])
    fig_compare.update_layout(barmode='group', title_text="Current vs. Proposed System: Annual Impact", yaxis_title="Value", legend_title="System", margin=dict(t=40))
    st.plotly_chart(fig_compare, use_container_width=True)

with col2:
    st.subheader("💰 Annual Cash Flow Breakdown")
    fig_waterfall = go.Figure(go.Waterfall(
        orientation = "v", measure = ["relative", "relative", "total"],
        x = ["Annual Energy Savings", "Annual Funding Cost", "Net Positive Cash Flow"],
        text = [f"£{v:,.0f}" for v in [annual_savings, -annual_funding_cost, net_cash_flow]],
        y = [annual_savings, -annual_funding_cost, net_cash_flow],
        connector = {"line":{"color":"rgb(63, 63, 63)"}},
        increasing = {"marker":{"color":"#00B050"}},
        decreasing = {"marker":{"color":"#FF5733"}},
        totals = {"marker":{"color":"#4682B4"}}
    ))
    fig_waterfall.update_layout(title="From Savings to Positive Cash Flow", yaxis_title="Amount (£)", margin=dict(t=40))
    st.plotly_chart(fig_waterfall, use_container_width=True)

st.header("Where Do The Savings Come From?")
area_savings = (df_existing_calc.groupby('Area')['Cost'].sum() - df_proposed_calc.groupby('Area')['Cost'].sum()).reset_index()
area_savings.columns = ['Area', 'Savings (£)']

# --- ROBUST FIX: Filter for POSITIVE savings before plotting ---
positive_area_savings = area_savings[area_savings['Savings (£)'] > 0].sort_values(by='Savings (£)', ascending=False)

if not positive_area_savings.empty:
    fig_treemap = px.treemap(positive_area_savings, path=[px.Constant("All Areas"), 'Area'], values='Savings (£)',
                             color='Savings (£)', color_continuous_scale='Greens',
                             title="Annual Savings Contribution by School Area")
    fig_treemap.update_traces(textinfo="label+value+percent-root", texttemplate="%{label}<br>£%{value:,.0f}")
    st.plotly_chart(fig_treemap, use_container_width=True)
else:
    st.info("Based on the current settings, there are no net savings in any area to display.")