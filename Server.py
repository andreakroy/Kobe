from flask import Flask, Response, jsonify, request, abort
from flask_restful import Resource, Api, reqparse
import requests 
import Notification as n
import Alarm as a
import datetime as d
import Reminder as r

app = Flask(__name__)
api = Api(app)

#stores all the notifications on the server
notification_list = []


'''
Method to determine whether or not the same object already exists in the list
    -if the notification does exist on the server, return the index of the object on the server
    -else return -1
'''
def is_unique(notification):
    if not isinstance(notification, n.Notification):
        raise TypeError('Notification parameter must be a notification object')
    for i in range(0, len(notification_list)):
        if notification == notification_list[i]:
            return i
    return -1


'''
GET Request method to return a list of Notifications from the server
    -if no type_in parameter is passed, every notification object is returned as a list of json strings
    -if type_in == Reminder, return all reminders on the server as a list of json strings
    -if type_in == Alarm, return all alarms on the server as a list of json strings
    -else if no parameter is passed, default returns all notifications
    -also can search for events with **alert time** within a range
    -if no start is provided, any notification before the end time is returned
    -if no end is provided, any notification after the start time is returned
    -if no end or start is provided, all notifications are returned
    -also searches by a query string searching the titles or the Notifcations (and the message if type is Reminder)
'''
def get(type_=n.Notification, start=None, end=None, query=None):
    if not isinstance(type_, type):
        raise TypeError('The type_parameter is invalid. type_ must be type object')
    if type_ != n.Notification or type_ != r.Reminder or type_ != a.Alarm:
        raise ValueError('The type_ parameter is invalid. type_ must be Notification, Reminder, or Alarm')
    if start != None and not isinstance(start, d.datetime):
        raise TypeError('The start parameter is invalid. start must be a datetime object')
    if end != None and not isinstance(end, d.datetime):
        raise TypeError('The end parameter is invalid. end must be a datetime object')
    if query != None and not isinstance(query, str):
        raise TypeError('The query parameter is invalid. query must be a string')
    ret = []
    for notification in notification_list:
        if isinstance(notification, type_):
            if start == None or notification.time >= start:
                if end == None or notification.time <= end:
                    if query == None or query in notification.title or (type_ == r.Reminder and query in notification.msg):
                        ret.append(notification.__str__())  
    return ret


'''
GET Request method for an individual reminder
Takes a title and returns the notification objectif it exists
Otherwise throws a ValueError
'''
def reminder_get(title):
    for notification in notification_list:
        if notification.title == title:
            return notification
    raise ValueError(title + " does not exist on the server.")


'''
GET request method for an individual alarm
Takes a time and returns the alarm object if it exists
Otherwise throws a ValueError
'''
def alarm_get(time):
    for alarm in alarm_list:
        if alarm.time == time:
            return alarm
        else:
            raise ValueError('There is no alarm at ' + time.isoformat('-') + ' on the server.')



'''
POST Request method
Takes all the requirements to create a new reminder object and appends the created reminder to notification_list
Otherwise throws a ValueError
'''
def reminder_post(title, msg, start, end):
    new = Notification.Notification(title, msg, start, end)
    print(reminder_is_unique(new))
    if reminder_is_unique(new) == -1:
        notification_list.append(new)
        return new
    else:
        raise ValueError("This event already exists")



'''
POST Request method
Takes all the requirements to create a new alarm object and appends the created alarm to alarm_list
time is passed as a datetime object
Otherwise throws a ValueError
'''
def alarm_post(time, title):
    new = a.Alarm(time, title)
    if alarm_is_unique(new) == -1:
        alarm_list.append(new)
        return new
    else:
        raise ValueError("This alarm already exists")



'''
PUT Request method
Takes a title parameter and all other notifcation parameters are optional
Each parameter which isn't passed remains the same on the server
If the parameter is passed, the field is updated to the parameter
Updates the notifcation with that title
'''
def reminder_put(title, msg, start, end):
    #find the event on the server and update each field with the new parameters
    try:
        update = reminder_get(title)
        if msg != None:
            update.msg = msg
        if start != None:
            update.start = start
        if end != None:
            update.end = end
        return update
    except ValueError:
        raise ValueError('No event with the title ' + title + ' exists on the server.')


'''
PUT Request method
Takes a time parameter and all other alarm parameters are optional
Each parameter which isn't passed remains the same on the server
If the parameter is passed, the field is updated to the parameter
Updates the alarm at that time
'''
def alarm_put(time, title=None):
    #if the reminder is not unique throw exception
    if alarm_is_unique(a.Alarm(time, title)) != -1:
        raise ValueError("This alarm already exists")
    #find the alarm on the server and update each field with the new parameters
    for alarm in alarm_list:
        if time == alarm.time:
            if title != None:
                alarm.title = title
            return alarm
    new = a.Alarm(time, title)   
    alarm_list.append(new)
    return new




'''
DELETE Request method
Takes a reminder and removes it from the server
If the hashed value isn't found on the server, raise an exception
'''
def reminder_delete(title, msg, start, end):
    other = Notification.Notification(title, msg, start, end)
    test = reminder_is_unique(other)
    if test < 0:
        raise ValueError("The object to be deleted is not on the server")
    else:
        ret = notification_list[i]
        del notification_list[i]
        return ret


'''
DELETE Request method
Takes a title and time and removes the object with those properties from the server if it exists
If the alarm isn't found on the server, raise an exception
'''
def alarm_delete(time, title):
    other = a.Alarm(time, title)
    test = alarm_is_unique(other)
    if test < 0:
        raise ValueError("The alarm to be deleted is not on the server")
    else:
        ret = alarm_list[test]
        del alarm_list[test]
        return ret
   




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
            try:
                return reminder_get(request.args['title'])
            except ValueError as e:
                return (str(e), 404)

        else:
            return jsonify(get_all_reminders())
    
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
        try:
            return reminder_post(request.args['title'], request.args['msg'],
                    d.datetime.fromtimestamp((float(request.args['start']))),
                    d.datetime.fromtimestamp((float(request.args['end'])))).get_json()
        except ValueError as e:
            return(str(e), 409)
        except (OverflowError, OSError) as e:
            return (str(e) + ' (start or end parameter is not a valid unix timestamp)', 400)
 
    
    #PUT
    elif request.method == 'PUT':
        if 'title' not in request.args:
            raise TypeError("No title argument was passed")
        par = {}
        if 'msg' in request.args:
            par['msg'] = request.args['msg']
        else:
            par['msg'] = None
        #if start and end times are present change them to datetimes and add to parameter list
        if 'start' in request.args:
            par['start'] = d.datetime.fromtimestamp((float(request.args['start'])))
        else:
            par['start'] = None
        if 'end' in request.args:
            par['end'] = d.datetime.fromtimestamp((float(request.args['end'])))
        else:
            par['end'] = None
        try:
            return reminder_put(request.args['title'], par['msg'], par['start'], par['end']).get_json()
        except ValueError as e:
            return (str(e), 404)
        except (OverflowError, OSError) as e:
            return (str(e) + ' (start or end parameter is not a valid unix timestamp)', 400)
 
    #DELETE
    elif request.method =='DELETE':
        if 'title' not in request.args:
            raise TypeError("No title argument was passed")
        elif 'msg' not in request.args:
            raise TypeError("No message argument was passed")
        elif 'start' not in request.args:
            raise TypeError("No start time argument was passed")
        elif 'msg' not in request.args:
            raise TypeError("No end time argument was passed")
        try:
            return reminder_delete(request.args['title'], d.datetime.fromtimestamp(float(request.args['time']))).get_json()
        except (OverflowError, OSError) as e:
            return (str(e) + ' (start or end parameter is not a valid unix timestamp)', 400)
        except ValueError as e:
            return (str(e), 404)



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
            try:
                alarm_get(d.datetime.fromtimestamp(float(request.args['time']))).get_json()
            except:
                raise TypeError('time parameter must be a unix timestamp')
        else:
            return jsonify(get_all_alarms())
    #POST
    elif request.method == 'POST':
        if 'title' not in request.args:
            raise TypeError("No title argument was passed")
        elif 'time' not in request.args:
            raise TypeError("No time argument was passed")
        try:
            return alarm_post(request.args['title'], d.datetime.fromtimestamp(float(request.args['time']))).get_json()
        except TypeError:
            raise TypeError('time parameter must be a unix timestamp')

    #PUT
    elif request.method == 'PUT':
        if 'time' not in request.args:
            raise TypeError("No time argument was passed")
        try:
            return alarm_put(request.args['title'], d.datetime.fromtimestamp(float(request.args['time']))).get_json()
        except TypeError:
            raise TypeError('time parameter must be a unix timestamp')

 
    #DELETE
    elif request.method =='DELETE':
        if 'title' not in request.args:
            raise TypeError("No title argument was passed")
        elif 'time' not in request.args:
            raise TypeError("No time argument was passed")
        try:
            return alarm_delete(request.args['title'], d.datetime.fromtimestamp(float(request.args['time']))).get_json()
        except TypeError:
            raise TypeError('time parameter must be a unix timestamp')


#DRIVER            
if __name__ == '__main__':
    app.run(debug=True)
