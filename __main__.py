import tkinter as tk
from tkinter import messagebox
import sys
import os

# Import encryptor/decryptor modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from encryptor import EncryptorGUI
    from decryptor import DecryptorGUI
except ImportError as e:
    messagebox.showerror("Ошибка импорта", f"Не удалось импортировать модули: {e}")
    sys.exit(1)


# --- THEMES ---
THEMES = {
    "dark": {
        "bg": "#23242a",
        "fg": "#f7f7f7",
        "btn": "#35363c",
        "btn_hover": "#44454b",
        "accent": "#4e8cff",
        "info": "#8ecfff",
        "shadow": "#111216",
    },
    "light": {
        "bg": "#f7f7f7",
        "fg": "#23242a",
        "btn": "#e0e0e0",
        "btn_hover": "#d0d0d0",
        "accent": "#007aff",
        "info": "#007aff",
        "shadow": "#cccccc",
    },
}

theme = "dark"


def c(name):
    return THEMES[theme][name]


# --- Rounded Canvas Button ---
class MacRoundButton(tk.Canvas):
    def __init__(self, master, text, command=None, width=260, height=60, radius=30, font=None):
        super().__init__(master, width=width, height=height, bg=c("bg"), highlightthickness=0, bd=0, cursor="hand2")
        self.text = text
        self.command = command
        self.radius = radius
        self.font = font or None
        self.hover = False

        self.bind("<Button-1>", lambda e: self.command and self.command())
        self.bind("<Enter>", lambda e: self._draw(True))
        self.bind("<Leave>", lambda e: self._draw(False))
        self.bind("<Configure>", lambda e: self._draw(self.hover))

        self._draw(False)

    def _draw(self, hover):
        self.hover = hover
        self.delete("all")
        w, h = self.winfo_width(), self.winfo_height()
        fill = c("btn_hover") if hover else c("btn")

        # Shadow
        self.create_rectangle(6, 8, w - 6, h - 2, fill=c("shadow"), outline="")
        # Button
        self.create_rectangle(4, 4, w - 4, h - 4, fill=fill, outline=c("accent"), width=2)
        # Text
        self.create_text(w // 2, h // 2, text=self.text, font=self.font, fill=c("fg"), anchor="c")


# --- MAIN APP ---
class MainApplication:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SFP (Secure File Program) v3.0")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        self.root.configure(bg=c("bg"))

        self.build_ui()
        self.apply_theme()

    def build_ui(self):
        # Theme toggle
        self.theme_btn = tk.Button(self.root, text="🌙", font=None, bd=0, command=self.toggle_theme, cursor="hand2")
        self.theme_btn.place(x=450, y=20, width=40, height=40)
        #self.theme_btn.place(x=840, y=20, width=40, height=40)

        # Title
        self.title = tk.Label(self.root, text="SFP (Secure File Program)", font=None)
        self.title.pack(pady=(40, 10))

        # Subtitle
        self.subtitle = tk.Label(self.root, text="Безопасное шифрование файлов", font=None)
        self.subtitle.pack(pady=(0, 30))

        # Buttons frame
        self.buttons_frame = tk.Frame(self.root, bg=c("bg"))
        self.buttons_frame.pack(pady=10)

        self.encrypt_btn = MacRoundButton(self.buttons_frame, "🔒 Шифрование", self.open_encryptor)
        #self.decrypt_btn = MacRoundButton(self.buttons_frame, "🔓 Дешифрование", self.open_decryptor)
        self.encrypt_btn.pack(pady=15)
        #self.decrypt_btn.pack(pady=15)

        # Info text
        info_lines = [
            "🔐 Алгоритмы безопасности:",
            "• AES-256 для шифрования",
            "• PBKDF2 с 100,000 итераций для генерации ключей",
            "• HMAC-SHA256 для проверки целостности",
            "• Случайные IV и соли для каждого файла",
            "\n",
            "⚠️ Важно: Без программы дешифрования и правильного пароля",
            "расшифровать файлы невозможно!"
        ]
        info_text = "\n".join(info_lines)

        self.info_label = tk.Label(self.root, text=info_text, font=None, justify="left", wraplength=850)
        self.info_label.pack(padx=25, pady=30)

        # Exit button
        self.exit_btn = MacRoundButton(self.root, "Выход", self.on_closing, width=180, height=52, font=None)
        self.exit_btn.pack(pady=20)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def apply_theme(self):
        self.root.configure(bg=c("bg"))
        self.title.configure(bg=c("bg"), fg=c("fg"))
        self.subtitle.configure(bg=c("bg"), fg=c("info"))
        self.info_label.configure(bg=c("bg"), fg=c("accent"))
        self.theme_btn.configure(bg=c("bg"), fg=c("accent"), activebackground=c("bg"), text="🌙" if theme == "dark" else "☀️")
        self.buttons_frame.configure(bg=c("bg"))
        #for btn in (self.encrypt_btn, """self.decrypt_btn""", self.exit_btn):
            #btn.configure(bg=c("bg"))
            #btn._draw(btn.hover)

    def toggle_theme(self):
        global theme
        theme = "light" if theme == "dark" else "dark"
        self.apply_theme()

    def open_encryptor(self):
        try:
            self.root.withdraw()
            enc = EncryptorGUI()
            enc.root.protocol("WM_DELETE_WINDOW", lambda: (enc.root.destroy(), self.root.deiconify()))
            enc.run()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось открыть шифровальщик: {e}")
            self.root.deiconify()

    """
    def open_decryptor(self):
        try:
            self.root.withdraw()
            dec = DecryptorGUI()
            dec.root.protocol("WM_DELETE_WINDOW", lambda: (dec.root.destroy(), self.root.deiconify()))
            dec.run()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось открыть дешифровальщик: {e}")
            self.root.deiconify()
    """

    def on_closing(self):
        if messagebox.askokcancel("Выход", "Вы уверены, что хотите выйти?"):
            self.root.destroy()

    def run(self):
        self.root.mainloop()


def check_dependencies():
    for m in ("Crypto", "tkinter", "hashlib", "hmac", "threading"):
        try:
            __import__(m)
        except ImportError:
            messagebox.showerror("Ошибка", f"Отсутствует модуль: {m}")
            return False
    return True


def main():
    if check_dependencies():
        MainApplication().run()


if __name__ == "__main__":
    main()
