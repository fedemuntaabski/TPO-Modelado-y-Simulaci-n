@echo off
echo.
echo ==========================================
echo   SIMULADOR MATEMATICO AVANZADO
echo   TPO Modelado y Simulacion 2025
echo ==========================================
echo.

echo Iniciando simulador matematico...
echo.

REM Verificar si Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado o no esta en el PATH
    echo Por favor instale Python 3.8 o superior desde https://python.org
    pause
    exit /b 1
)

echo Python detectado correctamente
echo.

REM Ejecutar el simulador
echo Ejecutando main.py...
python main.py

REM Si hay error, mostrar mensaje
if errorlevel 1 (
    echo.
    echo ERROR: Hubo un problema ejecutando el simulador
    echo Intente ejecutar manualmente: python main.py
    echo.
    pause
)

echo.
echo Simulador finalizado
pause
