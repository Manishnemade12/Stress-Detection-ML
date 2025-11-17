@echo off
echo ========================================
echo    Stress Detection ML - Full Version
echo ========================================
echo.

echo Starting full application with ML model...
echo Note: Requires TensorFlow and trained model
echo.

cd /d "%~dp0"
python main.py

pause
