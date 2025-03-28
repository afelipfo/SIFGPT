from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import sys
import io
import os

sys.path.append('src/')

from PQRS import PQRSProcessor

app = Flask(__name__)
CORS(app)

# Inicializamos el procesador de PQRS con la clave API necesaria
# Cargar variables del archivo .env
load_dotenv()

# Obtener la API key desde el archivo .env
api_key = os.getenv('OPENAI_API_KEY')

pqrs_proc = PQRSProcessor(base_url=None, openai_api_key=api_key, whisper_model='whisper-1')
audio_path = 'input/audios'

#TODO
# - Cambiar lectura de audio para que lea directamente de la caché (no desde el directorio)
# - Eliminar scroll horizontal en el bloque de chat

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.json.get('message')
    response = pqrs_proc.model_answer(user_input, test=False)
    return jsonify({'response': response})

@app.route('/process_audio', methods=['POST'])
def endpoint_transcribe():
   if 'audio' not in request.files:
      return jsonify({"error": "No audio file provided"}), 400
      
   audio_file = request.files['audio']
   try:
      # save a temporary instance of the file to satisfy the API
      audio_file.seek(0)
      temp_path = "./temp_audio.webm"
      audio_file.save(temp_path)
      with open(temp_path, "rb") as file:
         pqrs_proc.transcribe_audio_openai(file)
      # clean up
      os.remove(temp_path)
      return jsonify({'transcript': pqrs_proc.transcription}) 

   
   except Exception as e:
      print(e)
      return jsonify({"error": str(e)}), 500
   
if __name__ == '__main__':
    app.run(debug=True)
    print("running up...")