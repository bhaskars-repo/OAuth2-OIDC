###
# @Author: Bhaskar S
# @Blog:   https://www.polarsparc.com
# @Date:   05 Sep 2020
###

import requests
from flask import Flask, render_template, redirect
from urllib.parse import urlencode

app = Flask(__name__)

OAuthConfig = {
    'tokenURL': 'http://localhost:8080/auth/realms/testing/protocol/openid-connect/token',
    'profileURL': 'http://localhost:8080/auth/realms/testing/protocol/openid-connect/userinfo',
    'logoutURL': 'http://localhost:8080/auth/realms/testing/protocol/openid-connect/logout?'
}

oauth = {
    'flow': 'Client Credentials',
    'session': '',
    'a_token': '',
    'r_token': '',
    't_type': '',
    'scope': '',
    'email': ''
}


def oauth_init():
    oauth['session'] = ''
    oauth['a_token'] = ''
    oauth['r_token'] = ''
    oauth['t_type'] = ''
    oauth['scope'] = ''
    oauth['email'] = ''


@app.route('/')
def login():
    oauth_init()
    return render_template('index2.html', data=oauth)


@app.route('/access_token')
def token():
    data = {
        'client_id': 'test-client',
        'client_secret': 'f7d87a95-604b-4c66-9d60-44c42c91650f',
        'grant_type': 'client_credentials'
    }
    res = requests.post(OAuthConfig['tokenURL'], data=data)
    print(f"Status code: {res.status_code}")
    if res.status_code == 200:
        json = res.json()
        print(f"Received response: {json}")
        oauth['session'] = json['session_state']
        oauth['a_token'] = json['access_token']
        oauth['r_token'] = json['refresh_token']
        oauth['t_type'] = json['token_type']
        oauth['scope'] = json['scope']
    else:
        oauth['a_token'] = '*** FAILED ***'
    return render_template('index2.html', data=oauth)


@app.route('/user_profile')
def profile():
    res = requests.get(OAuthConfig['profileURL'], headers={'Authorization': 'Bearer ' + oauth['a_token']})
    print(f"Status code: {res.status_code}")
    if res.status_code == 200:
        json = res.json()
        print(f"Received response: {json}")
        # Service account - no email
        oauth['email'] = json['preferred_username']
    else:
        oauth['email'] = '*** UNKNOWN ***'
    return render_template('index2.html', data=oauth)


@app.route('/logout')
def logout():
    params = {'redirect_uri': 'http://localhost:5000/'}
    query_str = urlencode(params)
    return redirect(OAuthConfig['logoutURL'] + query_str)


if __name__ == '__main__':
    app.run(debug=True)
