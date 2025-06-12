
import streamlit as st
import random
import pandas as pd
import numpy as np
from datetime import datetime
import os
from dotenv import load_dotenv
from openai import OpenAI

# ----------------- SETTINGS -----------------
st.set_page_config(page_title="UK Chemical Formulation Assistant", layout="wide")
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
        "Efficacy (%)": [random.randint(70, 95) for _ in blends],
        "Corrosion Rate (mpy)": [round(random.uniform(0.1, 0.5), 2) for _ in blends],
        "Cost ($/bbl)": [round(random.uniform(1.2, 3.5), 2) for _ in blends],
    })

def simulate_weather():
    return {
        "Temperature (°C)": random.randint(-2, 15),
        "Wind Speed (km/h)": random.randint(10, 45),
        "Condition": random.choice(["Rainy", "Cloudy", "Clear", "Storm"]),
    }

def simulate_vendor_prices():
    chemicals = ["Inhibitor-X", "Solvent-Y", "Emulsifier-Z"]
    return pd.DataFrame({
        "Chemical": chemicals,
        "Unit Price ($/L)": [round(random.uniform(5, 20), 2) for _ in chemicals],
        "Availability": [random.choice(["In Stock", "2 weeks", "4 weeks"]) for _ in chemicals],
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
    formation = simulate_formation_profile()
    cols = st.columns(len(formation))
    for i, (key, val) in enumerate(formation.items()):
        cols[i].metric(label=key, value=f"{val:,}")
    st.subheader("💡 GenAI Insight")
    st.info(genai_summary(f"Explain the following formation data and chemical implications: {formation}"))

with tab4:
    st.header("📈 Live Field Conditions (Mocked)")
    alerts = [
        "⚠️ High corrosion rate detected",
        "✅ Injection pressure stable",
        "🧪 Scaling agent effective"
    ]
    st.write("Simulated Alerts:")
    for alert in alerts:
        st.markdown(f"- {alert}")
    st.subheader("💡 GenAI Insight")
    st.info(genai_summary(f"Based on these live field conditions, recommend any immediate chemical formulation adjustments or operational actions: {alerts}"))

with tab5:
    st.header("🌦 Weather & Environment")
    weather = simulate_weather()
    cols = st.columns(len(weather))
    for i, (key, val) in enumerate(weather.items()):
        cols[i].metric(label=key, value=f"{val}")
    st.subheader("💡 GenAI Insight")
    st.info(genai_summary(f"Based on this weather data, what impact could it have on chemical formulation? {weather}"))

with tab6:
    st.header("🧾 Lab Test Results")
    lab_df = simulate_lab_tests()
    st.dataframe(lab_df)
    st.subheader("💡 GenAI Insight")
    st.info(genai_summary(f"Interpret the following lab test results for chemical blends: {lab_df.to_dict(orient='records')}"))

with tab7:
    st.header("⚖️ Regulatory Compliance Check")
    selected_blend = st.selectbox("Select a Blend to Check", lab_df["Blend"])
    compliance_result = check_compliance(selected_blend)
    st.success(compliance_result)
    st.subheader("💡 GenAI Insight")
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
    3. Why each chemical is chosen (e.g. salty water, rust prevention)
    4. Expected outcome (e.g. fewer blockages, less rust)
    5. Cost vs effectiveness
    6. Any operational tips
    Make it clear and helpful.
    """
    result = genai_summary(prompt)
    st.markdown(result)
with tab9:
    st.header("🔁 Formulation Optimizer")
    st.write("Simulate performance by adjusting blend ratios (mock)")
    ratio = st.slider("Adjust inhibitor percentage", 0, 100, 50)
    cost = round(2.0 + (100 - ratio) * 0.02, 2)
    efficacy = round(70 + ratio * 0.2, 2)
    st.metric("Estimated Cost", f"${cost}/bbl")
    st.metric("Estimated Efficacy", f"{efficacy}%")

with tab10:
    st.header("📦 Vendor & Pricing")
    vendor_df = simulate_vendor_prices()
    st.dataframe(vendor_df)

with tab11:
    st.header("📄 Final Report Summary")
    st.markdown(f"- **Field:** {selected_field}")
    st.markdown(f"- **Formation Profile:** {formation}")
    st.markdown(f"- **Weather:** {weather}")
    st.markdown(f"- **Top Blend:** {lab_df.iloc[0]['Blend']}")
    st.markdown(f"- **Compliance:** {check_compliance(lab_df.iloc[0]['Blend'])}")

with tab12:
    st.header("⚙️ Settings / Admin")
    if st.button("Reset Simulation"):
        st.experimental_rerun()
    st.checkbox("Enable Mock Mode", value=True)
    st.markdown("Admin tools for developers")
