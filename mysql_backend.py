from flask import *
import MySQLdb


db = MySQLdb.connect(host="ahhh-db.cq2tyrgbq4kh.us-west-2.rds.amazonaws.com", port=3306, user="ahhh", passwd="password", db="ahhh_db")
cursor = db.cursor()
db.autocommit(True)

def add_admin(admin_pass,namespace):
    cursor.execute("""INSERT INTO admins (admin_pass,namespace)
                       VALUE (%s,%s)""", (admin_pass,namespace,))

def namespace_exists(namespace):
    nr = cursor.execute("SELECT * FROM admins WHERE namespace='{}'".format(namespace))
    return cursor.rowcount != 0

def get_admin_pass(namespace):
    cursor.execute("SELECT admin_pass FROM admins WHERE namespace='{}'".format(namespace))
    password = cursor.fetchone()
    return password[0]

# Remove admin passcode from namespace
def remove_admin(admin_pass):
    cursor.execute("DELETE FROM admins WHERE admin_pass="+str(admin_pass))

# Remove a question from database based on its unique ID
def remove_question(unique_id):
    cursor.execute("DELETE FROM questions WHERE QuestionID="+str(unique_id))

# Add question to database corresponding to the namespace
def add_question(string,namespace):
    cursor.execute("""INSERT INTO questions (string,upvotes,posted_time,namespace,answered)
                       VALUE (%s,1,NOW(),%s,0)""", (string,namespace))

# Sort unanswered questions by their number of upvotes
def get_questions_sorted_top_unanswered(namespace_value):
    cursor.execute("SELECT * FROM questions WHERE namespace='"+namespace_value+"'AND answered=0 ORDER BY upvotes DESC")
    return cursor.fetchall()

# Sort unanswered questions with newest first
def get_questions_sorted_new_unanswered(namespace_value):
    cursor.execute("SELECT * FROM questions WHERE namespace='"+namespace_value+"'AND answered=0 ORDER BY posted_time DESC")
    return cursor.fetchall()

# Get the answered questions, ordered chronologically
def get_questions_sorted_answered(namespace_value):
    cursor.execute("SELECT * FROM questions WHERE namespace='"+namespace_value+"' AND answered=1 ORDER BY posted_time DESC")
    return cursor.fetchall()

def answer_question(unique_id):
    cursor.execute("UPDATE questions SET answered=1 WHERE QuestionID="+str(unique_id))

def delete_question(unique_id):
    cursor.execute("DELETE FROM questions WHERE QuestionID=" + str(unique_id))

# Increase by one the number of upvotes of question corresopnding to unique ID
def increment_upvotes_by_one(unique_id, add_upvote):
    cursor.execute("SELECT upvotes FROM questions WHERE QuestionID="+str(unique_id))
    upvotes_value = cursor.fetchone()
    upvotes_val = add_upvote + upvotes_value[0]
    cursor.execute("UPDATE questions SET upvotes="+str(upvotes_val)+" WHERE QuestionID="+str(unique_id))

def run_updates():
    execution_str = 'DROP TABLE IF EXISTS questions'
    cursor.execute(execution_str)
    
    execution_str = 'DROP TABLE IF EXISTS admins'
    cursor.execute(execution_str)

    execution_str = 'CREATE TABLE questions( QuestionID INT NOT NULL AUTO_INCREMENT PRIMARY KEY, string VARCHAR(2000) NOT NULL, upvotes INT NOT NULL, posted_time TIMESTAMP, namespace VARCHAR(200) NOT NULL, answered TINYINT(1) );'

    cursor.execute(execution_str)

    execution_str = 'CREATE TABLE admins(ID INT NOT NULL AUTO_INCREMENT '\
    'PRIMARY KEY, admin_pass VARCHAR(6) NOT NULL, namespace VARCHAR(200) NOT NULL);'

    cursor.execute(execution_str)


if __name__ == '__main__':
    run_updates()