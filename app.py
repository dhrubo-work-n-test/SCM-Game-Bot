
import streamlit as st
import pandas as pd, json, os
from logic.sim_engine import simulate_planning, simulate_sourcing, simulate_manufacturing, simulate_delivery, simulate_returns

BASE = os.path.join(os.path.dirname(__file__), "")

# Load datasets
products = pd.read_csv(os.path.join(BASE, "products.csv"))
suppliers = pd.read_csv(os.path.join(BASE, "suppliers.csv"))
demand = pd.read_csv(os.path.join(BASE, "demand_timeseries.csv"))
scenarios = pd.read_csv(os.path.join(BASE, "scenarios.csv"))

# --- UI ---
st.set_page_config(page_title="SCM Game Bot", layout="wide")
st.title("🔮 SCM Game Bot — Supply Chain Numerical Simulator (Streamlit Prototype)")
st.markdown("### How to play\n1. Read the stage instructions shown on the right.\n2. Use sliders and inputs to make numeric decisions.\n3. Click **Simulate Stage** to apply decisions and see immediate metrics.\n4. Progress through the 5 stages. Your cumulative performance will appear in the dashboard.\n\n---")

# initialize session state
if "stage" not in st.session_state:
    st.session_state.stage = 1
if "metrics" not in st.session_state:
    st.session_state.metrics = {"profit":0.0, "inventory": 0, "revenue":0.0, "costs":0.0, "sold":0, "lost_sales":0}
if "history" not in st.session_state:
    st.session_state.history = []

col1, col2 = st.columns([2,1])

with col2:
    st.header("Stage Instructions")
    stage_instructions = {
        1: "Planning: Decide order quantities, safety stock and whether to expedite. You will see immediate effects on inventory, cost and sales.",
        2: "Sourcing: Choose supplier profile (cost vs reliability). This affects lead times and future costs.",
        3: "Manufacturing: Choose production volume, overtime and capacity increases.",
        4: "Delivery: Choose transport mode and decide on express shipping for critical shipments.",
        5: "Returns: Set return policy parameters and refurbishment decisions."
    }
    st.info(stage_instructions.get(st.session_state.stage, "Complete"))

with col1:
    # Product selector & scenario sample
    product = st.selectbox("Select product to play with", products["product_id"].tolist())
    prod_row = products[products["product_id"]==product].iloc[0].to_dict()
    st.write("Product summary:", prod_row)

    # Show a sample scenario (random)
    sample_scn = scenarios.sample(1).iloc[0].to_dict()
    st.write("Sample scenario (random):", sample_scn)

    # Stage-specific controls
    if st.session_state.stage == 1:
        st.subheader("Planning Decisions")
        order_qty = st.slider("Order quantity (units)", min_value=0, max_value=5000, value=prod_row["base_monthly_demand"], step=50)
        safety_stock = st.slider("Safety stock (units)", min_value=0, max_value=2000, value=100, step=10)
        expedite = st.checkbox("Expedite (expensive)", value=False)
        supplier_choice = st.selectbox("Choose supplier", suppliers["supplier_id"].tolist())
        supplier_row = suppliers[suppliers["supplier_id"]==supplier_choice].iloc[0].to_dict()
        if st.button("Simulate Stage"):
            decision = {
                "order_qty": order_qty,
                "safety_stock": safety_stock,
                "expediting": expedite,
                "supplier_cost_mult": supplier_row["cost_multiplier"],
                "lead_time_days": supplier_row["lead_time_days_mean"],
                "transport_cost": 0.0
            }
            # pick demand for current month for product (latest month)
            demand_row = demand[demand["product_id"]==product].sort_values("month").iloc[-1]
            result = simulate_planning(prod_row, decision, int(demand_row["demand"]), {"inventory": st.session_state.metrics["inventory"], "profit": st.session_state.metrics["profit"], "inventory_before": st.session_state.metrics["inventory"]})
            # update
            for k in ["inventory","profit","revenue","costs","sold","lost_sales"]:
                st.session_state.metrics[k] = result.get(k, st.session_state.metrics.get(k,0))
            st.session_state.history.append(("Planning", decision, result))
            st.success(f"Stage result — Profit Δ: {result['profit']:.2f}, Inventory: {result['inventory']}")
            st.session_state.stage += 1

    elif st.session_state.stage == 2:
        st.subheader("Sourcing Decisions")
        supplier_choice = st.selectbox("Choose supplier", suppliers["supplier_id"].tolist())
        supplier_row = suppliers[suppliers["supplier_id"]==supplier_choice].iloc[0].to_dict()
        reliability = st.slider("Negotiate reliability (%)", min_value=60, max_value=99, value=int(supplier_row["reliability_pct"]))
        if st.button("Simulate Stage"):
            decision = {"supplier_cost_mult": supplier_row["cost_multiplier"], "supplier_reliability": reliability}
            result = simulate_sourcing(prod_row, decision, st.session_state.metrics)
            st.session_state.history.append(("Sourcing", decision, result))
            st.success("Sourcing simulated. Supplier parameters updated (affects future stages).")
            st.session_state.stage += 1

    elif st.session_state.stage == 3:
        st.subheader("Manufacturing Decisions")
        produce_qty = st.slider("Produce units (in-house)", min_value=0, max_value=5000, value=0, step=50)
        overtime = st.checkbox("Allow overtime (costly)", value=False)
        if st.button("Simulate Stage"):
            decision = {"produce_qty": produce_qty, "overtime": overtime}
            result = simulate_manufacturing(prod_row, decision, st.session_state.metrics)
            # update metrics
            st.session_state.metrics["inventory"] = result.get("inventory", st.session_state.metrics["inventory"])
            st.session_state.metrics["profit"] = result.get("profit", st.session_state.metrics["profit"])
            st.session_state.history.append(("Manufacturing", decision, result))
            st.success(f"Manufacturing simulated. Inventory now {st.session_state.metrics['inventory']} units.")
            st.session_state.stage += 1

    elif st.session_state.stage == 4:
        st.subheader("Delivery Decisions")
        transport_mode = st.selectbox("Transport mode", ["sea","road","air"])
        express_pct = st.slider("Express shipping allocation (%)", min_value=0, max_value=100, value=0)
        if st.button("Simulate Stage"):
            decision = {"transport_mode": transport_mode, "express_pct": express_pct}
            result = simulate_delivery(prod_row, decision, st.session_state.metrics)
            st.session_state.metrics["profit"] = result.get("profit", st.session_state.metrics["profit"])
            st.session_state.history.append(("Delivery", decision, result))
            st.success(f"Delivery simulated. Transport cost: {result['transport_cost']:.2f}")
            st.session_state.stage += 1

    elif st.session_state.stage == 5:
        st.subheader("Returns & After-sales Decisions")
        return_rate = st.slider("Expected return rate (%)", min_value=0.0, max_value=20.0, value=2.0, step=0.5)
        put_back_pct = st.slider("Refurbish and put back to inventory (%)", min_value=0.0, max_value=100.0, value=50.0, step=5.0)
        if st.button("Simulate Stage"):
            decision = {"return_rate": return_rate/100.0, "put_back_pct": put_back_pct/100.0}
            result = simulate_returns(prod_row, decision, st.session_state.metrics)
            st.session_state.metrics["profit"] = result.get("profit", st.session_state.metrics["profit"])
            st.session_state.metrics["inventory"] = result.get("inventory", st.session_state.metrics["inventory"])
            st.session_state.history.append(("Returns", decision, result))
            st.success("Returns stage simulated. Game complete!")
            st.session_state.stage = 6

    else:
        st.subheader("Game Complete — Final Performance")
        st.write("### Cumulative metrics")
        st.write(st.session_state.metrics)
        st.write("### Stage history (last 10)")
        for h in st.session_state.history[-10:]:
            st.write(h)

        # Download results
        if st.button("Download game results (CSV)"):
            df_hist = pd.DataFrame([{"stage":h[0], **h[1], **({"result":h[2]})} for h in st.session_state.history])
            st.download_button("Download results", df_hist.to_csv(index=False), file_name="scm_game_results.csv", mime="text/csv")
