import os
import pandas as pd
from datetime import datetime
from glob import glob
from openai import OpenAI
from faster_whisper import WhisperModel
import json

########### TODO #############
# - Agregar correo electrónico
# - Que el modelo solicite la información si no fue dada (para certificar el envío) 
# - Poner el modelo de lenguaje en LangChain
# - RAG

class PQRSProcessor:
    def __init__(self, 
                 openai_api_key, 
                 hotwords = "", 
                 whisper_model = 'large-v3', 
                 openai_model = 'gpt-4o', 
                 base_url = None):
        
        #self.audio_model = WhisperModel(whisper_model, compute_type="int8")
        self.openai_client =  OpenAI(base_url=base_url, api_key=openai_api_key)
        self.hotwords = hotwords
        self.openai_model = openai_model
        self.whisper_model = whisper_model
        self.get_prompts()
        self.historico = pd.read_csv('input/historico/historico.csv', sep=";")
        print(self.historico.columns)

    def get_audio_files(self, folder_path):
        audio_extensions = ["*.aac","*.wav","*.opus","*.ogg","*.mp3","*.mp4","*.mpeg","*.m4a", '*.flac']
        audio_files = []
        for ext in audio_extensions:
            audio_files.extend(glob(os.path.join(folder_path, ext)))
        self.audio_files = audio_files

    def transcribe_audio(self, file_path):
        segments, info = self.audio_model.transcribe(file_path, beam_size=2, language="es",hotwords=self.hotwords)
        self.transcription = " ".join([segment.text for segment in segments])
        print(self.transcription)

    def transcribe_audio_openai(self, audio_file):
        #audio_file = open(file_path, "rb")
        self.transcription = self.openai_client.audio.transcriptions.create(
            model=self.whisper_model, 
            file=audio_file,
            language='es',
            response_format="text",
      )
        print(self.transcription)

    def model_answer(self, transcription, test=False):

        if test:
            test_response = f"""Gracias por ponerte en contacto con nosotros. Nos complace informarte que tu petición ha sido enviada al área encargada en la Secretaría de Educación y está siendo procesada en el sistema. A continuación, te proporcionamos una plantilla de solución de peticiones que puedes utilizar para seguir el estado de tu solicitud y obtener la información necesaria:

---

**Referencia de la Petición:** [Número de Radicado]

**Fecha de Recepción:** 08/15/2024

**Área Encargada:** Secretaría de Educación

**Estado Actual:** En proceso

**Próximos Pasos:** 

1. **Revisión Inicial:** El equipo revisará tu petición para asegurarse de que toda la información necesaria ha sido proporcionada.
2. **Asignación:** Tu petición será asignada a un funcionario específico que se encargará de darle seguimiento.
3. **Respuesta:** Recibirás una respuesta oficial por parte de la Secretaría de Educación dentro del plazo estipulado por la normativa vigente.

**Contacto Adicional:** Si tienes alguna pregunta adicional o necesitas más información, puedes ponerte en contacto con nosotros a través del correo electrónico [correo@tunja.gov.co] o llamando al [número de contacto].

Agradecemos tu paciencia y comprensión mientras trabajamos para resolver tu petición."""
            
            print(test_response)
            return test_response


        ## PETICION ##
        query = "Inicio PQRS:\n" + transcription + "\nFin PQRS.\nNo des explicaciones adicionales, sólo responde con el JSON."
        messages = [
            {"role": "system", "content": self.sys_prompt},
            {"role": "user", "content": query}
        ]

        chat_completion = self.openai_client.chat.completions.create(
                            messages=messages,
                            model=self.openai_model,
                            temperature=0,
                            response_format={"type": "json_object"}
                        )
        
        print(chat_completion.choices[0].message.content)


        ## SOLUCION ##
        
        json_resp = eval(chat_completion.choices[0].message.content)
        fecha = datetime.strftime(datetime.today(), format="%m/%d/%Y")           

        if json_resp['es_faq']=='Sí':
            with open('input/prompts/sys_prompt_faqs.txt') as f:
                self.sys_prompt_solucion = f.read()

            with open('input/prompts/respuestas_faqs.txt') as f:
                faqs = f.read()
                
            self.sys_prompt_solucion = self.sys_prompt_solucion.format(faqs=faqs)

            query = "Inicio PQRS:\n" + transcription + "\nFin PQRS.\nResponde con la respuesta de a la pregunta frecuente."

            messages = [
                {'role': 'system', 'content': self.sys_prompt_solucion},
                {'role': 'user', 'content': query}
            ]

            chat_completion = self.openai_client.chat.completions.create(
                        messages=messages,
                        model=self.openai_model,
                        temperature=0.7,
                    )
            
            print(chat_completion.choices[0].message.content)
            
        else:
            
            if json_resp["radicado"]=="":
    
                with open("input/plantillas_solucion/plantilla.txt") as f:
                    self.prompt_solucion = f.read()
                
                self.prompt_solucion = self.prompt_solucion.format(nombre=json_resp["nombre"],
                                                                   fecha=fecha,
                                                                   entidad = json_resp['entidad_responde'],
                                                                   clase=json_resp["clase"] )
                
                messages = [
                    {"role": "system", "content": self.sys_prompt_sol},
                    {"role": "user", "content": self.prompt_solucion}
                ]
        
                chat_completion = self.openai_client.chat.completions.create(
                                    messages=messages,
                                    model=self.openai_model,
                                    temperature=0.7,
                                )
                print(chat_completion.choices[0].message.content)
    
            else:
                 ## CONSULTAR BASE DE DATOS ##
    
                consulta_usuario = self.historico[self.historico["numero_radicado"]==json_resp["radicado"]].iloc[0].to_dict()
                
                with open("input/plantillas_solucion/plantilla_hist.txt") as f:
                    self.prompt_solucion_hist = f.read()
                
                self.prompt_solucion_hist = self.prompt_solucion_hist.format(nombre=json_resp["nombre"], 
                                                                             fecha=fecha,
                                                                             clase=json_resp["clase"], 
                                                                             estado_radicado = consulta_usuario)
                
                messages = [
                    {"role": "system", "content": self.sys_prompt_sol},
                    {"role": "user", "content": self.prompt_solucion_hist}
                ]
        
                chat_completion = self.openai_client.chat.completions.create(
                                    messages=messages,
                                    model=self.openai_model,
                                    temperature=0.7,
                                )
                print(chat_completion.choices[0].message.content)

        
        return chat_completion.choices[0].message.content

    def process_audios(self, folder_path, user_prompt, system_prompt):
        results = []
        audio_files = self.get_audio_files(folder_path)

        for audio_file in tqdm(audio_files):
            transcription = self.transcribe_audio(audio_file)
            table = self.generate_table(transcription, user_prompt, system_prompt)
            results.append({
                "audio_file": os.path.basename(audio_file),
                "transcription": transcription,
                "table": table
            })

        return results

    @staticmethod
    def save_to_json(data, output_file):
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=4)

    def get_prompts(self):
        with open('input/prompts/estructura_json.txt') as f:
            estructura = f.read()

        with open('input/prompts/categorias.txt') as f:
            categorias = f.read()
        
        with open('input/prompts/sys_prompt.txt') as f:
            sys_prompt = f.read()

        with open('input/prompts/sys_prompt_solucion.txt') as f:
            sys_prompt_sol = f.read()

        with open('input/plantillas_solucion/plantilla.txt') as f:
            prompt_solucion = f.read()

        with open('input/prompts/faqs.txt') as f:
            faqs = f.read()

        with open('input/prompts/entidades.txt') as f:
            entidades = f.read()


        self.sys_prompt = sys_prompt.format(estructura=estructura, faqs=faqs, categorias=categorias, entidades=entidades)
        self.sys_prompt_sol = sys_prompt_sol.format(faqs=faqs)
        self.prompt_solucion = prompt_solucion
        