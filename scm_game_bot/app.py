import streamlit as st
import pandas as pd
import requests
import random
import os
from scm_logic import SCMGame

# ---------------------- PAGE CONFIG ----------------------
st.set_page_config(page_title="SCM Game Bot", layout="wide")

# ---------------------- DARK BACKGROUND ----------------------
dark_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #0e1117;
    color: #ffffff;
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}
[data-testid="stSidebar"] {
    background-color: #161a23;
}
h1, h2, h3, h4, h5, h6, p, div, span {
    color: #ffffff !important;
}
.stButton>button {
    background-color: #00adb5;
    color: white;
    border-radius: 10px;
    font-weight: bold;
}
.stButton>button:hover {
    background-color: #05c2cb;
    color: black;
}
</style>
"""
st.markdown(dark_bg, unsafe_allow_html=True)

# ---------------------- INIT GAME ----------------------
if "game" not in st.session_state:
    data_path = os.path.join(os.path.dirname(__file__), "data") + "/"
    st.session_state.game = SCMGame(data_path=data_path)
    st.session_state.logs = []

game = st.session_state.game

# ---------------------- HEADER ----------------------
st.title("🤖 SCM Game Bot – Experiential Learning for Supply Chain Consultants")
st.markdown("Welcome to the **SCM Game Bot**! Step into the shoes of a Supply Chain Consultant and navigate the 5 critical stages below.")

# ---------------------- SCM STAGES ----------------------
st.markdown("""
### 🏗️ Supply Chain Stages:
1️⃣ **Planning** – Forecast demand and align resources.  
2️⃣ **Sourcing** – Choose suppliers and manage procurement.  
3️⃣ **Manufacturing** – Optimize production and minimize waste.  
4️⃣ **Delivery / Logistics** – Manage transportation and ensure timely delivery.  
5️⃣ **Returns / After-sales Service** – Handle returns and improve customer satisfaction.
""")

# ---------------------- DECISION SECTION ----------------------
st.subheader("🧩 Make Your SCM Decisions")

col1, col2 = st.columns(2)
with col1:
    stage = st.selectbox("Select Supply Chain Stage", 
                         ["Planning", "Sourcing", "Manufacturing", "Delivery/Logistics", "Returns/After-sales Service"])
with col2:
    action = st.text_input("Enter Your Decision (e.g., Increase inventory buffer, Switch supplier, etc.)")

if st.button("Submit Decision"):
    feedback = game.process_decision(stage, action)
    st.session_state.logs.append(f"Stage: {stage} | Action: {action} | Feedback: {feedback}")
    st.success(feedback)

# ---------------------- LOGS SECTION ----------------------
with st.expander("📜 View Game Logs"):
    if st.session_state.logs:
        for log in st.session_state.logs:
            st.text(log)
    else:
        st.write("No decisions made yet!")

# ---------------------- FACT OF THE DAY ----------------------
st.markdown("---")
st.subheader("💡 Supply Chain Fact of the Day")
facts = [
    "90% of world trade is transported via global shipping networks.",
    "The 'Just-in-Time' concept originated at Toyota to minimize inventory costs.",
    "AI and ML are now essential tools for demand forecasting in SCM.",
    "Container ships can carry more than 20,000 standard containers at once.",
    "Reverse logistics can make up nearly 10% of total supply chain costs."
]
st.info(random.choice(facts))

# ------------------ SUPPLY CHAIN NEWS ------------------ #
st.markdown("---")
st.markdown("<div class='section-title'>📰 Daily Supply Chain News</div>", unsafe_allow_html=True)

try:
    NEWS_API = "https://newsdata.io/api/1/news?apikey=pub_e4d7b2dfecaa4b4db0de9a55242cd38f&q=supply%20chain%20management&language=en"
    response = requests.get(NEWS_API)
    if response.status_code == 200:
        articles = response.json().get("results", [])
        if articles:
            article = articles[0]  # Only the first article
            title = article.get("title", "No title")
            description = article.get("description", "")
            short_desc = " ".join(description.split()[:50]) + "..." if description else "No description available."
            link = article.get("link", "#")

            # Display as subheader inside a rounded box
            st.markdown(f"""
                <div class='news-box'>
                    <h4 style='color:#00ADB5'>{title}</h4>
                    <p>{short_desc} <a href="{link}" target="_blank">Read more</a></p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("No live news available right now. Try again later.")
    else:
        st.warning("⚠️ Could not fetch news right now.")
except Exception as e:
    st.error(f"Error fetching news: {e}")

