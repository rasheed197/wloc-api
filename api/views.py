from django.shortcuts import render

import requests
from django.http import JsonResponse


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def hello(request):
    visitor_name = request.GET.get('visitor_name', 'Guest')
    client_ip = get_client_ip(request)
    
    # Use IPinfo API to get the location
    ipinfo_token = 'cceef769578db1'
    response = requests.get(f'https://ipinfo.io/{client_ip}/json?token={ipinfo_token}')
    location_data = response.json()
    city = location_data.get('city', 'Unknown')

    # Use OpenWeatherMap API to get the temperature
    openweather_api_key = '0ebf4ed69214ca650eb9916c52080339'
    weather_response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={openweather_api_key}&units=metric')
    weather_data = weather_response.json()
    temperature = weather_data['main']['temp']

    response_data = {
        'client_ip': client_ip,
        'location': city,
        'greeting': f'Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {city}'
    }
    return JsonResponse(response_data)

