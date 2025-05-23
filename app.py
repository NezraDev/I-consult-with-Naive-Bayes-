from flask import Flask, render_template, request, redirect, url_for
import pickle
import json

app = Flask(__name__)

# Load model and binarizer
with open('model/naive_bayes_model.pkl', 'rb') as f:
    model, mlb = pickle.load(f)

# Load data
with open('data/diseases/disease_symptoms.json') as f:
    symptoms_data = json.load(f)

with open('data/bodypart/body_part_symptoms.json') as f:
    body_part_symptoms = json.load(f)

@app.route('/')
def home():
    return render_template('index.html',
                           body_parts=body_part_symptoms.keys())

@app.route("/diagnosis")
def diagnosis():
    selected_part = request.args.get('part')
    return render_template('diagnosis.html', selected_part=selected_part)

@app.route("/assessment", methods=['GET'])
def assessment():
    selected_parts = request.args.get('part', '').split(',')

    if not selected_parts or selected_parts == ['']:
        return redirect(url_for('home'))

    symptoms = []
    for part in selected_parts:
        symptoms.extend(body_part_symptoms.get(part, []))

    valid_symptoms = [s for s in symptoms if s in mlb.classes_]

    possible_diseases = {
        disease
        for disease, symptom_list in symptoms_data.items()
        if any(s in symptom_list for s in valid_symptoms)
    }

    return render_template(
        'assessment.html',
        body_parts=selected_parts,
        symptoms=valid_symptoms,
        possible_diseases=list(possible_diseases)
    )

@app.route('/predict', methods=['POST'])
def predict():
    symptoms = request.form.getlist('symptoms[]')
    body_parts = request.form.getlist('body_parts[]')

    if not symptoms:
        return redirect(url_for('home'))

    try:
        input_vector = mlb.transform([symptoms])
        probabilities = model.predict_proba(input_vector)[0]
        classes = model.classes_

        prob_percent = [round(p * 100, 2) for p in probabilities]

        top_idx = prob_percent.index(max(prob_percent))
        top_disease = classes[top_idx]
        top_prob = prob_percent[top_idx]

        all_probs = sorted(
            zip(classes, prob_percent),
            key=lambda x: x[1],
            reverse=True
        )

        return render_template(
            'result.html',
            top_disease=top_disease,
            top_prob=top_prob,
            all_probs=all_probs,
            body_parts=body_parts
        )

    except Exception as e:
        return f"Error processing symptoms: {str(e)}", 400

if __name__ == '__main__':
    app.run(debug=True)