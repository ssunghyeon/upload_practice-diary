from flask import Flask, render_template, jsonify, request, redirect, url_for
app = Flask(__name__)
import requests
from bs4 import BeautifulSoup
from datetime import datetime

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbprac


@app.route('/')
def home():
    cards = list(db.cards.find({}, {'_id': False}))
    return render_template('index.html', cards=cards)

@app.route('/listing', methods=['GET'])
def listing():
    cards = list(db.cards.find({},{'_id': False}))
    return jsonify({'cards' : cards})

@app.route('/posting', methods=['POST'])
def posting():
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']
    file = request.files['file_give']

    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    savetime = today.strftime('%Y-%m-%d')
    extension = file.filename.split('.')[1]

    save_to = f'static/{mytime}.{extension}'
    file.save(save_to)

    doc = {'title': title_receive, 'content': content_receive, 'file': f'{mytime}.{extension}', 'savetime': f'{savetime}'}
    db.cards.insert_one(doc)
    return jsonify({'msg': '업로드 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)