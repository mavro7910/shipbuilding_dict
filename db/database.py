import sqlite3
import os


class ShipbuildingDB:
    """조선업 축약어 사전 데이터베이스 관리 클래스"""
    
    def __init__(self, db_path='shipbuilding_dict.db'):
        """
        데이터베이스 초기화
        
        Args:
            db_path: 데이터베이스 파일 경로
        """
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
        """축약어 테이블 생성"""
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
            
            # 검색 속도 향상을 위한 인덱스 생성
            self.cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_abbreviation 
                ON terms(abbreviation)
            ''')
            
            self.cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_full_term 
                ON terms(full_term)
            ''')
            
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"테이블 생성 오류: {e}")
            return False
    
    def add_term(self, abbreviation, full_term, definition='', image_path=''):
        """
        새로운 축약어 추가
        
        Args:
            abbreviation: 축약어
            full_term: 원어
            definition: 정의
            image_path: 이미지 경로
            
        Returns:
            bool: 성공 여부
        """
        try:
            self.cursor.execute('''
                INSERT INTO terms (abbreviation, full_term, definition, image_path)
                VALUES (?, ?, ?, ?)
            ''', (abbreviation, full_term, definition, image_path))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            print(f"축약어 '{abbreviation}'는 이미 존재합니다.")
            return False
        except sqlite3.Error as e:
            print(f"데이터 추가 오류: {e}")
            return False
    
    def update_term(self, term_id, abbreviation, full_term, definition='', image_path=''):
        """
        기존 축약어 수정
        
        Args:
            term_id: 항목 ID
            abbreviation: 축약어
            full_term: 원어
            definition: 정의
            image_path: 이미지 경로
            
        Returns:
            bool: 성공 여부
        """
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
        """
        축약어 삭제
        
        Args:
            term_id: 항목 ID
            
        Returns:
            bool: 성공 여부
        """
        try:
            self.cursor.execute('DELETE FROM terms WHERE id=?', (term_id,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"데이터 삭제 오류: {e}")
            return False
    
    def search_terms(self, keyword):
        """
        축약어 또는 원어로 검색
        
        Args:
            keyword: 검색 키워드
            
        Returns:
            list: 검색 결과 리스트
        """
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
        """
        모든 축약어 조회
        
        Returns:
            list: 모든 축약어 리스트
        """
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
        """
        ID로 특정 축약어 조회
        
        Args:
            term_id: 항목 ID
            
        Returns:
            tuple: 축약어 정보
        """
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
    
    def close(self):
        """데이터베이스 연결 종료"""
        if self.conn:
            self.conn.close()