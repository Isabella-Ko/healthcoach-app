from crewai import Agent, Task, Crew, Process
from datetime import datetime, timedelta
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

# Create a shared LLM instance for all agents
llm = ChatOpenAI(model="gpt-4o", temperature=0.7)

# -- Agent Definitions --

class NutritionistAgent(Agent):
    """
    Suggests daily meal plans based on user goals and collaborates with other agents.
    """
    def __init__(self, llm=llm):
        super().__init__(
            role='Nutritionist',
            goal='Create personalized meal plans that align with user health goals and complement workout schedules',
            backstory="""You are an experienced nutritionist with expertise in creating 
            balanced, healthy meal plans. You understand how nutrition affects workout 
            performance and recovery. You collaborate with fitness trainers to ensure 
            meal timing aligns with exercise schedules.""",
            verbose=True,
            allow_delegation=True,
            llm=llm
        )

class FitnessPlannerAgent(Agent):
    """
    Crafts workouts and collaborates with nutritionist for optimal timing.
    """
    def __init__(self, llm=llm):
        super().__init__(
            role='Fitness Planner',
            goal='Design effective workouts that complement meal timing and energy levels',
            backstory="""You are a certified fitness trainer specializing in home workouts 
            and bodyweight exercises. You understand the importance of proper nutrition 
            timing and work closely with nutritionists to optimize workout schedules.""",
            verbose=True,
            allow_delegation=True,
            llm=llm
        )

class MindfulnessGuideAgent(Agent):
    """
    Offers meditation and stress management, coordinating with other activities.
    """
    def __init__(self, llm=llm):
        super().__init__(
            role='Mindfulness Guide',
            goal='Provide meditation and stress management techniques that complement daily activities',
            backstory="""You are a mindfulness expert who understands how meditation 
            and stress management can enhance workout performance and eating habits. 
            You coordinate with other specialists to find optimal times for practice.""",
            verbose=True,
            allow_delegation=True,
            llm=llm
        )

class ScheduleCoordinatorAgent(Agent):
    """
    Coordinates and integrates all activities into a cohesive daily schedule.
    """
    def __init__(self, llm=llm):
        super().__init__(
            role='Schedule Coordinator',
            goal='Create a balanced daily schedule that optimizes all health activities',
            backstory="""You are an expert in time management and health optimization. 
            You take inputs from nutritionists, fitness trainers, and mindfulness guides 
            to create a harmonious daily schedule that maximizes the benefits of each activity.""",
            verbose=True,
            allow_delegation=True,
            llm=llm
        )

class ProgressReporterAgent(Agent):
    """
    Generates a weekly health recap and motivational note.
    """
    def __init__(self, llm=llm):
        super().__init__(
            role='Progress Reporter',
            goal='Track and report on user progress while providing motivation',
            backstory="""You are a health coach who specializes in tracking progress 
            and providing motivational support. You analyze the effectiveness of the 
            integrated schedule and suggest improvements.""",
            verbose=True,
            allow_delegation=True,
            llm=llm
        )

# -- Task Definitions --

def create_meal_plan_task(nutritionist, user_input):
    return Task(
        description=f"""Create a personalized meal plan based on the following:
        Goals: {user_input['goals']}
        Preferences: {user_input['preferences']}
        
        Consider:
        1. Optimal timing for pre and post-workout nutrition
        2. Energy levels throughout the day
        3. How meals might affect meditation practice
        
        Collaborate with the Fitness Planner and Mindfulness Guide to ensure your meal 
        timing complements their recommendations.
        
        When delegating or asking a coworker, always provide the task and context as plain strings, not as dictionaries or JSON.
        
        Include breakfast, lunch, dinner, and snacks.
        Provide nutritional information and portion sizes.""",
        agent=nutritionist,
        expected_output="""A detailed meal plan including:
        1. Daily meal schedule with specific times
        2. Specific food items and portions
        3. Nutritional information
        4. Preparation instructions
        5. Notes on how it complements workouts and meditation"""
    )

def create_workout_plan_task(fitness_planner, user_input):
    return Task(
        description=f"""Design a workout plan considering:
        Fitness Level: {user_input['fitness_level']}
        Available Equipment: {user_input['available_equipment']}
        
        Consider:
        1. How the workout timing affects meal schedules
        2. Energy levels needed for meditation
        3. Recovery time needed between activities
        
        Collaborate with the Nutritionist and Mindfulness Guide to ensure your workout 
        schedule complements their recommendations.
        
        When delegating or asking a coworker, always provide the task and context as plain strings, not as dictionaries or JSON.
        
        Include warm-up, main exercises, and cool-down.
        Provide detailed instructions and modifications.""",
        agent=fitness_planner,
        expected_output="""A comprehensive workout plan including:
        1. Workout schedule with specific times
        2. Warm-up routine
        3. Main exercises with sets and reps
        4. Cool-down exercises
        5. Modifications for different fitness levels
        6. Notes on how it complements meals and meditation"""
    )

def create_mindfulness_plan_task(mindfulness_guide, user_input):
    return Task(
        description=f"""Create a mindfulness plan based on:
        Current Mood: {user_input['mood']}
        
        Consider:
        1. Best times for meditation relative to meals
        2. How meditation can enhance workout performance
        3. Stress management throughout the day
        
        Collaborate with the Nutritionist and Fitness Planner to ensure your meditation 
        schedule complements their recommendations.
        
        When delegating or asking a coworker, always provide the task and context as plain strings, not as dictionaries or JSON.
        
        Include meditation techniques, breathing exercises, and stress management tips.""",
        agent=mindfulness_guide,
        expected_output="""A mindfulness program including:
        1. Meditation schedule with specific times
        2. Meditation techniques
        3. Breathing exercises
        4. Stress management strategies
        5. Notes on how it complements meals and workouts"""
    )

def create_integrated_schedule_task(coordinator, meal_plan, workout_plan, mindfulness_plan):
    return Task(
        description=f"""Create an integrated daily schedule using the following inputs:
        
        Meal Plan: {meal_plan}
        Workout Plan: {workout_plan}
        Mindfulness Plan: {mindfulness_plan}
        
        Your task is to:
        1. Review all plans and identify any timing conflicts
        2. Suggest adjustments to optimize the schedule
        3. Create a cohesive daily timetable
        4. Ensure proper spacing between activities
        5. Consider energy levels throughout the day
        
        Collaborate with all specialists to refine the schedule.
        
        When delegating or asking a coworker, always provide the task and context as plain strings, not as dictionaries or JSON.""",
        agent=coordinator,
        expected_output="""An integrated daily schedule including:
        1. Hour-by-hour timetable
        2. Activity transitions and preparation time
        3. Energy level considerations
        4. Notes on activity relationships
        5. Recommendations for schedule optimization"""
    )

def create_progress_report_task(progress_reporter, history, integrated_schedule):
    return Task(
        description=f"""Generate a weekly progress report based on:
        History: {history}
        Current Schedule: {integrated_schedule}
        
        Analyze:
        1. How well the integrated schedule is working
        2. Areas for improvement
        3. Success metrics
        
        Provide motivation and suggestions for improvement.
        
        When delegating or asking a coworker, always provide the task and context as plain strings, not as dictionaries or JSON.""",
        agent=progress_reporter,
        expected_output="""A detailed progress report including:
        1. Weekly achievements summary
        2. Schedule effectiveness analysis
        3. Recommendations for optimization
        4. Motivational message
        5. Next week's goals"""
    )

def run_health_coach(user_profile):
    try:
        # Initialize agents
        nutritionist = NutritionistAgent(llm=llm)
        fitness_planner = FitnessPlannerAgent(llm=llm)
        mindfulness_guide = MindfulnessGuideAgent(llm=llm)
        coordinator = ScheduleCoordinatorAgent(llm=llm)
        progress_reporter = ProgressReporterAgent(llm=llm)

        # Create initial planning tasks
        meal_task = create_meal_plan_task(nutritionist, user_profile)
        workout_task = create_workout_plan_task(fitness_planner, user_profile)
        mindfulness_task = create_mindfulness_plan_task(mindfulness_guide, user_profile)

        # Create and run the crew for initial planning
        planning_crew = Crew(
            agents=[nutritionist, fitness_planner, mindfulness_guide],
            tasks=[meal_task, workout_task, mindfulness_task],
            verbose=True,
            process=Process.sequential
        )

        # Get initial plans
        initial_plans = planning_crew.kickoff()
        print("\n--- Initial Plans ---")
        print(initial_plans)

        # Create and run the crew for schedule integration
        integration_crew = Crew(
            agents=[coordinator, nutritionist, fitness_planner, mindfulness_guide],
            tasks=[create_integrated_schedule_task(coordinator, initial_plans, initial_plans, initial_plans)],
            verbose=True,
            process=Process.sequential
        )

        # Get integrated schedule
        integrated_schedule = integration_crew.kickoff()
        print("\n--- Integrated Schedule ---")
        print(integrated_schedule)

        # Simulate storing daily outputs
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

        # Get weekly report
        weekly_report = weekly_crew.kickoff()
        print("\n--- Weekly Report ---")
        print(weekly_report)

    except Exception as e:
        print(f"Error in workflow: {str(e)}")
        raise

if __name__ == "__main__":
    # Validate required fields in user profile
    required_fields = ["goals", "preferences", "fitness_level", "available_equipment", "mood"]
    user_profile = {
        "goals": {"lose_weight": True, "gain_muscle": False},
        "preferences": {"diet": "balanced", "exclude": ["nuts"]},
        "fitness_level": "beginner",
        "available_equipment": ["yoga mat"],
        "mood": "stressed"
    }
    
    # Check if all required fields are present
    missing_fields = [field for field in required_fields if field not in user_profile]
    if missing_fields:
        raise ValueError(f"Missing required fields in user profile: {missing_fields}")
    
    run_health_coach(user_profile)
