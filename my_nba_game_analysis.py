import csv

def load_data(filename):
    result = []
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file, delimiter='|')
        fields = next(csv_reader)

        for row in csv_reader:
            result.append(row)
    return result


def analyse_nba_game(string_input):
    game_stats = load_data(string_input)
    
    the_player_list = []
    # Loop through the game statistics to locate the required information.
    for stat in game_stats:
        if stat != '\n':   
            
            # The description of the play is found at the end of the stats, requiring me to split it to access the description
            description = stat[-1]
            # Compiling a list of actions to look for in every play
            
            actions = {'Turnover':"TOV", 'steal': "STL", 'Defensive rebound': "DRB", 'assist': "AST", 'block': "BLK", 'Offensive rebound': "ORB", "Shooting foul": "PF", "makes free throw": "FT", 'throw':"FTA", 'makes 3-pt':"3P", '3-pt':"3PA", "makes 2-pt":"FG", "2-pt":"FGA"} # this should be a dictionary of values 
            for action in actions.keys():
                # Initially address the initial 6 actions within the actions dictionary due to their identical patterns
                if  action in description and list(actions.keys()).index(action) < 7:
                    name = " ".join(description.split(f'{action} by')[-1].split(' ')[0:3]).strip().split(')')[0]
                    if 'Team ' in name:
                        break
                    data = {'name': name, 'action': action}
                    update_player_list_(the_player_list, data, actions, action)
                    
                    
                    
                # Free throws, three-pointers, and two-pointers share a common pattern, allowing me to apply the same approach used for the initial five elements by considering indexes greater than five
                elif action in description and list(actions.keys()).index(action)  >=7 : # Here, updating the free thows attempts
                    name = " ".join(description.split(' ')[:2]).strip()
                    data = {'name': name, 'action': action}
                    update_player_list_(the_player_list, data, actions, action)
    the_home_team_stats = []
    the_away_team_stats = []
    HOME_TEAM = stat[2]
    AWAY_TEAM = stat[3]
    calculate_the_points_(the_player_list,game_stats[1:], the_home_team_stats, the_away_team_stats)     


    return {"home_team": {"name": HOME_TEAM, "players_data": the_home_team_stats}, "away_team": {"name": AWAY_TEAM, "players_data": the_away_team_stats}}


def the_value_exist(the_player_list, player_name): # This is used for confirming whether the player is already present in the list
    for index in range(len(the_player_list)):
        if player_name in the_player_list[index]['player_name']:
            return index
    return -1

def update_player_list_(the_player_list, data, actions, action):
    index = the_value_exist(the_player_list, data['name']); # This function provides the length of the player list
    if index > -1: # if player already exist before
        p_action = data['action']
        the_player_list[index][actions[p_action]] += 1
    else: # if player does not exist before
        result = {"player_name": data['name'], "FG": 0, "FGA": 0, "FG%": 0, "3P": 0, "3PA": 0, "3P%": 0, "FT": 0, "FTA": 0, "FT%": 0, "ORB": 0, "DRB": 0, "TRB": 0, "AST": 0, "STL": 0, "BLK": 0, "TOV": 0, "PF": 0, "PTS": 0}
        result[actions[action]] += 1
        the_player_list.append(result)

    # Calculating the percentage of the result
    result = the_player_list[index]

    try:
        result['FT%'] = round(result["FT"] / result["FTA"] * 100, 3)
    except:
        pass

    try:
        result['3P%'] = round(result["3P"] / result["3PA"]  * 100, 3)
    except:
        pass

def calculate_the_points_(the_player_list, game_stats, the_home_team_stats, the_away_team_stats):
    index = 0
    # This function computes the points scored by each player and their field goals
    for player in the_player_list:
        stat = game_stats[index]
        player_team = stat[2]
        home_team = stat[3]
        t_points = player["FG"]
        player["FG"] = player["3P"] + player["FG"]

        player["FGA"] = player["3PA"] + player["FGA"]
        try: 
            player["FG%"] = round(player["FG"] / player["FGA"] * 100, 3)
        except:
            pass

        # Here, we calculate the points collected for each player
        player["PTS"] = (t_points * 2) + (player["3P"] * 3) + player["FT"]

        if player_team == home_team:
            the_home_team_stats.append(player)
        else:
            the_away_team_stats.append(player)


        index += 1



test_string = 'nba_game_warriors_thunder_20181016.txt'     






def print_nba_game_stats(team):
    data = analyse_nba_game(test_string)

    # collecting the team to print here
    team = team.lower()
    players_stat = data[team]
    headers = [t for t in players_stat['players_data'][0].keys()]
    rows = players_stat['players_data']
    for header in headers:
        print(header, end = '\t')
    print('')
    
    sums = []
    for row in rows:
        count = 0
        for  item in row.values():
            try:
                sums[count] += item
            except:
                sums.append(item)
            if count != 18:
                print(item, end = '\t')
            else: 
                print(item)
                count = 0

            count+= 1


    print('Team Totals', end = '\t')
    # printing the total scores scored
    count = 0
    for item in sums[1:]:
        count += 1
        if headers[count] in ['FG%', '3P%', 'FT%']:
            print(round(item/len(rows), 3), end = '\t')
        else:
            print(item, end = '\t')


print_nba_game_stats('home_team')