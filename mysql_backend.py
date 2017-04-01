from flask import *
import MySQLdb

app = Flask(__name__)
db_data = MySQLdb.connect(host="localhost", user="root", passwd="12345", db="ahhh_data")
db_admins = MySQLdb.connect(host="localhost", user="root", passwd="12345", db="ahhh_admins")
cursor_data = db_data.cursor()
cursor_admins = db_admins.cursor()
db_data.autocommit(True)
db_admins.autocommit(True)

def register_admin(admin_number,namespace):
    cursor_admins.execute("""INSERT INTO admins (admin_number,namespace)
                       VALUE (%s,%s)""", (admin_number,namespace))

def remove_question(unique_id):
    cursor_data.execute("DELETE FROM questions WHERE QuestionID="+str(unique_id))

def add_question(string,namespace):
    cursor_data.execute("""INSERT INTO questions (string,upvotes,posted_time,namespace,answered)
                       VALUE (%s,1,NOW(),%s,0)""", (string,namespace))

def get_questions_sorted_top(namespace_value):
    cursor_data.execute("SELECT * FROM questions WHERE namespace='"+namespace_value+"' ORDER BY upvotes")
    return cursor_data.fetchall()

def get_questions_sorted_new(namespace_value):
    cursor_data.execute("SELECT * FROM questions WHERE namespace='"+namespace_value+"' ORDER BY posted_time")
    return cursor_data.fetchall()

def get_questions_sorted_answered(namespace_value):
    cursor_data.execute("SELECT * FROM questions WHERE namespace='"+namespace_value+"' AND answered=1")
    return cursor_data.fetchall()

def increment_upvotes_by_one(unique_id):
    cursor_data.execute("SELECT upvotes FROM questions WHERE QuestionID="+str(unique_id))
    upvotes_value = cursor_data.fetchone()
    upvotes_value = upvotes_value[0]+1
    cursor_data.execute("UPDATE questions SET upvotes="+str(upvotes_value)+" WHERE QuestionID="+str(unique_id))

def show_questions(data):
    print_string = ""
    for row in data:
        print_string = print_string+"string = "      +str(row[1])+"\n"
        print_string = print_string+"upvotes = "     +str(row[2])+"\n"
        print_string = print_string+"posted_time = " +str(row[3])+"\n"
        print_string = print_string+"namespace = "   +str(row[4])+"\n"
        print_string = print_string+"answered = "    +str(row[5])+"\n"
        print_string = print_string+"---------------\n"
    print(print_string)

@app.route("/")
def entry_action():
    add_question("added stupid question number 333333!","cs102")
    register_admin(1212,"cs103")
    increment_upvotes_by_one(26)
    data = get_questions_sorted_answered("cs102")
    show_questions(data)
    return ""

if __name__ == "__main__":
    app.run()