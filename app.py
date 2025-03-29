from flask import Flask, render_template, request, redirect, jsonify, url_for, session
from supabase import create_client
import os
from dotenv import load_dotenv
import random
import time
import requests

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "default-secret-key")
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)
RECAPTCHA_SITE_KEY = os.getenv("RECAPTCHA_SITE_KEY")
RECAPTCHA_SECRET_KEY = os.getenv("RECAPTCHA_SECRET_KEY")
RECAPTCHA_VERIFY_URL = "https://www.google.com/recaptcha/api/siteverify"

def get_random_nick():
    return random.choice(['Anonymous', 'Guest', 'print("0")'])

def verify_recaptcha(token):
    if not token:
        return False
    data = {
        'secret': RECAPTCHA_SECRET_KEY,
        'response': token
    }
    try:
        response = requests.post(RECAPTCHA_VERIFY_URL, data=data, timeout=5)
        return response.json().get('success', False)
    except:
        return False

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        recaptcha_token = request.form.get('g-recaptcha-response')
        if not verify_recaptcha(recaptcha_token):
            return jsonify(error="Captcha verification failed"), 400

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
        messages=messages,
        recaptcha_site_key=RECAPTCHA_SITE_KEY
    )

@app.route('/about')
def about():
    return render_template('about.html', active_page='about')

@app.route('/get_messages')
def get_messages():
    messages = supabase.table('messages') \
        .select('*') \
        .order('created_at', desc=False) \
        .execute() \
        .data
    return jsonify(messages=messages)

@app.route('/message/<message_id>')
def message_detail(message_id):
    return redirect(url_for('index', _anchor=f'message-{message_id}'))

if __name__ == '__main__':
    app.run(debug=True)
