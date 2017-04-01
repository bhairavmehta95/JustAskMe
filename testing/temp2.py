import os
import random, string
from flask import redirect, url_for

def gen_passcode():
    return ''.join(random.choice(string.ascii_lowercase) for i in range(5))

def check_namespace(namespace_value):
    cursor_data.execute("SELECT EXISTS(SELECT 1 FROM questions WHERE namespace='"+namespace_value+"')")
    return cursor_data.fetchall()

@app.route('/')
def clickGo():
    data = check_namespace("###get namespace from textbox###")
    if (data == NULL):
      #Alert user that no such namespace exists, creating new one- JS/HTML in future
      passw = gen_passcode()
      session["###get namespace from textbox###"] = passw
    else:
      # Alert user that they are joining an existing page- might be a JS/HTML thing in future 
      pass	# until code is written     
    return redirect(url_for("###get namespace from textbox###"), code=307)




       
