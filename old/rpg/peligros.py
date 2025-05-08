import arcade

class Bullet(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__(":resources:images/space_shooter/laserBlue01.png", 0.5)
        self.center_x = x
        self.center_y = y
        self.change_y = -5
        self.change_x = -1

    def update(self):
        self.center_y += self.change_y
        self.center_x += self.change_x
        if self.bottom < 0:
            self.remove_from_sprite_lists()
