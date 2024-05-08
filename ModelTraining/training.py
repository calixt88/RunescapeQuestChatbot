import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score

intent_df = pd.read_csv('intent_training_data.csv')
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(intent_df['question'])
y = intent_df['intent']

try:
    with open('vectorizer.pkl', 'wb') as file:
        pickle.dump(vectorizer, file)
except IOError:
    print("Failed to save the vectorizer to a model.")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("Classification Report:")
print(classification_report(y_test, y_pred))
print("Accuracy:", accuracy_score(y_test, y_pred))

cv_scores = cross_val_score(model, X, y, cv=5)
print("Cross-Validation Mean Accuracy:", cv_scores.mean())

try:
    with open('model.pkl', 'wb') as file:
        pickle.dump(model, file)
except IOError:
    print("Failed to save the trained model.")
