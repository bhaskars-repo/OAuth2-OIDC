###
# @Author: Bhaskar S
# @Blog:   https://www.polarsparc.com
# @Date:   26 Apr 2025
###

import requests
from flask import Flask, render_template, redirect, request
from urllib.parse import urlencode

app = Flask(__name__)

OAuthConfig = {
    'authURL': 'http://localhost:8080/realms/testing/protocol/openid-connect/auth?',
    'tokenURL': 'http://localhost:8080/realms/testing/protocol/openid-connect/token',
    'profileURL': 'http://localhost:8080/realms/testing/protocol/openid-connect/userinfo',
    'logoutURL': 'http://localhost:8080/realms/testing/protocol/openid-connect/logout?'
}

oauth = {
    'code': '',
    'state': '',
    'session': '',
    'a_token': '',
    'r_token': '',
    't_type': '',
    'scope': '',
    'email': ''
}

def oauth_init():
    oauth['code'] = ''
    oauth['state'] = ''
    oauth['session'] = ''
    oauth['a_token'] = ''
    oauth['r_token'] = ''
    oauth['t_type'] = ''
    oauth['scope'] = ''
    oauth['email'] = ''

@app.route('/')
def login():
    oauth_init()
    return render_template('index.html', data=oauth)

@app.route('/auth_code')
def authenticate():
    params = {'client_id': 'test-client',
              'response_type': 'code',
              'redirect_uri': 'http://localhost:5000/callback',
              'scope': 'openid'}
    query_str = urlencode(params)
    print(f"Ready to redirect to URL: {OAuthConfig['authURL'] + query_str}")
    return redirect(OAuthConfig['authURL'] + query_str, 302)

@app.route('/callback')
def callback():
    oauth['code'] = request.args.get('code')
    oauth['session'] = request.args.get('session_state')
    print(f"Received code: {oauth['code']}, session: {oauth['session']}, state: {request.args.get('state')}")
    return render_template('index.html', data=oauth)

@app.route('/access_token')
def token():
    data = {
        'client_id': 'test-client',
        'grant_type': 'authorization_code',
        'code': oauth['code'],
        'client_secret': 'g9YAmxsqegIvI1c4Bxsn3z949vcGsIf6',
        'redirect_uri': 'http://localhost:5000/callback'
    }
    res = requests.post(OAuthConfig['tokenURL'], data=data)
    print(f"Access Token - Status code: {res.status_code}")
    if res.status_code == 200:
        json = res.json()
        print(f"Received response: {json}")
        oauth['a_token'] = json['access_token']
        oauth['r_token'] = json['refresh_token']
        oauth['t_type'] = json['token_type']
        oauth['scope'] = json['scope']
    else:
        oauth['a_token'] = '*** FAILED ***'
    return render_template('index.html', data=oauth)

@app.route('/user_profile')
def profile():
    res = requests.get(OAuthConfig['profileURL'], headers={'Authorization': 'Bearer ' + oauth['a_token']})
    print(f"User Profile - Status code: {res.status_code}")
    if res.status_code == 200:
        json = res.json()
        print(f"Received response: {json}")
        oauth['email'] = json['email']
    else:
        oauth['email'] = '*** UNKNOWN ***'
    return render_template('index.html', data=oauth)

@app.route('/logout')
def logout():
    params = {'redirect_uri': 'http://localhost:5000/'}
    query_str = urlencode(params)
    return redirect(OAuthConfig['logoutURL'] + query_str)

if __name__ == '__main__':
    app.run(debug=True)
