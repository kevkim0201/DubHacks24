from flask import Flask, render_template, request
import os
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain

os.environ['OPENAI_API_KEY'] = '[put ur key here]'

app = Flask(__name__)

llm_resto = OpenAI(temperature=0.6)
#TODO: Put prompt template here 
prompt_template_resto = PromptTemplate(
    input_variables = ['age', 'gender', 'weight', 'height', 'disease', 'fitness goal']
)


@app.route('/')
def index():
    return render_template('index.html')

# TODO: implement this method
@app.route('/recommend', methods=['POST'])
def recommend():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)




