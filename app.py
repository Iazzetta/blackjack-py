import asyncio
from random import randint
from fastapi import FastAPI, Request
from filemanager import FileManager
from workers.matchmaking import matchmaking_worker
from workers.game_manager import game_manager_worker
from cards import gen_card
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.on_event("startup") 
async def start_workers():
    print("inicializando workers...")
    asyncio.create_task(matchmaking_worker())
    asyncio.create_task(game_manager_worker())

@app.get('/')
async def home(request: Request):

    user_id = randint(1111, 9999)

    fm = FileManager('players')
    players = fm.get()
    
    players[user_id] = {
        "game_id": None
    }

    fm.save(players)

    return templates.TemplateResponse(
        request=request, name="index.html", context={"user_id": user_id }
    )

@app.get('/search/{user_id}')
async def search_game(user_id: str):
    fm = FileManager('matchmaking')

    games = fm.get()

    games[user_id] = 'waiting'

    fm.save(games)

    return {'status': 'searching...'}


@app.get('/player/{user_id}')
async def get_player_info(user_id: str):
    fm = FileManager('players')
    players = fm.get()
    return players[user_id]

@app.get('/game/{game_id}/by/{user_id}')
async def get_game(game_id: str, user_id: str):

    fm = FileManager('gamemanager')
    games = fm.get()
    game = games[game_id]

    game_response = {
        "status": game['status'],
        "turn_counter": game['turn_counter'],
        "scoreboard": game['scoreboard'],
        "round": game['round'],
        "player": game['player1'] if game['player1']['id'] == user_id else game['player2'],
        "enemy": game['player2'] if game['player1']['id'] == user_id else game['player1'],
    }
    if game['show_cards'] is False:
        game_response['enemy']['hand_cards'] = ['' for x in game_response['enemy']['hand_cards']]

    return game_response


@app.get('/game/{game_id}/by/{user_id}/buy-card')
async def buy_card(game_id: str, user_id: str):

    fm = FileManager('gamemanager')
    games = fm.get()

    if games[game_id]['player1']['id'] == user_id:
        games[game_id]['player1']['hand_cards'].append(gen_card())
    else:
        games[game_id]['player2']['hand_cards'].append(gen_card())

    fm.save(games)

    return {}




    