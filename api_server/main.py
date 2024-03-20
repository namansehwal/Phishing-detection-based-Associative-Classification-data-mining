import warnings
import os

from flask import Flask, request, jsonify
import joblib
import numpy as np


from utils.url_parser import URLParser

# warnings.filterwarnings("ignore", message="X does not have valid feature names")

app = Flask(__name__)

# add "models/trained_models/phishing_model.pkl" to the path


model_path = os.path.join(
    os.path.dirname(__file__), "utils/trained_models/phishing_model.pkl")
model = joblib.load(model_path)


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    url = data["url"]
    parser = URLParser(url)
    data = parser.get_all_components_values()
    prediction = model.predict([np.array(list(data))])
    output = prediction[0].item()  # Convert numpy integer to Python integer

    return jsonify({"prediction": output, "url": url, "message": "Prediction says it's a phishing URL" if output == 1 else "Prediction says it's a benign URL"})


if __name__ == "__main__":
    app.run(port=5000, debug=True)
