
from authlib.integrations.requests_client import OAuth2Session
from flask import Blueprint, request, session
from flask import render_template, redirect
import json
from .socket import socketio
from .game_logic import *

#Client Information
client_id = "jOto33BdWpYlRO12Jy67S2Y9"
client_secret = "FZ4oSVID2fTAqK1CPoixZSHQTZMlyV0ubK9FD9wQqU75Aqpj"
scope = ['indicators','update_indicators']
authorize_url = "http://127.0.0.1:5000/rm/oauth/authorize"
token_url = "http://127.0.0.1:5000/rm/oauth/token"

#Current Oauth2 Sessions
session_list = {}

#Authblib Client Session Wrapper
class oauth2_session:

    def __init__(self,client_id,client_secret,scope,authorization_endpoint,token_endpoint):
        self.client = OAuth2Session(client_id, client_secret, scope=scope)
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope
        self.authorization_endpoint = authorization_endpoint
        self.token_endpoint = token_endpoint
    
    def create_authorization_url(self):
        uri,self.state = self.client.create_authorization_url(self.authorization_endpoint)
        return uri
    
    def fetch_token(self,authorization_response):
        return self.client.fetch_token(self.token_endpoint, authorization_response=authorization_response)
    
    def revoke_token(self,url,token):
        return self.client.revoke_token(url, token=token)

    def save_token(self,token):
        self.token = token

    def get(self,url):
        return self.client.get(url)
    
    def post(self,url,body):
        return self.client.post(url, json=body)

#Game User Class used for matchmaking
class game_user:
    def __init__(self,user,game,skill_preference,behaviour_preference,indicators):
        self.user = user
        self.game = game
        self.skill = int(indicators['skill'].split("/")[0])
        self.skill_bin = int(indicators['skill'].split("/")[1])
        self.behaviour = int(indicators['behaviour'].split("/")[0])
        self.behaviour_bin = int(indicators['behaviour'].split("/")[1])
        self.skill_preference = int(skill_preference)
        self.behaviour_preference = int(behaviour_preference)
    
    def __str__(self):
        return str(self.user) + "|" + str(self.game) + "|" + str(self.skill) + "|" + str(self.behaviour) + '|' + str(self.skill_bin) + '|' + str(self.skill_bin) + "|" + str(self.skill_preference) + "|" + str(self.behaviour_preference)


tm_bp = Blueprint('tm', __name__)

@tm_bp.route('/', methods=['GET'])
def home():
    return render_template('game_selection.html')

@tm_bp.route('/tm/callback', methods=('GET',))
def callback():
    #Fetch Access token
    token = session_list[session['username']].fetch_token(request.url)
    #Save Access token
    session_list[session['username']].save_token(token)
    return redirect('/tm/game')
    
@tm_bp.route('/tm/game', methods=('GET', 'POST'))
def game():
    #Fetch Indicators
    indicators = session_list[session['username']].get('http://127.0.0.1:5000/rm/users_reputation?game={}&bins={}'.format(session['game'],session['bins'])).json()
    user = game_user(session['username'], session['game'],session['skill_preference'],session['behaviour_preference'],indicators)
    #Matchmaking Logic
    room = checkMatchups(user)
    printRoomList()
    #If room is full
    if room[1]:
        #Generate random outcome
        result = mm(room)
        #Emit result to players
        socketio.emit(room[0]['id'],(str(json.dumps(result)),session['game']))
        #For each user update indicators and revoke access token
        for username in result:
            payload = {
                'result':result[username],
                'game':session['game']
            }
            session_list[username].post('http://127.0.0.1:5000/rm/update_indicators',json.dumps(payload))
            session_list[username].revoke_token("http://127.0.0.1:5000/rm/oauth/revoke",session_list[username].token['access_token'])
            del session_list[username]
        return render_template('result.html',state="True",username=session['username'], result=str(json.dumps(result)), game=session['game'] , room=room[0]['id'], )
    else:
        return render_template('result.html',state="False",username=session['username'], result="", game="" , room=room[0]['id'])

@tm_bp.route('/tm/start_game', methods=['GET'])
def startGame():
    session['game'] = request.args.get("game")
    username = request.args.get("username")
    #Verify if the gamer tag already exists
    if(username in session_list):
        return redirect("/?error='username'","302")
    session['username'] = username
    session['skill_preference'] = request.args.get("skill_pref")
    session['behaviour_preference'] = request.args.get("behaviour_pref")
    session['bins'] = request.args.get("bins")
    #Create oauth2_session for the new player.
    session_list[username] = oauth2_session(client_id,client_secret,scope,authorize_url,token_url)
    #Redirect to authorization url
    return redirect(session_list[username].create_authorization_url(), code=302)




