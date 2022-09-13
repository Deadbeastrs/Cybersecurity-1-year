from authlib.oauth2.rfc6749 import grants
from authlib.oauth2.rfc6750 import BearerTokenValidator
from authlib.oauth2.rfc7009 import RevocationEndpoint
from .database import User, query, commit
from .database import OAuth2Client, OAuth2AuthorizationCode, OAuth2Token
import time

#Authlib Configuration
#Configure Authorization Grant, Bearer Token Validator and Revocation Endpoint

class AuthorizationCodeGrant(grants.AuthorizationCodeGrant):
    TOKEN_ENDPOINT_AUTH_METHODS = [
        'client_secret_basic'
    ]

    def save_authorization_code(self, code, request):
        redirect_uri=request.redirect_uri
        scope=request.scope
        user_id=request.user.id
        client_id=request.client.client_id
        auth_time = int(time.time())
        query("insert into oauth2_code(code,client_id,redirect_uri,scope,user_id,auth_time) values (?,?,?,?,?,?)",
        (code,client_id,redirect_uri,scope,user_id,auth_time,))
        commit()
        return ""

    def query_authorization_code(self, code, client):
        auth_code_id = query("select id from oauth2_code where code = ? and client_id = ?",(code,client.client_id))
        if auth_code_id != []:
            authCode = OAuth2AuthorizationCode(auth_code_id[0][0])
            if not authCode.is_expired():
                return authCode
        
        return None

    def delete_authorization_code(self, authorization_code):
        query("delete from oauth2_code where id = ?",(authorization_code.id,))
        commit()
        

    def authenticate_user(self, authorization_code):
        user_id = query("select user_id from oauth2_code where id = ?",(authorization_code.id,))
        if user_id != []:
            return User(user_id[0][0])

class MyBearerTokenValidator(BearerTokenValidator):
    def authenticate_token(self, token_string):
        id_a = query("Select id from oauth2_token where access_token = ?",(token_string,))
        if id_a != []:
            return OAuth2Token(id_a[0][0])
        return None

    def request_invalid(self, request):
        return False

    def token_revoked(self, token):

        revoked = query("Select revoked from oauth2_token where id = ?",(token.id,))
        if revoked != []:
            return revoked[0][0]

class MyRevocationEndpoint(RevocationEndpoint):
    def query_token(self, token, token_type_hint):
        id_a = query("Select id from oauth2_token where access_token = ?",(token,))
        if id_a != []:
            return OAuth2Token(id_a[0][0])
        return None

    def revoke_token(self, token, request):
        query("UPDATE oauth2_token SET revoked = True WHERE id =?",(token.id,))
        commit()
        

def query_client(client_id):
    d_id = query("Select id from oauth2_client where client_id = ?",(client_id,))
    if d_id != []:
        return OAuth2Client(d_id[0][0])
    
def save_token(token, request):
    if request.user:
        user_id = request.user.id
    else:
        user_id = None
   
    client = request.client
    query("insert into oauth2_token(client_id,token_type,access_token,scope,issued_at,expires_in,user_id,revoked) values (?,?,?,?,?,?,?,?)",
        (client.client_id,token['token_type'],token['access_token'],token['scope'],int(time.time()),token['expires_in'],user_id,False))
    commit()
    return None

def configOauth(app,authorization,require_oauth):
    authorization.init_app(app)
    authorization.register_grant(AuthorizationCodeGrant)
    authorization.register_endpoint(MyRevocationEndpoint)
    require_oauth.register_token_validator(MyBearerTokenValidator())