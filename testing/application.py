from flask import *

app = Flask(__name__)
app.debug = True
SESSION_TYPE = 'redis'
app.config.from_object(__name__)

@app.route('/set/')
def set():
    session['namespace1'] = 'qwert'
    return 'ok'

@app.route('/get/')
def get(namespace):
    return session.get(namespace, 'not set')

@app.route('/', methods=['GET', 'POST'])
def main():
    session['namespace1'] = 'qwert'
    print("hello")
    return ""

if __name__ == '__main__':
    app.secret_key = 'eudah4328ueg7Tuhd2du'
    app.run(host='0.0.0.0')
