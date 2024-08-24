from flask import Flask, render_template, request, jsonify, send_file
import faster_whisper
from deep_translator import GoogleTranslator
import os
import tempfile

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def format_time(seconds):
    hours = int(seconds / 3600)
    minutes = int((seconds % 3600) / 60)
    seconds = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:06.3f}".replace('.', ',')

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
                start_time_formatted = format_time(start_time)
                end_time_formatted = format_time(end_time)
                
                srt_content.append(f"{subtitle_count}\n{start_time_formatted} --> {end_time_formatted}\n{translated_text}\n\n")
                subtitle_count += 1

        fd, temp_path = tempfile.mkstemp(suffix='.srt')
        with os.fdopen(fd, 'w', encoding='utf-8') as temp_file:
            temp_file.writelines(srt_content)
        return temp_path, None
    except Exception as e:
        return None, str(e)

def remove_temp_file(file_path):
    try:
        os.remove(file_path)
    except PermissionError:
        app.logger.warning(f"No se pudo eliminar el archivo temporal: {file_path}")
    except Exception as error:
        app.logger.error(f"Error al eliminar el archivo temporal: {error}")

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
            
            try:
                return send_file(srt_path, as_attachment=True, download_name=f"{os.path.splitext(file.filename)[0]}_sub.srt")
            finally:
                remove_temp_file(srt_path)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Tipo de archivo no permitido'}), 400

if __name__ == '__main__':
    os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
    app.run(debug=True)