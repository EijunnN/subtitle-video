import faster_whisper
import datetime
from deep_translator import GoogleTranslator
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'   # Solución para el error de duplicación de librerías

# Cargar el modelo de Whisper (puedes elegir el modelo según tus necesidades)
model = faster_whisper.WhisperModel("base", device="cpu", compute_type="float32")

# Especificar la ruta del archivo de video en tu sistema local
video_file = "./09_Enumerations.mp4"

# Transcribir el video directamente
segments, _ = model.transcribe(video_file, beam_size=5, vad_filter=True)

# Crear un objeto GoogleTranslator de deep_translator
translator = GoogleTranslator(source='en', target='es')

# Crear el contenido del archivo SRT
srt_content = ""
subtitle_count = 1

# Procesar cada segmento y generar los subtítulos en formato SRT
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

# Guardar el contenido del archivo SRT en un archivo
with open("subtitulos.srt", "w", encoding="utf-8") as srt_file:
    srt_file.write(srt_content)

print("Archivo SRT generado exitosamente.")