import streamlit as st
import pandas as pd
from sim_engine import (
    simulate_planning,
    simulate_sourcing,
    simulate_manufacturing,
    simulate_delivery,
    simulate_returns
)

# -------------------------
# Page Config
# -------------------------
st.set_page_config(page_title="SCM Game Bot", layout="wide")
st.title("📦 SCM Game Bot – Experiential Learning for Supply Chain Consultants")

# -------------------------
# Instructions
# -------------------------
st.markdown("""
Welcome to the **SCM Game Bot**!

### 🎯 Objective
You are a supply chain consultant. Make strategic decisions across 5 stages:

1. **Planning** – Forecast demand and set production targets  
2. **Sourcing** – Choose suppliers and manage procurement costs  
3. **Manufacturing** – Optimize production efficiency and cost  
4. **Delivery** – Manage logistics and delivery performance  
5. **Returns** – Handle after-sales service and returns

At the end, your performance metrics will be displayed.
""")

# -------------------------
# Initialize session state
# -------------------------
if "stage" not in st.session_state:
    st.session_state.stage = 1
if "results" not in st.session_state:
    st.session_state.results = {
        "profit": 0.0,
        "inventory_value": 0.0,
        "customer_satisfaction": 100.0
    }

# -------------------------
# Helper to safely update results
# -------------------------
def update_results(simulation_result):
    for k, v in simulation_result.items():
        if k not in st.session_state.results:
            st.session_state.results[k] = 0.0
        if isinstance(v, (int, float)):
            st.session_state.results[k] += v
        else:
            st.session_state.results[k] = v

def next_stage():
    st.session_state.stage += 1
    st.experimental_rerun()

# -------------------------
# Stage 1: Planning
# -------------------------
if st.session_state.stage == 1:
    st.header("Stage 1: Planning")
    st.write("Estimate demand and set production goals to balance cost and service.")
    demand_forecast = st.slider("📊 Forecast Demand (units)", 100, 1000, 500, 50)
    production_target = st.slider("🏭 Production Target (units)", 100, 1000, 600, 50)
    safety_stock = st.slider("📦 Safety Stock (units)", 0, 300, 100, 10)

    if st.button("Proceed to Sourcing"):
        result = simulate_planning(demand_forecast, production_target, safety_stock)
        update_results(result)
        next_stage()

# -------------------------
# Stage 2: Sourcing
# -------------------------
elif st.session_state.stage == 2:
    st.header("Stage 2: Sourcing")
    st.write("Select suppliers balancing cost and reliability.")
    supplier_cost = st.slider("💰 Supplier Cost per unit", 10, 50, 25, 1)
    supplier_reliability = st.slider("✅ Supplier Reliability (%)", 70, 100, 90, 1)

    if st.button("Proceed to Manufacturing"):
        result = simulate_sourcing(supplier_cost, supplier_reliability)
        update_results(result)
        next_stage()

# -------------------------
# Stage 3: Manufacturing
# -------------------------
elif st.session_state.stage == 3:
    st.header("Stage 3: Manufacturing")
    st.write("Decide production efficiency and manage unit cost.")
    production_efficiency = st.slider("⚙️ Production Efficiency (%)", 60, 100, 85, 1)
    production_cost = st.slider("🏷️ Production Cost per unit", 5, 30, 15, 1)

    if st.button("Proceed to Delivery"):
        result = simulate_manufacturing(production_efficiency, production_cost)
        update_results(result)
        next_stage()

# -------------------------
# Stage 4: Delivery
# -------------------------
elif st.session_state.stage == 4:
    st.header("Stage 4: Delivery / Logistics")
    st.write("Plan delivery routes and balance cost vs reliability.")
    delivery_cost = st.slider("🚚 Delivery Cost per unit", 1, 20, 10, 1)
    delay_risk = st.slider("⏱️ Delay Risk (%)", 0, 50, 20, 5)

    if st.button("Proceed to Returns"):
        result = simulate_delivery(delivery_cost, delay_risk)
        update_results(result)
        next_stage()

# -------------------------
# Stage 5: Returns
# -------------------------
elif st.session_state.stage == 5:
    st.header("Stage 5: Returns / After-Sales Service")
    st.write("Handle customer returns efficiently to improve satisfaction.")
    return_rate = st.slider("📦 Return Rate (%)", 0, 30, 10, 1)
    service_quality = st.slider("⭐ Service Quality (%)", 60, 100, 85, 1)

    if st.button("Show Final Results"):
        result = simulate_returns(return_rate, service_quality)
        update_results(result)
        next_stage()

# -------------------------
# Final Stage: Summary
# -------------------------
elif st.session_state.stage == 6:
    st.header("🏁 Final Performance Metrics")
    st.success("🎉 You’ve completed the SCM Simulation Game!")

    results = st.session_state.results
    df = pd.DataFrame(results.items(), columns=["Metric", "Value"])
    st.table(df)

    total_score = results["profit"] + results["customer_satisfaction"] - results["inventory_value"] * 0.1
    st.metric("Final Score", round(total_score, 2))

    if total_score > 500:
        st.success("🌟 Excellent performance! You optimized both profit and service.")
    elif total_score > 200:
        st.info("👍 Good job! You managed your supply chain effectively.")
    else:
        st.warning("⚠️ You faced some challenges. Try different strategies next time!")

    if st.button("Restart Game"):
        st.session_state.stage = 1
        st.session_state.results = {
            "profit": 0.0,
            "inventory_value": 0.0,
            "customer_satisfaction": 100.0
        }
        st.experimental_rerun()
