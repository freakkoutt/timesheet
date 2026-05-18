"""
Окно входа в систему
"""
import tkinter as tk
from tkinter import messagebox
import sys
import os

# Добавляем путь к backend модулям
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.auth.login import authenticate_user


class LoginWindow:
    """Окно авторизации пользователя"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Timesheet System - Вход")
        self.root.geometry("400x350")
        self.root.resizable(False, False)
        
        # Переменные для полей
        self.login_var = tk.StringVar()
        self.password_var = tk.StringVar()
        
        self.create_widgets()
        self.center_window()
        
    def center_window(self):
        """Центрирование окна"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Создание интерфейса"""
        
        # Заголовок
        title = tk.Label(self.root, text="⏱️ TIMESHEET SYSTEM", 
                         font=("Arial", 18, "bold"), fg="#2c3e50")
        title.pack(pady=(30, 5))
        
        subtitle = tk.Label(self.root, text="Учёт рабочего времени",
                            font=("Arial", 10), fg="#7f8c8d")
        subtitle.pack(pady=(0, 30))
        
        # Рамка для формы
        frame = tk.Frame(self.root, padx=40, pady=10)
        frame.pack(fill="both", expand=True)
        
        # Поле Логин
        tk.Label(frame, text="Логин:", font=("Arial", 11), anchor="w").pack(fill="x", pady=(0, 5))
        login_entry = tk.Entry(frame, textvariable=self.login_var, font=("Arial", 11), 
                                relief="solid", bd=1)
        login_entry.pack(fill="x", pady=(0, 15))
        login_entry.focus()
        
        # Поле Пароль
        tk.Label(frame, text="Пароль:", font=("Arial", 11), anchor="w").pack(fill="x", pady=(0, 5))
        password_entry = tk.Entry(frame, textvariable=self.password_var, font=("Arial", 11),
                                    show="•", relief="solid", bd=1)
        password_entry.pack(fill="x", pady=(0, 20))
        
        # Кнопка Входа
        login_btn = tk.Button(frame, text="ВОЙТИ", font=("Arial", 12, "bold"),
                               bg="#3498db", fg="white", activebackground="#2980b9",
                               relief="flat", pady=8, command=self.handle_login)
        login_btn.pack(fill="x", pady=(0, 15))
        
        # Ссылка на регистрацию
        register_link = tk.Label(frame, text="Нет аккаунта? Зарегистрироваться",
                                  font=("Arial", 10), fg="#3498db", cursor="hand2")
        register_link.pack()
        register_link.bind("<Button-1>", lambda e: self.open_registration())
        
        # Статус
        self.status_label = tk.Label(self.root, text="", font=("Arial", 9), fg="#e74c3c")
        self.status_label.pack(side="bottom", pady=10)
        
        # Enter на клавиатуре
        self.root.bind('<Return>', lambda event: self.handle_login())
    
    def handle_login(self):
        """Обработка входа"""
        login = self.login_var.get().strip()
        password = self.password_var.get()
        
        if not login or not password:
            self.status_label.config(text="❌ Заполните все поля")
            return
        
        self.status_label.config(text="⏳ Проверка...")
        self.root.update()
        
        # Аутентификация
        result = authenticate_user(login, password)
        
        if result["success"]:
            self.status_label.config(text=f"✅ {result['message']}")
            self.root.after(1000, lambda: self.open_main_window(result))
        else:
            self.status_label.config(text=f"❌ {result['message']}")
            self.password_var.set("")
    
    def open_main_window(self, user_data):

"""Открыть главное окно"""
        self.root.destroy()
        messagebox.showinfo("Успех", f"Добро пожаловать, {user_data['full_name']}!\n"
                            f"Роль: {'Руководитель' if user_data['role'] == 'manager' else 'Сотрудник'}")
    
    def open_registration(self):
        """Открыть окно регистрации"""
        self.root.destroy()
        # Здесь будет вызов окна регистрации
        print("Открытие окна регистрации...")
    
    def run(self):
        """Запуск приложения"""
        self.root.mainloop()


if name == "__main__":
    app = LoginWindow()
    app.run()
