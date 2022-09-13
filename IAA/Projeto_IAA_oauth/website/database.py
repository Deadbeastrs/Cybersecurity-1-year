import time
import secrets
import json
import sqlite3
import threading
from flask import session
from authlib.oauth2.rfc6749 import ClientMixin
from authlib.oauth2.rfc6749 import (
    TokenMixin,
    AuthorizationCodeMixin,
)
from authlib.oauth2.rfc6749.util import scope_to_list, list_to_scope

lock = threading.Lock()

#Get current user via session
def current_user():
    if 'id' in session:
        uid = session['id']
        ans = query("SELECT id from user where id = ?;",(uid,))[0]
        user = User(ans[0])
        return user

    return None

def current_milli_time():
    return round(time.time() * 1000)

#Start database cursor
con = sqlite3.connect('website/db.sqlite', check_same_thread=False)
cur = con.cursor()

#Safe multithread sql query
def query(queryString,values):
    res = None
    while(1):
        try:
            lock.acquire(True)
            cur.execute(queryString, values)
            res = cur.fetchall()
            break
        except:
            temp=0
        finally:
            lock.release()

    return res

#Safe multithread sql commit
def commit():
    while(1):
        try:
            lock.acquire(True)
            con.commit()
            break
        except:
            temp=0
        finally:
            lock.release()

class User:
    def __init__(self,id):
        self.id = id

    def get_user_id(self):
        return self.id
    
    def get_username(self):
        username = query("Select username from user where id = ?",(self.id,))
        if username != []:
            return username[0][0]
        return None
    
    def get_skill(self):
        skill = query("Select skill from user where id = ?",(self.id,))
        if skill != []:
            return skill[0][0]
        return None
    
    def get_behaviour(self):
        behaviour = query("Select behaviour from user where id = ?",(self.id,))
        if behaviour != []:
            return behaviour[0][0]
        return None
    
    def get_bins(self):
        bins = query("Select bins from user where id = ?",(self.id,))
        if bins != []:
            return bins[0][0]
        return None
    
    def get_skill_preference(self):
        skill_preference = query("Select skill_preference from user where id = ?",(self.id,))
        if skill_preference != []:
            return skill_preference[0][0]
        return None
    
    def get_behaviour_preference(self):
        behaviour_preference = query("Select behaviour_preference from user where id = ?",(self.id,))
        if behaviour_preference != []:
            return behaviour_preference[0][0]
        return None
    
    def get_cmd_id(self):
        cmd_id = query("Select cmd_id from user where id = ?",(self.id,))
        if cmd_id != []:
            return cmd_id[0][0]
        return None

#Oauth2 client wrapper class
class OAuth2Client(ClientMixin):
    def __init__(self,id):
        self.client_id = id

    def get_client_id(self):
        clientid = query("Select client_id from oauth2_client where id = ?",(self.client_id,))
        if clientid != []:
            return clientid[0][0]
        return None
    
    def get_default_redirect_uri(self):
        clientMetadata = query("Select client_metadata from oauth2_client where id = ?",(self.client_id,))
        if clientMetadata != []:
            client_metadata = json.loads(clientMetadata[0][0])
            
        if client_metadata['redirect_uris']:
            return client_metadata['redirect_uris'][0]
        
    def get_allowed_scope(self, scope):
        if not scope:
            return ''
        clientMetadata = query("Select client_metadata from oauth2_client where id = ?",(self.client_id,))
        
        if clientMetadata != []:
            client_metadata = json.loads(clientMetadata[0][0])

            allowed = set(client_metadata['scope'].split())
            scopes = scope_to_list(scope)
            return list_to_scope([s for s in scopes if s in allowed])
        return ''
        
    def check_redirect_uri(self, redirect_uri):
        clientMetadata = query("Select client_metadata from oauth2_client where id = ?",(self.client_id,))
        if clientMetadata != []:
            client_metadata = json.loads(clientMetadata[0][0])
            return redirect_uri in client_metadata['redirect_uris']
    
    def check_client_secret(self, client_secret):
        client_secret_db = query("Select client_secret from oauth2_client where id = ?",(self.client_id,))
        if client_secret_db != []:
            return secrets.compare_digest(client_secret_db[0][0], client_secret)

    def check_token_endpoint_auth_method(self, method):
        return self.check_endpoint_auth_method(method, 'token')
    
    def check_endpoint_auth_method(self, method, endpoint):
        if endpoint == 'token':
            clientMetadata = query("Select client_metadata from oauth2_client where id = ?",(self.client_id,))
            if clientMetadata != []:
                client_metadata = json.loads(clientMetadata[0][0])

            if client_metadata['token_endpoint_auth_method']:
                if method == client_metadata['token_endpoint_auth_method']:
                    return 1
                return 0
        return True
        
        
    def check_response_type(self, response_type):
        clientMetadata = query("Select client_metadata from oauth2_client where id = ?",(self.client_id,))
        if clientMetadata != []:
            client_metadata = json.loads(clientMetadata[0][0])
            
        if client_metadata['response_types']:
            if response_type in client_metadata['response_types']:
                return 1
            return 0

        return None

    def check_grant_type(self, grant_type):
        clientMetadata = query("Select client_metadata from oauth2_client where id = ?",(self.client_id,))
        if clientMetadata != []:
            client_metadata = json.loads(clientMetadata[0][0])
            
        if client_metadata['grant_types']:
            if grant_type in client_metadata['grant_types']:
                return 1
            return 0

        return None

#Oauth2 authorization code wrapper class
class OAuth2AuthorizationCode(AuthorizationCodeMixin):
    
    def __init__(self,id):
        self.id = id

    #Implementation of rfc authorizationCodeMixin get_redirect_uri() method
    def get_redirect_uri(self):
        uri = query("Select redirect_uri from oauth2_code where id = ?",(self.id,))
        if uri[0][0] == None:
            return ""
        return uri[0]
    
    def is_expired(self):
        auth_time = query("Select auth_time from oauth2_code where id = ?",(self.id,))
        if auth_time == []:
            return None
        return auth_time[0][0] + 300 < time.time()
        
    #Implementation of rfc authorizationCodeMixin scope() method
    def get_scope(self):
        scope = query("Select scope from oauth2_code where id = ?", (self.id,))
        if scope == []:
            return None
        return scope[0][0]

#Oauth2 access token wrapper class
class OAuth2Token(TokenMixin):
    
    def __init__(self,id):
        self.id = id

    def get_client_id(self):
        return self.id
    
    def check_client(self, client):
        client_id = query("Select client_id from oauth2_token where id = ?", (self.id,))
        if client_id != []:
            return client.client_id == int(client_id[0][0])
        return None

    #Implementation of rfc OAuth2TokenMixin get_scope() method
    def get_scope(self):
        scope = query("Select scope from oauth2_token where id = ?", (self.id,))
        if scope == []:
            return None
        return scope[0][0]

    def get_expires_in(self):
        expire_time = query("Select expires_in from oauth2_token where id = ?", (self.id,))
        if expire_time == []:
            return None
        return expire_time[0][0]

    #Implementation of rfc OAuth2TokenMixin is_expired() method    
    def is_expired(self):
        iss_exp = query("Select issued_at from oauth2_token where id = ?", (self.id,))
        if iss_exp != []:
            return iss_exp[0][0] + 1500 < time.time() # Mudar este valor
    
    def is_revoked(self):
        revoked = query("Select revoked from oauth2_token where id = ?", (self.id,))
        if revoked == []:
            return None        
        
        return revoked[0][0]

    def get_access_token(self):
        access = query("Select access_token from oauth2_token where id = ?", (self.id,))
        if access == []:
            return None
        
        return access [0][0]
    
    def to_dict(self):
        return  {
            'access_token': self.get_access_token(),
            "token_type": "Bearer",
            "expires_in": self.get_expires_in(),
            "scope" : self.get_scope()
        }
    
    def __str__(self) -> str:
        return str(query("Select * from oauth2_token where id = ?", (self.id,))[0])

    

