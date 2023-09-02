import requests
import datetime as dt
import smtplib


my_gmail = "your email"
gmail_connection = "smtp.gmail.com"
app_password = "your app pass"
# gmail_port = 465

OWM_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"
API_KEY = "get your own api key"
MY_LAT = 56.4256  # your latitude
MY_LON = 127.1328  # your longitude


def make_hours_text(rainy_list):
    if len(rainy_list) == 1:
        return str(rainy_list[0])
    elif len(rainy_list) == 2:
        return f"{rainy_list[0]} and {rainy_list[1]}"
    elif len(rainy_list) > 2:
        return f"{', '.join([str(i) for i in rainy_hours[:-1]])} and {rainy_hours[-1]}"


parameters = {
    "lat": MY_LAT,
    "lon": MY_LON,
    # "exclude": "current,minutely,hourly,daily",
    "appid": API_KEY,
    "units": "metric"
}
response = requests.get(OWM_ENDPOINT, params=parameters)
response.raise_for_status()
# print("Status Code:", response.status_code)

weather_data = response.json()
needed_hours_info = [{"hour": dt.datetime.fromtimestamp(data["dt"]).hour, "weather": {"id": data["weather"][0]["id"], "description": [data["weather"][0]["main"], data["weather"][0]["description"]]}} for data in weather_data["list"][:5]]
# print(*needed_hours_info, sep="\n")

rainy = False
rainy_hours = []
for hour in needed_hours_info:
    if hour["weather"]["id"] < 700 or hour["weather"]["id"] == 781:
        rainy = True
        rainy_hours.append(hour["hour"])

if rainy:
    message_text = f"It's going to rain around {make_hours_text(rainy_hours)} today...\nTake your Umbrella with you!"
    subject = "RAINY TODAY!"
    msg = f"Subject:{subject}\n\n{message_text}"
    with smtplib.SMTP(gmail_connection) as connection:
        connection.starttls()
        connection.login(user=my_gmail, password=app_password)
        connection.sendmail(from_addr=my_gmail, to_addrs=my_gmail, msg=msg)

else:
    message_text = "It's not going to rain today."
    subject = "NOT RAINY TODAY!"
    msg = f"Subject:{subject}\n\n{message_text}"
    with smtplib.SMTP(gmail_connection) as connection:
        connection.starttls()
        connection.login(user=my_gmail, password=app_password)
        connection.sendmail(from_addr=my_gmail, to_addrs=my_gmail, msg=msg)
