import tkinter as tk
from tkinter import ttk, messagebox
import requests
from PIL import Image, ImageTk

def search_weather():
    user_input = city_entry.get()
    api_key = "747f4278e4fe834e33b7f78d783d25af"  # Replace with your actual API key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + user_input + "&units=metric"

    try:
        loading_label.config(text="Loading...")
        weather_data = requests.get(complete_url)
        loading_label.config(text="")
        if weather_data.json()['cod'] == '404':
            messagebox.showerror("Error", "No City Found")
        else:
            weather = weather_data.json()['weather'][0]['main']
            temp = round(weather_data.json()['main']['temp'])
            humidity = weather_data.json()['main']['humidity']
            wind_speed = weather_data.json()['wind']['speed']
            result_label.config(text=f"Weather: {weather}\nTemperature: {temp}ºC\nHumidity: {humidity}%\nWind Speed: {wind_speed} m/s")
    except Exception as e:
        loading_label.config(text="")
        messagebox.showerror("Error", f"An error occurred: {e}")

# Create the main window
root = tk.Tk()
root.title("Weather App")
root.geometry("500x400")
root.configure(bg="#e0f7fa")

# Add background image
background_image = Image.open("background.jpg")  # Replace with your image path
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(root, image=background_photo)
background_label.place(relwidth=1, relheight=1)

# Create and place the widgets
style = ttk.Style()
style.configure("TLabel", font=("Helvetica", 12), background="#e0f7fa")
style.configure("TButton", font=("Helvetica", 10), padding=10)

# Header label
header_label = ttk.Label(root, text="Weather App", font=("Helvetica", 16, "bold"), background="#e0f7fa")
header_label.pack(pady=10)

# Frame for input and button
input_frame = ttk.Frame(root, padding="10 10 10 10", style="TFrame")
input_frame.pack(pady=10)

city_label = ttk.Label(input_frame, text="Enter city:")
city_label.grid(row=0, column=0, padx=5, pady=5)

city_entry = ttk.Entry(input_frame, width=20)
city_entry.grid(row=0, column=1, padx=5, pady=5)

search_button = ttk.Button(input_frame, text="Search", command=search_weather)
search_button.grid(row=0, column=2, padx=5, pady=5)

# Loading label
loading_label = ttk.Label(root, text="", font=("Helvetica", 12), background="#e0f7fa")
loading_label.pack(pady=5)

# Result label
result_label = ttk.Label(root, text="", font=("Helvetica", 12), background="#e0f7fa")
result_label.pack(pady=20)

# Run the application
root.mainloop()