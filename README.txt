# SCM Game Bot – Experiential Supply Chain Simulator 🎮

## Overview  
The SCM Game Bot is an interactive, browser-based simulation built with [Streamlit](https://streamlit.io) that places you in the role of a Supply Chain Consultant. Through the key stages of supply chain management (Planning → Sourcing → Manufacturing → Delivery → Returns), you’ll make strategic decisions, observe their impact on profit, customer satisfaction and inventory, and learn how real-world supply chains operate.  

This tool is ideal for:
- New joiners in supply-chain, logistics or operations roles
- Training and upskilling sessions for consultants or business analysts
- Engaging team workshops and experiential learning

---

## Why do we need this game?  
While many trainings cover supply chain in theory, learners often struggle to connect concepts to decisions in a live business environment.  
This simulation bridges that gap by:  
- Providing hands-on scenario-based decision making  
- Visualising trade-offs and consequences (cost vs speed vs quality)  
- Encouraging curiosity, reflection and iterative improvement  

---

## How it works – Game Flow  
You’ll progress through five supply chain stages:  

1. **Planning** – Adjust your forecast and determine production levels.  
2. **Sourcing** – Select suppliers based on cost, reliability and lead time.  
3. **Manufacturing** – Choose plant capacity, production units and manage efficiency.  
4. **Delivery / Logistics** – Pick shipping mode (Air / Road / Sea) and manage cost vs speed.  
5. **Returns / After-sales Service** – Set return rate, handle losses and impact on satisfaction.  

Once all stages are completed, click *Evaluate Week* to view your performance metrics – profit, inventory, and customer satisfaction – and review your decision log.  

---

## Key Metrics  
| Metric | Description |
|--------|-------------|
| **Total Profit** | Revenue minus all costs (sourcing + manufacturing + delivery + return losses). A key indicator of supply-chain efficiency. |
| **Customer Satisfaction** | Reflects service quality, timeliness of delivery, and product availability. High satisfaction supports brand & retention. |
| **Inventory** | Units still in stock post-sales and returns. Too high means wasted cost; too low risks missed sales. |

---

## Getting Started  
### Prerequisites  
- Python 3.9+  
- `pip` for package installation  

### Installation & Run  
```bash
git clone https://github.com/dhrubo-work-n-test/SCM-Game-Bot.git
cd SCM-Game-Bot
pip install -r requirements.txt
streamlit run app.py
