# DEFINITION
from flask import Flask
from flask_mysqldb import MySQL
from authlib.integrations.flask_client import OAuth
import os
from datetime import timedelta
from auth_decorator import login_required
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# DATABASE CONFIGURATION
app.config['MYSQL_HOST'] = "remotemysql.com"
app.config['MYSQL_USER'] = "xxx"
app.config['MYSQL_PASSWORD'] = "xxx"
app.config['MYSQL_DB'] = "xxx"

mysql = MySQL(app)

# OAUTH CONFIGURATION
app.secret_key = os.getenv("APP_SECRET_KEY")
app.config['SESSION_COOKIE_NAME'] = 'google-login-session'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  
    client_kwargs={'scope': 'openid email profile'},
)

