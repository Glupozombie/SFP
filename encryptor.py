import os
import base64
import hmac
import hashlib
import time
import logging
import sys
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, ttk
import threading

# Настройка логирования
logging.basicConfig(
    filename='encryption.log', 
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class SecureFileEncryptor:
    def __init__(self):
        self.ITERATIONS = 100000  # PBKDF2 iterations
        self.KEY_SIZE = 32  # AES-256
        self.SALT_SIZE = 32
        self.HMAC_SIZE = 32
        
    def generate_keys(self, password: str, salt: bytes) -> tuple:
        """Генерация ключей шифрования и HMAC из пароля"""
        try:
            # Генерируем ключ шифрования
            encryption_key = PBKDF2(
                password,
                salt,
                dkLen=self.KEY_SIZE,
                count=self.ITERATIONS
            )
            
            # Генерируем ключ HMAC (используем ту же соль)
            hmac_key = PBKDF2(
                password,
                salt,
                dkLen=self.KEY_SIZE,
                count=self.ITERATIONS
            )
            
            return encryption_key, hmac_key
        except Exception as e:
            logging.error(f"Ошибка генерации ключей: {e}")
            raise
    
    def encrypt_file(self, file_path: str, password: str) -> str:
        """Шифрование файла"""
        try:
            # Генерируем соль
            salt = get_random_bytes(self.SALT_SIZE)
            
            # Генерируем ключи
            encryption_key, hmac_key = self.generate_keys(password, salt)
            
            # Читаем файл
            with open(file_path, 'rb') as file:
                file_data = file.read()
            
            # Генерируем IV
            iv = get_random_bytes(16)
            
            # Шифруем данные
            cipher = AES.new(encryption_key, AES.MODE_CBC, iv)
            encrypted_data = cipher.encrypt(pad(file_data, AES.block_size))
            
            # Создаем HMAC
            hmac_value = hmac.new(hmac_key, encrypted_data + salt, hashlib.sha256).digest()
            
            # Сохраняем зашифрованный файл
            encrypted_file_path = file_path + '.encrypted'
            with open(encrypted_file_path, 'wb') as encrypted_file:
                # Формат: IV + encrypted_data + HMAC + salt
                encrypted_file.write(iv)
                encrypted_file.write(encrypted_data)
                encrypted_file.write(hmac_value)
                encrypted_file.write(salt)
            
            logging.info(f"Файл зашифрован: {encrypted_file_path}")
            return encrypted_file_path
            
        except Exception as e:
            logging.error(f"Ошибка шифрования файла: {e}")
            raise
    
    def encrypt_folder(self, folder_path: str, password: str) -> list:
        """Шифрование папки"""
        encrypted_files = []
        try:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    if not file_path.endswith('.encrypted'):
                        encrypted_file = self.encrypt_file(file_path, password)
                        encrypted_files.append(encrypted_file)
            
            logging.info(f"Папка зашифрована: {folder_path}")
            return encrypted_files
            
        except Exception as e:
            logging.error(f"Ошибка шифрования папки: {e}")
            raise

class EncryptorGUI:
    def __init__(self):
        self.encryptor = SecureFileEncryptor()
        self.setup_gui()
    
    def setup_gui(self):
        """Настройка графического интерфейса"""
        self.root = tk.Tk()
        self.root.title("SFP Secure File Encryptor v3.0")
        self.root.geometry("600x400")
        self.root.configure(bg='#2b2b2b')
        
        # Стили
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', padding=10, font=('Arial', 10))
        style.configure('TLabel', background='#2b2b2b', foreground='white', font=('Arial', 10))
        
        # Заголовок
        title_label = tk.Label(
            self.root, 
            text="SFP Secure File Encryptor", 
            font=('Arial', 16, 'bold'),
            bg='#2b2b2b',
            fg='#00ff00'
        )
        title_label.pack(pady=20)
        
        # Фрейм для кнопок
        button_frame = tk.Frame(self.root, bg='#2b2b2b')
        button_frame.pack(pady=20)
        
        # Кнопки
        encrypt_file_btn = tk.Button(
            button_frame,
            text="Зашифровать файл",
            command=self.encrypt_file_gui,
            bg='#4CAF50',
            fg='white',
            font=('Arial', 12),
            padx=20,
            pady=10,
            relief='flat'
        )
        encrypt_file_btn.pack(pady=10)
        
        encrypt_folder_btn = tk.Button(
            button_frame,
            text="Зашифровать папку",
            command=self.encrypt_folder_gui,
            bg='#2196F3',
            fg='white',
            font=('Arial', 12),
            padx=20,
            pady=10,
            relief='flat'
        )
        encrypt_folder_btn.pack(pady=10)
        
        # Статус
        self.status_label = tk.Label(
            self.root,
            text="Готов к работе",
            bg='#2b2b2b',
            fg='#00ff00',
            font=('Arial', 10)
        )
        self.status_label.pack(pady=20)
        
        # Прогресс бар
        self.progress = ttk.Progressbar(
            self.root,
            mode='indeterminate'
        )
        self.progress.pack(pady=10, padx=50, fill='x')
    
    def update_status(self, message: str, color: str = '#00ff00'):
        """Обновление статуса (безопасно для потоков)"""
        def _update():
            if self.status_label.winfo_exists():
                self.status_label.config(text=message, fg=color)
        self.root.after(0, _update)

    def show_info(self, title, message):
        self.root.after(0, lambda: messagebox.showinfo(title, message, parent=self.root))

    def show_error(self, title, message):
        self.root.after(0, lambda: messagebox.showerror(title, message, parent=self.root))

    def encrypt_file_gui(self):
        """GUI для шифрования файла (диалоги только в главном потоке)"""
        file_path = filedialog.askopenfilename(title="Выберите файл для шифрования")
        if not file_path:
            self.update_status("Файл не выбран", '#ff0000')
            return
        password = simpledialog.askstring("Пароль", "Введите пароль для шифрования:", show='*')
        if not password:
            self.update_status("Пароль не введен", '#ff0000')
            return
        def encrypt_thread():
            try:
                self.progress.start()
                self.update_status("Шифрование...", '#ffff00')
                encrypted_file = self.encryptor.encrypt_file(file_path, password)
                self.update_status(f"Файл зашифрован: {os.path.basename(encrypted_file)}", '#00ff00')
                self.show_info("Успех", f"Файл успешно зашифрован!\nСохранен как: {encrypted_file}")
            except Exception as e:
                self.update_status(f"Ошибка: {str(e)}", '#ff0000')
                self.show_error("Ошибка", f"Ошибка шифрования: {str(e)}")
            finally:
                self.progress.stop()
        threading.Thread(target=encrypt_thread, daemon=True).start()

    def encrypt_folder_gui(self):
        """GUI для шифрования папки (диалоги только в главном потоке)"""
        folder_path = filedialog.askdirectory(title="Выберите папку для шифрования")
        if not folder_path:
            self.update_status("Папка не выбрана", '#ff0000')
            return
        password = simpledialog.askstring("Пароль", "Введите пароль для шифрования:", show='*')
        if not password:
            self.update_status("Пароль не введен", '#ff0000')
            return
        def encrypt_thread():
            try:
                self.progress.start()
                self.update_status("Шифрование папки...", '#ffff00')
                encrypted_files = self.encryptor.encrypt_folder(folder_path, password)
                self.update_status(f"Зашифровано файлов: {len(encrypted_files)}", '#00ff00')
                self.show_info("Успех", f"Папка успешно зашифрована!\nЗашифровано файлов: {len(encrypted_files)}")
            except Exception as e:
                self.update_status(f"Ошибка: {str(e)}", '#ff0000')
                self.show_error("Ошибка", f"Ошибка шифрования: {str(e)}")
            finally:
                self.progress.stop()
        threading.Thread(target=encrypt_thread, daemon=True).start()
    
    def run(self):
        """Запуск GUI"""
        self.root.mainloop()

def main():
    """Главная функция"""
    try:
        app = EncryptorGUI()
        app.run()
    except Exception as e:
        logging.error(f"Критическая ошибка: {e}")
        messagebox.showerror("Критическая ошибка", f"Ошибка запуска: {str(e)}")

if __name__ == '__main__':
    main() 