from kivy.uix.screenmanager import Screen
from kivy.uix.video import Video
from kivy.core.window import Window
from config import START_VIDEO_PATH, MirrorSettings
import time
import os


class StartScreen(Screen):
    """Start screen displaying the looping intro video."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.corner_touches = []

        self.video = Video(
            source=START_VIDEO_PATH,
            state='play',
            options={'eos': 'loop'},
            fit_mode='fill',
            size_hint=(1, 1),
            volume=0
        )
        self.add_widget(self.video)

    def on_enter(self):
        """Play the intro video when entering this screen."""
        self.video.state = 'play'

    def on_touch_down(self, touch):
        """Handle screen touch events."""
        if touch.x < 150 and touch.y > Window.height - 150:
            current_time = time.time()
            self.corner_touches.append(current_time)
            self.corner_touches = [t for t in self.corner_touches if current_time - t < 2]

            if len(self.corner_touches) >= 5:
                print("Admin access")
                self.return_to_admin()
                self.corner_touches = []
                return True

        print("Screen touched - going to camera")
        self.manager.current = 'camera'
        return True

    def return_to_admin(self):
        """Return to the admin screen."""
        from config import MirrorSettings
        Window.size = MirrorSettings.ADMIN_SIZE
        self.manager.current = 'admin'