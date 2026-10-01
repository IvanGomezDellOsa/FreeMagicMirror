[English](README.en.md) | [Español](README.md)

# FreeMagicMirror

A desktop application built with **Python, Kivy, OpenCV and PyInstaller**, designed for touch screens such as smart mirrors and photobooths. It allows capturing photos, customizing them with drawings and stickers, and saving the results.

 **Interface optimized for children's use:** animated videos, smooth transitions and large, intuitive controls.

## Project Status

FreeMagicMirror is already a fully functional application, packaged as a .exe executable for Windows via PyInstaller. Designed for portable distribution with no external dependencies, making it easy to use in environments without technical knowledge.
Optimized for touch screens of any size, it supports portrait and landscape orientation with dynamic window adjustment.

## ✨ Features

* **🎨 Fully Visual Interface**
  Specifically designed for children's use with animated videos, smooth transitions and large, intuitive controls.

* **📸 Complete Photo Flow**
  Photo capture with an animated countdown, editing with drawings and stickers, and automatic saving to a local gallery.

* **🖌️ Integrated Children's Editor**
  Allows drawing with multiple colors, adding scalable/rotatable stickers, and undoing changes.

* **🎥 Optimized Videos**
  Smooth playback of custom videos for each stage of the process (start, pose, countdown).

* **🖥️ Hidden Administration Panel**
  Camera configuration, screen orientation (portrait/landscape) and output monitor selection.

* **📱 Multi-Orientation Support**
  Works perfectly in both portrait and landscape format.

* **🔒 Kiosk Mode**
  Full screen without borders, admin access only through secret gestures (5 taps in a corner).

* **💾 Local Storage**
  All photos are saved in the gallery/ folder with an automatic incremental counter.

## 🎬 Demo Video (Click to watch)

<div align="center">
  <a href="https://www.youtube.com/watch?v=UjSz98p7nPk" target="_blank">
    <img src="https://img.youtube.com/vi/UjSz98p7nPk/maxresdefault.jpg" alt="Ver Demo de FreeMagicMirror" style="width:100%;">
  </a>
</div>
<br><br>
<br><br>
<p align="center">
  <b>Deployed in a real environment</b>
  <br><br>
  <img src="https://github.com/user-attachments/assets/201c4995-becb-4142-9c6c-399b9c772439" width="300" alt="Niños usando FreeMagicMirror">
</p>

## 🛠️ Technical Details

Developed in Python, it combines the power of OpenCV for real-time hardware management and the use of Kivy for a touch, smooth and animated user interface. With .exe packaging implemented with PyInstaller and Dockerization of the project.

### 💻 Tech Stack

| Technology | Role in the project |
| :--- | :--- |
| **Python 3.11** | Core language and business logic. |
| **Kivy 2.3.1** | GPU-accelerated UI framework. Handling of multitouch events and the application lifecycle. |
| **OpenCV** | Hardware abstraction for cameras (`cv2.VideoCapture`) and image matrix manipulation (rotation). |
| **FFPyPlayer** | High-performance video decoding integrated into Kivy for the attraction loops. |
| **Pillow (PIL)** | Image processing backend used for the final encoding and saving of the edited photo (`.png`). |
| **PyInstaller** | Binary packaging, management of hidden assets and compilation of dynamic dependencies for Windows. |
| **Docker** | Containerization of the application for an isolated, reproducible and operating-system-agnostic deployment. |

### Architecture

* ScreenManager with 4 modules: Admin, Start, Camera, PhotoEdit
* Global configuration system (paths, camera/orientation settings)
* Persistent counter for unique photo IDs
* PyInstaller environment detection for dynamic paths

### ⚙️ Implemented Features

#### Administration Panel
* Automatic camera detection with OpenCV (`cv2.VideoCapture` + `CAP_DSHOW`)
* Orientation configuration (portrait/landscape) with dynamic window adjustment
* Output monitor selector
* Applying configuration and switching to borderless fullscreen mode

#### Photo Capture
* Sequential video playback: intro → pose prompt → countdown
* Deferred camera initialization (post-video) at 10 FPS to avoid stuttering
* Visual countdown generated with Kivy
* Automatic saving to gallery/ with rotation according to the configured orientation

#### Photo Editor
* Free drawing canvas (`kivy.graphics.Line`) with 5 predefined colors
* Horizontal sticker gallery (ScrollView + dynamic BoxLayout)
* Stickers manipulable with Scatter (scale, rotation, multi-touch translation)
* Undo system (operations stack) and full erase
* Export to PNG (`export_to_png()`) with the full canvas (photo + drawings + stickers)

## 🚀 Installation and Use

### 📦 Option 1: Portable Executable (Recommended)
The simplest way to use FreeMagicMirror on Windows. It requires no Python installation or dependency setup.

1. Go to the **[Releases](https://github.com/IvanGomezDellOsa/FreeMagicMirror/releases)** section of the repository.
2. Download the `.zip` file of the latest version.
3. Unzip the folder and run `FreeMagicMirror.exe`.

### 🛠️ Option 2: Source Code (Developers)
Ideal for inspecting the code or making modifications.

```bash
# 1. Clonar el repositorio
git clone [https://github.com/IvanGomezDellOsa/FreeMagicMirror.git](https://github.com/IvanGomezDellOsa/FreeMagicMirror.git)
cd FreeMagicMirror

# 2. Crear entorno virtual e instalar dependencias
python -m venv .venv
.venv\Scripts\Activate.ps1  # En Windows (PowerShell)
# source .venv/bin/activate # En Linux/Mac

pip install -r requirements.txt

# 3. Ejecutar la aplicación
python main.py
```
### 🐳 Option 3: Docker (Experimental / Linux)
**Note:** This option is recommended mainly for Linux environments or integration testing, since running graphical interface (GUI) applications with hardware access (camera) from Docker on Windows requires advanced X11 server configurations.

* **Docker Hub:** [ivangomezdellosa/freemagicmirror](https://hub.docker.com/r/ivangomezdellosa/freemagicmirror)

```bash
docker run -it --rm --device=/dev/video0 -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix ivangomezdellosa/freemagicmirror:v1.1
```

## 👤 Author

**Iván Gómez Dell'Osa**

- GitHub: https://github.com/IvanGomezDellOsa
- Email: ivangomezdellosa@gmail.com
- Linkedin: https://www.linkedin.com/in/ivangomezdellosa/
