from sqlalchemy import Table, Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db import Base



association_table = Table('usergroup', Base.metadata,
    Column('userid', ForeignKey('user.userid')),
    Column('groupname', ForeignKey('group.groupname'))
)


class User(Base):
    __tablename__ = 'user'
    
    userid = Column(String,primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    
    groups = relationship('Group',secondary=association_table)#,back_populates="users")
    
    def __repr__(self):
        return f"User(userid={self.userid!r},first_name={self.first_name!r},last_name={self.last_name!r},groups={self.groups!r})"
    
    

class Group(Base):
    __tablename__ = 'group'
    
    groupname = Column(String,primary_key=True)
    
    users = relationship('User',secondary=association_table,back_populates="groups",cascade="all")
    
    def __repr__(self):
        return f"Group(groupname={self.groupname!r})"
    



