# logic/sim_engine.py

import random

# --- Helper for consistency ---
def format_result(profit, cost, revenue, inventory, lost_sales, notes):
    return {
        "profit": round(profit, 2),
        "cost": round(cost, 2),
        "revenue": round(revenue, 2),
        "inventory_change": round(inventory, 2),
        "lost_sales": int(lost_sales),
        "notes": notes
    }

# --- Stage 1: Planning ---
def simulate_planning(demand_forecast, production_target, safety_stock):
    demand_variation = random.uniform(-0.1, 0.15)
    actual_demand = demand_forecast * (1 + demand_variation)
    gap = production_target - actual_demand
    cost = production_target * 40
    revenue = actual_demand * 70
    inventory = gap + safety_stock
    lost_sales = max(0, actual_demand - production_target)
    profit = revenue - cost - (inventory * 10)

    notes = (
        f"Demand variation: {demand_variation:.1%}. "
        f"Actual demand = {actual_demand:.0f} units. "
        f"{'Overproduction' if gap > 0 else 'Underproduction'} by {abs(gap):.0f} units."
    )
    return format_result(profit, cost, revenue, inventory, lost_sales, notes)


# --- Stage 2: Sourcing ---
def simulate_sourcing(supplier_choice, order_qty, lead_time_tolerance):
    supplier_risk = {"A": 0.05, "B": 0.10, "C": 0.20}[supplier_choice]
    delay = random.random() < supplier_risk
    delay_penalty = order_qty * 5 if delay else 0
    cost = order_qty * (100 if supplier_choice == "A" else 90 if supplier_choice == "B" else 80)
    revenue = order_qty * 120
    profit = revenue - cost - delay_penalty
    lost_sales = order_qty * 0.05 if delay else 0

    notes = f"Supplier {supplier_choice} {'delayed shipment' if delay else 'delivered on time'}."
    return format_result(profit, cost, revenue, 0, lost_sales, notes)


# --- Stage 3: Manufacturing ---
def simulate_manufacturing(production_rate, defect_rate, machine_utilization):
    good_units = production_rate * (1 - defect_rate / 100)
    cost = production_rate * 60
    revenue = good_units * 100
    downtime_penalty = (100 - machine_utilization) * 5
    profit = revenue - cost - downtime_penalty
    inventory = good_units - production_rate
    lost_sales = max(0, production_rate - good_units)

    notes = f"Defect rate: {defect_rate}%. Utilization: {machine_utilization}%. Output: {good_units:.0f} units."
    return format_result(profit, cost, revenue, inventory, lost_sales, notes)


# --- Stage 4: Delivery / Logistics ---
def simulate_delivery(shipment_size, transport_mode, route_efficiency):
    mode_cost = {"Air": 200, "Sea": 100, "Road": 150}[transport_mode]
    delay_chance = {"Air": 0.05, "Sea": 0.15, "Road": 0.10}[transport_mode]
    delayed = random.random() < delay_chance
    delay_penalty = shipment_size * 15 if delayed else 0
    base_cost = shipment_size * mode_cost
    cost = base_cost + delay_penalty
    revenue = shipment_size * 250 * route_efficiency
    profit = revenue - cost
    lost_sales = shipment_size * 0.02 if delayed else 0

    notes = f"Mode: {transport_mode}. {'Delay occurred' if delayed else 'Delivered on time'}."
    return format_result(profit, cost, revenue, 0, lost_sales, notes)


# --- Stage 5: Returns / After-sales ---
def simulate_returns(return_rate, refurbish_rate, disposal_cost):
    total_returns = 1000 * (return_rate / 100)
    refurbish_units = total_returns * (refurbish_rate / 100)
    disposal_units = total_returns - refurbish_units
    recovered_value = refurbish_units * 80
    cost = disposal_units * disposal_cost + refurbish_units * 20
    revenue = recovered_value
    profit = revenue - cost
    lost_sales = total_returns - refurbish_units

    notes = (
        f"Returns: {total_returns:.0f} units. Refurbished: {refurbish_units:.0f} units. "
        f"Disposed: {disposal_units:.0f} units."
    )
    return format_result(profit, cost, revenue, 0, lost_sales, notes)
