import requests
from datetime import datetime, timedelta


def get_weather_api(mesto):

    units = "metric"
    lang = "sk"
    mesto = mesto.lower()
    APIKEY = "ddac9aef54ea6f2bd618a5bab65c4bad"
    URL = f"https://api.openweathermap.org/data/2.5/weather?q={mesto}&appid={APIKEY}&units={units}&lang={lang}"
    request = requests.get(URL)
    data = request.json()

    city = data["name"]

    latitude = data["coord"]["lat"]
    longitude = data["coord"]["lon"]
    aktualne = data["weather"][0]["description"]

    sunrise = data["sys"]["sunrise"]
    sunrise = int(sunrise)
    sunrise = datetime.utcfromtimestamp(sunrise) + timedelta(hours=1)
    sunrise = sunrise.strftime('%H:%M:%S')

    sunset = data["sys"]["sunset"]
    sunset = int(sunset)
    sunset1 = datetime.utcfromtimestamp(sunset) + timedelta(hours=1)
    sunset = datetime.utcfromtimestamp(sunset) + timedelta(hours=1)
    sunset = sunset.strftime('%H:%M:%S')

    temp = data["main"]["temp"]
    temp_max = data["main"]["temp_max"]
    temp_mix = data["main"]["temp_min"]
    feels_like = data["main"]["feels_like"]

    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]

    if datetime.now() > sunset1:
        pocasie = (
                f"Mesto: {city} sa nachadza {latitude} zemepisnej sirky a {longitude} zemepisnej dlzky. Momentalne je {aktualne}"
                f"\nTeplota je {temp}°C. Pocitovo je {feels_like}°C. Max bude {temp_max}°C a min bude {temp_mix}°C"
                f"\nVlhkost je {humidity} % a rychlost vetra je {wind_speed}m/s."
                f"\nVychod slnka bude {sunrise} a zapad slnka bol {sunset}")
    else:
        pocasie = (
            f"Mesto: {city} sa nachadza {latitude} zemepisnej sirky a {longitude} zemepisnej dlzky. Momentalne je {aktualne}"
            f"\nTeplota je {temp}°C. Pocitovo je {feels_like}°C. Max bude {temp_max}°C a min bude {temp_mix}°C"
            f"\nVlhkost je {humidity} % a rychlost vetra je {wind_speed}m/s."
            f"\nVychod slnka bol {sunrise} a zapad slnka bude {sunset}")

    return pocasie
