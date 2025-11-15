import os
import sys
import webbrowser
import threading
import face_recognition
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from PIL import Image
import cv2

# PyInstaller için resource path
def resource_path(relative_path):
    """PyInstaller ile paketlenmiş dosyaların yolunu al"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

app = Flask(__name__, 
            template_folder=resource_path('templates'),
            static_folder=resource_path('static'))

# Upload klasörünü kullanıcının home dizininde oluştur
UPLOAD_BASE = os.path.join(os.path.expanduser('~'), '.yuz_tanima')
app.config['UPLOAD_FOLDER'] = os.path.join(UPLOAD_BASE, 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Upload klasörünü oluştur
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_face_encoding(image_path):
    """Bir fotoğraftan yüz encoding'i çıkar"""
    try:
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)
        if len(encodings) > 0:
            return encodings[0]
        return None
    except Exception as e:
        print(f"Hata ({image_path}): {str(e)}")
        return None

def process_uploaded_files(files):
    """Yüklenen dosyalardan yüz encoding'lerini çıkar"""
    face_data = []
    temp_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_folder')
    os.makedirs(temp_folder, exist_ok=True)
    
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(temp_folder, filename)
            file.save(filepath)
            
            encoding = get_face_encoding(filepath)
            if encoding is not None:
                face_data.append({
                    'path': filepath,
                    'filename': filename,
                    'encoding': encoding
                })
    
    return face_data

def find_matching_faces(uploaded_encoding, face_data, tolerance=0.6):
    """Yüklenen fotoğrafla eşleşen yüzleri bul"""
    matches = []
    
    for face in face_data:
        result = face_recognition.compare_faces([face['encoding']], uploaded_encoding, tolerance=tolerance)
        
        if result[0]:
            distance = face_recognition.face_distance([face['encoding']], uploaded_encoding)[0]
            url_path = '/' + face['path'].replace('\\', '/')
            matches.append({
                'path': face['path'],
                'filename': face['filename'],
                'url': url_path,
                'distance': float(distance),
                'similarity': float((1 - distance) * 100)
            })
    
    matches.sort(key=lambda x: x['distance'])
    return matches

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/match', methods=['POST'])
def match_faces():
    try:
        if 'photo' not in request.files:
            return jsonify({'error': 'Lütfen bir fotoğraf yükleyin'}), 400
        
        photo_file = request.files['photo']
        
        if photo_file.filename == '':
            return jsonify({'error': 'Fotoğraf seçilmedi'}), 400
        
        if not allowed_file(photo_file.filename):
            return jsonify({'error': 'Sadece .jpg, .jpeg, .png dosyaları kabul edilir'}), 400
        
        folder_files = request.files.getlist('folder_files')
        
        if not folder_files or len(folder_files) == 0:
            return jsonify({'error': 'Lütfen bir klasör seçin'}), 400
        
        filename = secure_filename(photo_file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        photo_file.save(filepath)
        
        uploaded_encoding = get_face_encoding(filepath)
        
        if uploaded_encoding is None:
            return jsonify({'error': 'Yüklenen fotoğrafta yüz bulunamadı'}), 400
        
        face_data = process_uploaded_files(folder_files)
        
        if len(face_data) == 0:
            return jsonify({'error': 'Seçilen klasörde yüz içeren fotoğraf bulunamadı'}), 400
        
        matches = find_matching_faces(uploaded_encoding, face_data)
        
        return jsonify({
            'success': True,
            'uploaded_photo': f'/static/uploads/{filename}',
            'total_scanned': len(face_data),
            'matches_found': len(matches),
            'matches': matches
        })
    
    except Exception as e:
        return jsonify({'error': f'Bir hata oluştu: {str(e)}'}), 500

def open_browser():
    """Tarayıcıyı otomatik aç"""
    webbrowser.open('http://127.0.0.1:5001')

if __name__ == '__main__':
    # 2 saniye sonra tarayıcıyı aç
    threading.Timer(2, open_browser).start()
    
    print("=" * 60)
    print("🔍 YÜZ TANIMA UYGULAMASI")
    print("=" * 60)
    print("Uygulama başlatılıyor...")
    print("Tarayıcı otomatik açılacak: http://127.0.0.1:5001")
    print("Kapatmak için bu pencereyi kapatın.")
    print("=" * 60)
    
    app.run(debug=False, host='0.0.0.0', port=5001, use_reloader=False)
