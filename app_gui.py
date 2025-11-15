import sys
import os
import face_recognition
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFileDialog, 
                             QProgressBar, QScrollArea, QGridLayout, QMessageBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PIL import Image
import numpy as np

class FaceMatchWorker(QThread):
    """Yüz eşleştirme işlemini arka planda yapan thread"""
    progress = pyqtSignal(int)
    finished = pyqtSignal(list, int)
    error = pyqtSignal(str)
    
    def __init__(self, photo_path, folder_path):
        super().__init__()
        self.photo_path = photo_path
        self.folder_path = folder_path
        self.allowed_extensions = {'.jpg', '.jpeg', '.png'}
    
    def get_face_encoding(self, image_path):
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
    
    def run(self):
        try:
            # Yüklenen fotoğrafın encoding'ini çıkar
            uploaded_encoding = self.get_face_encoding(self.photo_path)
            
            if uploaded_encoding is None:
                self.error.emit("Yüklenen fotoğrafta yüz bulunamadı!")
                return
            
            # Klasördeki tüm fotoğrafları tara
            photo_files = []
            for filename in os.listdir(self.folder_path):
                ext = os.path.splitext(filename)[1].lower()
                if ext in self.allowed_extensions:
                    photo_files.append(os.path.join(self.folder_path, filename))
            
            if not photo_files:
                self.error.emit("Klasörde fotoğraf bulunamadı!")
                return
            
            matches = []
            total = len(photo_files)
            
            for idx, file_path in enumerate(photo_files):
                encoding = self.get_face_encoding(file_path)
                
                if encoding is not None:
                    result = face_recognition.compare_faces([encoding], uploaded_encoding, tolerance=0.6)
                    
                    if result[0]:
                        distance = face_recognition.face_distance([encoding], uploaded_encoding)[0]
                        similarity = (1 - distance) * 100
                        
                        matches.append({
                            'path': file_path,
                            'filename': os.path.basename(file_path),
                            'similarity': similarity
                        })
                
                # İlerleme güncelle
                progress_percent = int((idx + 1) / total * 100)
                self.progress.emit(progress_percent)
            
            # Benzerlik oranına göre sırala
            matches.sort(key=lambda x: x['similarity'], reverse=True)
            
            self.finished.emit(matches, total)
            
        except Exception as e:
            self.error.emit(f"Hata oluştu: {str(e)}")

class YuzTanimaApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.photo_path = None
        self.folder_path = None
        self.matches = []
        self.init_ui()
    
    def init_ui(self):
        """Arayüzü oluştur"""
        self.setWindowTitle('🔍 Yüz Tanıma Uygulaması')
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QPushButton {
                background-color: #667eea;
                color: white;
                border: none;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #5568d3;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
            QLabel {
                font-size: 13px;
            }
            QProgressBar {
                border: 2px solid #667eea;
                border-radius: 5px;
                text-align: center;
                height: 25px;
            }
            QProgressBar::chunk {
                background-color: #667eea;
            }
        """)
        
        # Ana widget ve layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Başlık
        title = QLabel('🔍 Yüz Tanıma Uygulaması')
        title.setFont(QFont('Arial', 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet('color: #667eea; margin-bottom: 10px;')
        layout.addWidget(title)
        
        subtitle = QLabel('Tamamen Offline - Local Çalışır')
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet('color: #666; font-size: 14px; margin-bottom: 20px;')
        layout.addWidget(subtitle)
        
        # Klasör seçimi
        folder_layout = QHBoxLayout()
        self.folder_label = QLabel('📁 Klasör seçilmedi')
        self.folder_label.setStyleSheet('background: white; padding: 10px; border-radius: 5px;')
        folder_layout.addWidget(self.folder_label, 1)
        
        folder_btn = QPushButton('📂 Klasör Seç')
        folder_btn.clicked.connect(self.select_folder)
        folder_layout.addWidget(folder_btn)
        layout.addLayout(folder_layout)
        
        # Fotoğraf seçimi
        photo_layout = QHBoxLayout()
        self.photo_label = QLabel('📷 Fotoğraf seçilmedi')
        self.photo_label.setStyleSheet('background: white; padding: 10px; border-radius: 5px;')
        photo_layout.addWidget(self.photo_label, 1)
        
        photo_btn = QPushButton('📷 Fotoğraf Seç')
        photo_btn.clicked.connect(self.select_photo)
        photo_layout.addWidget(photo_btn)
        layout.addLayout(photo_layout)
        
        # Eşleştir butonu
        self.match_btn = QPushButton('🔎 Eşleştir')
        self.match_btn.setEnabled(False)
        self.match_btn.clicked.connect(self.start_matching)
        self.match_btn.setMinimumHeight(50)
        self.match_btn.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                padding: 15px;
            }
        """)
        layout.addWidget(self.match_btn)
        
        # İlerleme çubuğu
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Sonuç etiketi
        self.result_label = QLabel('')
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet('font-size: 14px; font-weight: bold; color: #667eea;')
        layout.addWidget(self.result_label)
        
        # Sonuçlar için scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet('background: white; border: 2px solid #e0e0e0; border-radius: 8px;')
        
        self.results_widget = QWidget()
        self.results_layout = QGridLayout()
        self.results_layout.setSpacing(15)
        self.results_widget.setLayout(self.results_layout)
        scroll.setWidget(self.results_widget)
        
        layout.addWidget(scroll, 1)
        
        main_widget.setLayout(layout)
    
    def select_folder(self):
        """Klasör seç"""
        folder = QFileDialog.getExistingDirectory(self, 'Klasör Seç')
        if folder:
            self.folder_path = folder
            folder_name = os.path.basename(folder)
            self.folder_label.setText(f'📁 {folder_name}')
            self.check_ready()
    
    def select_photo(self):
        """Fotoğraf seç"""
        photo, _ = QFileDialog.getOpenFileName(
            self, 
            'Fotoğraf Seç',
            '',
            'Images (*.png *.jpg *.jpeg)'
        )
        if photo:
            self.photo_path = photo
            photo_name = os.path.basename(photo)
            self.photo_label.setText(f'📷 {photo_name}')
            self.check_ready()
    
    def check_ready(self):
        """Eşleştir butonunu aktif et"""
        if self.photo_path and self.folder_path:
            self.match_btn.setEnabled(True)
    
    def start_matching(self):
        """Eşleştirmeyi başlat"""
        # UI'ı güncelle
        self.match_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.result_label.setText('Fotoğraflar taranıyor...')
        
        # Eski sonuçları temizle
        self.clear_results()
        
        # Worker thread başlat
        self.worker = FaceMatchWorker(self.photo_path, self.folder_path)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.show_results)
        self.worker.error.connect(self.show_error)
        self.worker.start()
    
    def update_progress(self, value):
        """İlerleme çubuğunu güncelle"""
        self.progress_bar.setValue(value)
    
    def clear_results(self):
        """Sonuçları temizle"""
        while self.results_layout.count():
            item = self.results_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
    
    def show_results(self, matches, total_scanned):
        """Sonuçları göster"""
        self.progress_bar.setVisible(False)
        self.match_btn.setEnabled(True)
        self.matches = matches
        
        if not matches:
            self.result_label.setText(f'Taranan: {total_scanned} | Eşleşme: 0')
            no_match = QLabel('❌ Eşleşme bulunamadı')
            no_match.setAlignment(Qt.AlignCenter)
            no_match.setStyleSheet('font-size: 16px; color: #999; padding: 40px;')
            self.results_layout.addWidget(no_match, 0, 0)
            return
        
        self.result_label.setText(f'Taranan: {total_scanned} | Eşleşme: {len(matches)}')
        
        # Sonuçları grid'de göster
        col = 0
        row = 0
        max_cols = 3
        
        for match in matches:
            # Kart widget
            card = QWidget()
            card.setStyleSheet("""
                QWidget {
                    background: white;
                    border-radius: 10px;
                    border: 2px solid #e0e0e0;
                }
                QWidget:hover {
                    border: 2px solid #667eea;
                }
            """)
            card_layout = QVBoxLayout()
            card_layout.setContentsMargins(10, 10, 10, 10)
            
            # Fotoğraf
            pixmap = QPixmap(match['path'])
            if not pixmap.isNull():
                pixmap = pixmap.scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                img_label = QLabel()
                img_label.setPixmap(pixmap)
                img_label.setAlignment(Qt.AlignCenter)
                card_layout.addWidget(img_label)
            
            # Benzerlik oranı
            similarity_label = QLabel(f"✅ %{match['similarity']:.1f}")
            similarity_label.setAlignment(Qt.AlignCenter)
            similarity_label.setStyleSheet('font-size: 16px; font-weight: bold; color: #667eea; padding: 5px;')
            card_layout.addWidget(similarity_label)
            
            # Dosya adı
            filename_label = QLabel(match['filename'])
            filename_label.setAlignment(Qt.AlignCenter)
            filename_label.setWordWrap(True)
            filename_label.setStyleSheet('font-size: 11px; color: #666;')
            card_layout.addWidget(filename_label)
            
            card.setLayout(card_layout)
            self.results_layout.addWidget(card, row, col)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
    
    def show_error(self, error_msg):
        """Hata göster"""
        self.progress_bar.setVisible(False)
        self.match_btn.setEnabled(True)
        self.result_label.setText('')
        
        QMessageBox.critical(self, 'Hata', error_msg)

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = YuzTanimaApp()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
