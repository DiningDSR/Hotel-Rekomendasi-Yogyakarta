from bootstrap.app import app 
import os 
import sys 

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app = app

if __name__ == "__main__":
    app.run(debug=True)