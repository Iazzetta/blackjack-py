import asyncio
from filemanager import FileManager
from cards import gen_card
from game_vars import TURN_COUNTER

async def create_game(player1, player2):
    fm = FileManager('gamemanager')
    games = fm.get()
    game_id = len(games.keys()) + 1
    games[game_id] = {
        "status": "running",
        "round": 1,
        "turn_counter": TURN_COUNTER,
        "show_cards": False,
        "player1": {
            "id": player1,
            "hand_cards": [
                gen_card(),gen_card()
            ]
        },
        "player2": {
            "id": player2,
            "hand_cards": [
                gen_card(),gen_card()
            ]
        },
        "scoreboard": [
            0,
            0
        ]
    }
    fm.save(games)

    fm2 = FileManager('players')
    players = fm2.get()
    players[player1]['game_id'] = game_id
    players[player2]['game_id'] = game_id
    fm2.save(players)


async def matchmaking_worker():
    fm = FileManager('matchmaking')
    while True:
        games = fm.get()
        if games:
            match_players = list( filter(lambda x: x[1] == 'waiting', games.items() ) )

            if len(match_players) >= 2:

                players = match_players[:2]

                for p in players:
                    games[p[0]] = 'playing'

                fm.save(games)
                    
                await create_game(players[0][0], players[1][0])

        await asyncio.sleep(1)