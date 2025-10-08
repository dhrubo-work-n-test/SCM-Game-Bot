import streamlit as st
import os
from scm_logic import SCMGame

# ------------------ PAGE SETUP ------------------ #
st.set_page_config(page_title="SCM Game Bot", layout="wide")
st.title("🤖 SCM Game Bot – Supply Chain Simulation")
st.markdown("### Step into the role of a Supply Chain Consultant and make decisions across all SCM stages.")

# ------------------ DATA PATH & INITIALIZATION ------------------ #
# Automatically locate the data folder relative to this script
data_path = os.path.join(os.path.dirname(__file__), "data") + "/"

if "game" not in st.session_state:
    try:
        st.session_state.game = SCMGame(data_path=data_path)
        st.session_state.messages = []
    except FileNotFoundError as e:
        st.error(f"❌ Missing data files! Please make sure CSVs exist in: {data_path}")
        st.stop()  # Stop execution if files are missing

game = st.session_state.game

# ------------------ STAGE 1: PLANNING ------------------ #
st.header("1️⃣ Planning Stage")
forecast_adjustment = st.slider("Adjust forecast (± units)", -50, 50, 0)
if st.button("Run Planning Stage"):
    adjusted = game.planning_stage(forecast_adjustment)
    st.session_state.messages.append(f"📊 Adjusted forecast to {adjusted} units.")

# ------------------ STAGE 2: SOURCING ------------------ #
st.header("2️⃣ Sourcing Stage")
supplier_choice = st.selectbox("Choose supplier:", game.suppliers["name"].tolist())
if st.button("Run Sourcing Stage"):
    supplier = game.sourcing_stage(supplier_choice)
    st.session_state.messages.append(
        f"🏭 Selected supplier: {supplier_choice} (Cost: {supplier['cost_per_unit']}, Reliability: {supplier['reliability']})"
    )

# ------------------ STAGE 3: MANUFACTURING ------------------ #
st.header("3️⃣ Manufacturing Stage")
plant_choice = st.selectbox("Select plant ID:", game.manufacturing["plant_id"].tolist())
units_to_produce = st.number_input("Units to produce:", min_value=50, max_value=1000, step=50)
if st.button("Run Manufacturing Stage"):
    output, cost = game.manufacturing_stage(plant_choice, units_to_produce)
    st.session_state.messages.append(f"⚙️ Produced {output} units at cost {cost}")

# ------------------ STAGE 4: DELIVERY ------------------ #
st.header("4️⃣ Delivery Stage")
delivery_mode = st.selectbox("Choose delivery mode:", ["Air", "Sea", "Road"])
if st.button("Run Delivery Stage"):
    cost, delay = game.delivery_stage(delivery_mode)
    st.session_state.messages.append(f"🚚 Delivery via {delivery_mode}: Delay {delay} days, Cost {cost}/unit")

# ------------------ STAGE 5: RETURNS ------------------ #
st.header("5️⃣ Returns Stage")
return_rate = st.slider("Return rate (0–20%)", 0.0, 0.2, 0.05)
if st.button("Run Returns Stage"):
    returned_units, loss = game.returns_stage(return_rate)
    st.session_state.messages.append(f"🔁 {returned_units} units returned, Loss: {loss}")

# ------------------ EVALUATE ------------------ #
if st.button("✅ Evaluate Week"):
    results = game.evaluate_week()
    st.session_state.messages.append(
        f"📈 Week Summary → Revenue: {results['revenue']} | Profit: {results['profit']} | Inventory left: {results['inventory_left']}"
    )

# ------------------ DISPLAY MESSAGES ------------------ #
st.markdown("---")
st.subheader("🧾 Game Log")
for msg in reversed(st.session_state.messages):
    st.info(msg)

st.markdown("---")
st.metric("💰 Total Profit", f"{game.total_profit}")
st.metric("😊 Customer Satisfaction", f"{game.customer_satisfaction}")
st.metric("📦 Inventory", f"{game.inventory}")
