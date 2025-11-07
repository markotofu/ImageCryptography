from flask import Flask, render_template, request, jsonify, send_file
import encryption
import decryption
from decryption import parseKey
import os

app = Flask(__name__, template_folder='.')

@app.route('/')
def index():
    return render_template('Page.html')

@app.route('/encrypt', methods=['POST', 'OPTIONS'])
def encrypt():
    # Handle CORS/preflight or stray OPTIONS gracefully
    if request.method == 'OPTIONS':
        return ('', 204)
    try:
        use_file = request.form.get('use_file', 'false') == 'true'
        text = ''

        if use_file:
            # Expect an uploaded .txt file under field 'uploaded_file'
            if 'uploaded_file' not in request.files:
                return jsonify({'success': False, 'error': 'No file uploaded'})
            upload = request.files['uploaded_file']
            if upload.filename == '':
                return jsonify({'success': False, 'error': 'Empty filename'})
            if not upload.filename.lower().endswith('.txt'):
                return jsonify({'success': False, 'error': 'Only .txt files are allowed'})
            try:
                raw = upload.read()
                text = raw.decode('utf-8', errors='replace')
            except Exception as fe:
                return jsonify({'success': False, 'error': f'Failed to read file: {fe}'})
        else:
            # Get text from form
            text = request.form.get('text', '')
            
        if not text:
            return jsonify({'success': False, 'error': 'No text provided'})

        # Encrypt the text
        key = encryption.encryption(text)
        
        return jsonify({
            'success': True,
            'key': key
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/decrypt', methods=['POST', 'OPTIONS'])
def decrypt():
    if request.method == 'OPTIONS':
        return ('', 204)
    key = request.form.get('key', '')
    if not key:
        return jsonify({'success': False, 'error': 'No key provided'})

    # Use project root for output_image.png to stay consistent with encryption.encryption save path
    root_output_path = os.path.join(os.getcwd(), 'output_image.png')

    # Check if an image file was uploaded
    image_file = None
    if 'image' in request.files:
        image_file = request.files['image']
    elif 'uploaded_image' in request.files:
        image_file = request.files['uploaded_image']

    if image_file is not None:
        if image_file.filename == '':
            return jsonify({'success': False, 'error': 'No image file selected'})
        image_file.save(root_output_path)
    elif not os.path.exists(root_output_path):
        return jsonify({'success': False, 'error': 'No encrypted image found. Please upload an image.'})

    # Validate key structure before attempting decryption to avoid IndexError
    try:
        cmds = parseKey(key)
    except Exception:
        return jsonify({'success': False, 'error': 'Invalid key format.'})
    if not any(cmd.get('type') == 'd' for cmd in cmds):
        return jsonify({'success': False, 'error': "Invalid key: missing 'd' (dummy pixels) command."})
    if not any(cmd.get('type') == 's' for cmd in cmds):
        return jsonify({'success': False, 'error': "Invalid key: missing 's' (channel shuffle) command."})

    try:
        decrypted_text = decryption.decryption(key)
    except IndexError:
        return jsonify({'success': False, 'error': 'Decryption failed: the key does not match the uploaded image (missing expected commands). Please ensure you use the exact key produced during encryption for this image.'})
    except Exception as e:
        return jsonify({'success': False, 'error': f'Decryption failed: {str(e)}'})

    return jsonify({'success': True, 'text': decrypted_text})

@app.route('/get-image')
def get_image():
    try:
        root_output_path = os.path.join(os.getcwd(), 'output_image.png')
        return send_file(root_output_path, mimetype='image/png')
    except Exception as e:
        return str(e), 404

@app.route('/download-image')
def download_image():
    try:
        root_output_path = os.path.join(os.getcwd(), 'output_image.png')
        return send_file(root_output_path, 
                        mimetype='image/png',
                        as_attachment=True,
                        download_name='encrypted_image.png')
    except Exception as e:
        return str(e), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
