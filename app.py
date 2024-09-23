import requests
from flask import Flask, render_template, request
import os
import random
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
def get_playlist_for_weather(weather_condition):
    playlists = {
        'Clear': [
            '37i9dQZF1DWSwyaV6GLT48',  # Happy Hits!
            '37i9dQZF1DX1L0MDB1OjHO',  # Summer Hits
            '37i9dQZF1DX0UrRvztWcAU',  # Feel Good Summer
            '37i9dQZF1DWVQFeOZe8RXK'   # Sunny Vibes
        ],
        'Rain': [
            '37i9dQZF1DWXe9gFZP0gtP',  # Rainy Day
            '37i9dQZF1DXbvABJXBIyiY',  # Rainy Jazz
            '37i9dQZF1DX2UgsUIg75Vg',  # Cozy Rainy Day
            '37i9dQZF1DWYxwmBaMqxsl'   # Rainy Lofi
        ],
        'Clouds': [
            '5LkCNhKwuKa1niaXnFuzVf',  # Cloudy Day
            '37i9dQZF1DX4wta20PHgwo',  # Melancholy Instrumental
            '37i9dQZF1DWWQRwui0ExPn',  # Cloudy Day
            '37i9dQZF1DWZd79rJ6a7lp'   # Atmospheric Calm
        ],
        'Snow': [
            '37i9dQZF1DX6xZZEgC9Ubl',  # Winter Wonderland
            '37i9dQZF1DX4H7FFCTN4M6',  # Cozy Winter
            '37i9dQZF1DWWCe7lhDTJjT',  # Hygge
            '37i9dQZF1DWX1KPlrqx6Qs'   # Winter Magic
        ],
        'Thunderstorm': [
            '37i9dQZF1DX4wta20PHgwo',  # Melancholy Instrumental
            '37i9dQZF1DXbITWG1ZJKYt',  # Acoustic Rock
            '37i9dQZF1DWXmlLSKkfdAk',  # Intense studying
            '37i9dQZF1DX5trt9i14X7j'   # Relaxing Thunderstorms
        ]
    }
    weather_playlists = playlists.get(weather_condition, playlists['Clear'])
    return random.choice(weather_playlists)

def get_playlist_for_mood(mood):
    playlists = {
        'Happy': [
            '37i9dQZF1DXdPec7aLTmlC',  # Happy Hits!
            '37i9dQZF1DX3rxVfibe1L0',  # Mood Booster
            '37i9dQZF1DX9XIFQuFvzM4',  # Confidence Boost
            '37i9dQZF1DX2sUQwD7tbmL'   # 500 Greatest Feel Good Songs
        ],
        'Sad': [
            '37i9dQZF1DX7qK8ma5wgG1',  # Life Sucks
            '37i9dQZF1DX3YSRoSdA634',  # Down in the Dumps
            '37i9dQZF1DWSqBruwoIXkA',  # Sad Indie
            '37i9dQZF1DX2pSTOxoPbx9'   # Sad Beats
        ],
        'Energetic': [
            '37i9dQZF1DX76Wlfdnj7AP',  # Beast Mode
            '37i9dQZF1DX3ZFxrt0Qh0T',  # Power Workout
            '37i9dQZF1DWTl4y3vgJOXW',  # Cardio
            '37i9dQZF1DX0HRj9P7NxeE'   # Workout Twerkout
        ],
        'Relaxed': [
            '37i9dQZF1DWZqd5JICZI0u',  # Peaceful Piano
            '37i9dQZF1DWYcDQ1hSjOpY',  # Deep Sleep
            '37i9dQZF1DX1s9knjP51Oa',  # Calm Vibes
            '37i9dQZF1DWXe9gFZP0pXh'   # Ambient Relaxation
        ],
        'Romantic': [
            '37i9dQZF1DX2L0iB23HSeC',  # Romantic Ballads
            '37i9dQZF1DX3oM43CtKnRV',  # Romance Latino
            '37i9dQZF1DWTbzY5gOVvKd',  # Love Pop
            '37i9dQZF1DX50QitC6Oqtn'   # Love Mood
        ],
        'Rain': [
            '37i9dQZF1DWXe9gFZP0gtP',  # Rainy Day
            '37i9dQZF1DXbvABJXBIyiY',  # Rainy Jazz
            '37i9dQZF1DX2UgsUIg75Vg',  # Cozy Rainy Day
            '37i9dQZF1DWYxwmBaMqxsl'   # Rainy Lofi
        ]

    }
    mood_playlists = playlists.get(mood, playlists['Happy'])
    return random.choice(mood_playlists)

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

@app.route('/mood', methods=['POST'])
def mood():
    mood = request.form['mood']
    playlist_id = get_playlist_for_mood(mood)
    return render_template('playlist.html', mood=mood, playlist_id=playlist_id)


# List of playlist IDs
playlist_ids = [
    '37i9dQZF1DXcBWIGoYBM5M',  # Today's Top Hits
    '37i9dQZF1DX0XUsuxWHRQd',  # RapCaviar
    '37i9dQZF1DWXRqgorJj26U',  # Rock Classics
    '37i9dQZF1DX4sWSpwq3LiO',  # Peaceful Piano
    '37i9dQZF1DX1lVhptIYRda',  # Hot Country
    '37i9dQZF1DX4WYpdgoIcn6',  # Chill Hits
    '37i9dQZF1DX76Wlfdnj7AP',  # Beast Mode
    '37i9dQZF1DX4UtSsGT1Sbe',  # All Out 80s
    '37i9dQZF1DX3rxVfibe1L0',  # Mood Booster
    '37i9dQZF1DX0BcQWzuB7ZO',  # Dance Hits
    '37i9dQZF1DX4o1oenSJRJd',  # Throwback Thursday
    '37i9dQZF1DX70RN3TfWWJh',  # Cardio
    '37i9dQZF1DXdPec7aLTmlC',  # Happy Hits!
    '37i9dQZF1DWSqmBTGDYngZ',  # Songs to Sing in the Car
    '37i9dQZF1DXadOVCgGhS7j',  # Workout
    '37i9dQZF1DWUa8ZRTfalHk',  # Pop Rising
    '37i9dQZF1DX2Nc3B70tvx0',  # Indie Pop
    '37i9dQZF1DX4JAvHpjipBk',  # New Music Friday
    '37i9dQZF1DWZeKCadgRdKQ',  # Deep Focus
    '37i9dQZF1DX0h0QnLkMBl4',  # Acoustic Hits
    '37i9dQZF1DX3YSRoSdA634',  # Soft Pop Hits
    '37i9dQZF1DXbITWG1ZJKYt',  # Jazz Vibes
    '37i9dQZF1DWWEJlAGA9gs0',  # Classical Essentials
    '37i9dQZF1DX10zKzsJ2jva',  # Latin Pop Hits
    '37i9dQZF1DX2SK4ytI2KAZ',  # Alternative Beats
]

@app.route('/random')
def random_playlist():
    # Fetch a random Spotify playlist and return the playlist ID
    # (implementation omitted for brevity)

    random_playlist_id = random.choice(playlist_ids)
    return render_template('playlist.html', playlist_id=random_playlist_id)

if __name__ == '__main__':
    app.run(debug=True)