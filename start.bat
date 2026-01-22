@echo off
chcp 65001 >nul
echo ========================================
echo    SFA Secure File Program Launcher
echo ========================================
echo.
echo Выберите версию для запуска:
echo.
echo 2. Проверить зависимости
echo 3. Выход
echo.
set /p choice="Введите номер (1-2): "

if "%choice%"=="1" goto check
if "%choice%"=="3" goto exit
goto invalid

:check
echo.
echo Проверка зависимостей...
echo.

echo Проверка Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python не установлен. Установите Python 3.8+
    echo Скачайте с: https://python.org/
) else (
    echo ✅ Python установлен
)

echo Проверка библиотеки cryptography...
python -c "import cryptography" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Библиотека cryptography не установлена
    echo Установите: pip install cryptography
) else (
    echo ✅ Библиотека cryptography установлена
)

echo.
echo Проверка завершена!
pause
goto exit

:invalid
echo.
echo Неверный выбор. Попробуйте снова.
pause
goto start

:exit
echo.
echo До свидания!
pause 