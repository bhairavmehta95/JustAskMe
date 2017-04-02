from flask import *
import MySQLdb

app = Flask(__name__)
db = MySQLdb.connect(host="localhost", user="root", passwd="12345", db="ahhh_data")
cursor = db.cursor()
db.autocommit(True)

def remove_row(unique_id):
    cursor.execute("DELETE FROM questions WHERE QuestionID="+str(unique_id));

def add_row(admin_id,string,namespace):
    cursor.execute("""INSERT INTO questions (admin_id,string,upvotes,posted_time,namespace,answered)
                       VALUE (%s,%s,1,NOW(),%s,0)""", (str(admin_id),string,namespace))

def get_rows(namespace_value):
    cursor.execute("SELECT * FROM questions WHERE namespace='"+namespace_value+"'")
    return cursor.fetchall()

def get_rows_sorted_top(namespace_value):
    cursor.execute("SELECT * FROM questions WHERE namespace='"+namespace_value+"' ORDER BY upvotes")
    return cursor.fetchall()

def get_rows_sorted_new(namespace_value):
    cursor.execute("SELECT * FROM questions WHERE namespace='"+namespace_value+"' ORDER BY posted_time")
    return cursor.fetchall()

def count_namespace(namespace_value):
    cursor_data.execute("SELECT COUNT(*) FROM questions WHERE namespace='"+namespace_value+"'")
    return cursor_data.fetchall()

def increment_upvotes_by_one(unique_id):
    cursor.execute("SELECT upvotes FROM questions WHERE QuestionID="+str(unique_id))
    upvotes_value = cursor.fetchone()
    upvotes_value = upvotes_value[0]+1
    cursor.execute("UPDATE questions SET upvotes="+str(upvotes_value)+" WHERE QuestionID="+str(unique_id))

def show_rows(data):
    print_string = ""
    for row in data:
        print_string = print_string+"admin_id = "+str(row[1])+"\n"
        print_string = print_string+"string = "+str(row[2])+"\n"
        print_string = print_string+"upvotes = "+str(row[3])+"\n"
        print_string = print_string+"posted_time = "+str(row[4])+"\n"
        print_string = print_string+"namespace = "+str(row[5])+"\n"
        print_string = print_string+"answered = "+str(row[6])+"\n"
        print_string = print_string+"---------------\n"
    print(print_string)

@app.route("/")
def entry_action():
    add_row(1000,"added stupid question number 333333!","cs102")
    increment_upvotes_by_one(26)
    increment_upvotes_by_one(26)
    increment_upvotes_by_one(26)
    increment_upvotes_by_one(26)
    increment_upvotes_by_one(26)
    data = get_rows("cs102")
    show_rows(data)
    return ""


if __name__ == "__main__":
    app.run()
