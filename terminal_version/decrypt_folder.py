#!/usr/bin/env python3
"""
SFA Secure File Program - Folder Decryption Script
"""

import sys
import os
import logging
from pathlib import Path
from decrypt_file import decrypt_file

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('folder_decryption.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def decrypt_folder(folder_path: str, password: str) -> bool:
    """Дешифрование папки"""
    try:
        path_obj = Path(folder_path)
        
        if not path_obj.exists():
            logger.error(f"Папка не найдена: {folder_path}")
            return False
            
        if not path_obj.is_dir():
            logger.error(f"Путь не является папкой: {folder_path}")
            return False

        # Получаем список всех зашифрованных файлов в папке
        files_to_decrypt = []
        for file_path in path_obj.rglob('*.encrypted'):
            if file_path.is_file():
                files_to_decrypt.append(file_path)

        if not files_to_decrypt:
            logger.warning(f"В папке нет зашифрованных файлов: {folder_path}")
            return True

        logger.info(f"Найдено {len(files_to_decrypt)} зашифрованных файлов")

        # Дешифруем каждый файл
        success_count = 0
        for file_path in files_to_decrypt:
            try:
                if decrypt_file(str(file_path), password):
                    success_count += 1
                    logger.info(f"Дешифрован файл: {file_path}")
                else:
                    logger.error(f"Ошибка дешифрования файла: {file_path}")
            except Exception as e:
                logger.error(f"Исключение при дешифровании файла {file_path}: {e}")

        logger.info(f"Успешно дешифровано {success_count} из {len(files_to_decrypt)} файлов")
        return success_count == len(files_to_decrypt)
        
    except Exception as e:
        logger.error(f"Ошибка при дешифровании папки {folder_path}: {e}")
        return False

def main():
    """Главная функция"""
    if len(sys.argv) != 3:
        print("Использование: python decrypt_folder.py <путь_к_папке> <пароль>")
        sys.exit(1)
        
    folder_path = sys.argv[1]
    password = sys.argv[2]
    
    if not password:
        print("Ошибка: пароль не может быть пустым")
        sys.exit(1)
        
    logger.info(f"Начинаем дешифрование папки: {folder_path}")
    
    success = decrypt_folder(folder_path, password)
    
    if success:
        print(f"Папка успешно дешифрована: {folder_path}")
    else:
        print(f"Ошибка при дешифровании папки: {folder_path}")
        sys.exit(1)

if __name__ == "__main__":
    main() 