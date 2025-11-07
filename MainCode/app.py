from flask import Flask, render_template, request, jsonify, send_file
import encryption
import decryption
import os

app = Flask(__name__, template_folder='.')

@app.route('/')
def index():
    """Landing page allowing mode selection before redirecting to dedicated UI."""
    return render_template('Page.html')

@app.route('/encrypt-ui')
def encrypt_ui():
    """Dedicated encryption interface."""
    return render_template('encrypt.html')

@app.route('/decrypt-ui')
def decrypt_ui():
    """Dedicated decryption interface."""
    return render_template('decrypt.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
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
                # Read entire file content as UTF-8 text
                raw = upload.read()
                text = raw.decode('utf-8', errors='replace')
            except Exception as fe:
                return jsonify({'success': False, 'error': f'Failed to read file: {fe}'})
        else:
            # Direct text input
            text = request.form.get('text', '')

        if not text.strip():
            return jsonify({'success': False, 'error': 'No text provided'})

        # Encrypt the text
        key = encryption.encryption(text)

        return jsonify({'success': True, 'key': key})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/decrypt', methods=['POST'])
def decrypt():
    try:
        key = request.form.get('key', '')
        if not key:
            return jsonify({'success': False, 'error': 'No key provided'})

        # If an image is uploaded, save it temporarily and use it for decryption
        temp_path = None
        if 'uploaded_image' in request.files:
            img_file = request.files['uploaded_image']
            if img_file and img_file.filename:
                if not img_file.filename.lower().endswith('.png'):
                    return jsonify({'success': False, 'error': 'Only .png images are allowed'})
                temp_path = 'uploaded_input.png'
                img_file.save(temp_path)

        # Ensure an image exists to decrypt
        image_path = temp_path if temp_path and os.path.exists(temp_path) else 'output_image.png'
        if not os.path.exists(image_path):
            return jsonify({'success': False, 'error': 'No encrypted image found. Please upload a .png image or encrypt text first.'})

        # Monkey-patch: temporarily point decryption to the selected image
        # The current decryption.decryption reads a hardcoded path. We'll open explicitly here.
        from PIL import Image
        img = Image.open(image_path)
        # Reuse internal helpers by lightly refactoring path through a small wrapper
        decrypted_text = _decrypt_with_image_and_key(img, key)

        # Clean up temp file
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass

        return jsonify({'success': True, 'text': decrypted_text})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

def _decrypt_with_image_and_key(img, key):
    """Wrapper that uses decryption module internals without changing its public API.
    We mirror decryption.decryption but inject the image object directly.
    """
    # Bring in needed helpers
    import numpy as np
    from decryption import imgToGrid, parseKey, reverseDetMultiplier, reverseMatrixObfuscation, reverseGrid, reverseDummyPixels, reverseColorShuffle, numToLetter, NULL_CHAR_INDEX

    grid = imgToGrid(img)
    commands = parseKey(key)

    manipulationCommands = [cmd for cmd in commands if cmd['type'] in ['M', 'm']]
    for command in manipulationCommands:
        if command['type'] == 'm':
            randomPos = int(command['data'])
            grid = reverseDetMultiplier(grid, randomPos)
        elif command['type'] == 'M':
            flatPixels = []
            for row in grid:
                for pixel in row:
                    flatPixels.append(pixel)
            flatPixels = reverseMatrixObfuscation(flatPixels, command['data'])
            height = len(grid)
            width = len(grid[0]) if height > 0 else 0
            grid = []
            pixelIndex = 0
            for y in range(height):
                row = []
                for x in range(width):
                    if pixelIndex < len(flatPixels):
                        row.append(flatPixels[pixelIndex])
                        pixelIndex += 1
                grid.append(row)

    pixelArray = reverseGrid(grid)
    dummyCommand = [cmd for cmd in commands if cmd['type'] == 'd'][0]
    dummyMultiplier = int(dummyCommand['data'])
    pixelArray = reverseDummyPixels(pixelArray, dummyMultiplier)

    shuffleCommand = [cmd for cmd in commands if cmd['type'] == 's'][0]
    usedChannels = [int(ch) for ch in shuffleCommand['data']]
    charData = reverseColorShuffle(pixelArray, usedChannels)

    finalText = ""
    for charNum in charData:
        if charNum < len(numToLetter) and charNum != NULL_CHAR_INDEX:
            finalText += numToLetter[charNum]

    return finalText

@app.route('/get-image')
def get_image():
    try:
        return send_file('output_image.png', mimetype='image/png')
    except Exception as e:
        return str(e), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
