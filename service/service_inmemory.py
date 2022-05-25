
from model.inmemory import *

class UserService:
    @classmethod
    def getUserbyId(cls,userid):
        filterresult = [ c for c in userlist if c['userid'] == userid ]
        return filterresult
    
    @classmethod
    def getAllUsers(cls,):
        return userlist   
     
    @classmethod
    def addNewUser(cls,data):
        userdict = {'first_name': data['first_name'],'last_name' : data['last_name'],
                     'userid' : data['userid'],'groups' : data['groups'] }
        userlist.append(userdict)
        usermap[userdict['userid']] = userdict
        
        for gname in data['groups']:
            if gname not in grouplist:
                grouplist.append({'name': gname })
    
    @classmethod
    def deleteUser(cls,userid):
        userlist = list(filter(lambda x: x['userid'] != userid,userlist))
        usermap.pop(userid)
    
    
    @classmethod
    def modifyUser(cls,userid,data,olduser):
        userlist.remove(olduser)
        userdict = {'first_name': data['first_name'],'last_name' : data['last_name'],
                     'userid' : data['userid'],'groups' : data['groups'] }
        userlist.append(userdict)
        usermap[userid] = userdict


class GroupService:
    @classmethod
    def getGroupbyId(cls,groupname):
        result = None
        group = [ c for c in grouplist if c['groupname'] == groupname ]
        if any(group):
            usersingroup = [ u for u in userlist if groupname in u['groups'] ]
            result = { 'groupinfo' : {'groupname' : groupname, 'members' : usersingroup } }
        
        return result

    @classmethod
    def getGroupsAllInfo(cls,groupname):
        result = None
        group = [ c for c in grouplist if c['groupname'] == groupname ]
        if any(group):
            usersingroup = [ u for u in userlist if groupname in u['groups'] ]
            result = { 'groupinfo' : {'groupname' : groupname, 'members' : usersingroup } }
        
        return result
    
    @classmethod
    def getAllGroups(cls,):
        return grouplist   
     
    @classmethod
    def addNewGroup(cls,data):
        grouplist.append({'groupname': data['groupname'] })
        
    @classmethod
    def deleteGroup(cls,groupname):
        userlist = list(filter(lambda x: x['groupname'] != groupname,grouplist))
        #usermap.pop(userid)
    
    
    @classmethod
    def modifyGroup(cls,groupname,usersInGroup,currentgrp):
        for u in usersInGroup:
            userdict = usermap.get(u['userid'])
            if userdict:
                userdict['first_name'] = u['first_name']
                userdict['last_name'] = u['last_name']
                if groupname not in userdict.get('groups'):
                    userdict.get('groups').append(groupname)
            else:
                userdict = {'first_name': u['first_name'],'last_name' : u['last_name'],
                                 'userid' : u['userid'],'groups' : [groupname] }
                userlist.append(userdict)
                usermap[u['userid']] = userdict

      