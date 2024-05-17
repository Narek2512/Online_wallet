from db import cursor, connection

def add_user(user_name, user_surname, user_email, user_password, balance, country, symbol, value):
    try:
        sql = "INSERT INTO `users` (`user_name`,`user_surname`,`user_email`,`user_password`,`balance`, `country`, `symbol`, `value`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, (user_name, user_surname, user_email, user_password, balance, country, symbol, value))
        connection.commit()
        return True
    except:
        return False

def delete_user(id):
    try:
        sql = "DELETE FROM `users` WHERE id = %s"
        cursor.execute(sql, id)
        connection.commit()
        return True
    except:
        return False


def update_password(id, user_password):
    try:
        sql = "UPDATE `users` SET user_password = %s WHERE id = %s"
        cursor.execute(sql, id, user_password)
        connection.commit()
        return True
    except:
        return False

def update_balance(id, balance):
    try:
        sql = "UPDATE `users` SET balance = %s WHERE id = %s"
        cursor.execute(sql, (balance, id))
        connection.commit()
        return True
    except:
        return False


def get_user():
    try:
        sql = "SELECT * FROM `users`"
        cursor.execute(sql)
        connection.commit()

        data = cursor.fetchall()
        return data
    except:
        return False

def get_user_by_id(id):
    try:
        sql = "SELECT * FROM `users` WHERE id = %s"
        cursor.execute(sql, id)
        connection.commit()

        data = cursor.fetchone()
        return data
    except:
        return False



def update_symbol(id, symbol):
    try:
        sql = "UPDATE `users` SET symbol = %s WHERE id = %s"
        cursor.execute(id, symbol)
        connection.commit()
        return True

    except:
        return False


def update_value(id, value):
    try:
        sql = "UPDATE `users` SET value = %s WHERE id = %s"
        cursor.execute(id, value)
        connection.commit()
        return True

    except:
        return False