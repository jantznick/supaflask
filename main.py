import os
from flask import Flask, request, jsonify, render_template, redirect
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

app = Flask(__name__, template_folder='./')

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/supabase/login', methods=['POST'])
def supabase_login():
    email = request.form.get('email')
    password = request.form.get('password')
    supabase.auth.sign_in_with_password({'email': email, "password": password})
    return redirect("/user_profile")

@app.route('/user_profile', methods=['GET'])
def user_profile():
    supabase_user = supabase.auth.get_user()
    print('supabase user:')
    print(supabase_user)
    return 'hello'

if __name__ == '__main__':
    app.run(debug=True)
