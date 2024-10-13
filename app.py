import os
import re
from flask import Flask, render_template, request
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain

# os.environ['OPENAI_API_KEY'] = 'your_api_key'

app = Flask(__name__)

llm_resto = OpenAI(temperature=0.6)
prompt_template_resto = PromptTemplate(
    input_variables=['age', 'gender', 'weight', 'height', 'disease', 'fitness_goal'],
    template="Exercise Recommendation System: \n"
            "Please provide a weekly workout plan for an individual based on the following criteria: \n"
             "Person age: {age}\n"
             "Person gender: {gender}\n"
             "Person weight: {weight} kg\n"
             "Person height: {height} cm\n"
             "Person generic disease or condition: {disease}\n"
             "Person fitness goal: {fitness_goal}\n"
            "The plan should include the following for each day of the week: \n"
            "Workout routine: a brief but detailed one to two sentence description of the workout \n"
            "Exercise type: type of exercise (ex: cardio, strength training, flexibility, etc.) \n"
            "Intensity level: a number on a scale from 1 (light) to 5 (intensive) \n"
            "Duration: approximate time in minutes \n"
            "Please format the response as follows for each day of the week starting on Monday: \n"
            "[Day of the week] \n"
            "Workout routine: \n"
            "Exercise type: \n"
            "Intensity level: \n"
            "Duration: \n"
)

food_prompt = PromptTemplate(
    input_variables=['age', 'gender', 'weight', 'height', 'disease', 'fitness_goal'],
    template="Diet Recommendation: \n"
            "Please provide a weekly diet plan for an individual based on the following criteria: \n"
             "Person age: {age}\n"
             "Person gender: {gender}\n"
             "Person weight: {weight} kg\n"
             "Person height: {height} cm\n"
             "Person generic disease or condition: {disease}\n"
             "Person fitness goal: {fitness_goal}\n"
             "The plan should include the following for each day of the week: \n"
             "Breakfast: a two to five word breakfast idea \n"
             "Lunch: a two to five word lunch idea \n"
             "Dinner: a two to five word dinner idea \n"
            "Please format the response as follows for each day of the week starting on Monday and ending on Sunday: \n"
            "[Day of the week] \n"
            "Breakfast: \n"
            "Lunch: \n"
            "Dinner: \n"
)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
@app.route('/recommend', methods=['POST'])
def recommend():
    if request.method == "POST":
        age = request.form.get('age')
        height = request.form.get('height')
        weight = request.form.get('weight')
        fitness_goal = request.form.get('fitness_goal')
        gender = request.form.get('gender')
        disease = request.form.get('disease')

        chain_resto = LLMChain(llm=llm_resto, prompt=prompt_template_resto)
        chain_rest_add = LLMChain(llm=llm_resto, prompt=food_prompt)

        input_data = {
            'age': age,
            'gender': gender,
            'weight': weight,
            'height': height,
            'disease': disease,
            'fitness_goal': fitness_goal
        }

        results = chain_resto.run(input_data)
        food_results = chain_rest_add.run(input_data)

        workout_pattern = r'Workout routine:\s*(.*?)(?=\nExercise type:|\Z)'
        workout_type = r'Exercise type:\s*(.*?)(?=\nIntensity level:|\Z)'
        intensity_pattern = r'Intensity level:\s*(.*?)(?=\nDuration:|\Z)'
        duration_pattern = r'Duration:\s*(.*?)(?=\n{2,}|\Z)'

        breakfast_pattern = r'Breakfast:\s*(.*?)(?=\nLunch:|\Z)'
        lunch_pattern = r'Lunch:\s*(.*?)(?=\Dinner:|\Z)'
        dinner_pattern = r'Dinner:\s*(.*?)(?=\n{2,}|\Z)'

        workout_routines = re.findall(workout_pattern, results, re.DOTALL)
        exercise_types = re.findall(workout_type, results, re.DOTALL)
        intensity_levels = re.findall(intensity_pattern, results, re.DOTALL)
        durations = re.findall(duration_pattern, results, re.DOTALL)

        breakfasts = re.findall(breakfast_pattern, food_results, re.DOTALL)
        lunches = re.findall(lunch_pattern, food_results, re.DOTALL)
        dinners = re.findall(dinner_pattern, food_results, re.DOTALL)

        workout_routines = [routine.strip() for routine in workout_routines]
        exercise_types = [exercise.strip() for exercise in exercise_types]
        intensity_levels = [intensity.strip() for intensity in intensity_levels]
        durations = [duration.strip() for duration in durations]

        breakfasts = [breakfast.strip() for breakfast in breakfasts]
        lunches = [lunch.strip() for lunch in lunches]
        dinners = [dinner.strip() for dinner in dinners]
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        zipped_data = zip(days, durations, workout_routines, exercise_types, intensity_levels, breakfasts, lunches, dinners)
        return render_template('result.html', zipped_data=zipped_data)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)