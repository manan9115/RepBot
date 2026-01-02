@echo off
echo ========================================
echo RepBot Backend Server
echo ========================================
echo.

cd /d "%~dp0"

REM Check if Python 3.11 is available, if not use default python
py -3.11 --version >nul 2>&1
if errorlevel 1 (
    echo Using default Python version...
    set PYTHON_CMD=python
) else (
    echo Python 3.11 detected - using it for better MediaPipe compatibility
    set PYTHON_CMD=py -3.11
)

if not exist "venv" (
    echo Creating virtual environment...
    %PYTHON_CMD% -m venv venv
    echo.
)

echo Activating virtual environment...
call venv\Scripts\activate

if not exist "venv\Scripts\python.exe" (
    echo ERROR: Virtual environment not created properly!
    echo Please run: python -m venv venv
    pause
    exit
)

echo.
echo Checking dependencies...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo Installing core dependencies first...
    echo.
    pip install flask flask-cors numpy scikit-learn joblib Pillow
    echo.
    echo Installing OpenCV...
    pip install opencv-python
    echo.
    echo Attempting to install MediaPipe...
    pip install mediapipe
    if errorlevel 1 (
        echo.
        echo WARNING: MediaPipe installation failed!
        echo This might be due to Python version compatibility.
        echo.
        echo Trying alternative installation method...
        python -m pip install --upgrade pip setuptools wheel
        pip install mediapipe --no-cache-dir
        if errorlevel 1 (
            echo.
            echo ========================================
            echo MediaPipe installation failed!
            echo ========================================
            echo.
            echo Please check your Python version:
            python --version
            echo.
            echo MediaPipe requires Python 3.8-3.11
            echo For Python 3.12+, you may need to use:
            echo   pip install mediapipe --pre
            echo.
            echo The server will start but pose detection may not work.
            echo.
            pause
        )
    )
    echo.
)

echo.
echo Starting RepBot Backend Server...
echo Make sure your camera is connected!
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python app.py

pause

