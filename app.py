import os
import re
from flask import Flask, render_template, request
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain

os.environ['OPENAI_API_KEY'] = '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'

app = Flask(__name__)

llm_resto = OpenAI(temperature=0.6)
#TODO: Put prompt template here 
prompt_template_resto = PromptTemplate(
    input_variables=['age', 'gender', 'weight', 'height', 'disease', 'fitness goal'],
    template="Exercise Recommendation System: \n"
            "I want you to recommend [prompt] based on the following criteria: "     
)



@app.route('/')
def index():
    return render_template('index.html')

# TODO: implement this method
@app.route('/recommend', methods=['POST'])
def recommend():
    if request.method == ["POST"]:
        age = request.form['age']
        gender = request.form['gender']
        weight = request.form['weight']
        height = request.form['height']
        disease = request.form['disease']
        fitness_goal = request.form['fitness goal']

        chain_resto = LLMChain(llm=llm_resto, prompt=prompt_template_resto)
        input_data = {
            'age': age,
            'gender': gender,
            'weight': weight,
            'height': height,
            'disease': disease,
            'fitness_goal': fitness_goal
        }
        
        results = chain_resto.run(input_data)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)