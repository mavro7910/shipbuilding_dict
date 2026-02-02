# 조선업 축약어 사전

조선업에서 사용되는 축약어와 용어를 관리하고 검색할 수 있는 데스크톱 애플리케이션입니다.

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

## 설치 방법

### 1. 저장소 클론

```bash
git clone <repository-url>
cd shipbuilding_dict
```

### 2. 필요한 패키지 설치

```bash
pip install -r requirements.txt
```

### 3. 애플리케이션 실행

```bash
python main.py
```

## EXE 파일 빌드 (배포용)

Python 환경 없이 실행 가능한 독립 실행 파일(.exe)을 만들 수 있습니다.

### Windows Build

**Using build script (Recommended)**
```batch
build.bat
```

This will:
1. Clean previous build files
2. Create a sample database with 15 shipbuilding terms
3. Build the EXE file
4. Copy the database to the distribution folder

**Manual build**
```batch
# Install PyInstaller (included in requirements.txt)
pip install pyinstaller

# (Optional) Create sample database
python add_sample_data.py

# Build EXE
pyinstaller --clean shipbuilding_dict.spec

# Create images folder
mkdir "dist\ShipbuildingDictionary\images"

# (Optional) Copy sample database
copy shipbuilding_dict.db "dist\ShipbuildingDictionary\"
```

After build completes, distribute the entire `dist\ShipbuildingDictionary\` folder.

### Linux/Mac Build

**Using build script**
```bash
# Run build script
chmod +x build.sh
./build.sh
```

This will create a sample database and build the executable automatically.

**Manual build**
```bash
# Install PyInstaller
pip install pyinstaller

# (Optional) Create sample database
python3 add_sample_data.py

# Build executable
pyinstaller --clean shipbuilding_dict.spec

# Create images folder
mkdir -p dist/ShipbuildingDictionary/images

# (Optional) Copy sample database
cp shipbuilding_dict.db dist/ShipbuildingDictionary/
```

### Build Customization

Edit `shipbuilding_dict.spec` file to customize build options:

- **Change icon**: `icon=None` → `icon='icon.ico'` (specify icon file path)
- **Show console**: `console=False` → `console=True` (useful for debugging)
- **Single file build**: Use `onefile=True` option instead of `a.binaries, a.zipfiles, a.datas`

### Distribution Notes

1. **Distribute entire folder**: You must distribute the entire `dist\ShipbuildingDictionary\` folder.
2. **Images folder**: The images folder is required for storing images.
3. **Database**: 
   - If built with build scripts, `shipbuilding_dict.db` includes 15 sample shipbuilding terms
   - Users can add/edit/delete terms after running the application
4. **Sample data included**: The build script automatically creates a database with terms like LNG, FPSO, DWT, VLCC, TEU, etc.

## 프로젝트 구조

```
shipbuilding_dict/
├── main.py              # 애플리케이션 진입점
├── requirements.txt     # 패키지 의존성
├── gui/                 # GUI 관련 코드
│   ├── __init__.py
│   ├── main_window.py   # 메인 윈도우
│   ├── add_dialog.py    # 추가 다이얼로그
│   └── edit_dialog.py   # 수정 다이얼로그
├── db/                  # 데이터베이스 관련 코드
│   ├── __init__.py
│   └── database.py      # DB 관리 클래스
└── images/              # 이미지 저장 폴더
```

## 사용 방법

### 용어 추가
1. 메인 화면에서 **추가** 버튼 클릭
2. 축약어, 원어, 정의 입력
3. 필요시 이미지 선택
4. **저장** 버튼 클릭

### 용어 검색
- 상단 검색창에 축약어 또는 원어를 입력하면 실시간으로 필터링됩니다.

### 용어 수정
1. 테이블에서 수정할 항목 선택
2. **수정** 버튼 클릭
3. 내용 수정 후 **저장** 버튼 클릭

### 용어 삭제
1. 테이블에서 삭제할 항목 선택
2. **삭제** 버튼 클릭
3. 확인 대화상자에서 **예** 선택

### 상세 정보 확인
- 테이블에서 항목을 선택하면 오른쪽 패널에 상세 정보가 표시됩니다.
- 축약어, 원어, 정의, 이미지를 확인할 수 있습니다.

## 데이터베이스

애플리케이션은 `shipbuilding_dict.db` 파일에 데이터를 저장합니다. 이 파일은 애플리케이션 실행 시 자동으로 생성됩니다.

### 데이터베이스 스키마

```sql
CREATE TABLE terms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    abbreviation TEXT NOT NULL UNIQUE,
    full_term TEXT NOT NULL,
    definition TEXT,
    image_path TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 샘플 데이터 추가

애플리케이션을 처음 실행한 후, 다음과 같은 조선업 용어들을 추가해보세요:

- **LNG**: Liquefied Natural Gas (액화천연가스)
- **FPSO**: Floating Production Storage and Offloading (부유식 원유생산저장하역설비)
- **DWT**: Deadweight Tonnage (재화중량톤수)
- **GT**: Gross Tonnage (총톤수)
- **LPG**: Liquefied Petroleum Gas (액화석유가스)

## 주의사항

- 이미지 파일은 `images/` 폴더에 자동으로 복사됩니다.
- 축약어는 중복될 수 없습니다.
- 데이터베이스 파일(`shipbuilding_dict.db`)을 백업하여 데이터를 보관하세요.

## 라이선스

MIT License

## 기여

이슈나 풀 리퀘스트는 언제든 환영합니다!