import sqlite3
import os


class ShipbuildingDB:
    """조선업 축약어 사전 데이터베이스 관리 클래스"""
    
    def __init__(self, db_path='shipbuilding_dict.db'):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_table()
    
    def connect(self):
        """데이터베이스 연결"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            return True
        except sqlite3.Error as e:
            print(f"데이터베이스 연결 오류: {e}")
            return False
    
    def create_table(self):
        """테이블 생성"""
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS terms (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    abbreviation TEXT NOT NULL UNIQUE,
                    full_term TEXT NOT NULL,
                    definition TEXT,
                    image_path TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # 관련 규정/표준 테이블
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS term_references (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    term_id INTEGER NOT NULL,
                    ref_type TEXT NOT NULL,
                    title TEXT NOT NULL,
                    content TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (term_id) REFERENCES terms(id) ON DELETE CASCADE
                )
            ''')

            self.cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_abbreviation 
                ON terms(abbreviation)
            ''')
            self.cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_full_term 
                ON terms(full_term)
            ''')
            self.cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_ref_term_id 
                ON term_references(term_id)
            ''')

            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"테이블 생성 오류: {e}")
            return False
    
    # ── terms CRUD ────────────────────────────────────────────────

    def add_term(self, abbreviation, full_term, definition='', image_path=''):
        try:
            self.cursor.execute('''
                INSERT INTO terms (abbreviation, full_term, definition, image_path)
                VALUES (?, ?, ?, ?)
            ''', (abbreviation, full_term, definition, image_path))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            print(f"축약어 '{abbreviation}'는 이미 존재합니다.")
            return None
        except sqlite3.Error as e:
            print(f"데이터 추가 오류: {e}")
            return None
    
    def update_term(self, term_id, abbreviation, full_term, definition='', image_path=''):
        try:
            self.cursor.execute('''
                UPDATE terms 
                SET abbreviation=?, full_term=?, definition=?, image_path=?, 
                    updated_at=CURRENT_TIMESTAMP
                WHERE id=?
            ''', (abbreviation, full_term, definition, image_path, term_id))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"데이터 수정 오류: {e}")
            return False
    
    def delete_term(self, term_id):
        try:
            self.cursor.execute('DELETE FROM terms WHERE id=?', (term_id,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"데이터 삭제 오류: {e}")
            return False
    
    def search_terms(self, keyword):
        try:
            self.cursor.execute('''
                SELECT id, abbreviation, full_term, definition, image_path 
                FROM terms 
                WHERE abbreviation LIKE ? OR full_term LIKE ?
                ORDER BY abbreviation
            ''', (f'%{keyword}%', f'%{keyword}%'))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"검색 오류: {e}")
            return []
    
    def get_all_terms(self):
        try:
            self.cursor.execute('''
                SELECT id, abbreviation, full_term, definition, image_path 
                FROM terms 
                ORDER BY abbreviation
            ''')
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"조회 오류: {e}")
            return []
    
    def get_term_by_id(self, term_id):
        try:
            self.cursor.execute('''
                SELECT id, abbreviation, full_term, definition, image_path 
                FROM terms 
                WHERE id=?
            ''', (term_id,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"조회 오류: {e}")
            return None

    # ── references CRUD ──────────────────────────────────────────

    def get_references(self, term_id):
        """특정 용어의 관련 규정 목록 조회"""
        try:
            self.cursor.execute('''
                SELECT id, ref_type, title, content
                FROM term_references
                WHERE term_id=?
                ORDER BY ref_type, title
            ''', (term_id,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"규정 조회 오류: {e}")
            return []

    def add_reference(self, term_id, ref_type, title, content=''):
        """관련 규정 추가"""
        try:
            self.cursor.execute('''
                INSERT INTO term_references (term_id, ref_type, title, content)
                VALUES (?, ?, ?, ?)
            ''', (term_id, ref_type, title, content))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"규정 추가 오류: {e}")
            return False

    def update_reference(self, ref_id, ref_type, title, content=''):
        """관련 규정 수정"""
        try:
            self.cursor.execute('''
                UPDATE term_references
                SET ref_type=?, title=?, content=?
                WHERE id=?
            ''', (ref_type, title, content, ref_id))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"규정 수정 오류: {e}")
            return False

    def delete_reference(self, ref_id):
        """관련 규정 삭제"""
        try:
            self.cursor.execute('DELETE FROM term_references WHERE id=?', (ref_id,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"규정 삭제 오류: {e}")
            return False

    def delete_references_by_term(self, term_id):
        """특정 용어의 모든 규정 삭제"""
        try:
            self.cursor.execute('DELETE FROM term_references WHERE term_id=?', (term_id,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"규정 일괄 삭제 오류: {e}")
            return False

    def close(self):
        """데이터베이스 연결 종료"""
        if self.conn:
            self.conn.close()