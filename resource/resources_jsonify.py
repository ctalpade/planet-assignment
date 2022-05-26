from flask_restful import fields

resource_user1 = {
    'first_name':   fields.String,
    'last_name':   fields.String,
    'userid':   fields.String,
}

resource_group1 = {
    'groupname' : fields.String
}


resource_group = {
    'groupname' : fields.String,
    'users' : fields.List(fields.Nested(resource_user1))
    }

resource_user = {
    'first_name':   fields.String,
    'last_name':   fields.String,
    'userid':   fields.String,
    'groups' : fields.List(fields.Nested(resource_group1))
}


resource_fields_user = {
    'userlist' : fields.List(fields.Nested(resource_user)),
}

resource_fields_group = {
    'grouplist' : fields.List(fields.Nested(resource_group)),
}
