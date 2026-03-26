import streamlit as st

st.set_page_config(page_title="TDS Calculator 2025", layout="wide")

st.title("TDS Calculator (Income Tax Act 2025)")

# --- Section Data (expand as needed) ---
TDS_SECTIONS_2025 = [
    {
        "section": "194J",
        "nature": "Other Professional Services",
        "rateIndividual": 10,
        "rateOther": 10,
        "threshold": 30000,
        "noPanRate": 20
    },
    {
        "section": "194I",
        "nature": "Rent",
        "rateIndividual": 10,
        "rateOther": 10,
        "threshold": 50000,
        "noPanRate": 20
    }
]

# --- Layout ---
col1, col2 = st.columns([1, 1])

# ---------------- LEFT PANEL ----------------
with col1:
    st.subheader("Input Details")

    # Nature of Payment
    selected_nature = st.selectbox(
        "Nature of Payment",
        [s["nature"] for s in TDS_SECTIONS_2025]
    )

    selected_section = next(
        s for s in TDS_SECTIONS_2025 if s["nature"] == selected_nature
    )

    # Payee Type
    payee_type = st.radio(
        "Payee Type",
        ["Individual/HUF", "Others"],
        horizontal=True
    )
    is_individual = payee_type == "Individual/HUF"

    # PAN Status
    pan_status = st.radio(
        "PAN Status",
        ["Available", "No PAN"],
        horizontal=True
    )
    has_pan = pan_status == "Available"

    # Amount Input
    label = "Rent per month (₹)" if "rent" in selected_nature.lower() else "Payment Amount (₹)"
    amount = st.number_input(label, min_value=0.0, value=0.0)

# ---------------- CALCULATION ----------------
is_rent = "rent" in selected_nature.lower()

if is_rent:
    threshold = 50000
    base_rate = 10

    rate = base_rate
    if not has_pan:
        rate = max(base_rate, 20)

    is_applicable = amount > threshold
    tds_amount = (amount * rate / 100) if is_applicable else 0

else:
    base_rate = selected_section["rateIndividual"] if is_individual else selected_section["rateOther"]

    rate = base_rate
    if not has_pan:
        rate = max(base_rate, selected_section.get("noPanRate", 20))

    is_applicable = amount > selected_section["threshold"]
    tds_amount = (amount * rate / 100) if is_applicable else 0

# ---------------- RIGHT PANEL ----------------
with col2:
    st.subheader("Calculation Result")

    if amount > 0:
        st.markdown("### Applicable Rate")
        st.write(f"**{rate}%**")

        if not has_pan and rate > base_rate:
            st.error("Higher rate applied due to No PAN (Sec 206AA)")

        st.markdown("### TDS Amount")
        st.success(f"₹ {tds_amount:,.2f}")

        if not is_applicable:
            if is_rent:
                st.warning("Monthly rent is below ₹50,000. No TDS applicable.")
            else:
                st.warning("Threshold not exceeded. No TDS applicable.")
    else:
        st.info("Enter an amount to calculate TDS")