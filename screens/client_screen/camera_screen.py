import cv2
from kivy.uix.screenmanager import Screen
from kivy.uix.video import Video
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.animation import Animation

from config import POSE_VIDEO_PATH, MirrorSettings, PHOTOS_DIR, get_next_id


class CameraScreen(Screen):
    """Handles camera preview, pose prompt, and photo capture."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = FloatLayout()
        self.camera = None
        self.current_frame = None

        self.video = Video(
            source=POSE_VIDEO_PATH,
            state='stop',
            options={'eos': 'stop'},
            fit_mode='fill',
            size_hint=(1, 1),
            volume=0
        )
        self.video.bind(eos=self.on_video_end)
        self.layout.add_widget(self.video)

        self.countdown_label = Label(
            text='',
            font_size='200sp',
            size_hint=(1, 1),
            color=(1, 1, 1, 1),
            bold=True,
            opacity=0
        )
        self.layout.add_widget(self.countdown_label)

        self.add_widget(self.layout)

        self.video_finished = False
        self.countdown_value = 5
        self.video_play_count = 0

    def on_enter(self):
        """Play the pose prompt video when entering this screen."""
        self.video.source = POSE_VIDEO_PATH
        self.video.state = 'play'
        self.video_play_count = 0
        self.video_finished = False
        self.video.opacity = 1
        print("Playing pose prompt video")

    def on_leave(self):
        """Release resources when leaving this screen."""
        if self.camera:
            self.camera.release()
            self.camera = None
            print("Camera released")

        Clock.unschedule(self.update_countdown)
        Clock.unschedule(self.update_camera_frame)

        if self.video.state == 'play':
            self.video.state = 'stop'

    def init_camera(self):
        """Initialize the selected camera."""
        camera_index = MirrorSettings.selected_camera
        self.camera = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)

        if not self.camera.isOpened():
            print(f"Failed to open camera {camera_index}")
            return

        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        Clock.schedule_interval(self.update_camera_frame, 1.0 / 30.0)
        print(f"Camera {camera_index} initialized")

    def update_camera_frame(self, dt):
        """Update the current camera frame."""
        if not self.camera:
            return

        ret, frame = self.camera.read()
        if ret:
            self.current_frame = frame

    def on_video_end(self, instance, value):
        """Handle pose video end and start countdown after several loops."""
        self.video_play_count += 1
        if self.video_play_count < 3:
            self.video.seek(0)
            self.video.state = 'play'
        else:
            if not self.video_finished:
                self.video_finished = True
                fade_out = Animation(opacity=0, duration=0.3)
                fade_out.bind(on_complete=lambda *args: self.start_countdown())
                fade_out.start(self.video)

    def start_countdown(self):
        """Start countdown before capturing a photo."""
        self.init_camera()
        Clock.schedule_interval(self.update_camera_frame, 1.0 / 10.0)
        self.countdown_label.opacity = 1
        self.countdown_value = 5
        Clock.schedule_interval(self.update_countdown, 1.0)

    def update_countdown(self, dt):
        """Update countdown display each second."""
        if self.countdown_value > 0:
            self.countdown_label.text = str(self.countdown_value)
            self.countdown_value -= 1
        else:
            Clock.unschedule(self.update_countdown)
            self.countdown_label.opacity = 0
            self.capture_photo()

    def capture_photo(self):
        """Capture photo and save it to the gallery."""
        Clock.unschedule(self.update_camera_frame)
        print("Capturing photo...")

        if self.current_frame is not None:
            photo_id = get_next_id()
            filename = f"photo_{photo_id}.png"
            filepath = PHOTOS_DIR / filename
            frame_to_save = self.current_frame

            if MirrorSettings.orientation == "vertical":
                frame_to_save = cv2.rotate(frame_to_save, cv2.ROTATE_90_CLOCKWISE)

            cv2.imwrite(str(filepath), frame_to_save)
            print(f"Photo saved: {filepath}")
            print(f"Photo ID: {photo_id}")
            Clock.schedule_once(lambda dt: self.go_to_edit(str(filepath)), 0.3)
        else:
            print("No frame available")

    def go_to_edit(self, photo_path):
        """Switch to photo edit screen after saving the photo."""
        if self.camera:
            self.camera.release()
            self.camera = None
            print("Camera released for edit")

        Clock.unschedule(self.update_camera_frame)
        Clock.unschedule(self.update_countdown)

        self.video.state = 'stop'

        edit_screen = self.manager.get_screen('photo_edit')
        edit_screen.photo_path = photo_path

        self.manager.current = 'photo_edit'
        print(f"Transitioning to edit screen with photo: {photo_path}")