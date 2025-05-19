from flask import Flask, render_template, request, redirect, url_for
import pickle
import json
from collections import defaultdict

app = Flask(__name__)

with open('model/naive_bayes_model.pkl', 'rb') as f:
    model, mlb = pickle.load(f)

with open('symptoms/disease_symptoms.json') as f:
    symptoms_data = json.load(f)

body_part_symptoms = {
  "head": ["headache", "light sensitivity", "nausea", "dizziness", "blurred vision", "vision changes"],
  "left-ear": ["left ear pain", "left hearing loss", "left ear discharge", "left ear itching", "left ear fullness"],
  "right-ear": ["right ear pain", "right hearing loss", "right ear discharge", "right ear itching", "right ear fullness"],
  "neck": ["neck pain", "neck stiffness", "neck swelling", "neck spasms", "neck tenderness"],
  "chest": ["chest pain", "chest tightness", "shortness of breath", "palpitations", "chest pressure"],
  "right-shoulder": ["right shoulder pain", "right shoulder stiffness", "right shoulder weakness", "right shoulder popping", "right shoulder swelling"],
  "left-shoulder": ["left shoulder pain", "left shoulder stiffness", "left shoulder weakness", "left shoulder popping", "left shoulder swelling"],
  "abdominal": ["abdominal pain", "bloating", "nausea", "vomiting", "diarrhea"],
  "pelvic": ["pelvic pain", "urinary urgency", "painful urination", "pelvic pressure", "pelvic heaviness"],
  "left-thigh": ["left thigh pain", "left thigh numbness", "left thigh swelling", "left thigh weakness", "left thigh cramping"],
  "right-thigh": ["right thigh pain", "right thigh numbness", "right thigh swelling", "right thigh weakness", "right thigh cramping"],
  "left-knee": ["left knee pain", "left knee swelling", "left knee stiffness", "left knee instability", "left knee clicking"],
  "right-knee": ["right knee pain", "right knee swelling", "right knee stiffness", "right knee instability", "right knee clicking"],
  "left-leg": ["left leg pain", "left leg swelling", "left leg cramps", "left leg numbness", "left leg weakness"],
  "right-leg": ["right leg pain", "right leg swelling", "right leg cramps", "right leg numbness", "right leg weakness"],
  "left-foot": ["left foot pain", "left foot swelling", "left foot numbness", "left foot tingling", "left foot weakness"],
  "right-foot": ["right foot pain", "right foot swelling", "right foot numbness", "right foot tingling", "right foot weakness"],
  "left-arm": ["left arm pain", "left arm numbness", "left arm weakness", "left arm tingling", "left arm swelling"],
  "right-arm": ["right arm pain", "right arm numbness", "right arm weakness", "right arm tingling", "right arm swelling"],
  "left-hand": ["left hand pain", "left hand numbness", "left hand tingling", "left hand weakness", "left hand stiffness"],
  "right-hand": ["right hand pain", "right hand numbness", "right hand tingling", "right hand weakness", "right hand stiffness"],
  "flu": ["fever", "cough", "sore throat", "muscle aches", "fatigue"],
  "migraine": ["headache", "light sensitivity", "nausea", "dizziness", "blurred vision", "vision changes"],
  "ear-infection": ["left ear pain", "left hearing loss", "left ear discharge", "left ear itching", "left ear fullness", "right ear pain", "right hearing loss", "right ear discharge", "right ear itching", "right ear fullness"],
  "neck-strain": ["neck pain", "neck stiffness", "neck swelling", "neck spasms", "neck tenderness"],
  "heart-disease": ["chest pain", "shortness of breath", "palpitations", "fatigue", "chest tightness", "chest pressure"],
  "diabetes": ["frequent urination", "blurred vision", "fatigue", "numbness", "slow healing"],
  "food-poisoning": ["abdominal pain", "nausea", "vomiting", "diarrhea", "bloating"],
  "right-shoulder-injury": ["right shoulder pain", "right shoulder stiffness", "right shoulder weakness", "right shoulder popping", "right shoulder swelling"],
  "left-shoulder-injury": ["left shoulder pain", "left shoulder stiffness", "left shoulder weakness", "left shoulder popping", "left shoulder swelling"],
  "uti": ["pelvic pain", "urinary urgency", "painful urination", "pelvic pressure", "pelvic heaviness"],
  "right-thigh-syndrome": ["right thigh pain", "right thigh numbness", "right thigh swelling", "right thigh weakness", "right thigh cramping"],
  "left-thigh-syndrome": ["left thigh pain", "left thigh numbness", "left thigh swelling", "left thigh weakness", "left thigh cramping"],
  "left-knee-condition": ["left knee pain", "left knee swelling", "left knee stiffness", "left knee instability", "left knee clicking"],
  "right-knee-condition": ["right knee pain", "right knee swelling", "right knee stiffness", "right knee instability", "right knee clicking"],
  "left-leg-disorder": ["left leg pain", "left leg swelling", "left leg cramps", "left leg numbness", "left leg weakness"],
  "right-leg-disorder": ["right leg pain", "right leg swelling", "right leg cramps", "right leg numbness", "right leg weakness"],
  "left-foot-disorder": ["left foot pain", "left foot swelling", "left foot numbness", "left foot tingling", "left foot weakness"],
  "right-foot-disorder": ["right foot pain", "right foot swelling", "right foot numbness", "right foot tingling", "right foot weakness"],
  "left-arm-condition": ["left arm pain", "left arm numbness", "left arm weakness", "left arm tingling", "left arm swelling"],
  "right-arm-condition": ["right arm pain", "right arm numbness", "right arm weakness", "right arm tingling", "right arm swelling"],
  "left-hand-condition": ["left hand pain", "left hand numbness", "left hand tingling", "left hand weakness", "left hand stiffness"],
  "right-hand-condition": ["right hand pain", "right hand numbness", "right hand tingling", "right hand weakness", "right hand stiffness"],
  "neuropathy": ["numbness", "tingling", "burning pain", "muscle weakness", "sensitivity"],
  "carpal-tunnel": ["hand numbness", "tingling", "weak grip", "hand pain", "night symptoms"],
  "alzheimers": ["memory loss", "confusion", "difficulty speaking", "mood swings", "disorientation", "memory problems"],
  "anxiety": ["palpitations", "restlessness", "sweating", "trembling", "chest tightness"],
  "depression": ["persistent sadness", "loss of interest", "fatigue", "sleep changes", "appetite changes"]
}



@app.route('/')
def home():
    return render_template('index.html', body_parts=body_part_symptoms.keys())

@app.route("/diagnosis")
def diagnosis():
    selected_part = request.args.get('part')
    return render_template('diagnosis.html', selected_part=selected_part)

@app.route("/assessment", methods=['GET'])
def assessment():
    selected_parts = request.args.get('part', '').split(',')
    
    if not selected_parts or selected_parts == ['']:
        return redirect(url_for('home'))
    
    # Get symptoms for all selected body parts
    symptoms = []
    for part in selected_parts:
        symptoms.extend(body_part_symptoms.get(part, []))
    
    print("All symptoms for", selected_parts, ":", symptoms)
    
    # Only use symptoms that exist in the model's MultiLabelBinarizer
    valid_symptoms = [s for s in symptoms if s in mlb.classes_]
    print("Valid symptoms:", valid_symptoms)
    
    # Find diseases that match at least one valid symptom
    possible_diseases = {
        disease
        for disease, symptom_list in symptoms_data.items()
        if any(s in symptom_list for s in valid_symptoms)
    }
    
    print("Possible diseases:", possible_diseases)
    
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
        return redirect(url_for('home'))  # Or flash an error message

    try:
        input_vector = mlb.transform([symptoms])  # Convert to vector for model
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