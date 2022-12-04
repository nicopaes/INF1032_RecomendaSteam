import requests
import json
import asyncio

key = ""
# steam_id = 76561198018909519
steam_id = 76561198068311174
getownedgameAPI = f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={key}&steamid={steam_id}&format=json'
getrecentgameAPI = f'http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key={key}&steamid={steam_id}&format=json'


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

# getSteamLibrary = requests.get(getownedgameAPI)

# text = getSteamLibrary.text
# jsonResponse = json.loads(text)['response']
# print(jsonResponse)

# game_count = jsonResponse['game_count']
# # print(game_count)

# games = jsonResponse['games']
# # print(games)


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

getRecentLibrary = requests.get(getrecentgameAPI)

# text = getRecentLibrary.text
# jsonResponse = json.loads(text)['response']
# print(jsonResponse)


# gameList = createListPlayedGames(games)
# with open(f'{steam_id}_gamelist.json', 'w') as file:
#     # print(json.dumps(gameList))
#     json.dump(gameList, file, indent=2)
#     print(f"New json file is created from steamid {steam_id}")


print(GetAppDetails(379720))