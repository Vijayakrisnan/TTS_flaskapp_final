from flask import Flask, render_template, send_from_directory, jsonify, url_for
from gtts import gTTS
import os
import uuid
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__, template_folder='somethingnew')
app.config['SECRET_KEY'] = 'your-secret-key'  # Set your secret key
csrf = CSRFProtect(app)

# Set the output directory for audio files
OUTPUT_DIR = 'audio_output'

# Set the directories for audio and transcription files
AUDIO_DIR = 'static/audio_files_small'
TEXT_DIR = 'text_files_small'


@app.route('/')
def text_to_speech():
    return render_template('new6.html', audio_files=get_audio_files())


@app.route('/convert/<filename>', methods=['GET'])
def convert_to_speech(filename):
    # Read the text content from the corresponding text file
    text_file = os.path.join(TEXT_DIR, f'{filename.replace("af", "tf").replace(".mp3", ".txt")}')

    with open(text_file, 'r') as file:
        text = file.read()

    # Generate a unique filename for the audio file
    unique_filename = str(uuid.uuid4()) + '.mp3'
    output_file = os.path.join(OUTPUT_DIR, unique_filename)

    # Initialize gTTS and generate the speech
    tts = gTTS(text)
    tts.save(output_file)

    # Return the converted audio file URL and text as a JSON response
    response = {
        'text': text,
        'output_file': url_for('serve_audio', filename=unique_filename),
    }
    return jsonify(response)


@app.route('/audio_output/<filename>', methods=['GET'])
def serve_audio(filename):
    return send_from_directory(OUTPUT_DIR, filename)


def get_audio_files():
    audio_files = []
    count = 0
    for file_name in os.listdir(AUDIO_DIR):
        if file_name.startswith('af') and file_name.endswith('.mp3'):
            audio_files.append(file_name)
            count += 1
            if count == 4:
                break
    return audio_files


if __name__ == '__main__':
    # Create the output directory if it doesn't exist
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    app.run(debug=True)
