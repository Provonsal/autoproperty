set "venv=.windows_venv"
set "activate=Scripts\activate.bat"
set "activation=%venv%\%activate%"
set "libs=setuptools cython"

echo "Проверка существования виртуального окружения..."

if exist "%venv%" (
    :venv_exist
    echo "Активируем окружение..."
    call %activation%
    echo "Устанавливаем библиотеки..."
    pip install %libs%
    echo "Собираем cython..."
    py autoproperty/setup.py build_ext --inplace
) else (
    echo "Окружение не найдено. Создаем..."
    python -m venv %venv%
    goto venv_exist
)

echo "Скрипт завершен"