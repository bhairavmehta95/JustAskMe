from flask import Flask, request

app = Flask(__name__)
app.debug = True

@app.route('/', methods=['GET', 'POST'])
def main():
    return "Hello!"


if __name__ == '__main__':
    app.run(host='0.0.0.0')