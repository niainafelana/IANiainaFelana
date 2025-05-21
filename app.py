from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os

from utils import extract_text_from_pdf
from summarizer import summarize_text

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/summarize', methods=['POST'])
def summarize():
    target_lang = request.form.get('lang') or request.json.get('lang')

    if 'file' in request.files:
        file = request.files['file']
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
        file.save(filepath)
        text = extract_text_from_pdf(filepath)
    elif request.json and 'text' in request.json:
        text = request.json['text']
    else:
        return jsonify({'error': 'Aucun fichier ou texte fourni'}), 400

    summary, detected = summarize_text(text, target_lang)
    return jsonify({
        'summary': summary,
        'lang_detected': detected,
        'lang_used': target_lang or detected
    })

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)
