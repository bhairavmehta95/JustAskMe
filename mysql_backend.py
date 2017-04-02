from flask import *
import MySQLdb

# NB: in the following commands, "namespace" reference to the unique identifier
# justaskk.me/<UNIQUE_IDENTIFIER> which hosts a question bank
# TODO encyrpt the namespace! So that outsiders cannot look at your question bank

db_data       = MySQLdb.connect(host="localhost", user="root", passwd="root", db="ahhh_data")
db_admins     = MySQLdb.connect(host="localhost", user="root", passwd="root", db="ahhh_admins")
cursor_data   = db_data.cursor()
cursor_admins = db_admins.cursor()
db_data.autocommit(True)
db_admins.autocommit(True)

# Add an admin passcode to namespace relationship to the admins table
def add_admin(admin_number,namespace):
    cursor_admins.execute("""INSERT INTO admins (admin_number,namespace)
                       VALUE (%s,%s)""", (admin_number,namespace))

# Get the admin passcode corresponding to the namespace
# TODO encryption! This is not safe...
def get_admin_number(namespace):
    cursor_admins.execute("SELECT * FROM admins WHERE namespace='"+namespace)

# Remove admin passcode from namespace
def remove_admin(admin_number):
    cursor_admins.execute("DELETE FROM admins WHERE admin_number="+str(admin_number))

# Remove a question from database based on its unique ID
def remove_question(unique_id):
    cursor_data.execute("DELETE FROM questions WHERE QuestionID="+str(unique_id))

# Add question to database corresponding to the namespace
def add_question(string,namespace):
    cursor_data.execute("""INSERT INTO questions (string,upvotes,posted_time,namespace,answered)
                       VALUE (%s,1,NOW(),%s,0)""", (string,namespace))

# Sort unanswered questions by their number of upvotes
def get_questions_sorted_top_unanswered(namespace_value):
    cursor_data.execute("SELECT * FROM questions WHERE namespace='"+namespace_value+"'AND answered=0 ORDER BY upvotes")
    return cursor_data.fetchall()

# Sort unanswered questions with newest first
def get_questions_sorted_new_unanswered(namespace_value):
    cursor_data.execute("SELECT * FROM questions WHERE namespace='"+namespace_value+"'AND answered=0 ORDER BY posted_time")
    return cursor_data.fetchall()

# Get the answered questions, ordered chronologically
def get_questions_sorted_answered(namespace_value):
    cursor_data.execute("SELECT * FROM questions WHERE namespace='"+namespace_value+"' AND answered=1 ORDER BY posted_time")
    return cursor_data.fetchall()

# Increase by one the number of upvotes of question corresopnding to unique ID
def increment_upvotes_by_one(unique_id):
    cursor_data.execute("SELECT upvotes FROM questions WHERE QuestionID="+str(unique_id))
    upvotes_value = cursor_data.fetchone()
    upvotes_value = upvotes_value[0]+1
    cursor_data.execute("UPDATE questions SET upvotes="+str(upvotes_value)+" WHERE QuestionID="+str(unique_id))
