#!/usr/bin/env python3
"""
SFA Secure File Program - Folder Encryption Script
"""

import sys
import os
import logging
from pathlib import Path
from encrypt_file import encrypt_file

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('folder_encryption.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def encrypt_folder(folder_path: str, password: str) -> bool:
    """Шифрование папки"""
    try:
        path_obj = Path(folder_path)
        
        if not path_obj.exists():
            logger.error(f"Папка не найдена: {folder_path}")
            return False
            
        if not path_obj.is_dir():
            logger.error(f"Путь не является папкой: {folder_path}")
            return False

        # Получаем список всех файлов в папке
        files_to_encrypt = []
        for file_path in path_obj.rglob('*'):
            if file_path.is_file() and not file_path.name.endswith('.encrypted'):
                files_to_encrypt.append(file_path)

        if not files_to_encrypt:
            logger.warning(f"В папке нет файлов для шифрования: {folder_path}")
            return True

        logger.info(f"Найдено {len(files_to_encrypt)} файлов для шифрования")

        # Шифруем каждый файл
        success_count = 0
        for file_path in files_to_encrypt:
            try:
                if encrypt_file(str(file_path), password):
                    success_count += 1
                    logger.info(f"Зашифрован файл: {file_path}")
                else:
                    logger.error(f"Ошибка шифрования файла: {file_path}")
            except Exception as e:
                logger.error(f"Исключение при шифровании файла {file_path}: {e}")

        logger.info(f"Успешно зашифровано {success_count} из {len(files_to_encrypt)} файлов")
        return success_count == len(files_to_encrypt)
        
    except Exception as e:
        logger.error(f"Ошибка при шифровании папки {folder_path}: {e}")
        return False

def main():
    """Главная функция"""
    if len(sys.argv) != 3:
        print("Использование: python encrypt_folder.py <путь_к_папке> <пароль>")
        sys.exit(1)
        
    folder_path = sys.argv[1]
    password = sys.argv[2]
    
    if not password:
        print("Ошибка: пароль не может быть пустым")
        sys.exit(1)
        
    logger.info(f"Начинаем шифрование папки: {folder_path}")
    
    success = encrypt_folder(folder_path, password)
    
    if success:
        print(f"Папка успешно зашифрована: {folder_path}")
    else:
        print(f"Ошибка при шифровании папки: {folder_path}")
        sys.exit(1)

if __name__ == "__main__":
    main() 