from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLineEdit, QTableWidget, QTableWidgetItem,
                             QLabel, QMessageBox, QHeaderView, QSplitter)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import os
from gui.add_dialog import AddTermDialog
from gui.edit_dialog import EditTermDialog
from db.database import ShipbuildingDB


class MainWindow(QMainWindow):
    """메인 윈도우 클래스"""
    
    def __init__(self):
        super().__init__()
        self.db = ShipbuildingDB()
        self.init_ui()
        self.load_all_terms()
    
    def init_ui(self):
        """UI 초기화"""
        self.setWindowTitle('조선업 축약어 사전')
        self.setGeometry(100, 100, 1200, 700)
        
        # 중앙 위젯
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 메인 레이아웃
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # 검색 영역
        search_layout = QHBoxLayout()
        search_label = QLabel('검색:')
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('축약어 또는 원어를 입력하세요...')
        self.search_input.textChanged.connect(self.search_terms)
        
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        
        main_layout.addLayout(search_layout)
        
        # 분할 위젯 (테이블 + 상세정보)
        splitter = QSplitter(Qt.Horizontal)
        
        # 테이블 위젯
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['ID', '축약어', '원어'])
        self.table.hideColumn(0)  # ID 컬럼 숨김
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.itemSelectionChanged.connect(self.show_term_details)
        
        splitter.addWidget(self.table)
        
        # 상세 정보 패널
        detail_widget = QWidget()
        detail_layout = QVBoxLayout()
        detail_widget.setLayout(detail_layout)
        
        # 상세 정보 라벨들
        self.detail_abbreviation = QLabel()
        self.detail_abbreviation.setStyleSheet('font-size: 24px; font-weight: bold; margin-bottom: 5px;')
        self.detail_full_term = QLabel()
        self.detail_full_term.setStyleSheet('font-size: 24px; color: #555; margin-bottom: 10px;')
        self.detail_definition = QLabel()
        self.detail_definition.setWordWrap(True)
        self.detail_definition.setStyleSheet('font-size: 24px; margin-top: 10px; line-height: 1.5;')
        
        # 이미지 라벨
        self.detail_image = QLabel()
        self.detail_image.setAlignment(Qt.AlignCenter)
        self.detail_image.setMinimumSize(600, 600)
        self.detail_image.setStyleSheet('border: 1px solid #ccc; background-color: #f5f5f5;')
        
        detail_layout.addWidget(QLabel('상세 정보'))
        detail_layout.addWidget(self.detail_abbreviation)
        detail_layout.addWidget(self.detail_full_term)
        detail_layout.addWidget(self.detail_definition)
        detail_layout.addWidget(self.detail_image)
        detail_layout.addStretch()
        
        splitter.addWidget(detail_widget)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)
        
        main_layout.addWidget(splitter)
        
        # 버튼 영역
        button_layout = QHBoxLayout()
        
        self.add_button = QPushButton('추가')
        self.add_button.clicked.connect(self.add_term)
        
        self.edit_button = QPushButton('수정')
        self.edit_button.clicked.connect(self.edit_term)
        self.edit_button.setEnabled(False)
        
        self.delete_button = QPushButton('삭제')
        self.delete_button.clicked.connect(self.delete_term)
        self.delete_button.setEnabled(False)
        
        self.refresh_button = QPushButton('새로고침')
        self.refresh_button.clicked.connect(self.load_all_terms)
        
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.refresh_button)
        button_layout.addStretch()
        
        main_layout.addLayout(button_layout)
    
    def load_all_terms(self):
        """모든 용어 로드"""
        self.search_input.clear()
        terms = self.db.get_all_terms()
        self.populate_table(terms)
        self.clear_detail_panel()
    
    def search_terms(self):
        """검색 실행"""
        keyword = self.search_input.text().strip()
        if keyword:
            terms = self.db.search_terms(keyword)
        else:
            terms = self.db.get_all_terms()
        self.populate_table(terms)
        # 검색 후 첫 번째 항목이 있으면 자동 선택
        if self.table.rowCount() > 0:
            self.table.selectRow(0)
        else:
            self.clear_detail_panel()
    
    def populate_table(self, terms):
        """테이블에 데이터 채우기"""
        self.table.clearContents()
        self.table.setRowCount(len(terms))
        for row, term in enumerate(terms):
            term_id, abbreviation, full_term, _, _ = term
            self.table.setItem(row, 0, QTableWidgetItem(str(term_id)))
            self.table.setItem(row, 1, QTableWidgetItem(abbreviation))
            self.table.setItem(row, 2, QTableWidgetItem(full_term))
    
    def show_term_details(self):
        """선택된 용어의 상세 정보 표시"""
        selected_rows = self.table.selectedItems()
        if selected_rows:
            self.edit_button.setEnabled(True)
            self.delete_button.setEnabled(True)
            
            row = selected_rows[0].row()
            term_id = int(self.table.item(row, 0).text())
            
            term = self.db.get_term_by_id(term_id)
            if term:
                _, abbreviation, full_term, definition, image_path = term
                
                self.detail_abbreviation.setText(f'축약어: {abbreviation}')
                self.detail_full_term.setText(f'원어: {full_term}')
                self.detail_definition.setText(f'정의: {definition if definition else "정의 없음"}')
                
                # 이미지 표시
                if image_path and os.path.exists(image_path):
                    pixmap = QPixmap(image_path)
                    if not pixmap.isNull():
                        scaled_pixmap = pixmap.scaled(700, 700, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                        self.detail_image.setPixmap(scaled_pixmap)
                    else:
                        self.detail_image.setText('이미지를 로드할 수 없습니다')
                else:
                    self.detail_image.clear()
                    self.detail_image.setText('이미지 없음')
        else:
            self.edit_button.setEnabled(False)
            self.delete_button.setEnabled(False)
            self.clear_detail_panel()
    
    def clear_detail_panel(self):
        """상세 정보 패널 초기화"""
        self.detail_abbreviation.clear()
        self.detail_full_term.clear()
        self.detail_definition.clear()
        self.detail_image.clear()
        self.detail_image.setText('용어를 선택하세요')
    
    def add_term(self):
        """용어 추가 다이얼로그 표시"""
        dialog = AddTermDialog(self)
        if dialog.exec_():
            abbreviation, full_term, definition, image_path = dialog.get_data()
            if self.db.add_term(abbreviation, full_term, definition, image_path):
                QMessageBox.information(self, '성공', '용어가 추가되었습니다.')
                self.load_all_terms()
            else:
                QMessageBox.warning(self, '오류', '용어 추가에 실패했습니다.')
    
    def edit_term(self):
        """용어 수정 다이얼로그 표시"""
        selected_rows = self.table.selectedItems()
        if not selected_rows:
            return
        
        row = selected_rows[0].row()
        term_id = int(self.table.item(row, 0).text())
        term = self.db.get_term_by_id(term_id)
        
        if term:
            dialog = EditTermDialog(self, term)
            if dialog.exec_():
                abbreviation, full_term, definition, image_path = dialog.get_data()
                if self.db.update_term(term_id, abbreviation, full_term, definition, image_path):
                    QMessageBox.information(self, '성공', '용어가 수정되었습니다.')
                    self.load_all_terms()
                else:
                    QMessageBox.warning(self, '오류', '용어 수정에 실패했습니다.')
    
    def delete_term(self):
        """용어 삭제"""
        selected_rows = self.table.selectedItems()
        if not selected_rows:
            return
        
        row = selected_rows[0].row()
        term_id = int(self.table.item(row, 0).text())
        abbreviation = self.table.item(row, 1).text()
        
        reply = QMessageBox.question(
            self, '삭제 확인',
            f"'{abbreviation}'를 삭제하시겠습니까?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.db.delete_term(term_id):
                QMessageBox.information(self, '성공', '용어가 삭제되었습니다.')
                self.load_all_terms()
            else:
                QMessageBox.warning(self, '오류', '용어 삭제에 실패했습니다.')
    
    def closeEvent(self, event):
        """윈도우 종료 시 데이터베이스 연결 종료"""
        self.db.close()
        event.accept()