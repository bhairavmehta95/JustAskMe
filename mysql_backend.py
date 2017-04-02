from flask import *
import MySQLdb

db = MySQLdb.connect(host="ahhh-db.cq2tyrgbq4kh.us-west-2.rds.amazonaws.com", port=3306, user="ahhh", passwd="password", db="ahhh_db")
cursor = db.cursor()
db.autocommit(True)


def add_admin(admin_number,namespace):
    cursor.execute("""INSERT INTO admins (admin_number,namespace)
                       VALUE (%s,%s)""", (admin_number,namespace))

def get_admin_number(namespace):
    cursor.execute("SELECT * FROM admins WHERE namespace='"+namespace)

def remove_admin(admin_number):
    cursor.execute("DELETE FROM admins WHERE admin_number="+str(admin_number))

def remove_question(unique_id):
    cursor.execute("DELETE FROM questions WHERE QuestionID="+str(unique_id))

def add_question(string,namespace):
    cursor.execute("""INSERT INTO questions (string,upvotes,posted_time,namespace,answered)
                       VALUE (%s,1,NOW(),%s,0)""", (string,namespace))

def get_questions_sorted_top_unanswered(namespace_value):
    cursor.execute("SELECT * FROM questions WHERE namespace='"+namespace_value+"'AND answered=0 ORDER BY upvotes")
    return cursor.fetchall()

def get_questions_sorted_new_unanswered(namespace_value):
    cursor.execute("SELECT * FROM questions WHERE namespace='"+namespace_value+"'AND answered=0 ORDER BY posted_time")
    return cursor.fetchall()

def get_questions_sorted_answered(namespace_value):
    cursor.execute("SELECT * FROM questions WHERE namespace='"+namespace_value+"' AND answered=1")
    return cursor.fetchall()

def increment_upvotes_by_one(unique_id):
    cursor.execute("SELECT upvotes FROM questions WHERE QuestionID="+str(unique_id))
    upvotes_value = cursor.fetchone()
    upvotes_value = upvotes_value[0]+1
    cursor.execute("UPDATE questions SET upvotes="+str(upvotes_value)+" WHERE QuestionID="+str(unique_id))

def run_updates():
    execution_str = 'DROP TABLE IF EXISTS questions'
    cursor.execute(execution_str)
    
    execution_str = 'DROP TABLE IF EXISTS admins'
    cursor.execute(execution_str)

    execution_str = 'CREATE TABLE questions( QuestionID INT NOT NULL AUTO_INCREMENT PRIMARY KEY, string VARCHAR(2000) NOT NULL, upvotes INT NOT NULL, posted_time TIMESTAMP, namespace VARCHAR(200) NOT NULL, answered TINYINT(1) );'

    cursor.execute(execution_str)

    execution_str = 'CREATE TABLE admins(ID INT NOT NULL AUTO_INCREMENT '\
    'PRIMARY KEY, admin_number INT UNSIGNED NOT NULL, namespace VARCHAR(200) NOT NULL);'

    cursor.execute(execution_str)


if __name__ == '__main__':
    run_updates()