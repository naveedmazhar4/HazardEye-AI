# app.py
import streamlit as st
from PIL import Image
import cv2
import numpy as np
import time

# Import real modules
from agents.hazard_detection import detect_hazards_with_boxes
from agents.risk_analysis import analyze_risk
from agents.action_plan import generate_action_plan
from agents.report_generator import generate_report
from utils.alerts import send_whatsapp_alert
from utils.voice import speak

# ----------------- Page Config -----------------
st.set_page_config(
    page_title="HazardEye - Industrial Safety",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- Session State -----------------
if "camera_running" not in st.session_state:
    st.session_state.camera_running = False
if "last_hazards" not in st.session_state:
    st.session_state.last_hazards = []

# ----------------- Header -----------------
st.markdown("""
<div style="background-color:#1F1F2E;padding:20px;border-radius:10px;text-align:center;">  
    <h1 style="color:#00AEEF;font-family:sans-serif;">🛠 HazardEye</h1>  
    <h4 style="color:#4CAF50;font-family:sans-serif;">Autonomous Industrial Safety Monitoring</h4>  
</div>  
""", unsafe_allow_html=True)

# ----------------- Tabs -----------------
tabs = st.tabs(["🏠 Home", "🖼 Detector", "📄 Reports", "ℹ️ About", "📞 Contact"])

# ================= HOME =================
with tabs[0]:
    st.markdown("""
    <div style='background-color:#00AEEF;color:white;padding:20px;border-radius:10px;text-align:center'>
        <h2>Welcome to HazardEye</h2>
        <p>Detect hazards, calculate risk, generate action plans, and send alerts — all autonomously!</p>
    </div>
    """, unsafe_allow_html=True)
    st.image("assets/bg_welcome.jpg", use_container_width=True)

# ================= DETECTOR =================
with tabs[1]:
    st.markdown("<h3>Hazard Detection</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    # --- IMAGE UPLOAD ---  
    with col1:
        uploaded_file = st.file_uploader("Upload an image", type=["jpg","png","jpeg"])
        if uploaded_file:
            img = Image.open(uploaded_file)
            st.image(img, caption="Uploaded Image", use_container_width=True)

            frame, hazards = detect_hazards_with_boxes(np.array(img))
            risk_score, risk_level = analyze_risk(hazards)
            plan = generate_action_plan(hazards, risk_level)

            st.subheader("Detected Hazards")
            st.write(hazards if hazards else "No hazards detected")
            st.subheader(f"Risk Score: {risk_score} | Risk Level: {risk_level}")
            st.subheader("Suggested Action Plan")
            for step in plan:
                st.write(f"- {step}")

            if st.button("Generate Full Report"):
                pdf_file_path = generate_report(img, hazards, risk_score, plan)
                with open(pdf_file_path, "rb") as f:
                    pdf_bytes = f.read()
                st.success("✅ Report generated!")
                st.download_button("📥 Download Report", data=pdf_bytes,
                                   file_name="HazardEye_Report.pdf", mime="application/pdf")

            if hazards and sorted(hazards) != sorted(st.session_state.last_hazards):
                send_whatsapp_alert(hazards, risk_level)
                speak(f"Attention! {risk_level} risk detected with hazards: {', '.join(hazards)}")
                st.session_state.last_hazards = hazards

    # --- LIVE CAMERA ---  
    with col2:
        st.info("⚡ Live Camera Feed")
        st_frame = st.empty()
        st_plan = st.empty()

        # Start / Stop buttons
        col_start, col_stop = st.columns(2)
        with col_start:
            if st.button("Start Monitoring"):
                st.session_state.camera_running = True
                st.session_state.last_hazards = []
        with col_stop:
            if st.button("Stop Monitoring"):
                st.session_state.camera_running = False

        # Camera feed
        cap = cv2.VideoCapture(0)
        if st.session_state.camera_running:
            ret, frame = cap.read()
            if ret:
                frame, hazards = detect_hazards_with_boxes(frame)
                risk_score, risk_level = analyze_risk(hazards)
                plan = generate_action_plan(hazards, risk_level)

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                st_frame.image(frame_rgb, caption=f"Hazards: {hazards} | Risk: {risk_level}", use_container_width=True)

                st_plan.subheader("Suggested Action Plan")
                for step in plan:
                    st_plan.write(f"- {step}")

                if hazards and sorted(hazards) != sorted(st.session_state.last_hazards):
                    send_whatsapp_alert(hazards, risk_level)
                    speak(f"Attention! {risk_level} risk detected with hazards: {', '.join(hazards)}")
                    st.session_state.last_hazards = hazards

            time.sleep(1)
            st.experimental_rerun()
        else:
            st_frame.text("Camera not running. Click 'Start Monitoring'.")
            cap.release()

# ================= REPORTS =================
with tabs[2]:
    st.markdown("<h3>Generate Safety Report</h3>", unsafe_allow_html=True)
    st.info("Select past sessions to generate report")
    st.checkbox("Include all annotated images", value=True)
    st.checkbox("Include Action Log", value=True)
    st.checkbox("Summary Statistics Only", value=False)
    if st.button("Generate Report"):
        st.success("✅ Report Generated!")

# ================= ABOUT =================
with tabs[3]:
    st.markdown("<h3>About HazardEye</h3>", unsafe_allow_html=True)
    st.markdown("""
HazardEye is an **autonomous, agentic AI system** for industrial safety.
- Detects hazards in real-time
- Generates actionable safety plans using GPT
- Produces detailed safety reports
- Sends alerts via voice and WhatsApp
""")

# ================= CONTACT =================
with tabs[4]:
    st.markdown("<h3>Contact Us</h3>", unsafe_allow_html=True)
    st.markdown("""
Have questions or need assistance? Reach out to our team. HazardEye is here to ensure industrial safety.

**Email:** support@hazardeye.com  
**Phone / WhatsApp:** +92-300-1234567  
**Address:** 123 Industrial Safety Rd, Tech City, Pakistan

You can also follow us on:
- [LinkedIn](https://www.linkedin.com/)
- [Twitter](https://twitter.com/)
- [GitHub](https://github.com/)
""")


