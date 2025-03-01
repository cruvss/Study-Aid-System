import streamlit as st
import pandas as pd

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
    
    class_options = ["Grade 11", "Grade 12"]
    selected_class = st.selectbox("Select Class", class_options)
    
    subject_options = ["Physics", "Chemistry", "Biology", "Mathematics"]
    selected_subject = st.selectbox("Select Subject", subject_options)
    
    topic_options = {
        "Physics": ["Laws of Motion", "Thermodynamics", "Optics", "Electrostatics", "Magnetism"],
        "Chemistry": ["Atomic Structure", "Chemical Bonding", "Equilibrium", "Organic Chemistry"],
        "Biology": ["Cell Structure", "Human Physiology", "Genetics", "Ecology"],
        "Mathematics": ["Calculus", "Algebra", "Trigonometry", "Statistics"]
    }
    
    selected_topic = st.selectbox("Select Topic", topic_options[selected_subject])
    
    st.header("Prompt Selection")
    
    neet_exam = st.checkbox("NEET Examination", value=True)
    simple_explanation = st.checkbox("Simple Explanation", value=True)
    curriculum_equations = st.checkbox("Curriculum Equations", value=True)
    real_life_examples = st.checkbox("Real-life Examples", value=True)
    practice_questions = st.checkbox("Practice Questions", value=True)
    past_neet_questions = st.checkbox("Past NEET Questions")
    custom_prompt = st.checkbox("Add Custom Prompt")
    
    if custom_prompt:
        custom_prompt_text = st.text_area("Enter custom prompt:", height=100)
    
    if st.button("Generate Content", type="primary"):
        st.session_state.generate_clicked = True

# Main content area
main_col = st.container()

with main_col:
    # Title area with Save PDF button
    col1, col2 = st.columns([5, 1])
    
    with col1:
        st.header(f"{selected_topic} - {selected_class} {selected_subject}")
    
    with col2:
        st.button("SAVE PDF")
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Explanation", "Equations", "Examples", "Questions"])
    
    # Content for each tab
    with tab1:
        if selected_subject == "Physics" and selected_topic == "Laws of Motion":
            st.subheader("Newton's Laws of Motion")
            
            st.write("Newton's Laws of Motion are three fundamental laws that describe the relationship between the motion of an object and the forces acting on it. These laws form the basis for classical mechanics.")
            
            st.subheader("First Law (Law of Inertia):")
            st.write("An object will remain at rest or in uniform motion in a straight line unless acted upon by an external force. This property of objects to resist changes in their state of motion is called inertia.")
            
            st.subheader("Second Law (F = ma):")
            st.write("The acceleration of an object is directly proportional to the net force acting on it and inversely proportional to its mass. Mathematically expressed as F = ma, where F is the net force, m is the mass, and a is the acceleration.")
            
            st.subheader("Third Law (Action-Reaction):")
            st.write("For every action, there is an equal and opposite reaction. When one object exerts a force on a second object, the second object exerts an equal and opposite force on the first.")
            
            st.write("These laws help us understand and predict the behavior of objects in everyday situations, from the motion of planets to the movement of vehicles and sports activities.")
            
            st.write("The principles established by Newton continue to be fundamental in solving mechanics problems in the NEET examination.")
        else:
            st.write(f"Explanation content for {selected_topic} in {selected_subject}")
    
    with tab2:
        if selected_subject == "Physics" and selected_topic == "Laws of Motion":
            st.subheader("Key Equations for Laws of Motion")
            
            st.write("Newton's Second Law:")
            st.latex("F = ma")
            
            st.write("Where:")
            st.write("- F is the net force (measured in Newtons, N)")
            st.write("- m is the mass of the object (measured in kilograms, kg)")
            st.write("- a is the acceleration (measured in meters per second squared, m/s²)")
            
            st.write("Weight of an object:")
            st.latex("W = mg")
            
            st.write("Where:")
            st.write("- W is the weight (measured in Newtons, N)")
            st.write("- m is the mass (measured in kilograms, kg)")
            st.write("- g is the acceleration due to gravity (approximately 9.8 m/s² near Earth's surface)")
            
            st.write("Friction force:")
            st.latex("F_f = \mu N")
            
            st.write("Where:")
            st.write("- F_f is the friction force (measured in Newtons, N)")
            st.write("- μ is the coefficient of friction (dimensionless)")
            st.write("- N is the normal force (measured in Newtons, N)")
        else:
            st.write(f"Equations content for {selected_topic} in {selected_subject}")
    
    with tab3:
        if selected_subject == "Physics" and selected_topic == "Laws of Motion":
            st.subheader("Real-life Examples of Newton's Laws")
            
            st.write("First Law Examples:")
            st.write("1. **Seat Belts**: When a car suddenly stops, passengers continue moving forward due to inertia. Seat belts prevent this motion.")
            st.write("2. **Tablecloth Trick**: Quickly pulling a tablecloth from under dishes works because the dishes have inertia and resist the sudden change in motion.")
            
            st.write("Second Law Examples:")
            st.write("1. **Rocket Propulsion**: Rockets accelerate by expelling gas in the opposite direction, demonstrating F = ma.")
            st.write("2. **Elevator Motion**: The feeling of heaviness when an elevator accelerates upward or lightness when it accelerates downward.")
            
            st.write("Third Law Examples:")
            st.write("1. **Walking**: We push backward on the ground, and the ground pushes forward on us with equal force.")
            st.write("2. **Recoil of a Gun**: When a gun fires a bullet forward, the gun recoils backward with equal momentum.")
            
            st.write("These examples are commonly tested in NEET examinations to assess understanding of how the laws apply in practical situations.")
        else:
            st.write(f"Examples content for {selected_topic} in {selected_subject}")
    
    with tab4:
        if selected_subject == "Physics" and selected_topic == "Laws of Motion":
            st.subheader("Practice Questions")
            
            st.write("Multiple Choice Questions:")
            
            st.write("1. A body of mass 5 kg is acted upon by a force that gives it an acceleration of 2 m/s². What is the magnitude of the force?")
            st.write("   - A) 2.5 N")
            st.write("   - B) 5 N")
            st.write("   - C) 10 N")
            st.write("   - D) 20 N")
            
            st.write("2. According to Newton's third law, the action and reaction forces:")
            st.write("   - A) Act on the same body")
            st.write("   - B) Act on different bodies")
            st.write("   - C) Always produce acceleration")
            st.write("   - D) Can sometimes cancel each other out")
            
            st.write("3. A book is at rest on a table. Which of Newton's laws best explains why the book doesn't fall through the table?")
            st.write("   - A) First law only")
            st.write("   - B) Second law only")
            st.write("   - C) Third law only")
            st.write("   - D) Both first and third laws")
            
            st.write("4. An object of mass 2 kg moving with a velocity of 10 m/s collides with a wall and rebounds with the same speed. If the collision lasts for 0.1 seconds, the average force exerted by the wall on the object is:")
            st.write("   - A) 200 N")
            st.write("   - B) 400 N")
            st.write("   - C) 20 N")
            st.write("   - D) 40 N")
            
            st.write("*Answers: 1-C, 2-B, 3-D, 4-B*")
        else:
            st.write(f"Questions content for {selected_topic} in {selected_subject}")
    
    # Footer
    st.caption("Generated by Meta AI • Processing time: 2.3 seconds")