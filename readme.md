# Subtitle Generator

Subtitle Generator is a web application that allows users to generate and translate subtitles for video files. It uses the Whisper model for audio transcription and Google Translate for translation.

## Features

- Supports multiple video formats (mp4, avi, mov)
- Audio transcription using different Whisper models (tiny, base, small, medium, large)
- Translation of subtitles into various languages
- Intuitive and easy-to-use user interface
- Generation of subtitle files in SRT format

## Requirements

- Python 3.7+
- Flask
- faster_whisper
- deep_translator

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/EijunnN/subtitle-video.git
   cd subtitle-video
   ```

2. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```
   python app.py
   ```

2. Open a web browser and go to `http://localhost:5000`

3. Select a video file, choose the source and target languages, and select the Whisper model.

4. Click on "Generate Subtitles" and wait for the process to complete.

5. The subtitle file will be automatically downloaded once generated.

## Contributing

Contributions are welcome. Please open an issue to discuss significant changes before submitting a pull request.

## License

[MIT](https://choosealicense.com/licenses/mit/)