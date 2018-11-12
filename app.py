from flask import Flask, jsonify, request, render_template
import random
import requests
from bs4 import BeautifulSoup
from sqlalchemy.sql.expression import func

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import *

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql:///movie'
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db.init_app(app)
migrate = Migrate(app,db)

@app.route('/')
def index():
    movies = Movie.query.all()
    return render_template('index.html',movies=movies)

@app.route('/keyboard')
def keyboard():
    keyboard = {
        "type" : "buttons",
        "buttons" : ["메뉴 추천","로또","고양이","영화","영화저장"]
    }
    
    return jsonify(keyboard)

@app.route('/message', methods=['POST'])
def message():
    user_msg = request.json['content']
    msg = "기본응답"
    img_bool = False
    url = "기본 주소"
    
    if user_msg == "메뉴 추천":
        img_bool = True
        # 메뉴를 담은 리스트 만들기
        menus = {'제육볶음' : "http://mblogthumb3.phinf.naver.net/20140916_154/dew36_14107988004269WVlb_JPEG/1.jpg?type=w2",
                '부대찌개':"https://previews.123rf.com/images/lcc54613/lcc546131708/lcc54613170800447/84577110-%EB%B6%80%EB%8C%80-%EC%B0%8C%EA%B0%9C-%EB%83%84%EB%B9%84.jpg",
                '샤브샤브':"http://item.ssgcdn.com/16/55/60/item/1000019605516_i1_1200.jpg",
                '탕수육':"https://i1.wp.com/starkaraokeuiuc.net/wp-content/uploads/2017/09/K-11.jpg?fit=639%2C409",
                "초밥":"https://t1.daumcdn.net/cfile/tistory/234FFE3F55C5BE3F35",
                "돈까스":"https://post-phinf.pstatic.net/MjAxNzAzMjBfMjc4/MDAxNDg5OTkwMDY2MTc4.4vPmaHR24MKU7VP-NVmVxU8YlVXCiBKnfY_ibaGiUxEg.mCSbZz1LWvaFUAL2IC8BKdxrhX7HrGI0YRQycPqfoXkg.JPEG/%EB%A7%A4%EC%9A%B4%EB%8F%88%EA%B9%8C%EC%8A%A4%EC%86%8C%EC%8A%A4_%EB%88%88%EA%BD%83%EB%8F%88%EA%B9%8C%EC%8A%A4_%EC%B9%98%EC%A6%88%EB%8F%88%EA%B9%8C%EC%8A%A4_%EB%A7%8C%EB%93%A4%EA%B8%B0_%EC%88%98%EC%A0%9C%EB%8F%88%EA%B9%8C%EC%8A%A4_%EC%86%90%EC%A7%88_.JPG?type=w1200",
                "삼겹살":"http://cdn.jinfooduae.com/wp-content/uploads/2017/04/%EC%98%A4%EC%82%BC%EA%B2%B9%EC%82%B42-400x400.jpg",
                "찜닭":"https://t1.daumcdn.net/cfile/tistory/243FBD4F559A355F24",
                '곱창':"http://cfile240.uf.daum.net/image/2172893E5226D4DA36BEED",
                "잔치국수":"https://t1.daumcdn.net/cfile/tistory/23079C39535CA33214",
                "김밥":"http://www.gimgane.co.kr/board/data/file/menu/1935589796_BoOuG9yS_ECB2B4EB8BA4ECB998ECA688.png",
                "라면":"https://img.insight.co.kr/static/2017/12/13/700/4449r257yzqjwcu867k9.jpg"
                
        }
        
        
        # 그중 하나를 랜덤하게 고르기
        pick = random.choice(list(menus))
        
        
        # msg변수에 담기
        msg = pick
        url = menus[pick]
        
        
    elif user_msg == "로또":
        # 1~45가 들어간 숫자들 만들기
        numbers = range(1,46)
        # 그중에서 6개 추첨하기
        pick = random.sample(numbers,6)
        # msg 에 6개 숫자 넣기
        msg = str(sorted(pick))
    elif user_msg == "고양이":
        img_bool = True
        cat_api = 'https://api.thecatapi.com/v1/images/search?mime_types=jpg'
        req = requests.get(cat_api).json()
        # msg = url 정보를 담아서 출력
        cat_url = req[0]['url']
        url = cat_url
        msg = "나만 고양이 없어 :("
    elif user_msg == "영화":
        img_bool = True
        movie = Movie.query.order_by(func.random()).first()
        msg = movie.title + ' / ' + str(movie.star)
        url = movie.img
    elif user_msg == "영화저장":
        db.session.query(Movie).delete()
        naver_movie = 'https://movie.naver.com/movie/running/current.nhn'
        req = requests.get(naver_movie).text
        soup = BeautifulSoup(req, 'html.parser')
        
        title_list = soup.select('dt.tit > a')
        star_list = soup.select('a > span.num')
        img_url_list = soup.select('div.thumb > a > img')
        
        movies = {}
        for i in range(0,15):
            movies[i] ={
                'title':title_list[i].text,
                'star':star_list[i].text,
                'url':img_url_list[i]['src']
            }
        for i in range(0,15):
            movie=Movie(
                title_list[i].text,
                star_list[i].text,
                img_url_list[i]['src']
            )
            db.session.add(movie)
            db.session.commit()
        msg = "저장완료"
    return_dict = {
        'message':{
            'text':msg
        },
        'keyboard':{
            "type" : "buttons",
            "buttons" : ["로또","메뉴 추천","고양이","영화","영화저장"]
        }
    }
    return_img_dict = {
        'message':{
            'text':msg,
            'photo':{
                'url':url,
                'width':720,
                'height':630
            }
        },
        'keyboard':{
            "type" : "buttons",
            "buttons" : ["로또","메뉴 추천","고양이","영화","영화저장"]
        }
    }
    
    if img_bool:
        return jsonify(return_img_dict)
    else:
        return jsonify(return_dict)
    
    
    
    
    
    
    
    
    
    