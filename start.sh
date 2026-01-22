#!/bin/bash

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функция для вывода заголовка
print_header() {
    echo -e "${BLUE}========================================"
    echo -e "    SFA Secure File Program Launcher"
    echo -e "========================================${NC}"
    echo
}

# Функция для проверки зависимостей
check_dependencies() {
    echo -e "${YELLOW}Проверка зависимостей...${NC}"
    echo

    # Проверка Python
    echo -n "Проверка Python... "
    if command -v python3 &> /dev/null; then
        echo -e "${GREEN}✅ Установлен${NC}"
    elif command -v python &> /dev/null; then
        echo -e "${GREEN}✅ Установлен${NC}"
    else
        echo -e "${RED}❌ Не установлен${NC}"
        echo "Установите Python 3.8+: https://python.org/"
    fi

    # Проверка библиотеки cryptography
    echo -n "Проверка библиотеки cryptography... "
    if python3 -c "import cryptography" &> /dev/null 2>&1; then
        echo -e "${GREEN}✅ Установлена${NC}"
    elif python -c "import cryptography" &> /dev/null 2>&1; then
        echo -e "${GREEN}✅ Установлена${NC}"
    else
        echo -e "${RED}❌ Не установлена${NC}"
        echo "Установите: pip install cryptography"
    fi

    echo
    echo -e "${GREEN}Проверка завершена!${NC}"
    read -p "Нажмите Enter для продолжения..."
}


# Главное меню
while true; do
    clear
    print_header
    echo "Выберите версию для запуска:"
    echo
    echo "1. Проверить зависимости"
    echo "2. Выход"
    echo
    read -p "Введите номер (1-2): " choice

    case $choice in
        1)
            check_dependencies
            ;;
        2)
            echo
            echo -e "${GREEN}До свидания!${NC}"
            exit 0
            ;;
        *)
            echo
            echo -e "${RED}Неверный выбор. Попробуйте снова.${NC}"
            read -p "Нажмите Enter для продолжения..."
            ;;
    esac
done 