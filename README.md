# 조선업 축약어 사전

조선업에서 사용되는 축약어와 용어를 관리하고 검색할 수 있는 Windows 데스크톱 애플리케이션입니다.

## 기능

- ✅ 축약어 및 원어 관리
- ✅ 용어 정의 입력
- ✅ 이미지 첨부 기능
- ✅ 실시간 검색 기능
- ✅ 직관적인 GUI 인터페이스
- ✅ SQLite 데이터베이스 기반

## 기술 스택

- **Python 3.x**
- **PyQt5**: GUI 프레임워크
- **SQLite**: 로컬 데이터베이스
- **PyInstaller**: 실행 파일 빌드

## 개발 환경 설정

### 1. 저장소 클론
```bash
git clone https://github.com/mavro7910/shipbuilding_dict.git
cd shipbuilding_dict
```

### 2. 패키지 설치
```bash
pip install -r requirements.txt
```

### 3. 애플리케이션 실행
```bash
python main.py
```

## EXE 빌드 (Windows)

### 빌드 스크립트 실행 (권장)
```bash
build.bat
```

자동으로 수행되는 작업:
1. 이전 빌드 파일 정리
2. 샘플 데이터베이스 생성 (조선업 용어 15개 포함)
3. 단일 EXE 파일 빌드
4. 빌드 중간 산출물(`build/`) 자동 삭제

### 빌드 결과물
```
dist/
└── ShipbuildingDictionary.exe  ← 단일 실행 파일
shipbuilding_dict.db            ← 데이터베이스 (exe 옆에 위치해야 함)
```

> ⚠️ **주의:** `ShipbuildingDictionary.exe`와 `shipbuilding_dict.db`는 **같은 폴더**에 있어야 합니다.

### 수동 빌드
```bash
# 샘플 DB 생성 (선택)
python add_sample_data.py

# EXE 빌드
pyinstaller --clean shipbuilding_dict.spec
```

## 프로젝트 구조
```
shipbuilding_dict/
├── main.py                # 애플리케이션 진입점
├── requirements.txt       # 패키지 의존성
├── shipbuilding_dict.spec # PyInstaller 빌드 설정
├── build.bat              # Windows 빌드 스크립트
├── add_sample_data.py     # 샘플 데이터 생성 스크립트
├── gui/                   # GUI 관련 코드
│   ├── __init__.py
│   ├── main_window.py     # 메인 윈도우
│   ├── add_dialog.py      # 추가 다이얼로그
│   └── edit_dialog.py     # 수정 다이얼로그
├── db/                    # 데이터베이스 관련 코드
│   ├── __init__.py
│   └── database.py        # DB 관리 클래스
└── images/                # 이미지 저장 폴더
```

## 사용 방법

### 용어 추가
1. **추가** 버튼 클릭
2. 축약어, 원어, 정의 입력
3. 필요시 이미지 선택
4. **저장** 버튼 클릭

### 용어 검색
- 상단 검색창에 축약어 또는 원어 입력 시 실시간 필터링

### 용어 수정
1. 테이블에서 항목 선택
2. **수정** 버튼 클릭 후 내용 수정
3. **저장** 버튼 클릭

### 용어 삭제
1. 테이블에서 항목 선택
2. **삭제** 버튼 클릭 후 확인

### 상세 정보 확인
- 항목 선택 시 오른쪽 패널에 축약어, 원어, 정의, 이미지 표시

## 데이터베이스 스키마
```sql
CREATE TABLE terms (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    abbreviation TEXT NOT NULL UNIQUE,
    full_term    TEXT NOT NULL,
    definition   TEXT,
    image_path   TEXT,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 주의사항

- 이미지 파일은 `images/` 폴더에 자동으로 복사됩니다.
- 축약어는 중복될 수 없습니다.
- `shipbuilding_dict.db` 파일을 정기적으로 백업하세요.

## 라이선스

MIT License