from flask import Flask, request, jsonify
# from flask_sslify import SSLify
from datetime import date, timedelta
from models import *


import pymysql
import time

app = Flask(__name__)
# app.config['JSON_AS_ASCII'] = False

print(" "+"=" * 50)
print("∥              [INFO] server 초기화 성공          ∥") 
print(" "+"=" * 50)


# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ


@app.route('/', methods=['GET', 'POST'])
def news():
    
    # app 버전
    if request.method == 'GET':
        
        conn = pymysql.connect(host='localhost', user='root', password='root',
                       db='news', charset='utf8mb4')
        curs = conn.cursor(pymysql.cursors.DictCursor)
        sql = "select * from `news`.summarized where 발행일자=%s"
        curs.execute(sql, ((date.today() - timedelta(1)).strftime("%Y-%m-%d")))
        
        result = curs.fetchall()
        
        conn.close()
        
        # JSON 객체 생성
        return jsonify(result)
    
        
    
@app.route('/rank', methods=['GET', 'POST'])
def rank():
    # user point update
    if request.method == 'POST':
        # 테스트용
        user = '아이유'
        point = 30
        # user = request.form['user']
        # point = request.form['point']
        
        
        conn = pymysql.connect(host='localhost', user='root', password='root',
                       db='news', charset='utf8mb4')
        curs = conn.cursor(pymysql.cursors.DictCursor)
        
        sql = "select 유저 from `news`.point"
        curs.execute(sql)

        # 데이타 Fetch
        rows = curs.fetchall()
        
        # 신규 유저인지 확인
        user_list = []
        for i in range(len(rows)):
            user_list.append(rows[i]['유저'])
            
         # 신규 유저이면 데이터 생성
        if user not in user_list:
            sql = "insert into `news`.point (유저, 포인트) values (%s, %s)"
            curs.execute(sql, (user, 0))
            conn.commit()
            
        # 유저 point update
        sql = "UPDATE `news`.point SET 포인트 = 포인트+%s WHERE 유저 = %s"
        curs.execute(sql, (point, user))
        conn.commit()
        
        conn.close()
        

        # # 테스트용
        # result = 'bye'
        # return jsonify(result)
    
    
    # user point return
    elif request.method == 'GET':
        
        
        
        
        
        return "hello"
    
    
    
if __name__ == '__main__':
    
    app.debug = True
    app.run(host='0.0.0.0', port=8000 )
        
        


