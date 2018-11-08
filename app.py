from flask import Flask, jsonify, request
import random
import requests
from bs4 import BeautifulSoup

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import *

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql:///movie'
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db.init_app(app)
migrate = Migrate(app,db)

@app.route('/keyboard')
def keyboard():
    keyboard = {
        "type" : "buttons",
        "buttons" : ["메뉴","로또","고양이","영화"]
    }
    
    return jsonify(keyboard)

@app.route('/message', methods=['POST'])
def message():
    user_msg = request.json['content']
    msg = "기본응답"
    img_bool = False
    url = "기본 주소"
    
    if user_msg == "메뉴":
        # 메뉴를 담은 리스트 만들기
        menus = ['20층','멀캠식당','급식']
        # 그중 하나를 랜덤하게 고르기
        pick = random.choice(menus)
        # msg변수에 담기
        msg = pick
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
        naver_movie = 'https://movie.naver.com/movie/running/current.nhn'
        req = requests.get(naver_movie).text
        soup = BeautifulSoup(req, 'html.parser')
        
        title_list = soup.select('dt.tit > a')
        star_list = soup.select('a > span.num')
        img_url_list = soup.select('div.thumb > a > img')
        
        movies = {}
        for i in range(0,5):
            movies[i] ={
                'title':title_list[i].text,
                'star':star_list[i].text,
                'url':img_url_list[i]['src']
            }
        num = random.randrange(0,5)
        pick_movie = movies[num]
        msg = pick_movie['title'] +'/'+ pick_movie['star']
        url = pick_movie['url']
    
    return_dict = {
        'message':{
            'text':msg
        },
        'keyboard':{
            "type" : "buttons",
            "buttons" : ["로또","메뉴","고양이","영화"]
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
            "buttons" : ["로또","메뉴","고양이","영화"]
        }
    }
    
    if img_bool:
        return jsonify(return_img_dict)
    else:
        return jsonify(return_dict)
    
    
    
    
    
    
    
    
    
    