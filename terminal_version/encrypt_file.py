#!/usr/bin/env python3
"""
SFA Secure File Program - File Encryption Script
Совместим с основным шифровальщиком
"""

import sys
import os
import base64
import hashlib
import hmac
import logging
from pathlib import Path
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('encryption.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def derive_key(password: str, salt: bytes) -> bytes:
    """Генерация ключа из пароля с использованием PBKDF2"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # 256 бит
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode('utf-8'))

def encrypt_file(file_path: str, password: str) -> bool:
    """Шифрование файла"""
    try:
        path_obj = Path(file_path)
        
        if not path_obj.exists():
            logger.error(f"Файл не найден: {file_path}")
            return False
            
        if not path_obj.is_file():
            logger.error(f"Путь не является файлом: {file_path}")
            return False

        # Читаем исходный файл
        with open(path_obj, 'rb') as f:
            data = f.read()
            
        if not data:
            logger.warning(f"Файл пустой: {file_path}")
            return False

        # Генерируем случайную соль и IV
        salt = os.urandom(16)
        iv = os.urandom(16)
        
        # Генерируем ключ из пароля
        key = derive_key(password, salt)
        
        # Создаем шифр
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        
        # Добавляем padding к данным
        padding_length = 16 - (len(data) % 16)
        padded_data = data + bytes([padding_length] * padding_length)
        
        # Шифруем данные
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        
        # Создаем HMAC для проверки целостности
        hmac_key = hashlib.sha256(key + salt).digest()
        hmac_obj = hmac.new(hmac_key, encrypted_data, hashlib.sha256)
        hmac_digest = hmac_obj.digest()
        
        # Формируем зашифрованный файл
        encrypted_file_data = (
            b'SFA_ENCRYPTED_FILE_V1\n' +  # Заголовок версии
            salt +                        # Соль (16 байт)
            iv +                          # IV (16 байт)
            hmac_digest +                 # HMAC (32 байта)
            encrypted_data                # Зашифрованные данные
        )
        
        # Сохраняем зашифрованный файл
        encrypted_file_path = path_obj.with_suffix(path_obj.suffix + '.encrypted')
        with open(encrypted_file_path, 'wb') as f:
            f.write(encrypted_file_data)
            
        logger.info(f"Файл успешно зашифрован: {encrypted_file_path}")
        return True
        
    except Exception as e:
        logger.error(f"Ошибка при шифровании файла {file_path}: {e}")
        return False

def main():
    """Главная функция"""
    if len(sys.argv) != 3:
        print("Использование: python encrypt_file.py <путь_к_файлу> <пароль>")
        sys.exit(1)
        
    file_path = sys.argv[1]
    password = sys.argv[2]
    
    if not password:
        print("Ошибка: пароль не может быть пустым")
        sys.exit(1)
        
    logger.info(f"Начинаем шифрование файла: {file_path}")
    
    success = encrypt_file(file_path, password)
    
    if success:
        print(f"Файл успешно зашифрован: {file_path}")
    else:
        print(f"Ошибка при шифровании файла: {file_path}")
        sys.exit(1)

if __name__ == "__main__":
    main() 