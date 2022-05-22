# from app.controllers.usermanagement import user
from app.controllers.data_management import dataManager

def register(app):
    # app.register_blueprint(user, url_prefix="/")
    app.register_blueprint(dataManager, url_prefix="/")