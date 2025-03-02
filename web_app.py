import streamlit as st
import requests
import time 

FASTAPI_URL = "http://127.0.0.1:8000/generate-explanations"

# Set page configuration
st.set_page_config(
    page_title="NEET Study Aid System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Header
st.title("NEET Study Aid System")

# Initialize session state for dynamic prompt boxes 
# The initial state includes two prompt boxes: one for NEET-focused explanations and another for simple explanations. Change this as requrired
# to make it flexible We have added placeholder text for each prompt box
if 'prompt_boxes' not in st.session_state:
    st.session_state.prompt_boxes = [
        {"key": "neet_focus", "placeholder": "Explain the topic with NEET exam focus..."},
        {"key": "simple_explanation", "placeholder": "Include simple explanation..."}
    ]

# Function to generate and display explanations
def generate_and_display_explanations(prompts, selected_topic, selected_class, selected_subject, selected_language):
    # Combine all prompts
    combined_prompt = [prompt for prompt in prompts.values() if prompt.strip()]
    st.write("Combined Prompts:", combined_prompt) #remove this line after testing prupose
    
    # Send request to FastAPI
    payload = {
        "topic": selected_topic,
        "grade_level": selected_class,
        "subject": selected_subject,
        "language": selected_language,
        "custom_prompt": combined_prompt
    }
    
    # checking time taken to generate response
    start_time = time.time()
    response = requests.post(FASTAPI_URL, json=payload)
    end_time = time.time()
    st.write(f"Time taken to generate response: {end_time - start_time:.2f} seconds")
    
    if response.status_code == 200:
        data = response.json()
        explanations = data.get("explanations", [])
        topics = combined_prompt #for that tab name in the UI
        
        if explanations:
            tabs = st.tabs([f"{topics[i]}" for i in range(len(topics))])
            for tab, explanation in zip(tabs, explanations):
                with tab:
                    st.write(explanation)
        else:
            st.warning("No explanations were generated.")
    else:
        st.error("Failed to generate explanations. Please check the FastAPI server.")

# Sidebar
with st.sidebar: #this contains all side bar content
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
    
    # Function to add a new prompt box
    def add_prompt_box():
        new_key = f"custom_prompt_{len(st.session_state.prompt_boxes)}"
        st.session_state.prompt_boxes.append(
            {"key": new_key, "placeholder": "Enter additional requirement..."}
        )
    
    # Display all prompt boxes with headers
    prompts = {}
    for i, prompt_box in enumerate(st.session_state.prompt_boxes):
        # Add a header for each prompt box
        if i == 0:
            st.subheader("Prompt 1")
        elif i == 1:
            st.subheader("Prompt 2")
        else:
            st.subheader(f"Prompt {i+1}")
            
        prompts[prompt_box["key"]] = st.text_area(
            label="",
            placeholder=prompt_box["placeholder"],
            key=prompt_box["key"],
            height=80
        )
    
    # Button to add more prompt boxes
    if st.button("Add More Requirements"):
        add_prompt_box()
        #st.rerun()
    
    # Button to generate content
    if st.button("Generate Content", type="primary"):
        st.session_state.generate_clicked = True

# Main view
if st.session_state.get("generate_clicked", False):
    generate_and_display_explanations(prompts, selected_topic, selected_class, selected_subject, selected_language)
    st.session_state.generate_clicked = False
    
    
# If the "Generate Content" button is clicked from the side bar 
#  then generate_and_display_explanations function is called with the selected inputs and prompts
