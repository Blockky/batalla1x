import arcade
import random
from peligros import Bullet
from hud import CombatHUD

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.player = None
        self.npc = None
        self.bullets = arcade.SpriteList()
        self.state = "exploration"  # other states: dialog, bullet_hell, combat_menu
        self.dialog_text = []
        self.dialog_index = 0
        self.dialog_box_visible = False
        self.combat_timer = 0
        self.hud = CombatHUD(self)

    def setup(self):
        self.npc_list = arcade.SpriteList()
        npc = arcade.Sprite(":resources:images/animated_characters/male_person/malePerson_idle.png", scale=1)
        npc.center_x = 400
        npc.center_y = 300
        self.npc_list.append(npc)

        self.player = arcade.Sprite(":resources:images/animated_characters/female_person/femalePerson_idle.png", 0.5)
        self.player.center_x = 100
        self.player.center_y = 300

        self.npc = arcade.Sprite(":resources:images/animated_characters/zombie/zombie_idle.png", 0.5)
        self.npc.center_x = 400
        self.npc.center_y = 300

        self.state = "exploration"
        self.dialog_text = []
        self.dialog_index = 0
        self.dialog_box_visible = False
        self.bullets = arcade.SpriteList()
        self.combat_timer = 0
        self.hud.setup()

    def on_show(self):
        self.setup()

    def on_draw(self):
        arcade.start_render()
        self.player.draw()
        self.npc_list.draw()

        if self.state == "bullet_hell":
            self.bullets.draw()

        if self.dialog_box_visible:
            arcade.draw_rectangle_filled(400, 100, 700, 150, arcade.color.BROWN)
            arcade.draw_text(self.dialog_text[self.dialog_index], 100, 100, arcade.color.WHITE, 14, width=600)

        if self.state == "combat_menu":
            self.hud.draw()

    def update(self, delta_time):
        if self.state == "bullet_hell":
            self.combat_timer += delta_time
            self.bullets.update()

            if self.combat_timer > 8.0:
                self.state = "combat_menu"
                self.hud.show()
                self.bullets = arcade.SpriteList()

            if random.random() < 0.2:
                self.spawn_bullet()

        self.player.update()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.player.change_y = 2
        elif key == arcade.key.S:
            self.player.change_y = -2
        elif key == arcade.key.A:
            self.player.change_x = -2
        elif key == arcade.key.D:
            self.player.change_x = 2

        # Si tienes interacción con E, la puedes mantener
        if key == arcade.key.E:
            if self.state == "exploration":
                hit = arcade.check_for_collision_with_list(self.player, self.npc_list)
                if hit:
                    self.start_dialog(["¡Prepárate para hgjhghjghjgjhluchar!"])
                    self.state = "dialog"

        if key == arcade.key.E:
            if self.state == "dialog":
                self.advance_dialog()

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.W, arcade.key.S):
            self.player.change_y = 0
        elif key in (arcade.key.A, arcade.key.D):
            self.player.change_x = 0

    def start_dialog(self, lines):
        self.dialog_text = lines
        self.dialog_index = 0
        self.dialog_box_visible = True
        self.state = "dialog"

    def advance_dialog(self):
        self.dialog_index += 1
        if self.dialog_index >= len(self.dialog_text):
            self.dialog_box_visible = False
            self.start_bullet_hell()

    def start_bullet_hell(self):
        self.state = "bullet_hell"
        self.combat_timer = 0

    def spawn_bullet(self):
        x = random.randint(0, SCREEN_WIDTH)
        bullet = Bullet(x, SCREEN_HEIGHT)
        self.bullets.append(bullet)
