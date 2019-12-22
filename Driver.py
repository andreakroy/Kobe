import requests
import Notification
import Server

response = requests.get('http://127.0.0.1:5000/reminders')
response1 = requests.post('http://127.0.0.1:5000/reminders', params={'title': 'f', 'msg': 'g', 'start': 'h', 'end': 'i', 'rpt': 'k'}) 
response2 = requests.get('http://127.0.0.1:5000/reminders')
response3 = requests.put('http://127.0.0.1:5000/reminders', params={'title': 'f', 'msg': 'g', 'start': 'i', 'end': 'j', 'rpt': 'l'})
response4 = requests.get('http://127.0.0.1:5000/reminders')
print(response.text)
print(response2.text)
print(response4.text)
