# SFP Secure File Program

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-blue?style=flat-square" />
  <img src="https://img.shields.io/badge/Frontend-React-blue?style=flat-square" />
  <img src="https://img.shields.io/badge/Backend-Tauri%20%7C%20Python%20%7C%20Rust-orange?style=flat-square" />
  <img src="https://img.shields.io/badge/Security-AES--256%20%7C%20PBKDF2%20%7C%20HMAC-green?style=flat-square" />
</p>

---

# 🇷🇺 Русская версия

##  Описание
**SFA Secure File Program** — современное кроссплатформенное приложение для безопасного шифрования и дешифрования файлов. Интерфейс — React, ядро — Tauri (Rust) и Python. Всё просто, быстро и безопасно.

---

##  Быстрый старт

1. Установите [Node.js 18+](https://nodejs.org/), [Python 3.8+](https://python.org/) (с галочкой "Add to PATH"), [Rust](https://rustup.rs/)
2. `pip install -r requirements.txt`
3. Windows: `start.bat` | Linux/macOS: `chmod +x start.sh && ./start.sh`

---

##  Ручная установка

```bash
cd tauri-react
npm install
pip install -r ../requirements.txt
cargo install tauri-cli
npm run tauri dev
```

---

##  Структура проекта
```
SFA_Secure_File_Programm-main/
├── tauri-react/           # Основная папка приложения
│   ├── src/              # Исходники React (интерфейс)
│   ├── src-tauri/        # Ядро Tauri (Rust), конфиги, иконки
│   ├── python_scripts/   # Скрипты Python для шифрования/дешифрования
│   ├── package.json      # Node.js зависимости
│   └── ...
├── start.bat             # Быстрый запуск для Windows
├── start.sh              # Быстрый запуск для Linux/macOS
├── requirements.txt      # Python-зависимости
├── README.md             # Документация (этот файл)
├── БЫСТРЫЙ_ЗАПУСК.md     # Краткая инструкция
└── ...
```

---

##  Безопасность
- **Шифрование:** AES-256 (CBC)
- **Ключи:** PBKDF2 (100 000 итераций, соль)
- **Контроль целостности:** HMAC-SHA256
- **Каждый файл:** уникальная соль и IV
- **Пароли:** нигде не сохраняются

---

##  Как пользоваться
1. Запустите приложение
2. Выберите режим: "Зашифровать" или "Дешифровать"
3. Выберите файл или папку
4. Введите пароль (запомните его!)
5. Дождитесь завершения операции

---

##  Логи и отладка
- Все действия логируются:
  - `encryption.log` — шифрование
  - `decryption.log` — дешифрование
  - `folder_encryption.log` — шифрование папок
  - `folder_decryption.log` — дешифрование папок
- Если что-то не работает — проверьте эти логи!

---

## ❓ FAQ
- **Node.js не найден:** Установите с https://nodejs.org/ и перезагрузите ПК
- **Python не найден:** Установите с https://python.org/ ("Add to PATH")
- **cryptography не установлена:** `pip install cryptography`
- **Rust не найден:** `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh && cargo install tauri-cli`
- **Не запускается:** Запустите `start.bat` или `start.sh` — они сами проверят зависимости

---

##  Для новичков
1. Запустите `start.bat` (Windows) или `./start.sh` (Linux/macOS)
2. Если появится ошибка — следуйте подсказкам
3. Если не помогло — проверьте README.md и логи
4. Всё равно не работает? — напишите issue на GitHub

---

##  Лицензия
Этот проект предназначен для защиты ваших данных. Пароль не восстанавливается — храните его в надёжном месте!

---

##  Важно для пользователей Windows

> **Рекомендуется запускать проект через редактор кода** (например, [Cursor](https://www.cursor.so/) или [Visual Studio Code](https://code.visualstudio.com/)),
> чтобы избежать проблем с путями и правами доступа. Если запускать не из редактора, программа может не стартовать или работать некорректно!

---

# 🇬🇧 English version

##  Description
**SFA Secure File Program** is a modern cross-platform app for secure file encryption and decryption. UI — React, core — Tauri (Rust) & Python. Simple, fast, secure.

---

##  Quick Start

1. Install [Node.js 18+](https://nodejs.org/), [Python 3.8+](https://python.org/) (with "Add to PATH"), [Rust](https://rustup.rs/)
2. `pip install -r requirements.txt`
3. Windows: `start.bat` | Linux/macOS: `chmod +x start.sh && ./start.sh`

---

##  Manual install

```bash
cd tauri-react
npm install
pip install -r ../requirements.txt
cargo install tauri-cli
npm run tauri dev
```

---

##  Project structure
```
SFA_Secure_File_Programm-main/
├── tauri-react/           # Main app folder
│   ├── src/              # React frontend
│   ├── src-tauri/        # Tauri core (Rust), configs, icons
│   ├── python_scripts/   # Python scripts for encryption/decryption
│   ├── package.json      # Node.js dependencies
│   └── ...
├── start.bat             # Quick launch for Windows
├── start.sh              # Quick launch for Linux/macOS
├── requirements.txt      # Python dependencies
├── README.md             # Documentation (this file)
├── БЫСТРЫЙ_ЗАПУСК.md     # Quick start in Russian
└── ...
```

---

##  Security
- **Encryption:** AES-256 (CBC)
- **Keys:** PBKDF2 (100,000 iterations, salt)
- **Integrity:** HMAC-SHA256
- **Each file:** unique salt and IV
- **Passwords:** never stored

---

##  How to use
1. Launch the app
2. Choose mode: "Encrypt" or "Decrypt"
3. Select file or folder
4. Enter password (remember it!)
5. Wait for the operation to finish

---

##  Logs & troubleshooting
- All actions are logged:
  - `encryption.log` — encryption
  - `decryption.log` — decryption
  - `folder_encryption.log` — folder encryption
  - `folder_decryption.log` — folder decryption
- If something doesn't work — check these logs!

---

## ❓ FAQ
- **Node.js not found:** Install from https://nodejs.org/ and reboot
- **Python not found:** Install from https://python.org/ ("Add to PATH")
- **cryptography not installed:** `pip install cryptography`
- **Rust not found:** `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh && cargo install tauri-cli`
- **App won't start:** Run `start.bat` or `start.sh` — they will check dependencies for you

---

##  For beginners
1. Run `start.bat` (Windows) or `./start.sh` (Linux/macOS)
2. If you see an error — follow the instructions
3. If it doesn't help — check README.md and logs
4. Still not working? — open an issue on GitHub

---

##  License
This project is intended to protect your data. Passwords cannot be recovered — keep them safe!

---

##  Важно для пользователей Windows

> **Рекомендуется запускать проект через редактор кода** (например, [Cursor](https://www.cursor.so/) или [Visual Studio Code](https://code.visualstudio.com/)),
> чтобы избежать проблем с путями и правами доступа. Если запускать не из редактора, программа может не стартовать или работать некорректно!

---
