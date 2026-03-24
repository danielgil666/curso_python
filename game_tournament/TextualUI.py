from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Static
from textual.containers import Vertical, VerticalScroll
from textual.screen import Screen
import os
from Tournament import Tournament
import random

class TextualUI(App):
    CSS = """
    Screen {
        align: center middle;
    }

    #menu-container {
        width: 40;
        height: auto;
        border: thick $primary;
        padding: 1;
        background: $surface;
    }

    #tournament-scroll {
        padding: 2;
        border: solid $accent;
    }

    .title {
        text-align: center;
        width: 100%;
        text-style: bold;
        background: $primary;
        color: $text;
        margin-bottom: 1;
    }

    .header {
        text-style: bold underline;
        color: $secondary;
        margin-top: 1;
    }

    .subheader {
        text-style: italic;
        color: $accent;
    }

    #groups-scroll {
        padding: 2;
        border: solid $secondary;
    }

    #groups-scroll .subheader {
        background: $surface;
        color: $text;
        text-style: bold;
        padding-left: 2;
    }

    #games-scroll, #simulation-scroll {
        padding: 2;
    }

    .table-header {
        background: $surface;
        color: $text;
        text-style: bold;
        padding-left: 2;
    }

    Button {
        width: 100%;
        margin-bottom: 1;
    }

    Static {
        margin-bottom: 0;
    }
    """

    BINDINGS = [
        ("l", "load", "[L]oad"),
        ("t", "display_tournament", "[T]ournament"),
        ("g", "display_groups", "[G]roups"),
        ("m", "display_games", "Ga[m]es"),
        ("p", "play", "[P]lay"),
        ("q", "exit_app", "[Q]uit"),
        ("up", "focus_previous", "Focus Previous"),
        ("down", "focus_next", "Focus Next"),
    ]

    def __init__(self):
        super().__init__()
        self.tournament = None  
        self.current_file = None
    
    def on_mount(self):
        self.query_one("#load").focus()
    
    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="menu-container"):
            yield Button("Load Tournament", id="load", variant="primary")
            yield Button("Tournament", id="tournament", variant="secondary")
            yield Button("Groups", id="groups", variant="secondary")
            yield Button("Games", id="games", variant="secondary")
            yield Button("Play", id="play", variant="success")
            yield Button("Quit", id="quit", variant="error")
        yield Footer()  
    def action_load(self):
        self.get_tournament_json()
    def action_display_tournament(self):
        self.display_tournament()
    def action_display_groups(self):
        self.display_groups()
    def action_display_games(self):
        self.display_games()
    def action_play(self):
        self.play_games()
    def action_quit(self):
        self.exit_app()
    def set_current_file(self, file_path:str):
        self.current_file = file_path
    def open_tournament(self):
        if self.current_file and os.path.exists(self.current_file):
            self.tournament = Tournament("Tournament")
            self.tournament.load_from_json(self.current_file)
            self.tournament.set_group_stage()
            self.notify(f"Tournament {self.tournament.name} loaded successfully")
        else:
            self.notify("No tournament file selected")
    def display_tournament(self):
        if self.tournament:
            self.notify("Here goes the tournament screen")
            #self.push_screen(TournamentScreen(self.tournament))
        else:
            self.notify("No tournament loaded")
    def display_groups(self):
        if self.tournament:
            self.notify("Here goes the groups screen")
            #self.push_screen(GroupsScreen(self.tournament))
        else:
            self.notify("No tournament loaded")
    def display_games(self):
        if self.tournament:
            self.notify("Here goes the games screen")
            #self.push_screen(GamesScreen(self.tournament))
        else:
            self.notify("No tournament loaded")
    def play_games(self):
        if self.tournament:
            self.push_screen(PlayGamesScreen(self.tournament))
        else:
            self.notify("No tournament loaded")
    def exit_app(self):
        self.exit()
    def display_menu(self):
        self.run()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "load":
            self.get_tournament_json()
        elif button_id == "display":
            self.display_tournament()
        elif button_id == "groups":
            self.display_groups()
        elif button_id == "games":
            self.display_games()
        elif button_id == "play":
            self.play_games()
        elif button_id == "exit":
            self.exit_app()
            
            class TournamentScreen(Screen):
    """Screen to display tournament details."""
    BINDINGS = [("escape", "app.pop_screen", "Back to Menu")]

    def __init__(self, tournament):
        super().__init__()
        self.tournament = tournament

    def compose(self) -> ComposeResult:
        yield Header()
        with VerticalScroll(id="tournament-scroll"):
            yield Static(f"Tournament: {self.tournament.name}", classes="title")
            
            yield Static("\nGroups", classes="header")
            for group_name, group in self.tournament.groups.items():
                yield Static(f"\n{group_name}", classes="subheader")
                for team in group.teams:
                    yield Static(f"  • {team.name}")
            
            yield Static("\nGames", classes="header")
            # Checking both tournament.games and group games
            for group_name, group in self.tournament.groups.items():
                if group.games:
                    yield Static(f"\n{group_name} Games", classes="subheader")
                    for game in group.games:
                        yield Static(f"  - {game}")
            
            if self.tournament.games:
                yield Static("\nTournament Games", classes="subheader")
                for game in self.tournament.games:
                    yield Static(f"  - {game}")

        yield Footer()
if __name__ == "__main__":
    app = TextualUI()
    app.set_current_file("tournament.json")
    app.open_tournament()   
    app.run()
 

