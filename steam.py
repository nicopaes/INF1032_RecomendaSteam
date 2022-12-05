import requests
import json
import asyncio

key = ""

async def GetAppDetailsAsync(appid):
    return await requests.get(f'https://store.steampowered.com/api/appdetails?appids={appid}')

def GetAppDetails(appid):
    appidtext = str(appid)
    reponse = requests.get(f'https://store.steampowered.com/api/appdetails?appids={appid}')
    if (reponse.status_code == 200):
        reponse.encoding = 'utf-8-sig'
        if (reponse.text != ""):
            jsonObj = json.loads(reponse.text)[appidtext]
            return jsonObj.get('data')
        else:
            print(appid)
            return None
    else:
        print(f'Code not 200 {appid}')
        return None

def createListPlayedGames(games):
    gamelist = []
    for i in range(int(game_count) - 1):
        game = games[i]
        appid = game['appid']
        playtimeforever = game['playtime_forever']
        appinfo = GetAppDetails(appid)
        if (appinfo == None):
            print(appid)
        else:
            if (playtimeforever > 0):
                gamename = appinfo['name']
                gamelist.append(
                    {"name": gamename, "playtimeforever": playtimeforever})
                print(len(gamelist))
    return gamelist

def GetOwnedGames(steam_id):    
    gamelist = []
    ##
    getownedgames = f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={key}&steamid={steam_id}&format=json'
    getOwnedLibrary = requests.get(getownedgames)
    text = getOwnedLibrary.text
    jsonResponse = json.loads(text)['response']
    total_count = jsonResponse['game_count']
    if(total_count > 0):
        games = jsonResponse['games']
        for i in range(int(total_count) - 1):
            game = games[i]
            appid = game['appid']
            playtimeforever = game['playtime_forever']
            appinfo = GetAppDetails(appid)
            if (appinfo == None):
                print(appid)
            else:
                if (playtimeforever > 0):
                    gamename = appinfo['name']
                    gamelist.append(
                        {"name": gamename, "playtimeforever": playtimeforever})
    return sorted(gamelist, key= lambda game: game["playtimeforever"], reverse=True)

def GetRecentPlayerGames(steam_id):    
    gamelist = []
    ##
    getrecentgameAPI = f'http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key={key}&steamid={steam_id}&format=json'
    getRecentLibrary = requests.get(getrecentgameAPI)
    text = getRecentLibrary.text
    jsonResponse = json.loads(text)['response']
    total_count = jsonResponse['total_count']
    if(total_count > 0):
        games = jsonResponse['games']
        for i in range(int(total_count) - 1):
            game = games[i]
            appid = game['appid']
            name = game["name"]
            playtimeforever = game['playtime_forever']
            gamelist.append(
                    {"appid": appid,"name": name, "playtimeforever": playtimeforever})
    return sorted(gamelist, key= lambda game: game["playtimeforever"], reverse=True)

def CreateGameList(steamid):
    finalist = []
    gamerecent = GetRecentPlayerGames(steamid)
    if(len(gamerecent) < 5):
        gameowned = GetOwnedGames(steamid)
        finalist = [x for x in gamerecent[0:len(gamerecent)]]
        for i in range(len(gameowned)):
            if(len(finalist) == 5):
                return sorted(finalist, key= lambda game: game["playtimeforever"], reverse=True)                 
            else:
                if(gameowned[i] not in finalist):
                    finalist.append(gameowned[i])            
    else:
        return gamerecent[:5]

print(CreateGameList(76561198068311174))

# gameList = createListPlayedGames(games)
# with open(f'{steam_id}_gamelist.json', 'w') as file:
#     # print(json.dumps(gameList))
#     json.dump(gameList, file, indent=2)
#     print(f"New json file is created from steamid {steam_id}")

