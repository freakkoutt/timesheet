"""
Модуль аутентификации пользователя
"""
import sqlite3
import bcrypt
from typing import Dict


def authenticate_user(login: str, password: str, db_path: str = "timesheet.db") -> Dict:
    """
    Проверка логина и пароля пользователя
    
    Returns:
        Dict с полями:
            success: bool
            role: str (employee/manager) - только при успехе
            full_name: str - только при успехе
            message: str - при ошибке
    """
    
    if not login or not password:
        return {'success': False, 'message': 'Заполните все поля'}
    
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, password_hash, full_name, role FROM users WHERE login = ?",
                (login,)
            )
            user = cursor.fetchone()
            
            if not user:
                return {'success': False, 'message': 'Неверный логин или пароль'}
            
            user_id, password_hash, full_name, role = user
            
            # Проверка пароля
            if bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8')):
                return {
                    'success': True,
                    'user_id': user_id,
                    'full_name': full_name,
                    'role': role,
                    'message': f'Добро пожаловать, {full_name}!'
                }
            else:
                return {'success': False, 'message': 'Неверный логин или пароль'}
                
    except Exception as e:
        return {'success': False, 'message': f'Ошибка: {str(e)}'}


if __name__ == "__main__":
    print("=== Тестирование аутентификации ===")
    
    # Сначала создадим тестового пользователя
    from register import register_user
    register_user("admin", "admin123", "Администратор", "manager")
    
    # Теперь проверим вход
    result = authenticate_user("admin", "admin123")
    print(result)
