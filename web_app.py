import streamlit as st
import requests


FASTAPI_URL = "http://127.0.0.1:8000/generate-explanations"

# Streamlit UI
st.title("study aid system")
st.write("Select a topic ,subject and grade level to be explained.")

topic = st.text_input("Enter a topic:", "Laws of motion")
grade_level = st.number_input("Enter grade level:", min_value=1, max_value=12, value=5, step=1)
subject = st.text_input("Enter subject:", "Physics")
language = st.text_input("Enter language:", "English")
custom_prompt = st.text_area("Custom Prompt", "Provide an explanation for the topic Laws of motion in English language.")

if st.button("Provide Explanations"):
    # Send request to FastAPI
    payload = {"topic": topic, "grade_level": grade_level,"subject": subject,"language": language,"custom_prompt":custom_prompt} # make sure the payload mathces the pydantic model of the FastAPI
    response = requests.post(FASTAPI_URL, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        st.subheader("Explanation: ")
        
        # Process and display facts
        for prompt_gen in data["explanations"]:
            st.write(prompt_gen)
    else:
        st.error("Failed to generate facts. Please check the FastAPI server.")
