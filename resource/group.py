from flask import request
from flask_restful import Resource
from flask_restful import marshal_with

from service.service_db import GroupService
from resource.resources_jsonify import *
    


class Group(Resource):
    
    def post(self):
        #default values
        statusmessage = 'Group successfully created.'
        statuscode = 201
        
        data = request.get_json(force=True)
        print('Creating Group '+str(data))

        #check if duplicate user
        group = GroupService.getGroupbyId(data['groupname']) #[ g for g in grouplist if g['name'] == data['name'] ]
        if group:
            statuscode = 409 # conflict
            statusmessage = 'Duplicate Group details. Please fix the data.'
        else:
            GroupService.addNewGroup(data) #grouplist.append({'name': data['name'] })
         
        return { 'status' : statusmessage },statuscode    

    def put(self,groupname):
        #default values
        statusmessage = 'Group updated successfully.'
        statuscode = 201
        print('Modify User '+str(groupname))
        usersInGroup = request.get_json(force=True)
        #check if duplicate user
        currentgrp = GroupService.getGroupbyId(groupname)
        if currentgrp:
            GroupService.modifyGroup(groupname,usersInGroup,currentgrp)
        else:
            statusmessage = 'Group not found.'
            statuscode = 404

        return { 'status' : statusmessage },statuscode    
 
    def delete(self,groupname):
        print('Delete Group '+str(groupname))
        #default values
        statusmessage = 'Group updated successfully.'
        statuscode = 200
        try:
            GroupService.deleteGroup(groupname)
        except Exception as e:
            statusmessage = str(e)
            statuscode = 400
            
            
        
        return { 'status' : statusmessage },statuscode    

    @marshal_with(resource_fields_group)
    def get(self,groupname=None):
        print('get Group '+str(groupname))
        if groupname:
            result = GroupService.getGroupsAllInfo(groupname)
        else:
            result = GroupService.getAllGroups()
        return {'grouplist': result }, 200 if result and any(result) else 404     
