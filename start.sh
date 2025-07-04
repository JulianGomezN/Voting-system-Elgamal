#!/bin/bash
echo "==================================="
echo "Sistema de Votacion Seguro ElGamal"
echo "==================================="
echo

echo "Verificando Python..."
python3 --version
if [ $? -ne 0 ]; then
    echo "ERROR: Python no esta instalado"
    exit 1
fi

echo
echo "Instalando dependencias..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: No se pudieron instalar las dependencias"
    exit 1
fi

echo
echo "Iniciando aplicacion..."
echo
echo "La aplicacion estara disponible en: http://localhost:5000"
echo
echo "Para crear el primer administrador, ve a: http://localhost:5000/admin/create_admin"
echo
echo "Presiona Ctrl+C para detener el servidor"
echo
python3 app.py
