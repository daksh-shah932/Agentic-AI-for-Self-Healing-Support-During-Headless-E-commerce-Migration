import streamlit as st
import json
import pandas as pd
import subprocess
import os
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Agentic Support | Self-Healing System", layout="wide")

# --- CSS STYLING ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #FAFAFA; }
    .risk-high { color: #ff4b4b; border: 1px solid #ff4b4b; padding: 2px 8px; border-radius: 4px; font-weight: bold; }
    .risk-low { color: #21c354; border: 1px solid #21c354; padding: 2px 8px; border-radius: 4px; font-weight: bold; }
    .metric-card { background-color: #262730; padding: 15px; border-radius: 8px; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

# --- FILE OPERATIONS ---
def load_tickets():
    if os.path.exists("tickets.json"):
        with open("tickets.json", "r") as f: return json.load(f)
    return []

def save_new_ticket(merchant_id, message):
    tickets = load_tickets()
    new_id = len(tickets) + 1
    tickets.append({"ticket_id": new_id, "merchant_id": int(merchant_id), "message": message})
    with open("tickets.json", "w") as f:
        json.dump(tickets, f, indent=2)

def run_backend_agent():
    """Runs the python main.py script and waits for it to finish."""
    with st.spinner("🤖 Agent is Observing, Reasoning, and Clustering..."):
        subprocess.run(["python", "main.py"])
        time.sleep(1) 
    st.success("Analysis Complete!")
    st.rerun()

def load_agent_analysis():
    if os.path.exists("analysis_output.json"):
        with open("analysis_output.json", "r") as f: return json.load(f)
    return []

# ==========================================
# SIDEBAR NAVIGATION & SIMULATOR
# ==========================================
st.sidebar.title("🎛️ Control Panel")

# 1. VIEW MODE TOGGLE (Fixes the missing e-commerce side)
view_mode = st.sidebar.radio(
    "Select Persona:", 
    ["Platform Ops (Internal)", "Merchant (External)"]
)

st.sidebar.markdown("---")

# 2. TICKET SIMULATOR
st.sidebar.subheader("⚡ Ticket Simulator")
with st.sidebar.form("new_ticket_form"):
    m_id = st.text_input("Merchant ID", "44")
    msg = st.text_area("Support Message", "loading internet high")
    submitted = st.form_submit_button("📩 Send Ticket")

    if submitted:
        save_new_ticket(m_id, msg)
        st.sidebar.success("Ticket Sent!")
        run_backend_agent()

if st.sidebar.button("🔄 Rerun Agent Manually"):
    run_backend_agent()

# ==========================================
# MAIN DASHBOARD LOGIC
# ==========================================
tickets = load_tickets()
clusters = load_agent_analysis()

# --- VIEW 1: PLATFORM OPS (Internal) ---
if view_mode == "Platform Ops (Internal)":
    st.title("🛡️ Agentic Support Operations")
    
    # Global Stats
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Tickets", len(tickets))
    c2.metric("Active Clusters", len(clusters))
    c3.metric("System Status", "Operational" if len(clusters) < 2 else "Degraded")

    st.markdown("---")

    if not clusters:
        st.info("No clusters detected. Try sending a ticket from the sidebar!")
    else:
        left_col, right_col = st.columns([1, 2])
        
        with left_col:
            st.subheader("🔴 Incident Clusters")
            for c in clusters:
                risk_label = "HIGH RISK" if c['risk'] == 'High' else "LOW RISK"
                with st.expander(f"[{risk_label}] {c['title']}", expanded=True):
                    st.caption(f"{len(c['ticket_ids'])} Tickets • {c['stage']}")
                    st.progress(c['confidence'])
                    st.write(f"**Action:** {c['timeline']['Decide']}")
        
        with right_col:
            st.subheader("Deep Dive: Agent Reasoning")
            active = clusters[0] 
            st.markdown(f"### {active['title']}")
            
            # Timeline Visualization
            st.markdown("#### 🧠 Reasoning Timeline")
            st.json(active['timeline'])
            
            # Restraint Box
            st.markdown("#### 🛑 Automation Restraint")
            st.error(f"**Action Not Taken:** {active['restraint']['action_not_taken']}")
            st.caption(f"Reason: {active['restraint']['reason']}")

            if active['repro_pack']:
                st.success(f"✅ Repro Pack Generated: {active['repro_pack']['id']}")

# --- VIEW 2: MERCHANT PORTAL (External) ---
else:
    st.title("🛍️ Merchant Support Portal")
    
    # Merchant Login Simulation
    st.markdown("Simulating logged-in Merchant view...")
    
    # Check if there are clusters affecting generic merchants
    # (In a real app, we filter by the logged-in ID)
    if not clusters:
        st.success("✅ All systems operational. Your store is healthy.")
    else:
        st.warning("⚠️ We are experiencing elevated error rates.")
        
        for c in clusters:
            st.markdown(f"""
            <div class="metric-card">
                <h3>System Notice: {c['root_cause']}</h3>
                <p>We have detected an issue affecting your store's checkout.</p>
                <p><strong>Status:</strong> {c['timeline']['Decide']}</p>
                <p><em>No action required on your part. Engineering is investigating.</em></p>
            </div>
            """, unsafe_allow_html=True)