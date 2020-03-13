from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.core.audio import SoundLoader


def collides(rect1, rect2):
    r1x = rect1[0][0]
    r1y = rect1[0][1]
    r2x = rect2[0][0]
    r2y = rect2[0][1]
    r1w = rect1[1][0]
    r1h = rect1[1][1]
    r2w = rect2[1][0]
    r2h = rect2[1][1]

    if (r1x < r2x + r2w and r1x + r1w > r2x and r1y < r2y + r2h and r1y + r1h > r2y):
        return True
    else:
        return False


class GameWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard = Window.request_keyboard(
            self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self._keyboard.bind(on_key_up=self._on_key_up)
        with self.canvas:
            self.player = Rectangle(
                source='player.png', pos=(0, 0), size=(100, 100))
            self.enemy = Rectangle(
                source='legault_confident.jpeg', pos=(400, 0), size=(150, 100))

        self.keysPressed = set()

        Clock.schedule_interval(self.move_step, 0)
        # Source : https://www.youtube.com/watch?v=iBk0-xTvjT0
        self.background_music = SoundLoader.load(
            'L_hymne_a_L_hiver_Quebecois.wav')
        self.tabarnacle_sound = SoundLoader.load('tabarnacle.wav')
        self.background_music.play()

        # import ipdb
        # ipdb.set_trace()

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard.unbind(_on_key_up=self._on_key_up)
        self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        self.keysPressed.add(keycode)

    def _on_key_up(self, keyboard, keycode):
        if keycode in self.keysPressed:
            self.keysPressed.remove(keycode)

    def move_step(self, dt):

        currentx = self.player.pos[0]
        currenty = self.player.pos[1]

        step_size = 200 * dt

        # 273 up
        # 274 down

        # import ipdb
        # ipdb.set_trace()

        if (275, 'right') in self.keysPressed:
            currentx += step_size

        if (276, 'left') in self.keysPressed:
            currentx -= step_size

        self.player.pos = (currentx, currenty)

        if collides((self.player.pos, self.player.size), (self.enemy.pos, self.enemy.size)):
            print(f"Colliding!{self.player.pos}")
            self.tabarnacle_sound.play()


class MyApp(App):
    def build(self):
        return GameWidget()


if __name__ == '__main__':
    app = MyApp()
    app.run()
