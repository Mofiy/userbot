import sqlite3
import time
from decimal import Decimal
import logging

__version__ = 0.0001


def adapt_decimal(d):
    return format(round(d, 14), 'f')


def convert_decimal(s):
    return Decimal(s)


class BotDatabase:
    def __init__(self, name: str):
        sqlite3.register_adapter(Decimal, adapt_decimal)
        sqlite3.register_converter("decimal", convert_decimal)
        self.name = name
        self.Initialise()

    def Initialise(self):
        """ Initialises the Database """

        conn = sqlite3.connect(self.name, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        # Create tables
        c.execute("CREATE TABLE IF NOT EXISTS users ("
                  "user_id INTEGER PRIMARY KEY, "
                  "first_name VARCHAR(50), "
                  "username VARCHAR(50), "
                  "chat_id INTEGER"
                  ")")
        conn.commit()

        logging.info("DB: DB ready to work")

    def save_user(self, user):
        """
        Adds a User to the Database
        user_id INTEGER PRIMARY KEY,
        first_name VARCHAR(50),
        username VARCHAR(50),
        chat_id INTEGER
        """
        conn = sqlite3.connect(self.name, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        values = (user["user_id"],
                  user["first_name"],
                  user["username"],
                  user["chat_id"])
        c.execute('INSERT INTO users VALUES (?, ?, ?, ?)', values)
        conn.commit()
        logging.info(f"DB: save user {user}")

    def get_user(self, user_id_or_name):
        """ Gets User details from Database

        return None - if new user
        return user info  if user registered already  """

        conn = sqlite3.connect(self.name, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE user_id = ? OR username = ?', (user_id_or_name, user_id_or_name))
        user = c.fetchone()
        result = None
        if user is not None:
            result = {"user_id": user["user_id"],
                        "first_name": user["first_name"],
                        "username": user["username"],
                        "chat_id": user["chat_id"]}

        logging.info(f"DB: get user {result}")
        return result

    def update_user(self, user_data):
        """ Updates a User within the Database """

        conn = sqlite3.connect(self.name, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        c.execute("UPDATE users SET "
                  "first_name = ?, "
                  "username = ?, "
                  "chat_id = ? "
                  "WHERE user_id = ?",
                  (user_data["first_name"],
                   user_data["username"],
                   user_data["chat_id"],
                   user_data["user_id"]))
        logging.info(f"DB: update user {user_data}")
        conn.commit()

    # def get_payed_users_list(self, take_stopped=True):
    #     """ Gets list of users  from Database who have positive balance
    #
    #     return [] - if no users
    #     return list of users if it finds them in DB"""
    #     conn = sqlite3.connect(self.name, detect_types=sqlite3.PARSE_DECLTYPES)
    #     conn.row_factory = sqlite3.Row
    #     c = conn.cursor()
    #     if take_stopped:
    #         c.execute("SELECT user_id, wallet FROM users WHERE wallet > 0")
    #     else:
    #         c.execute("SELECT user_id, wallet FROM users WHERE wallet > 0 AND stopped == 0")
    #     answer = c.fetchall()
    #     result = []
    #     if answer is not None:
    #         for row in answer:
    #             result.append([row['user_id'], row['wallet']])
    #         l = len(result)
    #         logging.info(f"DB: get users list with positive balance: {l} records")
    #     else:
    #         logging.info("DB: get users list with positive balance: None")
    #     return result
    #
    # def get_unpayed_users_list(self, take_stopped=True):
    #     """ Gets list of users  from Database who have zero balance
    #
    #     return [] - if no users
    #     return list of users if it finds them in DB"""
    #     conn = sqlite3.connect(self.name, detect_types=sqlite3.PARSE_DECLTYPES)
    #     conn.row_factory = sqlite3.Row
    #     c = conn.cursor()
    #     if take_stopped:
    #         c.execute("SELECT user_id, wallet FROM users WHERE wallet == 0")
    #     else:
    #         c.execute("SELECT user_id, wallet FROM users WHERE wallet == 0 AND stopped == 0")
    #     answer = c.fetchall()
    #     result = []
    #     if answer is not None:
    #         for row in answer:
    #             result.append([row['user_id'], row['wallet']])
    #         l = len(result)
    #         logging.info(f"DB: get users list with zero balance: {l} records")
    #     else:
    #         logging.info("DB: get users list with zero balance: None")
    #     return result
    #
    # def get_all_users_list(self, take_stopped=True):
    #     """ Gets all list of users from Database
    #
    #     return [] - if no users
    #     return list of users if it finds them in DB"""
    #     conn = sqlite3.connect(self.name, detect_types=sqlite3.PARSE_DECLTYPES)
    #     conn.row_factory = sqlite3.Row
    #     c = conn.cursor()
    #     if take_stopped:
    #         c.execute("SELECT user_id FROM users")
    #     else:
    #         c.execute("SELECT user_id FROM users WHERE stopped == 0")
    #     answer = c.fetchall()
    #     result = []
    #     if answer is not None:
    #         for row in answer:
    #             result.append(row['user_id'])
    #         pass
    #         logging.info(f"DB: get all users list from DB: {len(result)} records")
    #     else:
    #         logging.info("DB: get all users list from DB: None")
    #     return result
    #
    # def get_stopped_users(self):
    #     """ Gets users list from Database who has 1 in column stopped
    #
    #             return [] - if no users
    #             return list of users if it finds them in DB"""
    #     conn = sqlite3.connect(self.name, detect_types=sqlite3.PARSE_DECLTYPES)
    #     conn.row_factory = sqlite3.Row
    #     c = conn.cursor()
    #     c.execute("SELECT user_id FROM users WHERE stopped == 1")
    #     answer = c.fetchall()
    #     result = []
    #     if answer is not None:
    #         for row in answer:
    #             result.append(row['user_id'])
    #         pass
    #         logging.info(f"DB: get users list with stopped bot from DB: {len(result)} records")
    #     else:
    #         logging.info("DB: get users list with stopped bot from DB: None")
    #     return result
    #
    # def decrease_wallets_payed_users(self):
    #     """ Updates a User within the Database """
    #
    #     conn = sqlite3.connect(self.name, detect_types=sqlite3.PARSE_DECLTYPES)
    #     conn.row_factory = sqlite3.Row
    #     c = conn.cursor()
    #     c.execute("UPDATE users SET wallet = wallet - 1 WHERE wallet > 0 ")
    #     logging.info(f"DB: decrease all wallets -1 RQ")
    #     conn.commit()
    #
    # def add_story(self, user_name, event, text):
    #     """
    #     Add story to the Database
    #
    #     id INTEGER PRIMARY KEY  AUTO_INCREMENT, - auto generated
    #     date TIMESTAMP,         - current time
    #     user_id INTEGER         - who add
    #     event VARCHAR(10),      - kind of event: [add, info, pred]
    #     text TEXT               - text of message
    #     """
    #     conn = sqlite3.connect(self.name, detect_types=sqlite3.PARSE_DECLTYPES)
    #     conn.row_factory = sqlite3.Row
    #     c = conn.cursor()
    #     values = (time.time(),
    #               user_name,
    #               event,
    #               text)
    #     c.execute('INSERT INTO story VALUES (?, ?, ?, ?)', values)
    #     conn.commit()
    #     logging.info(f"DB: save story {event}")
    #
    # def add_coins(self, user_name, value: int):
    #     """
    #     Add coins to user
    #     format of command in message "/add user_name 100"
    #     :param user_name:   - it can be user name or user id
    #     :param value:       - value coins for add
    #     :return:    True - OK
    #                 False - didn't find user
    #     """
    #     user_data = self.get_user(user_id_or_name=user_name)
    #     if user_data:
    #         user_data["wallet"] = user_data["wallet"] + int(value)
    #         self.update_user(user_data)
    #         logging.info(f"DB: ADD COINS added {value}RQ to user: {user_name}")
    #         return True
    #     else:
    #         logging.info(f"DB: ADD COINS didn't find user: {user_name}")
    #         return False
    #     pass
    #
    # def db_request(self, request):
    #     conn = sqlite3.connect(self.name, detect_types=sqlite3.PARSE_DECLTYPES)
    #     conn.row_factory = sqlite3.Row
    #     c = conn.cursor()
    #     # Create tables
    #     c.execute(request)
    #     conn.commit()
    #     pass
    #
    # def mark_as_stopped(self, user_id_list):
    #     """
    #     Set value in column stopped in 1 if user in list
    #
    #     :param user_id_list: list if users for marking
    #     :return:
    #     """
    #     why = ''
    #     for user in user_id_list:
    #         why = "user_id == " + str(user) + " OR "
    #     why = why[:-4]
    #     print(why)
    #     conn = sqlite3.connect(self.name, detect_types=sqlite3.PARSE_DECLTYPES)
    #     conn.row_factory = sqlite3.Row
    #     c = conn.cursor()
    #     c.execute("UPDATE users SET stopped = 1 WHERE " + why)
    #     logging.info(f"DB: mark {len(user_id_list)} user(s) as stopped")
    #     conn.commit()
