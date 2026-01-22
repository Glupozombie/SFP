import os
import hmac
import hashlib
import logging
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Protocol.KDF import PBKDF2
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, ttk
import threading

# Настройка логирования
logging.basicConfig(
    filename='decryption.log', 
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class SecureFileDecryptor:
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
    
    def verify_hmac(self, hmac_key: bytes, encrypted_data: bytes, salt: bytes, expected_hmac: bytes) -> bool:
        """Проверка HMAC"""
        try:
            calculated_hmac = hmac.new(hmac_key, encrypted_data + salt, hashlib.sha256).digest()
            return hmac.compare_digest(calculated_hmac, expected_hmac)
        except Exception as e:
            logging.error(f"Ошибка проверки HMAC: {e}")
            return False
    
    def decrypt_file(self, file_path: str, password: str) -> str:
        """Дешифрование файла"""
        try:
            # Читаем зашифрованный файл
            with open(file_path, 'rb') as file:
                iv = file.read(16)
                file_content = file.read()
                # Новый разбор: [encrypted_data][hmac][salt]
                salt = file_content[-32:]
                hmac_value = file_content[-64:-32]
                encrypted_data = file_content[:-64]
            
            # Генерируем ключи
            encryption_key, hmac_key = self.generate_keys(password, salt)
            
            # Проверяем HMAC
            if not self.verify_hmac(hmac_key, encrypted_data, salt, hmac_value):
                raise ValueError("HMAC проверка не прошла. Файл может быть поврежден или пароль неверный.")
            
            # Дешифруем данные
            cipher = AES.new(encryption_key, AES.MODE_CBC, iv)
            decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
            
            # Сохраняем дешифрованный файл
            decrypted_file_path = file_path.replace('.encrypted', '.decrypted')
            with open(decrypted_file_path, 'wb') as decrypted_file:
                decrypted_file.write(decrypted_data)
            
            logging.info(f"Файл дешифрован: {decrypted_file_path}")
            return decrypted_file_path
            
        except Exception as e:
            logging.error(f"Ошибка дешифрования файла: {e}")
            raise
    
    def decrypt_folder(self, folder_path: str, password: str) -> list:
        """Дешифрование папки"""
        decrypted_files = []
        try:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    if file_path.endswith('.encrypted'):
                        decrypted_file = self.decrypt_file(file_path, password)
                        decrypted_files.append(decrypted_file)
            
            logging.info(f"Папка дешифрована: {folder_path}")
            return decrypted_files
            
        except Exception as e:
            logging.error(f"Ошибка дешифрования папки: {e}")
            raise

class DecryptorGUI:
    def __init__(self):
        self.decryptor = SecureFileDecryptor()
        self.setup_gui()
    
    def setup_gui(self):
        """Настройка графического интерфейса"""
        self.root = tk.Tk()
        self.root.title("SFP Secure File Decryptor v3.0")
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
            text="SFP Secure File Decryptor", 
            font=('Arial', 16, 'bold'),
            bg='#2b2b2b',
            fg='#00ff00'
        )
        title_label.pack(pady=20)
        
        # Фрейм для кнопок
        button_frame = tk.Frame(self.root, bg='#2b2b2b')
        button_frame.pack(pady=20)
        
        # Кнопки
        decrypt_file_btn = tk.Button(
            button_frame,
            text="Дешифровать файл",
            command=self.decrypt_file_gui,
            bg='#FF9800',
            fg='white',
            font=('Arial', 12),
            padx=20,
            pady=10,
            relief='flat'
        )
        decrypt_file_btn.pack(pady=10)
        
        decrypt_folder_btn = tk.Button(
            button_frame,
            text="Дешифровать папку",
            command=self.decrypt_folder_gui,
            bg='#9C27B0',
            fg='white',
            font=('Arial', 12),
            padx=20,
            pady=10,
            relief='flat'
        )
        decrypt_folder_btn.pack(pady=10)
        
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

    def decrypt_file_gui(self):
        """GUI для дешифрования файла (диалоги только в главном потоке)"""
        file_path = filedialog.askopenfilename(title="Выберите зашифрованный файл", filetypes=[("Encrypted files", "*.encrypted"), ("All files", "*.*")])
        if not file_path:
            self.update_status("Файл не выбран", '#ff0000')
            return
        password = simpledialog.askstring("Пароль", "Введите пароль для дешифрования:", show='*')
        if not password:
            self.update_status("Пароль не введен", '#ff0000')
            return
        def decrypt_thread():
            try:
                self.progress.start()
                self.update_status("Дешифрование...", '#ffff00')
                decrypted_file = self.decryptor.decrypt_file(file_path, password)
                self.update_status(f"Файл дешифрован: {os.path.basename(decrypted_file)}", '#00ff00')
                self.show_info("Успех", f"Файл успешно дешифрован!\nСохранен как: {decrypted_file}")
            except Exception as e:
                self.update_status(f"Ошибка: {str(e)}", '#ff0000')
                self.show_error("Ошибка", f"Ошибка дешифрования: {str(e)}")
            finally:
                self.progress.stop()
        threading.Thread(target=decrypt_thread, daemon=True).start()

    def decrypt_folder_gui(self):
        """GUI для дешифрования папки (диалоги только в главном потоке)"""
        folder_path = filedialog.askdirectory(title="Выберите папку с зашифрованными файлами")
        if not folder_path:
            self.update_status("Папка не выбрана", '#ff0000')
            return
        password = simpledialog.askstring("Пароль", "Введите пароль для дешифрования:", show='*')
        if not password:
            self.update_status("Пароль не введен", '#ff0000')
            return
        def decrypt_thread():
            try:
                self.progress.start()
                self.update_status("Дешифрование папки...", '#ffff00')
                decrypted_files = self.decryptor.decrypt_folder(folder_path, password)
                self.update_status(f"Дешифровано файлов: {len(decrypted_files)}", '#00ff00')
                self.show_info("Успех", f"Папка успешно дешифрована!\nДешифровано файлов: {len(decrypted_files)}")
            except Exception as e:
                self.update_status(f"Ошибка: {str(e)}", '#ff0000')
                self.show_error("Ошибка", f"Ошибка дешифрования: {str(e)}")
            finally:
                self.progress.stop()
        threading.Thread(target=decrypt_thread, daemon=True).start()
    
    def run(self):
        """Запуск GUI"""
        self.root.mainloop()

def main():
    """Главная функция"""
    try:
        app = DecryptorGUI()
        app.run()
    except Exception as e:
        logging.error(f"Критическая ошибка: {e}")
        messagebox.showerror("Критическая ошибка", f"Ошибка запуска: {str(e)}")

if __name__ == '__main__':
    main() 