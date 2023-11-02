# Flask 모듈을 가져옴
from flask import Flask, render_template, request, redirect, session, flash
# MySQL 모듈을 가져옴
from mysql import Mysql
# 시간 관련 모듈인 timedelta를 가져옴
from datetime import timedelta
# 데코레이터를 사용하기 위한 functools 모듈의 wraps 함수를 가져옴
from functools import wraps
# 임의의 문자열을 생성하기 위한 random과 string 모듈을 가져옴
import random
import string
# 이메일 전송을 위한 smtplib와 MIME 모듈을 가져옴
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# 외부 파일에서 소셜로그인 관련 기능을 가져옴
from loginapi import naver_login, kakao_login, google_login
# 비밀번호 해싱을 위한 passlib 모듈의 pbkdf2_sha256 함수를 가져옴
from passlib.hash import pbkdf2_sha256

# Flask 애플리케이션 생성
app = Flask(__name__)

# 세션에서 사용할 시크릿키 설정
app.secret_key = "eungok"

# 세션 수명 설정
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=15)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'

# Mysql 클래스의 인스턴스 생성
mysql = Mysql()

# 로그인(세션) 확인 데코레이터
def is_loged_in(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        # 세션에 사용자가 로그인했는지 확인
        if 'is_loged_in' in session:
            return func(*args, **kwargs)
        else:
            # 로그인이 되어 있지 않다면 로그인 페이지로 리디렉션
            return redirect('/login')
    return wrap

# 회원가입 시 이메일로 전송되는 인증코드 생성
def generate_verification_code():
    # 랜덤한 6자리 코드 생성
    number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return number

# 회원가입 시 이메일로 인증 링크를 보내는 함수
def send_verification_email(email, number):
    # DB 연결
    db = mysql.connect()
    cursor = db.cursor()
    # 사용자의 이메일이 DB에 있는지 확인
    sql='SELECT * FROM user WHERE email = %s'
    cursor.execute(sql, [email])
    users = cursor.fetchone()
    # print(users)

    # 사용자가 없다면(이메일이 등록되어 있지 않은 경우), 이메일 및 코드 정보를 삽입
    if users==None:
        # 이메일과 코드 정보를 DB에 삽입
        sql = '''
            INSERT INTO user (email, code )
            VALUES (%s ,%s )
        '''
        verification_code = pbkdf2_sha256.hash(number)
        print(number)
        cursor.execute(sql,(email, verification_code))
        db.commit()

        # 이메일 발송을 위한 설정
        from_email = 'eunahp86@gmail.com'
        password = 'trwcpqrofghewkxy'
        subject = 'Email Verification'

        # 이메일 내용 설정
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = email
        msg['Subject'] = subject

        # 이메일 본문내용 작성
        verification_link = f'https://thinkerin.pythonanywhere.com/verify?email={email}&code={number}'
        message = f"Hello,\n\nPlease click the following link to verify your email:\n\n{verification_link}\n\nBest regards,\nYour Website Team"
        # 이메일 내용을 MIMEText로 첨부
        msg.attach(MIMEText(message, 'plain'))

        # 이메일 전송 시도
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, email, msg.as_string())
            server.quit()
            print('Email sent successfully!')
        except Exception as e:
            print(f'Error sending email: {e}')
    # 이미 사용자가 있다면, 해당 사용자의 코드 업데이트 후 이메일 재전송
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

# 메인 페이지
@app.route('/')
def index():
    return render_template('index.html')

# 기업소개 페이지
@app.route('/intro', methods=['GET', 'POST'])
def intro():
    if request.method =="GET":
        return render_template('intro.html')
    
# 평가안내 페이지
@app.route('/eve', methods=['GET', 'POST'])
def eve():
    if request.method =="GET":
        return render_template('eve.html')

# 공지사항 페이지
@app.route('/notice')
def notice():
    return render_template('notice.html')

# 이벤트 페이지
@app.route('/event')
def event():
    return render_template('event.html')

# 자주 묻는 질문 페이지
@app.route('/faq')
def faq():
    return render_template('faq.html')

# 미완성 페이지
@app.route('/end')
def end():
    return render_template('end.html')

# 회원가입을 위한 이메일 입력 페이지
@app.route('/email', methods=['GET', 'POST'])
def email():
    if request.method == 'POST':
        email = request.form.get('email')
        db = mysql.connect()
        curs = db.cursor()

        # 사용자가 입력한 이메일을 DB에서 검색, 결과 가져오기
        sql = f'SELECT * FROM user WHERE email = %s;'
        curs.execute(sql , email)
        rows = curs.fetchone()
        if rows:
            # 이미 인증된 이메일인 경우 로그인 페이지로 이동
            if rows[6]:
                flash("이미 가입된 이메일입니다.")
                return render_template('login.html')
            # 인증되지 않은 경우 등록 페이지로 이동
            else:
                return render_template('register.html',email=email)
        # 등록되지 않은 이메일로도 등록 페이지로 이동
        else:
            return render_template('register.html',email=email)
    # GET 방식인 경우 이메일 입력 페이지로 이동
    else:
        return render_template('email.html')

# 가입이 완료되었으니 해당 메일로 발송된 인증메일 확인하라는 페이지
@app.route('/emailcheck', methods=['GET', 'POST'])
def emailcheck():
    email=request.form.get('email')
    return render_template('emailcheck.html')

# 회원가입 페이지
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # 사용자가 제출한 데이터를 가져옴
        username = request.form.get('username')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        # 이메일 인증 코드 생성
        number = generate_verification_code()
        # 생성된 코드를 해당 이메일로 전송
        send_verification_email(email, number)
        # 비밀번호 해싱
        password = mysql.hashing_password(password)
        # print(password)
        db = mysql.connect()
        curs = db.cursor()

        # 이메일을 기반으로 사용자 정보 업데이트
        sql = f'UPDATE user SET username =%s, phone=%s,password=%s WHERE email = %s;'
        curs.execute(sql , (username,phone,password,email))
        db.commit()
        db.close()
        # 이메일 확인 페이지로 이동
        return render_template('emailcheck.html', email=email)
    elif request.method == "GET":
        return redirect('/email')

# Verification route
@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'GET':
        email = request.args.get('email')
        code = request.args.get('code')
        db = mysql.connect()
        cursor = db.cursor()
        sql = 'SELECT * FROM user WHERE email = %s'
        cursor.execute(sql, [email])
        users = cursor.fetchone()
        # print(users)

        # 이메일이 등록되지 않은 경우
        if users == None:
            # flash 메시지: 이메일이 등록되지 않았음
            flash('이메일이 등록되지 않았습니다.')
            # 실패 메시지 반환
            return "fail"
        # 이메일이 등록된 경우
        else:
            # 사용자가 입력한 확인 코드와 저장된 해시된 코드 비교
            if pbkdf2_sha256.verify(code, users[5]):
                # flash 메시지: 이메일 인증 성공
                flash('이메일 인증에 성공했습니다.')
                # DB에서 사용자 'auth' 값을 업데이트
                sql = '''
                UPDATE user SET auth = %s WHERE email = %s
            '''
                cursor.execute(sql,( "1", email))
                db.commit()

                return redirect('/login')
            else:
                # flash 메시지: 잘못된 확인 코드
                flash('잘못된 확인 코드입니다.')
                # 실패 메시지 반환
                return "fail"


@app.route('/login',  methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')
    elif request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        db = mysql.connect()
        curs = db.cursor()

        # 사용자가 입력한 이메일이 DB에 있는지 확인
        sql = 'SELECT * FROM user WHERE email = %s;'
        curs.execute(sql , email)
        rows = curs.fetchall()
        # print(rows)

        if rows:
            # 입력한 비밀번호를 해시된 비밀번호와 비교하여 인증
            result = mysql.verify_password(password, rows[0][4])
            if result:
                # 세션 설정하여 로그인 유지
                session['is_loged_in'] = True
                session['username'] = rows[0][1]
                session['iduser'] = rows[0][0]

                print(session['is_loged_in'])
                # 로그인 성공 시 메인 페이지로 리디렉션
                return render_template('index.html', is_loged_in = session['is_loged_in'] , username=session['username'], iduser=session['iduser'] )
            else:
                # 실패 시 로그인 페이지로 리디렉션
                flash("비밀번호가 일치하지 않습니다.")
                return redirect('/login')
        else:
            # 등록되지 않은 이메일로 로그인 시도 시 로그인 페이지로 리디렉션
            flash("해당 이메일로 등록된 사용자 정보가 없습니다.")
            return render_template('login.html')


@app.route('/testinfo', methods=['GET' , 'POST'])
@is_loged_in
def testinfo():
    if request.method == "GET":
        return render_template('testinfo.html')
    # POST 요청 시 사용자 정보 DB에 추가 후 시험(퀴즈) 페이지 렌더링
    elif request.method == "POST":
        user_iduser = request.form['iduser']
        sex = request.form['sex']
        age = request.form['age']
        location = request.form['location']
        edu = request.form['edu']
        result = mysql.insert_info(user_iduser, sex, age, location, edu)
        quiz = mysql.get_quiz()
        return render_template('test.html', quiz=quiz)

@app.route('/test', methods=['GET','POST'])
@is_loged_in
def test():
    if request.method == "GET":
        user_iduser = session.get('iduser')

        # DB 결과 테이블에서 사용자 정보 존재 여부 확인
        db = mysql.connect()
        curs = db.cursor()
        sql = "SELECT * FROM result WHERE user_iduser = %s"
        curs.execute(sql, (user_iduser,))
        user_result = curs.fetchone()
        db.close()

        if user_result:
            flash("이미 응시한 이력이 있습니다.")
            # 사용자 결과가 있는 경우 결과 페이지로 이동
            return redirect('/result')

        # 결과테이블에 사용자 정보가 없고, info테이블에 사용자 정보가 있는지 확인
        db = mysql.connect()
        curs = db.cursor()
        sql = "SELECT * FROM info WHERE user_iduser = %s"
        curs.execute(sql, (user_iduser,))
        user_info = curs.fetchone()
        db.close()

        if user_info:
            # info테이블에 사용자 정보가 있는 경우 퀴즈 페이지 렌더링
            quiz = mysql.get_quiz()
            return render_template('test.html', quiz=quiz)
        else:
            # info테이블에 사용자 정보가 없는 경우 정보 입력 페이지로 리디렉션
            return redirect('/testinfo')

    # 문항수가 많아져도 일일히 작성하지 않고 반복문사용시 (** 랜덤으로 문제가 뽑히는 경우 채점상황도 고려해봐야함/Mysql파일도수정필요)
    elif request.method == "POST":
        user_iduser = session.get('iduser')
        answers = {}
        # 10문제로 가정 (필요에 따라 범위 변경 필요)
        for i in range(1, 11):
            # HTML 양식에 입력 이름 '1', '2', ..., '10'
            answers[f'q{i}'] = request.form[str(i)]  
            # 모든 답변을 DB에 삽입
            result = mysql.insert_answers(user_iduser, **answers)
    return redirect('/result')

@app.route('/update_phone' , methods=['GET', 'POST'])
def update():
    email = request.form.get("email")
    username = request.form.get("username")
    phone = request.form.get("phone")
    rows = mysql.additional_info(email,username,phone)
    session['is_loged_in'] = True
    session['username'] = rows[0][1]
    session['iduser'] = rows[0][0]
    return redirect('/', is_loged_in = session['is_loged_in'] , username=session['username'], iduser=session['iduser'] )

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

# 시험 결과 시각화 페이지
@app.route('/result/', methods=['GET', 'POST'])
@is_loged_in
def result():
    if request.method == "GET":
        user_iduser = session.get('iduser')

        db = mysql.connect()
        curs = db.cursor()
        sql = "SELECT * FROM result WHERE user_iduser = %s"
        curs.execute(sql, (user_iduser,))
        user_result = curs.fetchone()
        db.close()

        if user_result:
            print(session['iduser'])
            cat_score, rec_book = mysql.calculate_score(session['iduser'])
            scores = mysql.calculate_score2()

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

        else:
            flash("응시 이력이 없습니다. 시험 응시 페이지로 가시겠습니까?")
            return redirect('/test')



# 로그아웃 : 세션종료
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# Social_login
app.register_blueprint(naver_login.bp)
app.register_blueprint(kakao_login.bp)
app.register_blueprint(google_login.bp)

# Flask 애플리케이션 실행
if __name__ == '__main__':
    app.run(debug=True)
