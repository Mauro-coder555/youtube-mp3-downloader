# 🎵 YouTube MP3 Downloader

Aplicación de escritorio simple creada con **Python + Tkinter** para descargar el audio de un video de YouTube en formato **MP3**.

> Proyecto desarrollado como parte del reto personal de crear un proyecto por día para practicar programación, constancia y desarrollo de herramientas útiles.

---

## ✅ Alcance del proyecto

Esta aplicación permite:

- Pegar un enlace de YouTube.
- Descargar el audio como archivo MP3.
- Guardar el archivo directamente en la carpeta **Descargas** del usuario.
- Cambiar la interfaz entre **Inglés** y **Español**.
- Abrir la carpeta de descargas desde la aplicación.
- Usar una interfaz gráfica simple, clara y amigable.

El proyecto está pensado como una herramienta local, sencilla y práctica para usuarios que no quieren usar comandos ni páginas con anuncios.

---

## 🧰 Tecnologías usadas

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-green?style=for-the-badge)
![yt-dlp](https://img.shields.io/badge/yt--dlp-Downloader-red?style=for-the-badge)
![FFmpeg](https://img.shields.io/badge/FFmpeg-Audio-orange?style=for-the-badge&logo=ffmpeg)

---

## 📁 Estructura del proyecto

```txt
youtube-mp3-downloader/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── ui.py
│   └── downloader.py
│
├── assets/
│   └── .gitkeep
│
├── downloads/
│   └── .gitkeep
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

## ⚙️ Instalación

### 1. Clonar o abrir el proyecto

```powershell
cd youtube-mp3-downloader
```

### 2. Crear entorno virtual

```powershell
python -m venv .venv
```

### 3. Activar entorno virtual en Windows

```powershell
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la activación, ejecutar una vez:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Luego volver a activar el entorno virtual.

### 4. Instalar dependencias

```powershell
pip install -r requirements.txt
```

---

## 🎧 Requisito importante: FFmpeg

Para convertir el audio a MP3, es necesario tener **FFmpeg** instalado.

Verificar instalación:

```powershell
ffmpeg -version
```

Instalar en Windows con `winget`:

```powershell
winget install Gyan.FFmpeg
```

Después de instalarlo, cerrar y abrir nuevamente la terminal.

---

## ▶️ Cómo usar la aplicación

Ejecutar desde la raíz del proyecto:

```powershell
python -m app.main
```

Luego:

1. Pegar un enlace de YouTube.
2. Elegir idioma si se desea.
3. Presionar **Download MP3 / Descargar MP3**.
4. El archivo se guardará automáticamente en la carpeta **Descargas**.

---

## 🌎 Idiomas disponibles

- 🇺🇸 English
- 🇪🇸 Español

---

## 📝 Notas

Esta herramienta debe usarse únicamente con videos propios, contenido de dominio público o contenido que tengas permiso para descargar.

---

## 🚀 Estado del proyecto

Proyecto funcional con interfaz gráfica, descarga de audio, conversión a MP3, soporte multiidioma y guardado automático en Descargas.
