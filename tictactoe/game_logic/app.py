"""
Author:Daniel Gil Cota
"""

#from game_logic import game
from game_logic import two_players
from menu import display_menu



def main():
    """Main function to run the Tic Tac Toe game"""
    while True:
      choice = display_menu()
      if choice==1:
         print("One Player Game is not implemented yet.")
       #Here you would call the one player game function when implemented
      elif choice==2:
           two_players()
      elif choice==3:
        print("Exiting the game. Goodbye!")
        break
      else:
        print("Inavlid choice.Please select a valid option.")


if __name__ =="__main__":
    main()