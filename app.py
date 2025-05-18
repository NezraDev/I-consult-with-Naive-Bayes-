from flask import Flask, render_template, request
import pickle
import os

app = Flask(__name__)


with open('model/naive_bayes_model.pkl', 'rb') as f:
    model, mlb = pickle.load(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    symptoms = request.form.getlist('symptoms')
    input_vector = mlb.transform([symptoms])
    
    
    probabilities = model.predict_proba(input_vector)[0]
    classes = model.classes_

   
    prob_dict = {disease: round(prob * 100, 2) for disease, prob in zip(classes, probabilities)}
    sorted_probs = sorted(prob_dict.items(), key=lambda x: x[1], reverse=True)

   
    top_disease, top_prob = sorted_probs[0]

    return render_template('result.html', top_disease=top_disease, top_prob=top_prob, all_probs=sorted_probs)

if __name__ == '__main__':
    app.run(debug=True)
