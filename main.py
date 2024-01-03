import os
from flask import Flask, request, jsonify, render_template, redirect
from dotenv import load_dotenv
from supabase import create_client, Client
from functools import wraps

load_dotenv()

app = Flask(__name__, template_folder='./')

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def get_user_data(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        jwt = request.cookies.get('auth') or ''
        if not jwt:
            return redirect('/login')
        try:
            supabase_user = supabase.auth.get_user(jwt)
        except Exception as e:
            print(f"Exception: {e}")
        return f(supabase_user.user, *args, **kwargs)
    return decorated_function

def get_extra_user_data(id):
    response = supabase.table('users').select("*").eq('id', id).execute()
    return response

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/supabase/login', methods=['POST'])
def supabase_login():
    email = request.form.get('email')
    password = request.form.get('password')
    user = supabase.auth.sign_in_with_password({'email': email, "password": password})
    response = redirect("/user_profile")
    response.set_cookie('auth', user.session.access_token)
    supabase.auth.sign_out()
    return response

@app.route('/supabase/logout', methods=['POST'])
def supabase_logout():
    response = redirect("/login")
    response.set_cookie('auth', expires=0)
    supabase.auth.sign_out()
    return response

@app.route('/user_profile', methods=['GET'])
@get_user_data
def user_profile(supabase_user):
    print(supabase_user.id)
    print(get_extra_user_data(supabase_user.id))
    return render_template('user_profile.html', email=supabase_user.email, metadata=supabase_user.user_metadata)

if __name__ == '__main__':
    app.run(debug=True)
