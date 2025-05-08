import arcade
from game_view import GameView

def main():
    window = arcade.Window(800, 600, "Bullet Hell RPG")
    game_view = GameView()
    window.show_view(game_view)
    arcade.run()

if __name__ == "__main__":
    main()
