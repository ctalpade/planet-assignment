from flask import request
from flask_restful import Resource
from flask_restful import marshal_with

from service.service_db import UserService
from resource.resources_jsonify import *



class User(Resource):
        
    def post(self,name=None):
        #default values
        statusmessage = 'User successfully created.'
        statuscode = 201
        
        data = request.get_json(force=True)
        print('Creating User '+str(data))

        #check if duplicate user
        try:
            curruser = UserService.getUserbyId(data['userid']) #[ c for c in userlist if c['userid'] == data['userid'] ]
            if curruser:
                statuscode = 409 # conflict
                statusmessage = 'Duplicate User details. Please fix the data.'
            else:
                UserService.addNewUser(data)
        except Exception as e:
            statusmessage = str(e)
            statuscode = 400
            
        return { 'status' : statusmessage },statuscode

    def delete(self,userid):
        print('delete User '+str(userid))
        #default values
        statusmessage = 'User deleted successfully.'
        statuscode = 200
        try:
            UserService.deleteUser(userid)
        except Exception as e:
            statusmessage = str(e)
            statuscode = 404

        return { 'status' : statusmessage },statuscode
 
 
    def put(self,userid):
        print('Modify User '+str(userid))
        #default values
        statusmessage = 'User modified successfully.'
        statuscode = 200
        try:
            data = request.get_json(force=True)
            if userid != data['userid']:
                raise Exception('Userid in body does not match the userid in url. Please fix data and retry.')
            UserService.modifyUser(userid, data)
        except Exception as e:
            statusmessage = str(e)
            statuscode = 400
        return { 'status' : statusmessage },statuscode
       
    @marshal_with(resource_fields_user) 
    def get(self,userid=None):
        print('get User '+str(userid))
        user = UserService.getUserbyId(userid) if userid else []
        result = user if userid else UserService.getAllUsers()
        return { 'userlist' : result }, 200 if result and any(result) else 404




