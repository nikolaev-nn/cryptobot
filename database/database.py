import sqlite3
import asyncio


class DataBase:
    def __init__(self, path='database/bot.sqlite'):
        self.con = sqlite3.connect(path, check_same_thread=False)
        self.con.execute('''CREATE TABLE if not exists users (
                                id int primary key unique, 
                                username varchar(100), 
                                first_name varchar(100)
                            );''')
        self.con.execute('''CREATE TABLE if not exists coins (
                                id integer primary key AUTOINCREMENT default 0,
                                coin_name varchar(30),
                                coin_ticker varchar(30),
                                price decimal(38,16),
                                last_price decimal(38,16),
                                user_id int,
                                foreign key (id) references users(id)
                            );''')
        self.con.commit()

    async def select_items(self):
        print(list(self.con.execute('select * from users')))
        print(list(self.con.execute('select * from coins')))

    async def create_request(self, request):
        print(list(self.con.execute(request)))
        self.con.commit()

    async def add_user(self, user_info):
        self.con.execute("INSERT or IGNORE INTO users(id, username, first_name) VALUES (?, ?, ?);", tuple(user_info))
        self.con.commit()

    async def save_alert(self, alert_info):
        self.con.execute("INSERT INTO coins(coin_name, coin_ticker, price, last_price, user_id) VALUES (?, ?, ?, ?, ?);", tuple(alert_info.values()))
        self.con.commit()

    async def get_alert(self, user_id):
        return list(self.con.execute(f"select coin_name, coin_ticker, price, last_price from coins where user_id={user_id};"))

    async def delete_alert(self, alert_info):
        self.con.execute("delete from coins where (user_id = ? and coin_name = ? and price = ?);", tuple(alert_info))
        self.con.commit()

    async def show_alerts(self, user_id):
        return list(self.con.execute(f"select coin_name, price from coins where user_id={user_id};"))

    async def get_users_id(self):
        return list(self.con.execute(f"select id from users;"))

    async def drop_tables(self):
        self.con.execute(""" drop table coins; """)
        self.con.commit()
        # self.con.execute(""" drop table users;""")


if __name__ == '__main__':
    db = DataBase(path='bot.sqlite')
    asyncio.run(db.drop_tables())
