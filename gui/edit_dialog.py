from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QTextEdit, QPushButton, QFileDialog,
                             QMessageBox, QTabWidget, QWidget, QTableWidget,
                             QTableWidgetItem, QComboBox, QHeaderView)
from PyQt5.QtCore import Qt
import os
import shutil


REF_TYPES = ['SOLAS', 'MARPOL', 'ISM', 'ISPS', 'MLC', 'SP', 'OTHER']


class EditTermDialog(QDialog):
    """용어 수정 다이얼로그"""
    
    def __init__(self, parent=None, term_data=None, references=None):
        super().__init__(parent)
        self.term_data = term_data
        self.image_path = ''
        self.references = list(references) if references else []  # [(id, ref_type, title, content), ...]
        self.deleted_ref_ids = []
        self.new_references = []  # 새로 추가된 것 [(ref_type, title, content), ...]
        self.init_ui()
        self.load_data()

    def init_ui(self):
        self.setWindowTitle('용어 수정')
        self.setMinimumWidth(550)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # ── 탭1: 기본 정보 ──────────────────────────────────────
        basic_tab = QWidget()
        basic_layout = QVBoxLayout()
        basic_tab.setLayout(basic_layout)

        abbr_layout = QHBoxLayout()
        abbr_label = QLabel('축약어:')
        abbr_label.setMinimumWidth(80)
        self.abbr_input = QLineEdit()
        abbr_layout.addWidget(abbr_label)
        abbr_layout.addWidget(self.abbr_input)
        basic_layout.addLayout(abbr_layout)

        full_layout = QHBoxLayout()
        full_label = QLabel('원어:')
        full_label.setMinimumWidth(80)
        self.full_input = QLineEdit()
        full_layout.addWidget(full_label)
        full_layout.addWidget(self.full_input)
        basic_layout.addLayout(full_layout)

        basic_layout.addWidget(QLabel('정의:'))
        self.def_input = QTextEdit()
        self.def_input.setMaximumHeight(100)
        basic_layout.addWidget(self.def_input)

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
        basic_layout.addLayout(image_layout)
        basic_layout.addStretch()

        self.tabs.addTab(basic_tab, '기본 정보')

        # ── 탭2: 관련 규정/표준 ──────────────────────────────────
        ref_tab = QWidget()
        ref_layout = QVBoxLayout()
        ref_tab.setLayout(ref_layout)

        input_group = QWidget()
        input_layout = QVBoxLayout()
        input_group.setLayout(input_layout)

        row1 = QHBoxLayout()
        type_label = QLabel('구분:')
        type_label.setMinimumWidth(60)
        self.ref_type_combo = QComboBox()
        self.ref_type_combo.addItems(REF_TYPES)
        self.ref_type_combo.setMinimumWidth(120)
        title_label = QLabel('제목:')
        self.ref_title_input = QLineEdit()
        self.ref_title_input.setPlaceholderText('예) SOLAS Ch.II-2 Reg.4')
        row1.addWidget(type_label)
        row1.addWidget(self.ref_type_combo)
        row1.addWidget(title_label)
        row1.addWidget(self.ref_title_input, 1)
        input_layout.addLayout(row1)

        row2 = QHBoxLayout()
        content_label = QLabel('내용:')
        content_label.setMinimumWidth(60)
        self.ref_content_input = QTextEdit()
        self.ref_content_input.setMaximumHeight(70)
        self.ref_content_input.setPlaceholderText('규정 내용 요약 (선택)')
        add_ref_btn = QPushButton('추가')
        add_ref_btn.setFixedWidth(60)
        add_ref_btn.clicked.connect(self.add_reference_row)
        row2.addWidget(content_label)
        row2.addWidget(self.ref_content_input, 1)
        row2.addWidget(add_ref_btn)
        input_layout.addLayout(row2)

        ref_layout.addWidget(input_group)

        self.ref_table = QTableWidget()
        self.ref_table.setColumnCount(3)
        self.ref_table.setHorizontalHeaderLabels(['구분', '제목', '내용'])
        self.ref_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.ref_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.ref_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.ref_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.ref_table.setEditTriggers(QTableWidget.NoEditTriggers)
        ref_layout.addWidget(self.ref_table)

        del_ref_btn = QPushButton('선택 삭제')
        del_ref_btn.clicked.connect(self.delete_reference_row)
        ref_layout.addWidget(del_ref_btn, alignment=Qt.AlignRight)

        self.tabs.addTab(ref_tab, '관련 규정/표준')

        # ── 저장/취소 ────────────────────────────────────────────
        button_layout = QHBoxLayout()
        self.save_button = QPushButton('저장')
        self.save_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton('취소')
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addStretch()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

    def load_data(self):
        """기존 데이터 로드"""
        if self.term_data:
            _, abbreviation, full_term, definition, image_path = self.term_data
            self.abbr_input.setText(abbreviation)
            self.full_input.setText(full_term)
            self.def_input.setPlainText(definition if definition else '')
            if image_path and os.path.exists(image_path):
                self.image_path = image_path
                self.image_path_label.setText(os.path.basename(image_path))
                self.image_path_label.setStyleSheet('color: #000;')

        # 기존 규정 목록 로드
        for ref in self.references:
            ref_id, ref_type, title, content = ref
            row = self.ref_table.rowCount()
            self.ref_table.insertRow(row)
            self.ref_table.setItem(row, 0, QTableWidgetItem(ref_type))
            self.ref_table.setItem(row, 1, QTableWidgetItem(title))
            self.ref_table.setItem(row, 2, QTableWidgetItem(content or ''))

    # ── 이미지 ───────────────────────────────────────────────────

    def select_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, '이미지 선택', '',
            'Images (*.png *.jpg *.jpeg *.bmp *.gif)'
        )
        if file_path:
            try:
                filename = os.path.basename(file_path)
                dest_dir = 'images'
                os.makedirs(dest_dir, exist_ok=True)
                dest_path = os.path.join(dest_dir, filename)
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
        self.image_path = ''
        self.image_path_label.setText('이미지 없음')
        self.image_path_label.setStyleSheet('color: #888;')

    # ── 규정 ─────────────────────────────────────────────────────

    def add_reference_row(self):
        title = self.ref_title_input.text().strip()
        if not title:
            QMessageBox.warning(self, '입력 오류', '제목을 입력해주세요.')
            return
        ref_type = self.ref_type_combo.currentText()
        content = self.ref_content_input.toPlainText().strip()

        # 새로 추가된 항목은 id=None 으로 표시
        self.references.append((None, ref_type, title, content))
        self.new_references.append((ref_type, title, content))

        row = self.ref_table.rowCount()
        self.ref_table.insertRow(row)
        self.ref_table.setItem(row, 0, QTableWidgetItem(ref_type))
        self.ref_table.setItem(row, 1, QTableWidgetItem(title))
        self.ref_table.setItem(row, 2, QTableWidgetItem(content))

        self.ref_title_input.clear()
        self.ref_content_input.clear()

    def delete_reference_row(self):
        selected = self.ref_table.selectedItems()
        if not selected:
            return
        row = selected[0].row()
        ref = self.references[row]
        if ref[0] is not None:  # 기존 DB 항목이면 삭제 목록에 추가
            self.deleted_ref_ids.append(ref[0])
        self.ref_table.removeRow(row)
        del self.references[row]

    # ── 데이터 반환 ──────────────────────────────────────────────

    def get_data(self):
        return (
            self.abbr_input.text().strip(),
            self.full_input.text().strip(),
            self.def_input.toPlainText().strip(),
            self.image_path
        )

    def get_new_references(self):
        return self.new_references

    def get_deleted_ref_ids(self):
        return self.deleted_ref_ids

    def accept(self):
        abbreviation, full_term, _, _ = self.get_data()
        if not abbreviation:
            QMessageBox.warning(self, '입력 오류', '축약어를 입력해주세요.')
            self.tabs.setCurrentIndex(0)
            self.abbr_input.setFocus()
            return
        if not full_term:
            QMessageBox.warning(self, '입력 오류', '원어를 입력해주세요.')
            self.tabs.setCurrentIndex(0)
            self.full_input.setFocus()
            return
        super().accept()