import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_products(self):
        sql = """CREATE TABLE IF NOT EXISTS Products (
        item_id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name VARCHAR, 
        photo VARCHAR, 
        description VARCHAR,
        puffs_number INT);
        """
        self.execute(sql, commit=True)

    def create_table_texts(self):
        sql = "CREATE TABLE IF NOT EXISTS Texts (position VARCHAR, text VARCHAR);"
        self.execute(sql, commit=True)

    def create_table_users(self):
        sql = "CREATE TABLE IF NOT EXISTS Users (user_id INT PRIMARY KEY);"
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_product(self, name: str, photo: str, description: str, puffs_number: int):
        sql = """
        INSERT INTO Products(name, photo, description, puffs_number) VALUES(?, ?, ?, ?)
        """
        self.execute(sql, parameters=(name, photo, description, puffs_number,), commit=True)

    def add_user(self, user_id: int):
        sql = "INSERT INTO Users(user_id) VALUES(?)"
        self.execute(sql, parameters=(user_id,), commit=True)

    def select_all_product_names_id(self):
        sql = """
        SELECT name, item_id FROM Products
        """
        return self.execute(sql, fetchall=True)

    def select_all_product_names_id_puffs(self):
        sql = "SELECT name, item_id, puffs_number FROM Products"
        return self.execute(sql, fetchall=True)

    def select_all_positions_texts(self):
        sql = """
        SELECT position FROM Texts
        """
        return self.execute(sql, fetchall=True)

    def select_all_users(self):
        sql = "SELECT * FROM Users"
        return self.execute(sql, fetchall=True)

    def select_all_puffs(self):
        sql = "SELECT puffs_number FROM Products"
        return self.execute(sql, fetchall=True)

    def select_product(self, **kwargs):
        sql = "SELECT * FROM Products WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def select_text(self, **kwargs):
        sql = "SELECT text FROM Texts WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def update_text(self, text, position):
        sql = f"""
        UPDATE Texts SET text=? WHERE position=?
        """
        return self.execute(sql, parameters=(text, position,), commit=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Products;", fetchone=True)

    def delete_product(self, **kwargs):
        sql = "DELETE FROM Products WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, commit=True)
