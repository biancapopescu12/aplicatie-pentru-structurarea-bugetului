import streamlit as st
import plotly.graph_objects as go


st.set_page_config(page_title="Buget", page_icon="💰", layout="wide")

st.title("Buget total")

if "costuri" not in st.session_state:
    st.session_state.costuri = [{"label": "", "cost": 0.0}]

st.markdown(
    """
    <style>
    :root {
        --mint-light: #84ee95;
        --mint: #00cc90;
        --cyan: #00cdff;
    }
    .stApp {
        background: linear-gradient(135deg, #f4fff6 0%, #efffff 100%);
    }
    [data-testid="stHeading"] h1,
    h1[data-testid="stHeading"] {
        color: #00AE5E !important;
    }
    h2, h3 {
        color: #008b68;
    }
    div[data-testid="stMetric"] {
        background: linear-gradient(120deg, var(--mint-light), #d9fff2);
        border: 1px solid var(--mint);
        border-radius: 16px;
        padding: 18px 22px;
    }
    div[data-testid="stMetric"] label,
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #006c62;
    }
    div[data-testid="stTextInput"] input,
    div[data-testid="stNumberInput"] input,
    div[data-testid="stSelectbox"] [data-baseweb="select"] > div {
        border-color: var(--mint);
        border-radius: 10px;
    }
    div[data-testid="stButton"] button {
        background: linear-gradient(110deg, var(--mint), var(--cyan));
        color: #003b3d;
        border: 0;
        border-radius: 12px;
        font-weight: 700;
    }
    div[data-testid="stButton"] button:hover {
        border: 0;
        color: #003b3d;
        filter: brightness(0.96);
    }
    div[data-testid="stNumberInput"] {
        width: max-content;
        min-width: 400px;
        max-width: 800px;
    }
    div[data-testid="stSelectbox"] {
        width: max-content;
        min-width: 400px;
        max-width: 800px;
    }
    div[data-testid="stHorizontalBlock"]:has(div[data-testid^="stTextInput"]) {
        max-width: 1000px;
    }
    div[data-testid="stPlotlyChart"] {
        margin-left: 0;
        margin-right: auto;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

buget_total = st.number_input("Introdu bugetul total", min_value=0.0, step=100.0)
moneda = st.selectbox("Monedă", ["RON", "EUR", "USD", "GBP"], index=0)

total_costuri = sum(
    st.session_state[f"cost_value_{index}"]
    for index in range(len(st.session_state.costuri))
    if f"cost_value_{index}" in st.session_state
)
buget_ramas = buget_total - total_costuri

total_col, ramas_col = st.columns(2)
total_col.metric("Buget total", f"{buget_total:,.2f} {moneda}")
ramas_col.metric("Buget rămas", f"{buget_ramas:,.2f} {moneda}")

st.subheader("Costuri")
for index, cost in enumerate(st.session_state.costuri):
    label_col, cost_col = st.columns([2, 1])
    with label_col:
        cost["label"] = st.text_input(
            "Etichetă", value=cost["label"], key=f"cost_label_{index}"
        )
    with cost_col:
        cost["cost"] = st.number_input(
            "Cost", min_value=0.0, step=10.0, value=cost["cost"],
            key=f"cost_value_{index}"
        )

add_col, _ = st.columns([2, 1])
with add_col:
    add_cost = st.button("+", help="Adaugă un cost")

if add_cost:
    st.session_state.costuri.append({"label": "", "cost": 0.0})
    st.rerun()

costuri_grafic = [
    {"Element": cost["label"].strip() or f"Cost {index + 1}", "Valoare": cost["cost"]}
    for index, cost in enumerate(st.session_state.costuri)
    if cost["cost"] > 0
]

if costuri_grafic:
    st.subheader("Distribuția costurilor")
    culori = ["#84ee95", "#00cc90", "#00cdff"]
    grafic = go.Figure(
        data=[
            go.Pie(
                labels=[cost["Element"] for cost in costuri_grafic],
                values=[cost["Valoare"] for cost in costuri_grafic],
                domain={"x": [0, 0.65]},
                hole=0.48,
                sort=False,
                textposition="inside",
                textinfo="label+percent",
                hovertemplate="%{label}<br>%{value:,.2f} " + moneda + "<extra></extra>",
                marker={"colors": culori, "line": {"color": "white", "width": 3}},
            )
        ]
    )
    grafic.update_layout(
        showlegend=True,
        legend={"x": 0.68, "xanchor": "left", "y": 0.5, "yanchor": "middle"},
        legend_title_text="Costuri",
        margin=dict(t=20, b=20, l=20, r=20),
        height=420,
    )
    st.plotly_chart(grafic, use_container_width=True)

    
