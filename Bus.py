import requests as r

key = 'b853288713ca475c8f71169a57266915'
base_url = 'https://developer.cumtd.com/api/2.2/json' 

'''
Stop object stores:
    -Name
    -Dictionary with string key bus name, and value is a list of datetimes of the next 10 buses of that type
'''
class Stop:
    def __int__(self, name, buses):
        self.name = name
        self.buses = buses
    '''
    gets the earliest bus of a given name at the given stop
    returns a datetime object
    '''
    def get_earliest_bus(self, name):
        x = r.get(base_url + '/getdeparturesbystop', params = {'key': key, 'stop_id': 'IT', count : '5'}).text
        print(x)
    def update(self):
        print('update')
