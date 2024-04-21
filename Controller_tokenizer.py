from flask import Flask, request, jsonify,make_response
from ckiptagger import WS
from pymongo import MongoClient
import datetime
import json

# 連接到MongoDB
client = MongoClient('mongodb://localhost:27017/')
# 資料庫DB
db = client['ispan_team']
# 集合Collection
collection = db['tweet_data']


app = Flask(__name__)
app.config['JSON_AS_ASCII']=False


ws = WS("./data", disable_cuda=False)
stop_words=[',','我','你','妳','和','的','是','最',' ','、','。','堂','900','600','能','估','至','，','!','了','一','去','有','今天','這','']

def count_words(word_sentence_list):
    word_count = {}
    for word_sentence in word_sentence_list:
        for word in word_sentence:
            # 過濾掉停用詞
            if word and word.strip() not in stop_words:
                if word in word_count:
                    word_count[word] += 1
                else:
                    word_count[word] = 1
    return word_count

#JSON 序列化，處理 datetime 物件
def serialize_datetime(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError ("Object of type '{}' is not JSON serializable".format(type(obj)))


@app.route('/api/process_sentence', methods=['POST'])
def process_sentence():
    data = request.json
    sentence_list = data.get('sentences', [])
    word_sentence_list = ws(sentence_list)
    filtered_word_count = count_words(word_sentence_list)

    # （count）降冪排序，取前10。
    sorted_word_count = sorted(filtered_word_count.items(),key=lambda x:x[1],reverse=True)[:10]
    sorted_word_count_dict = dict(sorted_word_count)
    
    # 在資料中加入時間戳記
    current_time = datetime.datetime.now()
    
    response_data = {"words": sorted_word_count_dict, "timestamp": current_time}

   # 建response
    response = make_response(json.dumps(response_data, default=serialize_datetime, ensure_ascii=False))
    
    # 設headers
    response.headers["Content-Disposition"] = "attachment; filename=result.json"
    response.headers["Content-Type"] = "application/json; charset=utf-8"


    result = collection.insert_one(response_data)

    if result.acknowledged:
        print(" MongoDB insert successed")
    else:
        print(" MongoDB insert failed")


   
  
    return response

if __name__ == '__main__':
    app.run(debug=True)