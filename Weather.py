import requests
import json

key = '84ab6e41784948bd85e6660fdd342f33'

class Weather:
    
    '''
    A weather object stores the current weather in a particular area
    A weather object is created from the response to a call to the WeatherBit API
    A weather object contains the following fields: city, state, sunrise, sunset, time_last_updated,
            pressure, wind_speed, wind_direction, temperature, feels_like, description,
            precipitation, snowfall, uv_index, aq_index)
        
    '''

    def __init__(self, zip_code):
        r = requests.get('https://api.weatherbit.io/v2.0/current',
                params={'key': key, 'lang': 'en', 'units': 'I', 'postal_code': zip_code})
        ret = (json.loads(r.content)['data'])[0]
        self.city = ret['city_name']
        self.state = ret['state_code']
        self.sunrise = ret['sunrise']
        self.sunset = ret['sunset']
        self.time_last_updated = ret['ts']
        self.pressure = ret['pres']
        self.wind_speed = ret['wind_spd']
        self.wind_direction = ret['wind_cdir']
        self.temperature = ret['temp']
        self.feels_like = ret['app_temp']
        self.description = (ret['weather'])['description']
        self.precipitation = ret['precip']
        self.snowfall = ret['snow']


    '''
    returns a string for text to speech giving a full weather readout
    '''
    def full_weather_readout(self):
        return 'Weather in ' + self.city + ', ' + self.state + ' as of ' + str(self.time_last_updated) + '. ' + self.description + '. Current temperature: ' + str(self.temperature) + ' degrees. Feels like: ' + str(self.feels_like) + ' degrees. Wind Speed: ' + str(self.wind_speed) + ' miles per hour, Wind Direction: ' + str(self.wind_direction) + '. Sunrise: ' + str(self.sunrise) + '. Sunset: ' + str(self.sunset)
