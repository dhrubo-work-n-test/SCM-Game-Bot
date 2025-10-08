import streamlit as st 
import pandas as pd 
import requests 
import random 
import os 
from scm_logic import SCMGame
# ------------------ PAGE CONFIG & STYLE ------------------ #
st.set_page_config(page_title="Supply Chain Simulator", layout="wide")
st.markdown("""
    <style>
    body { background-color: #0E1117; color: white; }
    .stButton>button { background-color: #00ADB5; color: white; border-radius: 10px; padding: 0.6em 1.2em; font-weight: bold; }
    .stButton>button:hover { background-color: #02C39A; color: black; }
    .news-box, .fact-box, .log-box {
        background-color: #1E1E1E; 
        border-radius: 15px; 
        padding: 15px 20px;
        margin: 10px 0;
        box-shadow: 0 0 10px rgba(0,0,0,0.4);
    }
    .section-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #00ADB5;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------ INITIAL SETUP ------------------ #
import os
from scm_logic import SCMGame
data_path = os.path.join(os.path.dirname(__file__), "data") + "/"
game = SCMGame(data_path=data_path)

if "messages" not in st.session_state:
    st.session_state.messages = []
# ---------------------- HEADER ---------------------- #
st.title("🤖 SCM Game Bot – Experiential Learning for Supply Chain Consultants")
st.markdown("Welcome to the **SCM Game Bot**! Step into the shoes of a Supply Chain Consultant and navigate the 5 critical stages below.")
# ------------------ WELCOME / INSTRUCTIONS POP-UP ------------------ #
if "show_instructions" not in st.session_state:
    st.session_state.show_instructions = True

if st.session_state.show_instructions:
    with st.expander("🎮 Welcome to SCM Game Bot! How to Play", expanded=True):
        st.markdown("""
        **Welcome to the SCM Game Bot!**  

        In this interactive game, you step into the shoes of a Supply Chain Consultant.  
        You will navigate through the **five critical stages of a supply chain**:

        1️⃣ **Planning** – Forecast demand and align resources.  
        2️⃣ **Sourcing** – Choose suppliers and manage procurement.  
        3️⃣ **Manufacturing** – Optimize production and minimize waste.  
        4️⃣ **Delivery / Logistics** – Manage transportation and ensure timely delivery.  
        5️⃣ **Returns / After-sales Service** – Handle returns and improve customer satisfaction.  

        **Objective:** Maximize profit, keep customers happy, and manage inventory efficiently.  

        Click the **“Close Instructions”** button below to start playing the game.
        """)
        if st.button("Close Instructions"):
            st.session_state.show_instructions = False

# ---------------------- SCM STAGES ---------------------- #
st.markdown("""
### 🏗️ Supply Chain Stages:
1️⃣ **Planning** – Forecast demand and align resources.  
2️⃣ **Sourcing** – Choose suppliers and manage procurement.  
3️⃣ **Manufacturing** – Optimize production and minimize waste.  
4️⃣ **Delivery / Logistics** – Manage transportation and ensure timely delivery.  
5️⃣ **Returns / After-sales Service** – Handle returns and improve customer satisfaction.
""")


# ------------------ STAGES ------------------ #
# STAGE 1: Planning
st.header("1️⃣ Planning Stage")
forecast_adjustment = st.slider("Adjust forecast (± units)", -50, 50, 0)
if st.button("Run Planning Stage"):
    adjusted = game.planning_stage(forecast_adjustment)
    st.session_state.messages.append(f"📊 Adjusted forecast to {adjusted} units.")

# STAGE 2: Sourcing
st.header("2️⃣ Sourcing Stage")
supplier_choice = st.selectbox("Choose supplier:", game.suppliers["name"].tolist())
if st.button("Run Sourcing Stage"):
    supplier = game.sourcing_stage(supplier_choice)
    st.session_state.messages.append(
        f"🏭 Selected supplier: {supplier_choice} (Cost: {supplier['cost_per_unit']}, Reliability: {supplier['reliability']})"
    )

# STAGE 3: Manufacturing
st.header("3️⃣ Manufacturing Stage")
plant_choice = st.selectbox("Select plant ID:", game.manufacturing["plant_id"].tolist())
units_to_produce = st.number_input("Units to produce:", min_value=50, max_value=1000, step=50)
if st.button("Run Manufacturing Stage"):
    output, cost = game.manufacturing_stage(plant_choice, units_to_produce)
    st.session_state.messages.append(f"⚙️ Produced {output} units at cost {cost}")

# STAGE 4: Delivery
st.header("4️⃣ Delivery Stage")
delivery_mode = st.selectbox("Choose delivery mode:", ["Air", "Sea", "Road"])
if st.button("Run Delivery Stage"):
    cost, delay = game.delivery_stage(delivery_mode)
    st.session_state.messages.append(f"🚚 Delivery via {delivery_mode}: Delay {delay} days, Cost {cost}/unit")

# STAGE 5: Returns
st.header("5️⃣ Returns Stage")
return_rate = st.slider("Return rate (0–20%)", 0.0, 0.2, 0.05)
if st.button("Run Returns Stage"):
    returned_units, loss = game.returns_stage(return_rate)
    st.session_state.messages.append(f"🔁 {returned_units} units returned, Loss: {loss}")

# EVALUATE WEEK
if st.button("✅ Evaluate Week"):
    results = game.evaluate_week()
    st.session_state.messages.append(
        f"📈 Week Summary → Revenue: {results['revenue']} | Profit: {results['profit']} | Inventory left: {results['inventory_left']}"
    )

# ------------------ METRICS / POINTS ------------------ #
st.markdown("---")
st.subheader("🏆 Your Performance")
col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Profit", f"{game.total_profit}")
col2.metric("😊 Customer Satisfaction", f"{game.customer_satisfaction}")
col3.metric("📦 Inventory", f"{game.inventory}")

# ------------------ DAILY SUPPLY CHAIN FACT ------------------ #
st.markdown("---")
st.markdown("<div class='section-title'>💡 Daily Supply Chain Fact</div>", unsafe_allow_html=True)
import random
facts = [
    "Amazon’s predictive logistics system can forecast and pre-ship products before customers order them!",
    "Over 90% of world trade is carried by the shipping industry.",
    "Walmart’s supply chain efficiency saved the company over $2 billion annually.",
    "Toyota’s Just-in-Time system revolutionized lean manufacturing globally.",
    "The global supply chain industry is worth over $10 trillion as of 2025."
]
st.markdown(f"<div class='fact-box'>{random.choice(facts)}</div>", unsafe_allow_html=True)

# ------------------ DAILY SUPPLY CHAIN NEWS ------------------ #
st.markdown("---")
st.markdown("<div class='section-title'>📰 Daily Supply Chain News</div>", unsafe_allow_html=True)

try:
    NEWS_API = "https://newsdata.io/api/1/news?apikey=pub_e4d7b2dfecaa4b4db0de9a55242cd38f&q=supply%20chain%20management&language=en"
    response = requests.get(NEWS_API)
    if response.status_code == 200:
        articles = response.json().get("results", [])
        if articles:
            article = articles[0]  # Only the first news article
            title = article.get("title", "No title")
            description = article.get("description", "")
            short_desc = " ".join(description.split()[:50]) + "..." if description else "No description available."
            link = article.get("link", "#")

            # Rounded box for news content
            st.markdown(f"""
                <div class='fact-box'>
                    <b>{title}</b><br>
                    {short_desc} <a href="{link}" target="_blank">Read more</a>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("No live news available right now. Try again later.")
    else:
        st.warning("⚠️ Could not fetch news right now.")
except Exception as e:
    st.error(f"Error fetching news: {e}")


# ------------------ GAME LOG ------------------ #
st.markdown("---")
# Collapsible log at the bottom
with st.expander("🧾 Game Log", expanded=False):
    if st.session_state.messages:
        for msg in reversed(st.session_state.messages):
            st.markdown(f"<div class='log-box'>{msg}</div>", unsafe_allow_html=True)
    else:
        st.info("No game activity yet. Play the stages to see logs here.")


