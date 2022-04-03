from ast import excepthandler
import os
import sqlite3
from xmlrpc.client import boolean

from matplotlib import use

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
        self.create_transactions_table()

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
        res = {}
        data = self.cursor.execute(
                '''
                    SELECT * FROM users WHERE ID = ?;
                '''
                , (user_id,))

        for row in data:
            res = {"id": row[0], "name": row[1], "username": row[2], "balance": row[3]}

        if res:
            res["transactions"] = self.get_user_transaction(user_id)
        return res

    
    def delete_user(self, user_id):
        '''
            Deletes and returns user with id <user_id>
        '''

        data = self.get_user(user_id)
        print(data)
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

            return ({"error": "Insufficient funds for transfer", "code": 403})
        return ({"error": "Both sender and receiver should be valid users", "code": 400})


    def delete_all_users(self):
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

    
    def create_transactions_table(self):
        '''
            Create a transactions table
        '''

        try:
            self.cursor.execute(
                '''
                    CREATE TABLE transactions(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        sender_id INTEGER SECONDARY KEY NOT NULL,
                        receiver_id INTEGER SECONDARY KEY NOT NULL,
                        amount INTEGER NOT NULL,
                        message TEXT NOT NULL,
                        accepted BOOLEAN
                    );
                '''
            )
        except Exception as e:
            return e

    def get_transactions(self):
        '''
            Queries and returns all transactions
        '''
        result = []
        data = self.cursor.execute(
                '''
                    SELECT id, sender_id, receiver_id, amount, accepted FROM transactions;
                ''')
        
        # Parse the data
        for row in data:
            temp = {"id": row[0], "sender_id": row[1], "receiver_id": row[2], "amount": row[3], "accepted": row[4]}
            result.append(temp)

        return result

    def get_transaction(self, txn_id):
        '''
            Get a particular transaction with id <txn_id>
        '''
        user_transactions = self.cursor.execute(
                '''
                    SELECT * FROM transactions WHERE id = ?;
                '''
                , (txn_id,))

        res = [{"id": txn[0], 
                "sender_id": txn[1],
                "receiver_id": txn[2], 
                "amount": txn[3],
                "message": txn[4],
                "accepted": txn[5]} for txn in user_transactions]
        
        return res[0]

    def get_user_transaction(self, user_id):
        '''
            Get the transaction of a user with id <user_id>
        '''

        user_transactions = self.cursor.execute(
                '''
                    SELECT * FROM transactions WHERE sender_id = ? OR receiver_id = ?;
                '''
                , (user_id, user_id))

        res = [{"id": txn[0], 
                "sender_id": txn[1],
                "receiver_id": txn[2], 
                "amount": txn[3],
                "accepted": txn[5]} for txn in user_transactions]
        
        return res

    def exec_transactions(self, sender_id, receiver_id, amount, message, accepted):
        '''
            Execute a transaction from user with <sender_id> to user with id <receiver_id>
        '''
        self.cursor.execute(
            '''
                INSERT INTO transactions(sender_id, receiver_id, amount, message, accepted) VALUES(?, ?, ?, ?, ?);
            '''
            , (sender_id, receiver_id, amount, message, accepted))

        self.conn.commit()
        
        if accepted:
            res = self.send(sender_id, receiver_id, amount)
            if res != True:
                return res
        
        return self.get_transaction(self.cursor.lastrowid)
        
    def update_transaction(self, accepted, txn_id):
        '''
            Update the accepted field of a transaction, if possible
        '''
        self.cursor.execute(
            '''
                UPDATE transactions SET accepted= ? WHERE id= ?
            '''
        , (accepted, txn_id))

        txn = self.get_transaction(txn_id)

        if type(txn["accepted"]) == boolean:
            return {"error": "Transaction accepted field cannot be changed", "code": 403}

        if accepted:
            res = self.send(txn["sender_id"], txn["receiver_id"], txn["amount"])

            if res != True:
                return res
            return txn


    def delete_all_transactions(self):
        '''
            Deletes all users. Returns []
        '''

        self.cursor.execute(
            '''
                DELETE FROM transactions;
            '''
        )
        self.conn.commit()
        return self.get_transactions()
    

    def drop_transactions(self):
        '''
            Drop transactions table
        '''
        self.cursor.execute(
            '''
                 DROP TABLE transactions;
            '''
        )
        self.conn.commit()


       

    
    





    
