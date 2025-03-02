import streamlit as st
import requests

FASTAPI_URL = "http://127.0.0.1:8000/generate-explanations"

# Set page configuration
st.set_page_config(
    page_title="NEET Study Aid System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Header
st.title("NEET Study Aid System")

# Sidebar
with st.sidebar:
    st.header("Class & Subject")
    selected_class = st.number_input("Enter grade level:", min_value=1, max_value=12, value=5, step=1)
    subject_options = ["Physics", "Chemistry", "Biology", "Mathematics"]
    selected_subject = st.selectbox("Select Subject", subject_options)
    language_options = ["English", "Hindi"]
    selected_language = st.selectbox("Select Language", language_options)
    
    topic_options = {
        "Physics": ["Laws of Motion", "Thermodynamics", "Optics", "Electrostatics", "Magnetism"],
        "Chemistry": ["Atomic Structure", "Chemical Bonding", "Equilibrium", "Organic Chemistry"],
        "Biology": ["Cell Structure", "Human Physiology", "Genetics", "Ecology"],
        "Mathematics": ["Calculus", "Algebra", "Trigonometry", "Statistics"]
    }
    
    selected_topic = st.selectbox("Select Topic", topic_options[selected_subject])
    
    st.header("Prompt Selection")
    neet_exam = st.checkbox(st.text_area("Prompt 1:", height=68), value=True)
    simple_explanation = st.checkbox("Simple Explanation", value=True)
    curriculum_equations = st.checkbox("Curriculum Equations", value=True)
    real_life_examples = st.checkbox("Real-life Examples", value=True)
    practice_questions = st.checkbox("Practice Questions", value=True)
    past_neet_questions = st.checkbox("Past NEET Questions")
    custom_prompt = st.checkbox("Add Custom Prompt")
    
    custom_prompt_text = ""
    if custom_prompt:
        custom_prompt_text = st.text_area("Enter custom prompt:", height=68)
    
    if st.button("Generate Content", type="primary"):
        st.session_state.generate_clicked = True

if st.button("Provide Explanations"):
    # Send request to FastAPI
    payload = {
        "topic": selected_topic,
        "grade_level": selected_class,
        "subject": selected_subject,
        "language": selected_language,
        "custom_prompt": custom_prompt_text
    }
    response = requests.post(FASTAPI_URL, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        explanations = data.get("explanations", [])
        
        if explanations:
            if "edited_explanations" not in st.session_state:
                st.session_state.edited_explanations = explanations  # Store in session state

            tabs = st.tabs([f"Explanation {i+1}" for i in range(len(explanations))])
            for i, (tab, explanation) in enumerate(zip(tabs, explanations)):
                with tab:
                    st.session_state.edited_explanations[i] = st.text_area(
                        f"Edit Explanation {i+1}", 
                        value=st.session_state.edited_explanations[i], 
                        height=200
                    )

            if st.button("Save Changes"):
                st.success("Explanations saved successfully!")

        else:
            st.warning("No explanations were generated.")
    else:
        st.error("Failed to generate explanations. Please check the FastAPI server.")
