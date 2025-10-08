import pandas as pd
import numpy as np
import random

class SCMGame:
    def __init__(self, data_path="data/"):
        # Load synthetic data
        self.suppliers = pd.read_csv(data_path + "suppliers.csv")
        self.demand = pd.read_csv(data_path + "demand.csv")
        self.manufacturing = pd.read_csv(data_path + "manufacturing.csv")

        # Game state
        self.week = 1
        self.total_profit = 0
        self.customer_satisfaction = 100
        self.inventory = 500  # starting inventory
        self.stage = "Planning"

    # ---------------- STAGE 1: PLANNING ---------------- #
    def planning_stage(self, forecast_adjustment):
        """Player adjusts demand forecast"""
        base_demand = self.demand.loc[self.demand["week"] == self.week, "forecast_demand"].values[0]
        adjusted = base_demand + forecast_adjustment

        print(f"[Planning] Week {self.week} | Base Forecast: {base_demand} | Adjusted: {adjusted}")
        return adjusted

    # ---------------- STAGE 2: SOURCING ---------------- #
    def sourcing_stage(self, supplier_choice):
        """Choose a supplier"""
        supplier = self.suppliers[self.suppliers["name"] == supplier_choice].iloc[0]
        cost = supplier["cost_per_unit"]
        reliability = supplier["reliability"]
        lead_time = supplier["lead_time_days"]

        print(f"[Sourcing] Supplier: {supplier_choice}, Cost: {cost}, Reliability: {reliability}, Lead Time: {lead_time}")
        return supplier.to_dict()

    # ---------------- STAGE 3: MANUFACTURING ---------------- #
    def manufacturing_stage(self, plant_choice, units_to_produce):
        """Simulate production outcome"""
        plant = self.manufacturing[self.manufacturing["plant_id"] == plant_choice].iloc[0]
        effective_output = int(units_to_produce * plant["efficiency"])
        production_cost = effective_output * plant["cost_per_unit"]

        print(f"[Manufacturing] Plant {plant_choice} | Produced: {effective_output} | Cost: {production_cost}")
        self.inventory += effective_output
        return effective_output, production_cost

    # ---------------- STAGE 4: DELIVERY ---------------- #
    def delivery_stage(self, delivery_mode):
        """Handle logistics"""
        cost = {"Air": 10, "Sea": 5, "Road": 7}[delivery_mode]
        delay = {"Air": 1, "Sea": 5, "Road": 3}[delivery_mode]
        satisfaction_change = -delay * 2

        print(f"[Delivery] Mode: {delivery_mode} | Delay: {delay} days | Cost per unit: {cost}")
        self.customer_satisfaction += satisfaction_change
        return cost, delay

    # ---------------- STAGE 5: RETURNS ---------------- #
    def returns_stage(self, return_rate):
        """Handle product returns"""
        returned_units = int(self.inventory * return_rate)
        loss = returned_units * 5  # fixed loss per unit

        print(f"[Returns] Returned Units: {returned_units} | Loss: {loss}")
        self.inventory -= returned_units
        self.total_profit -= loss
        return returned_units, loss

    # ---------------- EVALUATION ---------------- #
    def evaluate_week(self):
        """Calculate weekly performance"""
        demand_actual = self.demand.loc[self.demand["week"] == self.week, "actual_demand"].values[0]
        sold_units = min(self.inventory, demand_actual)
        revenue = sold_units * 15  # fixed price per unit
        cost = random.randint(2000, 3000)  # total weekly cost estimate
        profit = revenue - cost

        self.inventory -= sold_units
        self.total_profit += profit

        print(f"[Week {self.week} Summary] Revenue: {revenue}, Cost: {cost}, Profit: {profit}, Inventory left: {self.inventory}")
        self.week += 1
        return {"revenue": revenue, "profit": profit, "inventory_left": self.inventory}
