import pickle

# load trained model
model = pickle.load(open("models/role_classifier.pkl", "rb"))
vectorizer = pickle.load(open("models/vectorizer.pkl", "rb"))


def predict_role(text):

    text_vec = vectorizer.transform([text])

    role = model.predict(text_vec)[0]

    return role


# # test the model when file is run directly
# if __name__ == "__main__":

#     sample_resume = """
#     Python pandas machine learning deep learning SQL numpy
#     """

#     result = predict_role(sample_resume)

#     print("Predicted Role:", result)