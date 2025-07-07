from crewai import Agent, Task, Crew, Process
from langchain.tools import tool
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class HealthCoach:
    def __init__(self):
        # Initialize agents
        self.nutritionist = Agent(
            role='Nutritionist',
            goal='Create personalized meal plans that align with user health goals',
            backstory="""You are an experienced nutritionist with expertise in creating 
            balanced, healthy meal plans. You understand different dietary needs and 
            can adapt recommendations based on user preferences and restrictions.""",
            verbose=True
        )

        self.fitness_planner = Agent(
            role='Fitness Planner',
            goal='Design effective workouts that can be done with minimal equipment',
            backstory="""You are a certified fitness trainer specializing in home workouts 
            and bodyweight exercises. You create safe, effective workout routines that 
            can be performed anywhere.""",
            verbose=True
        )

        self.mindfulness_guide = Agent(
            role='Mindfulness Guide',
            goal='Provide meditation and stress management techniques',
            backstory="""You are a mindfulness expert with years of experience in 
            meditation and stress management. You help people develop healthy mental 
            habits and coping strategies.""",
            verbose=True
        )

        self.progress_reporter = Agent(
            role='Progress Reporter',
            goal='Track and report on user progress while providing motivation',
            backstory="""You are a health coach who specializes in tracking progress 
            and providing motivational support. You help users stay accountable and 
            celebrate their achievements.""",
            verbose=True
        )

    def create_meal_plan(self, user_goals, dietary_restrictions):
        task = Task(
            description=f"""Create a personalized meal plan based on the following:
            Goals: {user_goals}
            Dietary Restrictions: {dietary_restrictions}
            Include breakfast, lunch, dinner, and snacks.
            Provide nutritional information and portion sizes.""",
            agent=self.nutritionist,
            expected_output="""A detailed meal plan including:
            1. Daily meal schedule
            2. Specific food items and portions
            3. Nutritional information
            4. Preparation instructions"""
        )
        return task

    def create_workout_plan(self, fitness_level, available_equipment):
        task = Task(
            description=f"""Design a workout plan considering:
            Fitness Level: {fitness_level}
            Available Equipment: {available_equipment}
            Include warm-up, main exercises, and cool-down.
            Provide detailed instructions and modifications.""",
            agent=self.fitness_planner,
            expected_output="""A comprehensive workout plan including:
            1. Warm-up routine
            2. Main exercises with sets and reps
            3. Cool-down exercises
            4. Modifications for different fitness levels"""
        )
        return task

    def create_mindfulness_plan(self, stress_level, time_availability):
        task = Task(
            description=f"""Create a mindfulness plan based on:
            Current Stress Level: {stress_level}
            Available Time: {time_availability}
            Include meditation techniques, breathing exercises, and stress management tips.""",
            agent=self.mindfulness_guide,
            expected_output="""A mindfulness program including:
            1. Meditation techniques
            2. Breathing exercises
            3. Stress management strategies
            4. Daily practice schedule"""
        )
        return task

    def generate_progress_report(self, weekly_activities, achievements):
        task = Task(
            description=f"""Generate a weekly progress report including:
            Activities Completed: {weekly_activities}
            Achievements: {achievements}
            Provide motivation and suggestions for improvement.""",
            agent=self.progress_reporter,
            expected_output="""A detailed progress report including:
            1. Weekly achievements summary
            2. Progress analysis
            3. Motivational message
            4. Recommendations for improvement"""
        )
        return task

    def run_health_coach(self, user_profile):
        # Create tasks based on user profile
        tasks = [
            self.create_meal_plan(user_profile['goals'], user_profile['dietary_restrictions']),
            self.create_workout_plan(user_profile['fitness_level'], user_profile['equipment']),
            self.create_mindfulness_plan(user_profile['stress_level'], user_profile['time_availability']),
            self.generate_progress_report(user_profile['weekly_activities'], user_profile['achievements'])
        ]

        # Create and run the crew
        crew = Crew(
            agents=[self.nutritionist, self.fitness_planner, self.mindfulness_guide, self.progress_reporter],
            tasks=tasks,
            verbose=True,
            process=Process.sequential
        )

        result = crew.kickoff()
        return result

def main():
    # Example user profile
    user_profile = {
        'goals': 'Weight loss and improved energy levels',
        'dietary_restrictions': 'Vegetarian, no nuts',
        'fitness_level': 'Beginner',
        'equipment': 'Yoga mat, resistance bands',
        'stress_level': 'Moderate',
        'time_availability': '30 minutes daily',
        'weekly_activities': '3 workouts, 2 meditation sessions',
        'achievements': 'Completed all planned workouts'
    }

    coach = HealthCoach()
    result = coach.run_health_coach(user_profile)
    print("\nHealth Coach Recommendations:")
    print(result)

if __name__ == "__main__":
    main() 