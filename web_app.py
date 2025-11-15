import os
import sqlite3
import hashlib
import uuid
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import face_recognition
from PIL import Image
import io
import base64

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['AGENCY_PHOTOS'] = 'uploads/agency'
app.config['USER_PHOTOS'] = 'uploads/users'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Klasörleri oluştur
os.makedirs(app.config['AGENCY_PHOTOS'], exist_ok=True)
os.makedirs(app.config['USER_PHOTOS'], exist_ok=True)

# Veritabanı başlat
def init_db():
    conn = sqlite3.connect('photo_gallery.db')
    c = conn.cursor()
    
    # Admin tablosu
    c.execute('''CREATE TABLE IF NOT EXISTS admins
                 (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)''')
    
    # Ajans fotoğrafları tablosu
    c.execute('''CREATE TABLE IF NOT EXISTS agency_photos
                 (id INTEGER PRIMARY KEY, 
                  filename TEXT, 
                  filepath TEXT,
                  face_encoding BLOB,
                  upload_date TIMESTAMP,
                  active INTEGER DEFAULT 1)''')
    
    # Kullanıcı oturumları tablosu
    c.execute('''CREATE TABLE IF NOT EXISTS user_sessions
                 (id INTEGER PRIMARY KEY,
                  session_id TEXT UNIQUE,
                  user_photo TEXT,
                  face_encoding BLOB,
                  created_at TIMESTAMP)''')
    
    # Eşleşmeler tablosu
    c.execute('''CREATE TABLE IF NOT EXISTS matches
                 (id INTEGER PRIMARY KEY,
                  session_id TEXT,
                  agency_photo_id INTEGER,
                  similarity REAL,
                  matched_at TIMESTAMP)''')
    
    # Varsayılan admin ekle (username: admin, password: admin123)
    admin_pass = hashlib.sha256('admin123'.encode()).hexdigest()
    try:
        c.execute('INSERT INTO admins (username, password) VALUES (?, ?)', 
                  ('admin', admin_pass))
    except sqlite3.IntegrityError:
        pass
    
    conn.commit()
    conn.close()

init_db()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_face_encoding(image_path):
    """Fotoğraftan yüz encoding'i çıkar"""
    try:
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)
        if len(encodings) > 0:
            return encodings[0].tobytes()
        return None
    except Exception as e:
        print(f"Encoding hatası: {str(e)}")
        return None

def compare_faces(encoding1_bytes, encoding2_bytes, tolerance=0.6):
    """İki yüz encoding'ini karşılaştır"""
    import numpy as np
    encoding1 = np.frombuffer(encoding1_bytes, dtype=np.float64)
    encoding2 = np.frombuffer(encoding2_bytes, dtype=np.float64)
    
    distance = face_recognition.face_distance([encoding1], encoding2)[0]
    similarity = (1 - distance) * 100
    
    return distance <= tolerance, similarity

# ============= ADMIN ROUTES =============

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        conn = sqlite3.connect('photo_gallery.db')
        c = conn.cursor()
        c.execute('SELECT * FROM admins WHERE username=? AND password=?', 
                  (username, password_hash))
        admin = c.fetchone()
        conn.close()
        
        if admin:
            session['admin'] = username
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin_login.html', error='Hatalı kullanıcı adı veya şifre')
    
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('admin_login'))

@app.route('/admin')
def admin_dashboard():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    
    conn = sqlite3.connect('photo_gallery.db')
    c = conn.cursor()
    c.execute('SELECT id, filename, filepath, upload_date, active FROM agency_photos ORDER BY upload_date DESC')
    photos = c.fetchall()
    conn.close()
    
    return render_template('admin_dashboard.html', photos=photos)

@app.route('/admin/upload', methods=['POST'])
def admin_upload():
    if 'admin' not in session:
        return jsonify({'error': 'Yetkisiz erişim'}), 401
    
    if 'photos' not in request.files:
        return jsonify({'error': 'Fotoğraf seçilmedi'}), 400
    
    files = request.files.getlist('photos')
    uploaded = 0
    failed = 0
    
    conn = sqlite3.connect('photo_gallery.db')
    c = conn.cursor()
    
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            filepath = os.path.join(app.config['AGENCY_PHOTOS'], unique_filename)
            
            file.save(filepath)
            
            # Yüz encoding'i çıkar
            encoding = get_face_encoding(filepath)
            
            if encoding:
                c.execute('''INSERT INTO agency_photos 
                            (filename, filepath, face_encoding, upload_date) 
                            VALUES (?, ?, ?, ?)''',
                         (filename, filepath, encoding, datetime.now()))
                uploaded += 1
            else:
                os.remove(filepath)
                failed += 1
    
    conn.commit()
    conn.close()
    
    return jsonify({
        'success': True,
        'uploaded': uploaded,
        'failed': failed,
        'message': f'{uploaded} fotoğraf yüklendi, {failed} fotoğrafta yüz bulunamadı'
    })

@app.route('/admin/delete/<int:photo_id>', methods=['POST'])
def admin_delete(photo_id):
    if 'admin' not in session:
        return jsonify({'error': 'Yetkisiz erişim'}), 401
    
    conn = sqlite3.connect('photo_gallery.db')
    c = conn.cursor()
    c.execute('SELECT filepath FROM agency_photos WHERE id=?', (photo_id,))
    photo = c.fetchone()
    
    if photo:
        # Dosyayı sil
        if os.path.exists(photo[0]):
            os.remove(photo[0])
        
        # Veritabanından sil
        c.execute('DELETE FROM agency_photos WHERE id=?', (photo_id,))
        conn.commit()
    
    conn.close()
    return jsonify({'success': True})

@app.route('/admin/stats')
def admin_stats():
    if 'admin' not in session:
        return jsonify({'error': 'Yetkisiz erişim'}), 401
    
    conn = sqlite3.connect('photo_gallery.db')
    c = conn.cursor()
    
    c.execute('SELECT COUNT(*) FROM agency_photos WHERE active=1')
    total_photos = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM user_sessions')
    total_sessions = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM matches')
    total_matches = c.fetchone()[0]
    
    conn.close()
    
    return jsonify({
        'total_photos': total_photos,
        'total_sessions': total_sessions,
        'total_matches': total_matches
    })

# ============= USER ROUTES =============

@app.route('/')
def index():
    return render_template('user_index.html')

@app.route('/upload_selfie', methods=['POST'])
def upload_selfie():
    if 'photo' not in request.files:
        return jsonify({'error': 'Fotoğraf seçilmedi'}), 400
    
    file = request.files['photo']
    
    if not file or not allowed_file(file.filename):
        return jsonify({'error': 'Geçersiz dosya formatı'}), 400
    
    # Session ID oluştur
    session_id = str(uuid.uuid4())
    
    # Fotoğrafı kaydet
    filename = f"{session_id}.jpg"
    filepath = os.path.join(app.config['USER_PHOTOS'], filename)
    file.save(filepath)
    
    # Yüz encoding'i çıkar
    user_encoding = get_face_encoding(filepath)
    
    if not user_encoding:
        os.remove(filepath)
        return jsonify({'error': 'Fotoğrafta yüz bulunamadı. Lütfen net bir selfie çekin.'}), 400
    
    # Veritabanına kaydet
    conn = sqlite3.connect('photo_gallery.db')
    c = conn.cursor()
    c.execute('''INSERT INTO user_sessions 
                (session_id, user_photo, face_encoding, created_at) 
                VALUES (?, ?, ?, ?)''',
             (session_id, filepath, user_encoding, datetime.now()))
    conn.commit()
    
    # Ajans fotoğraflarıyla eşleştir
    c.execute('SELECT id, filepath, face_encoding FROM agency_photos WHERE active=1')
    agency_photos = c.fetchall()
    
    matches = []
    for photo in agency_photos:
        photo_id, photo_path, photo_encoding = photo
        is_match, similarity = compare_faces(user_encoding, photo_encoding)
        
        if is_match:
            c.execute('''INSERT INTO matches 
                        (session_id, agency_photo_id, similarity, matched_at) 
                        VALUES (?, ?, ?, ?)''',
                     (session_id, photo_id, similarity, datetime.now()))
            
            matches.append({
                'id': photo_id,
                'path': photo_path,
                'similarity': similarity
            })
    
    conn.commit()
    conn.close()
    
    # Benzerlik oranına göre sırala
    matches.sort(key=lambda x: x['similarity'], reverse=True)
    
    return jsonify({
        'success': True,
        'session_id': session_id,
        'matches_count': len(matches),
        'matches': matches
    })

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    """Yüklenen dosyaları serve et"""
    import os
    # uploads/agency/file.jpg veya uploads/users/file.jpg
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    # Sadece filename verilmişse agency klasöründe ara
    agency_path = os.path.join(app.config['AGENCY_PHOTOS'], filename)
    if os.path.exists(agency_path):
        return send_from_directory(app.config['AGENCY_PHOTOS'], filename)
    return "File not found", 404

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=False, host='0.0.0.0', port=port)
