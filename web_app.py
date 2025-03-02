import streamlit as st
import requests
import time

FASTAPI_URL = "http://127.0.0.1:8000/generate-explanations"

# Set page configuration
st.set_page_config(
    page_title="Study Aid System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Header
st.title("NEET Study Aid System")

# Initialize session state for dynamic prompt boxes and explanations
if 'prompt_boxes' not in st.session_state:
    st.session_state.prompt_boxes = [
        {"key": "neet_focus", "placeholder": "Explain the topic with NEET exam focus..."},
        {"key": "simple_explanation", "placeholder": "Include simple explanation..."}
    ]

if 'explanations' not in st.session_state:
    st.session_state.explanations = []  # Store initial and edited explanations here

if 'combined_prompt' not in st.session_state:
    st.session_state.combined_prompt = []  # Store the combined prompts

if 'display_explanations' not in st.session_state:
    st.session_state.display_explanations = False  # Track whether to display explanations
    
    

# Function to generate and display explanations
def generate_and_display_explanations(prompts, selected_topic, selected_class, selected_subject, selected_language):
    
    # Combine all prompts
    combined_prompt = [prompt for prompt in prompts.values() if prompt.strip()]
    
    # Store the combined prompts in session state
    st.session_state.combined_prompt = combined_prompt
    
    # Only generate new explanations if there are no explanations yet
    if not st.session_state.explanations:
        start_time = time.time()
        payload = {
            "topic": selected_topic,
            "grade_level": selected_class,
            "subject": selected_subject,
            "language": selected_language,
            "custom_prompt": combined_prompt
        }
        
        response = requests.post(FASTAPI_URL, json=payload)
        end_time = time.time()
        st.write(f"Time taken to generate response: {end_time - start_time:.2f} seconds")
        
        if response.status_code == 200:
            data = response.json()
            explanations = data.get("explanations", [])
            if explanations:
                st.session_state.explanations = explanations  # Store initial explanations
            else:
                st.warning("No explanations were generated.")
        else:
            st.error("Failed to generate explanations. Please check the FastAPI server.")
    
    # Display tabs with editable explanations
    if st.session_state.explanations:
        # Use the prompts as tab labels, or use default labels if no prompts for proper error hanling
        if len(st.session_state.combined_prompt) >= len(st.session_state.explanations): # this will be true and run if the number of prompts is greater than or equal to the number of explanations
            tab_labels = [st.session_state.combined_prompt[i] if i < len(st.session_state.combined_prompt) and st.session_state.combined_prompt[i] 
                          else f"Explanation {i+1}" for i in range(len(st.session_state.explanations))]
     

            
        else: # now if fewer prompts than explanations, then use default labels
            tab_labels = [f"Explanation {i+1}" for i in range(len(st.session_state.explanations))]
        
        # Create tabs with the appropriate labels
        tabs = st.tabs(tab_labels)
        
        for i, (tab, explanation) in enumerate(zip(tabs, st.session_state.explanations)):
            with tab:
                # Use a unique key for each text_area based on the index and topic
                explanation_key = f"explanation_{selected_topic}_{i}"
                if explanation_key not in st.session_state:
                    st.session_state[explanation_key] = explanation
                
                # Allow editing and persist changes in session state
                edited_explanation = st.text_area(
                    label="",
                    value=st.session_state[explanation_key],
                    height=400,
                    key=f"edit_{selected_topic}_{i}"
                )
                
                # Update session state when the user edits
                if edited_explanation != st.session_state[explanation_key]:
                    st.session_state[explanation_key] = edited_explanation
                    st.session_state.explanations[i] = edited_explanation  # Update the explanations list

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
    
    # Function to add a new prompt box
    def add_prompt_box():
        new_key = f"custom_prompt_{len(st.session_state.prompt_boxes)}"
        st.session_state.prompt_boxes.append(
            {"key": new_key, "placeholder": "Enter additional requirement..."}
        )
    
    # Display all prompt boxes with headers
    prompts = {}
    for i, prompt_box in enumerate(st.session_state.prompt_boxes):
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
    
    # Button to generate content
    if st.button("Generate Content", type="primary"):
        # Clear previous explanations when generating new content
        st.session_state.explanations = []
        # Reset explanation-specific session states
        for key in list(st.session_state.keys()):
            if key.startswith("explanation_"):
                del st.session_state[key]
        st.session_state.generate_clicked = True

# Main view - only call generate_and_display_explanations once
if st.session_state.get("generate_clicked", False):
    generate_and_display_explanations(prompts, selected_topic, selected_class, selected_subject, selected_language)
    # After generating, set the flag to false and enable display
    st.session_state.generate_clicked = False
    st.session_state.display_explanations = True
    
elif st.session_state.get("display_explanations", False):
    # Only display existing explanations without regenerating
    generate_and_display_explanations({}, selected_topic, selected_class, selected_subject, selected_language)