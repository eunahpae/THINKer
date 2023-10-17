# A very simple Flask Hello World app for you to get started with...

import requests
from flask import Flask, render_template, request, redirect, session, url_for,flash
from mysql import Mysql
import pymysql
from datetime import timedelta
from authlib.integrations.flask_client import OAuth
from functools import wraps
import os
import random
import string
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd

from passlib.hash import pbkdf2_sha256
import config

app = Flask(__name__)
app.secret_key = "eungok"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=15)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'

mysql = Mysql()

# OAuth Setup
oauth = OAuth(app)

# Naver OAuth
naver_client_id = config.naver_client_id
naver_client_secret = config.naver_client_secret
naver=oauth.register(
    name='naver',
    client_id = naver_client_id,
    client_secret = naver_client_secret,
    access_token_url = 'https://nid.naver.com/oauth2.0/token',
    access_token_params = None,
    authorize_url = 'https://nid.naver.com/oauth2.0/authorize',
    authorize_params = None,
    refresh_token_url = None,
    redirect_uri = 'http://thinkerin.pythonanywhere.com/callback',
    client_kwargs = {'scope': 'name email'})

# Google OAuth
google_client_id = config.google_client_id
google_client_secret = config.google_client_secret
google=oauth.register(
    name="google",
    client_id = google_client_id,
    client_secret = google_client_secret,
    access_token_url = "https://www.googleapis.com/oauth2/v4/token",
    access_token_params = None,
    authorize_url = "https://accounts.google.com/o/oauth2/v2/auth",
    authorize_params = None,
    api_base_url = "https://www.googleapis.com/oauth2/v3/",
    client_kwargs = {"scope": "openid email profile"},
    server_metadata_url = 'https://accounts.google.com/.well-known/openid-configuration')

# Kakao OAuth
kakao_client_id = config.kakao_client_id
kakao_client_secret = config.kakao_client_secret
kakao = oauth.register(
    name = 'kakao',
    client_id = kakao_client_id,
    client_secret = kakao_client_secret,
    access_token_url = 'https://kauth.kakao.com/oauth/token',
    access_token_params = None,
    authorize_url = 'https://kauth.kakao.com/oauth/authorize',
    authorize_params = None,
    refresh_token_url = None,
    redirect_uri = 'http://thinkerin.pythonanywhere.com/kakao-callback')

def is_loged_in(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if 'is_loged_in' in session:
            return func(*args, **kwargs)
        else:
            return redirect('/login')
    return wrap

def connect():
        return pymysql.connect(host=mysql.host, user=mysql.user, db=mysql.db, password=mysql.password, charset=mysql.charset)

# Generate a random verification code
def generate_verification_code():
    number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return number

# Send email verification link
def send_verification_email(email, number):
    db = connect()
    cursor = db.cursor()
    sql='SELECT * FROM user WHERE email = %s'
    cursor.execute(sql, [email])
    users = cursor.fetchone()
    print(users)
    if users==None:
        sql = '''
            INSERT INTO user (email, code )
            VALUES (%s ,%s )
        '''
        verification_code = pbkdf2_sha256.hash(number)
        print(number)
        cursor.execute(sql,(email, verification_code))
        db.commit()
        from_email = 'eunahp86@gmail.com'
        password = 'trwcpqrofghewkxy'
        subject = 'Email Verification'

        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = email
        msg['Subject'] = subject

        verification_link = f'https://thinkerin.pythonanywhere.com/verify?email={email}&code={number}'
        message = f"Hello,\n\nPlease click the following link to verify your email:\n\n{verification_link}\n\nBest regards,\nYour Website Team"

        msg.attach(MIMEText(message, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, email, msg.as_string())
            server.quit()
            print('Email sent successfully!')
        except Exception as e:
            print(f'Error sending email: {e}')
    else:
        sql = '''
            UPDATE user SET code = %s WHERE email = %s
        '''
        verification_code = pbkdf2_sha256.hash(number)
        # print(f"fewfwe: {verification_code}")
        cursor.execute(sql,( verification_code, email))
        db.commit()
        from_email = 'eunahp86@gmail.com'
        password = 'trwcpqrofghewkxy'
        subject = 'Email Verification'

        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = email
        msg['Subject'] = subject

        verification_link = f'https://thinkerin.pythonanywhere.com/verify?email={email}&code={number}'
        message = f"Hello,\n\nPlease click the following link to verify your email:\n\n{verification_link}\n\nBest regards,\nYour Website Team"

        msg.attach(MIMEText(message, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, email, msg.as_string())
            server.quit()
            print('Email sent successfully!')
        except Exception as e:
            print(f'Error sending email: {e}')
        return 'Sent'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/intro', methods=['GET', 'POST'])
def intro():
    if request.method =="GET":
        return render_template('intro.html')


@app.route('/email', methods=['GET', 'POST'])
def email():
    if request.method == 'POST':
        email = request.form.get('email')
        db = connect()
        curs = db.cursor()

        sql = f'SELECT * FROM user WHERE email = %s;'
        curs.execute(sql , email)
        rows = curs.fetchone()
        if rows:
            if rows[6] == '1':
                return render_template('login.html')
            else:
                return render_template('register.html',email=email)
        else:
            return render_template('register.html',email=email)
    else:
        return render_template('email.html')

@app.route('/emailcheck', methods=['GET', 'POST'])
def emailcheck():
    email=request.form.get('email')
    return render_template('emailcheck.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        number = generate_verification_code()
        send_verification_email(email, number)
        password = mysql.hashing_password(password)
        print(password)
        db = connect()
        curs = db.cursor()
        sql = f'UPDATE user SET username =%s, phone=%s,password=%s WHERE email = %s;'
        curs.execute(sql , (username,phone,password,email))
        db.commit()
        db.close()
        return render_template('emailcheck.html', email=email)

    elif request.method == "GET":
        return redirect('/email')


# Verification route
@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'GET':
        email = request.args.get('email')
        code = request.args.get('code')
        db=connect()
        cursor = db.cursor()
        sql='SELECT * FROM user WHERE email = %s'
        cursor.execute(sql, [email])
        users = cursor.fetchone()
        print(users)
        if users == None:
            flash('Email not registered.')
            return "fail"
        else:
            if pbkdf2_sha256.verify(code, users[5]):
                flash('Email verified successfully.')
                sql = '''
                UPDATE user SET auth = %s WHERE email = %s
            '''
                cursor.execute(sql,( "1", email))
                db.commit()

                return redirect('/login')
            else:
                flash('Invalid verification code.')
                return "fail"


@app.route('/login',  methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')
    elif request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        db = connect()
        curs = db.cursor()

        sql = f'SELECT * FROM user WHERE email = %s;'
        curs.execute(sql , email)

        rows = curs.fetchall()
        print(rows)

        if rows:
            # result = pbkdf2_sha256.verify(password, rows[0][4])
            result = mysql.verify_password(password, rows[0][4])
            if result:
                session['is_loged_in'] = True
                session['username'] = rows[0][1]
                session['iduser'] = rows[0][0]

                print(session['is_loged_in'])
                return redirect('/')
                return render_template('index.html', is_loged_in = session['is_loged_in'] , username=session['username'], iduser=session['iduser'] )
            else:
                return redirect('/login')
        else:
            return render_template('login.html')


@app.route('/eve', methods=['GET', 'POST'])
def eve():
    if request.method =="GET":
        return render_template('eve.html')


@app.route('/testinfo', methods=['GET' , 'POST'])
@is_loged_in
def testinfo():
    if request.method == "GET":
        return render_template('testinfo.html')
    elif request.method == "POST":
        user_iduser = request.form['iduser']
        sex = request.form['sex']
        age = request.form['age']
        location = request.form['location']
        edu = request.form['edu']
        result = mysql.insert_info(user_iduser, sex, age, location, edu)
        quiz = mysql.get_quiz()
        return render_template('test.html',quiz=quiz)

@app.route('/test', methods=['GET','POST'])
@is_loged_in
def test():
    if request.method == "GET":
        user_iduser = session.get('iduser')

        # Check if user info exists in the result table
        db = connect()
        curs = db.cursor()
        sql = "SELECT * FROM result WHERE user_iduser = %s"
        curs.execute(sql, (user_iduser,))
        user_result = curs.fetchone()
        db.close()

        if user_result:
            # User result exists, redirect to result page
            return render_template('tested.html')

        # User result doesn't exist, check if user info exists
        db = connect()
        curs = db.cursor()
        sql = "SELECT * FROM info WHERE user_iduser = %s"
        curs.execute(sql, (user_iduser,))
        user_info = curs.fetchone()
        db.close()

        if user_info:
            # User info exists, proceed to test
            quiz = mysql.get_quiz()
            return render_template('test.html', quiz=quiz)
        else:
            # User info doesn't exist, redirect to testinfo
            return redirect('/testinfo')

    elif request.method == "POST":
        # Get user_iduser from session
        user_iduser = session.get('iduser')
        q1 = request.form['1']
        q2 = request.form['2']
        q3 = request.form['3']
        q4 = request.form['4']
        q5 = request.form['5']
        q6 = request.form['6']
        q7 = request.form['7']
        q8 = request.form['8']
        q9 = request.form['9']
        q10 = request.form['10']

        result = mysql.insert_answer(user_iduser, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10)
        print(result)
        return redirect('/result')




# 네이버 로그인
@app.route('/naver')
def NaverLogin():
    return naver.authorize_redirect(redirect_uri=url_for('callback', _external=True))

@app.route('/callback')
def callback():
    naver_token = naver.authorize_access_token()
    user_info = naver.get('https://openapi.naver.com/v1/nid/me').json()
    # Process user_info and store session or user data as needed
    social_name = user_info['response']['name']
    social_email = user_info['response']['email']
    social_phone =  user_info['response']['mobile']
    social_password = "naver"
    result  = mysql.social_check(social_name, social_email, social_phone, social_password)

    db = connect()
    curs = db.cursor()
    sql = f'SELECT * FROM user WHERE email = %s;'
    curs.execute(sql , social_email)
    result = curs.fetchone()
    print(result[0])

    if len(str(result)) != 0:
        session['is_loged_in'] = True
        session['username'] = result[1]
        session['iduser'] = result[0]
        return redirect('/')
    print(result)
    return redirect('/')

# Google 로그인
# @app.route('/google')
# def googlelogin():
#     google = google.create_client('google')  # create the google oauth client
#     redirect_uri = url_for('authorize', _external=True)
#     return google.authorize_redirect(redirect_uri)

# @app.route('/authorize')
# def authorize():
#     google = google.create_client('google')  # create the google oauth client
#     token = google.authorize_access_token()  # Access token from google (needed to get user info)
#     resp = google.get('userinfo')  # userinfo contains stuff u specificed in the scrope
#     user_info = resp.json()
#     user = oauth.google.userinfo()  # uses openid endpoint to fetch user info
#     print(f'user: {user}')
#     social_name = user['name']
#     social_email = user['email']
#     print(social_email)
#     social_phone = None
#     social_password = 'google'
#     result  = mysql.social_check(social_name, social_email, social_phone, social_password)
#     if len(str(result)) != 0:
#         session['is_loged_in'] = True
#         session['username'] = social_name
#         db = pymysql.connect(host=mysql.host, user=mysql.user, db=mysql.db, password=mysql.password, charset=mysql.charset)
#         curs = db.cursor()

#         sql = f'SELECT * FROM user WHERE email = %s;'
#         curs.execute(sql , social_email)
#         result = curs.fetchone()
#         print(result[3])
#         if result[3] == None:
#             return render_template('add.html', email=social_email)
#         else:
#             return redirect('/')

# @app.route('/update_phone' , methods=['GET', 'POST'])
# def update():
#     email = request.form.get("email")
#     phone = request.form.get("phone")
#     mysql.additional_info(email, phone)
#     return redirect('/')

# # 카카오 로그인 - 추후 추가 예정
# @app.route('/kakao')
# def kakao_login():
#     return kakao.authorize_redirect(redirect_uri=url_for('kakao_callback', _external=True))

# @app.route('/kakao-callback')
# def kakao_callback():
#     kakao_token = kakao.authorize_access_token()
#     user_info = kakao.get('user').json()
#     user = oauth.kakao.userinfo()
#     print(user)
#     # social_name = user['name']
#     # social_email = user['email']
#     # social_phone =  user['mobile']
#     # social_password = "kakao"
#     # result  = mysql.social_check(social_name, social_email, social_phone, social_password)
#     # if len(str(result)) != 0:
#     #     session['is_loged_in'] = True
#     #     session['username'] = social_name
#     #     return redirect('/')
#     # print(result)
#     # return redirect('/')

@app.route('/list', methods=['GET','POST'])
def list() :
    if request.method == 'GET' :
         result = mysql.get_book_data()
         return render_template('book_list.html', data=result )

    elif request.method == 'POST' :
        title = request.form['title']
        desc = request.form['desc']
        author = request.form['author']

        result = mysql.insert_data(title, desc, author)
        return render_template('book_list.html')

@app.route('/board', methods=['GET','POST'])
def b_list() :
    if request.method == 'GET' :
         result = mysql.get_board_data()
         return render_template('board_list.html', data=result )

    elif request.method == 'POST' :
        category = request.form['category']
        title = request.form['title']
        author = request.form['author']
        content = request.form['content']

        result = mysql.insert_board_data(category, title, author, content)
        return render_template('board_list.html')

@app.route('/board_register', methods=['GET'])
def board_register() :
    if request.method == 'GET' :
         result = mysql.get_board_data()
         return render_template('board_register.html', data=result )

@app.route('/result/', methods=['GET', 'POST'])
@is_loged_in
def result():
    if request.method =="GET":
        print(session['iduser'])
        cat_score, rec_book = mysql.calculate_score(session['iduser'])
        scores = mysql.calculate_score2()
        # 이 곳에  sql query문으로 내 점수의 평균 값, 성별 평균, 연령대의 평균, 총 평균 값을 구하는 함수를 생성하시거나
        # pandas를 이용하여 점수 테이블의 정보를 데이터프레임화

        # 데이터프레임에서 내 점수의 평균 값 구하기 loc[index조건]를 이용하여 내 데이터만 출력 후 mean()을 이용하여 평균 값 구하기
        user_mean = scores.loc[scores['user_iduser'] == session['iduser'], 'mean_score'].values[0]
        # 로그인한 아이디의 성별 값 불러오기
        user_sex = scores.loc[scores['user_iduser'] == session['iduser'], 'sex'].values[0]
        # 성별로 그룹화하여 성별 평균 점수 구하기
        sex_score = scores.loc[scores['sex'] == user_sex, 'mean_score'].mean()
        # 로그인한 아이디의 연령대 구하기
        user_age = scores.loc[scores['user_iduser'] == session['iduser'], 'age'].values[0]
        # 연령대로 그룹화 하여 평균 점수 구하기
        age_score = scores.loc[scores['age'] == user_age, 'mean_score'].mean()
        # 전체의 데이터 점수를 mean()함수를 이용하여 평균 값 구하기
        mean_score = scores['mean_score'].mean()
        # 위에서 만들어진 4개의 데이터를 리스트의 형태로 만들기
        score_list = [user_mean, sex_score, age_score, mean_score]
        # 만들어진 리스트 데이터를 render_template()안에 데이터로 삽입하여 chartjs의 수치 값 하드코딩한 부분에 데이터로 변경

        print(cat_score)
        print(rec_book)
        return render_template('result.html', data=cat_score, books=rec_book, scores=score_list)


# @app.route('/result/<id>', methods=['GET', 'POST'])
# # @is_loged_in
# def result(id):
#     result = mysql.get_result_by_user(id)
#     if result:
#         cat_score = result
#     else:
#         cat_score = mysql.calculate_score(id)

#     print(cat_score)
#     return render_template('result.html', data=cat_score)


@app.route('/end')
def end():
    return render_template('end.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
