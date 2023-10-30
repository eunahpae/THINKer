import pymysql
from passlib.hash import pbkdf2_sha256
import numpy as np
import pandas as pd

def hash_password(original_password):
    salt = 'eungok'
    password = original_password + salt
    password = pbkdf2_sha256.hash(password)
    return password
def check_password(input_password, hashed_password):
    print(input_password,hashed_password)
    salt = 'eungok'
    password = input_password + salt
    result=pbkdf2_sha256.verify(password, hashed_password)
    return result

class Mysql:
    # MySQL 데이터베이스에 연결하기 위한 초기화 함수
    def __init__(self, host='thinkerIn.mysql.pythonanywhere-services.com', user='thinkerIn', db='thinkerIn$thinker', password='pyflask9', charset='utf8'):
        self.host = host
        self.user = user
        self.db = db
        self.password = password
        self.charset = charset

    # 데이터베이스 연결 함수
    def connect(self):
        return pymysql.connect(host=self.host, user=self.user, db=self.db, password=self.password, charset=self.charset)

    # SQL 쿼리 실행을 위한 함수
    def execute_sql(self, sql, *args):
        db = self.connect()
        with db.cursor() as curs:
            result = curs.execute(sql, args)
            db.commit()
        db.close()
        return result

    def social_check(self, social_name, social_email, social_phone, social_password):
        sql = "SELECT * FROM user WHERE email = %s"
        with self.connect().cursor() as curs:
            curs.execute(sql, (social_email))
            rows = curs.fetchall()

        if rows:
            return "이미 존재하는 이메일입니다"
        else:
            sql = "INSERT INTO user (username, email, phone, password) VALUES (%s, %s, %s, %s)"
            return self.execute_sql(sql, social_name, social_email, social_phone, social_password)

    def verify_password(self, password, hashed_password):
        return check_password(password, hashed_password)

    def hashing_password(self, password):
        return hash_password(password)

    def additional_info(self, email, phone):
        sql = "UPDATE user SET phone =%s WHERE email =%s;"
        with self.connect().cursor() as curs:
            curs.execute(sql)
            rows = curs.fetchall()
        return rows

    def insert_user(self, username, email, phone, password):
        hashed_password = hash_password(password)
        sql = "INSERT INTO user (username, email, phone, password) VALUES (%s, %s, %s, %s)"
        return self.execute_sql(sql, username, email, phone, hashed_password)

    def insert_info(self, user_iduser, sex, age, location, edu):
        sql = "INSERT INTO info (user_iduser, sex, age, location, edu) VALUES (%s, %s, %s, %s, %s)"
        return self.execute_sql(sql, user_iduser, sex, age, location, edu)

    def insert_answer(self, user_iduser, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10):
        sql = "INSERT INTO result (user_iduser, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        return self.execute_sql(sql, user_iduser, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10)
    
    # 문항수가 많아져도 일일히 작성하지 않고 반복문사용시 (** 랜덤으로 문제가 뽑히는 경우 채점상황도 고려해봐야함/app파일도수정필요)
    # def insert_answers(self, user_iduser, **answers):
    #     # Convert the answers dictionary into a list preserving the insertion order
    #     answers_list = [answers[f'q{i}'] for i in range(1, 11)]  # Assuming 10 questions    
    #     # Create the SQL query dynamically
    #     sql = "INSERT INTO result (user_iduser, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"        
    #     # Execute the SQL query with the user ID and answers
    #     return self.execute_sql(sql, user_iduser, *answers_list)

    def get_user(self):
        sql = "SELECT * FROM user;"
        with self.connect().cursor() as curs:
            curs.execute(sql)
            rows = curs.fetchall()
        return rows
    
    def del_user(self, email):
        sql = "DELETE FROM user WHERE email = %s"
        return self.execute_sql(sql, email)

    def get_quiz(self):
        sql = "SELECT * FROM quiz;"
        with self.connect().cursor() as curs:
            curs.execute(sql)
            rows = curs.fetchall()
            print(rows)
        return rows

    def calculate_score(self,id):
        # 데이터베이스 연결
        db = self.connect()
        curs = db.cursor()

        # 퀴즈 정답 조회 쿼리
        sql_ans = "select answer from quiz;"
        # 사용자 응답 및 카테고리 정보 조회 쿼리
        sql_res = "select q1,q2,q3,q4,q5,q6,q7,q8,q9,q10 from result where user_iduser = %s;"
        sql_cat = "select edu from info where user_iduser = %s"

        curs.execute(sql_ans)
        ans_rows = np.ravel(curs.fetchall(), order='C')

        curs.execute(sql_res,id)
        a = curs.fetchall()
        # print(a)
        res_rows = np.ravel(a, order='C')

        curs.execute(sql_cat,id)
        fab_book = curs.fetchall()

        # 정답과 사용자 응답을 비교하여 일치 여부 확인
        scr = np.where((ans_rows == res_rows),1,0)
        cat_score = np.reshape(scr,(5,2)).sum(axis=1)

        # 카테고리 별 추천 도서 조회 쿼리
        rec_sql = "select * from book2 where category = %s order by 'score' desc limit 3;"
        curs.execute(rec_sql, fab_book[0][0])
        rec_book = curs.fetchall()

        # print(fab_book[0][0])
        # print(rec_book)
        db.close()

        # 카테고리별 점수와 추천 도서 정보 반환
        return cat_score, rec_book

    def calculate_score2(self):
        db = self.connect()
        curs = db.cursor(pymysql.cursors.DictCursor)

        sql = "select * from result;"
        sql2 = "select * from info;"
        sql3 = "select answer from quiz;"
        
        curs.execute(sql)
        result_data = curs.fetchall()
        curs.execute(sql2)
        info_data = curs.fetchall()
        curs.execute(sql3)
        answer_data = curs.fetchall()
        
        result_df = pd.DataFrame(result_data)
        info_df = pd.DataFrame(info_data)
        answer_df = pd.DataFrame(answer_data)
        # merge 함수를 이용하여 result table과 info table을 user_iduser값을 기준으로 조인 결합
        merge_df = pd.merge(result_df, info_df, on='user_iduser', how='left')

        # 데이터프레임에 평균 점수 파생변수 생성 
        for i in range(len(merge_df)):
            # merge 데이터에서 인덱스 별 컬럼은 q1부터 q10까지의 데이터를 nparray 형태로 추출
            user_answer = merge_df.loc[i, 'q1':'q10'].values
            # 답안 테이블을 nparray의 형태를 평평한 형태로 변환
            answer_data = answer_df.values.ravel()
            # 답안을 체크한 뒤 평균 점수 값을 대입하여 새로운 파생변수에 일일이 대입
            merge_df.loc[i, 'mean_score'] = np.where((user_answer == answer_data), 1, 0).sum() * 50 / 5
            # print(np.where((user_answer == answer_data), 1, 0).sum())
        # 파생변수가 만들어진 데이터프레임을 리턴
        return merge_df
    


    def insert_board_data(self,category, title, content, author) :
        db = self.connect()
        curs = db.cursor()
        sql = f'insert into board(b_category, b_title, b_content, b_author) values(%s,%s,%s,%s)'
        result = curs.execute(sql, (category, title, content, author))
        db.commit()
        db.close()    

    def get_book_data(self) :
        db = self.connect()
        curs = db.cursor()
        sql ="select * from book2 where category = '문학' limit 10;"
        curs.execute(sql)

        rows = curs.fetchall()
        db.close()
        return rows

    def get_board_data(self) :
        db = self.connect()
        curs = db.cursor()
        sql ="select * from board;"
        curs.execute(sql)

        rows = curs.fetchall()
        db.close()
        return rows
            