import sys
try:
    import pysqlite3
    sys.modules["sqlite3"] = pysqlite3
    sys.modules["sqlite3.dbapi2"] = pysqlite3.dbapi2
except ImportError:
    pass

import streamlit as st
from health_advisor import (
    NutritionistAgent, FitnessPlannerAgent, MindfulnessGuideAgent,
    ScheduleCoordinatorAgent, ProgressReporterAgent,
    create_meal_plan_task, create_workout_plan_task, create_mindfulness_plan_task,
    create_integrated_schedule_task, create_progress_report_task
)
from crewai import Crew, Process
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
    section[data-testid="stSidebar"] {
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

    /* Add styles for expandable sections */
    .expandable-section {
        margin: 10px 0;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        overflow: hidden;
    }
    
    .expandable-header {
        background-color: var(--google-light-gray);
        padding: 10px 15px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 1px solid #e0e0e0;
    }
    
    .expandable-header:hover {
        background-color: #f1f3f4;
    }
    
    .expandable-content {
        padding: 15px;
        background-color: var(--google-white);
    }
    
    .thought-process {
        font-style: italic;
        color: var(--google-gray);
        padding: 10px;
        background-color: #f8f9fa;
        border-radius: 4px;
        margin: 5px 0;
    }
    
    .thought-process strong {
        color: var(--google-blue);
    }
    
    /* Add styles for the expand/collapse icon */
    .expand-icon {
        transition: transform 0.3s ease;
    }
    
    .expanded .expand-icon {
        transform: rotate(180deg);
    }

    section[data-testid="stSidebar"] {
        background-color: var(--google-light-gray);
    }
    </style>
    """, unsafe_allow_html=True)

def format_agent_output(output):
    """Format the agent output for better readability"""
    if isinstance(output, str):
        try:
            output = json.loads(output)
        except:
            if "raw" in output:
                return output["raw"]
            return output
    
    if isinstance(output, dict):
        if "raw" in output:
            return output["raw"]
        if "tasks_output" in output:
            tasks = output["tasks_output"]
            if isinstance(tasks, list) and len(tasks) > 0:
                task = tasks[0]
                if hasattr(task, "raw"):
                    return task.raw
                if isinstance(task, dict) and "raw" in task:
                    return task["raw"]
        return json.dumps(output, indent=2)
    
    if isinstance(output, list):
        formatted = []
        for item in output:
            if hasattr(item, "raw"):
                formatted.append(item.raw)
            elif isinstance(item, dict) and "raw" in item:
                formatted.append(item["raw"])
            else:
                formatted.append(str(item))
        return "\n\n".join(formatted)
    
    return str(output)

def display_agent_message(role, content, icon, thought_process=None, chain_of_thought=None):
    """Display a message from an agent with custom styling, thought process, and chain-of-thought steps"""
    formatted_content = format_agent_output(content)
    expander_key = f"expander_{role}_{hash(formatted_content)}"
    st.markdown(f"""
        <div class="agent-message {role.lower()}">
            <div class="agent-header">
                <span class="agent-icon">{icon}</span>
                <span class="agent-name">{role}</span>
            </div>
            <div class="formatted-output">
                {formatted_content}
            </div>
        </div>
    """, unsafe_allow_html=True)
    if thought_process or chain_of_thought:
        with st.expander("🤔 View Thought Process", expanded=False):
            if thought_process:
                st.markdown(f"<div class='thought-process'>{thought_process}</div>", unsafe_allow_html=True)
            if chain_of_thought:
                for step in chain_of_thought:
                    if 'title' in step:
                        st.markdown(f"**{step['title']}**")
                    if 'text' in step:
                        st.markdown(step['text'])
                    if 'tool_input' in step:
                        st.markdown("**Tool Input:**")
                        st.code(step['tool_input'], language='json')
                    if 'tool_output' in step:
                        st.markdown("**Tool Output:**")
                        st.code(step['tool_output'], language='json')

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
    This AI-powered health coach combines the expertise of multiple specialists to create your personalized wellness plan.
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

            # Initialize agents
            nutritionist = NutritionistAgent()
            fitness_planner = FitnessPlannerAgent()
            mindfulness_guide = MindfulnessGuideAgent()
            coordinator = ScheduleCoordinatorAgent()
            progress_reporter = ProgressReporterAgent()

            # Create tabs for different stages
            tab1, tab2, tab3 = st.tabs(["Initial Planning", "Schedule Integration", "Weekly Report"])

            with tab1:
                st.header("Initial Planning Phase")
                st.info("Your specialists are discussing and creating their initial recommendations...")
                
                # Create and run the crew for initial planning
                planning_crew = Crew(
                    agents=[nutritionist, fitness_planner, mindfulness_guide],
                    tasks=[
                        create_meal_plan_task(nutritionist, user_profile),
                        create_workout_plan_task(fitness_planner, user_profile),
                        create_mindfulness_plan_task(mindfulness_guide, user_profile)
                    ],
                    verbose=True,
                    process=Process.sequential
                )

                initial_plans = planning_crew.kickoff()
                
                # Demo chain_of_thought for Nutritionist
                nutritionist_chain = [
                    {
                        "title": "# Agent: Nutritionist",
                        "text": "## Thought: I need to create a meal plan that supports the user's fitness goals and energy levels."
                    },
                    {
                        "title": "## Using tool: Ask question to coworker",
                        "tool_input": {
                            "question": "What time are the main workouts scheduled? This will help me optimize meal timing.",
                            "context": "I am planning meals for energy and recovery.",
                            "coworker": "Fitness Planner"
                        },
                        "tool_output": "Workouts are scheduled at 7am and 6pm."
                    },
                    {
                        "title": "## Using tool: Ask question to coworker",
                        "tool_input": {
                            "question": "Are there any mindfulness practices that require fasting or specific meal timing?",
                            "context": "I want to avoid meal-meditation conflicts.",
                            "coworker": "Mindfulness Guide"
                        },
                        "tool_output": "Morning meditation is best before breakfast."
                    }
                ]
                display_agent_message(
                    "Nutritionist",
                    "Here's my initial meal plan recommendation...",
                    "🥗",
                    "**Thought Process:** Analyzing user goals, dietary preferences, and collaborating with other agents to optimize meal timing.",
                    chain_of_thought=nutritionist_chain
                )
                display_interaction_arrow()
                # Demo chain_of_thought for Fitness Planner
                fitness_chain = [
                    {
                        "title": "# Agent: Fitness Planner",
                        "text": "## Thought: I need to design workouts that align with meal timing and energy levels."
                    },
                    {
                        "title": "## Using tool: Ask question to coworker",
                        "tool_input": {
                            "question": "What are the user's preferred workout times and available equipment?",
                            "context": "I want to tailor the workout plan.",
                            "coworker": "Schedule Coordinator"
                        },
                        "tool_output": "Preferred times: 7am, 6pm. Equipment: Yoga mat."
                    }
                ]
                display_agent_message(
                    "Fitness Planner",
                    "Here's my initial workout plan recommendation...",
                    "💪",
                    "**Thought Process:** Considering meal timing, user preferences, and collaborating with the team for optimal workout scheduling.",
                    chain_of_thought=fitness_chain
                )
                display_interaction_arrow()
                # Demo chain_of_thought for Mindfulness Guide
                mindfulness_chain = [
                    {
                        "title": "# Agent: Mindfulness Guide",
                        "text": "## Thought: I need to schedule mindfulness practices that complement meals and workouts."
                    },
                    {
                        "title": "## Using tool: Ask question to coworker",
                        "tool_input": {
                            "question": "Are there any high-stress periods in the user's day?",
                            "context": "I want to place meditation sessions for maximum benefit.",
                            "coworker": "Schedule Coordinator"
                        },
                        "tool_output": "User reports stress in the afternoon."
                    }
                ]
                display_agent_message(
                    "Mindfulness Guide",
                    "Here's my initial mindfulness plan recommendation...",
                    "🧘‍♀️",
                    "**Thought Process:** Reviewing user mood and collaborating with the team to optimize meditation timing.",
                    chain_of_thought=mindfulness_chain
                )
                display_interaction_arrow()
                # Demo chain_of_thought for Schedule Coordinator
                coordinator_chain = [
                    {
                        "title": "# Agent: Schedule Coordinator",
                        "text": "## Thought: I need to integrate all plans into a conflict-free daily schedule."
                    },
                    {
                        "title": "## Using tool: Ask question to coworker",
                        "tool_input": {
                            "question": "Any last-minute adjustments needed for your plans?",
                            "context": "I am finalizing the integrated schedule.",
                            "coworker": "All"
                        },
                        "tool_output": "No further changes."
                    }
                ]
                display_agent_message(
                    "Schedule Coordinator",
                    "Here's the integrated initial plan:",
                    "📅",
                    "**Thought Process:** Reviewing all plans and ensuring a harmonious daily flow.",
                    chain_of_thought=coordinator_chain
                )

            with tab2:
                st.header("Schedule Integration Phase")
                st.info("Your Schedule Coordinator is working with the team to create a cohesive daily schedule...")
                
                # Create and run the crew for schedule integration
                integration_crew = Crew(
                    agents=[coordinator, nutritionist, fitness_planner, mindfulness_guide],
                    tasks=[create_integrated_schedule_task(coordinator, initial_plans, initial_plans, initial_plans)],
                    verbose=True,
                    process=Process.sequential
                )

                integrated_schedule = integration_crew.kickoff()
                
                # Display integration process with thought processes
                display_agent_message(
                    "Schedule Coordinator",
                    "I've reviewed all plans. Let me create an integrated schedule...",
                    "📅",
                    "**Thought Process:** Creating a balanced daily schedule that optimizes energy levels and recovery time between activities."
                )
                display_interaction_arrow()
                
                display_agent_message(
                    "Nutritionist",
                    "I'll adjust meal timings to better support the workout schedule.",
                    "🥗",
                    "**Thought Process:** Fine-tuning meal timing to ensure optimal energy for workouts and proper recovery nutrition."
                )
                display_interaction_arrow()
                
                display_agent_message(
                    "Fitness Planner",
                    "I'll modify workout intensity based on meal timing.",
                    "💪",
                    "**Thought Process:** Adjusting workout intensity and duration to align with energy levels from meals."
                )
                display_interaction_arrow()
                
                display_agent_message(
                    "Mindfulness Guide",
                    "I'll add short meditation breaks between activities.",
                    "🧘‍♀️",
                    "**Thought Process:** Identifying natural transition points for mindfulness practices to enhance overall well-being."
                )
                display_interaction_arrow()
                
                # Demo chain_of_thought for Schedule Coordinator
                demo_chain_of_thought = [
                    {
                        "title": "# Agent: Schedule Coordinator",
                        "text": "## Thought: I need to gather insights from the Fitness Planner and Mindfulness Guide to finalize the optimized schedule without timing conflicts."
                    },
                    {
                        "title": "## Using tool: Ask question to coworker",
                        "tool_input": {
                            "question": "Can you review the current schedule and suggest any adjustments or improvements regarding workout timing and mindfulness practices to enhance overall daily efficiency and energy levels?",
                            "context": "The daily mindfulness program includes meal timings, workout sessions, meditation, and mindfulness practices. I'm working on creating a cohesive timetable that optimizes transitions between activities and considers energy levels throughout the day. I need your input on workout-related aspects.",
                            "coworker": "Fitness Planner"
                        },
                        "tool_output": "The Fitness Planner suggests moving the workout to 7am for better energy."
                    },
                    {
                        "title": "## Using tool: Ask question to coworker",
                        "tool_input": {
                            "question": "Can you review the current schedule and suggest any adjustments or improvements regarding mindfulness practices?",
                            "context": "The daily schedule includes meal timings, workout sessions, meditation, and mindfulness practices. I'm working on creating a cohesive timetable that optimizes transitions between activities and considers energy levels throughout the day. I need your input on mindfulness-related aspects.",
                            "coworker": "Mindfulness Guide"
                        },
                        "tool_output": "The Mindfulness Guide recommends a short meditation after lunch."
                    }
                ]
                display_agent_message(
                    "Schedule Coordinator",
                    "Here's your final integrated schedule:",
                    "📅",
                    "**Thought Process:** Finalizing the schedule with all adjustments and ensuring a harmonious flow of activities.",
                    chain_of_thought=demo_chain_of_thought
                )
                # Demo chain_of_thought for Nutritionist in integration
                nutritionist_integration_chain = [
                    {
                        "title": "# Agent: Nutritionist",
                        "text": "## Thought: I need to adjust meal timings to better support the new workout schedule."
                    },
                    {
                        "title": "## Using tool: Review schedule",
                        "tool_input": {
                            "schedule": "Integrated daily schedule with workouts at 7am and 6pm."
                        },
                        "tool_output": "Adjusted breakfast to 8am and dinner to 7pm for optimal recovery."
                    }
                ]
                display_agent_message(
                    "Nutritionist",
                    "I've updated meal timings to support the new schedule.",
                    "🥗",
                    "**Thought Process:** Fine-tuning meal timing for optimal energy and recovery.",
                    chain_of_thought=nutritionist_integration_chain
                )
                display_interaction_arrow()
                # Demo chain_of_thought for Fitness Planner in integration
                fitness_integration_chain = [
                    {
                        "title": "# Agent: Fitness Planner",
                        "text": "## Thought: I need to modify workout intensity based on the new meal timing."
                    },
                    {
                        "title": "## Using tool: Review meal plan",
                        "tool_input": {
                            "meal_plan": "Breakfast at 8am, dinner at 7pm."
                        },
                        "tool_output": "Scheduled high-intensity workouts after breakfast for best results."
                    }
                ]
                display_agent_message(
                    "Fitness Planner",
                    "I've modified workout intensity based on meal timing.",
                    "💪",
                    "**Thought Process:** Adjusting workout intensity and duration to align with energy levels from meals.",
                    chain_of_thought=fitness_integration_chain
                )
                display_interaction_arrow()
                # Demo chain_of_thought for Mindfulness Guide in integration
                mindfulness_integration_chain = [
                    {
                        "title": "# Agent: Mindfulness Guide",
                        "text": "## Thought: I need to add short meditation breaks between activities."
                    },
                    {
                        "title": "## Using tool: Review schedule",
                        "tool_input": {
                            "schedule": "Integrated daily schedule with meals and workouts."
                        },
                        "tool_output": "Added 10-minute meditation after lunch and before bed."
                    }
                ]
                display_agent_message(
                    "Mindfulness Guide",
                    "I've added short meditation breaks between activities.",
                    "🧘‍♀️",
                    "**Thought Process:** Identifying natural transition points for mindfulness practices.",
                    chain_of_thought=mindfulness_integration_chain
                )
                display_interaction_arrow()
                # Render the final integrated schedule as markdown at the end
                st.markdown(format_agent_output(integrated_schedule), unsafe_allow_html=True)

            with tab3:
                st.header("Weekly Progress Report")
                st.info("Your Progress Reporter is analyzing your schedule and preparing recommendations...")
                
                # Simulate history
                history = [
                    {"date": (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")}
                    for i in range(7)
                ]

                # Create and run the crew for weekly report
                weekly_crew = Crew(
                    agents=[progress_reporter, coordinator],
                    tasks=[create_progress_report_task(progress_reporter, history, integrated_schedule)],
                    verbose=True,
                    process=Process.sequential
                )

                weekly_report = weekly_crew.kickoff()
                
                # Display reporting process with thought processes
                display_agent_message(
                    "Progress Reporter",
                    "I'll analyze how well the integrated schedule is working...",
                    "📊",
                    "**Thought Process:** Evaluating schedule adherence and effectiveness, identifying patterns and areas for improvement."
                )
                display_interaction_arrow()
                
                display_agent_message(
                    "Schedule Coordinator",
                    "Let me provide some insights on schedule effectiveness...",
                    "📅",
                    "**Thought Process:** Analyzing the practical implementation of the schedule and identifying optimization opportunities."
                )
                display_interaction_arrow()
                
                display_agent_message(
                    "Progress Reporter",
                    "Here's your weekly progress report:",
                    "📊",
                    "**Thought Process:** Compiling insights and recommendations to support continued progress and motivation."
                )
                # Render the final weekly report as markdown at the end
                st.markdown(format_agent_output(weekly_report), unsafe_allow_html=True)

                # Demo chain_of_thought for Progress Reporter
                progress_reporter_chain = [
                    {
                        "title": "# Agent: Progress Reporter",
                        "text": "## Thought: I need to analyze how well the integrated schedule is working."
                    },
                    {
                        "title": "## Using tool: Review history",
                        "tool_input": {
                            "history": "User completed 90% of scheduled activities."
                        },
                        "tool_output": "User showed strong commitment and consistency."
                    },
                    {
                        "title": "## Using tool: Suggest improvements",
                        "tool_input": {
                            "analysis": "Some mindfulness sessions were missed in the afternoon."
                        },
                        "tool_output": "Recommend scheduling mindfulness earlier in the day."
                    }
                ]
                display_agent_message(
                    "Progress Reporter",
                    "Here's your weekly progress report:",
                    "📊",
                    "**Thought Process:** Compiling insights and recommendations to support continued progress and motivation.",
                    chain_of_thought=progress_reporter_chain
                )
                display_interaction_arrow()
                # Demo chain_of_thought for Schedule Coordinator in report
                coordinator_report_chain = [
                    {
                        "title": "# Agent: Schedule Coordinator",
                        "text": "## Thought: I need to provide insights on schedule effectiveness."
                    },
                    {
                        "title": "## Using tool: Review report",
                        "tool_input": {
                            "report": "Weekly progress report with recommendations."
                        },
                        "tool_output": "Schedule was effective, but flexibility is needed for mindfulness."
                    }
                ]
                display_agent_message(
                    "Schedule Coordinator",
                    "Here are my insights on schedule effectiveness.",
                    "📅",
                    "**Thought Process:** Analyzing the practical implementation of the schedule and identifying optimization opportunities.",
                    chain_of_thought=coordinator_report_chain
                )

if __name__ == "__main__":
    main() 