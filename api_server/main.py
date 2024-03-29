import warnings
import os

from flask import Flask, request, jsonify
import joblib
import numpy as np
import datetime
from connect_database import add_entry, fetch_all_entries

from utils.url_parser import URLParser

# warnings.filterwarnings("ignore", message="X does not have valid feature names")

app = Flask(__name__)

# add "models/trained_models/phishing_model.pkl" to the path


model_path = os.path.join(
    os.path.dirname(__file__), "utils/trained_models/phishing_model.pkl"
)
model = joblib.load(model_path)


@app.route("/predict", methods=["POST"])
def predict():
    ip_address = request.remote_addr

    data = request.get_json()
    url = data["url"]

    parser = URLParser(url)
    
    prediction = model.predict(parser.np_array())

    output = prediction[0].item()  # Convert numpy integer to Python integer
    # Add an entry
    result = "safe" if output == 0 else "phishing"
    add_entry(ip_address, datetime.datetime.now(), url, result)

    # Fetch all entries
    all_entries = fetch_all_entries()
    for entry in all_entries:
        print(entry)

    return jsonify(
        {
            "prediction": output,
            "url": "url",
            "message": (
                "Prediction says it's a phishing URL"
                if output == 1
                else "Prediction says it's a safe browsing URL"
            ),
        }
    )


if __name__ == "__main__":
    app.run(port=5000, debug=True)
