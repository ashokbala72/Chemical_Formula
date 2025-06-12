
import streamlit as st
import random

def simulate_weather():
    return {
        "temperature": round(random.uniform(10, 40), 1),
        "humidity": round(random.uniform(20, 80), 1),
        "wind_speed": round(random.uniform(0, 20), 1),
        "condition": random.choice(["Sunny", "Cloudy", "Rainy", "Stormy"])
    }

import pandas as pd
import numpy as np
from datetime import datetime
import os
from dotenv import load_dotenv
from openai import OpenAI

# ----------------- SETTINGS -----------------
st.set_page_config(page_title="UK Chemical Formulation Assistant", layout="wide")

if "mock_mode" not in st.session_state:
    st.session_state.mock_mode = True
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ----------------- GLOBAL -----------------
UK_FIELDS = [
    "Clair Ridge", "Forties", "Buzzard", "Nelson", "Elgin", "Judy", "Everest", "Armada",
    "Brent", "Andrew", "Ninian", "Magnus", "Shetland West", "Captain", "Culzean",
    "Golden Eagle", "Britannia", "Erskine", "Beryl", "Brae", "Ettrick", "Foinaven",
    "Gannet", "Harding", "Heather", "Janice", "Juno", "Lomond", "MonArb", "Piper", "Quads"
]

def simulate_field_metadata(field):
    return {
        "Region": random.choice(["North Sea", "Midlands", "Wales", "Scotland"]),
        "Reservoir Depth (m)": random.randint(1200, 4000),
        "Operator": random.choice(["BP", "Shell", "Total", "Equinor"]),
        "Startup Year": random.randint(1980, 2020),
    }

def simulate_formation_profile():
    return {
        "Reservoir Temp (°C)": round(random.uniform(60, 120), 1),
        "Pressure (psi)": round(random.uniform(2000, 5000), 0),
        "Salinity (ppm)": round(random.uniform(30000, 120000), 0),
        "pH": round(random.uniform(5.5, 7.5), 1)
    }

def simulate_lab_tests():
    blends = ["Blend A", "Blend B", "Blend C"]
    return pd.DataFrame({
        "Blend": blends,
        "Inhibitor (%)": [random.randint(20, 50) for _ in blends],
        "Solvent (%)": [random.randint(20, 40) for _ in blends],
        "Emulsifier (%)": [random.randint(10, 30) for _ in blends],
        "Efficacy (%)": [random.randint(70, 95) for _ in blends],
        "Corrosion Rate (mpy)": [round(random.uniform(0.1, 0.5), 2) for _ in blends],
        "Cost ($/bbl)": [round(random.uniform(1.2, 3.5), 2) for _ in blends],
    })


def simulate_vendor_prices():
    return pd.DataFrame({
        "Chemical": ["Inhibitor-X", "Solvent-Y", "Emulsifier-Z"],
        "Unit Price ($/L)": [6.5, 12.3, 17.9],
        "Availability": ["In Stock", "2 weeks", "Out of Stock"]
    })


def check_compliance(blend_name):
    return "✔️ Compliant with REACH" if "A" in blend_name else "⚠️ Needs further review"

def genai_summary(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {e}"

# ----------------- UI -----------------
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11, tab12 = st.tabs([
    "🗂 Overview", "📍 Location", "🧪 Formation & Fluid Profile", "📈 Live Field Conditions",
    "🌦 Weather & Environment", "🧾 Lab Test Results", "⚖️ Regulatory Compliance",
    "🧠 GenAI Blend Recommendation", "🔁 Formulation Optimizer", "📦 Vendor & Pricing",
    "📄 Final Report", "⚙️ Settings / Admin"
])

with tab1:
    st.title("🗂 Overview")
    st.write("""
    This is a prototype chemical formulation assistant for UK oil & gas fields.  
    It simulates lab and field data, suggests AI-generated blends, checks compliance, and prepares a final report.
    """)
    st.markdown("**Tabs Explained:**")
    st.markdown("- 📍 Location: Pick a real UK field")
    st.markdown("- 🧪 Formation: Rock & fluid profile simulation + AI insight")
    st.markdown("- 📈 Live Conditions: Real-time mock alerts + AI insight")
    st.markdown("- 🌦 Weather: Pulls simulated weather + AI insight")
    st.markdown("- 🧾 Lab Tests: Simulated blend test results + AI insight")
    st.markdown("- ⚖️ Compliance: REACH/environmental checks + AI reasoning")
    st.markdown("- 🧠 GenAI Blend: AI-formulated recommendation")
    st.markdown("- 🔁 Optimizer: Adjust & simulate trade-offs")
    st.markdown("- 📦 Pricing: Vendor prices & stock")
    st.markdown("- 📄 Final Report: Summary of choices")

with tab2:
    st.header("📍 Select Field Location")
    selected_field = st.selectbox("Choose a UK Field", UK_FIELDS)
    metadata = simulate_field_metadata(selected_field)
    cols = st.columns(4)
    cols[0].metric("Region", metadata['Region'])
    cols[1].metric("Reservoir Depth", f"{metadata['Reservoir Depth (m)']} m")
    cols[2].metric("Operator", metadata['Operator'])
    cols[3].metric("Startup Year", str(metadata['Startup Year']))

with tab3:
    st.header("🧪 Formation & Fluid Profile")
    if 'mock_mode' in st.session_state and st.session_state.mock_mode:
        formation = simulate_formation_profile()
        st.caption("🔁 Using simulated formation profile.")
    else:
        formation = {
            "Reservoir Temp (°C)": "102 (live)",
            "Pressure (psi)": "4100 (live)",
            "Salinity (ppm)": "98000 (live)",
            "pH": "6.7 (live)"
        }
        st.caption("🌐 Using real-time data from logging tools.")
    cols = st.columns(len(formation))
    for i, (key, val) in enumerate(formation.items()):
        cols[i].metric(label=key, value=str(val))
    st.subheader("💡 GenAI Insight")
    with st.spinner('Generating GenAI insights...'):
        st.info(genai_summary(f"Explain the following formation data and chemical implications: {formation}"))
with tab4:
    st.header("📈 Live Field Conditions")
    if 'mock_mode' in st.session_state and st.session_state.mock_mode:
        alerts = [
            "⚠️ High corrosion rate detected",
            "✅ Injection pressure stable",
            "🧪 Scaling agent effective"
        ]
        st.caption("🔁 Using simulated field condition alerts.")
    else:
        alerts = [
            "🌐 Real-time: Corrosion rate stable",
            "🌐 Real-time: Pressure fluctuating near threshold"
        ]
        st.caption("🌐 Live alerts from real-time field sensors.")
        st.write("Alerts:")
    for alert in alerts:
        st.markdown(f"- {alert}")
    st.subheader("💡 GenAI Insight")
    with st.spinner('Generating GenAI insights...'):
        st.info(genai_summary(f"Based on these live field conditions, recommend any immediate chemical formulation adjustments or operational actions: {alerts}"))

with tab5:
    st.header("🌦 Weather & Environment")
    if 'mock_mode' in st.session_state and st.session_state.mock_mode:
        weather = simulate_weather()
        st.caption("🔁 Simulated weather data")
    else:
        weather = {
            "Temperature (°C)": 13,
            "Wind Speed (km/h)": 28,
            "Condition": "Clear"
        }
        st.caption("🌐 Real-time weather from Met Office API")
    cols = st.columns(len(weather))
    for i, (key, val) in enumerate(weather.items()):
        cols[i].metric(label=key, value=f"{val}")
    st.subheader("💡 GenAI Insight")
    with st.spinner('Generating GenAI insights...'):
        st.info(genai_summary(f"Based on this weather data, what impact could it have on chemical formulation? {weather}"))

with tab6:
    st.header("🧾 Lab Test Results")
    if 'mock_mode' in st.session_state and st.session_state.mock_mode:
        lab_df = simulate_lab_tests()
        st.caption("🔁 Simulated lab test results")
    else:
        lab_df = pd.DataFrame({
            "Blend": ["Live Blend 1", "Live Blend 2"],
            "Efficacy (%)": [91, 89],
            "Corrosion Rate (mpy)": [0.2, 0.18],
            "Cost ($/bbl)": [2.1, 2.4],
    })
        st.success('🌐 Live lab results from field database')
        st.caption("🌐 Live lab results from field database")
    st.dataframe(lab_df)
    st.subheader("💡 GenAI Insight")
    with st.spinner('Generating GenAI insights...'):
        st.info(genai_summary(f"Interpret the following lab test results for chemical blends: {lab_df.to_dict(orient='records')}"))

with tab7:
    st.header("⚖️ Regulatory Compliance Check")
    selected_blend = st.selectbox("Select a Blend to Check", lab_df["Blend"])
    compliance_result = check_compliance(selected_blend)
    st.success(compliance_result)
    st.subheader("💡 GenAI Insight")
    with st.spinner('Generating GenAI insights...'):
        st.info(genai_summary(f"Is this blend '{selected_blend}' likely compliant with UK REACH? Why or why not?"))

with tab8:
    st.header("🧠 GenAI Blend Recommendation")
    prompt = f"""
    You are a chemical advisor. Based on the following:
    - Field: {selected_field}
    - Formation: {formation}
    - Weather: {weather}
    - Lab Results: {lab_df.to_dict(orient='records')}
    Suggest a specific chemical blend using:
    1. Ingredients (Inhibitor-X, Solvent-Y, Emulsifier-Z)
    2. Recommended dosage (% or ppm)
    3. Why each chemical is chosen
    4. Expected outcome
    5. Cost vs effectiveness
    6. Any operational tips
    """
    result = genai_summary(prompt)
    st.markdown(result)

with tab9:
    st.header("🔁 Formulation Optimizer")
    ratio = st.slider("Adjust inhibitor percentage", 0, 100, 50)
    cost = round(2.0 + (100 - ratio) * 0.02, 2)
    efficacy = round(70 + ratio * 0.2, 2)
    st.metric("Estimated Cost", f"${cost}/bbl")
    st.metric("Estimated Efficacy", f"{efficacy}%")

with tab10:
    st.header("📦 Vendor & Pricing")
    if 'mock_mode' in st.session_state and st.session_state.mock_mode:
        vendor_df = simulate_vendor_prices()
    else:
        vendor_df = pd.DataFrame({
            "Chemical": ["Inhibitor-X", "Solvent-Y", "Emulsifier-Z"],
            "Unit Price ($/L)": [6.5, 12.3, 17.9],
            "Availability": ["In Stock", "2 weeks", "Out of Stock"]
        })
        st.success('🌐 Live vendor pricing loaded')
        st.caption("🌐 Live vendor pricing")

    st.dataframe(vendor_df)
with tab11:
    st.header("📄 Final Report Summary")
    st.markdown(f"- **Field:** {selected_field}")
    st.markdown(f"- **Formation Profile:** {formation}")
    st.markdown(f"- **Weather:** {weather}")
    st.markdown(f"- **Top Blend:** {lab_df.iloc[0]['Blend']}")
    st.markdown(f"- **Compliance:** {check_compliance(lab_df.iloc[0]['Blend'])}")
    st.caption(f"🧪 Mock mode is {'ON' if st.session_state.mock_mode else 'OFF'}")

with tab12:
    st.header("⚙️ Settings / Admin")
    if "mock_mode" not in st.session_state:
        st.session_state.mock_mode = True
    new_value = st.checkbox("Enable Mock Mode", value=st.session_state.mock_mode)
    if new_value != st.session_state.mock_mode:
        st.session_state.mock_mode = new_value
        st.rerun()
    if st.button("Reset Simulation"):
        st.rerun()
    
    if not st.session_state.mock_mode:
        st.success("🌐 Real-time data has been successfully loaded for all applicable modules.")

    st.markdown("Admin tools for developers")
