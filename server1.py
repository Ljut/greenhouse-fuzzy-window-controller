
# A very simple Flask Hello World app for you to get started with...
import requests
from flask import Flask, request, jsonify
import fuz

app = Flask(__name__)

with open(".secret", "r") as secret:
    WAQI_TOKEN = secret.read()
WAQI_URL_TEMPLATE = 'https://api.waqi.info/feed/{}/?token={}'

@app.route('/')
def hello_world():
    return ' dajPoslic.pythonanywhere.com/AQI [POST] {"grad":"sarajevo"} | dajPoslic.pythonanywhere.com/paradajz_fuzzy [POST] {"grad":"sarajevo"} '

@app.route('/AQI', methods=['POST'])
def get_air_quality():
    data = request.get_json()

    if not data or 'grad' not in data:
        return jsonify({'error': 'Missing "grad" in request'}), 400

    grad = data['grad'].strip().lower()
    url = WAQI_URL_TEMPLATE.format(grad, WAQI_TOKEN)

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        aqi = data["data"]["aqi"]
        return jsonify({"aqi": aqi})
        return jsonify(response.json())
    except requests.RequestException as e:
        return jsonify({'error': 'Failed to fetch data from WAQI API', 'details': str(e)}), 500

@app.route('/paradajz_fuzzy', methods=['POST'])
def calc_fuzzy():
    vektor = []
    vektor.append(int(request.form['TemperaturaZraka']))
    vektor.append(int(request.form['VlaznostZraka']))
    vektor.append(int(request.form['BrzinaVjetra']))
    vektor.append(int(request.form['AQI']))
    vektor.append(int(request.form['DaLiPadaKisa']))
    vektor.append(int(request.form['VrijemeDana']))
    return jsonify({"povrce":"paradajz","fuzzy": fuz.paradajz_fuzzy(vektor)})

if __name__ == '__main__':
    app.run(debug=True)
