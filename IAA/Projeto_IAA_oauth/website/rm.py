import math
import json
import re
import requests
from flask import Blueprint, request, session
from flask import render_template, redirect
from authlib.integrations.flask_oauth2 import current_token
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from .database import query, commit, current_user
from .oauth2 import query_client, save_token
from authlib.integrations.flask_oauth2 import (
    AuthorizationServer,
    ResourceProtector
)

#CMD Client Information
client_id="9113170755799990166"
scopes = "http://interop.gov.pt/MDC/Cidadao/NIC"
redirect_uri = "http://127.0.0.1:5000/rm/callback"

#Authlib Authorization Server
authorization = AuthorizationServer(
    query_client=query_client,
    save_token=save_token,
)

#Authlib Resource Server
require_oauth = ResourceProtector() 

#RM Endpoints
rm_bp = Blueprint('rm', __name__)

@rm_bp.route('/rm/authCMD', methods=['GET'])
def authorize_CMD():
    auth_req = "https://preprod.autenticacao.gov.pt/oauth/askauthorization?redirect_uri={}&client_id={}&scope={}&response_type=token"
    return redirect(auth_req.format(redirect_uri,client_id,scopes), code=302)

@rm_bp.route('/rm/callback', methods=('GET', 'POST'))
def callback():
    #If the access token is in the uri fragment, redirect to the access_token_fetch.html
    if '?access_token' not in request.url :
        return render_template('access_token_fetch.html')
    
    access_token = re.search('\?access_token=(.+?)(?=&)',request.url).groups()[0]
    body = {'token':access_token,'attributesName':[scopes]}
    
    token_context = requests.post("https://preprod.autenticacao.gov.pt/oauthresourceserver/api/AttributeManager",data=body)

    api = 'https://preprod.autenticacao.gov.pt/oauthresourceserver/api/AttributeManager?token={}&authenticationContextId={}'
    
    token_context_json = token_context.json()

    api_request_url = api.format(token_context_json['token'],token_context_json['authenticationContextId'])
    attributes_req = requests.get(api_request_url)
    
    attr_val = [a['value'] for a in attributes_req.json() if a['name'] == "http://interop.gov.pt/MDC/Cidadao/NIC"]
    
    #NIC Tranformation with PBKDF2HMAC
    kdf = PBKDF2HMAC(algorithm=hashes.SHA1(),length=16,salt=str.encode("IAA"),iterations=50000)
    NIC = kdf.derive(str.encode(attr_val[0]))
    
    session['NIC'] = NIC
    check_user = "SELECT id FROM user where cmd_id = ?"
    number = query(check_user, (session['NIC'],))

    #If user not in database, then reditect to register webpage, else login
    if number == []:
        return redirect("/rm/register_cmd", code=302)
    session['id'] = number[0][0]
    return redirect(session['authUrl'], code=302)
    
@rm_bp.route('/rm/register_cmd', methods=('GET', 'POST'))
def register():

    if request.method == 'GET':
        return render_template('register.html')
    
    username = request.form.get('username')
    password = request.form.get('password')
    check_user = "SELECT id FROM user where cmd_id = ?"
    number = query(check_user, (session['NIC'],))
    
    if number == []:
        #Password Tranformation with PBKDF2HMAC
        kdf = PBKDF2HMAC(algorithm=hashes.SHA1(),length=16,salt=str.encode("IAA"),iterations=50000)
        password = kdf.derive(str.encode(password))
        queryString = "INSERT INTO user(username,password,cmd_id) VALUES (?,?,?) "
        values = (username,password,session['NIC'])
        query(queryString, values)
        commit()
    
    check_user = "SELECT id FROM user where cmd_id = ?"
    number = query(check_user, (session['NIC'],))
    if number != []:
        session['id'] = number[0][0]
    
    #Redirect back to authortization endpoint
    return redirect(session['authUrl'], code=302)

@rm_bp.route('/rm/login', methods=('GET', 'POST'))
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    #Get credentials from login page
    username = request.form.get('username')
    password = request.form.get('password')

    #Transform the password to comapare with database
    kdf = PBKDF2HMAC(algorithm=hashes.SHA1(),length=16,salt=str.encode("IAA"),iterations=50000)
    password = kdf.derive(str.encode(password))

    #Get the user with corresponding username and password
    user = query("SELECT id from user where username = ? and password = ?;",(username,password,))
    
    #If the user exists redirect back to the authorization URL
    if user != []:
        session['id'] = user[0][0] 
        return redirect(session['authUrl'], code=302)
    
    #If the user does not exist reditect back to the login page
    return redirect('/rm/login')

@rm_bp.route('/rm/preferences',methods=('POST','GET'))
def change_prefences():

    user = current_user()
    # if user login status is not true (Auth server), then to log it in
    if not user:
        session['authUrl'] = request.url
        return redirect('/rm/authCMD',code=302)
    
    # If the user is not logged in with CMD
    if user.get_cmd_id() == None:
        session['authUrl'] = request.url
        return redirect('/rm/authCMD',code=302)

    if request.method == 'GET':
        session['callback'] = request.args.get("callback")
        return render_template('change_preferences.html')
    
    #Alter password
    password = request.form.get('password')
    kdf = PBKDF2HMAC(algorithm=hashes.SHA1(),length=16,salt=str.encode("IAA"),iterations=50000)
    password = kdf.derive(str.encode(password))
    query("UPDATE user SET password = ? WHERE id = ?",(password,user.id))
    commit()
    
    return redirect(session['callback'],code=302)

@rm_bp.route('/rm/logout')
def logout():
    del session['id']
    return redirect('/')

@rm_bp.route('/rm/oauth/authorize', methods=['GET', 'POST'])
def authorize():
    
    user = current_user()
    # if user login status is not true (Auth server), then to log it in
    if not user:
        session['authUrl'] = request.url
        return redirect('/rm/login',code=302)

    if request.method == 'GET':
        return render_template('authorize_v2.html', user=user)
        
    grant_user = user
    
    #Generate authorization response
    return authorization.create_authorization_response(grant_user=grant_user)


@rm_bp.route('/rm/oauth/token', methods=['POST'])
def issue_token():
    #Generate token response
    return authorization.create_token_response()


@rm_bp.route('/rm/oauth/revoke', methods=['POST'])
def revoke_token():
    #Revoke access token
    return authorization.create_endpoint_response('revocation')

@rm_bp.route('/rm/update_indicators', methods=['POST'])
@require_oauth('update_indicators')
def update_indicators():
    #Parse result
    result = request.get_json()
    result = json.loads(result)
    access = current_token.get_access_token()

    #Get user from access token
    user = query("Select user_id from oauth2_token where access_token = ? ", (access,))
    if access == []:
        return None
    
    get = "Select skill,behaviour from Games WHERE user_id = ? and game = ?"
    update = "UPDATE Games SET skill = ?, behaviour = ? WHERE user_id = ? and game = ?"
    
    current_info = query(get, (user[0][0], result['game']))
    skill = current_info[0][0]
    behaviour = current_info[0][1]

    #Indicators update logic
    if result['result'] == "win":
        skill = skill + 1
        behaviour = behaviour + 1
    
    if result['result'] == "lost":
        if skill > 0:
            skill = skill - 1
        behaviour = behaviour + 1

    if result['result'] == "quit" or result['result'] == "cheating":
        if behaviour > 0:
            behaviour = behaviour - 1

    query(update, (skill,behaviour,user[0][0], result['game']))
    commit()

    return "Indicators Updated"

@rm_bp.route('/rm/users_reputation')
@require_oauth('indicators')
def users_reputation():
    game = request.args.get("game")
    bins = int(request.args.get("bins"))
    #Set max number of bins
    if bins > 10 :
        bins = 10
    access = current_token.get_access_token()
    
    #Get user from access token
    user = query("Select user_id from oauth2_token where access_token = ? ", (access,))
    if access == []:
        return None
    
    #Check if games exist and create database entry
    check_game = query("Select * from Games where user_id = ? and game = ?" , (user[0][0], game))
    if check_game == []:
        query("insert into Games(game,skill,behaviour,user_id) values(?,?,?,?)",(game,0,0,user[0][0]))
        commit()
    
    all_skill = query("Select skill from Games where game = ?" , (game,))
    all_skill_sorted = sorted([entry[0] for entry in all_skill], reverse=True)
    
    all_behaviour = query("Select behaviour from Games where game = ?" , (game,))
    all_behaviour_sorted = sorted([entry[0] for entry in all_behaviour], reverse=True)

    user_skill_bins_preferences = query("Select skill,behaviour from Games where user_id = ? and game = ?" , (user[0][0], game))
    
    if user_skill_bins_preferences == []:
        return None

    user_skill = user_skill_bins_preferences[0][0]
    user_behavior = user_skill_bins_preferences[0][1]

    #Calculate skill and behaviour bin
    interval_skill = len(all_skill_sorted) / bins
    interval_behaviour = len(all_behaviour_sorted) / bins
    
    position_skill = all_skill_sorted.index(user_skill) + 1
    position_behaviour = all_behaviour_sorted.index(user_behavior) + 1

    bin_skill = math.ceil(position_skill / interval_skill)
    bin_behaviour = math.ceil(position_behaviour / interval_behaviour)
   
    value = {
        'skill': '{}/{}'.format(bin_skill,bins),
        'behaviour': '{}/{}'.format(bin_behaviour,bins)
    }
    
    return json.dumps(value)
