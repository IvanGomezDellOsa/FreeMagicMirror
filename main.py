from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window

from screens.admin_screen.admin_screen import AdminScreen
from screens.client_screen.start_screen import StartScreen
from screens.client_screen.camera_screen import CameraScreen
from screens.client_screen.photo_edit_screen import PhotoEditScreen


class FreeMagicMirrorApp(App):
    """Main application class for the FreeMagicMirror"""

    def build(self):
        """Initialize and configure the screen manager."""
        Window.bind(on_keyboard=self.on_keyboard)

        sm = ScreenManager()

        admin = AdminScreen(name='admin')
        start = StartScreen(name='start')
        camera = CameraScreen(name='camera')
        photo_edit = PhotoEditScreen(name='photo_edit')

        sm.add_widget(admin)
        sm.add_widget(start)
        sm.add_widget(camera)
        sm.add_widget(photo_edit)

        sm.current = 'admin'
        return sm

    def on_keyboard(self, window, key, *args):
        """Close the app when the ESC key is pressed."""
        if key == 27:
            self.stop()
            return True
        return False


if __name__ == '__main__':
    FreeMagicMirrorApp().run()