
import random
from datetime import datetime

def simulate_planning(product, decision, demand, state):
    """
    decision: dict with keys: order_qty, safety_stock, expediting (True/False), choose_supplier (supplier_id)
    state: previous state dict containing inventory, profit, metrics
    """
    inv = state.get("inventory", 0)
    profit = state.get("profit", 0.0)
    costs = 0.0
    revenue = 0.0

    unit_cost = product["unit_cost"] * decision.get("supplier_cost_mult", 1.0)
    sell_price = product["sell_price"]
    order_qty = int(decision.get("order_qty", 0))
    safety_stock = int(decision.get("safety_stock", 0))
    expediting = decision.get("expediting", False)
    lead_time_days = decision.get("lead_time_days", 14)
    transport_cost = decision.get("transport_cost", 0.0)

    # Supply arrives this cycle for simplicity
    supply = order_qty
    inv += supply
    # Fulfill demand
    sold = min(inv, demand)
    inv -= sold
    revenue += sold * sell_price

    # Costs: purchase + holding + transport + expediting penalty
    purchase_cost = order_qty * unit_cost
    holding_cost = max(0, inv) * product["holding_cost_per_unit_per_month"]
    expediting_cost = (0.25 * purchase_cost) if expediting else 0.0
    costs += purchase_cost + holding_cost + transport_cost + expediting_cost

    # Penalty for stockout (lost sales)
    lost_sales = max(0, demand - (supply + state.get("inventory_before",0)))
    lost_sales_cost = lost_sales * (sell_price * 0.4)  # lost margin
    costs += lost_sales_cost

    profit += (revenue - costs)
    metrics = {
        "inventory": inv,
        "profit": profit,
        "revenue": revenue,
        "costs": costs,
        "sold": sold,
        "lost_sales": lost_sales
    }
    return metrics

def simulate_sourcing(product, decision, state):
    # simplified sourcing: choose supplier, affects lead_time and cost
    supplier_mult = decision.get("supplier_cost_mult", 1.0)
    reliability = decision.get("supplier_reliability", 90)
    # small immediate effect: cost adjustment
    state["profit"] -= 0  # no immediate profit change; affects future stages
    return {"supplier_mult": supplier_mult, "reliability": reliability}

def simulate_manufacturing(product, decision, state):
    # decision: produce_qty, overtime (True/False), capacity_increase_pct
    produce_qty = int(decision.get("produce_qty", 0))
    unit_cost = product["unit_cost"] * 0.9  # in-house cheaper
    prod_cost = produce_qty * unit_cost
    if decision.get("overtime", False):
        prod_cost *= 1.25  # overtime premium
    state["profit"] -= prod_cost
    state["inventory"] = state.get("inventory",0) + produce_qty
    return {"prod_cost": prod_cost, "inventory": state["inventory"], "profit": state["profit"]}

def simulate_delivery(product, decision, state):
    # decision: transport_mode ('sea','air','road'), expedite_pct
    transport_mode = decision.get("transport_mode","sea")
    transport_multiplier = {"sea":1.0,"road":1.2,"air":1.8}.get(transport_mode,1.0)
    transport_cost = state.get("inventory",0) * 0.05 * transport_multiplier
    state["profit"] -= transport_cost
    return {"transport_cost": transport_cost, "profit": state["profit"]}

def simulate_returns(product, decision, state):
    # decision: lenient_return_policy (True/False), refurbish_rate
    return_rate = decision.get("return_rate", 0.02)
    returned_units = int(state.get("sold",0) * return_rate)
    refurbish_cost = returned_units * product["unit_cost"] * 0.4
    state["profit"] -= refurbish_cost
    state["inventory"] += returned_units * decision.get("put_back_pct",0.5)
    return {"returned_units": returned_units, "refurbish_cost": refurbish_cost, "inventory": state["inventory"], "profit": state["profit"]}
