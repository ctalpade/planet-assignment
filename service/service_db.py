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
        grouplist = s.execute(select(Group).options(selectinload(Group.users))).scalars().all()
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
            group = s.execute(select(Group).where(Group.groupname == groupname)).scalars().one_or_none()
            print('group '+str(group))
            if group:
                s.delete(group)
                s.commit()
            else:
                raise Exception('Group does not exist..')
    
    
    @classmethod
    def modifyGroup(cls,groupname,usersInGroup,currentgrp):
        # update group
        with engine.connect() as conn:
            for data in usersInGroup:
                #if new user select * from user where userid = :userid 
                result = conn.execute(text('select * from user where userid = :userid '),[{ 'userid' : data['userid'] }])
                if not any(result):
                    # insert into user , usergroup
                    conn.execute(text('insert into user (userid,first_name,last_name) values (:userid,:first_name,:last_name)')
                                 ,[{ 'userid' : data['userid'],'first_name' : data['first_name'],'last_name' : data['last_name'] }])
                    conn.execute(text('insert into usergroup (userid,groupname) values (:userid,:groupname)')
                                 ,[{ 'userid' : data['userid'],'groupname' : groupname }])
                else:
                    #if existing user 
                    # if not mapped to group insert into usergroup
                    result = conn.execute(text('select * from usergroup where groupname = :groupname and userid = :userid')
                                 ,[{'userid': data['userid'],'groupname': groupname}])
                     
                    if not any(result):
                        conn.execute(text('insert into usergroup (userid,groupname) values (:userid,:groupname)')
                                     ,[{ 'userid' : data['userid'],'groupname' : groupname }])
                        
                     
            conn.commit()

        
            