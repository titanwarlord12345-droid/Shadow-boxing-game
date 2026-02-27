# we have 2 players(player or cpu),movement(up,down,right and left) and 20 sec time limit 
import random
from shutil import move
import time
import signal
import sys
import math

# Timeout used for player input (seconds)
INPUT_TIMEOUT = 20

class _InputTimeout(Exception):
    pass

def _timeout_handler(signum, frame):
    raise _InputTimeout()

def input_with_timeout(prompt, timeout=INPUT_TIMEOUT):
    try:
        signal.signal(signal.SIGALRM, _timeout_handler)
        signal.alarm(timeout)
        value = input(prompt)
        signal.alarm(0)
        return value
    except _InputTimeout:
        print("\nTime's up! (no input)")
        signal.alarm(0)
        return None
    finally:
        try:
            signal.signal(signal.SIGALRM, signal.SIG_IGN)
        except Exception:
            pass

# rounds left counter (do not shadow built-in `round`)
rounds = 10

# game state
player_move = None
cpu_move_value = None
prev_player_move = None
prev_cpu_move = None
combo_p1 = 0
combo_cpu = 0
current_turn = 'player'
player_used_moves = set()
cpu_used_moves = set()

#ask for cpu or player 2
def player2 ():
    opponent = int(input("type 1 for player 2 or type 2 for cpu "))
    if opponent == 1 :
        username = input("what is your username")
        print("player 2 is", username)
    else:
        print("player 2 is CPU")
#round counter
def round_counter():
    global rounds
    if rounds % 2 == 0:
        print("player 2's turn")
    else:
        print("player 1's turn")
    # rounds are decremented once per full cycle in play_time
def turn():
    global player_move, player_used_moves
    start = time.time()
    player_move = None
    while True:
        elapsed = time.time() - start
        remaining = INPUT_TIMEOUT - elapsed
        if remaining <= 0:
            print("\nTime's up! (no move)")
            break
        # ask with remaining time
        resp = input_with_timeout("type 1 for up, 2 for left, 3 for right and 4 for down\n", math.ceil(remaining))
        if resp is None:
            player_move = None
            break
        try:
            mv = int(resp)
        except ValueError:
            print("invalid input")
            continue
        if mv not in (1, 2, 3, 4):
            print("invalid move, choose 1-4")
            continue
        if mv in player_used_moves:
            print("you already used that move; pick another")
            continue
        # accept move
        player_move = mv
        player_used_moves.add(mv)
        if len(player_used_moves) >= 4:
            # all moves used; reset so player can reuse
            player_used_moves.clear()
        if player_move == 1:
            print("you moved up")
        elif player_move == 2:
            print("you moved left")
        elif player_move == 3:
            print("you moved right")
        elif player_move == 4:
            print("you moved down")
        break
def turn_check():
    # kept for compatibility; combo logic handled in play_time
    return

def cpu_move():
    global cpu_move_value, prev_player_move, cpu_used_moves
    bias_prob = 0.6
    remaining = [m for m in (1, 2, 3, 4) if m not in cpu_used_moves]
    if not remaining:
        # reset if CPU used all moves
        cpu_used_moves.clear()
        remaining = [1, 2, 3, 4]
    # try biased pick if possible and not already used
    pick = None
    if prev_player_move is not None and prev_player_move in remaining and random.random() < bias_prob:
        pick = prev_player_move
    if pick is None:
        pick = random.choice(remaining)
    cpu_move_value = pick
    cpu_used_moves.add(cpu_move_value)
    if len(cpu_used_moves) >= 4:
        cpu_used_moves.clear()
    if cpu_move_value == 1:
        print("CPU moved up")
    elif cpu_move_value == 2:
        print("CPU moved left")
    elif cpu_move_value == 3:
        print("CPU moved right")
    elif cpu_move_value == 4:
        print("CPU moved down")
# legacy combo functions removed; combo state handled in play_time
def play_time ():
    global prev_cpu_move, prev_player_move, combo_p1, combo_cpu, rounds, current_turn
    while rounds > 0 and combo_p1 < 3 and combo_cpu < 3:
        # display whose turn it is
        if current_turn == 'player':
            print("player's turn")
            # player turn
            turn()
            print()

            # only treat valid moves (1-4) as meaningful
            if player_move in (1, 2, 3, 4):
                # check player combo against previous CPU move
                if prev_cpu_move is not None and player_move == prev_cpu_move:
                    combo_p1 += 1
                    print(username, "combo", combo_p1)
                else:
                    if combo_p1 > 0:
                        print("combo broken")
                    combo_p1 = 0
                prev_player_move = player_move
            else:
                # invalid or timed-out input breaks combo
                if combo_p1 > 0:
                    print("combo broken (no valid move)")
                combo_p1 = 0

            # hand control to CPU next
            current_turn = 'cpu'
        else:
            print("CPU's turn")
            # cpu turn
            cpu_move()

            # check cpu combo against previous player move
            if prev_player_move is not None and cpu_move_value == prev_player_move:
                combo_cpu += 1
                print("CPU combo", combo_cpu)
            else:
                if combo_cpu > 0:
                    print("CPU combo broken")
                combo_cpu = 0
            prev_cpu_move = cpu_move_value

            # completed a full round (player+cpu)
            rounds -= 1
            current_turn = 'player'
        # check winners
        if combo_p1 >= 3:
            print(username, "wins")
            break
        if combo_cpu >= 3:
            print("CPU wins")
            break

                       


#Ask for username and explain game rules
username = input("what is your username")
print("this game is called shadow boxing" )
print("the goal of the game is to combo your opponent")
print("You can do this by typeing one of these numbers once each turn ")
print("1(up),2(left),3(right) and 4(down) but you only have 20 seconds to decide ")
play = input("if you want to start type Y  ")
#start the game
if play == "y" or play == "Y":
    
    print()
    time.sleep(3)
    player2()
    print()
    time.sleep(3)
    # start the play loop; play_time handles turns
    play_time()
    

    
