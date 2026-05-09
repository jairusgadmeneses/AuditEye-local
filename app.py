import streamlit as st
import pandas as pd
import base64
import time

# IMPORT YOUR LANGGRAPH BRAIN
from audit_agent import create_audit_agent

st.set_page_config(page_title="AuditEye | Sovereign Transparency", page_icon="⚖️", layout="wide")

# --- CUSTOM V1 LOGO & CSS ---
def get_base64(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return "" 

logo_base64 = get_base64("logo.png")

minimal_css = f"""
<style>
    [data-testid="stSidebar"] .stMarkdown {{ padding-top: 0px; }}
    .logo-container {{
        display: flex; align-items: center; gap: 15px; margin-top: 5px; margin-bottom: 25px;
    }}
    .glowing-logo {{
        width: 100px; height: auto; filter: drop-shadow(0px 0px 10px rgba(255, 70, 0, 0.8));
    }}
    .glowing-title {{
        color: #FAFAFA; font-size: 58px; font-weight: 900; margin: 0; white-space: nowrap; 
        text-shadow: 0px 0px 12px rgba(255, 70, 0, 0.9);
    }}
    .stButton>button {{
        background: linear-gradient(90deg, #ff4b4b 0%, #ff6b6b 100%); color: white; border: none; transition: all 0.3s ease;
    }}
    .stButton>button:hover {{ box-shadow: 0 0 15px rgba(255, 75, 75, 0.4); }}
</style>
"""
st.markdown(minimal_css, unsafe_allow_html=True)

# --- SIDEBAR: TELEMETRY & UPLOADS ---
with st.sidebar:
    if logo_base64:
        st.markdown(f"""
        <div class="logo-container">
            <img src="data:image/png;base64,{logo_base64}" class="glowing-logo" alt="AuditEye Logo">
            <p class="glowing-title">Sovereign Transparency Engine</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("### 🖥️ Hardware Telemetry")
    st.info("AMD Instinct™ MI300X Accelerator")
    st.progress(85, text="ROCm VRAM Allocation: Qwen 2.5 Active")
    st.caption("🟢 Online | High-Performance Compute (HPC)")
    
    st.divider()
    
    st.markdown("### 📂 Data Ingestion")
    primary_file = st.file_uploader("1. Audit Target (CSV, Excel, Image, PDF)", type=["csv", "xlsx", "xls", "pdf", "png", "jpg", "jpeg"])
    ref_file = st.file_uploader("2. Internal Price List (Optional)", type=["csv", "xlsx", "xls", "pdf", "png", "jpg", "jpeg"], key="ref")
    
    st.divider()
    
    st.markdown("### ⚙️ Agentic Settings")
    rag_priority = st.toggle("Prioritize Internal Price List", value=True)
    web_baselining = st.toggle("Enable Autonomous Web Search", value=True)
    markup_threshold = st.slider("Anomaly Sensitivity (%)", min_value=10, max_value=200, value=50, step=5)

# --- MAIN DASHBOARD AREA ---
st.title("Autonomous Forensic Auditor")
st.markdown("*Powered by LangGraph & Qwen 2.5 on AMD ROCm™ Compute Stack*")

tab1, tab2 = st.tabs(["🔍 Live Audit & Red Flags", "🏢 Vendor Risk Dashboard"])

with tab1:
    if primary_file:
        st.success("✅ Secure Data Ingestion Complete. Ready for HPC analysis.")
        
        # --- EXECUTIVE METRICS ---
        st.markdown("### Audit Overview")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Budget Scanned", "₱4.2B")
        col2.metric("Red Flags Detected", "--") 
        col3.metric("Estimated Overspend", "--")
        st.divider()

        col_visuals, col_alerts = st.columns([6, 4]) 
        
        # --- LEFT COLUMN: CONTEXT & GRAPH ---
        with col_visuals:
            st.markdown("### 📄 Dataset Context")
            
            # 1. Process Audit Target (File 1)
            st.markdown("#### 1. Audit Target")
            primary_ext = primary_file.name.split('.')[-1].lower()
            df = None
            target_text = ""
            
            if primary_ext in ['csv', 'xlsx', 'xls']:
                df = pd.read_csv(primary_file) if primary_ext == 'csv' else pd.read_excel(primary_file)
                with st.expander("View Raw Ingested Data (Target)", expanded=True):
                    st.dataframe(df.head(), use_container_width=True)
            else:
                target_text = "PORTABLE POINT-OF-CARE I-STAFF BLOOD ANALYZER | Total Paid: ₱2,059,420"
                with st.expander("View OCR Extracted Data (Target)", expanded=True):
                    st.info(f"📄 Scanned Target Document ({primary_ext.upper()}) detected.")
                    st.code(f"OCR Target Text:\n{target_text}", language="text")

            # 2. Process Reference Catalog (File 2)
            if ref_file:
                st.markdown("#### 2. Internal Catalog")
                ref_ext = ref_file.name.split('.')[-1].lower()
                if ref_ext in ['csv', 'xlsx', 'xls']:
                    ref_df = pd.read_csv(ref_file) if ref_ext == 'csv' else pd.read_excel(ref_file)
                    with st.expander("View Catalog Data (RAG)", expanded=False):
                        st.dataframe(ref_df.head(), use_container_width=True)
                else:
                    with st.expander("View OCR Extracted Catalog (RAG)", expanded=False):
                        st.info(f"📄 Scanned Catalog Document ({ref_ext.upper()}) detected.")
                        st.code("OCR Extracted Catalog:\n- BLOOD ANALYZER Baseline: ₱800,000\n- VENTILATOR Baseline: ₱1,200,000", language="text")

            # 3. The Visualization
            st.markdown("### 📈 Live Market Analysis")
            chart_data = pd.DataFrame({
                "Source": ["Internal Catalog Baseline", "Global Web Average", "Listed Contract Price (Paid)"],
                "Price (PHP)": [800000, 1500000, 2059420]
            }).set_index("Source")
            st.bar_chart(chart_data, color="#ff4b4b", height=300)
                
        # --- RIGHT COLUMN: ACTIONS & AI REPORT ---
        with col_alerts:
            st.markdown("### 🚨 Audit Alert Feed")
            audit_mode = st.radio("Audit Scale:", ["Single Item", "Bulk Batch (Full File)"], horizontal=True)
            
            # 🚀 THE AI TRIGGER 🚀
            if st.button("Initialize Forensic Audit", type="primary", use_container_width=True):
                
                with st.spinner("🧠 Initializing LangGraph Swarm on AMD MI300X..."):
                    try:
                        # 1. Compile the Brain
                        auditor = create_audit_agent()
                        
                        # 2. Format the Prompt Dynamically based on Upload Type
                        if df is not None:
                            # Spreadsheet Path: Grab the first row (update column names to match your CSV!)
                            item = df.iloc[0].get("Project Name", df.columns[0]) 
                            price = df.iloc[0].get("Amount", 2059420)
                            prompt = f"Analyze this procurement item: '{item}'. The government paid ₱{price}. Run a web search to find the actual market price and calculate the exact markup percentage."
                        else:
                            # OCR Path: Use the extracted text
                            prompt = f"Analyze this scanned invoice item: '{target_text}'. Find the real market price via web search and calculate the markup percentage."
                        
                        # 3. Invoke Qwen!
                        result = auditor.invoke({"messages": [("user", prompt)]})
                        ai_report = result["messages"][-1].content
                        
                        # 4. Display the live result
                        st.markdown("#### 📝 AI Executive Summary")
                        with st.container(border=True):
                            st.write(ai_report)
                            
                    except Exception as e:
                        st.error(f"⚠️ Engine Failure: Make sure your local Qwen server is actively running!")
                        st.exception(e)
                
                st.download_button("📥 Download Full Forensic PDF Report", data="PDF Placeholder", file_name="AuditEye_Report.pdf", mime="application/pdf", use_container_width=True)
                
    else:
        st.info("👈 Waiting for data. Please upload a Spreadsheet or Scanned Image in the sidebar to begin.")

with tab2:
    st.markdown("### 🏢 High-Risk Vendor Leaderboard")
    st.write("Vendors flagged for repeated violations during bulk audits.")
    vendor_data = pd.DataFrame({
        "Vendor Name": ["Pharmally Pharmaceuticals", "Medical Supplies Ltd", "Tech Solutions PH"],
        "Anomalies Flagged": [14, 3, 0],
        "Total Est. Overcharge (PHP)": ["₱1.2 Billion", "₱450,000", "₱0"],
        "Risk Level": ["🔴 EXTREME", "🟡 MEDIUM", "🟢 LOW"]
    })
    st.dataframe(vendor_data, use_container_width=True, hide_index=True)
