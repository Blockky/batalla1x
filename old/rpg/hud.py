import arcade

class CombatHUD:
    def __init__(self, game_view):
        self.visible = False
        self.game_view = game_view
        self.buttons = ["Atacar", "Usar Ítem", "No hacer nada"]
        self.selected = 0
        self.button_height = 40  # Altura de cada opción en el menú
        self.button_spacing = 10  # Espaciado entre las opciones

    def setup(self):
        self.selected = 0
        self.visible = False

    def show(self):
        self.visible = True

    def draw(self):
        if not self.visible:
            return

        arcade.draw_rectangle_filled(400, 100, 700, 150, arcade.color.DARK_BLUE_GRAY)

        for i, option in enumerate(self.buttons):
            color = arcade.color.YELLOW if i == self.selected else arcade.color.WHITE
            # Dibuja cada opción de menú
            arcade.draw_text(option, 200, 100 + i * (self.button_height + self.button_spacing), color, 18)

    def on_key_press(self, key):
        if not self.visible:
            return

        # Usar flechas arriba y abajo para seleccionar la opción
        if key == arcade.key.UP:
            self.selected = (self.selected - 1) % len(self.buttons)
        elif key == arcade.key.DOWN:
            self.selected = (self.selected + 1) % len(self.buttons)

        # Si presionas ENTER, ejecutas la acción seleccionada
        elif key == arcade.key.ENTER or key == arcade.key.RETURN:
            self.execute_action()

    def on_mouse_press(self, x, y, button, modifiers):
        if not self.visible:
            return

        # Verificar si el clic fue dentro de una de las opciones
        for i, option in enumerate(self.buttons):
            option_top = 100 + i * (self.button_height + self.button_spacing)
            option_bottom = option_top + self.button_height
            # Si el clic está dentro de los límites de la opción
            if 200 <= x <= 600 and option_top <= y <= option_bottom:
                self.selected = i
                self.execute_action()

    def execute_action(self):
        action = self.buttons[self.selected]
        print(f"Elegiste: {action}")
        self.visible = False
        self.game_view.start_dialog([f"Elegiste: {action}", "¡Fin del combate!"])
        self.game_view.state = "dialog"
