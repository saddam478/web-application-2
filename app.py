from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
import os
from aws_lambda_web_adapter.frameworks.flask import ProxyEvent

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secure random key in production

oauth = OAuth(app)

oauth.register(
    name='oidc',
    authority='https://cognito-idp.ap-south-1.amazonaws.com/ap-south-1_Y36019795',
    client_id='16evn7ec0mirhlhms2ciul61nb',
    client_secret=os.getenv('COGNITO_CLIENT_SECRET'),
    server_metadata_url='https://cognito-idp.ap-south-1.amazonaws.com/ap-south-1_Y36019795/.well-known/openid-configuration',
    client_kwargs={'scope': 'email openid phone'}
)

@app.route('/')
def index():
    user = session.get('user')
    if user:
        return f'Hello, {user["email"]}. <a href="/logout">Logout</a>'
    else:
        return 'Welcome! Please <a href="/login">Login</a>.'

@app.route('/login')
def login():
    return oauth.oidc.authorize_redirect('https://web-app-bucket123.s3.ap-south-1.amazonaws.com/logged_in.html')

@app.route('/authorize')
def authorize():
    token = oauth.oidc.authorize_access_token()
    user = token['userinfo']
    session['user'] = user
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

def lambda_handler(event, context):
    proxy_event = ProxyEvent(event)
    return proxy_event.transform_response(app)
