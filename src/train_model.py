import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import os

def main():
    print("Loading dataset...")
    df = pd.read_csv("data/real_resumes.csv")
    
    print(f"Dataset shape: {df.shape}")
    
    # Check if classes have enough samples
    print("Class distribution:")
    print(df['Category'].value_counts())

    # Preprocessing
    X = df['Resume']
    y = df['Category']

    print("Vectorizing text...")
    vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
    X_vec = vectorizer.fit_transform(X)

    # Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, random_state=42)

    print("Training Random Forest Classifier...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    print("Evaluating Model...")
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    
    print(f"Accuracy: {acc * 100:.2f}%")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

    print("Saving models...")
    os.makedirs('models', exist_ok=True)
    with open("models/role_classifier.pkl", "wb") as f:
        pickle.dump(model, f)
    with open("models/vectorizer.pkl", "wb") as f:
        pickle.dump(vectorizer, f)
        
    print("Done! Models saved successfully.")

if __name__ == "__main__":
    main()
