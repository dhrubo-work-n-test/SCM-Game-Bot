import streamlit as st
import pandas as pd
import os

# Import simulation functions
from sim_engine import (
    simulate_planning,
    simulate_sourcing,
    simulate_manufacturing,
    simulate_delivery,
    simulate_returns
)

st.set_page_config(page_title="SCM Game Bot", layout="wide")

# --- Instructions at start ---
st.title("📦 SCM Game Bot – Experiential Learning for Supply Chain Consultants")
st.markdown("""
Welcome to the **SCM Game Bot** — your interactive supply chain simulation experience!

### 🎯 Objective
You’ll play as a supply chain consultant. At each stage of the SCM process, 
you’ll make data-driven decisions and see how they impact **profit, inventory, and performance**.

Stages:
1. **Planning** – Forecast demand and set production targets  
2. **Sourcing** – Choose suppliers and manage procurement costs  
3. **Manufacturing** – Decide production batch sizes and costs  
4. **Delivery** – Plan logistics and delivery routes  
5. **Returns** – Handle returned goods and customer service  

At the end, your performance will be evaluated using metrics like **profit**, **inventory value**, and **service level**.
""")

# --- Initialize session state ---
if "stage" not in st.session_state:
    st.session_state.stage = 1
if "results" not in st.session_state:
    st.session_state.results = {
        "profit": 0,
        "inventory_value": 0,
        "customer_satisfaction": 100
    }

# --- Stage 1: Planning ---
if st.session_state.stage == 1:
    st.header("Stage 1: Planning")
    st.write("Forecast demand and set production targets based on expected sales and safety stock.")
    demand_forecast = st.slider("📊 Forecast Demand (units)", 100, 1000, 500, 50)
    production_target = st.slider("🏭 Production Target (units)", 100, 1000, 600, 50)
    safety_stock = st.slider("📦 Safety Stock (units)", 0, 300, 100, 10)

    if st.button("Proceed to Sourcing"):
        planning_result = simulate_planning(demand_forecast, production_target, safety_stock)
        for k, v in planning_result.items():
            st.session_state.results[k] = st.session_state.results.get(k, 0) + v
        st.session_state.stage = 2
        st.experimental_rerun()

# --- Stage 2: Sourcing ---
elif st.session_state.stage == 2:
    st.header("Stage 2: Sourcing")
    st.write("Select your supplier strategy balancing cost and reliability.")
    supplier_cost = st.slider("💰 Supplier Cost per unit", 10, 50, 25, 1)
    supplier_reliability = st.slider("✅ Supplier Reliability (%)", 70, 100, 90, 1)

    if st.button("Proceed to Manufacturing"):
        sourcing_result = simulate_sourcing(supplier_cost, supplier_reliability)
        for k, v in sourcing_result.items():
            st.session_state.results[k] = st.session_state.results.get(k, 0) + v
        st.session_state.stage = 3
        st.experimental_rerun()

# --- Stage 3: Manufacturing ---
elif st.session_state.stage == 3:
    st.header("Stage 3: Manufacturing")
    st.write("Decide how efficiently to produce while managing cost and time.")
    production_efficiency = st.slider("⚙️ Production Efficiency (%)", 60, 100, 85, 1)
    production_cost = st.slider("🏷️ Production Cost per unit", 5, 30, 15, 1)

    if st.button("Proceed to Delivery"):
        manufacturing_result = simulate_manufacturing(production_efficiency, production_cost)
        for k, v in manufacturing_result.items():
            st.session_state.results[k] = st.session_state.results.get(k, 0) + v
        st.session_state.stage = 4
        st.experimental_rerun()

# --- Stage 4: Delivery ---
elif st.session_state.stage == 4:
    st.header("Stage 4: Delivery/Logistics")
    st.write("Plan how to deliver goods efficiently while minimizing delays and costs.")
    delivery_cost = st.slider("🚚 Delivery Cost per unit", 1, 20, 10, 1)
    delay_risk = st.slider("⏱️ Delay Risk (%)", 0, 50, 20, 5)

    if st.button("Proceed to Returns"):
        delivery_result = simulate_delivery(delivery_cost, delay_risk)
        for k, v in delivery_result.items():
            st.session_state.results[k] = st.session_state.results.get(k, 0) + v
        st.session_state.stage = 5
        st.experimental_rerun()

# --- Stage 5: Returns ---
elif st.session_state.stage == 5:
    st.header("Stage 5: Returns / After-Sales Service")
    st.write("Handle customer returns and service quality.")
    return_rate = st.slider("📦 Return Rate (%)", 0, 30, 10, 1)
    service_quality = st.slider("⭐ Service Quality (%)", 60, 100, 85, 1)

    if st.button("Show Final Results"):
        returns_result = simulate_returns(return_rate, service_quality)
        for k, v in returns_result.items():
            st.session_state.results[k] = st.session_state.results.get(k, 0) + v
        st.session_state.stage = 6
        st.experimental_rerun()

# --- Stage 6: Final Results ---
elif st.session_state.stage == 6:
    st.header("🏁 Final Performance Metrics")
    st.success("Congratulations! You've completed the SCM Simulation Game.")
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
            "profit": 0,
            "inventory_value": 0,
            "customer_satisfaction": 100
        }
        st.experimental_rerun()
