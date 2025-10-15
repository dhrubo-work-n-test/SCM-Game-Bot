import random

# Helper: create result dictionary
def result_dict(stage, profit=0, inventory=0, cost=0, revenue=0, lost_sales=0):
    return {
        "stage": stage,
        "profit": profit,
        "inventory": inventory,
        "cost": cost,
        "revenue": revenue,
        "lost_sales": lost_sales
    }

# Stage 1 – Planning
def simulate_planning(demand_forecast, production_target, safety_stock):
    demand_variation = random.uniform(0.9, 1.1)
    actual_demand = demand_forecast * demand_variation
    inventory_change = production_target - actual_demand + safety_stock

    cost = production_target * 8  # $8/unit
    revenue = actual_demand * 15  # $15/unit
    profit = revenue - cost
    lost_sales = max(0, actual_demand - (production_target + safety_stock))

    return result_dict("Planning", profit, inventory_change, cost, revenue, lost_sales)

# Stage 2 – Sourcing
def simulate_sourcing(supplier_quality, supplier_cost, order_volume):
    delay_factor = (100 - supplier_quality) / 100
    cost = order_volume * supplier_cost
    lost_sales = order_volume * delay_factor * 0.1
    revenue = order_volume * 0.2 * supplier_quality
    profit = revenue - cost * delay_factor
    inventory_change = order_volume * (1 - delay_factor)

    return result_dict("Sourcing", profit, inventory_change, cost, revenue, lost_sales)

# Stage 3 – Manufacturing
def simulate_manufacturing(production_efficiency, labor_hours, machine_utilization):
    base_output = labor_hours * (machine_utilization / 100) * (production_efficiency / 100)
    cost = labor_hours * 15 + machine_utilization * 20
    revenue = base_output * 25
    profit = revenue - cost
    lost_sales = max(0, 1000 - base_output)
    inventory_change = base_output - 1000

    return result_dict("Manufacturing", profit, inventory_change, cost, revenue, lost_sales)

# Stage 4 – Delivery
def simulate_delivery(transport_mode, delivery_speed, logistics_cost):
    mode_factor = {"Truck": 1.0, "Rail": 0.8, "Air": 1.5}[transport_mode]
    satisfaction = max(0, 100 - delivery_speed * 5)
    cost = logistics_cost * mode_factor
    revenue = satisfaction * 50
    profit = revenue - cost
    inventory_change = -random.randint(50, 200)
    lost_sales = 200 - satisfaction

    return result_dict("Delivery", profit, inventory_change, cost, revenue, lost_sales)

# Stage 5 – Returns
def simulate_returns(return_rate, refurbish_cost, customer_service_score):
    returns = return_rate * 10
    cost = returns * refurbish_cost + (10000 - customer_service_score)
    revenue = max(0, customer_service_score * 0.5)
    profit = revenue - cost
    lost_sales = return_rate * 5
    inventory_change = -returns

    return result_dict("Returns", profit, inventory_change, cost, revenue, lost_sales)
