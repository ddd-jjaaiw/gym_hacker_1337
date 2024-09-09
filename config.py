import uuid 

class config():
    SQLALCHEMY_DATABASE_URI='sqlite:///./db.sqlite'
    SECRET_KEY =  uuid.uuid4().hex
    SQLALCHEMY_TRACK_MODIFICATIONS = False
