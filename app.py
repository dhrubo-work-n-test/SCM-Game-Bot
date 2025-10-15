import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), 'logic'))

import streamlit as st
import pandas as pd
import numpy as np
from sim_engine import (
    simulate_planning,
    simulate_sourcing,
    simulate_manufacturing,
    simulate_delivery,
    simulate_returns
)

# ------------------------------
# APP CONFIGURATION
# ------------------------------
st.set_page_config(page_title="SCM Game Bot", layout="wide")

st.title("🧩 SCM Game Bot – Experiential Learning for Supply Chain Consultants")

st.markdown("""
### 🎮 Welcome to the Supply Chain Simulation Game!

You are stepping into the role of a **Supply Chain Consultant** for a manufacturing company.
Your goal is to **maximize total profit** while maintaining **inventory balance** and **customer satisfaction**.

#### 🧭 How to Play
1. The game progresses through 5 key stages of Supply Chain Management:
   - **Planning**
   - **Sourcing**
   - **Manufacturing**
   - **Delivery / Logistics**
   - **Returns / After-Sales**

2. In each stage, you’ll make **numeric decisions** using sliders (e.g., how much to produce, source, or deliver).

3. The bot will simulate the impact and update your performance metrics:
   - 💰 Profit
   - 📦 Inventory Level
   - 🚚 Customer Service (based on stockouts and delays)

4. At the end, you’ll see your **total performance summary** and can download your report.
---
""")

# ------------------------------
# SESSION STATE INITIALIZATION
# ------------------------------
if 'stage' not in st.session_state:
    st.session_state.stage = 1
if 'results' not in st.session_state:
    st.session_state.results = []

# ------------------------------
# GLOBAL METRICS
# ------------------------------
if 'profit' not in st.session_state:
    st.session_state.profit = 0
if 'inventory' not in st.session_state:
    st.session_state.inventory = 1000  # Starting inventory
if 'cost' not in st.session_state:
    st.session_state.cost = 0
if 'revenue' not in st.session_state:
    st.session_state.revenue = 0
if 'lost_sales' not in st.session_state:
    st.session_state.lost_sales = 0


# ------------------------------
# STAGE 1 – PLANNING
# ------------------------------
if st.session_state.stage == 1:
    st.header("📅 Stage 1: Planning")
    st.info("Objective: Forecast demand and set production targets based on expected sales and inventory goals.")

    demand_forecast = st.slider("Expected Demand (units)", 500, 2000, 1200, 50)
    production_target = st.slider("Production Plan (units)", 500, 2000, 1000, 50)
    safety_stock = st.slider("Safety Stock Level (units)", 0, 500, 100, 10)

    if st.button("Simulate Planning Stage"):
        result = simulate_planning(demand_forecast, production_target, safety_stock)
        st.session_state.results.append(result)
        for k, v in result.items():
            if k in st.session_state:
                st.session_state[k] += v
        st.session_state.stage = 2
        st.experimental_rerun()

# ------------------------------
# STAGE 2 – SOURCING
# ------------------------------
elif st.session_state.stage == 2:
    st.header("🏭 Stage 2: Sourcing")
    st.info("Objective: Select suppliers and manage procurement costs, lead times, and reliability.")

    supplier_quality = st.slider("Supplier Quality Score", 50, 100, 80, 5)
    supplier_cost = st.slider("Average Procurement Cost per Unit ($)", 5, 20, 10, 1)
    order_volume = st.slider("Order Volume (units)", 500, 2000, 1000, 50)

    if st.button("Simulate Sourcing Stage"):
        result = simulate_sourcing(supplier_quality, supplier_cost, order_volume)
        st.session_state.results.append(result)
        for k, v in result.items():
            if k in st.session_state:
                st.session_state[k] += v
        st.session_state.stage = 3
        st.experimental_rerun()

# ------------------------------
# STAGE 3 – MANUFACTURING
# ------------------------------
elif st.session_state.stage == 3:
    st.header("⚙️ Stage 3: Manufacturing")
    st.info("Objective: Optimize production efficiency and manage labor and machinery utilization.")

    production_efficiency = st.slider("Production Efficiency (%)", 60, 100, 85, 5)
    labor_hours = st.slider("Labor Hours Allocated", 100, 1000, 500, 50)
    machine_utilization = st.slider("Machine Utilization (%)", 50, 100, 80, 5)

    if st.button("Simulate Manufacturing Stage"):
        result = simulate_manufacturing(production_efficiency, labor_hours, machine_utilization)
        st.session_state.results.append(result)
        for k, v in result.items():
            if k in st.session_state:
                st.session_state[k] += v
        st.session_state.stage = 4
        st.experimental_rerun()

# ------------------------------
# STAGE 4 – DELIVERY / LOGISTICS
# ------------------------------
elif st.session_state.stage == 4:
    st.header("🚚 Stage 4: Delivery / Logistics")
    st.info("Objective: Manage transportation, delivery costs, and customer satisfaction.")

    transport_mode = st.selectbox("Transport Mode", ["Truck", "Rail", "Air"])
    delivery_speed = st.slider("Delivery Speed (Days)", 1, 10, 5)
    logistics_cost = st.slider("Logistics Cost per Shipment ($)", 1000, 10000, 5000, 500)

    if st.button("Simulate Delivery Stage"):
        result = simulate_delivery(transport_mode, delivery_speed, logistics_cost)
        st.session_state.results.append(result)
        for k, v in result.items():
            if k in st.session_state:
                st.session_state[k] += v
        st.session_state.stage = 5
        st.experimental_rerun()

# ------------------------------
# STAGE 5 – RETURNS / AFTER-SALES
# ------------------------------
elif st.session_state.stage == 5:
    st.header("🔁 Stage 5: Returns / After-Sales Service")
    st.info("Objective: Handle customer returns efficiently and manage cost impact.")

    return_rate = st.slider("Return Rate (%)", 0, 20, 5, 1)
    refurbish_cost = st.slider("Refurbish Cost per Unit ($)", 10, 100, 30, 5)
    customer_service_score = st.slider("Customer Service Investment ($)", 1000, 10000, 5000, 500)

    if st.button("Simulate Returns Stage"):
        result = simulate_returns(return_rate, refurbish_cost, customer_service_score)
        st.session_state.results.append(result)
        for k, v in result.items():
            if k in st.session_state:
                st.session_state[k] += v
        st.session_state.stage = 6
        st.experimental_rerun()

# ------------------------------
# FINAL RESULTS DASHBOARD
# ------------------------------
elif st.session_state.stage == 6:
    st.header("🏁 Game Summary – Your Performance Metrics")

    st.success("🎉 Congratulations! You’ve completed all stages of the SCM Game Bot simulation.")

    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Total Profit", f"${st.session_state.profit:,.2f}")
    col2.metric("📦 Final Inventory", f"{st.session_state.inventory:.0f} units")
    col3.metric("🚫 Lost Sales", f"{st.session_state.lost_sales:.0f} units")

    col4, col5 = st.columns(2)
    col4.metric("📈 Total Revenue", f"${st.session_state.revenue:,.2f}")
    col5.metric("💸 Total Cost", f"${st.session_state.cost:,.2f}")

    df = pd.DataFrame(st.session_state.results)
    st.dataframe(df)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Results as CSV", data=csv, file_name="scm_game_results.csv", mime='text/csv')

    if st.button("🔄 Restart Game"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()
