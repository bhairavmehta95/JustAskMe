import os
import random, string
from flask import redirect, url_for

def gen_passcode():
    return ''.join(random.choice(string.ascii_lowercase) for i in range(5))

def check_namespace(namespace_value):
    cursor_data.execute("SELECT EXISTS(SELECT 1 FROM questions WHERE namespace='"+namespace_value+"')")
    return cursor_data.fetchall()

@app.route('/')
def clickStart():
    data = check_namespace(###get namespace from textbox###)
    if (!data):
      passw = gen_passcode()
      session[###get namespace from textbox###] = passw);
      return redirect(url_for(###get namespace from textbox###), code=307)
    elif:
      # Alert user that namespace already exists- might be a JS/HTML thing in future
      return "Err: Namespace already exists"
def clickJoin():
    data = check_namespace(###get namespace from textbox###)
    if (!data):
      #Alert user that no such namespace exists- JS/HTML in future
      return "Err: No namespace exists"
    elif:
      return redirect(url_for(###get namespace from textbox###), code=307)



       
