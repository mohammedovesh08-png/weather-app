from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv("WEATHER_API_KEY")

@app.route("/", methods=["GET", "POST"])
def home():
    weather = None
    error = None

    if request.method == "POST":
        city = request.form.get("city")

        if not city:
            error = "Please enter a city name."
        elif not API_KEY:
            error = "Weather API key is not configured."
        else:
            url = "https://api.openweathermap.org/data/2.5/weather"

            params = {
                "q": city,
                "appid": API_KEY,
                "units": "metric"
            }

            response = requests.get(url, params=params)

            if response.status_code == 200:
                data = response.json()

                weather = {
                    "city": data["name"],
                    "country": data["sys"]["country"],
                    "temperature": data["main"]["temp"],
                    "humidity": data["main"]["humidity"],
                    "wind": data["wind"]["speed"],
                    "condition": data["weather"][0]["description"]
                }
            else:
                error = "City not found. Please try again."

    return render_template("index.html", weather=weather, error=error)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
