from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ObjectProperty
from random import randint
from kivy.clock import Clock
from kivy.core.window import Window


def collision(a, b):
    if a.right < b.x:
        return False
    if a.x > b.right:
        return False
    if a.top < b.gap_top and a.y > b.gap_bottom:
        return False
    return True


class Bird(Widget):
    pass


class Pipe(Widget):
    pass


class Background(Widget):
    def __init__(self, **kwargs):
        super(Background, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'spacebar':
            self.jump()

    bird = ObjectProperty(None)
    pipe1 = ObjectProperty(None)
    pipe2 = ObjectProperty(None)

    bird_speed = 0
    game_speed = 3
    score = NumericProperty(0)

    def update(self, dt):
        self.game_speed = 3 + self.score * .5
        self.pipe1.x -= self.game_speed
        self.pipe2.x -= self.game_speed
        self.bird.y += self.bird_speed
        self.bird_speed -= .5

        if self.pipe1.x < -200:
            self.pipe1.x = self.width
            self.pipe1.center_y = randint(-600, -100)
            self.score += 1
        if self.pipe2.x < -200:
            self.pipe2.x = self.width
            self.pipe2.center_y = randint(-600, -100)
            self.score += 1

        if self.bird.y < 0:
            self.game_over()

        if collision(self.bird, self.pipe1) or collision(self.bird, self.pipe2):
            self.game_over()

    def jump(self):
        self.bird_speed = 10

    def game_over(self):
        self.reset_game()

    def reset_game(self):
        self.score = 0
        self.bird_speed = 0
        self.bird.center_y = self.center_y
        self.pipe1.center_x = self.center_x - 100
        self.pipe1.center_y = -400
        self.pipe2.center_x = self.width
        self.pipe2.center_y = -400


class Game(App):
    def build(self):
        display = Background()
        Clock.schedule_interval(display.update, 1/60)
        return display


if __name__ == '__main__':
    Game().run()
