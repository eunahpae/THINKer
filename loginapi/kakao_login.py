from flask import request ,redirect, session, Blueprint
from mysql import Mysql
import config
import pymysql
import requests
from random import randint

mysql = Mysql()
bp = Blueprint('kakao', __name__, url_prefix='/')

@bp.route('/kakao')
def KakaoLogin():
    client_id = config.kakao_client_id
    redirect_uri = "http://eunahpae.pythonanywhere.com/kakao-callback"
    # 카카오톡으로 로그인 버튼을 눌렀을 때
    url = f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    return redirect(url)


@bp.route('/kakao-callback')
def callback():
    code = request.args.get("code")
    client_id = config.kakao_client_id
    client_secret = config.kakao_client_secret
    redirect_uri = "http://eunahpae.pythonanywhere.com/kakao-callback"
    token_request = requests.get(f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&redirect_uri={redirect_uri}&code={code}")
    token_json = token_request.json()
    # print(token_json)
    access_token = token_json.get("access_token")
    profile_request = requests.get("https://kapi.kakao.com/v2/user/me", headers={"Authorization" : f"Bearer {access_token}"},)
    profile_data = profile_request.json()
    print(profile_data)

    # 카카오 로그인 시 유저 정보 전달 받기
    social_name  = profile_data['kakao_account']['profile']['nickname']
    social_email = profile_data['kakao_account']['email']
    social_phone = 'kakao'
    social_password = profile_data['id']
    print(social_name)
    print(social_email)
    print(social_password)

    result  = mysql.social_check(social_name, social_email, social_phone, social_password)

    if len(result) != 0:
        session['is_loged_in'] = True
        session['username'] = social_name
        session['email'] = social_email
        session['phone'] = social_phone
        return redirect('/')



