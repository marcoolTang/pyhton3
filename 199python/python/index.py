from flask import Flask, url_for,render_template, send_file, redirect, jsonify
import logging
from logging.handlers import RotatingFileHandler
import pandas as pd
from bs4 import BeautifulSoup
import requests
from threading import Thread

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import openpyxl
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
app.debug=True

# 配置日志输出文件
logfile = 'app.log'
handler = RotatingFileHandler(logfile, maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)


# 设置日志格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# 添加日志处理器到 Flask 的日志系统中
app.logger.addHandler(handler)

# @app.route('/')
# def hello_world():
#     app.logger.info('hello route accessed')
#     return render_template('hello.html')

# @app.route('/hello/')
# @app.route('/hello/<name>')
# def hello(name=None):
   
#     return render_template('hello.html', name=name)

# 全局变量，用于存储爬取线程
scraper_thread = None

@app.route('/login')
def login():
    return 'Logins'

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id


class ScraperThread(Thread):
    def __init__(self, query):
        super().__init__()
        self.query = query
        self.result = None

    def run(self):
        # 执行爬取任务
        # url = f"https://s.taobao.com/search?q={self.query}"
        url = f"https://jiage.cngold.org/shucai/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser', from_encoding='utf-8')
        items = soup.select('.xh_quote_s.xh_quote')
        print(items)
        prices = []
        titles = []
        links = []
        for item in items:
            price = item.select('strong.red')[0].text
            title = item.select('p.xh_name strong')[0].text
            link = 'https:'
            prices.append(price)
            titles.append(title)
            links.append(link)
            self.result = pd.DataFrame({'名称': titles, '价格': prices, '链接': links})

@app.route('/')
def index():
    # 默认搜索关键词

    global scraper_thread  # 使用全局变量

    query = '手机'
    
    # 获取数据
    scraper_thread = ScraperThread(query)
    scraper_thread.start()

    # 等待爬取任务完成
    scraper_thread.join()

    if scraper_thread.result is not None:
        data = scraper_thread.result

        # 将 DataFrame 保存到 Excel 文件
        excel_file = 'output.xlsx'
        data.to_excel(excel_file, index=False)

        return render_template('index.html', excel_file=excel_file, allow_download=True)
    else:
        return render_template('index.html', allow_download=False)

@app.route('/download_excel')
def download_excel():
    # 用户点击下载链接时返回 Excel 文件
    excel_file = 'output.xlsx'
    return send_file(excel_file, as_attachment=True)
@app.route('/status')
def status():
    # 返回任务状态
    if scraper_thread.is_alive():
        return jsonify(status='in_progress')
    else:
        return jsonify(status='completed')
    
if __name__ == '__main__':
    app.run()