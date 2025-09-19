from flask import Flask, render_template, request, send_file
from gtts import gTTS
import os
import io

# Importar las librerías para manejar archivos
import docx
from PyPDF2 import PdfReader

app = Flask(__name__)

# Directorio para guardar los archivos temporales
UPLOAD_FOLDER = 'temp_files'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ruta principal que sirve el formulario HTML
@app.route('/')
def index():
    return render_template('index.html')

# Función para leer el texto de un archivo
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
            text = "" # En caso de error, el texto queda vacío

    return text

# Ruta que procesa el archivo subido
@app.route('/convertir', methods=['POST'])
def convertir_a_audio():
    if 'file' not in request.files:
        return "No se encontró el archivo.", 400

    file = request.files['file']
    if file.filename == '':
        return "No se seleccionó ningún archivo.", 400

    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # 1. Leer el texto del archivo
        texto_extraido = get_text_from_file(file_path)
        
        # 2. Si hay texto, convertirlo a audio
        lang = request.form.get('lang', 'es')
        if texto_extraido:
            tts = gTTS(text=texto_extraido, lang=lang)
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            
            # Limpiar el archivo subido después de procesarlo
            os.remove(file_path)

            return send_file(
                audio_buffer,
                mimetype='audio/mp3',
                as_attachment=True,
                download_name="audio_generado.mp3"
            )
        else:
            os.remove(file_path)
            return "No se pudo extraer texto del archivo.", 400

# Asegurarse de que el servidor se ejecute solo si se llama a este script
if __name__ == '__main__':
    app.run(debug=True)