import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # For handling background image

# Your API Key
api_key = '747f4278e4fe834e33b7f78d783d25af'

# Function to get weather data
def get_weather():
    city = city_entry.get()  # Get the city from the input field
    if not city:
        messagebox.showerror("Input Error", "Please enter a city name.")
        return

    try:
        # API Request
        weather_data = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        ).json()

        if weather_data.get('cod') == '404':
            messagebox.showerror("Error", "City not found.")
        else:
            weather = weather_data['weather'][0]['main']
            temp = round(weather_data['main']['temp'])
            # Display weather data
            result_label.config(
                text=f"Weather in {city}: {weather}\nTemperature: {temp}°C"
            )
    except Exception as e:
        messagebox.showerror("Error", "Unable to fetch weather data.")

# Create the Tkinter window
root = tk.Tk()
root.title("Weather Picker")
root.geometry("800x500")
root.resizable(False, False)





# Heading Label
heading_label = tk.Label(
    root, text="Weather Picker", font=("calibri", 30, "bold")
)
heading_label.pack(pady=20)

# City Input
city_label = tk.Label(root, text="Enter city name:", font=("calibri", 19) )
city_label.pack(pady=5)

city_entry = tk.Entry(root, font=("Arial", 14), width=35, relief="solid")
city_entry.pack(pady=5)

# Get Weather Button
get_weather_button = tk.Button(
    root,
    text="Get Weather",
    font=("Arial", 14),
    bg="#4CAF50",
    fg="white",
    activebackground="#45a049",
    relief="raised",
    command=get_weather,
)
get_weather_button.pack(pady=15)

# Result Label
result_label = tk.Label(
    root, text="", font=("Arial", 14, "bold"), fg="white", bg="#4682B4", justify="center"
)
result_label.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()
