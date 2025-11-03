from kivy.uix.screenmanager import Screen
from kivy.uix.video import Video
from kivy.core.window import Window
from config import START_VIDEO_PATH, MirrorSettings
import time
import os


class StartScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.corner_touches = []

        keep_ratio = False
        self.video = Video(
            source=START_VIDEO_PATH,
            state='play',
            options={'eos': 'loop'},
            allow_stretch=True,
            keep_ratio=keep_ratio,
            size_hint=(1, 1),
            volume=0
        )

        self.add_widget(self.video)

    def on_enter(self):
        """Called when entering this screen"""
        self.video.state = 'play'

    def on_touch_down(self, touch):
        """Detect touches"""
        if touch.x < 150 and touch.y > Window.height - 150:
            current_time = time.time()
            self.corner_touches.append(current_time)
            self.corner_touches = [t for t in self.corner_touches if current_time - t < 2]

            if len(self.corner_touches) >= 3:
                print("✓ Admin access")
                self.return_to_admin()
                self.corner_touches = []
                return True

        print("✓ Screen touched - going to camera")
        #Aca deriva a la camara post videos TODO: self.manager.current = 'camera'
        print("⚠️ camera_screen not implemented yet")
        return True

    def return_to_admin(self):
        """Return to admin"""
        from config import MirrorSettings
        Window.size = MirrorSettings.ADMIN_SIZE
        self.manager.current = 'admin'