from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView

from decouple import config
import requests
from datetime import datetime

from .models import City
from .forms import CityForm


class IndexView(ListView):
    template_name = 'weatherapp/index.html'
    model = City

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CityForm
        
        if self.request.method == 'GET':
            if self.request.GET.get('city_name'):
                coords = get_city_coords(self.request.GET.get('city_name'))
                context["weather"] = get_coord_weather(coords) 
                context['weather']['city'] = coords['city_name'] # Because OpenWeather current weather response names are weird/wrong; e.g. Tokyo = Japan
                
            else:
                context['REMOTE_ADDR'] = self.request.META.get('REMOTE_ADDR')
                coords = get_ip_coords(self.request.META.get('REMOTE_ADDR'))
                if coords: 
                    context["weather"] = get_coord_weather(coords)
                    context['weather']['city'] = coords['city_name'] # Because OpenWeather current weather response names are weird/wrong; e.g. Tokyo = Japan

        if context['city_list']:
            favorite_cities_weather_data = []
            for city in context['city_list']:
                coords = get_city_coords(city)
                favorite_cities_weather_data.append(get_coord_weather(coords))
                favorite_cities_weather_data[-1]['city'] = city.city_name
                favorite_cities_weather_data[-1]['pk'] = city.pk
            context['favorite_cities_list'] = favorite_cities_weather_data

        return context


class ForecastDetailView(DetailView):
    template_name = 'weatherapp/forecast.html'
    model = City

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CityForm
        coords = {'latitude': self.object.latitude, 'longitude': self.object.latitude}
        context['weather'] = get_coord_forecast(coords)
        return context


def add(request):
    if request.method == 'POST':
        city_name = request.POST['city']
        latitude = request.POST['lat']
        longitude = request.POST['lon']
        City.objects.create(city_name=city_name,latitude=latitude,longitude=longitude)
    return HttpResponseRedirect(f'{reverse("weatherapp:index_url")}?city_name={city_name}')

def delete(request, pk):
    if request.method == 'POST':
        city = City.objects.get(pk=pk)
        city.delete()
        return redirect('weatherapp:index_url')

# Custom functions used in IndexView #TODO convert to class
# --------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------
def get_ip_coords(ip): 
    """ Gets coordinates of input IP; returns dict of coordinates """
    url = get_api_url('ipstack')
    api_res = make_api_request(url, ip)
    return parse_api_response(api_res, 'ipstack')

def get_city_coords(city_name):
    """ Gets coordinates of input city; returns dict of city name + coordinates in dict """
    url = get_api_url('geo')
    api_res = make_api_request(url, city_name)
    return parse_api_response(api_res, 'geo')

def get_coord_weather(coords):
    """ Get current weather at coordinates; returns weather dict for template context """
    url = get_api_url('weather')
    api_res = make_api_request(url, coords)
    return parse_api_response(api_res, 'weather')

def get_coord_forecast(coords):
    """ Get current weather at coordinates; returns weather dict for template context """
    url = get_api_url('forecast')
    api_res = make_api_request(url, coords)
    return parse_api_response(api_res, 'forecast')


def get_api_url(api_name):
    """ Returns the specified API url with the respective api key """
    OPENWEATHER_ENDPOINTS = ['weather', 'forecast', 'geo']
    IPSTACK_ENDPOINT = 'ipstack'

    if api_name in OPENWEATHER_ENDPOINTS:
        API_KEY = config("openweather_API")
        if api_name == 'weather':
            url = 'https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&units=imperial&appid=' + API_KEY
        elif api_name == 'forecast':
            url = 'https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&units=imperial&appid=' + API_KEY
        else: 
            url = 'http://api.openweathermap.org/geo/1.0/direct?q={}&appid=' + API_KEY
    elif api_name == IPSTACK_ENDPOINT:
        API_KEY = config('IPstack_API')
        url = "http://api.ipstack.com/{}?access_key=" + API_KEY

    return url

def make_api_request(url, url_params):
    """ Use requests to call API and returns response as json """
    if 'ipstack' in url:
        try:
            api_response = requests.get(url.format(url_params)).json() 
        except Exception as e: print(f'ipstack api fail -> {e}')
    elif 'geo' in url:
        try: 
            api_response = requests.get(url.format(url_params)).json()
        except Exception as e: print(f'geo api fail -> {e}')
    elif 'forecast' in url:
        try:
            api_response = requests.get(url.format(url_params["latitude"], url_params["longitude"])).json()
        except Exception as e: print(f'forecast api fail -> {e}')
    else:
        try:
            api_response = requests.get(url.format(url_params["latitude"], url_params["longitude"])).json()
        except Exception as e: print(f'current weather api fail -> {e}')
    
    return api_response

def parse_api_response(api_response, api_name):
    """ Consume API response to get relevant data """
    OPENWEATHER_ENDPOINTS = ['weather', 'forecast', 'geo']
    IPSTACK_ENDPOINT = 'ipstack'

    if api_name == IPSTACK_ENDPOINT:
        try:
            city_name = api_response['city']
            latitude = api_response["latitude"]
            longitude = api_response["longitude"]
            return {'city_name': city_name, "latitude": latitude, "longitude": longitude}
        except Exception as e: 
            print(f"ipstack unexpected response -> {e}")
            return {}
    elif api_name in OPENWEATHER_ENDPOINTS:
        if api_name == 'geo':
            try:
                city_name = api_response[0]['name']
                latitude = api_response[0]["lat"]
                longitude = api_response[0]["lon"]
                return {'city_name': city_name, "latitude": latitude, "longitude": longitude}
            except Exception as e:
                print(f"geo unexpected response -> {e}")
                return {}
        elif api_name == 'weather':
            try:
                weather = {
                    'city_name': api_response['name'],
                    'temperature': api_response['main']['temp'],
                    'description': api_response['weather'][0]['description'],
                    'icon': api_response['weather'][0]['icon'],
                    'latitude': api_response['coord']['lat'],
                    'longitude': api_response['coord']['lon'],
                }
                return weather
            except Exception as e:
                print(f"current weather unexpected response -> {e}")
                return {}
        elif api_name == 'forecast':
            try: 
                days = [ ]
                for interval in api_response['list']:
                    days.append(interval['dt_txt'].split()[0])

                days = list(set(days))
                days = sorted(days)
                # e.g. ['2023-03-13', '2023-03-14', '2023-03-15', '2023-03-16', '2023-03-17', '2023-03-18']

                weather  = {}
                for i in range(len(days)):
                    weather[f'day{i}'] = {}
                    for interval in api_response['list']:
                        if days[i] in interval['dt_txt']:
                            weather[f'day{i}'][interval['dt_txt']] = interval['main']['temp']
                                
                # KEY: day0 
                # VALUES: {'2023-03-13 03:00:00': 289.87, '2023-03-13 06:00:00': 288.66, '2023-03-13 09:00:00': 287.88, '2023-03-13 12:00:00': 284.49, '2023-03-13 15:00:00': 283.52, '2023-03-13 18:00:00': 282.1, '2023-03-13 21:00:00': 280.42}
                temp = []
                for key in weather:
                    for subkey in weather[key]:
                        temp.append(weather[key][subkey])
                    weather[key]['low'] = min(temp)
                    weather[key]['high'] = max(temp)
                    temp = []
                
                for i in range(len(days)):
                    weather[f'day{i}']['date'] = datetime.strptime(days[i], '%Y-%m-%d').strftime('%b. %d')

                return weather

            except Exception as e:
                print(f"forecast weather unexpected response -> {e}")
                return {}