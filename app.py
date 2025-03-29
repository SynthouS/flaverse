from flask import Flask, render_template, request, redirect, jsonify, url_for
from supabase import create_client
import os
from dotenv import load_dotenv
import random

load_dotenv()
app = Flask(__name__)
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

def get_random_nick():
    return random.choice(['Anonymous', 'Guest', 'print("0")'])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nickname = request.form.get('nickname', '').strip()[:25]
        message = request.form.get('message', '').strip()[:150]
        
        if not nickname:
            nickname = get_random_nick()
        
        if message:
            supabase.table('messages').insert({
                'nickname': nickname,
                'message': message
            }).execute()
            
        return redirect(url_for('index'))
    
    messages = supabase.table('messages') \
        .select('*') \
        .order('created_at', desc=True) \
        .execute() \
        .data
    
    return render_template('index.html', active_page='home', messages=messages)

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