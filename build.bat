@echo off
echo ========================================
echo Shipbuilding Dictionary EXE Build
echo ========================================
echo.

echo [1/4] Cleaning previous build files...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist shipbuilding_dict.db del shipbuilding_dict.db
echo Done!
echo.

echo [2/4] Creating sample database...
python add_sample_data.py
echo Done!
echo.

echo [3/4] Building EXE with PyInstaller...
pyinstaller --clean shipbuilding_dict.spec
echo Done!
echo.

echo [4/4] Setting up distribution folder...
if exist "dist\ShipbuildingDictionary" (
    if not exist "dist\ShipbuildingDictionary\images" mkdir "dist\ShipbuildingDictionary\images"
    echo Copying database file...
    if exist shipbuilding_dict.db (
        copy /Y shipbuilding_dict.db "dist\ShipbuildingDictionary\"
        echo Database copied successfully!
    ) else (
        echo WARNING: shipbuilding_dict.db not found!
    )
    echo Distribution folder ready!
) else (
    echo ERROR: dist\ShipbuildingDictionary folder not found!
)
echo.

echo ========================================
echo Build completed!
echo Executable: dist\ShipbuildingDictionary\ShipbuildingDictionary.exe
echo Sample data included in shipbuilding_dict.db
echo ========================================
pause