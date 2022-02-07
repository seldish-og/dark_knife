import sqlite3


class History:
    def __init__(self) -> None:
        self.connection = sqlite3.connect("./history.sqlite")
        self.cursor = self.connection.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS history (result text)''')

    def append_result(self, result) -> None:
        self.cursor.execute("insert into history values (?);", [result])
        self.connection.commit()

    def get_results(self) -> None:
        self.cursor.execute(f"select * from history")
        response = self.cursor.fetchall()
        self.connection.commit()
        return response

    def close_connection(self) -> None:
        self.connection.close()
