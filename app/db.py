from sqlite3 import connect


class DB:
    def __init__(self, db_name) -> None:
        self.connection = connect(database=db_name, check_same_thread=False)
        self.cur = self.connection.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS form_data(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, phone TEXT)"
        )

    def add_data(self, name, email, phone):
        self.cur.execute(
            "INSERT INTO form_data ('name', 'email', 'phone') VALUES(?, ?, ?)",
            (name, email, phone),
        )
        self.connection.commit()

    def get_all_data(self, table_name):
        res = self.cur.execute(f"SELECT * FROM {table_name}")
        data = res.fetchall()
        self.connection.commit()
        return data


db_con = DB("app_db.db")
