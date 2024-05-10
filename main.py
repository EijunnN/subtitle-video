import faster_whisper
import datetime
from deep_translator import GoogleTranslator
import os

os.environ['KMP_DUPLICATE_LIB_OK']='True'  # Solución para el error de duplicación de librerías

# Cargar el modelo de Whisper (puedes elegir el modelo según tus necesidades)
model = faster_whisper.WhisperModel("base", device="cpu", compute_type="float32")

video_file = "./09_Enumerations.mp4"
segments, _ = model.transcribe(video_file, beam_size=5, vad_filter=True)

# Crear un objeto traductor de Google Translator para traducir los subtítulos al español o cualquier otro idioma cambiando el valor de target
translator = GoogleTranslator(source='en', target='es')


srt_content = ""
subtitle_count = 1


for segment in segments:
    start_time = segment.start
    end_time = segment.end
    text = segment.text
    translated_text = translator.translate(text)
    
    start_time_formatted = f"{int(start_time / 3600):02d}:{int((start_time % 3600) / 60):02d}:{int(start_time % 60):02d}"
    end_time_formatted = f"{int(end_time / 3600):02d}:{int((end_time % 3600) / 60):02d}:{int(end_time % 60):02d}"
    
    srt_content += f"{subtitle_count}\n"
    srt_content += f"{start_time_formatted} --> {end_time_formatted}\n"
    srt_content += f"{translated_text}\n\n"
    subtitle_count += 1


video_name = os.path.splitext(os.path.basename(video_file))[0]
srt_file_name = f"{video_name}_sub.srt" # Se crea un archivo SRT con el nombre del video


with open(srt_file_name, "w", encoding="utf-8") as srt_file:
    srt_file.write(srt_content)

print(f"Archivo SRT generado exitosamente: {srt_file_name}")