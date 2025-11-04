import cv2
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from screeninfo import get_monitors

from config import MirrorSettings, PHOTOS_DIR


class AdminScreen(Screen):
    """Admin interface for configuring camera, orientation, and display."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        Window.size = MirrorSettings.ADMIN_SIZE

        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        with layout.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            self.bg_rect = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self._update_bg, pos=self._update_bg)

        title = Label(
            text='FreeMagicMirror Configuration',
            font_size='32sp',
            size_hint=(1, 0.1),
            color=(0.2, 0.2, 0.2, 1)
        )
        layout.add_widget(title)

        camera_label = Label(
            text='Camera Selection',
            font_size='20sp',
            size_hint=(1, 0.05),
            color=(0.2, 0.2, 0.2, 1)
        )
        layout.add_widget(camera_label)

        self.detect_cameras()

        camera_options = [f"Camera {i}" for i in MirrorSettings.available_cameras]
        if not camera_options:
            camera_options = ["No cameras detected"]

        self.camera_spinner = Spinner(
            text=f"Camera {MirrorSettings.selected_camera}",
            values=camera_options,
            size_hint=(1, 0.08),
            font_size='18sp'
        )
        self.camera_spinner.bind(text=self.on_camera_selected)
        layout.add_widget(self.camera_spinner)

        orientation_label = Label(
            text='MagicMirror screen orientation',
            font_size='20sp',
            size_hint=(1, 0.05),
            color=(0.2, 0.2, 0.2, 1)
        )
        layout.add_widget(orientation_label)

        self.orientation_spinner = Spinner(
            text='Vertical',
            values=['Vertical', 'Horizontal'],
            size_hint=(1, 0.08),
            font_size='18sp'
        )
        self.orientation_spinner.bind(text=self.on_orientation_selected)
        layout.add_widget(self.orientation_spinner)

        screen_label = Label(
            text='Display Output (MagicMirror)',
            font_size='20sp',
            size_hint=(1, 0.05),
            color=(0.2, 0.2, 0.2, 1)
        )
        layout.add_widget(screen_label)

        screens = get_monitors()
        screen_options = [f"Screen {i + 1}" for i, _ in enumerate(screens)] or ["Screen 1"]

        self.screen_spinner = Spinner(
            text=f"Screen {MirrorSettings.selected_screen + 1}",
            values=screen_options,
            size_hint=(1, 0.08),
            font_size='18sp'
        )
        self.screen_spinner.bind(text=self.on_screen_selected)
        layout.add_widget(self.screen_spinner)

        photos_info = Label(
            text=f' Photos saved to:\n{PHOTOS_DIR}',
            font_size='16sp',
            size_hint=(1, 0.20),
            color=(0.3, 0.3, 0.3, 1),
            halign='center'
        )
        photos_info.bind(size=photos_info.setter('text_size'))
        layout.add_widget(photos_info)

        exit_info = Label(
            text='IMPORTANT:\n Press ESC to exit Magic Mirror mode or tap 5 times in top-left corner',
            font_size='18sp',
            size_hint=(1, 0.25),
            color=(0.3, 0.3, 0.3, 1),
            halign='center',
            valign='middle'
        )
        exit_info.bind(size=lambda instance, value: setattr(instance, 'text_size', value))
        layout.add_widget(exit_info)

        layout.add_widget(Label(size_hint=(1, 0.31)))

        start_button = Button(
            text='START MAGIC MIRROR',
            font_size='24sp',
            size_hint=(1, 0.2),
            background_color=(0.2, 0.8, 0.2, 1),
            background_normal=''
        )
        start_button.bind(on_press=self.start_mirror)
        layout.add_widget(start_button)

        self.add_widget(layout)

    def _update_bg(self, instance, value):
        """Update background rectangle size."""
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos

    def detect_cameras(self):
        """Detect available cameras using OpenCV."""
        available = []

        for i in range(5):
            cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
            if cap.isOpened():
                available.append(i)
                cap.release()

        MirrorSettings.available_cameras = available

        if not available:
            MirrorSettings.selected_camera = -1
            print("No cameras detected.")
        elif MirrorSettings.selected_camera not in available:
            MirrorSettings.selected_camera = available[0]

        print(f"Detected cameras: {available}")

    def on_camera_selected(self, spinner, text):
        """Handle camera selection from the spinner."""
        if "No cameras" in text:
            return
        try:
            camera_index = int(text.split()[-1])
            MirrorSettings.selected_camera = camera_index
            print(f"Camera selected: {camera_index}")
        except ValueError:
            print("Invalid camera selection.")

    def on_orientation_selected(self, spinner, text):
        """Handle orientation change."""
        if "vertical" in text:
            MirrorSettings.orientation = "vertical"
        else:
            MirrorSettings.orientation = "horizontal"

        MirrorSettings.orientation = text.lower()
        print(f"Orientation set to: {MirrorSettings.orientation}")

    def on_screen_selected(self, spinner, text):
        """Handle screen selection from the spinner."""
        try:
            MirrorSettings.selected_screen = int(text.split()[-1]) - 1
            print(f"Selected screen: {MirrorSettings.selected_screen}")
        except Exception:
            MirrorSettings.selected_screen = 0
            print("Invalid screen selection.")

    def start_mirror(self, instance):
        """Start Magic Mirror display on the selected screen."""
        if MirrorSettings.selected_camera == -1:
            print("Cannot start: No camera available.")
            return

        screens = get_monitors()
        index = getattr(MirrorSettings, "selected_screen", 0)

        if len(screens) > index:
            screen = screens[index]
            Window.left = screen.x
            Window.top = screen.y
            Window.size = (screen.width, screen.height)
            Window.borderless = True
            print(f"Opening Magic Mirror on Screen {index + 1}")
        else:
            Window.fullscreen = 'auto'
            print("Fullscreen on main screen.")

        print(f"Window resized to: {Window.size}")
        self.manager.current = 'start'
        print(f"Starting Magic Mirror with camera {MirrorSettings.selected_camera}")
        print(f"Orientation: {MirrorSettings.orientation}")