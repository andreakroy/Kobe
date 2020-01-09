import requests
import datetime as d
import json
import zipcodes
key = '84ab6e41784948bd85e6660fdd342f33'

class Weather:
    
    '''
    A weather object stores the current weather in a particular area
    A weather object is created from the response to a call to the WeatherBit API
    A weather object contains the following fields: city, state, time_last_updated,
    pressure, wind_speed, wind_direction, temperature, feels_like, description,
    precipitation, snowfall, uv_index, aq_index, humidity
        
    '''

    def __init__(self, zip_code):
        if not zip_code_is_valid(zip_code):
            raise ValueError(zip_code + ' is an invalid zip code.')

        r = requests.get('https://api.weatherbit.io/v2.0/current',
                params={'key': key, 'lang': 'en', 'units': 'I', 'postal_code': zip_code})
        ret = (json.loads(r.content)['data'])[0]
        self.city = ret['city_name']
        self.state = ret['state_code']
        self.zip_code = zip_code
        self.time_last_updated = ret['ts']
        self.pressure = ret['pres']
        self.wind_speed = ret['wind_spd']
        self.wind_direction = ret['wind_cdir_full']
        self.temperature = ret['temp']
        self.feels_like = ret['app_temp']
        self.description = (ret['weather'])['description']
        self.precipitation = ret['precip']
        self.snowfall = ret['snow']
        self.aqi = ret['aqi']
        self.uv = ret['uv']
        self.humidity = ret['rh']
        self.clouds = ret['clouds']


    '''
    returns a string for text to speech giving a full weather readout
    '''
    def full__readout(self):
        return 'Weather in ' + self.city + ' as of ' + str(datetime.fromtimestamp(self.time_last_updated)) + '. ' + self.description + '. Current temperature: ' + str(self.temperature) + ' degrees. Feels like: ' + str(self.feels_like) + ' degrees. Wind Speed: ' + str(self.wind_speed) + ' miles per hour, Wind Direction: ' + str(self.wind_direction) + '. Humidity: ' + str(self.humidity) + '.'


class Weather_Forecast:
    '''
    Holds a weather forecast specific to 6am the next day after the current date and zip code
    Stores date, wind_speed, wind_direction, average temp, high temp, low temp, precipitation probability
    inches of snow, inches of precipitation, pressure, description, cloud coverage, uv index, humidity
    zip_code is a five digit zip code
    date is a valid datetime object
    '''
    def __init__(self, zip_code, date):
        current = d.datetime.now() 
        #throw exception if the date is not a datetime object
        if not isinstance(date, d.datetime):
            raise ValueError('Date parameter muet be a valid datetime object.')
        diff = date - current
        #throw exception uf the difference between the date and current date is less than 0 days
        if diff < d.timedelta(days = 0):
            raise ValueError('Date parameter: ' + str(date) + ' must be after the current date and time.') 
        #if the difference between dae and current date > 0 and < 1, return the current weather
        if diff == d.timedelta(days = 0):
            raise ValueError('Cannot provide a weather forecast for the current day. Check current weather')
        if diff > d.timedelta(days = 16):
            raise ValueError('Date parameter: ' + str(date) + ' must be within 16 days of the ccurrent date.')
        if not zip_code_is_valid(zip_code):
            raise ValueError(zip_code + ' is an invalid zip code.')
        days = diff.days
        
        r = requests.get('https://api.weatherbit.io/v2.0/forecast/daily',
                params={'key': key, 'lang': 'en', 'units': 'I', 'days': days, 'postal_code': zip_code})
        meta = json.loads(r.content)
        #want data from the last day requested
        ret = (meta['data'])[-1]
        self.date = date
        self.city = meta['city_name']
        self.state = meta['state_code']
        self.pressure = ret['pres']
        self.wind_speed = ret['wind_spd']
        self.wind_direction = ret['wind_cdir_full']
        self.average_temperature = ret['temp']
        self.high_temperature = ret['high_temp']
        self.low_temperature = ret['low_temp']
        self.precipitation_prob = ret['pop']
        self.snow = ret['snow']
        self.description = (ret['weather'])['description']
        self.precipitation = ret['precip']
        self.snowfall = ret['snow']
        self.uv = ret['uv']
        self.humidity = ret['rh']
        self.clouds = ret['clouds']
        print(ret)

    '''
    returns a string for text to speech giving a full weather readout
    '''
    def full_readout(self):
        return 'Weather forecast for ' + self.city + ' for the date of ' + self.date.strftime("%A %d. %B %Y") + '. ' + self.description + '. Forecasted average temperature of: ' + str(self.average_temperature) + ' degrees with a high of ' + str(self.high_temperature) + ' degrees and a low of ' + str(self.low_temperature) + ' degrees. Wind Speed: '  + str(self.wind_speed) + ' miles per hour, Wind Direction: ' + str(self.wind_direction) + '. Humidity: ' + str(self.humidity) + ' percent. Chance of Rain: ' + str(self.precipitation_prob) + ' percent.'

 



'''
Checks if a given zip code is valid
'''
def zip_code_is_valid(zip_code):
    x = []
    try: 
        x = zipcodes.matching(zip_code)
        if x == []:
            return False
        else:
            return True
    except ValueError:
        return False
