from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window

from screens.admin_screen.admin_screen import AdminScreen
from screens.client_screen.start_screen import StartScreen


class FreeMagicMirrorApp(App):
    def build(self):
        Window.bind(on_keyboard=self.on_keyboard)

        sm = ScreenManager()

        admin = AdminScreen(name='admin')
        start = StartScreen(name='start')

        sm.add_widget(admin)
        sm.add_widget(start)

        sm.current = 'admin'

        return sm

    def on_keyboard(self, window, key, *args):
        """Handle ESC key to close app"""
        if key == 27:
            self.stop()
            return True
        return False

if __name__ == '__main__':
    FreeMagicMirrorApp().run()