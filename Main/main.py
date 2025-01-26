import tkinter as tk
from tkinter import ttk, messagebox
import requests
from PIL import Image, ImageTk
import os

def search_weather():
    user_input = city_entry.get()
    api_key = "747f4278e4fe834e33b7f78d783d25af"  # Replace with your actual API key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + user_input + "&units=metric"

    try:
        loading_label.config(text="Loading...")
        root.update_idletasks()  # Ensure the UI updates while loading
        weather_data = requests.get(complete_url).json()
        loading_label.config(text="")

        # Check for errors in the API response
        if weather_data.get('cod') != 200:
            error_message = weather_data.get('message', 'Error fetching weather data.')
            messagebox.showerror("Error", error_message.capitalize())
            return

        # Extract weather details
        weather = weather_data['weather'][0]['main'].lower()
        temp = round(weather_data['main']['temp'])
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed']
        result_label.config(
            text=f"Weather: {weather.capitalize()}\nTemperature: {temp}ºC\nHumidity: {humidity}%\nWind Speed: {wind_speed} m/s"
        )
        
        # Change background based on weather
        update_background(weather)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def update_background(weather_condition):
    """Updates the background image based on the weather condition."""
    weather_images = {
        "clear": "sunny.jpg",
        "clouds": "cloudy.jpg",
        "rain": "rainy.jpg",
        "snow": "snowy.jpg",
        "mist": "misty.jpg",
        "drizzle": "drizzle.jpg",
        "thunderstorm": "stormy.jpg"
    }
    image_file = weather_images.get(weather_condition, "default.jpg")
    image_path = os.path.join(os.path.dirname(__file__), image_file)
    
    try:
        bg_image = Image.open(image_path)
        bg_image = bg_image.resize((400, 300), Image.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
        background_label.config(image=bg_photo)
        background_label.image = bg_photo
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create the main window
root = tk.Tk()
root.title("Weather Picker Application")
root.geometry("400x300")
root.resizable(False, False)

# Create and place the widgets
background_label = tk.Label(root)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

title_label = ttk.Label(root, text="Weather Picker", font=("Helvetica", 16))
title_label.pack(pady=10)

city_label = ttk.Label(root, text="Enter City Name:")
city_label.pack(pady=5)

city_entry = ttk.Entry(root, width=30)
city_entry.pack(pady=5)

search_button = ttk.Button(root, text="Search Weather", command=search_weather)
search_button.pack(pady=10)

loading_label = ttk.Label(root, text="", font=("Helvetica", 10))
loading_label.pack(pady=5)

result_label = ttk.Label(root, text="", font=("Helvetica", 12), background="")
result_label.pack(pady=10)

# Run the application
root.mainloop()