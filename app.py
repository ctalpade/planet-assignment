from flask import Flask,request,jsonify 
from flask_restful import Resource,Api
from flask_restful import fields, marshal_with 

from resource.user import User
from resource.group import Group


app = Flask(__name__)


api = Api(app)

  

'''
{
"first_name": "Joe",
"last_name": "Smith",
"userid": "jsmith",
"groups": ["admins", "users"]
}
'''



api.add_resource(User,
                 '/users/<string:userid>',
                 '/users',endpoint='user')

api.add_resource(Group,
                 '/groups/<string:groupname>',
                 '/groups',endpoint='group')

app.run(port=5000,debug=True)
