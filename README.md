[Español](README.md) | [English](README.en.md)

# FreeMagicMirror

Aplicación de escritorio construida con **Python, Kivy, OpenCV y PyInstaller**, diseñada para pantallas tactiles como espejos inteligentes y fotomatones. Permite capturar fotos, personalizarlas con dibujos y stickers, y guardar los resultados.

 **Interfaz optimizada para uso infantil:** videos animados, transiciones suaves y controles grandes e intuitivos.

## Estado del Proyecto

FreeMagicMirror ya es una aplicación completamente funcional, empaquetada como ejecutable .exe para Windows mediante PyInstaller. Diseñada para distribución portable sin dependencias externas, facilitando su uso en entornos sin conocimientos técnicos.
Optimizada para pantallas táctiles de cualquier tamaño, soporta orientación vertical y horizontal con ajuste dinámico de ventana.

## ✨ Características

* **🎨 Interfaz Totalmente Visual**
  Diseñada específicamente para uso infantil con videos animados, transiciones suaves y controles grandes e intuitivos.

* **📸 Flujo Fotográfico Completo**
  Captura de fotos con countdown animado, edición con dibujos y stickers, y guardado automático en galería local.

* **🖌️ Editor Infantil Integrado**
  Permite dibujar con múltiples colores, agregar stickers escalables/rotables, y deshacer cambios.

* **🎥 Videos Optimizados**
  Reproducción fluida de videos personalizados para cada etapa del proceso (inicio, pose, countdown).

* **🖥️ Panel de Administración Oculto**
  Configuración de cámara, orientación de pantalla (vertical/horizontal) y selección de monitor de salida.

* **📱 Soporte Multi-Orientación**
  Funciona perfectamente tanto en formato vertical como horizontal.

* **🔒 Modo Kiosko**
  Pantalla completa sin bordes, acceso admin solo mediante gestos secretos (5 toques en esquina).

* **💾 Almacenamiento Local**
  Todas las fotos se guardan en carpeta gallery/ con contador incremental automático.

## 🎬 Video Demostración (Click para ver)

<div align="center">
  <a href="https://www.youtube.com/watch?v=UjSz98p7nPk" target="_blank">
    <img src="https://img.youtube.com/vi/UjSz98p7nPk/maxresdefault.jpg" alt="Ver Demo de FreeMagicMirror" style="width:100%;">
  </a>
</div>
<br><br>
<br><br>
<p align="center">
  <b>Desplegado en entorno real</b>
  <br><br>
  <img src="https://github.com/user-attachments/assets/201c4995-becb-4142-9c6c-399b9c772439" width="300" alt="Niños usando FreeMagicMirror">
</p>

## 🛠️ Datos Técnicos

Desarrollado en Python, combina la potencia de OpenCV para la gestión de hardware en tiempo real y el uso Kivy para una interfaz de usuario tactil, fluida y animada. Con empaquetado .exe implementado con PyInstaller y Dockerizacion del proyecto.

### 💻 Stack Tecnológico

| Tecnología | Rol en el proyecto |
| :--- | :--- |
| **Python 3.11** | Lenguaje núcleo y lógica de negocio. |
| **Kivy 2.3.1** | Framework de UI acelerado por GPU. Manejo de eventos multitáctiles y ciclo de vida de la aplicación. |
| **OpenCV** | Abstracción de hardware para cámaras (`cv2.VideoCapture`) y manipulación de matrices de imagen (rotación). |
| **FFPyPlayer** | Decodificación de video de alto rendimiento integrada en Kivy para los bucles de atracción. |
| **Pillow (PIL)** | Backend de procesamiento de imágenes utilizado para la codificación y guardado final de la foto editada (`.png`). |
| **PyInstaller** | Empaquetado de binarios, gestión de assets ocultos y compilación de dependencias dinámicas para Windows. |
| **Docker** | Contenerización de la aplicación para un despliegue aislado, reproducible y agnóstico del sistema operativo. |

### Arquitectura

* ScreenManager con 4 módulos: Admin, Start, Camera, PhotoEdit
* Sistema de configuración global (rutas, settings de cámara/orientación)
* Contador persistente para IDs únicos de fotos
* Detección de entorno PyInstaller para rutas dinámicas

### ⚙️ Funcionalidades Implementadas

#### Panel de Administración
* Detección automática de cámaras con OpenCV (`cv2.VideoCapture` + `CAP_DSHOW`)
* Configuración de orientación (vertical/horizontal) con ajuste dinámico de ventana
* Selector de monitor de salida
* Aplicación de configuración y cambio a modo fullscreen borderless

#### Captura de Fotos
* Reproducción secuencial de videos: intro → pose prompt → countdown
* Inicialización diferida de cámara (post-video) a 10 FPS para evitar stuttering
* Countdown visual generado con Kivy
* Guardado automático en gallery/ con rotación según orientación configurada

#### Editor de Fotos
* Canvas de dibujo libre (`kivy.graphics.Line`) con 5 colores predefinidos
* Galería horizontal de stickers (ScrollView + BoxLayout dinámico)
* Stickers manipulables con Scatter (escala, rotación, traslación multi-touch)
* Sistema de deshacer (stack de operaciones) y borrado total
* Exportación a PNG (`export_to_png()`) con canvas completo (foto + dibujos + stickers)

## 🚀 Instalación y Uso

### 📦 Opción 1: Ejecutable Portable (Recomendado)
La forma más sencilla de utilizar FreeMagicMirror en Windows. No requiere instalación de Python ni configuración de dependencias.

1. Ve a la sección de **[Releases](https://github.com/IvanGomezDellOsa/FreeMagicMirror/releases)** del repositorio.
2. Descarga el archivo `.zip` de la última versión.
3. Descomprime la carpeta y ejecuta `FreeMagicMirror.exe`.

### 🛠️ Opción 2: Código Fuente (Desarrolladores)
Ideal para inspeccionar el código o realizar modificaciones.

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
### 🐳 Opción 3: Docker (Experimental / Linux)
**Nota:** Esta opción se recomienda principalmente para entornos Linux o pruebas de integración, ya que ejecutar aplicaciones con interfaz gráfica (GUI) y acceso a hardware (cámara) desde Docker en Windows requiere configuraciones avanzadas de servidores X11.

* **Docker Hub:** [ivangomezdellosa/freemagicmirror](https://hub.docker.com/r/ivangomezdellosa/freemagicmirror)

```bash
docker run -it --rm --device=/dev/video0 -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix ivangomezdellosa/freemagicmirror:v1.1
```

## 👤 Autor

**Iván Gómez Dell'Osa**

- GitHub: https://github.com/IvanGomezDellOsa
- Email: ivangomezdellosa@gmail.com
- Linkedin: https://www.linkedin.com/in/ivangomezdellosa/
