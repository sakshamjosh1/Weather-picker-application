import requests

api_key = '747f4278e4fe834e33b7f78d783d25af'

user_input = input("Enter city: ")

weather_data = requests.get(
    f"http://api.openweathermap.org/data/2.5/weather?q={user_input}&appid={api_key}&units=metric")

if weather_data.json()['cod'] == '404':
    print("No City Found")
else:
    weather = weather_data.json()['weather'][0]['main']
    temp = round(weather_data.json()['main']['temp'])

    print(f"The weather in {user_input} is: {weather}")
    print(f"The temperature in {user_input} is: {temp}ºC")