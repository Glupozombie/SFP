#!/usr/bin/env python3
"""
SFA Secure File Program - File Decryption Script
Совместим с основным дешифровальщиком
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
        logging.FileHandler('decryption.log', encoding='utf-8'),
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

def decrypt_file(file_path: str, password: str) -> bool:
    """Дешифрование файла"""
    try:
        path_obj = Path(file_path)
        
        if not path_obj.exists():
            logger.error(f"Файл не найден: {file_path}")
            return False
            
        if not path_obj.is_file():
            logger.error(f"Путь не является файлом: {file_path}")
            return False

        # Читаем зашифрованный файл
        with open(path_obj, 'rb') as f:
            encrypted_data = f.read()
            
        if not encrypted_data:
            logger.error(f"Файл пустой: {file_path}")
            return False

        # Проверяем заголовок
        if not encrypted_data.startswith(b'SFA_ENCRYPTED_FILE_V1\n'):
            logger.error(f"Неверный формат файла: {file_path}")
            return False

        # Извлекаем компоненты
        header_end = encrypted_data.find(b'\n') + 1
        salt = encrypted_data[header_end:header_end + 16]
        iv = encrypted_data[header_end + 16:header_end + 32]
        hmac_digest = encrypted_data[header_end + 32:header_end + 64]
        ciphertext = encrypted_data[header_end + 64:]

        # Генерируем ключ из пароля
        key = derive_key(password, salt)
        
        # Проверяем HMAC
        hmac_key = hashlib.sha256(key + salt).digest()
        hmac_obj = hmac.new(hmac_key, ciphertext, hashlib.sha256)
        expected_hmac = hmac_obj.digest()
        
        if not hmac.compare_digest(hmac_digest, expected_hmac):
            logger.error(f"HMAC не совпадает - файл поврежден или неверный пароль: {file_path}")
            return False

        # Создаем дешифр
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        
        # Дешифруем данные
        decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
        
        # Удаляем padding
        padding_length = decrypted_data[-1]
        if padding_length > 16 or padding_length < 1:
            logger.error(f"Неверный padding: {file_path}")
            return False
            
        original_data = decrypted_data[:-padding_length]
        
        # Сохраняем дешифрованный файл
        if path_obj.suffix == '.encrypted':
            decrypted_file_path = path_obj.with_suffix('')
        else:
            decrypted_file_path = path_obj.with_suffix(path_obj.suffix + '.decrypted')
            
        with open(decrypted_file_path, 'wb') as f:
            f.write(original_data)
            
        logger.info(f"Файл успешно дешифрован: {decrypted_file_path}")
        return True
        
    except Exception as e:
        logger.error(f"Ошибка при дешифровании файла {file_path}: {e}")
        return False

def main():
    """Главная функция"""
    if len(sys.argv) != 3:
        print("Использование: python decrypt_file.py <путь_к_файлу> <пароль>")
        sys.exit(1)
        
    file_path = sys.argv[1]
    password = sys.argv[2]
    
    if not password:
        print("Ошибка: пароль не может быть пустым")
        sys.exit(1)
        
    logger.info(f"Начинаем дешифрование файла: {file_path}")
    
    success = decrypt_file(file_path, password)
    
    if success:
        print(f"Файл успешно дешифрован: {file_path}")
    else:
        print(f"Ошибка при дешифровании файла: {file_path}")
        sys.exit(1)

if __name__ == "__main__":
    main() 