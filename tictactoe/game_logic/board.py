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

if __name__ == "__main__":
    board = {x:str(x) for x in range(9)}
    board[0] = "X"
    board[4] = "O"
    display_board(board)
    
    
    
     # Tictactoe

#A game of tic-tac-toe
#implemented in Python

# Author
#Developed by Daniel Gil Cota
    