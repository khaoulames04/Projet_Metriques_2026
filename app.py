import requests
from flask import Flask, jsonify, render_template

app = Flask(__name__)

# Route principale
@app.route('/')
def hello_world():
    return render_template('hello.html')

# ------------------------
# Routes API (données JSON)
# ------------------------

@app.get("/paris")
def api_paris():
    url = "https://api.open-meteo.com/v1/forecast?latitude=48.8566&longitude=2.3522&hourly=temperature_2m"
    response = requests.get(url)
    data = response.json()

    times = data.get("hourly", {}).get("time", [])
    temps = data.get("hourly", {}).get("temperature_2m", [])

    n = min(len(times), len(temps))
    result = [{"datetime": times[i], "temperature_c": temps[i]} for i in range(n)]
    return jsonify(result)

@app.get("/vent")
def api_vent():
    # Exemple : vitesse du vent à Marseille
    url = "https://api.open-meteo.com/v1/forecast?latitude=43.2965&longitude=5.3698&hourly=windspeed_10m"
    response = requests.get(url)
    data = response.json()

    times = data.get("hourly", {}).get("time", [])
    winds = data.get("hourly", {}).get("windspeed_10m", [])

    # Prendre la première mesure de chaque jour
    daily = {}
    for t, w in zip(times, winds):
        date = t.split("T")[0]
        if date not in daily:
            daily[date] = w

    result = [{"date": d, "windspeed": daily[d]} for d in daily]
    return jsonify(result)

# ------------------------
# Routes HTML (pages)
# ------------------------

@app.route("/contact")
def MaPremiereAPI():
    return render_template("contact.html")

@app.route("/rapport")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme")
def mon_histogramme():
    return render_template("histogramme.html")

@app.route("/atelier")
def atelier():
    return render_template("atelier.html")

# ------------------------
# Lancement du serveur
# ------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
