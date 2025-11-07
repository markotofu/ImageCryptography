from flask import Flask, render_template, request, jsonify, send_file
import encryption
import decryption
import os

app = Flask(__name__, template_folder='.')

@app.route('/')
def index():
    return render_template('Page.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    try:
        use_file = request.form.get('use_file', 'false') == 'true'
        
        if use_file:
            # Read from testText file
            script_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(script_dir, "testText")
            
            if not os.path.exists(file_path):
                return jsonify({'success': False, 'error': 'testText file not found'})
            
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
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

@app.route('/decrypt', methods=['POST'])
def decrypt():
    try:
        key = request.form.get('key', '')
        
        if not key:
            return jsonify({'success': False, 'error': 'No key provided'})
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(script_dir, 'output_image.png')
        
        # Check if an image file was uploaded
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file.filename == '':
                return jsonify({'success': False, 'error': 'No image file selected'})
            
            # Save the uploaded image as output_image.png in MainCode folder
            image_file.save(output_path)
        elif not os.path.exists(output_path):
            return jsonify({'success': False, 'error': 'No encrypted image found. Please upload an image.'})
        
        # Decrypt the image
        decrypted_text = decryption.decryption(key)
        
        return jsonify({
            'success': True,
            'text': decrypted_text
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/get-image')
def get_image():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(script_dir, 'output_image.png')
        return send_file(output_path, mimetype='image/png')
    except Exception as e:
        return str(e), 404

@app.route('/download-image')
def download_image():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(script_dir, 'output_image.png')
        return send_file(output_path, 
                        mimetype='image/png',
                        as_attachment=True,
                        download_name='encrypted_image.png')
    except Exception as e:
        return str(e), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
