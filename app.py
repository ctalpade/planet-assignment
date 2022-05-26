import os
from flask import Flask 
from flask_restful import Api
from resource.user import User
from resource.group import Group

os.environ['DBPATH']=os.environ.get('DBPATH',os.path.dirname(__file__)) 

app = Flask(__name__)


api = Api(app)

def initDb():
    import os
    if not os.path.exists(os.environ['DBPATH']+'/'+os.environ.get('DBFILENAME','test.db')):
        from db import init
        print('Initializing the db')
        init()
        print('Completed..')
    else:
        print('Using existing db')  

initDb()

api.add_resource(User,
                 '/users/<string:userid>',
                 '/users',endpoint='user')

api.add_resource(Group,
                 '/groups/<string:groupname>',
                 '/groups',endpoint='group')

app.run(host='0.0.0.0',port=5000,debug=True)
