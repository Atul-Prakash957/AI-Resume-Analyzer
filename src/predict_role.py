import pickle

# load trained model
model = pickle.load(open("models/role_classifier.pkl", "rb"))
vectorizer = pickle.load(open("models/vectorizer.pkl", "rb"))


def predict_role(text):

    text_vec = vectorizer.transform([text])

    role = model.predict(text_vec)[0]

    return role

