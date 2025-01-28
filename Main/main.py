import tkinter as tk  # GUI library for creating the application window
from tkinter import ttk, messagebox  # ttk for styled widgets, messagebox for showing error dialogs
import requests  # For making API requests to fetch weather data
from PIL import Image, ImageTk, ImageFilter  # For handling images and applying effects
import os  # For file path handling

# Function to fetch weather data based on user input
def search_weather():
    user_input = city_entry.get()  # Get the city name entered by the user
    api_key = "747f4278e4fe834e33b7f78d783d25af"  # API key for OpenWeatherMap
    base_url = "http://api.openweathermap.org/data/2.5/weather?"  # Base URL for the API
    complete_url = base_url + "appid=" + api_key + "&q=" + user_input + "&units=metric"  # Full API request URL

    try:
        # Display loading message while fetching data
        loading_label.config(text="Fetching Weather Data...")
        root.update_idletasks()  # Ensure the UI updates while loading
        weather_data = requests.get(complete_url).json()  # Get weather data in JSON format
        loading_label.config(text="")  # Clear the loading message

        # Check for API errors
        if weather_data.get("cod") != 200:
            error_message = weather_data.get("message", "Error fetching weather data.")
            messagebox.showerror("Error", error_message.capitalize())  # Show error message
            return

        # Extract weather details from the API response
        weather = weather_data["weather"][0]["main"].lower()  # Weather condition (e.g., clear, clouds)
        temp = round(weather_data["main"]["temp"])  # Current temperature
        humidity = weather_data["main"]["humidity"]  # Humidity percentage
        wind_speed = weather_data["wind"]["speed"]  # Wind speed in m/s
        
        # Display the weather data on the UI
        result_label.config(
            text=f"{weather.capitalize()} | {temp}ºC\nHumidity: {humidity}% | Wind: {wind_speed} m/s"
        )
        update_background(weather)  # Update the background image based on the weather
    except Exception as e:
        messagebox.showerror("Error", str(e))  # Show any unexpected errors

# Function to update the background image based on weather conditions
def update_background(weather_condition):
    """
    Update the background image based on the weather condition and apply a blur effect with transparency.
    """
    # Map weather conditions to corresponding image files
    weather_images = {
        "clear": "sunny.jpg",
        "clouds": "cloudy.jpg",
        "rain": "rainy.jpg",
        "snow": "snowy.jpg",
        "mist": "misty.jpg",
        "drizzle": "drizzle.jpg",
        "thunderstorm": "stormy.jpg",
        "haze": "haze.jpg",
        "smoke": "smoke.jpg",
    }
    image_file = weather_images.get(weather_condition, "default.jpg")  # Default image if condition is unknown
    image_path = os.path.join(os.path.dirname(__file__), image_file)  # Full path to the image file

    try:
        # Load and resize the image
        bg_image = Image.open(image_path)
        bg_image = bg_image.resize((800, 600), Image.LANCZOS)

        # Add an overlay for better contrast
        overlay = Image.new("RGBA", bg_image.size, (0, 0, 0, 120))  # Semi-transparent black overlay
        blended_image = Image.alpha_composite(bg_image.convert("RGBA"), overlay)  # Blend overlay with background image

        bg_photo = ImageTk.PhotoImage(blended_image)  # Convert the image to a format usable in Tkinter
        background_label.config(image=bg_photo)  # Update the background image
        background_label.image = bg_photo  # Prevent garbage collection
    except Exception as e:
        messagebox.showerror("Error", str(e))  # Show error if image fails to load

# Create the main window
root = tk.Tk()
root.title("Weather Picker Application")  # Set window title
root.geometry("600x500")  # Set fixed window size
root.resizable(False, False)  # Disable resizing for consistent layout

# Define colors and fonts for UI elements
font_large = ("Segoe UI", 30, "bold")
font_medium = ("Segoe UI", 18)
font_small = ("Segoe UI", 14)
text_color = "black"  # Text color

# Create and place the background image label
background_label = tk.Label(root)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Title and input section
title_label = tk.Label(
    root,
    text="Weather App",
    font=font_large,
    fg=text_color,
    bg="white",  # Background color
)
title_label.pack(pady=20)  # Add spacing around the title

city_entry = ttk.Entry(root, font=font_medium, justify="center")  # Input field for city name
city_entry.pack(pady=10)
city_entry.insert(0, "Enter city name...")  # Placeholder text

search_button = ttk.Button(root, text="Search Weather", command=search_weather)  # Button to fetch weather
search_button.pack(pady=15)

loading_label = tk.Label(root, text="", font=font_small, fg=text_color, bg=None)  # Label for loading message
loading_label.pack()

# Result display label
result_label = tk.Label(
    root,
    text="",
    font=("Segoe UI", 22, "bold"),
    fg=text_color,
    bg="white",  # Background color
    justify="center",
)
result_label.pack(pady=20)

# Run the application
root.mainloop()
