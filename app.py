from flask import Flask, jsonify, request
import random
import requests
app = Flask(__name__)

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
        cat_api = 'https://api.thecatapi.com/v1/images/search?mime_types=jpg'
        req = requests.get(cat_api).json()
        # msg = url 정보를 담아서 출력
        cat_url = req[0]['url']
        msg = cat_url
    
    return_dict = {
        'message':{
            'text':msg,
            'photo':{
                'url':msg,
                'width':720,
                'height':630
            }
        },
        'keyboard':{
            "type" : "buttons",
            "buttons" : ["로또","메뉴","고양이","영화"]
        }
    }
    return jsonify(return_dict)
    
    
    
    
    
    
    
    
    
    