import json
import pickle
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import MultiLabelBinarizer
import os

with open('data/diseases/disease_symptoms.json', 'r') as f:
    disease_symptoms = json.load(f)

data = [(symptoms, disease) for disease, symptoms in disease_symptoms.items()]

symptoms = [item[0] for item in data]
labels = [item[1] for item in data]

mlb = MultiLabelBinarizer()
X = mlb.fit_transform(symptoms)
y = labels

model = MultinomialNB(alpha=0.5)
model.fit(X, y)

os.makedirs('model', exist_ok=True)
with open('model/naive_bayes_model.pkl', 'wb') as f:
    pickle.dump((model, mlb), f)

print("Model trained and saved successfully!")