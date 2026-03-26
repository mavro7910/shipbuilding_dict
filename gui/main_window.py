from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLineEdit, QTableWidget, QTableWidgetItem,
                             QLabel, QMessageBox, QHeaderView, QSplitter, QFrame,
                             QScrollArea, QSizePolicy)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
import os
from gui.add_dialog import AddTermDialog
from gui.edit_dialog import EditTermDialog
from db.database import ShipbuildingDB


class MainWindow(QMainWindow):
    """메인 윈도우 클래스"""

    def __init__(self):
        super().__init__()
        self.db = ShipbuildingDB()
        self._current_pixmap = None  # 원본 이미지 보관 (리사이즈용)
        self.init_ui()
        self.load_all_terms()

    def init_ui(self):
        self.setWindowTitle('조선업 사전')
        self.setGeometry(100, 100, 1600, 900)

        base_font = QFont('Malgun Gothic', 10)
        self.setFont(base_font)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        main_layout.setSpacing(8)
        main_layout.setContentsMargins(10, 10, 10, 10)
        central_widget.setLayout(main_layout)

        # ── 검색 영역 ─────────────────────────────────────────────
        search_layout = QHBoxLayout()
        search_label = QLabel('검색:  ')
        search_label.setFixedWidth(65)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('축약어 또는 원어를 입력하세요...')
        self.search_input.setFixedHeight(32)
        self.search_input.textChanged.connect(self.search_terms)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        main_layout.addLayout(search_layout)

        # ── 분할 위젯 ─────────────────────────────────────────────
        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(6)

        # 왼쪽: 용어 목록
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 4, 0)
        left_widget.setLayout(left_layout)

        list_title = QLabel('용어 목록')
        list_title.setStyleSheet('font-size: 11pt; font-weight: bold; padding: 4px 0;')
        left_layout.addWidget(list_title)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['ID', '축약어', '원어'])
        self.table.hideColumn(0)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.itemSelectionChanged.connect(self.show_term_details)
        self.table.verticalHeader().setDefaultSectionSize(30)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet('''
            QTableWidget { font-size: 10pt; }
            QTableWidget::item:selected { background-color: #0078d7; color: white; }
        ''')
        left_layout.addWidget(self.table)
        splitter.addWidget(left_widget)

        # 오른쪽: 상세 정보
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        detail_widget = QWidget()
        self.detail_layout = QVBoxLayout()
        self.detail_layout.setAlignment(Qt.AlignTop)
        self.detail_layout.setSpacing(6)
        self.detail_layout.setContentsMargins(16, 10, 16, 10)
        detail_widget.setLayout(self.detail_layout)

        detail_title = QLabel('상세 정보')
        detail_title.setStyleSheet('font-size: 12pt; font-weight: bold; padding-bottom: 6px;')
        self.detail_layout.addWidget(detail_title)

        # 축약어 (20pt, 굵게)
        self.detail_abbreviation = QLabel()
        self.detail_abbreviation.setWordWrap(True)
        self.detail_abbreviation.setStyleSheet('''
            font-size: 20pt; font-weight: bold;
            color: #1a1a2e; padding: 4px 0;
        ''')
        self.detail_layout.addWidget(self.detail_abbreviation)

        # 원어 (14pt)
        self.detail_full_term = QLabel()
        self.detail_full_term.setWordWrap(True)
        self.detail_full_term.setStyleSheet('font-size: 14pt; color: #444; padding: 2px 0;')
        self.detail_layout.addWidget(self.detail_full_term)

        # 구분선
        line1 = QFrame()
        line1.setFrameShape(QFrame.HLine)
        line1.setFixedHeight(1)
        line1.setStyleSheet('background-color: #ddd; margin: 6px 0;')
        self.detail_layout.addWidget(line1)

        # 정의 (11pt)
        def_label = QLabel('정의')
        def_label.setStyleSheet('font-size: 10pt; font-weight: bold; color: #888;')
        self.detail_layout.addWidget(def_label)

        self.detail_definition = QLabel()
        self.detail_definition.setWordWrap(True)
        self.detail_definition.setStyleSheet('font-size: 11pt; color: #222; padding: 4px 0 8px 0;')
        self.detail_layout.addWidget(self.detail_definition)

        # 이미지
        img_label = QLabel('이미지')
        img_label.setStyleSheet('font-size: 10pt; font-weight: bold; color: #888;')
        self.detail_layout.addWidget(img_label)

        self.detail_image = QLabel()
        self.detail_image.setAlignment(Qt.AlignCenter)
        self.detail_image.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.detail_image.setMinimumHeight(200)
        self.detail_image.setStyleSheet('''
            border: 1px solid #ddd;
            background-color: #fafafa;
            border-radius: 4px;
            padding: 8px;
        ''')
        self.detail_layout.addWidget(self.detail_image)

        # 구분선
        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setFixedHeight(1)
        line2.setStyleSheet('background-color: #ddd; margin: 10px 0 6px 0;')
        self.detail_layout.addWidget(line2)

        # 관련 규정/표준
        ref_header = QLabel('📋 관련 규정/표준')
        ref_header.setStyleSheet('font-size: 11pt; font-weight: bold; padding-bottom: 4px;')
        self.detail_layout.addWidget(ref_header)

        self.ref_table = QTableWidget()
        self.ref_table.setColumnCount(3)
        self.ref_table.setHorizontalHeaderLabels(['구분', '제목', '내용'])
        self.ref_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.ref_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.ref_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.ref_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.ref_table.setSelectionMode(QTableWidget.NoSelection)
        self.ref_table.verticalHeader().setDefaultSectionSize(30)
        self.ref_table.setStyleSheet('font-size: 10pt;')
        self.ref_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.ref_table.setMaximumHeight(240)
        self.detail_layout.addWidget(self.ref_table)

        self.no_ref_label = QLabel('등록된 규정/표준이 없습니다.')
        self.no_ref_label.setStyleSheet('color: #bbb; font-size: 10pt; padding: 4px 0;')
        self.detail_layout.addWidget(self.no_ref_label)

        self.detail_layout.addStretch()
        scroll_area.setWidget(detail_widget)
        splitter.addWidget(scroll_area)

        # 목록 1 : 상세 2 비율
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        splitter.setSizes([400, 800])

        main_layout.addWidget(splitter)

        # ── 버튼 영역 ─────────────────────────────────────────────
        btn_style = 'QPushButton { padding: 6px 18px; font-size: 10pt; }'
        button_layout = QHBoxLayout()

        self.add_button = QPushButton('➕  추가')
        self.add_button.clicked.connect(self.add_term)
        self.add_button.setStyleSheet(btn_style)

        self.edit_button = QPushButton('✏️  수정')
        self.edit_button.clicked.connect(self.edit_term)
        self.edit_button.setEnabled(False)
        self.edit_button.setStyleSheet(btn_style)

        self.delete_button = QPushButton('🗑️  삭제')
        self.delete_button.clicked.connect(self.delete_term)
        self.delete_button.setEnabled(False)
        self.delete_button.setStyleSheet(btn_style)

        self.refresh_button = QPushButton('🔄  새로고침')
        self.refresh_button.clicked.connect(self.load_all_terms)
        self.refresh_button.setStyleSheet(btn_style)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.refresh_button)
        button_layout.addStretch()
        main_layout.addLayout(button_layout)

    # ── 데이터 로드 ───────────────────────────────────────────────

    def load_all_terms(self):
        self.search_input.clear()
        terms = self.db.get_all_terms()
        self.populate_table(terms)
        self.clear_detail_panel()

    def search_terms(self):
        keyword = self.search_input.text().strip()
        terms = self.db.search_terms(keyword) if keyword else self.db.get_all_terms()
        self.populate_table(terms)
        if self.table.rowCount() > 0:
            self.table.selectRow(0)
        else:
            self.clear_detail_panel()

    def populate_table(self, terms):
        self.table.clearContents()
        self.table.setRowCount(len(terms))
        for row, term in enumerate(terms):
            term_id, abbreviation, full_term, _, _ = term
            self.table.setItem(row, 0, QTableWidgetItem(str(term_id)))
            self.table.setItem(row, 1, QTableWidgetItem(abbreviation))
            self.table.setItem(row, 2, QTableWidgetItem(full_term))

    # ── 상세 정보 ─────────────────────────────────────────────────

    def show_term_details(self):
        selected_rows = self.table.selectedItems()
        if selected_rows:
            self.edit_button.setEnabled(True)
            self.delete_button.setEnabled(True)

            row = selected_rows[0].row()
            term_id = int(self.table.item(row, 0).text())
            term = self.db.get_term_by_id(term_id)

            if term:
                _, abbreviation, full_term, definition, image_path = term
                self.detail_abbreviation.setText(abbreviation)
                self.detail_full_term.setText(full_term)
                self.detail_definition.setText(definition if definition else '—')

                if image_path and os.path.exists(image_path):
                    pixmap = QPixmap(image_path)
                    if not pixmap.isNull():
                        self._current_pixmap = pixmap
                        self._update_image_size()
                    else:
                        self._current_pixmap = None
                        self.detail_image.setText('이미지를 로드할 수 없습니다')
                else:
                    self._current_pixmap = None
                    self.detail_image.clear()
                    self.detail_image.setText('이미지 없음')

                self._load_references(term_id)
        else:
            self.edit_button.setEnabled(False)
            self.delete_button.setEnabled(False)
            self.clear_detail_panel()

    def _update_image_size(self):
        """상세 패널 너비에 맞게 이미지 동적 리사이즈"""
        if self._current_pixmap is None:
            return
        available_w = self.detail_image.width() - 20
        if available_w < 100:
            available_w = 700
        scaled = self._current_pixmap.scaledToWidth(available_w, Qt.SmoothTransformation)
        self.detail_image.setPixmap(scaled)
        self.detail_image.setFixedHeight(scaled.height() + 16)

    def resizeEvent(self, event):
        """창 리사이즈 시 이미지도 함께 리사이즈"""
        super().resizeEvent(event)
        self._update_image_size()

    def _load_references(self, term_id):
        refs = self.db.get_references(term_id)
        self.ref_table.clearContents()
        self.ref_table.setRowCount(0)

        if refs:
            self.ref_table.setVisible(True)
            self.no_ref_label.setVisible(False)
            for ref_id, ref_type, title, content in refs:
                row = self.ref_table.rowCount()
                self.ref_table.insertRow(row)
                self.ref_table.setItem(row, 0, QTableWidgetItem(ref_type))
                self.ref_table.setItem(row, 1, QTableWidgetItem(title))
                self.ref_table.setItem(row, 2, QTableWidgetItem(content or ''))
            row_h = self.ref_table.verticalHeader().defaultSectionSize()
            header_h = self.ref_table.horizontalHeader().height()
            self.ref_table.setFixedHeight(
                min(header_h + row_h * len(refs) + 4, 240)
            )
        else:
            self.ref_table.setVisible(False)
            self.no_ref_label.setVisible(True)

    def clear_detail_panel(self):
        self._current_pixmap = None
        self.detail_abbreviation.clear()
        self.detail_full_term.clear()
        self.detail_definition.clear()
        self.detail_image.clear()
        self.detail_image.setText('용어를 선택하세요')
        self.detail_image.setFixedHeight(200)
        self.ref_table.clearContents()
        self.ref_table.setRowCount(0)
        self.ref_table.setVisible(False)
        self.no_ref_label.setVisible(False)

    # ── CRUD ──────────────────────────────────────────────────────

    def add_term(self):
        dialog = AddTermDialog(self)
        if dialog.exec_():
            abbreviation, full_term, definition, image_path = dialog.get_data()
            term_id = self.db.add_term(abbreviation, full_term, definition, image_path)
            if term_id:
                for ref_type, title, content in dialog.get_references():
                    self.db.add_reference(term_id, ref_type, title, content)
                QMessageBox.information(self, '성공', '용어가 추가되었습니다.')
                self.load_all_terms()
            else:
                QMessageBox.warning(self, '오류', '용어 추가에 실패했습니다. (중복된 축약어)')

    def edit_term(self):
        selected_rows = self.table.selectedItems()
        if not selected_rows:
            return
        row = selected_rows[0].row()
        term_id = int(self.table.item(row, 0).text())
        term = self.db.get_term_by_id(term_id)

        if term:
            existing_refs = self.db.get_references(term_id)
            dialog = EditTermDialog(self, term, existing_refs)
            if dialog.exec_():
                abbreviation, full_term, definition, image_path = dialog.get_data()
                if self.db.update_term(term_id, abbreviation, full_term, definition, image_path):
                    for ref_id in dialog.get_deleted_ref_ids():
                        self.db.delete_reference(ref_id)
                    for ref_type, title, content in dialog.get_new_references():
                        self.db.add_reference(term_id, ref_type, title, content)
                    QMessageBox.information(self, '성공', '용어가 수정되었습니다.')
                    self.load_all_terms()
                else:
                    QMessageBox.warning(self, '오류', '용어 수정에 실패했습니다.')

    def delete_term(self):
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
            self.db.delete_references_by_term(term_id)
            if self.db.delete_term(term_id):
                QMessageBox.information(self, '성공', '용어가 삭제되었습니다.')
                self.load_all_terms()
            else:
                QMessageBox.warning(self, '오류', '용어 삭제에 실패했습니다.')

    def closeEvent(self, event):
        self.db.close()
        event.accept()