import asyncio
from filemanager import FileManager
from cards import gen_card
from game_vars import *


async def game_manager_worker():
    fm = FileManager('gamemanager')
    print("game manager...")
    while True:
        games = fm.get()
        if games:
            games_running = list( filter(lambda x: x[1]['status']  == 'running', games.items() ) )
            for game in games_running:
                game_id = game[0]

                if games[game_id]['turn_counter'] == 0:
                    player1_sum = sum(games[game_id]["player1"]["hand_cards"])
                    player2_sum = sum(games[game_id]["player2"]["hand_cards"])

                    if player1_sum > 21 and player2_sum <= 21:
                        games[game_id]["scoreboard"][1] += 1
                        print("player 1 ganhou")
                    elif player2_sum > 21 and player1_sum <= 21:
                        games[game_id]["scoreboard"][0] += 1
                        print("player 2 ganhou")
                    elif player1_sum > player2_sum:
                        games[game_id]["scoreboard"][0] += 1
                        print("player 1 ganhou")
                    elif player2_sum > player1_sum:
                        games[game_id]["scoreboard"][1] += 1
                        print("player 2 ganhou")
                    elif player1_sum == player2_sum:
                        print("empate")

                    if games[game_id]['round'] < ROUNDS:
                        games[game_id]['turn_counter'] = TURN_COUNTER

                        games[game_id]['show_cards'] = False

                        games[game_id]['player1']['hand_cards'] = [gen_card(), gen_card()]
                        games[game_id]['player2']['hand_cards'] = [gen_card(), gen_card()]

                        games[game_id]['round'] += 1
                        print("round", games[game_id]['round'])
                    else:
                        games[game_id]['status'] = "finished"
                        fm2 = FileManager('players')
                        players = fm2.get()
                        players[games[game_id]['player1']['id']]['game_id'] = None
                        players[games[game_id]['player2']['id']]['game_id'] = None
                        fm2.save(players)
                        print("game end")
                else:
                    if games[game_id]['turn_counter'] <= SHOW_CARDS_SECOND:
                        games[game_id]['show_cards'] = True

                    games[game_id]['turn_counter'] -= 1
                    print(f"restam: {games[game_id]['turn_counter']} segundos" )

                
                fm.save(games)

        await asyncio.sleep(1)