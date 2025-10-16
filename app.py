import streamlit as st
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="SCM Game Bot", layout="wide")
st.title("🏭 SCM Game Bot — Supply Chain Simulation with Learning Guidance & Dashboard")

# --- RESTART BUTTON ---
if st.sidebar.button("🔄 Restart Simulation"):
    st.session_state.clear()
    st.experimental_rerun()

# --- STAGE SELECTOR ---
st.sidebar.header("🧭 Navigate SCM Stages")
stage = st.sidebar.selectbox(
    "Select SCM Stage",
    ["Planning", "Sourcing", "Manufacturing", "Delivery", "Returns", "Final Results"]
)

# --- SESSION STATE ---
if "results" not in st.session_state:
    st.session_state.results = {
        "Planning": {},
        "Sourcing": {},
        "Manufacturing": {},
        "Delivery": {},
        "Returns": {},
    }

# --- HELPER FUNCTION ---
def display_stage_metrics(stage_name, metrics):
    """Display metrics for each stage and update session_state"""
    st.subheader(f"📊 {stage_name} Performance")
    for k, v in metrics.items():
        st.metric(k, f"{v:.2f}" if isinstance(v, (int, float)) else v)
    st.session_state.results[stage_name] = metrics

# --- STAGE 1: PLANNING ---
if stage == "Planning":
    st.header("📦 Stage 1: Planning — Demand & Forecasting")
    st.write("Plan your production to meet demand while maintaining inventory efficiency.")

    demand = st.slider("Forecasted Demand (Units)", 500, 5000, 2500, 100,
                       help="Expected customer demand units.")
    production_target = st.slider("Production Target (Units)", 500, 5000, 2400, 100,
                                  help="Planned production units. Too high increases inventory cost; too low risks lost sales.")
    safety_stock = st.slider("Safety Stock (%)", 5, 50, 20, 5,
                             help="Extra stock to handle unexpected demand fluctuations.")

    # Calculation
    cost_per_unit = 30
    revenue_per_unit = 50
    total_revenue = min(production_target, demand) * revenue_per_unit
    total_cost = production_target * cost_per_unit
    profit = total_revenue - total_cost
    inventory = production_target - demand + (safety_stock / 100) * demand

    metrics = {
        "Revenue": total_revenue,
        "Cost": total_cost,
        "Profit": profit,
        "Ending Inventory": inventory
    }
    display_stage_metrics("Planning", metrics)

    st.info("""
    **Learning Tips:**  
    - Match production to forecast to avoid excess inventory.  
    - Safety stock helps prevent stockouts.  
    - Overproduction increases cost without adding revenue.
    """)

# --- STAGE 2: SOURCING ---
elif stage == "Sourcing":
    st.header("🧾 Stage 2: Sourcing — Supplier & Procurement")

    supplier_efficiency = st.slider("Supplier Efficiency (%)", 50, 100, 80, 5,
                                    help="Efficiency/quality of supplier deliveries.")
    material_cost = st.slider("Material Cost per Unit ($)", 10, 50, 25, 5,
                              help="Cost to purchase each unit from supplier.")
    order_quantity = st.slider("Order Quantity (Units)", 500, 5000, 2000, 100,
                               help="Number of units ordered from supplier.")

    total_cost = order_quantity * material_cost
    delay_risk = 100 - supplier_efficiency
    quality_factor = supplier_efficiency / 100
    profit_impact = (quality_factor * 1000) - delay_risk * 5

    metrics = {
        "Procurement Cost": total_cost,
        "Delay Risk (%)": delay_risk,
        "Supplier Quality": quality_factor,
        "Profit Impact": profit_impact
    }
    display_stage_metrics("Sourcing", metrics)

    st.info("""
    **Learning Tips:**  
    - High-quality suppliers reduce defects and returns but may cost more.  
    - Low supplier efficiency increases delay risk.  
    - Balance cost vs quality to maximize profit.
    """)

# --- STAGE 3: MANUFACTURING ---
elif stage == "Manufacturing":
    st.header("🏭 Stage 3: Manufacturing — Efficiency & Output")

    machine_efficiency = st.slider("Machine Efficiency (%)", 60, 100, 85, 5,
                                   help="Operational efficiency of your machines.")
    defect_rate = st.slider("Defect Rate (%)", 0, 20, 5, 1,
                            help="Percentage of defective units produced.")
    labor_cost = st.slider("Labor Cost per Unit ($)", 10, 50, 25, 5,
                           help="Cost to produce one unit.")
    units_produced = st.slider("Units Produced", 1000, 5000, 3000, 100,
                               help="Total number of units manufactured.")

    good_units = units_produced * (1 - defect_rate / 100)
    production_cost = units_produced * labor_cost
    profit = (good_units * 50) - production_cost

    metrics = {
        "Good Units": good_units,
        "Production Cost": production_cost,
        "Profit": profit,
        "Efficiency": machine_efficiency
    }
    display_stage_metrics("Manufacturing", metrics)

    st.info("""
    **Learning Tips:**  
    - Minimize defect rates to increase revenue.  
    - Higher machine efficiency reduces cost per unit.  
    - Labor cost management impacts profitability.
    """)

# --- STAGE 4: DELIVERY ---
elif stage == "Delivery":
    st.header("🚚 Stage 4: Delivery — Logistics & Fulfillment")

    on_time_rate = st.slider("On-Time Delivery Rate (%)", 50, 100, 90, 5,
                             help="Percentage of orders delivered on time.")
    shipping_cost = st.slider("Shipping Cost per Unit ($)", 5, 30, 10, 1,
                              help="Cost to ship one unit.")
    distance = st.slider("Average Delivery Distance (km)", 100, 2000, 500, 50,
                         help="Average shipping distance.")
    units_shipped = st.slider("Units Shipped", 500, 5000, 2500, 100,
                              help="Number of units shipped.")

    total_shipping_cost = units_shipped * shipping_cost
    late_deliveries = (100 - on_time_rate) / 100 * units_shipped
    satisfaction = on_time_rate - (shipping_cost / 2)
    profit = (units_shipped * 50) - total_shipping_cost

    metrics = {
        "Shipping Cost": total_shipping_cost,
        "Late Deliveries": late_deliveries,
        "Customer Satisfaction": satisfaction,
        "Profit": profit
    }
    display_stage_metrics("Delivery", metrics)

    st.info("""
    **Learning Tips:**  
    - On-time delivery improves customer satisfaction.  
    - Choose shipping mode and cost wisely to maximize profit.  
    - Late deliveries can lead to lost sales and reputation damage.
    """)

# --- STAGE 5: RETURNS ---
elif stage == "Returns":
    st.header("🔁 Stage 5: Returns — After-Sales Management")

    return_rate = st.slider("Return Rate (%)", 0, 30, 10, 2,
                            help="Percentage of sold units returned by customers.")
    refurbish_cost = st.slider("Refurbish Cost per Unit ($)", 5, 25, 10, 1,
                               help="Cost to repair/refurbish returned units.")
    returned_units = st.slider("Returned Units", 0, 1000, 200, 10,
                               help="Total units returned.")

    total_refurbish_cost = returned_units * refurbish_cost
    resale_revenue = (returned_units * (1 - return_rate / 100)) * 40
    net_profit = resale_revenue - total_refurbish_cost

    metrics = {
        "Refurbish Cost": total_refurbish_cost,
        "Resale Revenue": resale_revenue,
        "Net Profit": net_profit
    }
    display_stage_metrics("Returns", metrics)

    st.info("""
    **Learning Tips:**  
    - Efficient refurbishment recovers value.  
    - Reducing return rates improves profit.  
    - Disposal costs reduce net profit; manage sustainably.
    """)

# --- FINAL RESULTS + DASHBOARD + KEY LEARNINGS ---
elif stage == "Final Results":
    st.header("🏆 Final SCM Performance Summary")

    total_profit = 0
    total_cost = 0
    total_revenue = 0
    profit_per_stage = {}
    revenue_cost_data = {}

    for stage_name, values in st.session_state.results.items():
        profit = values.get("Profit", values.get("Net Profit", 0))
        revenue = values.get("Revenue", values.get("Resale Revenue", 0))
        cost = values.get("Cost", values.get("Procurement Cost", 0)) + values.get("Production Cost", 0)

        total_profit += profit
        total_cost += cost
        total_revenue += revenue

        profit_per_stage[stage_name] = profit
        revenue_cost_data[stage_name] = [revenue, cost]

    # --- Metrics ---
    st.subheader("💹 Overall KPIs")
    st.metric("💰 Total Profit", f"${total_profit:,.2f}")
    st.metric("📦 Total Cost", f"${total_cost:,.2f}")
    st.metric("📈 Total Revenue", f"${total_revenue:,.2f}")

    # --- Dashboard Charts ---
    st.subheader("📊 Stage-wise Profit")
    st.bar_chart(profit_per_stage)

    st.subheader("📊 Revenue vs Cost per Stage")
    rev_cost_df = pd.DataFrame(revenue_cost_data, index=["Revenue", "Cost"])
    st.bar_chart(rev_cost_df.T)

    # --- Key Learnings ---
    st.subheader("📝 Key Learnings")
    learnings = []

    # Planning
    pl = st.session_state.results.get("Planning", {})
    if pl.get("Ending Inventory", 0) > 1000:
        learnings.append("Planning: Inventory is high → consider reducing production or safety stock.")
    if pl.get("Profit", 0) < 0:
        learnings.append("Planning: Profit is negative → adjust production vs demand.")

    # Sourcing
    sc = st.session_state.results.get("Sourcing", {})
    if sc.get("Delay Risk (%)", 0) > 20:
        learnings.append("Sourcing: High supplier delay risk → choose higher-quality suppliers.")
    if sc.get("Profit Impact", 0) < 0:
        learnings.append("Sourcing: Supplier choices negatively impact profit.")

    # Manufacturing
    mf = st.session_state.results.get("Manufacturing", {})
    if mf.get("Efficiency", 0) < 75:
        learnings.append("Manufacturing: Machine efficiency is low → optimize operations.")
    if mf.get("Profit", 0) < 0:
        learnings.append("Manufacturing: Profit is negative → check defect rates or production cost.")

    # Delivery
    dl = st.session_state.results.get("Delivery", {})
    if dl.get("Customer Satisfaction", 0) < 50:
        learnings.append("Delivery: Customer satisfaction is low → improve on-time deliveries.")
    if dl.get("Profit", 0) < 0:
        learnings.append("Delivery: Delivery cost is too high → optimize shipping.")

    # Returns
    rt = st.session_state.results.get("Returns", {})
    if rt.get("Net Profit", 0) < 0:
        learnings.append("Returns: Net profit from returns is negative → reduce return rate or refurbish cost.")

    if learnings:
        for l in learnings:
            st.info(l)
    else:
        st.success("Great job! All metrics look good. Keep optimizing for even better performance.")

    st.write("✅ Adjust earlier stages to explore different SCM strategies and see the impact on overall performance.")
