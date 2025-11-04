from pathlib import Path
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image as KivyImage
from kivy.uix.scatter import Scatter
from kivy.graphics import Color, Line
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView

from config import PHOTOS_DIR, ASSETS_DIR


class DrawingCanvas(Widget):
    """Canvas widget for freehand drawing."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.drawing = False
        self.current_color = (1, 0, 0, 1)
        self.line_width = 5
        self.lines_batch = []

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return False
        self.drawing = True
        with self.canvas:
            Color(*self.current_color)
            touch.ud['line'] = Line(points=(touch.x, touch.y), width=self.line_width)
            self.lines_batch.append((self.current_color, touch.ud['line']))
        return True

    def on_touch_move(self, touch):
        if not self.drawing or 'line' not in touch.ud:
            return False
        touch.ud['line'].points += [touch.x, touch.y]
        return True

    def on_touch_up(self, touch):
        if 'line' in touch.ud:
            self.drawing = False
        return True

    def set_color(self, color):
        """Change the current drawing color."""
        self.current_color = color

    def clear_last(self):
        """Undo the last drawn line."""
        if self.lines_batch:
            _, line = self.lines_batch.pop()
            self.canvas.remove(line)

    def clear_all(self):
        """Clear all drawings."""
        self.canvas.clear()
        self.lines_batch = []


class PhotoEditScreen(Screen):
    """Screen for drawing and adding stickers on photos."""
    photo_path = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.main_layout = FloatLayout()

        self.photo_widget = KivyImage(
            size_hint=(1, 1),
            allow_stretch=True,
            keep_ratio=True
        )
        self.main_layout.add_widget(self.photo_widget)

        self.drawing_canvas = DrawingCanvas(size_hint=(1, 1))
        self.main_layout.add_widget(self.drawing_canvas)

        self.stickers_container = FloatLayout(size_hint=(1, 1))
        self.main_layout.add_widget(self.stickers_container)

        self.sticker_dir = ASSETS_DIR / "stickers"
        self.sticker_dir.mkdir(exist_ok=True)
        self.available_stickers = []
        self.load_stickers()

        self.panel = None
        self.sticker_scroll = None
        self.create_control_panel()
        self.create_sticker_tray()

        self.add_widget(self.main_layout)

    def create_control_panel(self):
        """Create the control panel with drawing tools."""
        self.panel = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.12),
            pos_hint={'x': 0, 'y': 0},
            padding=10,
            spacing=10
        )

        colors = [
            ('Rojo', (1, 0, 0, 1)),
            ('Azul', (0, 0, 1, 1)),
            ('Verde', (0, 1, 0, 1)),
            ('Amarillo', (1, 1, 0, 1)),
            ('Negro', (0, 0, 0, 1)),
        ]

        for name, color in colors:
            btn = Button(
                text=name,
                background_color=color,
                background_normal=''
            )
            btn.bind(on_press=lambda b, c=color: self.drawing_canvas.set_color(c))
            self.panel.add_widget(btn)

        undo_btn = Button(
            text='Borrar',
            background_color=(0.5, 0.5, 0.5, 1),
            background_normal=''
        )
        undo_btn.bind(on_press=lambda x: self.drawing_canvas.clear_last())
        self.panel.add_widget(undo_btn)

        clear_btn = Button(
            text='Borrar Todo',
            background_color=(0.7, 0.3, 0.3, 1),
            background_normal=''
        )
        clear_btn.bind(on_press=lambda x: (self.drawing_canvas.clear_all(), self.stickers_container.clear_widgets()))
        self.panel.add_widget(clear_btn)

        save_btn = Button(
            text='Sacar otra foto',
            background_color=(0.2, 0.8, 0.2, 1),
            background_normal='',
            size_hint_x=1.5
        )
        save_btn.bind(on_press=self.save_and_continue)
        self.panel.add_widget(save_btn)

        self.main_layout.add_widget(self.panel)

    def create_sticker_tray(self):
        """Create the horizontal sticker tray."""
        self.sticker_scroll = ScrollView(
            size_hint=(1, 0.1),
            pos_hint={'x': 0, 'y': 0.12},
            do_scroll_x=True,
            do_scroll_y=False
        )

        sticker_tray = BoxLayout(
            orientation='horizontal',
            size_hint_x=None,
            padding=(10, 5),
            spacing=10
        )
        sticker_tray.bind(minimum_width=sticker_tray.setter('width'))

        for sticker_path in self.available_stickers:
            sticker_btn = Button(
                background_normal=str(sticker_path),
                size_hint=(None, 1),
                width=sticker_tray.height,
                border=(0, 0, 0, 0)
            )
            sticker_btn.bind(on_press=lambda x, path=sticker_path: self.add_sticker_from_tray(path))
            sticker_tray.add_widget(sticker_btn)

        self.sticker_scroll.add_widget(sticker_tray)
        self.main_layout.add_widget(self.sticker_scroll)

    def load_stickers(self):
        """Load sticker images from the assets folder."""
        if self.sticker_dir.exists():
            self.available_stickers = list(self.sticker_dir.glob("*.png"))
        if not self.available_stickers:
            print("No stickers found. Add PNG images to assets/stickers/")

    def add_sticker_from_tray(self, sticker_path):
        """Add a sticker to the photo."""
        try:
            scatter = Scatter(
                size_hint=(None, None),
                size=(150, 150),
                do_rotation=True,
                do_scale=True,
                do_translation=True
            )

            sticker_img = KivyImage(
                source=str(sticker_path),
                size=(150, 150),
                allow_stretch=True
            )

            scatter.add_widget(sticker_img)
            scatter.center = self.center
            self.stickers_container.add_widget(scatter)
            print(f"Added sticker: {sticker_path.name}")
        except Exception as e:
            print(f"Error adding sticker: {e}")

    def on_enter(self):
        """Load the selected photo when entering this screen."""
        if self.photo_path:
            Clock.schedule_once(self._load_photo, 0)

    def _load_photo(self, dt):
        """Load photo asynchronously."""
        try:
            self.photo_widget.source = self.photo_path
            self.photo_widget.reload()
            print(f"Photo loaded for editing: {self.photo_path}")
        except Exception as e:
            print(f"Error loading photo: {e}")

    def save_and_continue(self, instance):
        """Save the edited photo and return to start screen."""
        print("Saving edited photo...")
        Clock.schedule_once(self._save_photo, 0)

    def _save_photo(self, dt):
        """Save the edited photo to file."""
        try:
            if not self.photo_widget.texture:
                print("No photo texture available")
                return

            original_path = Path(self.photo_path)
            edited_path = original_path.parent / f"{original_path.stem}_edited{original_path.suffix}"

            self.panel.opacity = 0
            self.sticker_scroll.opacity = 0

            self.main_layout.export_to_png(str(edited_path))

            self.panel.opacity = 1
            self.sticker_scroll.opacity = 1

            print(f"Edited photo saved: {edited_path}")
            Clock.schedule_once(self._cleanup_and_return, 0.5)
        except Exception as e:
            print(f"Error saving photo: {e}")
            self._cleanup_and_return(0)

    def _cleanup_and_return(self, dt):
        """Clear data and return to the start screen."""
        self.drawing_canvas.clear_all()
        self.stickers_container.clear_widgets()
        self.photo_widget.source = ""
        self.photo_path = ""
        self.manager.current = 'start'
        print("Returned to start screen")

    def on_leave(self):
        """Cleanup when leaving the screen."""
        pass