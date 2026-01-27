"""
Docstring for tictactoe.
game_logic.board
Author : Daniel Gil Cota

"""
def display_board(dboard:dict) -> None:
    """Display game board of Tictactoe"""

    d = dboard
    print(f"{d[0]:2s}|{d[1]:2}|{d[2]:2s}")
    print("--+--+--")
    print(f"{d[3]:2s}|{d[4]:2}|{d[5]:2s}")
    print("--+--+--")
    print(f"{d[6]:2s}|{d[7]:2}|{d[8]:2s}")


def player_turn(player:str, dboard:dict)->bool:

    user_input = input(f"Player{player},Enter your move(0-8):")
    user_input = int(user_input) 
    print(f"value entered: {user_input} type: {type(user_input)}")
    if user_input in dboard.keys():
        if dboard[user_input] not in ['x','0']:
            dboard[user_input] = player
            valid_move = True
        else:
            print("Invalid move: cell already occupied.")
    else:
            print("invalid move: cell doesn't exist")
    return valid_move

if __name__ == "__main__":
     board = {x:str(x) for x in range(9)}
     display_board(board)
     move=player_turn('X',board)
     print()

    # board[0] = "X"
    # board[4] = "O"
     display_board(board)
     player_turn("X", board)
     print(board)
    
     # Tictactoe

#A game of tic-tac-toe
#implemented in Python

# Author
#Developed by Daniel Gil Cota
    