```python
import streamlit as st
import pandas as pd
import requests
import random
import os
from scm_logic import SCMGame

# ---------- CONFIG ----------
st.set_page_config(page_title="SCM Game Bot", layout="wide")

# ---------- PAGE BACKGROUND ----------
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: linear-gradient(135deg, #c3e0e5, #f9f9f9);
    background-size: cover;
}
[data-testid="stHeader"] {
    background-color: rgba(0,0,0,0);
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ---------- GAME INITIALIZATION ----------
if "game" not in st.session_state:
    data_path = os.path.join(os.path.dirname(__file__), "data") + "/"
    st.session_state.game = SCMGame(data_path=data_path)
    st.session_state.logs = []

game = st.session_state.game

st.title("🤖 SCM Game Bot – Experiential Supply Chain Learning")

# ---------- MAIN INTERACTION ----------
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

# ---------- COLLAPSIBLE LOGS ----------
with st.expander("📜 View Game Logs"):
    if st.session_state.logs:
        for log in st.session_state.logs:
            st.text(log)
    else:
        st.write("No decisions made yet!")

# ---------- FACT OF THE DAY ----------
st.markdown("---")
st.subheader("💡 Supply Chain Fact of the Day")
facts = [
    "Did you know? 90% of world trade is carried by the global shipping industry.",
    "The term 'Just-in-Time' was popularized by Toyota to reduce waste and increase efficiency.",
    "Artificial Intelligence is transforming demand forecasting in modern supply chains.",
    "A single container ship can carry over 20,000 containers across the world!",
    "Reverse logistics (returns) can account for up to 10% of total supply chain costs."
]
st.info(random.choice(facts))

# ---------- LIVE SUPPLY CHAIN NEWS ----------
st.markdown("---")
st.subheader("📰 Latest in Supply Chain Management")

API_KEY = "pub_e4d7b2dfecaa4b4db0de9a55242cd38f"
url = f"https://newsdata.io/api/1/news?apikey={API_KEY}&q=supply%20chain%20management&language=en"

try:
    response = requests.get(url)
    data = response.json()

    if "results" in data:
        for i, article in enumerate(data["results"][:3]):
            st.markdown(f"**{article.get('title', 'No title')}**")
            st.caption(article.get("source_id", "Unknown Source"))
            st.write(article.get("description", "No description available."))
            if article.get("link"):
                st.markdown(f"[Read more →]({article['link']})")
            st.markdown("---")
    else:
        st.warning("No live news available right now. Try again later.")
except Exception as e:
    st.error(f"Error fetching news: {e}")
```
