from django.shortcuts import render
from django.http import Http404
from datetime import datetime
from .models import Parks
from django.views.generic import TemplateView
from django.views.generic import CreateView, ListView
from django.conf import settings
from datetime import datetime 
from plotly.graph_objs import Bar
from plotly import offline

# import json to load json data to python dictionary
import json

# import requests to make a request to api
import requests

class HomeView(TemplateView):
    template_name = 'main/index.html'

class ParksCreateView(CreateView):
    model = Parks
    fields = ['title', 'description', 'latitude', 'longitude', 'image']
    success_url = '/parks/'

class ParksListView(ListView):
    model = Parks    
    context_object_name = "parks"

def parks_detail(request, pk):

    try:
        park = Parks.objects.get(pk=pk)

        # Get Current Weather Data
        r = requests.get('http://api.openweathermap.org/data/2.5/weather?lat=' + str(park.latitude) + '&lon=' + str(park.longitude) + '&appid=' + settings.API_KEY + '&units=imperial')
        data = r.json()

        # Get 5 Day Forecast Data
        f = requests.get('http://api.openweathermap.org/data/2.5/forecast?lat=' + str(park.latitude) + '&lon=' + str(park.longitude) + '&appid=' + settings.API_KEY + '&units=imperial')
        fdata = f.json()

        # Access Python dictionary and convert to CDT
        sunrise = data["sys"]["sunrise"] + data["timezone"]
        sunset = data["sys"]["sunset"] + data["timezone"]

        # Format datetime
        m = datetime.fromtimestamp(sunrise).strftime('%I:%M:%S %p %D')
        n = datetime.fromtimestamp(sunset).strftime('%I:%M:%S %p %D')

        # Three Lists
        ftime, ftemp, tooltips = [], [], []

        # Format forecast times
        for forecast in fdata['list']:
            forecast['local_time'] = datetime.fromtimestamp(forecast['dt'] + data['timezone']).strftime('%D %I:%M %p')

            forecast['day_time'] = datetime.fromtimestamp(forecast['dt'] + data['timezone']).strftime('%A %I:%M %p')            

            ftime.append(forecast['day_time'])
            ftemp.append(forecast['main']['temp'])

            tttemp = forecast['main']['temp']
            ttfeels = forecast['main']['feels_like']
            ttdescription = forecast['weather'][0]['description']
            ttwind = forecast['wind']['speed']
            tthumidity = forecast['main']['humidity']

            tooltip = f"Forecasted Conditions: {ttdescription}<br />Temperature: {tttemp}°F<br />Feels Like: {ttfeels}°F<br />Wind Speed: {ttwind} mph<br />Humidity: {tthumidity}%"

            tooltips.append(tooltip)

        vdata = [{
            'type': 'bar',
            'x': ftime,
            'y': ftemp,
            'hovertext': tooltips,
            'marker': {
                'color': 'rgb(252, 111, 54)'
            }
        }]

        vlayout = {
            'title': '5 Day Forecast',
            'xaxis': {'title': 'Time'},
            'yaxis': {'title': 'Temperature (°F)'}
        }

        visual = offline.plot({
            'data': vdata,
            'layout': vlayout,
        }, output_type='div')

        print(fdata)

    except Parks.DoesNotExist:
        raise Http404("Sorry, no park found here.")    

    return render(request, "main/parks_detail.html", {'park':park, 'data':data, 'fdata':fdata, 'm':m, 'n':n, 'visual':visual })   