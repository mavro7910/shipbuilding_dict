from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QTextEdit, QPushButton, QFileDialog,
                             QMessageBox)
from PyQt5.QtCore import Qt
import os
import shutil


class AddTermDialog(QDialog):
    """용어 추가 다이얼로그"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image_path = ''
        self.init_ui()
    
    def init_ui(self):
        """UI 초기화"""
        self.setWindowTitle('용어 추가')
        self.setMinimumWidth(500)
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # 축약어 입력
        abbr_layout = QHBoxLayout()
        abbr_label = QLabel('축약어:')
        abbr_label.setMinimumWidth(80)
        self.abbr_input = QLineEdit()
        abbr_layout.addWidget(abbr_label)
        abbr_layout.addWidget(self.abbr_input)
        layout.addLayout(abbr_layout)
        
        # 원어 입력
        full_layout = QHBoxLayout()
        full_label = QLabel('원어:')
        full_label.setMinimumWidth(80)
        self.full_input = QLineEdit()
        full_layout.addWidget(full_label)
        full_layout.addWidget(self.full_input)
        layout.addLayout(full_layout)
        
        # 정의 입력
        def_label = QLabel('정의:')
        self.def_input = QTextEdit()
        self.def_input.setMaximumHeight(100)
        layout.addWidget(def_label)
        layout.addWidget(self.def_input)
        
        # 이미지 선택
        image_layout = QHBoxLayout()
        image_label = QLabel('이미지:')
        image_label.setMinimumWidth(80)
        self.image_path_label = QLabel('이미지 없음')
        self.image_path_label.setStyleSheet('color: #888;')
        self.image_button = QPushButton('이미지 선택')
        self.image_button.clicked.connect(self.select_image)
        self.clear_image_button = QPushButton('제거')
        self.clear_image_button.clicked.connect(self.clear_image)
        
        image_layout.addWidget(image_label)
        image_layout.addWidget(self.image_path_label, 1)
        image_layout.addWidget(self.image_button)
        image_layout.addWidget(self.clear_image_button)
        layout.addLayout(image_layout)
        
        # 버튼 영역
        button_layout = QHBoxLayout()
        self.save_button = QPushButton('저장')
        self.save_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton('취소')
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
    
    def select_image(self):
        """이미지 파일 선택"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            '이미지 선택',
            '',
            'Images (*.png *.jpg *.jpeg *.bmp *.gif)'
        )
        
        if file_path:
            # images 폴더로 복사
            try:
                filename = os.path.basename(file_path)
                dest_dir = 'images'
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)
                
                dest_path = os.path.join(dest_dir, filename)
                
                # 파일명 중복 처리
                base, ext = os.path.splitext(filename)
                counter = 1
                while os.path.exists(dest_path):
                    dest_path = os.path.join(dest_dir, f"{base}_{counter}{ext}")
                    counter += 1
                
                shutil.copy2(file_path, dest_path)
                self.image_path = dest_path
                self.image_path_label.setText(os.path.basename(dest_path))
                self.image_path_label.setStyleSheet('color: #000;')
            except Exception as e:
                QMessageBox.warning(self, '오류', f'이미지 복사 실패: {str(e)}')
    
    def clear_image(self):
        """이미지 제거"""
        self.image_path = ''
        self.image_path_label.setText('이미지 없음')
        self.image_path_label.setStyleSheet('color: #888;')
    
    def get_data(self):
        """입력된 데이터 반환"""
        return (
            self.abbr_input.text().strip(),
            self.full_input.text().strip(),
            self.def_input.toPlainText().strip(),
            self.image_path
        )
    
    def accept(self):
        """저장 버튼 클릭 시 유효성 검사"""
        abbreviation, full_term, _, _ = self.get_data()
        
        if not abbreviation:
            QMessageBox.warning(self, '입력 오류', '축약어를 입력해주세요.')
            self.abbr_input.setFocus()
            return
        
        if not full_term:
            QMessageBox.warning(self, '입력 오류', '원어를 입력해주세요.')
            self.full_input.setFocus()
            return
        
        super().accept()