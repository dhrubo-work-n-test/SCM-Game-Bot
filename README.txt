
SCM Game Bot - Streamlit Prototype
Files created:
- products.csv: product master data
- suppliers.csv: supplier profiles
- demand_timeseries.csv: monthly demand for each product (36 months)
- scenarios.csv: 500 random scenarios/events to drive gameplay
- logic/sim_engine.py: simulation functions for each SCM stage
- app.py: streamlit app to run the game locally

How to run:
1. On a machine with Python and Streamlit installed, copy the 'scm_game_bot' folder.
2. Install requirements: pip install streamlit pandas numpy
3. Run: streamlit run app.py
4. Use the UI to play through 5 stages. Use sliders as controls.
