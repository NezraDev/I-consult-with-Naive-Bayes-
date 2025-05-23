import json
import pickle
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import os

with open('data/diseases/disease_symptoms.json', 'r') as f:
    disease_symptoms = json.load(f)


data = []
for disease, symptom_lists in disease_symptoms.items():
    for symptoms in symptom_lists:
        data.append((symptoms, disease))


symptom_lists = [item[0] for item in data]
labels = [item[1] for item in data]


mlb = MultiLabelBinarizer()
X = mlb.fit_transform(symptom_lists)
y = labels

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train model
model = MultinomialNB(alpha=0.1)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save model
os.makedirs('model', exist_ok=True)
with open('model/naive_bayes_model.pkl', 'wb') as f:
    pickle.dump((model, mlb), f)

print("Model trained and evaluated successfully!")
