from flask import Flask, request, jsonify
import joblib
import numpy as np
import warnings

warnings.filterwarnings("ignore", message="X does not have valid feature names")

app = Flask(__name__)

# add "models/trained_models/phishing_model.pkl" to the path
import os

model_path = os.path.join(
    os.path.dirname(__file__), "models/trained_models/phishing_model.pkl"
)
model = joblib.load(model_path)


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    prediction = model.predict([np.array(list(data.values()))])
    output = prediction[0].item()  # Convert numpy integer to Python integer

    return jsonify(output)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
