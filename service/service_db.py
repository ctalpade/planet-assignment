
from model.inmemory import *
from model.allmodels import Group,User
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy import text


from db import engine

class UserService:
    @classmethod
    def getUserbyId(cls,userid):
        user = None
        with Session(engine) as s:
            user = s.execute(select(User).where(User.userid == userid)).scalars().one_or_none()
        return user
    
    @classmethod
    def getAllUsers(cls,):
        userlist = None
        with Session(engine) as s:
            userlist = s.execute(select(User).options(selectinload(User.groups))).scalars().all()
        return userlist   
     
    @classmethod
    def addNewUser(cls,data):
        u = User(userid=data['userid'],first_name=data['first_name'],last_name=data['last_name'])
        with Session(engine) as s:
            for g in data['groups']:
                grp =  GroupService.getGroupbyId(g)
                if grp:
                    s.add(grp)
                    if grp:
                        grp.users.append(u)
                        s.add(u)
                else:
                    raise Exception('Create Group before you assign User..')
                    
            s.commit()
        
            
    
    @classmethod
    def deleteUser(cls,userid):
        user = None
        with Session(engine) as s:
            user = s.execute(select(User).where(User.userid == userid)).scalars().one_or_none()
                
            if user:
                s.delete(user)
                s.commit()
            else:
                raise Exception('User does not exist. Please check..')
            
    @classmethod
    def modifyUser(cls,userid,data):
        # update user
        with engine.connect() as conn:
            conn.execute(text('update user set first_name = :first_name , last_name = :last_name where userid = :userid ')
                            ,[{'first_name' : data['first_name'], 'last_name' : data['last_name'] , 'userid' : userid }])

            conn.execute(text('delete from usergroup where userid = :userid'),[{'userid': userid}])
            for g in data['groups']:
                grp = GroupService.getGroupbyId(g)
                if grp:
                    conn.execute(text('insert into usergroup (userid,groupname) values (:userid,:group_name) ')
                                ,[{'group_name' : g , 'userid' : data['userid'] }])
                else:
                    raise Exception('Group does not exist. Please fix the data and try again '+str(g))
            
            conn.commit()
        # update usergroup 


class GroupService:
    @classmethod
    def getGroupbyId(cls,groupname):
        group = None
        with Session(engine) as s:
            group = s.execute(select(Group).where(Group.groupname == groupname)).scalars().one_or_none()
            print('group '+str(group))

        return group
    

    @classmethod
    def getGroupsAllInfo(cls,groupname):
        group = None
        with Session(engine) as s:
            group = s.execute(select(Group).options(selectinload(Group.users)).where(Group.groupname == groupname)).scalars().one_or_none()
            print('group '+str(group))

        return group
    
    @classmethod
    def getAllGroups(cls,):
        s = Session(engine)
        grouplist = s.execute(select(Group)).scalars().all()
        return grouplist   
     
    @classmethod
    def addNewGroup(cls,data):
        g = Group(groupname=data['groupname'])
        s = Session(engine)
        s.add(g)
        s.commit()
        
        
    @classmethod
    def deleteGroup(cls,groupname):
        with Session(engine) as s:
            group = s.execute(select(Group).where(Group.groupname == groupname)).scalars().one()
            print('group '+str(group))
            s.delete(group)
            s.commit()
    
    
    @classmethod
    def modifyGroup(cls,groupname,usersInGroup,currentgrp):
        
        with Session(engine) as s:
            group = s.execute(select(Group).where(Group.groupname == groupname)).scalars().one()
            print('group '+str(group))
            for data in usersInGroup:
                group.users.append(User(userid=data['userid'],first_name=data['first_name'],last_name=data['last_name']))
    
            s.add(group)
            s.commit()
            