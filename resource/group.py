from flask import Flask,request
from flask_restful import Resource
from flask_restful import fields, marshal_with
from resource.resources import resource_fields_group

useDB=True

if useDB:
    pass
    from service.service_db import GroupService
else:
    from service.service_inmemory import GroupService
    


class Group(Resource):
    
    def post(self):
        #default values
        statusmessage = 'Group successfully created.'
        statuscode = 200
        
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
        statuscode = 200
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
 
    @marshal_with(resource_fields_group)
    def get(self,groupname):
        print('get Group '+str(groupname))
        result = GroupService.getGroupsAllInfo(groupname)
        return {'grouplist': result }, 200 if result else 404     


    def delete(self,groupname):
        print('Delete Group '+str(groupname))
        #default values
        statusmessage = 'Group updated successfully.'
        statuscode = 200

        GroupService.deleteGroup(groupname) #[ u for u in userlist if groupname in u['groups'] ]
        
        return { 'status' : statusmessage },statuscode    
