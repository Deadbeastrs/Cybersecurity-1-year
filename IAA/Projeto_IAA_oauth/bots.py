import math
import time
import json
import requests
import socketio
import random
import threading
import sqlite3
import re
import html
import sys
import argparse
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

log = open("bot_log.txt","w")

game_list=['chess','checkers','sueca']

con = sqlite3.connect('website/db.sqlite', check_same_thread=False)

def insert_user(username,password):
    
    cur = con.cursor()
    check_user = "SELECT * FROM user where username = ?"
    cur.execute(check_user, (username,))
    number = cur.fetchall()
    if number == []:
        kdf = PBKDF2HMAC(algorithm=hashes.SHA1(),length=16,salt=str.encode("IAA"),iterations=50000)
        password = kdf.derive(str.encode(password))
        queryString = "INSERT INTO user(username,password) VALUES (?,?) "
        values = (username,password)
        cur.execute(queryString, values)
        con.commit()

def game_client(game,username,user_db,pass_db):
    #Verify arguments
    session = requests.Session()
    if args.np == False:
        random_skill_pref = random.randint(-1,1)
        random_behaviour_pref = random.randint(-1,1)
    else:
        random_skill_pref = 0
        random_behaviour_pref = 0

    if args.bins == None:
        random_bin = random.randint(1,10)
    else:
        random_bin = int(args.bins)
    # Start Game with bins and preferences
    start_game = 'http://127.0.0.1:5000/tm/start_game?game={}&username={}&skill_pref={}&behaviour_pref={}&bins={}'
    first_page = session.get(start_game.format(game,username,random_skill_pref,random_behaviour_pref,random_bin))
    payload = {'username':user_db,'password':pass_db}
    # Check if username is already beeing used
    if 'username' not in first_page.url:
        # Login with credentials
        login = session.post("http://127.0.0.1:5000/rm/login",data=payload)
        after_login = session.post(login.url)
        # Find Socket Id
        socket_id = re.search('socket.on\(\"(.*?)\"',after_login.text).groups()[0]
        # If final user in room, the outcome will be preloaded on the returned webpage ,else listen with socket ans wait result
        if re.search('if\(\"True\" == \"True\"\){',after_login.text) != None:
            result = re.search('\(\"(.*?)\",decodeHtml\(\"(.*?)\"\),\"(.*?)\"\)',after_login.text).groups()
            result_json = json.loads(html.unescape(result[1]))
            log.write("{} {} at {}\n".format(result[0],result_json[result[0]],result[2]))
            log.flush()
            print("{} {} at {}".format(result[0],result_json[result[0]],result[2]))
        else:
            #Listen to the websocket
            sio = socketio.Client()
            sio.connect('http://localhost:5000')
            @sio.on(socket_id)
            def game_result(result,game):
                result_json = json.loads(result)
                log.write("{} {} at {}\n".format(username,result_json[username],game))
                log.flush()
                print("{} {} at {}".format(username,result_json[username],game))
                sio.disconnect()
    exit(1)

def start_threads():
    numThreads = []
    for k in range(int(args.rounds)):
        for i in range(0,int(args.players)):
            time.sleep(0.5)
            random_game = random.randint(0,len(game_list)-1)
            username = "player" + str(i)
            insert_user(username, "pwd")
            thread = threading.Thread(target=game_client, args=(game_list[random_game],username,username,"pwd",))
            numThreads.append(thread)
            thread.start()

        for x in numThreads:
            x.join()

if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument('-r', '--rounds', nargs='?',required=True, help='Number of rounds')
    parser.add_argument('-p', '--players', nargs='?',required=True, help='Number of players')
    parser.add_argument('-b', '--bins', nargs='?',required=False, help='Number of bins')
    parser.add_argument('-np', action='store_true', help='Flag for no preference')
    global args
    args=parser.parse_args()
    print("The bots might not get matched in the end of this script")
    print("If that is the case, use ctrl-c to exit")
    print("All results are logged in bot_log.txt")
    time.sleep(4)
    print("Bots will now start!")
    thread = threading.Thread(target=start_threads, args=())
    thread.start()
    thread.join()
        
        
        
    
    

