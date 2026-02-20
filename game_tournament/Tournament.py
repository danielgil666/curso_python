"""
Docstring for game_tournament.Tournament
"""
import random
import json
from Game import Game
from Team import Team
from Sport import Sport
from Athlete import Athlete

class Tournament:
    """ Tournament class represents a tournament. It has a name, a list of games, and a list of teams. """
    def __init__(self, name):
        """ Custom constructor for Tournament class. """
        self.name = name
        self.games = []
        self.teams = []
    def add_team(self, team):
        """ Add a team to the tournament. """
        if isinstance(team, Team):
            self.teams.append(team)
        else:
            raise ValueError("Only Team objects can be added as a team.")
    def add_game(self, game):
        """ Add a game to the tournament. """
        if isinstance(game, Game):
            self.games.append(game)
        else:
            raise ValueError("Only Game objects can be added as a game.") 
    def __str__(self):
        """ String representation of the Tournament class. """
        return f"Tournament: {self.name}, Teams: {len(self.teams)}, Games: {len(self.games)}"
    def __repr__(self):
        """ String representation of the Tournament class. """
        return f"Tournament(name={self.name}, teams={repr(self.teams)}, games={repr(self.games)})"
    def to_json(self):
        """ Convert the Tournament object to a JSON string. """
        return {
            "name": self.name,
            "teams": [team.to_json() for team in self.teams],
            "games": [game.to_json() for game in self.games]
        }
    def set_group(self,group_list,group_name):
   group= Group(group_name)
for team in group_list:
    group.add_team(team)
       self.groups 
    def set_group_stage(self):
if len(self.teams)==8:
    group_a=self.teams[:4]
    group_b=self.teams[4:]
   
    def load_json(self, filename):
        """ Load a Tournament object from a JSON file."""
        print("Tournament")
        with open(filename, 'r', encoding="utf-8") as f:
            data = json.load(f)
            for team_data in data:
                team_name = team_data["name"]
                sport_name = team_data["sport"]["name"]
                sport_league = team_data["sport"]["league"]
                sport_num_players = team_data["sport"]["num_players"]
                sport = Sport(sport_name, sport_num_players, sport_league)
                team = Team(team_name, sport)
                players = team_data["athletes"]
                for player in players:
                    team.add_athlete(Athlete(player))
                self.add_team(team)

if __name__ == "__main__":
    tournament = Tournament("FIFA World Cup")
    tournament.load_json("tournament.json")
    print(tournament)