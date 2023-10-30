from flask import Blueprint, redirect, request, session
from mysql import Mysql
import config
import requests
from random import randint

mysql = Mysql()
bp = Blueprint('naver', __name__, url_prefix='/')

@bp.route("/naver")
def NaverLogin():
    client_id = config.naver_client_id
    redirect_uri = "http://eunahpae.pythonanywhere.com/callback"
    url = f"https://nid.naver.com/oauth2.0/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    return redirect(url)

@bp.route("/callback")
def callback():
    params = request.args.to_dict()
    code = params.get("code")
    client_id = config.naver_client_id
    client_secret = config.naver_client_secret
    redirect_uri = "http://eunahpae.pythonanywhere.com/callback"
    token_request = requests.get(f"https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&code={code}")
    token_json = token_request.json()
    print(token_json)
    access_token = token_json.get("access_token")
    profile_request = requests.get("https://openapi.naver.com/v1/nid/me", headers={"Authorization" : f"Bearer {access_token}"},)
    profile_data = profile_request.json()
    print(profile_data)
    # 네이버 접속 시 유저 정보 전달 받기
    social_name = profile_data['response']['name']
    social_email = profile_data['response']['email']
    social_phone = "naver"
    social_password = str(randint(1000000, 9999999))
    
    result  = mysql.social_check(social_name, social_email, social_phone, social_password)
    print(result)

    if len(result) != 0:
        session['is_loged_in'] = True
        session['username'] = social_name
        session['email'] = social_email
        return redirect('/')