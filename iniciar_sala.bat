@echo off
:: Configurar la consola a UTF-8
chcp 65001 >nul
title Sala de Mapas - Servidor Activo
color 0E

echo ==================================================================================================
echo ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣄⣠⣀⡀⣀⣠⣤⣤⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
echo ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣄⢠⣠⣼⣿⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⢠⣤⣦⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⢦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
echo ⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣟⣾⣿⣽⣿⣿⣅⠈⠉⠻⣿⣿⣿⣿⣿⡿⠇⠀⠀⠀⠀⠀⠉⠀⠀⠀⠀⠀⢀⡶⠒⢉⡀⢠⣤⣶⣶⣿⣷⣆⣀⡀⠀⢲⣖⠒⠀⠀⠀⠀⠀⠀⠀
echo ⢀⣤⣾⣶⣦⣤⣤⣶⣿⣿⣿⣿⣿⣿⣽⡿⠻⣷⣀⠀⢻⣿⣿⣿⡿⠟⠀⠀⠀⠀⠀⠀⣤⣶⣶⣤⣀⣀⣬⣷⣦⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣦⣤⣦⣼⣀⠀
echo ⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠓⣿⣿⠟⠁⠘⣿⡟⠁⠀⠘⠛⠁⠀⠀⢠⣾⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠏⠙⠁
echo ⠀⠸⠟⠋⠀⠈⠙⣿⣿⣿⣿⣿⣿⣷⣦⡄⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⣼⣆⢘⣿⣯⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡉⠉⢱⡿⠀⠀⠀⠀⠀
echo ⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⡿⠦⠀⠀⠀⠀⠀⠀⠀⠙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⡗⠀⠈⠀⠀⠀⠀⠀⠀
echo                                                                                                         [ L O D T E ]
echo ==================================================================================================
echo.
echo                       CONECTANDO A LA NUBE...
echo.

echo Comprobando el motor y las librerias cloud...
:: Agregamos la comprobacion de 'dns' que es la que usa MongoDB SRV
python -c "import flask, pymongo, cloudinary, dns" >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Instalando dependencias de la nube...
    :: Instalamos pymongo con soporte para srv
    pip install flask "pymongo[srv]" cloudinary
    echo [OK] Dependencias instaladas.
) else (
    echo [OK] Sistemas en linea.
)
echo.

echo Iniciando el servidor y abriendo tu navegador...
start /b cmd /c "ping localhost -n 3 >nul & start http://localhost:5000"

echo.
echo EL SERVIDOR ESTA CORRIENDO AQUI MISMO.
echo Para terminar la sesion, simplemente CIERRA ESTA VENTANA NEGRA (X).
echo.
echo --------------------------------------------------------------------------------------------------

:: Ejecutamos el servidor
python sala_de_mapas.py

:: Si el servidor falla y se corta, el PAUSE evita que la ventana se cierre
echo.
echo [ERROR CRITICO] El servidor de Python se detuvo inesperadamente.
pause