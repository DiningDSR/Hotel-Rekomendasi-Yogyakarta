import os 
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

class Config(object):
    HOST = 'mongodb+srv://{}:{}@cluster0.a1trg.mongodb.net/{}?retryWrites=true&w=majority'.format(
        str(os.environ.get('USER')),
        str(os.environ.get('PASSWORD')),
        str(os.environ.get('DATABASE'))
    )
    MONGODB_SETTINGS = { 'host': HOST }
    SECRET_KEY = str(os.environ.get('SECRET_KEY'))
    WTF_CSRF_SECRET_KEY = str(os.environ.get('WTF_CSRF_SECRET_KEY'))