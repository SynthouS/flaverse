from flask import Flask, render_template, request, redirect, jsonify, url_for, session
from supabase import create_client
import os
from dotenv import load_dotenv
import random
import time

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "default-secret-key")
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

def get_random_nick():
    return random.choice(['Anonymous', 'Guest', 'print("0")'])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Проверка времени между запросами
        last_submit = session.get('last_submit', 0)
        if time.time() - last_submit < 10:
            return jsonify(error="Please wait 10 seconds between messages"), 429

        nickname = request.form.get('nickname', '').strip()[:25]
        message = request.form.get('message', '').strip()[:150]

        if not nickname:
            nickname = get_random_nick()

        if message:
            try:
                supabase.table('messages').insert({
                    'nickname': nickname,
                    'message': message
                }).execute()
                session['last_submit'] = time.time()
                return redirect(url_for('index'))
            except Exception as e:
                return jsonify(error=str(e)), 500

    messages = supabase.table('messages') \
        .select('*') \
        .order('created_at', desc=True) \
        .execute() \
        .data

    return render_template(
        'index.html', 
        active_page='home',
        messages=messages
    )

@app.route('/about')
def about():
    return render_template('about.html', active_page='about')

@app.route('/get_messages')
def get_messages():
    messages = supabase.table('messages') \
        .select('*') \
        .order('created_at', desc=True) \
        .execute() \
        .data
    return jsonify(messages=messages)

@app.route('/message/<message_id>')
def message_detail(message_id):
    return redirect(url_for('index', _anchor=f'message-{message_id}'))

if __name__ == '__main__':
    app.run(debug=True)
