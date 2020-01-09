from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
import requests
import Notification
import datetime

app = Flask(__name__)
api = Api(app)

#stores all the notifications on the server
notification_list = []
notification_list.append(Notification.Notification('a', 'b', 'c', 'd', 'e'))



'''
Method to determine whether or not the same object already exists in the list
Takes a notification object as a parameter and checks the hash code against all
other reminders on the server
If the object is unique, returns -1
If not, returns its index
'''
def is_unique(reminder):
    for i in range(0, len(notification_list)):
        if hash(reminder) == hash(notification_list[i]):
            return i
    return -1



'''
GET Request method to return all notifications on the server as a json 
'''
def get_all():
    ret = []
    for notification in notification_list:
       ret.append(notification.get_json_dict())  
    return jsonify(ret)



'''
GET Request method for an individual reminder
Takes a title and returns the notification object as a json if it exists
Otherwise throws a ValueError
'''
def get(title):
    for notification in notification_list:
        if notification.title == title:
            return notification.get_json()
        else:
            raise ValueError(title + " does not exist on the server.")



'''
POST Request method
Takes all the requirements to create a new notification object and appends the created notification to notification_list
Otherwise throws a ValueError
'''
def post(title, msg, start, end, rpt):
    new = Notification.Notification(title, msg, start, end, rpt)
    if is_unique(new) == -1:
        notification_list.append(new)
        return new.get_json()
    else:
        raise ValueError("This event already exists")



'''
PUT Request method
Takes a title parameter and all other notifcation parameters are optional
Each parameter which isn't passed remains the same on the server
If the parameter is passed, the field is updated to the parameter
Updates the notifcation with that title
'''
def put(title, msg, start, end, rpt):
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
DELETE Request method
Takes a hashed value representing a Notification and removes it from the server
If the hashed value isn't found on the server, raise an exception
'''
def delete(hash_val):
    for i in range(i, len(notification_list)):
        if hash(notification_list[i]) == hash_val:
            ret = notification_list[i]
            del notification_list[i]
            return ret
    raise ValueError("The object to be deleted is not on the server")


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
            return get(request.args['title'])
        else:
            return get_all()
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
        return post(request.args['title'], request.args['msg'], request.args['start'],
                request.args['end'], request.args['rpt'])
    #PUT
    elif request.method == 'PUT':
        if 'title' not in request.args:
            raise TypeError("No title argument was passed")
        return put(request.args['title'], request.args['msg'], request.args['start'],
                request.args['end'], request.args['rpt'])
    #DELETE
    elif request.method =='DELETE':
        if 'title' not in request.args:
            raise TypeError("No title argument was passed")
        return delete(request.args['hash_val'])


#DRIVER            
if __name__ == '__main__':
    app.run(debug=True)
