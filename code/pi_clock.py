#coding: utf-8
import scrollphathd as sphd
import datetime
import json
import requests
import time

from scrollphathd.fonts import font3x5


def get_weather_data(app_id, city):
    """Performs the call to the openweathermap service to obtain meteorological information.

	Parameters
	----------
	app_id: str
		API key.
	city: str
		City name.

	Returns
	-------
	dictionary
    	A dictionary containing the current weather conditions.
	"""

    if (app_id == None) or (city == None):
        return None

    url_format = "https://api.openweathermap.org/data/2.5/weather?appid={app_id}&q={city}&units=metric"
    url = url_format.format(app_id=app_id, city=city)
    data = None

    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            data = resp.json()
        else:
            data = None
    except:
        data = None

    return data


def get_weather_status(data):
    """Process the service response to get a text string with the prevailing weather condition.

	Parameters
	----------
	data : dictionary
		Dictionary containing the current weather conditions.

	Returns
	-------
	str
		A text string with the prevailing weather condition.
	"""

    weather = data["weather"][0]
    id = weather["id"]

    options = {
        200: "Tormenta con lluvia ligera",
        201: "Tormenta con lluvia",
        202: "Tormenta con lluvia intensa",
        210: "Tormenta ligera",
        211: "Tormenta",
        212: "Tormenta intensa",
        221: "Tormenta aislada",
        230: "Tormenta con llovizna ligera",
        231: "Tormenta con llovizna",
        232: "Tormenta con llovizna intensa",
        300: "Llovizna ligera",
        301: "Llovizna",
        302: "Llovizna intensa",
        310: "Llovizna ligera",
        311: "Llovizna",
        312: "Llovizna intensa",
        313: "Llovizna y aguaceros",
        314: "Llovizna y lluvia intensa",
        321: "Llovizna",
        500: "Lluvia ligera",
        501: "Lluvia moderada",
        502: "Lluvia intensa",
        503: "Lluvia muy intensa",
        504: "Lluvia torrencial",
        511: "Agua nieve",
        520: "Aguacero ligero",
        521: "Aguacero",
        522: "Aguacero intenso",
        531: "Aguacero aislado",
        600: "Nieve ligera",
        601: "Nieve",
        602: "Nieve intensa",
        611: "Aguanieve",
        612: "Aguanieve ligera",
        613: "Aguanieve intensa",
        615: "Lluvia ligera y nieve",
        616: "Lluvia y nieve",
        620: "Tormenta ligera de nieve",
        621: "Tormenta de nieve",
        622: "Tormenta intensa de nieve",
        701: "Niebla",
        702: "Humo",
        721: "Neblina",
        731: "Polvo",
        741: "Bruma",
        751: "Tormenta de arena",
        761: "Polvo",
        762: "Ceniza",
        771: "Rachas de viento",
        781: "Huracan",
        800: "Despejado",
        801: "Poco nuboso",
        802: "Nubes dispersas",
        803: "Nuboso",
        804: "Muy nuboso"
    }

    return options.get(id, "")


def get_temperature(data):
    """Process the service response to get a text string with the current temperature.

	Parameters
	----------
	data : dictionary
		Dictionary containing the current weather conditions.

	Returns
	-------
	str
		A text string with the current temperature.
	"""

    tmp = data["main"]["temp"]
    return str(int(tmp))


def get_humidity(data):
    """Process the service response to get a text string with the current humidity.

	Parameters
	----------
	data : dictionary
		Dictionary containing the current weather conditions.

	Returns
	-------
	str
		A text string with the current humidity.
	"""

    tmp = data["main"]["humidity"]
    return str(int(tmp))


def build_text(data):
    """Builds the text to show.

	Parameters
	----------
	data : dictionary
		Dictionary containing the current weather conditions.

	Returns
	-------
	str
		A text string with the information to show.
	"""

    text = " "
    now = datetime.datetime.now()
    hour = now.strftime("%H:%M")

    if not (data is None):
        status = get_weather_status(data)
        temp = get_temperature(data)
        hum = get_humidity(data)
        text_format = "{hour} {status}, {temp} grados y {hum}% de humedad "
        text = text_format.format(hour=hour, status=status, temp=temp, hum=hum)
    else:
        text_format = "{hour} Datos no disponibles "
        text = text_format.format(hour=hour)

    return text


def display_text(text):
    """Displays the text.

	Parameters
	----------
	text : string
		Text to show in the display.
	"""

    sphd.write_string(text, y=1, font=font3x5, brightness=0.2)
    sphd.show()

    time.sleep(5)

    length = sphd.get_buffer_shape()[0]

    for x in range(length):
        sphd.scroll()
        sphd.show()
        time.sleep(0.01)

    time.sleep(5)


def main():
    sphd.rotate(180)
    sphd.set_clear_on_exit(False)

    app_id = "xxx"  #Openweathermap API Key
    query = "city"  #City name
    data = get_weather_data(app_id, query)

    text = build_text(data)
    display_text(text)


main()