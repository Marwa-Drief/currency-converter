import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

API_KEY = "115b084b8c2b42612340623c"  # Remplace par une clé d'API valide
BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/convert', methods=['GET'])
def convert_currency():
    amount = float(request.args.get('amount'))
    from_currency = request.args.get('from')
    to_currency = request.args.get('to')

    # Récupérer les taux de change
    response = requests.get(BASE_URL + from_currency)
    data = response.json()

    if response.status_code != 200 or "conversion_rates" not in data:
        return jsonify({"error": "Impossible de récupérer les taux de change."})

    rate = data["conversion_rates"].get(to_currency)
    if not rate:
        return jsonify({"error": "Devise non supportée."})

    converted_amount = amount * rate
    return jsonify({"amount": amount, "from": from_currency, "to": to_currency, "converted": converted_amount})

if __name__ == '__main__':
    app.run(debug=True)
