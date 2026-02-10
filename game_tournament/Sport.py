""" Sport class represents a sport in the tournament. It has a name and a league. """
class Sport:
    """ Sport class represents a sport in the tournament. It has a name and a league. """
    def __init__(self, name, num_players, league):
        """ Custom constructor for Sport class. """
        self.name = name
        self.league = league
        self.num_players = num_players
    def __str__(self):
        """ String representation of the Sport class. """
        return f"{self.name} ({self.league}) - {self.num_players} players"
    def __repr__(self):
        """ String representation of the Sport class. """
        return f"Sport(name={self.name}, league={self.league}), players={self.num_players})"
    def to_json(self):
        """ Convert the Sport object to a JSON string. """
        return {
            "name": self.name,
            "league": self.league,
            "num_players": self.num_players
        }

if __name__ == "__main__":
    sport = Sport("Basketball", 10, "NBA")
    print(sport)
    print(sport.to_json())
    print(repr(sport))