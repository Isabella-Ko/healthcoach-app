import streamlit as st
from simple_health_advisor import SimpleHealthAdvisor
from datetime import datetime, timedelta
import json

st.set_page_config(
    page_title="AI Health & Wellness Coach",
    page_icon="🏋️‍♀️",
    layout="wide"
)

# Custom CSS for better visualization
st.markdown("""
    <style>
    /* Google Colors */
    :root {
        --google-blue: #4285F4;
        --google-red: #EA4335;
        --google-yellow: #FBBC05;
        --google-green: #34A853;
        --google-gray: #5f6368;
        --google-light-gray: #f8f9fa;
        --google-white: #ffffff;
    }

    /* Global Styles */
    body {
        background-color: var(--google-white);
    }

    /* Sidebar Styling */
    .css-1d391kg {
        background-color: var(--google-light-gray);
    }
    
    .sidebar .sidebar-content {
        background-color: var(--google-light-gray);
    }

    /* Sidebar Headers */
    .sidebar h1, .sidebar h2, .sidebar h3 {
        color: var(--google-blue);
        font-weight: 500;
    }

    /* Sidebar Select Boxes */
    .stSelectbox, .stMultiselect {
        background-color: var(--google-white);
        border: 1px solid #e0e0e0;
        border-radius: 8px;
    }

    /* Sidebar Sliders */
    .stSlider {
        color: var(--google-blue);
    }

    /* Sidebar Buttons */
    .stButton button {
        background-color: var(--google-blue);
        color: var(--google-white);
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }

    .stButton button:hover {
        background-color: #3367d6;
    }

    /* Multi-select and Select Box Styling */
    .stMultiSelect [data-baseweb="select"] {
        background-color: var(--google-white);
        border-radius: 8px;
    }

    .stMultiSelect [data-baseweb="select"] span {
        color: var(--google-gray);
    }

    /* Slider Styling */
    .stSlider [data-baseweb="slider"] {
        color: var(--google-blue);
    }

    .stSlider [data-baseweb="slider"] [data-baseweb="thumb"] {
        background-color: var(--google-blue);
    }

    /* Agent Message Styling */
    .agent-message {
        padding: 20px;
        border-radius: 12px;
        margin: 15px 0;
        border: 1px solid #e0e0e0;
        background-color: var(--google-white);
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    .nutritionist { 
        background-color: #e8f0fe;
        border-left: 5px solid var(--google-blue);
    }
    .fitness { 
        background-color: #e6f4ea;
        border-left: 5px solid var(--google-green);
    }
    .mindfulness { 
        background-color: #fef7e0;
        border-left: 5px solid var(--google-yellow);
    }
    .coordinator { 
        background-color: #fce8e6;
        border-left: 5px solid var(--google-red);
    }
    .reporter { 
        background-color: #e8f0fe;
        border-left: 5px solid var(--google-blue);
    }
    .agent-header {
        display: flex;
        align-items: center;
        margin-bottom: 10px;
    }
    .agent-icon {
        font-size: 24px;
        margin-right: 10px;
    }
    .agent-name {
        font-size: 18px;
        font-weight: 500;
        color: var(--google-gray);
    }
    .agent-content {
        color: var(--google-gray);
        line-height: 1.5;
    }
    .interaction-arrow {
        text-align: center;
        color: var(--google-gray);
        margin: 5px 0;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        border-bottom: 1px solid #e0e0e0;
        background-color: var(--google-white);
    }

    .stTabs [data-baseweb="tab"] {
        color: var(--google-gray);
        padding: 0.5rem 1rem;
        font-weight: 500;
    }

    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: var(--google-blue);
        border-bottom: 2px solid var(--google-blue);
    }

    /* Main Content Area */
    .main .block-container {
        padding-top: 2rem;
        background-color: var(--google-white);
    }

    /* Info Box Styling */
    .stInfo {
        background-color: #e8f0fe;
        border: 1px solid var(--google-blue);
        border-radius: 8px;
    }

    /* Title Styling */
    h1 {
        color: var(--google-blue);
        font-weight: 500;
    }

    /* Override Streamlit's default colors */
    .stSelectbox [data-baseweb="select"] {
        background-color: var(--google-white);
    }

    .stSelectbox [data-baseweb="select"] span {
        color: var(--google-gray);
    }

    /* Override Streamlit's default slider colors */
    .stSlider [data-baseweb="slider"] [data-baseweb="track"] {
        background-color: #e0e0e0;
    }

    .stSlider [data-baseweb="slider"] [data-baseweb="track"][data-baseweb="selected"] {
        background-color: var(--google-blue);
    }

    /* Add styles for formatted output */
    .formatted-output {
        background-color: var(--google-white);
        border-radius: 8px;
        padding: 20px;
        margin: 10px 0;
        border: 1px solid #e0e0e0;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    
    .formatted-output h3 {
        color: var(--google-blue);
        margin-bottom: 15px;
    }
    
    .formatted-output ul {
        list-style-type: none;
        padding-left: 0;
    }
    
    .formatted-output li {
        margin: 10px 0;
        padding-left: 20px;
        position: relative;
    }
    
    .formatted-output li:before {
        content: "•";
        color: var(--google-blue);
        position: absolute;
        left: 0;
    }
    
    .formatted-output strong {
        color: var(--google-gray);
    }
    
    .formatted-output p {
        margin: 10px 0;
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

def display_agent_message(role, content, icon):
    """Display a message from an agent with custom styling"""
    st.markdown(f"""
        <div class="agent-message {role.lower().replace(' ', '')}">
            <div class="agent-header">
                <span class="agent-icon">{icon}</span>
                <span class="agent-name">{role}</span>
            </div>
            <div class="formatted-output">
                {content}
            </div>
        </div>
    """, unsafe_allow_html=True)

def display_interaction_arrow():
    """Display an arrow indicating agent interaction"""
    st.markdown("""
        <div class="interaction-arrow">
            ↓
        </div>
    """, unsafe_allow_html=True)

def main():
    st.title("🏋️‍♀️ AI Health & Wellness Coach")
    st.markdown("""
    This AI-powered health coach provides personalized wellness plans using advanced AI technology.
    Meet your team of experts:
    - 🥗 **Nutritionist**: Creates personalized meal plans
    - 💪 **Fitness Planner**: Designs effective workouts
    - 🧘‍♀️ **Mindfulness Guide**: Provides meditation and stress management
    - 📅 **Schedule Coordinator**: Integrates all activities
    - 📊 **Progress Reporter**: Tracks your journey
    """)

    # Sidebar for user input
    with st.sidebar:
        st.header("Your Profile")
        goals = st.multiselect(
            "Health Goals",
            ["Weight Loss", "Muscle Gain", "Stress Reduction", "Better Sleep", "More Energy"],
            default=["Weight Loss", "More Energy"]
        )
        
        diet = st.selectbox(
            "Dietary Preference",
            ["Balanced", "Vegetarian", "Vegan", "Keto", "Mediterranean"]
        )
        
        restrictions = st.multiselect(
            "Dietary Restrictions",
            ["No Nuts", "No Dairy", "No Gluten", "No Shellfish", "No Eggs"]
        )
        
        fitness_level = st.select_slider(
            "Fitness Level",
            options=["Beginner", "Intermediate", "Advanced"]
        )
        
        equipment = st.multiselect(
            "Available Equipment",
            ["Yoga Mat", "Resistance Bands", "Dumbbells", "Pull-up Bar", "None"]
        )
        
        mood = st.select_slider(
            "Current Stress Level",
            options=["Very Stressed", "Stressed", "Neutral", "Calm", "Very Calm"]
        )

    # Main content area
    if st.button("Generate My Health Plan"):
        with st.spinner("Your AI health team is working on your personalized plan..."):
            # Create user profile
            user_profile = {
                "goals": {goal.lower().replace(" ", "_"): True for goal in goals},
                "preferences": {
                    "diet": diet.lower(),
                    "exclude": [r.lower().replace(" ", "_") for r in restrictions]
                },
                "fitness_level": fitness_level.lower(),
                "available_equipment": equipment,
                "mood": mood.lower()
            }

            # Initialize the health advisor
            advisor = SimpleHealthAdvisor()

            # Create tabs for different stages
            tab1, tab2, tab3 = st.tabs(["Initial Planning", "Schedule Integration", "Weekly Report"])

            with tab1:
                st.header("Initial Planning Phase")
                st.info("Your specialists are creating their initial recommendations...")
                
                # Get meal plan
                with st.spinner("🥗 Nutritionist is creating your meal plan..."):
                    meal_plan = advisor.create_meal_plan(user_profile)
                
                display_agent_message("Nutritionist", meal_plan, "🥗")
                display_interaction_arrow()
                
                # Get workout plan
                with st.spinner("💪 Fitness Planner is designing your workout..."):
                    workout_plan = advisor.create_workout_plan(user_profile)
                
                display_agent_message("Fitness Planner", workout_plan, "💪")
                display_interaction_arrow()
                
                # Get mindfulness plan
                with st.spinner("🧘‍♀️ Mindfulness Guide is creating your meditation plan..."):
                    mindfulness_plan = advisor.create_mindfulness_plan(user_profile)
                
                display_agent_message("Mindfulness Guide", mindfulness_plan, "🧘‍♀️")
                display_interaction_arrow()
                
                # Get integrated schedule
                with st.spinner("📅 Schedule Coordinator is integrating all plans..."):
                    integrated_schedule = advisor.create_integrated_schedule(meal_plan, workout_plan, mindfulness_plan)
                
                display_agent_message("Schedule Coordinator", integrated_schedule, "📅")

            with tab2:
                st.header("Schedule Integration Phase")
                st.info("Your Schedule Coordinator is creating a cohesive daily schedule...")
                
                # Display the integrated schedule
                st.markdown("### Final Integrated Schedule")
                st.markdown(integrated_schedule)

            with tab3:
                st.header("Weekly Progress Report")
                st.info("Your Progress Reporter is analyzing your schedule and preparing recommendations...")
                
                # Simulate history
                history = [
                    {"date": (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")}
                    for i in range(7)
                ]

                # Get progress report
                with st.spinner("📊 Progress Reporter is generating your weekly report..."):
                    progress_report = advisor.create_progress_report(history, integrated_schedule)
                
                display_agent_message("Progress Reporter", progress_report, "📊")

if __name__ == "__main__":
    main() 