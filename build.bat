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
if exist "dist\ShipbuildingDictionary.exe" (
    echo Build successful!
    if exist shipbuilding_dict.db (
        echo NOTE: DB file needs to be placed next to exe manually.
    )
) else (
    echo ERROR: ShipbuildingDictionary.exe not found!
)
echo.

echo Cleaning up build folder...
if exist build rmdir /s /q build
echo Done!
echo.

echo ========================================
echo Build completed!
echo Executable: dist\ShipbuildingDictionary\ShipbuildingDictionary.exe
echo Sample data included in shipbuilding_dict.db
echo ========================================
pause