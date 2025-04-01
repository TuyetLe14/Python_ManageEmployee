# ketnoi.py
import pyodbc

class CnnDatabase:
    def __init__(self, server, database, username=None, password=None):
        if username and password:
            str_sql = f"DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}"
        else:
            str_sql = f"DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes"

        self.connection = pyodbc.connect(str_sql)
        self.cursor = self.connection.cursor()

    def execute_query(self, query):
        return self.cursor.execute(query)

    def execute(self, query):
        self.cursor.execute(query)
        self.cursor.commit()

    def insert_(self, sql, params=None):
        try:
            if params is None:
                self.cursor.execute(sql)
            else:
                self.cursor.execute(sql, params)
            self.connection.commit()
            print("Insert thành công.")
        except pyodbc.Error as e:
            print(f"Lỗi khi thực hiện insert: {e}")
            print(f"Query causing the error: {sql}")
            self.connection.rollback()

    def commit(self):
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()

    def fetch_one(self, query, params=None):
        cursor = self.cursor.execute(query, params)
        return cursor.fetchone()

    def select(self, query, params=None):
        cursor = self.cursor.execute(query, params)
        return cursor.fetchall()

    def delete(self, query, params=None):
        try:
            if params is None:
                self.cursor.execute(query)
            else:
                self.cursor.execute(query, params)
            self.connection.commit()
            print("Xóa thành công.")
        except Exception as e:
            print(f"Lỗi khi thực hiện xóa: {e}")
            self.connection.rollback()

    def update(self, query, parameters=None):
        try:
            if parameters is None:
                self.cursor.execute(query)
            else:
                self.cursor.execute(query, parameters)
            self.connection.commit()
            print("Cập nhật thành công.")
        except Exception as e:
            print(f"Lỗi khi thực hiện cập nhật: {e}")
            self.connection.rollback()

    def rollback(self):
        if self.connection:
            self.connection.rollback()
