from flask import *
import os

if not os.environ.get('db_host'):
    import config

    os.environ['db_host'] = config.DB_HOST
    os.environ['db_user'] = config.DB_USER
    os.environ['db_password'] = config.DB_PASS
    os.environ['db_name'] = config.DB_NAME
    os.environ['db_port'] = '3306'


import random, string
import re

from twilio.twiml.messaging_response import MessagingResponse
from socket_utility import *


@application.route('/index')
@application.route('/')
def default():
  return render_template('start_page.html')


@application.route('/<room>')
def room(room):
    if (request.method == 'POST'):
        if not json.loads(request.data).get('is_in_use'):
            new_passw = ''.join(random.choice(string.ascii_lowercase) for i in range(6))#gen rand letters
            session[room] = new_passw     # New cookie
            session['room'] = room
            add_admin(new_passw, room)     # Add a new admin to the admin table
        else:
            return redirect(room)
    return render_template('questions.html')

@application.route('/api/genAdminPw', methods=['POST'])
def gen_admin_pw():
    namespace = json.loads(request.data).get('namespace')
    namespace = re.sub(r'[\W_]+', '', namespace)

    if namespace_exists(namespace):
        url_new = '/' + namespace
        return json.dumps({
            'exists': True,
            'namespace': namespace
        })

    new_passw = ''.join(random.choice(string.ascii_lowercase) for i in range(6))
    return json.dumps({
        'password': new_passw,
        'namespace': namespace,
        'exists': False
    })


@application.route('/api/addRow', methods=['POST'])
def api_add_row():
    json_data = request.json
    namespace = json_data['namespace']
    question = json_data['question']

    add_question(question, namespace)

    return json.dumps({
        'status_code': 200
    })


@application.route('/api/getAnsweredChron', methods=['POST'])
def api_answered_chron():
    json_data = request.json
    namespace = json_data['namespace']

    get_questions_sorted_answered(namespace)

    return json.dumps({
        'status_code': 200
    })


@application.route('/api/verifyAdmin', methods=['POST'])
def api_verify_admin():
    namespace = json.loads(request.data).get('room')
    password = json.loads(request.data).get('password')
    namespace = re.sub(r'\W+', '', namespace)
    true_pw = get_admin_pass(namespace)
    print(true_pw)

    if password == true_pw:
        session[namespace] = password
        session['room'] = str(namespace)

        return json.dumps({
            'verified': True
        })
    else:
        return json.dumps({
            'verified': False
        })


@application.route('/api/addAdmin', methods=['POST'])
def api_add_admin():
    namespace = json.loads(request.data).get('namespace')
    admin_pass = json.loads(request.data).get('password')

    add_admin(admin_pass, namespace)

    return json.dumps({
        'status_code': 200
    })


@application.route('/api/getAnswered', methods=['POST'])
def api_get_answered_chron():
    json_data = request.json
    namespace = json_data['namespace']

    rows = get_questions_sorted_answered(namespace)
    unique_ids = []
    questions = []
    timestamps = []
    upvotes = []

    for val in rows:
        unique_ids.append(val[0])
        questions.append(val[1])
        upvotes.append(val[2])
        timestamps.append(val[3])

    return json.dumps({
        'unique_ids': unique_ids,
        'questions': questions,
        'timestamps': timestamps,
        'upvotes': upvotes
    })


@application.route('/api/getRowsChron', methods=['POST'])
def api_get_rows_chron():
    json_data = request.json
    namespace = json_data['namespace']

    rows = get_questions_sorted_new_unanswered(namespace)
    unique_ids = []
    questions = []
    timestamps = []
    upvotes = []

    for val in rows:
        unique_ids.append(val[0])
        questions.append(val[1])
        upvotes.append(val[2])
        timestamps.append(val[3])

    return json.dumps({
        'unique_ids': unique_ids,
        'questions': questions,
        'timestamps': timestamps,
        'upvotes': upvotes
    })


@application.route('/api/getRowsTop', methods=['POST'])
def api_get_rows_top():
    json_data = request.json
    namespace = json_data['namespace']

    rows = get_questions_sorted_top_unanswered(namespace)
    questions = []
    timestamps = []
    upvotes = []
    unique_ids = []

    for val in rows:
        unique_ids.append(val[0])
        questions.append(val[1])
        upvotes.append(val[2])
        timestamps.append(val[3])

    return json.dumps({
        'unique_ids': unique_ids,
        'questions': questions,
        'timestamps': timestamps,
        'upvotes': upvotes
    })


@application.route('/api/addUpvote', methods=['POST'])
def api_add_upvote():
    json_data = request.json
    unique_id = json_data['unique_id']
    add_upvote = json_data['add_upvote']

    increment_upvotes_by_one(unique_id, add_upvote)

    return json.dumps({

    })


@application.route('/api/answerQuestion', methods=['POST'])
def api_answer_question():
    json_data = request.json
    unique_id = json_data['unique_id']

    answer_question(unique_id)

    return json.dumps({

    })


@application.route('/api/deleteQuestion', methods=['POST'])
def api_delete_question():
    json_data = request.json
    unique_id = json_data['unique_id']

    delete_question(unique_id)

    return json.dumps({

    })


@application.route('/api/sortChron', methods=['POST'])
def sort_chronological():
    json_data = request.json
    namespace_value = request['namespace']
    order = get_questions_sorted_new_unanswered(namespace_value)
    return json.dumps({
        'questions': order['string'],
        'timestamps': order['posted_time'],
        'upvotes': order['upvotes']
    })


@application.route('/api/sortTop', methods=['POST'])
def sort_top():
    json_data = request.json
    namespace_value = request['namespace']
    order = get_questions_sorted_top_unanswered(namespace_value)
    return json.dumps({
        'questions': order['string'],
        'timestamps': order['posted_time'],
        'upvotes': order['upvotes']
    })

@application.route('/sms', methods=['GET', 'POST'])
def reply():
    question = request.form['Body']
    question = question.split()

    namespace = question[0].lower()
    question = ' '.join(question[1:])

    add_question(question, namespace)

    resp = MessagingResponse()
    resp.message("Your question has been sent to {}!".format(namespace))

    return str(resp)


if __name__ == '__main__':
    sio.run(application)