#!/usr/bin/env python3
"""
Тест совместимости шифрования и дешифрования
Проверяет, что файлы, зашифрованные шифровальщиком, корректно дешифруются дешифровальщиком
"""

import os
import tempfile
import hashlib
from encryptor import SecureFileEncryptor
from decryptor import SecureFileDecryptor

def create_test_file(content: str) -> str:
    """Создает временный тестовый файл"""
    fd, path = tempfile.mkstemp(suffix='.txt')
    with os.fdopen(fd, 'w', encoding='utf-8') as f:
        f.write(content)
    return path

def get_file_hash(file_path: str) -> str:
    """Вычисляет SHA-256 хеш файла"""
    with open(file_path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

def test_encryption_decryption():
    """Тест шифрования и дешифрования"""
    print("🔍 Тестирование совместимости шифрования и дешифрования...")
    
    # Создаем тестовые данные
    test_content = "Это тестовый файл для проверки шифрования и дешифрования.\n"
    test_content += "Содержит русский текст и специальные символы: !@#$%^&*()\n"
    test_content += "И числа: 1234567890\n"
    
    # Создаем временный файл
    original_file = create_test_file(test_content)
    original_hash = get_file_hash(original_file)
    
    print(f"📄 Создан тестовый файл: {original_file}")
    print(f"🔢 Хеш оригинального файла: {original_hash[:16]}...")
    
    try:
        # Инициализируем шифровальщик и дешифровальщик
        encryptor = SecureFileEncryptor()
        decryptor = SecureFileDecryptor()
        
        # Тестовый пароль
        password = "TestPassword123!"
        
        print(f"🔐 Тестовый пароль: {password}")
        
        # Шифруем файл
        print("🔒 Шифрование файла...")
        encrypted_file = encryptor.encrypt_file(original_file, password)
        print(f"✅ Файл зашифрован: {encrypted_file}")
        
        # Проверяем, что зашифрованный файл существует
        if not os.path.exists(encrypted_file):
            raise Exception("Зашифрованный файл не создан")
        
        # Дешифруем файл
        print("🔓 Дешифрование файла...")
        decrypted_file = decryptor.decrypt_file(encrypted_file, password)
        print(f"✅ Файл дешифрован: {decrypted_file}")
        
        # Проверяем, что дешифрованный файл существует
        if not os.path.exists(decrypted_file):
            raise Exception("Дешифрованный файл не создан")
        
        # Сравниваем хеши
        decrypted_hash = get_file_hash(decrypted_file)
        print(f"🔢 Хеш дешифрованного файла: {decrypted_hash[:16]}...")
        
        if original_hash == decrypted_hash:
            print("✅ ТЕСТ ПРОЙДЕН: Хеши совпадают!")
            
            # Читаем содержимое для дополнительной проверки
            with open(decrypted_file, 'r', encoding='utf-8') as f:
                decrypted_content = f.read()
            
            if decrypted_content == test_content:
                print("✅ ТЕСТ ПРОЙДЕН: Содержимое файлов идентично!")
                return True
            else:
                print("❌ ТЕСТ ПРОВАЛЕН: Содержимое файлов отличается!")
                return False
        else:
            print("❌ ТЕСТ ПРОВАЛЕН: Хеши не совпадают!")
            return False
            
    except Exception as e:
        print(f"❌ ОШИБКА ТЕСТА: {e}")
        return False
    
    finally:
        # Очищаем временные файлы
        try:
            if os.path.exists(original_file):
                os.remove(original_file)
            if 'encrypted_file' in locals() and os.path.exists(encrypted_file):
                os.remove(encrypted_file)
            if 'decrypted_file' in locals() and os.path.exists(decrypted_file):
                os.remove(decrypted_file)
            print("🧹 Временные файлы удалены")
        except Exception as e:
            print(f"⚠️ Ошибка при удалении временных файлов: {e}")

def test_wrong_password():
    """Тест с неправильным паролем"""
    print("\n🔍 Тестирование с неправильным паролем...")
    
    test_content = "Тест неправильного пароля"
    original_file = create_test_file(test_content)
    
    try:
        encryptor = SecureFileEncryptor()
        decryptor = SecureFileDecryptor()
        
        correct_password = "CorrectPassword123!"
        wrong_password = "WrongPassword456!"
        
        # Шифруем с правильным паролем
        encrypted_file = encryptor.encrypt_file(original_file, correct_password)
        
        # Пытаемся дешифровать с неправильным паролем
        try:
            decryptor.decrypt_file(encrypted_file, wrong_password)
            print("❌ ТЕСТ ПРОВАЛЕН: Файл дешифровался с неправильным паролем!")
            return False
        except Exception as e:
            if "HMAC" in str(e) or "пароль" in str(e).lower():
                print("✅ ТЕСТ ПРОЙДЕН: Неправильный пароль корректно отклонен")
                return True
            else:
                print(f"⚠️ Неожиданная ошибка: {e}")
                return False
                
    except Exception as e:
        print(f"❌ ОШИБКА ТЕСТА: {e}")
        return False
    
    finally:
        # Очищаем временные файлы
        try:
            if os.path.exists(original_file):
                os.remove(original_file)
            if 'encrypted_file' in locals() and os.path.exists(encrypted_file):
                os.remove(encrypted_file)
        except:
            pass

def main():
    """Главная функция тестирования"""
    print("🚀 Запуск тестов совместимости SFA Secure File Program v3.0")
    print("=" * 60)
    
    # Тест 1: Правильное шифрование и дешифрование
    test1_passed = test_encryption_decryption()
    
    # Тест 2: Неправильный пароль
    test2_passed = test_wrong_password()
    
    print("\n" + "=" * 60)
    print("📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:")
    print(f"✅ Тест шифрования/дешифрования: {'ПРОЙДЕН' if test1_passed else 'ПРОВАЛЕН'}")
    print(f"✅ Тест неправильного пароля: {'ПРОЙДЕН' if test2_passed else 'ПРОВАЛЕН'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ! Программа работает корректно.")
        return True
    else:
        print("\n❌ НЕКОТОРЫЕ ТЕСТЫ ПРОВАЛЕНЫ! Требуется отладка.")
        return False

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1) 