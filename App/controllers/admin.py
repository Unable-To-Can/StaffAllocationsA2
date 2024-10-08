from App.models.admin import *
from App.models.user import *

def create_admin(username, password):
    newAdmin= Admin(username=username, password=password)
    db.session.add(newAdmin)
    db.session.commit()
    return newAdmin