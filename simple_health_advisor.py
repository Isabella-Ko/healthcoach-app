import openai
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class SimpleHealthAdvisor:
    """Simplified health advisor that doesn't use CrewAI"""
    
    def __init__(self):
        self.client = client
    
    def create_meal_plan(self, user_profile):
        """Create a personalized meal plan"""
        prompt = f"""
        As a nutritionist, create a personalized meal plan based on:
        
        User Goals: {user_profile['goals']}
        Dietary Preferences: {user_profile['preferences']['diet']}
        Restrictions: {user_profile['preferences']['exclude']}
        Fitness Level: {user_profile['fitness_level']}
        
        Provide:
        1. Daily meal schedule with specific times
        2. Specific food items and portions
        3. Nutritional information
        4. Preparation instructions
        5. Notes on how it complements workouts and meditation
        
        Format the response in a clear, structured way.
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    def create_workout_plan(self, user_profile):
        """Create a personalized workout plan"""
        prompt = f"""
        As a fitness trainer, design a workout plan considering:
        
        Fitness Level: {user_profile['fitness_level']}
        Available Equipment: {user_profile['available_equipment']}
        
        Consider:
        1. How the workout timing affects meal schedules
        2. Energy levels needed for meditation
        3. Recovery time needed between activities
        
        Provide:
        1. Workout schedule with specific times
        2. Warm-up routine
        3. Main exercises with sets and reps
        4. Cool-down exercises
        5. Modifications for different fitness levels
        6. Notes on how it complements meals and meditation
        
        Format the response in a clear, structured way.
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    def create_mindfulness_plan(self, user_profile):
        """Create a mindfulness plan"""
        prompt = f"""
        As a mindfulness expert, create a mindfulness plan based on:
        
        Current Mood: {user_profile['mood']}
        
        Consider:
        1. Best times for meditation relative to meals
        2. How meditation can enhance workout performance
        3. Stress management throughout the day
        
        Provide:
        1. Meditation schedule with specific times
        2. Meditation techniques
        3. Breathing exercises
        4. Stress management strategies
        5. Notes on how it complements meals and workouts
        
        Format the response in a clear, structured way.
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    def create_integrated_schedule(self, meal_plan, workout_plan, mindfulness_plan):
        """Create an integrated daily schedule"""
        prompt = f"""
        As a schedule coordinator, create an integrated daily schedule using:
        
        Meal Plan: {meal_plan}
        Workout Plan: {workout_plan}
        Mindfulness Plan: {mindfulness_plan}
        
        Your task is to:
        1. Review all plans and identify any timing conflicts
        2. Suggest adjustments to optimize the schedule
        3. Create a cohesive daily timetable
        4. Ensure proper spacing between activities
        5. Consider energy levels throughout the day
        
        Provide:
        1. Hour-by-hour timetable
        2. Activity transitions and preparation time
        3. Energy level considerations
        4. Notes on activity relationships
        5. Recommendations for schedule optimization
        
        Format the response in a clear, structured way.
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    def create_progress_report(self, history, integrated_schedule):
        """Create a weekly progress report"""
        prompt = f"""
        As a health coach, generate a weekly progress report based on:
        
        History: {history}
        Current Schedule: {integrated_schedule}
        
        Analyze:
        1. How well the integrated schedule is working
        2. Areas for improvement
        3. Success metrics
        
        Provide:
        1. Weekly achievements summary
        2. Progress analysis
        3. Motivation and encouragement
        4. Suggestions for improvement
        5. Next week's goals
        
        Format the response in a clear, structured way.
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        return response.choices[0].message.content 