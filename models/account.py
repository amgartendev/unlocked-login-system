import config
import mysql.connector  # type: ignore
from models import connectdb  # type: ignore
from typing import Union


class Account:
    def __init__(self: object, user: str, email: str, password: str) -> None:
        self.__user: str = user
        self.__email: str = email
        self.__password: str = password

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.__user}, {self.__email}, {self.__password})'

    @property
    def user(self) -> str:
        return self.__user

    @property
    def email(self) -> str:
        return self.__email

    @property
    def password(self) -> str:
        return self.__password

    @staticmethod
    def check_user(user: str) -> bool:
        """Check if the user is already taken and return True"""
        db = connectdb.ConnectDB(config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_NAME)
        conn = db.connect()
        cursor = conn.cursor()

        sql = f"SELECT * FROM accounts WHERE user='{user}'"
        cursor.execute(sql)
        rows = cursor.fetchall()  # Fetch all rows from database table

        # Check if one or more users were find in the database with the same user passed as argument
        if len(rows) > 0:
            return True  # User already taken
        return False

    @staticmethod
    def check_email(email: str) -> bool:
        """Check if the email is already taken and return True"""
        db = connectdb.ConnectDB(config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_NAME)
        conn = db.connect()
        cursor = conn.cursor()

        sql = f"SELECT * FROM accounts WHERE email='{email}'"
        cursor.execute(sql)
        rows = cursor.fetchall()  # Fetch all rows from database table

        # Check if one or more emails were find in the database with the same email passed as argument
        if len(rows) > 0:
            return True  # Email already taken
        return False

    @staticmethod
    def send_account(*args) -> Union[bool, str]:
        """Send account details to the database"""

        account = tuple(args)

        try:
            db = connectdb.ConnectDB(config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_NAME)
            conn = db.connect()
            cursor = conn.cursor()

            sql_accounts = f"INSERT INTO accounts (user, email, password) " \
                           f"VALUES ('{account[0]}', '{account[1]}', '{account[2]}')"
            cursor.execute(sql_accounts)
            conn.commit()
            return True
        except mysql.connector.Error as errorMsg:
            return f'Error: {errorMsg}'

    @staticmethod
    def change_username(old_username: str, new_username: str) -> Union[bool, str]:
        """Change the username of the account and update it in the database"""
        db = connectdb.ConnectDB(config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_NAME)
        conn = db.connect()
        cursor = conn.cursor()

        try:
            sql = f"UPDATE accounts SET user='{new_username}' WHERE user='{old_username}'"
            cursor.execute(sql)
            conn.commit()
            return True
        except mysql.connector.Error as errorMsg:
            return f'Error: {errorMsg}'

    @staticmethod
    def change_email(old_email, new_email) -> Union[bool, str]:
        """Change the email of the account and update it in the database"""
        db = connectdb.ConnectDB(config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_NAME)
        conn = db.connect()
        cursor = conn.cursor()

        try:
            sql = f"UPDATE accounts SET email='{new_email}' WHERE user='{old_email}'"
            cursor.execute(sql)
            conn.commit()
            return True
        except mysql.connector.Error as errorMsg:
            return f'Error: {errorMsg}'

    @staticmethod
    def change_password(new_password: str, user: str) -> Union[bool, str]:
        """Change the password of the account and update it in the database"""
        db = connectdb.ConnectDB(config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_NAME)
        conn = db.connect()
        cursor = conn.cursor()

        try:
            sql = f"UPDATE accounts SET password='{new_password}' WHERE user='{user}'"
            cursor.execute(sql)
            conn.commit()
            return True
        except mysql.connector.Error as errorMsg:
            return f'Error: {errorMsg}'
