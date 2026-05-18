"""
Модуль регистрации пользователя
"""
import sqlite3
import bcrypt
import re
from typing import Dict

class UserRegistration:
    """Класс для регистрации новых пользователей"""
    
    def __init__(self, db_path: str = "timesheet.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Создание таблицы пользователей"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    login TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    full_name TEXT NOT NULL,
                    role TEXT NOT NULL CHECK(role IN ('employee', 'manager')),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
    
    def _validate_login(self, login: str):
        """Проверка логина"""
        if not login:
            return False, "Логин не может быть пустым"
        if len(login) < 3:
            return False, "Логин должен быть не менее 3 символов"
        if len(login) > 20:
            return False, "Логин не может быть длиннее 20 символов"
        if not re.match(r'^[a-zA-Z0-9_]+$', login):
            return False, "Логин может содержать только латинские буквы, цифры и подчёркивание"
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE login = ?", (login,))
            if cursor.fetchone():
                return False, "Пользователь с таким логином уже существует"
        
        return True, None
    
    def _validate_password(self, password: str):
        """Проверка пароля"""
        if not password:
            return False, "Пароль не может быть пустым"
        if len(password) < 6:
            return False, "Пароль должен быть не менее 6 символов"
        if not re.search(r'\d', password):
            return False, "Пароль должен содержать хотя бы одну цифру"
        if not re.search(r'[a-zA-Z]', password):
            return False, "Пароль должен содержать хотя бы одну букву"
        return True, None
    
    def _validate_full_name(self, full_name: str):
        """Проверка ФИО"""
        if not full_name:
            return False, "ФИО не может быть пустым"
        if len(full_name) < 2:
            return False, "ФИО должно содержать хотя бы 2 символа"
        return True, None
    
    def _validate_role(self, role: str):
        """Проверка роли"""
        if role not in ['employee', 'manager']:
            return False, "Роль должна быть 'employee' или 'manager'"
        return True, None
    
    def register_user(self, login: str, password: str, full_name: str, role: str = 'employee') -> Dict:
        """Главная функция регистрации"""
        
        # Валидация
        for validator, value in [
            (self._validate_login, login),
            (self._validate_password, password),
            (self._validate_full_name, full_name),
            (self._validate_role, role)
        ]:
            is_valid, error = validator(value)
            if not is_valid:
                return {'success': False, 'message': error, 'user_id': None}
        
        # Хеширование пароля
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
        
        # Сохранение в БД
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO users (login, password_hash, full_name, role)
                    VALUES (?, ?, ?, ?)
                """, (login, password_hash, full_name, role))
                conn.commit()
                
                return {
                    'success': True,
                    'message': f"Пользователь {login} успешно зарегистрирован",
                    'user_id': cursor.lastrowid
                }
        except Exception as e:
            return {'success': False, 'message': f"Ошибка: {str(e)}", 'user_id': None}


def register_user(login: str, password: str, full_name: str, role: str = 'employee', db_path: str = "timesheet.db") -> Dict:
    """Упрощённая функция для вызова"""
    reg = UserRegistration(db_path)
    return reg.register_user(login, password, full_name, role)


if __name__ == "__main__":
    print("=== Тестирование регистрации ===")
    result = register_user("testuser", "pass123", "Тестовый Пользователь", "employee")
    print(result)
