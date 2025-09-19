from flask import Flask, render_template, request, send_file, after_this_request
import pyttsx3
import os
import uuid  # To generate unique filenames

# Importar las librerías para manejar archivos
import docx
from PyPDF2 import PdfReader
import ezodf
from striprtf.striprtf import rtf_to_text

app = Flask(__name__)

# Directorio para guardar los archivos temporales
UPLOAD_FOLDER = 'temp_files'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_available_voices():
    """Gets a list of available voices from pyttsx3."""
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.stop()
        return [{'id': voice.id, 'name': voice.name} for voice in voices]
    except Exception as e:
        print(f"Could not initialize pyttsx3: {e}")
        return []

@app.route('/')
def index():
    """Renders the main page with the list of available voices."""
    voices = get_available_voices()
    return render_template('index.html', voices=voices)

def get_text_from_file(file_path):
    text = ""
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == '.txt':
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    elif file_extension == '.docx':
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    elif file_extension == '.pdf':
        try:
            with open(file_path, 'rb') as f:
                reader = PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text()
        except Exception as e:
            print(f"Error al leer el archivo PDF: {e}")
            text = ""
    elif file_extension == '.odt':
        try:
            doc = ezodf.opendoc(file_path)
            text = ""
            for p in doc.body:
                if isinstance(p, ezodf.text.Paragraph):
                    text += p.plaintext()
        except Exception as e:
            print(f"Error al leer el archivo ODT: {e}")
            text = ""
    elif file_extension == '.rtf':
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                rtf_content = f.read()
                text = rtf_to_text(rtf_content)
        except Exception as e:
            print(f"Error al leer el archivo RTF: {e}")
            text = ""
    return text

@app.route('/convertir', methods=['POST'])
def convertir_a_audio():
    input_method = request.form.get('input_method')
    voice_id = request.form.get('voice')
    texto_extraido = ""

    if input_method == 'text':
        texto_extraido = request.form.get('text_input')
    elif input_method == 'file':
        if 'file' not in request.files:
            return "No se encontró el archivo.", 400
        file = request.files['file']
        if file.filename == '':
            return "No se seleccionó ningún archivo.", 400
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            texto_extraido = get_text_from_file(file_path)
            os.remove(file_path)

    if texto_extraido and texto_extraido.strip():
        try:
            engine = pyttsx3.init()
            
            if voice_id:
                engine.setProperty('voice', voice_id)

            temp_audio_filename = f"{uuid.uuid4()}.mp3"
            temp_audio_path = os.path.join(app.config['UPLOAD_FOLDER'], temp_audio_filename)

            engine.save_to_file(texto_extraido, temp_audio_path)
            engine.runAndWait()
            engine.stop()

            @after_this_request
            def cleanup(response):
                try:
                    os.remove(temp_audio_path)
                except Exception as e:
                    print(f"Error removing temporary audio file: {e}")
                return response

            return send_file(
                temp_audio_path,
                mimetype='audio/mp3',
                as_attachment=True,
                download_name="audio_generado.mp3"
            )
        except Exception as e:
            print(f"Error during audio generation: {e}")
            return "Ocurrió un error al generar el audio.", 500
    else:
        return "No se proporcionó texto o no se pudo extraer texto del archivo.", 400

if __name__ == '__main__':
    app.run(debug=True)