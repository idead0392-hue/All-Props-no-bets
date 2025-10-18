import streamlit as st
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cfb_prop_predictor.workflow import run_workflow_sync

# --- Streamlit Page Configuration ---
st.set_page_config(
    page_title="CFB Prop Predictor",
    page_icon="🏈",
    layout="wide"
)

# --- UI Components ---
st.title("🏈 CFB Prop Predictor")
st.markdown("An AI-powered agent workflow to analyze and predict college football player props.")

st.sidebar.header("Prediction Inputs")
game = st.sidebar.text_input("Game (e.g., Alabama vs Georgia):", "Alabama vs Georgia")
player = st.sidebar.text_input("Player Name:", "Jalen Milroe")
prop_type = st.sidebar.selectbox(
    "Prop Type:",
    ["player_passing_yards", "player_rushing_yards", "player_receiving_yards"],
    index=0
)

if st.sidebar.button("▶️ Run Prediction"):
    request = {
        "game": game,
        "player": player,
        "prop_type": prop_type
    }
    
    with st.spinner("🔍 Agent is scraping live odds and running analysis..."):
        try:
            result = run_workflow_sync(request)
            
            prediction = result['prediction']
            analysis = result['analysis']
            gathered_data = result['gathered_data']

            # --- Display Results ---
            st.header(f"Prediction for {player}")

            col1, col2, col3 = st.columns(3)
            
            bet_color = "green" if prediction['recommended_bet'] == "over" else "red"
            col1.metric(
                label="Recommendation",
                value=f"{prediction['recommended_bet'].upper()} {gathered_data['odds_data']['prop_line'] if gathered_data.get('odds_data') else ''}"
            )
            
            col2.metric(label="Confidence", value=f"{prediction['confidence']}%")
            col3.metric(label="Projected Value", value=prediction['projected_value'], delta=f"{prediction['edge']} edge")
            
            st.subheader("📝 Reasoning & Analysis")
            st.info(analysis['summary'])
            
            with st.expander("Show Detailed Data"):
                st.write("**Risk Factors Identified:**")
                for risk in analysis['risk_factors']:
                    st.write(f"- {risk}")
                st.write("---")
                st.json(result)

        except Exception as e:
            st.error(f"An error occurred during the workflow: {e}")


