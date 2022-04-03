import os
import sqlite3

# From: https://goo.gl/YzypOI
def singleton(cls):
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return getinstance

class DatabaseDriver(object):
    """
    Database driver for the Task app.
    Handles with reading and writing data with the database.
    """

    def __init__(self):
        '''
            Establish connection, create cursor for execution and create users table
        '''
        self.conn = sqlite3.connect("users", check_same_thread= False)
        self.cursor = self.conn.cursor()
        self.create_users_table()

    def create_users_table(self):
        '''
            Create users table
        '''
        try:
            self.cursor.execute(
                '''
                    CREATE TABLE users(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        username TEXT NOT NULL,
                        balance DOUBLE
                    );
                '''
            )
        except Exception as e:
            return e
    
    
    def get_users(self):
        '''
            Queries and returns all users
        '''

        result = []
        data = self.cursor.execute(
                '''
                    SELECT id, name, username FROM users;
                ''')
        

        # Parse the data
        for row in data:
            temp = {"id": row[0], "name": row[1], "username": row[2]}
            result.append(temp)

        return result


    def create_user(self, name, username, balance):
        '''
            Creates and returns a new user with <name>, <username> and <balance>
        '''

        self.cursor.execute(
            '''
                INSERT INTO users(name, username, balance) VALUES(?, ?, ?);
            '''
            , (name, username, balance))

        self.conn.commit()
        return self.get_user(self.cursor.lastrowid)
    

    def get_user(self, user_id):
        '''
            Returns user with id <user_id>
        '''
        data = self.cursor.execute(
                '''
                    SELECT * FROM users WHERE ID = ?;
                '''
                , (user_id,))

        for row in data:
            return {"id": row[0], "name": row[1], "username": row[2], "balance": row[3]}

    def delete_user(self, user_id):
        '''
            Deletes and returns user with id <user_id>
        '''

        data = self.get_user(user_id)
        self.cursor.execute(
                '''
                    DELETE FROM users WHERE id = ?
                '''
                , (user_id,))
        
        self.conn.commit()
        return data

    def send(self, sender_id, receiver_id, amount):
        '''
            Sends <amount> from user with id <sender_id> to user with id <receiver_id>
        '''

        sender = self.get_user(sender_id)
        receiver = self.get_user(receiver_id)

        if sender and receiver:
            if sender["balance"] >= amount:
                self.cursor.execute(
                    '''
                        UPDATE users SET balance = ? WHERE id = ?;
                    '''
                , (sender["balance"]-amount, sender_id))
                
                self.cursor.execute(
                    '''
                        UPDATE users SET balance = ? WHERE id = ?;
                    '''
                , (receiver["balance"]+amount, receiver_id))
                
                self.conn.commit()
                return True

            return ("Insufficient funds for transfer")
        return ("Both sender and receiver should be valid users")



    def delete_all(self):
        '''
            Deletes all users. Returns []
        '''

        self.cursor.execute(
            '''
                DELETE FROM users;
            '''
        )
        self.conn.commit()

        return self.get_users()






    
