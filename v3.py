#!/usr/bin/env python
# coding: utf-8

# In[2]:


import folium
import requests
import webbrowser
import time
import logging
import pyautogui

logging.basicConfig(filename='output.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Function to get the weather data
def get_weather_data(api_key, lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=imperial"
    response = requests.get(url)
    data = response.json()
    return data

# Function to display the map
def display_map(api_key, zoom):
    # Create the map object
    map = folium.Map(location=[39.8283, -98.5795], zoom_start=zoom)

    # Get the list of cities from the file
    with open('untitled.txt', 'r') as file:
        cities = file.readlines()

    # Loop through each city and add a marker to the map
    for city in cities:
        city = city.strip()  # Remove newline characters
        url = f"https://nominatim.openstreetmap.org/search?q={city}&format=json"
        response = requests.get(url)
        data = response.json()
        if data:
            lat = data[0]['lat']
            lon = data[0]['lon']
            weather_data = get_weather_data(api_key, lat, lon)
            temp = weather_data['main']['temp']
            humidity = weather_data['main']['humidity']
            wind_speed = weather_data['wind']['speed']
            description = weather_data['weather'][0]['description']
            popup = f"Temperature: {temp}°F<br>Humidity: {humidity}%<br>Wind Speed: {wind_speed} mph<br>Description: {description}"
            folium.Marker(location=[lat, lon], popup=popup).add_to(map)

    # Display the map
    return map

# Main function to run the program
def main():
    # Enter your OpenWeatherMap API key here
    api_key = "40c452e13554e6a9ec421b99eef31b8e"
    url = 'weather_map.html'
    zoom = 4
    first_iteration = True

    while True:
        # Display the map
        map = display_map(api_key,zoom)
        map.save(url)
        logging.info('Map refreshed.')
        print("Map saved as weather_map.html")

        # Reload the page if not the first iteration
        if not first_iteration:
            windows = pyautogui.getWindowsWithTitle('weather_map.html')
            if windows:
                window = windows[0]
                window.activate()
                pyautogui.hotkey('ctrl', 'r')
        else:
            webbrowser.open(url, new=2)
            first_iteration = False

        time.sleep(30)

if __name__ == "__main__":
    main()

    #refreshes the page we want but messes up zoom level after refresh


# In[4]:





# In[ ]:




