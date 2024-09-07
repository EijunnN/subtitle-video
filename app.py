from flask import Flask, render_template, request, jsonify, send_file
import faster_whisper
from deep_translator import GoogleTranslator
import os
import tempfile
import threading
import time

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def format_time(seconds):
    hours = int(seconds / 3600)
    minutes = int((seconds % 3600) / 60)
    seconds = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:06.3f}".replace('.', ',')

def split_subtitle(text, max_chars=50):
    words = text.split()
    lines = []
    current_line = []
    current_length = 0
    
    for word in words:
        if current_length + len(word) + 1 > max_chars and current_line:
            lines.append(' '.join(current_line))
            current_line = [word]
            current_length = len(word)
        else:
            current_line.append(word)
            current_length += len(word) + 1
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines

def process_video(video_file, source_lang, target_lang, model_size):
    model = faster_whisper.WhisperModel(model_size, device="cpu", compute_type="int8")
    translator = GoogleTranslator(source=source_lang, target=target_lang)
    
    try:
        segments, _ = model.transcribe(video_file, 
                                       beam_size=5, 
                                       word_timestamps=True,
                                       vad_filter=True,
                                       vad_parameters=dict(min_silence_duration_ms=500))
        
        srt_content = []
        subtitle_count = 1

        for segment in segments:
            start_time = segment.start
            end_time = segment.end
            text = segment.text.strip()
            
            if text:
                translated_text = translator.translate(text)
                split_lines = split_subtitle(translated_text)
                
                start_time_formatted = format_time(start_time)
                end_time_formatted = format_time(end_time)
                
                if len(split_lines) == 1:
                    srt_content.append(f"{subtitle_count}\n{start_time_formatted} --> {end_time_formatted}\n{split_lines[0]}\n\n")
                    subtitle_count += 1
                else:
                    time_per_line = (end_time - start_time) / len(split_lines)
                    for i, line in enumerate(split_lines):
                        line_start = start_time + i * time_per_line
                        line_end = line_start + time_per_line
                        line_start_formatted = format_time(line_start)
                        line_end_formatted = format_time(line_end)
                        srt_content.append(f"{subtitle_count}\n{line_start_formatted} --> {line_end_formatted}\n{line}\n\n")
                        subtitle_count += 1

        fd, temp_path = tempfile.mkstemp(suffix='.srt')
        with os.fdopen(fd, 'w', encoding='utf-8') as temp_file:
            temp_file.writelines(srt_content)
        return temp_path, None
    except Exception as e:
        return None, str(e)

def delayed_file_removal(file_path, delay=5):
    def remove_file():
        time.sleep(delay)
        try:
            os.remove(file_path)
            app.logger.info(f"Archivo temporal eliminado: {file_path}")
        except Exception as e:
            app.logger.error(f"Error al eliminar el archivo temporal: {e}")

    thread = threading.Thread(target=remove_file)
    thread.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_subtitles():
    if 'file' not in request.files:
        return jsonify({'error': 'No se encontró ningún archivo'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No se seleccionó ningún archivo'}), 400
    if file and allowed_file(file.filename):
        source_lang = request.form.get('source_lang', 'en')
        target_lang = request.form.get('target_lang', 'es')
        model_size = request.form.get('model', 'tiny')
        
        try:
            srt_path, error = process_video(file, source_lang, target_lang, model_size)
            
            if error:
                return jsonify({'error': error}), 500
            
            response = send_file(srt_path, as_attachment=True, download_name=f"{os.path.splitext(file.filename)[0]}_sub.srt")
            
            # Programar la eliminación del archivo temporal
            delayed_file_removal(srt_path)
            
            return response
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Tipo de archivo no permitido'}), 400

if __name__ == '__main__':
    os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
    app.run(debug=True)