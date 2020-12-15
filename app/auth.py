# AS simeple as possbile flask google oAuth 2.0
from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
import os
from datetime import timedelta
from __init__ import *

# decorator for routes that should be accessible only by logged in users
from auth_decorator import login_required

# dotenv setup
from dotenv import load_dotenv
load_dotenv()

def login_funct():
    google = oauth.create_client('google')  # create the google oauth client
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

def authorize_funct():
    google = oauth.create_client('google')  # create the google oauth client
    token = google.authorize_access_token()  # Access token from google (needed to get user info)
    resp = google.get('userinfo')  # userinfo contains stuff u specificed in the scrope
    user_info = resp.json()
    user = oauth.google.userinfo()  # uses openid endpoint to fetch user info
    session['profile'] = user_info
    session['token'] = token
    session.permanent = True  # make the session permanant so it keeps existing after broweser gets closed

    # print(session['profile']['email'])
    return redirect('/homepage')

def logout_funct():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/homepage')
