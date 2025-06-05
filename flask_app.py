
# A very simple Flask Hello World app for you to get started with...

import requests
from flask import Flask, request, jsonify
import fuz
print("ok")
app = Flask(__name__)

with open("/home/fuzzypico/mysite/.secret", "r") as secret:
    WAQI_TOKEN = secret.read()
WAQI_URL_TEMPLATE = 'https://api.waqi.info/feed/{}/?token={}'

@app.route('/')
def hello_world():
    return ' fuzzypico.pythonanywhere.com/AQI [POST] {"grad":"sarajevo"} | fuzzypico.pythonanywhere.com/paradajz_fuzzy [POST] {"grad":"sarajevo"} '

@app.route('/QT')
def QuTe():
    return "QuTe"

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
    print("Form data:", request.form)
    vektor = []
    try:
        vektor.append(float(request.form['TemperaturaZraka']))
        vektor.append(float(request.form['VlaznostZraka']))
        vektor.append(float(request.form['BrzinaVjetra']))
        vektor.append(int(request.form['AQI']))
        vektor.append(int(request.form['DaLiPadaKisa']))
        vektor.append(float(request.form['VrijemeDana']))
    except Exception as e:
        return jsonify({"ERROR":str(e)}), 500
    val, zatvori, otvori, nista = fuz.paradajz_fuzzy(vektor)
    #"povrce":"paradajz",
    return jsonify({"fuzzy": val, "zatvori": zatvori, "otvori": otvori, "nista":nista})
