import streamlit as st
import plotly.graph_objects as go

def calculate_compound_interest(principal, rate, time, compounds_per_year):
    if principal == 0 or rate == 0 or time == 0 or compounds_per_year == 0:
        return "Please enter valid values for all fields."
    r = rate / 100
    amount = principal * (1 + r / compounds_per_year) ** (compounds_per_year * time)
    return round(amount - principal, 2)

def calculate_simple_interest(principal, rate, time):
    return (principal * rate * time) / 100

def calculate_total_amount(principal, interest):
    return principal + interest

def tools_page():
    st.markdown("""
    <style>
    * { font-family: Verdana, sans-serif !important; }

    .calc-box {
        background-color: #efebef;
        color: black;
        border-radius: 15px;
        padding: 24px 20px 20px 20px;
        margin: 10px auto;
    }
    .calc-title {
        color: white;
        font-size: 1.3em;
        font-weight: bold;
        margin-bottom: 16px;
        text-align: left;
    }
    .result-box {
        background-color: #D6FF58;
        color: black;
        border-radius: 8px;
        padding: 10px 14px;
        margin-bottom: 16px;
        font-size: 1em;
        font-weight: bold;
        min-height: 44px;
    }
    .slider-label {
        font-size: 1.1em;
        margin-bottom: 2px;
    }
    /* Make number input labels dark inside calc boxes */
    .calc-box label {
        color: #4A4A4A !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h3 style='margin-bottom: -10px;'>Try out some of our handy tools...</h3>",
                unsafe_allow_html=True)

    # ── EMI Calculator ──────────────────────────────────────────────────────
    st.markdown("<h4>EMI Calculator</h4>", unsafe_allow_html=True)

    col_gap, col_chart, col_sliders = st.columns([0.2, 1.5, 2])

    with col_chart:
        total_amount_output = st.empty()
        total_amount_output.markdown(
            "<div class='result-container'>"
            "<span style='color:orange;font-weight:bold;font-size:1.4em;'>₹0</span>"
            "</div>",
            unsafe_allow_html=True,
        )
        chart_placeholder = st.empty()

    with col_sliders:
        st.markdown("<div class='slider-label'>Loan Amount (₹)</div>", unsafe_allow_html=True)
        principal = st.slider("", min_value=0, max_value=1000000, value=1000, step=1, key="loan_amt")

        st.markdown("<div class='slider-label'>Rate of Interest (% p.a.)</div>", unsafe_allow_html=True)
        rate = st.slider("", min_value=0.0, max_value=30.0, value=3.0, step=0.1, key="interest")

        st.markdown("<div class='slider-label'>Loan Tenure (Years)</div>", unsafe_allow_html=True)
        time = st.slider("", min_value=0, max_value=30, value=5, step=1, key="loan_emi_time")

        interest = calculate_simple_interest(principal, rate, time)
        total_amount = calculate_total_amount(principal, interest)

        total_amount_output.markdown(
            f"<div class='result-container'>"
            f"<span style='color:orange;font-weight:bold;font-size:1.4em;'>₹{total_amount:,.2f}</span>"
            f"</div>",
            unsafe_allow_html=True,
        )

        fig = go.Figure(data=[go.Pie(
            labels=["Principal", "Interest"],
            values=[principal, interest],
            hole=0.3,
        )])
        fig.update_layout(
            title_text="Loan Breakdown",
            title_x=0.4, title_y=0.9,
            title_xanchor="center", title_yanchor="top",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        chart_placeholder.plotly_chart(fig)

    # ── SI & CI Calculators ─────────────────────────────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown("<div class='calc-title'>S.I. Calculator</div>", unsafe_allow_html=True)

            si_result = st.empty()
            si_result.markdown("<div class='result-box'>₹ — &nbsp; Total Simple Interest</div>",
                               unsafe_allow_html=True)

            si_p    = st.number_input("Principal Amount (₹)",      min_value=0.0, key="si_p")
            si_rate = st.number_input("Rate of Interest (% p.a.)",  min_value=0.0, key="si_rate")
            si_time = st.number_input("Time Period (Years)",         min_value=0.0, key="si_time")

            if st.button("Calculate", key="si_button"):
                result = calculate_simple_interest(si_p, si_rate, si_time)
                si_result.markdown(
                    f"<div class='result-box'>₹{result:,.2f} &nbsp; Total Simple Interest</div>",
                    unsafe_allow_html=True,
                )

    with col2:
        with st.container(border=True):
            st.markdown("<div class='calc-title'>C.I. Calculator</div>", unsafe_allow_html=True)

            ci_result = st.empty()
            ci_result.markdown("<div class='result-box'>₹ — &nbsp; Total Compound Interest</div>",
                               unsafe_allow_html=True)

            ci_p    = st.number_input("Principal Amount (₹)",      min_value=0.0, key="ci_p")
            ci_rate = st.number_input("Rate of Interest (% p.a.)",  min_value=0.0, key="ci_rate")
            ci_time = st.number_input("Time Period (Years)",         min_value=0.0, key="ci_time")
            ci_cpy  = st.number_input("Compounds per Year",          min_value=1,   key="ci_year")

            if st.button("Calculate", key="ci_button"):
                result = calculate_compound_interest(ci_p, ci_rate, ci_time, ci_cpy)
                ci_result.markdown(
                    f"<div class='result-box'>₹{result:,.2f} &nbsp; Total Compound Interest</div>",
                    unsafe_allow_html=True,
                )