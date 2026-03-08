import streamlit as st
from PIL import Image

# Import internal modules
from utils import common_disclaimer, setup_logger
from interaction_engine import fuzzy_match_medicine, check_interactions
from ai_engine import generate_interaction_explanation, parse_prescription_text
from symptom_engine import analyze_symptoms
from side_effect_engine import analyze_side_effects
from risk_engine import calculate_risk_score
from ocr_utils import extract_text_from_image

logger = setup_logger(__name__)

# Configure Streamlit page
st.set_page_config(
    page_title="MedSafe AI",
    page_icon="⚕️",
    layout="wide"
)

# Header
st.title("⚕️ MedSafe AI")
st.markdown("### Intelligent Medicine Safety and Prescription Analysis Platform")
st.info(common_disclaimer())

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "💊 Medicine Interaction Checker",
    "📄 Prescription OCR Analyzer",
    "🤒 Symptom & Doubt Solver",
    "⚠️ Side Effect Monitor",
    "📊 Emergency Risk Predictor"
])

# ----------------- TAB 1: Medicine Interaction Checker -----------------
with tab1:
    st.header("Medicine Interaction Checker")
    st.write("Enter multiple medicines to check for known interactions.")
    
    med_input = st.text_input("Enter medicine names (comma separated):", placeholder="e.g., Paracetamol, Ibuprofen")
    
    if st.button("Check Interactions"):
        if med_input:
            raw_meds = [m.strip() for m in med_input.split(',')]
            matched_meds = []
            
            st.write("### Identified Medicines:")
            for m in raw_meds:
                matched_name, score = fuzzy_match_medicine(m)
                if score > 80:
                    matched_meds.append(matched_name)
                    st.success(f"✔️ {m} -> Matched as **{matched_name}** (Confidence: {score:.1f}%)")
                else:
                    st.warning(f"❌ {m} -> Could not find a high confidence match.")
            
            if len(matched_meds) > 1:
                st.write("### Interaction Results:")
                interactions = check_interactions(matched_meds)
                
                if not interactions:
                    st.success("No known interactions found between the identified medicines.")
                else:
                    for idx, inter in enumerate(interactions):
                        meds = inter['meds']
                        sev = inter['severity']
                        desc = inter['description']
                        
                        severity_color = "red" if sev.lower() == "high" else "orange"
                        st.markdown(f"<h4 style='color: {severity_color}'>⚠️ Interaction: {meds[0].title()} & {meds[1].title()} ({sev.title()} Severity)</h4>", unsafe_allow_html=True)
                        st.write(desc)
                        
                        # AI Explanation expansion
                        with st.expander("🤖 AI Explanation"):
                            with st.spinner("Generating explanation..."):
                                exp = generate_interaction_explanation(meds[0], meds[1], sev)
                                st.write(exp)
        else:
            st.error("Please enter at least one medicine.")

# ----------------- TAB 2: Prescription OCR Analyzer -----------------
with tab2:
    st.header("Prescription OCR Analyzer")
    st.write("Upload a prescription image to extract medicine names automatically.")
    
    uploaded_file = st.file_uploader("Choose an image (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Prescription", width=400)
        
        if st.button("Extract Data"):
            with st.spinner("Extracting text via Tesseract OCR..."):
                raw_text = extract_text_from_image(image)
            
            if raw_text:
                with st.expander("Show Raw OCR Text"):
                    st.text(raw_text)
                    
                with st.spinner("Parsing text with AI Engine..."):
                    parsed_data = parse_prescription_text(raw_text)
                    
                st.write("### Extracted Medicines:")
                meds = parsed_data.get("medicines", [])
                if meds:
                    for m in meds:
                        st.success(f"💊 Name: **{m.get('name', 'N/A')}** | Salt: **{m.get('salt', 'N/A')}**")
                else:
                    st.warning("AI could not structure any medicines from the text.")
            else:
                st.error("Text extraction failed. Try a clearer image.")

# ----------------- TAB 3: Symptom & Doubt Solver -----------------
with tab3:
    st.header("Symptom & Doubt Solver")
    st.write("Describe your symptoms to receive advice and warning levels.")
    
    symp_input = st.text_area("Describe your symptoms:")
    
    if st.button("Analyze Symptoms"):
        if symp_input:
            result = analyze_symptoms(symp_input)
            level = result['level']
            
            if level == "High":
                st.error(f"🚨 {result['warning']}")
            elif level == "Moderate":
                st.warning(f"⚠️ {result['warning']}")
            else:
                st.success(f"ℹ️ {result['warning']}")
                
            st.info(f"💡 **Advice:** {result['advice']}")
        else:
            st.error("Please enter your symptoms.")

# ----------------- TAB 4: Side Effect Monitor -----------------
with tab4:
    st.header("Side Effect Monitor")
    
    med_name = st.text_input("Medicine Taken:", placeholder="e.g., Paracetamol")
    se_symptoms = st.text_area("Experienced Symptoms:", placeholder="e.g., feeling nausea and slight chest pain")
    
    if st.button("Check Side Effects"):
        if med_name and se_symptoms:
            matched_med, score = fuzzy_match_medicine(med_name)
            if score > 80:
                st.write(f"Matched Medicine: **{matched_med}**")
                result = analyze_side_effects(matched_med, se_symptoms)
                
                if result['has_reaction']:
                    st.warning("⚠️ **Possible Side Effects Detected!**")
                    st.write("Matched symptoms:")
                    for m in result['matched_symptoms']:
                        st.write(f"- {m.title()}")
                    st.error(result['advice'])
                else:
                    st.success("✅ " + result['advice'])
            else:
                st.error("Could not recognize the medicine name.")
        else:
            st.error("Please fill out both fields.")

# ----------------- TAB 5: Emergency Risk Predictor -----------------
with tab5:
    st.header("Emergency Risk Predictor")
    
    col1, col2 = st.columns(2)
    with col1:
        age_input = st.number_input("Age:", min_value=1, max_value=120, value=30)
        risk_meds = st.text_input("Currently Taking (comma separated):", placeholder="e.g., Amoxicillin")
    with col2:
        risk_symptoms = st.text_area("Current Symptoms:", placeholder="e.g., vomiting, shortness of breath")
        
    if st.button("Calculate Risk Score"):
        med_list = [m.strip() for m in risk_meds.split(',')] if risk_meds else []
        
        # Determine side effect matches roughly if possible
        total_se_matches = 0
        if med_list and risk_symptoms:
            for m in med_list:
                mm, sc = fuzzy_match_medicine(m)
                if sc > 80:
                    se_res = analyze_side_effects(mm, risk_symptoms)
                    total_se_matches += len(se_res['matched_symptoms'])
                    
        risk_data = calculate_risk_score(age_input, risk_symptoms, med_list, total_se_matches)
        
        st.write("### Risk Assessment")
        
        score = risk_data['risk_score']
        level = risk_data['risk_level']
        
        if "Low" in level:
            st.metric(label="Risk Score", value=f"{score}%", delta="Low Risk", delta_color="normal")
        elif "Moderate" in level:
            st.metric(label="Risk Score", value=f"{score}%", delta="Moderate Risk", delta_color="off")
        else:
            st.metric(label="Risk Score", value=f"{score}%", delta="High Risk", delta_color="inverse")
            
        st.info(f"📋 **Recommendation:** {risk_data['recommendation']}")
