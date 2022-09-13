import random
import string
import os
import sys
import math 
from tabulate import tabulate

# Game Result Decision MM

def mm(room):

    number_of_players = len(room[0]['players'].keys())
    results = [a for a in room[0]['players'].keys()]
    results_dic = {}

    winlose_cheatingquiting = random.randint(0,10) # if < 3 then outcome will be eitheir cheating or quitting

    if winlose_cheatingquiting <= 3:
        quitting_cheating = random.randint(0,1) # cheating or quitting with the same probability

        affected_player = random.randint(0,number_of_players-1)
        for i in range(0,number_of_players):
            if i == affected_player:
                if quitting_cheating == 0:
                    results_dic[results[i]] = 'quit'
                else:
                    results_dic[results[i]] = 'cheating'
            else:
                results_dic[results[i]] = 'draw'
    else:
        if (number_of_players == 2):
            affected_player = random.randint(0,number_of_players-1)
            for i in range(0,number_of_players):
                if i == affected_player:
                    results_dic[results[i]] = 'win'
                else:
                    results_dic[results[i]] = 'lost'

        else:
            affected_player = random.sample(range(0, number_of_players-1), 2)
            for i in range(0,number_of_players):
                if i == affected_player[0] or i == affected_player[1]:
                    results_dic[results[i]] = 'win'
                else:
                    results_dic[results[i]] = 'lost'

    return results_dic

# Matchmaking Logic TM

players_by_game = {
    'sueca' : (4,2),    #Numer of players, number of winners
    'checkers' : (2,1),
    'chess' : (2,1)
}

def combineChars(chars, spacing):
    lines = []
    for line_i in range(max([len(x) for x in chars])):
        line = []
        for char in chars:
            if len(char) > line_i:
                line.append(char[line_i])
        lines.append(spacing.join(line))
    return '\n'.join(lines)

def split(a, n):
    return [a[i:i+n] for i in range(0,len(a),n)]

#Horizontal dynamic room print
def printRoomList():
    os.system('clear')
    all_col = []
    sortedList  = sorted(roomList, key=lambda room: room['game'])
    for room in sortedList:
        temp = ""
        room_string = "Room <{}> {} : ".format(room['id'],room['game'])
        temp += (f"{room_string:<30}\n")
        for user in room['players']:
            user_string = "     User: {}".format(user)
            temp += (f"{user_string:<30}\n")
        all_col.append(temp)

    columns, rows = os.get_terminal_size(0)
    
    available_col = math.floor(columns / 30)
    tep1 = list(split(all_col,available_col))
    for chunk in tep1:
        print(tabulate([chunk], tablefmt="plain"))
        print()

    sys.stdout.flush()
    
    
roomList = []

def checkMatchups(user):
    #Check all available rooms
    for room in roomList:
        in_room = False
        #Check if the user is place game as the room, and if the room is not full
        if room['game'] == user.game and len(room['players'].keys()) < players_by_game[user.game][0]:
            #Verify if the preferences are compatible
            if checkPreferences(room['players'],user):
                room['players'][user.user] = user
                in_room = True

        #If the room is full, remove the room and return True
        if len(room['players'].keys()) == players_by_game[user.game][0] and in_room:
            roomList.remove(room)
            return (room,True)

        elif in_room:
            return (room,False)

    #Room Structure
    room = {
        'id' : ''.join(random.choices(string.ascii_uppercase + string.digits, k = 10)),
        'game' : user.game,
        'players' : {
            user.user : user
        }
    }
    roomList.append(room)
    return (room,False)


def checkPreferences(players,user):
    checkAllPlayers=[]
    #For each player of the room, the new player needs to verify his compatibility
    for player in players:
        skill_check = False
        behaviour_check = False
        if players[player].skill_preference <= 0 and user.skill_preference >= 0:
            if players[player].skill * user.skill_bin >= user.skill * players[player].skill_bin:
                skill_check = True

        if players[player].skill_preference >= 0 and user.skill_preference <= 0:
            if players[player].skill * user.skill_bin <= user.skill * players[player].skill_bin:
                skill_check = True
        
        if players[player].behaviour_preference <= 0 and user.behaviour_preference >= 0:
            if players[player].behaviour * user.behaviour_bin >= user.behaviour * players[player].behaviour_bin:
                behaviour_check = True

        if players[player].behaviour_preference >= 0 and user.behaviour_preference <= 0:
            if players[player].behaviour * user.behaviour_bin <= user.behaviour * players[player].behaviour_bin:
                behaviour_check = True
        
        if skill_check and behaviour_check:
            checkAllPlayers.append(True)
        else:
            checkAllPlayers.append(False)
    
    if all(checkAllPlayers):
        return True

    return False