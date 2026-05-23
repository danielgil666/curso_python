"""
Docstring for game_tournament.Team
"""
from Athlete import Athlete
from Sport import Sport

class Team:
    """ Team class represents a team in the tournament. It has a name, a sport, and a list of athletes. """
    def __init__(self, name, sport:Sport):
        """ Custom constructor for Team class. """
        self.name = name
        self.set_sport(sport)
        self.athletes = []
    def set_sport(self, sport):
        """ Set the sport for the team. """
        if isinstance(sport, Sport):
            self.sport = sport
        else:
            raise ValueError("Only Sport objects can be set as the team's sport.")
    def add_athlete(self, athlete):
        """ Add an athlete to the team. """
        if isinstance(athlete, Athlete):
            self.athletes.append(athlete)
        else:
            raise ValueError("Only Athlete objects can be added to the team.")
    def __str__(self):
        """ String representation of the Team class. """
        return f"{self.name} - {self.sport.name} ({len(self.athletes)} athletes)"
    def __repr__(self):
        """ String representation of the Team class. """
        return f"Team(name={self.name}, sport={repr(self.sport)})"
    def to_json(self):
        """ Convert the Team object to a JSON string. """
        return {
            "name": self.name,
            "sport": self.sport.to_json(),
            "athletes": [athlete.to_json() for athlete in self.athletes]
        }

class GroupsScreen(Screen):
    """Screen to display group details and standings."""
    BINDINGS = [("escape", "app.pop_screen", "Back to Menu")]

    def __init__(self, tournament):
        super().__init__()
        self.tournament = tournament

    def compose(self) -> ComposeResult:
        yield Header()
        with VerticalScroll(id="groups-scroll"):
            yield Static("Groups and Standings", classes="title")
            
            for group_name, group in self.tournament.groups.items():
                yield Static(f"\n{group_name}", classes="header")
                
                # Table-like header for standings
                standings_header = f"{'Team':<15} {'Pts':>3} {'W':>2} {'L':>2} {'D':>2} {'GF':>3}:{'GA':<2} {'GD':>3}"
                yield Static(standings_header, classes="subheader")
                
                # Sort teams by points if standings are available
                sorted_standings = sorted(group.points.items(), key=lambda x: x[1]["points"], reverse=True)
                
                for team, stats in sorted_standings:
                    line = (f"{team.name[:15]:<15} {stats['points']:>3} {stats['wins']:>2} "
                            f"{stats['losses']:>2} {stats['draws']:>2} {stats['goals_for']:>3}:"
                            f"{stats['goals_against']:<2} {stats['goal_difference']:>3}")
                    yield Static(f"  {line}")
                    
        yield Footer()

class GamesScreen(Screen):
    """Screen to display all games."""
    BINDINGS = [("escape", "app.pop_screen", "Back to Menu")]

    def __init__(self, tournament):
        super().__init__()
        self.tournament = tournament

    def compose(self) -> ComposeResult:
        yield Header()
        with VerticalScroll(id="games-scroll"):
            yield Static("Tournament Games", classes="title")
            for group_name, group in self.tournament.groups.items():
                yield Static(f"\n{group_name}", classes="header")
                for game in group.games:
                    yield Static(f"  - {game}")
            
            if self.tournament.games:
                yield Static("\nGeneral Games", classes="header")
                for game in self.tournament.games:
                    yield Static(f"  - {game}")
        yield Footer()

class PlayGamesScreen(Screen):
    """Screen to run simulation and display all results."""
    BINDINGS = [("escape", "app.pop_screen", "Back to Menu")]

    def __init__(self, tournament):
        super().__init__()
        self.tournament = tournament

    def on_mount(self) -> None:
        # We run the simulation when the screen is mounted
        # Note: play_games() has print statements, but we'll focus on displaying the state
        #self.tournament.play_games()
        for group in self.tournament.groups:
            self.tournament.groups[group].play_group_games()
        #self.tournament.display_games()
        #self.tournament.display_standings()
        self.tournament.set_knockout_stage()
        self.tournament.play_knockout_stage()
        self.tournament.play_final_stage()
        self.tournament.display_final_stage()

    def compose(self) -> ComposeResult:
        yield Header()
        with VerticalScroll(id="simulation-scroll"):
            yield Static("Tournament Simulation Results", classes="title")
            
            # 1. Group Standings
            for group in self.tournament.groups:
                self.tournament.groups[group].play_group_games()    
            
            yield Static("\nGroup Stage Standings", classes="header")
            for group_name, group in self.tournament.groups.items():
                yield Static(f"\n{group_name}", classes="subheader")
                standings_header = f"{'Team':<15} {'Pts':>3} {'W':>2} {'L':>2} {'D':>2} {'GF':>3}:{'GA':<2} {'GD':>3}"
                yield Static(standings_header, classes="table-header")
                
                sorted_standings = sorted(group.points.items(), key=lambda x: x[1]["points"], reverse=True)
                for team, stats in sorted_standings:
                    line = (f"{team.name[:15]:<15} {stats['points']:>3} {stats['wins']:>2} "
                            f"{stats['losses']:>2} {stats['draws']:>2} {stats['goals_for']:>3}:"
                            f"{stats['goals_against']:<2} {stats['goal_difference']:>3}")
                    yield Static(f"  {line}")

            # 2. Knockout Stage
            self.tournament.set_knockout_stage()
            if hasattr(self.tournament, 'set_knockout_stage'):
                yield Static("\nKnockout Stage", classes="header")
                for game in self.tournament.knockout_stage:
                    game.play()
                    if game.winner is None:
                        flip = random.randint(0, 1)
                        if flip == 0:
                            game.winner = game.team_a
                            game.loser = game.team_b
                        else:
                            game.winner = game.team_b
                            game.loser = game.team_a
                    result = f"Game: {game.team_a.name} {game.score.get(game.team_a.name, 0)} - {game.score.get(game.team_b.name, 0)} {game.team_b.name}"
                    winner = f"Winner: [bold green]{game.winner.name}[/bold green]" if game.winner else "TBD"
                    yield Static(f"\n  {result}")
                    yield Static(f"  {winner}")

                    

            # 3. Final Stage
            self.tournament.set_final_stage()   
            self.tournament.play_final_stage()
            if hasattr(self.tournament, 'set_final_stage'):
                yield Static("\nFinal Stage", classes="header")
                # Usually final_stage[0] is Final, final_stage[1] is 3rd place if logic follows
                for i, game in enumerate(self.tournament.final_stage):
                    label = "Final" if i == 0 else "Third Place"
                    result = f"{game.team_a.name} {game.score.get(game.team_a.name, 0)} - {game.score.get(game.team_b.name, 0)} {game.team_b.name}"
                    winner = f"{label} Winner: [bold gold1]{game.winner.name}[/bold gold1]" if game.winner else f"{label} TBD"
                    yield Static(f"\n  ({label}) {result}")
                    yield Static(f"  {winner}")

        yield Footer()
        
if __name__ == "__main__":
    a = Athlete("Lionel Messi")
    b = Athlete("Diego Armando")
    s = Sport("Futbol",11,"FIFA")
    argentina  = Team("Argentina",s)
    argentina.add_athlete(a)
    argentina.add_athlete(b)
    print(argentina)
    print(repr(argentina))
    print(argentina.to_json())