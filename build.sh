#!/bin/bash

echo "========================================"
echo "Shipbuilding Dictionary Build Script"
echo "========================================"
echo ""

echo "[1/4] Cleaning previous build files..."
rm -rf build dist shipbuilding_dict.db
echo "Done!"
echo ""

echo "[2/4] Creating sample database..."
python3 add_sample_data.py
echo "Done!"
echo ""

echo "[3/4] Building executable with PyInstaller..."
pyinstaller --clean shipbuilding_dict.spec
echo "Done!"
echo ""

echo "[4/4] Setting up distribution folder..."
if [ -d "dist/ShipbuildingDictionary" ]; then
    mkdir -p dist/ShipbuildingDictionary/images
    echo "Copying database file..."
    if [ -f "shipbuilding_dict.db" ]; then
        cp -v shipbuilding_dict.db dist/ShipbuildingDictionary/
        echo "Database copied successfully!"
    else
        echo "WARNING: shipbuilding_dict.db not found!"
    fi
    echo "Distribution folder ready!"
else
    echo "ERROR: dist/ShipbuildingDictionary folder not found!"
fi
echo ""

echo "========================================"
echo "Build completed!"
echo "Executable: dist/ShipbuildingDictionary/ShipbuildingDictionary"
echo "Sample data included in shipbuilding_dict.db"
echo "========================================"