import pyodbc


class ModelLogin:
    def __init__(self):
        # Connect to your SQL Server database
        connection_string = 'DRIVER={SQL Server};SERVER=LAPTOPSN\SQLEXPRESST;DATABASE=qlnv;Trusted_Connection=yes'
        self.connection = pyodbc.connect(connection_string)
        self.cursor = self.connection.cursor()

    def verify_user(self, username, password):
        # Replace 'users' with your actual table name
        query = f"SELECT * FROM ThongTinLogin WHERE Username=? AND Pass=?"
        result = self.cursor.execute(query, (username, password)).fetchone()
        return result is not None

    def find_LoaiNV(self, username):
        # Replace 'users' with your actual table name
        query = f"SELECT LoaiNhanVien FROM ChamCongTongHop WHERE MaNhanVien=?"
        result = self.cursor.execute(query, (username,)).fetchone()
        return result[0] if result else None
