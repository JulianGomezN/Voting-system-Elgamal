@echo off
echo ===================================
echo Sistema de Votacion Seguro ElGamal
echo ===================================
echo.

echo Verificando Python...
python --version
if errorlevel 1 (
    echo ERROR: Python no esta instalado
    pause
    exit /b 1
)

echo.
echo Instalando dependencias...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: No se pudieron instalar las dependencias
    pause
    exit /b 1
)

echo.
echo Iniciando aplicacion...
echo.
echo La aplicacion estara disponible en: http://localhost:5000
echo.
echo Para crear el primer administrador, ve a: http://localhost:5000/admin/create_admin
echo.
echo Presiona Ctrl+C para detener el servidor
echo.
python app.py
