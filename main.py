import streamlit as st
import plotly.graph_objects as go


st.set_page_config(page_title="Buget", page_icon="💰", layout="wide")

st.title("Buget total")

if "costuri" not in st.session_state:
    st.session_state.costuri = [{"label": "", "cost": 0.0}]

st.markdown(
    """
    <style>
    div[data-testid="stNumberInput"] { width: max-content; }
    div[data-testid="stSelectbox"] { width: max-content; }
    </style>
    """,
    unsafe_allow_html=True,
)

buget_total = st.number_input("Introdu bugetul total", min_value=0.0, step=100.0)
moneda = st.selectbox("Monedă", ["RON", "EUR", "USD", "GBP"], index=0)

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

total_costuri = sum(
    st.session_state[f"cost_value_{index}"]
    for index in range(len(st.session_state.costuri))
)
buget_ramas = buget_total - total_costuri

total_col, ramas_col = st.columns(2)
total_col.metric("Buget total", f"{buget_total:,.2f} {moneda}")
ramas_col.metric("Buget rămas", f"{buget_ramas:,.2f} {moneda}")

if st.button("+", help="Adaugă un cost"):
    st.session_state.costuri.append({"label": "", "cost": 0.0})
    st.rerun()

costuri_grafic = [
    {"Element": cost["label"].strip() or f"Cost {index + 1}", "Valoare": cost["cost"]}
    for index, cost in enumerate(st.session_state.costuri)
    if cost["cost"] > 0
]

if costuri_grafic:
    st.subheader("Distribuția costurilor")
    culori = ["#6C5CE7", "#00B894", "#0984E3", "#E17055", "#FDCB6E", "#E84393", "#00CEC9"]
    grafic = go.Figure(
        data=[
            go.Pie(
                labels=[cost["Element"] for cost in costuri_grafic],
                values=[cost["Valoare"] for cost in costuri_grafic],
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
        legend_title_text="Costuri",
        margin=dict(t=20, b=20, l=20, r=20),
        height=420,
    )
    st.plotly_chart(grafic, use_container_width=True)
