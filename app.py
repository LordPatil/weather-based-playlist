import requests
from flask import Flask, render_template, request
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify API setup
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv('SPOTIPY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
    redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'),
    scope="user-library-read playlist-read-private"
))


app = Flask(__name__)

# OpenWeather API key
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')

def get_weather(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric'
    response = requests.get(url)
    return response.json()

# Function to map weather condition to Spotify playlist
def get_playlist_for_weather(weather_condition):
    playlists = {
        'Clear': '37i9dQZF1DWSwyaV6GLT48',  # Example sunny playlist ID
        'Rain': '37i9dQZF1DWXe9gFZP0gtP',  # Example rainy playlist ID
        'Clouds': '5LkCNhKwuKa1niaXnFuzVf',  # Example cloudy playlist ID
        'Snow': '37i9dQZF1DX6xZZEgC9Ubl',  # Example snowy playlist ID
        'Thunderstorm': '37i9dQZF1DX4wta20PHgwo',  # Thunderstorm playlist
    }

    playlist_id = playlists.get(weather_condition, '37i9dQZF1DWSwyaV6GLT48')  # Default playlist
    return playlist_id


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form['city']
    weather_data = get_weather(city)
    
    if weather_data.get('cod') != 200:
        return "City not found"
    
    weather_condition = weather_data['weather'][0]['main']
    temperature = weather_data['main']['temp']
    
    playlist_id = get_playlist_for_weather(weather_condition)
    
    return render_template('playlist.html', weather=weather_condition, temp=temperature, city=city, playlist_id=playlist_id)


if __name__ == '__main__':
    app.run(debug=True)
