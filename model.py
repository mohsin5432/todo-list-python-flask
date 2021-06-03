import sqlite3


def signup(email,username,password):
    connection = sqlite3.connect('login_data.db' , check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute(""" SELECT password FROM users WHERE username='{username}';""".format(username = username))
    exist = cursor.fetchone()
    if exist is None:
        cursor.execute("""INSERT INTO users(email,username,password,date)VALUES('{email}','{username}','{password}',(CURRENT_TIMESTAMP));""".format(email = email , password = password , username = username))
        connection.commit()
        cursor.close()
        connection.close()
    else:
        return False

    return True


def pass_check(username):
    connection = sqlite3.connect('login_data.db' , check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute(""" SELECT password FROM users WHERE username='{username}' ORDER BY pk DESC;""".format(username = username))
    passs = cursor.fetchone()
    password = passs and passs[0]
    connection.commit()
    cursor.close()
    connection.close()
    return password

def check_users():
    connection = sqlite3.connect('login_data.db' , check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute("""SELECT username from users ORDER BY pk DESC;""")
    db_users = cursor.fetchall()
    users = []
    for i in range(len(db_users)):
        person = db_users[i][0]
        users.append(person)

    connection.commit()
    cursor.close()
    connection.close()
    return users

def email(username):
    connection = sqlite3.connect('login_data.db' , check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute("""SELECT email
                    FROM users
                    WHERE  username = '{username}';""".format(username = username))
    mail = cursor.fetchone()
    if mail is None:
        connection.commit()
        cursor.close()
        connection.close()
        return False
    else:
        connection.commit()
        cursor.close()
        connection.close()
        return mail[0]





def addtask(username,email,subject,memo,status,date):
    connection = sqlite3.connect('tasks.db' , check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute("""INSERT INTO tasks(username,email,subject,memo,status,date)VALUES('{username}','{email}','{subject}','{memo}','{status}','{date}');""".format(username = username,email=email,subject=subject,memo=memo,status=status,date=date))
    connection.commit()
    cursor.close()
    connection.close()
    return 'you have successfully ADDED TASK'


def pendingtask(username):
    status = "pending"
    connection = sqlite3.connect('tasks.db' , check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute("""SELECT *
                    FROM tasks
                    WHERE  username = '{username}' AND status='{status}'
                    order by date;""".format(username = username,status=status))
    pendingtask = cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    return pendingtask


def progresstask(username):
    status = "progress"
    connection = sqlite3.connect('tasks.db' , check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute("""SELECT *
                    FROM tasks
                    WHERE  username = '{username}' AND status='{status}'
                    order by date;""".format(username = username,status=status))
    progresstask = cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    return progresstask

def completedtask(username):
    status = "completed"
    connection = sqlite3.connect('tasks.db' , check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute("""SELECT *
                    FROM tasks
                    WHERE  username = '{username}' AND status='{status}'
                    order by date;""".format(username = username,status=status))
    finishedtask = cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    return finishedtask


def start(id_data):
    pk=id_data
    status="progress"
    connection = sqlite3.connect('tasks.db' , check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute(""" UPDATE tasks SET status = '{status}'  WHERE pk = '{pk}';""".format(status=status,pk=pk))
    connection.commit()
    cursor.close()
    connection.close()
    return 'you have successfully deleted intro'

def completed(id_data):
    pk=id_data
    status="completed"
    connection = sqlite3.connect('tasks.db' , check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute(""" UPDATE tasks SET status = '{status}'  WHERE pk = '{pk}';""".format(status=status,pk=pk))
    connection.commit()
    cursor.close()
    connection.close()
    return 'you have successfully deleted intro'

def delete(id_data):
    pk = id_data
    connection = sqlite3.connect('tasks.db' , check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute(""" DELETE FROM tasks WHERE pk = '{pk}';""".format(pk=pk))
    connection.commit()
    cursor.close()
    connection.close()

def remainder():
    connection = sqlite3.connect('tasks.db' , check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute("""SELECT email
                    FROM tasks
                    WHERE  date <= datetime('now','+2 day');""")
    mails = cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    return mails

def news(email):
    connection = sqlite3.connect('news.db' , check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute(""" SELECT * FROM mails WHERE email='{email}';""".format(email = email))
    exist = cursor.fetchone()
    if exist is None:
        cursor.execute("""INSERT INTO mails(email,date)VALUES('{email}',(CURRENT_TIMESTAMP));""".format(email = email))
        connection.commit()
        cursor.close()
        connection.close()
    else:
        return False

    return True

def emails():
    connection = sqlite3.connect('news.db' , check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute("""SELECT *
                    FROM mails;""")
    mails = cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    return mails


def admpass_check(username):
    connection = sqlite3.connect('admin.db' , check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute(""" SELECT password FROM admin WHERE username='{username}' ORDER BY pk DESC;""".format(username = username))
    passs = cursor.fetchone()
    password = passs and passs[0]
    connection.commit()
    cursor.close()
    connection.close()
    return password
