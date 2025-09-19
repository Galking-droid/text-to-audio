# Text to Audio Converter

Herramienta web simple creada con Python (Flask) y gTTS para convertir texto de documentos a voz. Soporta archivos .txt, .docx y .pdf.

## Características

*   Convierte texto desde archivos `.txt`, `.docx` y `.pdf` a audio.
*   Permite seleccionar el idioma del audio (Español, Inglés, Francés, Alemán).
*   Descarga el audio generado en formato MP3.
*   Interfaz de usuario limpia y fácil de usar.

## Tecnologías Utilizadas

*   **Backend:**
    *   Python
    *   Flask
*   **Conversión de Texto a Voz:**
    *   gTTS (Google Text-to-Speech)
*   **Lectura de Archivos:**
    *   `python-docx` para archivos .docx
    *   `PyPDF2` para archivos .pdf
*   **Frontend:**
    *   HTML5
    *   CSS3

## Instalación y Uso

Sigue estos pasos para ejecutar el proyecto en tu máquina local.

1.  **Clona el repositorio:**
    ```bash
    git clone https://github.com/Galking-droid/text-to-audio.git
    cd text-to-audio
    ```

2.  **Crea y activa un entorno virtual:**
    ```bash
    # Crear el entorno
    python -m venv venv

    # Activar en Windows
    .\venv\Scripts\activate

    # Activar en macOS/Linux
    source venv/bin/activate
    ```

3.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Ejecuta la aplicación:**
    ```bash
    python app.py
    ```

5.  Abre tu navegador y ve a `http://127.0.0.1:5000`.

## Estructura del Proyecto

```
.text-to-audio/
├── app.py                # Lógica principal de la aplicación Flask
├── requirements.txt      # Dependencias de Python
├── .gitignore            # Archivos ignorados por Git
├── README.md             # Este archivo
├── static/
│   └── css/
│       └── style.css     # Hoja de estilos
├── templates/
│   └── index.html        # Interfaz de usuario (HTML)
└── temp_files/           # Directorio temporal para archivos subidos
```