from typing_extensions import Any

try:
    from .database_config import SQLBaseConnect
except ImportError as error:
    from database_config import SQLBaseConnect


class SQLUsersPart(SQLBaseConnect):
    def save_user(self, data_user: tuple) -> None:
        try:
            sql = '''
                INSERT INTO users(fio, email, phone_number, lang, is_admin, is_ceo, is_client, tg_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            '''
            fio, email, phone_number, lang, is_admin, is_ceo, is_client, tg_id = data_user
            self.manager(sql, fio, email, phone_number, lang, is_admin, is_ceo, is_client, tg_id, commit=True)
        except Exception as error:
            print(f'Ошибка {error.__class__} в db_create_products')

    def save_feedback(self, text: str, rating: int, datetime: Any, user_id: int) -> None:
        sql = '''
            INSERT INTO feedback(text, rating, datetime_creation, user_id)
            VALUES (%s, %s, %s, %s)
        '''
        self.manager(sql, text, rating, datetime, user_id, commit=True)

    def get_lang(self, tg_id: int) -> str:
        try:
            sql = '''
                SELECT lang FROM users WHERE tg_id = %s
            '''
            lang = self.manager(sql, tg_id, fetchone=True)
            if lang is not None:
                return lang[0]
            else:
                return '404'
        except Exception as error:
            print(f'Ошибка {error.__class__} в get_lang')

    def get_user(self, tg_id: int) -> tuple:
        try:
            sql = '''
                SELECT * FROM users WHERE tg_id = %s
            '''
            user = self.manager(sql, tg_id, fetchone=True)
            if user is not None:
                return user
            else:
                return ('404', )
        except Exception as error:
            print(f'Ошибка {error.__class__} в get_user')

    def change_lang(self, tg_id, new_lang):
        sql = '''
            UPDATE users SET
            lang = %s
            WHERE tg_id = %s
        '''
        self.manager(sql, new_lang, tg_id, commit=True)

    def get_feedback(self, type_filter: str, data: tuple) -> list:
        if type_filter == 'month':
            sql = '''
                SELECT text, rating, fio FROM feedback
                JOIN users USING (user_id) WHERE EXTRACT(MONTH FROM datetime_creation) = %s
            '''
            list_feedback = self.manager(sql, data[0], fetchall=True)
            return list_feedback
        elif type_filter == 'year':
            sql = '''
                SELECT text, rating, fio FROM feedback
                JOIN users USING (user_id) WHERE EXTRACT(YEAR FROM datetime_creation) = %s
            '''
            list_feedback = self.manager(sql, data[0], fetchall=True)
            return list_feedback
        elif type_filter == 'day':
            sql = '''
                SELECT text, rating, fio FROM feedback
                JOIN users USING (user_id) WHERE EXTRACT(DAY FROM datetime_creation) = %s
            '''
            list_feedback = self.manager(sql, data[0], fetchall=True)
            return list_feedback
        elif type_filter == 'custom':
            month, year = data
            sql = '''
                SELECT text, rating, fio FROM feedback 
                JOIN users USING (user_id) WHERE
                EXTRACT(YEAR FROM datetime_creation) = %s AND EXTRACT(MONTH FROM datetime_creation) = %s
            '''
            list_feedback = self.manager(sql, year, month, fetchall=True)
            return list_feedback

    def staff_manager(self, tg_id: int) -> str:
        sql = '''
            SELECT is_admin, is_ceo, is_client FROM users WHERE tg_id = %s
        '''
        is_admin, is_ceo, is_client = self.manager(sql, tg_id, fetchone=True)

        if is_ceo is True and is_admin is True and is_client is True:
            return 'CEO'
        elif is_ceo is False and is_admin is True and is_client is True:
            return 'ADMIN'
        elif is_ceo is False and is_admin is False and is_client is True:
            return 'CLIENT'
        else:
            return '404'

    def delete_employee(self, fio: str, phone_number: str) -> int:
        sql_check_user = 'SELECT * FROM users WHERE fio = %s AND phone_number = %s'
        status_code = self.manager(sql_check_user, fio, phone_number, fetchone=True)
        if status_code is None:
            return 404
        else:
            sql = 'DELETE FROM users WHERE fio = %s AND phone_number = %s'
            self.manager(sql, fio, phone_number, commit=True)

    def change_post(self, fio: str, phone_number: str, post: tuple) -> int:
        sql_check_user = 'SELECT * FROM users WHERE fio = %s AND phone_number = %s'
        status_code = self.manager(sql_check_user, fio, phone_number, fetchone=True)
        if status_code is None:
            return 404
        else:
            sql = '''
                UPDATE users SET
                    is_admin = %s, 
                    is_ceo = %s, 
                    is_client = %s
                WHERE fio = %s AND phone_number = %s
            '''
            is_admin, is_ceo, is_client = post
            self.manager(sql, is_admin, is_ceo, is_client, fio, phone_number, commit=True)

    def get_list_tg_id_admin(self) -> list:
        sql = '''
            SELECT tg_id FROM users WHERE is_admin = true AND is_ceo = true
            UNION ALL
            SELECT tg_id FROM users WHERE is_admin = true AND is_ceo = false;
        '''
        list_tg_id = self.manager(sql, fetchall=True)
        return [tg_id[0] for tg_id in list_tg_id]

    def get_list_employee(self) -> list:
        sql = '''
            SELECT fio, phone_number FROM users WHERE is_admin = true OR is_ceo = true
        '''
        list_employee = self.manager(sql, fetchall=True)
        return list_employee
