from flask import Blueprint, redirect, request, session, render_template
from random import randint
import requests
import config
from mysql import Mysql

mysql = Mysql()
bp = Blueprint('google', __name__, url_prefix='/')

@bp.route('/google')
def google_login():
    client_id = config.google_client_id
    redirect_uri = "http://eunahpae.pythonanywhere.com/authorize"
    scope = "https://www.googleapis.com/auth/userinfo.email"
    url = f"https://accounts.google.com/o/oauth2/auth?client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}&response_type=code"
    return redirect(url)

@bp.route('/authorize')
def authorize():
    code = request.args.get('code')
    client_id = config.google_client_id
    client_secret = config.google_client_secret
    redirect_uri = "http://eunahpae.pythonanywhere.com/authorize"
    token_request = requests.post(f"https://accounts.google.com/o/oauth2/token?code={code}&client_id={client_id}&client_secret={client_secret}&redirect_uri={redirect_uri}&grant_type=authorization_code")
    token_data = token_request.json()
    access_token = token_data['access_token']
    user_info = requests.get("https://www.googleapis.com/oauth2/v2/userinfo", headers={'Authorization': f"Bearer {access_token}"})
    print(user_info)
    user_data = user_info.json()
    
    # 구글 접속 시 유저 정보 전달 받기
    social_name = user_data['name']
    social_email = user_data['email']
    social_phone = "google"
    social_password = str(randint(1000000, 9999999))

    result = mysql.social_check(social_name, social_email, social_phone, social_password)
    print(result)
    
    if len(str(result)) != 0:
        session['is_loged_in'] = True
        session['username'] = social_name
        session['email'] = social_email
        
        db = mysql.connect()
        curs = db.cursor()
        sql = f'SELECT * FROM user WHERE email = %s;'
        curs.execute(sql , social_email)
        result = curs.fetchone()
        print(result[3])
        if result[3] == None:
            return render_template('add.html', email=social_email)
        else:
            return redirect('/')