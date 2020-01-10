from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
import requests
import Notification
import Alarm as a
import datetime

app = Flask(__name__)
api = Api(app)

#stores all the notifications on the server
notification_list = []
#stores all the alarms on the server
alarm_list = []
notification_list.append(Notification.Notification('a', 'b', 'c', 'd', 'e'))



'''
Method to determine whether or not the same object already exists in the list
Takes a notification object as a parameter and checks the hash code against all
other reminders on the server
If the object is unique, returns -1
If not, returns its index
'''
def reminder_is_unique(reminder):
    for i in range(0, len(notification_list)):
        if hash(reminder) == hash(notification_list[i]):
            return i
    return -1

'''
Method to check whther or not the same object already exists in the list
Takes an alarm object as a parameter and checks the hash code
against all other alarms on the server
If the object is unique, returns -1
Else returns the index of the duplicate object on the server
'''
def alarm_is_unique(alarm):
    for i in range(0, len(alarm_list)):
        if hash(reminder) == hash(notigication_list[i]):
            return i
    return -1

'''
GET Request method to return all notifications on the server as a json 
'''
def get_all_reminders():
    ret = []
    for notification in notification_list:
       ret.append(notification.get_json_dict())  
    return jsonify(ret)

'''
GET Request method to return all alarms on the server as a json
'''
def get_all_alarms():
    ret = []
    for alarm in alarm_list:
       ret.append(alarm.get_json_dict())  
    return jsonify(ret)

'''
GET Request method for an individual reminder
Takes a title and returns the notification object as a json if it exists
Otherwise throws a ValueError
'''
def reminder_get(title):
    for notification in notification_list:
        if notification.title == title:
            return notification.get_json()
        else:
            raise ValueError(title + " does not exist on the server.")


'''
GET request method for an individual alarm
Takes a time and returns the alarm object as a json if it exists
Otherwise throws a ValueError
'''
def alarm_get(time):
    for alarm in alarm_list:
        if alarm.time == time:
            return alarm.get_json()
        else:
            raise ValueError('There is no alarm at ' + time.strftime('%A %d. %B %&') + ' on the server.')



'''
POST Request method
Takes all the requirements to create a new reminder object and appends the created reminder to notification_list
Otherwise throws a ValueError
'''
def reminder_post(title, msg, start, end, rpt):
    new = Notification.Notification(title, msg, start, end, rpt)
    if reminder_is_unique(new) == -1:
        notification_list.append(new)
        return new.get_json()
    else:
        raise ValueError("This event already exists")



'''
POST Request method
Takes all the requirements to create a new alarm object and appends the created alarm to alarm_list
Otherwise throws a ValueError
'''
def alarm_post(title, time):
    new = a.Alarm(title, time)
    if alarm_is_unique(new) == -1:
        alarm_list.append(new)
        return new.get_json()
    else:
        raise ValueError("This alarm already exists")



'''
PUT Request method
Takes a title parameter and all other notifcation parameters are optional
Each parameter which isn't passed remains the same on the server
If the parameter is passed, the field is updated to the parameter
Updates the notifcation with that title
'''
def reminder_put(title, msg, start, end, rpt):
    #if the reminder is not unique throw exception
    if is_unique(Notification.Notification(title, msg, start, end, rpt)) != -1:
        raise ValueError("This event already exists")
    #find the event on the server and update each field with the new parameters
    for notification in notification_list:
        if title == notification.title:
            if msg != None:
                notification.msg = msg
            if start != None:
                notification.start = start
            if end != None:
                notification.end = end
            if rpt != None:
                notification.rpt = rpt
            return notification.get_json()
    new = Notification.Notification(title, msg, start, end, rpt)   
    notification_list.append(new)
    return new




'''
PUT Request method
Takes a time parameter and all other alarm parameters are optional
Each parameter which isn't passed remains the same on the server
If the parameter is passed, the field is updated to the parameter
Updates the alarm at that time
'''
def alarm_put(title, time):
    #if the reminder is not unique throw exception
    if is_unique(a.Alarm(title, time)) != -1:
        raise ValueError("This alarm already exists")
    #find the alarm on the server and update each field with the new parameters
    for alarm in alarm_list:
        if time == alarm.time:
            if title != None:
                alarm.title = title
            return alarn.get_json()
    new = a.Alarm(title, time)   
    alarm_list.append(new)
    return new




'''
DELETE Request method
Takes a hashed value representing a Notification and removes it from the server
If the hashed value isn't found on the server, raise an exception
'''
def reminder_delete(hash_val):
    for i in range(i, len(notification_list)):
        if hash(notification_list[i]) == hash_val:
            ret = notification_list[i]
            del notification_list[i]
            return ret
    raise ValueError("The object to be deleted is not on the server")



'''
DELETE Request method
Takes a hashed value representing an alarm and removes it from the server
If the hashed value isn't found on the server, raise an exception
'''
def alarm_delete(hash_val):
    for i in range(i, len(alarm_list)):
        if hash(alarm_list[i]) == hash_val:
            ret = alarm_list[i]
            del alarm_list[i]
            return ret
    raise ValueError("The alarm to be deleted is not on the server")




#define url routing
@app.route('/reminders', methods=['GET', 'POST', 'PUT', 'DELETE'])
def reminders():
    #GET
    '''
    if a title argument is passed get the notification with that title if it exists
    else get a json with every notification on the server
    '''
    if request.method == 'GET':
        if 'title' in request.args:
            return reminder_get(request.args['title'])
        else:
            return get_all_reminders()
    #POST
    elif request.method == 'POST':
        if 'title' not in request.args:
            raise TypeError("No title argument was passed")
        elif 'msg' not in request.args:
            raise TypeError("No msg argument was passed") 
        elif 'start' not in request.args:
            raise TypeError("No start argument was passed")
        elif 'end' not in request.args:
            raise TypeError("No end argument was passed")
        elif 'rpt' not in request.args:
            raise TypeError("No rpt argument was passed")   
        return reminder_post(request.args['title'], request.args['msg'], request.args['start'],
                request.args['end'], request.args['rpt'])
    #PUT
    elif request.method == 'PUT':
        if 'title' not in request.args:
            raise TypeError("No title argument was passed")
        return reminder_put(request.args['title'], request.args['msg'], request.args['start'],
                request.args['end'], request.args['rpt'])
    #DELETE
    elif request.method =='DELETE':
        if 'hash_val' not in request.args:
            raise TypeError("No hash value was passed")
        return reminder_delete(request.args['hash_val'])


#define url routing
@app.route('/alarms', methods=['GET', 'POST', 'PUT', 'DELETE'])
def alarms():
    #GET
    '''
    return the alarm object represented by the alarm time if a datetime is supplied    
    else return a json with all alarms on the server
    '''
    if request.method == 'GET':
        if 'time' in request.args:
            return alarm_get(request.args['time'])
        else:
            return get_all_alarms()
    #POST
    elif request.method == 'POST':
        if 'title' not in request.args:
            raise TypeError("No title argument was passed")
        elif 'time' not in request.args:
            raise TypeError("No time argument was passed")    
        return alarm_post(request.args['title'], request.args['title'])

    #PUT
    elif request.method == 'PUT':
        if 'time' not in request.args:
            raise TypeError("No time argument was passed")
        return reminder_put(request.args['title'], request.args['time'])

    #DELETE
    elif request.method =='DELETE':
        if 'hash_val' not in request.args:
            raise TypeError("No hash value was passed")
        return reminder_delete(request.args['hash_val'])








#DRIVER            
if __name__ == '__main__':
    app.run(debug=True)
