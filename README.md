# THINKer  독서능력진단 평가 사이트 개발

# 프로젝트 소개

반응형 웹사이트 THINKer는 현대사회의 문제로 대두되는 **성인 문해력 저하** 실태를 짚어보고, 독서능력진단평가를 통해 이를 개선할 해법을 모색하고자 제작되었습니다.

사이트 바로가기 : [THINKer*](https://eunahpae.pythonanywhere.com/)

![image](https://github.com/eunahpae/THINKer_ver3-4/assets/139094990/9572f596-6e7d-43d5-a639-db44e9538513)

## 설치 방법

anyio==3.7.1
blinker==1.6.2
certifi==2023.5.7
click==8.1.6
colorama==0.4.6
dnspython==2.4.0
exceptiongroup==1.1.2
Flask==2.3.2
h11==0.14.0
httpcore==0.17.3
idna==3.4
itsdangerous==2.1.2
Jinja2==3.1.2
MarkupSafe==2.1.3
passlib==1.7.4
pymongo==4.4.1
sniffio==1.3.0
Werkzeug==2.3.6

## 기술 스택 및 언어

- **언어 및 프레임워크**
    - Python을 주 언어로 사용한 Flask 웹 프레임워크
    - HTML5, CSS3, JavaScript
- **라이브러리 및 도구**
    - Flask, MySQL
    - jQuery, Jinja2
    - pandas, SMTP, passlib, datetime, functools, smtplib, email.mime 라이브러리 등
    

## 주요 구현 기능

- **회원가입 및 로그인**
    - **사이트 자체**
        - 회원가입: 이메일을 통한 가입 절차, 비밀번호 해싱(PBKDF2)을 통한 보안
        - 로그인: 이메일과 비밀번호를 통한 로그인, 세션을 이용한 인증 유지
    - **소셜 로그인**
        - Naver, Google, Kakao
        - Flask 라이브러리 중 Blueprint를 활용하여 각 파일 분류, 유지보수에 유리하게 적용

- **테스트 및 결과 제공**
    - **테스트 : 독서능력진단평가**
        - 시험 응시 전 사용자 사전 정보 입력
        - 데이터베이스에서 문제를 불러와 답안 제출을 통한 테스트진행
    
    ```python
    **mysql.py)**
    # DB에서 시험문제 조회하는 함수
        def get_quiz(self):
            sql = "SELECT * FROM quiz;"
            with self.connect().cursor() as curs:
                curs.execute(sql)
                rows = curs.fetchall()
                print(rows)
            return rows
    
    **flask_app.py)**
    	    if user_info:
                # info테이블에 사용자 정보가 있는 경우 퀴즈 페이지 렌더링
                quiz = mysql.get_quiz()
    			# 해당 template에 jinja2 문법을 사용하여 DB에서 시험문제를 불러와 뿌려줌
                return render_template('test.html', quiz=quiz)
            else:
                # info테이블에 사용자 정보가 없는 경우 정보 입력 페이지로 리디렉션
                return redirect('/testinfo')
    ```
    
    - **결과**
        - 사용자의 제출 답안과 정답을 비교하여 결과 시각화
            
            ```python
            mysql.py에서 **calculate_score,calculate_score 함수 불러와 시험결과를 채첨하고 
            원하는 방식으로 시각화**
            
            **flask_app.py)**
               if user_result:
                  cat_score, rec_book = mysql.**calculate_score**(session['iduser'])
                  scores = mysql.**calculate_score2**()
            
                  # 데이터프레임에서 내 점수의 평균 값 구하기
                  # loc[index조건]를 이용하여 내 데이터만 출력 후 mean()으로 평균값 구하기
                  user_mean = scores.loc[scores['user_iduser']  == session['iduser'], 'mean_score'].values[0]
                  # 로그인한 아이디의 성별 값 불러오기
                  user_sex = scores.loc[scores['user_iduser']  == session['iduser'], 'sex'].values[0]
            	  
                  ...

                  # 연령대로 그룹화 하여 평균 점수 구하기
                  age_score = scores.loc[scores['age'] == user_age, 'mean_score'].mean()
                  # 전체의 데이터 점수를 mean()함수를 이용하여 평균 값 구하기
                  mean_score = scores['mean_score'].mean()
                  # 위에서 만들어진 4개의 데이터를 리스트의 형태로 만들기
                  score_list = [user_mean, sex_score, age_score, mean_score]
            
                  return render_template('result.html', data=cat_score, books=rec_book, scores=score_list)
            	 
                  ...
            ```
            
        
        - 각 항목별 사용자의 점수와 전체 평균 오각형 그래프
            
            ![image](https://github.com/eunahpae/THINKer_ver3-4/assets/139094990/df0368e4-2f46-4c82-9dc2-70608c41a1dd)
            
        
        - 사용자의 총점과 성별, 연령대, 전체 평균 비교 바형 그래프
            
            ![image](https://github.com/eunahpae/THINKer_ver3-4/tree/main/static/images/md/result2.jpg)
            
    
    - **도서추천**
        - 사용자가 사전정보에서 입력한 도서 선호장르를 기반으로 시험점수별 추천 도서 제공
          ( 현재 장르별 도서 추천기능 구현, 점수별 추천은 아직 개발중 )
        
        ![image](https://www.notion.so/THINKer-8e098eb53dc84cf19e3059cfb6d008ca?pvs=4#4816fc57185f47dabff101bf0e95537e)
        
- **데이터베이스 상호작용**
    - MySQL을 사용하여 사용자 정보, 테스트 결과, 책 정보, 게시판 데이터 저장 및 관리
    - 데이터베이스 연동하여 사용자 정보, 테스트 결과를 활용하여 특정 기능 수행
    
    ![image](https://github.com/eunahpae/THINKer_ver3-4/assets/139094990/aaa394b6-de7b-460c-88b8-e797fcdb1a9c)
    
- **레이아웃 분리 /  전체 적용**