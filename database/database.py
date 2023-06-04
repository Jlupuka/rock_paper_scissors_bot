import psycopg2

from config_data.config import Config, load_config


class DataBase:
    def __init__(self) -> None:
        config: Config = load_config()
        self.connection = psycopg2.connect(dbname=config.db.dbname, host=config.db.host, user=config.db.user,
                                           password=config.db.password, port=config.db.port)
        self.connection.autocommit = True

    def check_user(self, user_id: int) -> bool:
        with self.connection.cursor() as cursor:
            cursor.execute('''SELECT ID FROM users WHERE USER_ID=%s''', (user_id,))
            result_check = cursor.fetchone()
            cursor.close()
        return True if result_check else False

    def create_user(self, user_id: int) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute('''INSERT INTO users (USER_ID) VALUES (%s)''', (user_id,))
            cursor.close()

    def user(self, user_id: int) -> None:
        if not self.check_user(user_id=user_id):
            self.create_user(user_id=user_id)

    def get_count_win(self, user_id: int) -> int:
        with self.connection.cursor() as cursor:
            cursor.execute('''SELECT COUNT_WIN FROM users WHERE USER_ID=%s''', (user_id,))
            count_win: int = cursor.fetchone()[0]
            cursor.close()
        return count_win

    def get_count_lose(self, user_id: int) -> int:
        with self.connection.cursor() as cursor:
            cursor.execute('''SELECT COUNT_LOSE FROM users WHERE USER_ID=%s''', (user_id,))
            count_lose: int = cursor.fetchone()[0]
            cursor.close()
        return count_lose

    def get_count_game(self, user_id: int) -> int:
        with self.connection.cursor() as cursor:
            cursor.execute('''SELECT COUNT_GAME FROM users WHERE USER_ID=%s''', (user_id,))
            count_game: int = cursor.fetchone()[0]
            cursor.close()
        return count_game

    def get_percent_user_win(self, user_id: int) -> str:
        count_game = self.get_count_game(user_id=user_id)
        return f'{self.get_count_win(user_id=user_id) / count_game * 100:.2f}' if count_game else '0.00'

    def add_game(self, user_id: int) -> None:
        with self.connection.cursor() as cursor:
            old_count_game = self.get_count_game(user_id=user_id)
            cursor.execute('''UPDATE users SET COUNT_GAME=%s WHERE USER_ID=%s''', (old_count_game + 1, user_id,))
            cursor.close()

    def add_win(self, user_id: int) -> None:
        with self.connection.cursor() as cursor:
            old_count_win = self.get_count_win(user_id=user_id)
            cursor.execute('''UPDATE users SET COUNT_WIN=%s WHERE USER_ID=%s''', (old_count_win + 1, user_id,))
            cursor.close()

    def add_lose(self, user_id: int) -> None:
        with self.connection.cursor() as cursor:
            old_count_lose = self.get_count_lose(user_id=user_id)
            cursor.execute('''UPDATE users SET COUNT_LOSE=%s WHERE USER_ID=%s''', (old_count_lose + 1, user_id,))
            cursor.close()

    def clear_statistic(self, user_id: int) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute('''UPDATE users SET COUNT_GAME=0, COUNT_WIN=0, COUNT_LOSE=0 WHERE USER_ID=%s''', (user_id,))
            cursor.close()
