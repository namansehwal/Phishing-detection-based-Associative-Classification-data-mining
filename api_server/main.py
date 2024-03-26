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
    os.path.dirname(__file__), "utils/trained_models/phishing_model.pkl"
)
model = joblib.load(model_path)


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    url = data["url"]

    parser = URLParser(url)
    data = parser.get_all_components()
    # prediction = model.predict(np.array(list(dict(data).values())))
    # a = [2.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 15.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.0, 14.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, 0.0, 0.935901, 0.0, 4766.0, -1.0, -1.0, 1.0, 2.0, 3.0, 589.0, 1.0, 0.0, 0.0, 0.0, 0.0]
    a = [
        data["qty_dot_url"],
        data["qty_hyphen_url"],
        data["qty_underline_url"],
        data["qty_slash_url"],
        data["qty_questionmark_url"],
        data["qty_equal_url"],
        data["qty_at_url"],
        data["qty_and_url"],
        data["qty_exclamation_url"],
        data["qty_space_url"],
        data["qty_tilde_url"],
        data["qty_comma_url"],
        data["qty_plus_url"],
        data["qty_asterisk_url"],
        data["qty_hashtag_url"],
        data["qty_dollar_url"],
        data["qty_percent_url"],
        data["qty_tld_url"],
        data["length_url"],
        data["qty_dot_domain"],
        data["qty_hyphen_domain"],
        data["qty_underline_domain"],
        data["qty_slash_domain"],
        data["qty_questionmark_domain"],
        data["qty_equal_domain"],
        data["qty_at_domain"],
        data["qty_and_domain"],
        data["qty_exclamation_domain"],
        data["qty_space_domain"],
        data["qty_tilde_domain"],
        data["qty_comma_domain"],
        data["qty_plus_domain"],
        data["qty_asterisk_domain"],
        data["qty_hashtag_domain"],
        data["qty_dollar_domain"],
        data["qty_percent_domain"],
        data["qty_vowels_domain"],
        data["domain_length"],
        data["domain_in_ip"],
        data["server_client_domain"],
        data["qty_dot_directory"],
        data["qty_hyphen_directory"],
        data["qty_underline_directory"],
        data["qty_slash_directory"],
        data["qty_questionmark_directory"],
        data["qty_equal_directory"],
        data["qty_at_directory"],
        data["qty_and_directory"],
        data["qty_exclamation_directory"],
        data["qty_space_directory"],
        data["qty_tilde_directory"],
        data["qty_comma_directory"],
        data["qty_plus_directory"],
        data["qty_asterisk_directory"],
        data["qty_hashtag_directory"],
        data["qty_dollar_directory"],
        data["qty_percent_directory"],
        data["directory_length"],
        data["qty_dot_file"],
        data["qty_hyphen_file"],
        data["qty_underline_file"],
        data["qty_slash_file"],
        data["qty_questionmark_file"],
        data["qty_equal_file"],
        data["qty_at_file"],
        data["qty_and_file"],
        data["qty_exclamation_file"],
        data["qty_space_file"],
        data["qty_tilde_file"],
        data["qty_comma_file"],
        data["qty_plus_file"],
        data["qty_asterisk_file"],
        data["qty_hashtag_file"],
        data["qty_dollar_file"],
        data["qty_percent_file"],
        data["file_length"],
        data["qty_dot_params"],
        data["qty_hyphen_params"],
        data["qty_underline_params"],
        data["qty_slash_params"],
        data["qty_questionmark_params"],
        data["qty_equal_params"],
        data["qty_at_params"],
        data["qty_and_params"],
        data["qty_exclamation_params"],
        data["qty_space_params"],
        data["qty_tilde_params"],
        data["qty_comma_params"],
        data["qty_plus_params"],
        data["qty_asterisk_params"],
        data["qty_hashtag_params"],
        data["qty_dollar_params"],
        data["qty_percent_params"],
        data["params_length"],
        data["tld_present_params"],
        data["qty_params"],
        data["email_in_url"],
        data["time_response"],
        data["domain_spf"],
        data["asn_ip"],
        data["time_domain_activation"],
        data["time_domain_expiration"],
        data["qty_ip_resolved"],
        data["qty_nameservers"],
        data["qty_mx_servers"],
        data["ttl_hostname"],
        data["tls_ssl_certificate"],
        data["qty_redirects"],
        data["url_google_index"],
        data["domain_google_index"],
        data["url_shortened"],
    ]
    prediction = model.predict([np.array(a)])
    # prediction = model.predict([np.array(list(data))])

    output = prediction[0].item()  # Convert numpy integer to Python integer

    return jsonify(
        {
            "prediction": output,
            "url": "url",
            "message": (
                "Prediction says it's a phishing URL"
                if output == 1
                else "Prediction says it's a benign URL"
            ),
        }
    )


if __name__ == "__main__":
    app.run(port=5000, debug=True)
