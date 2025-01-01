import pandas as pd
from flask import Flask, render_template, jsonify, request
import random

# 创建 Flask 应用
app = Flask(__name__)

# 读取 CSV 文件并加载数据
df = pd.read_csv('cleaned_douban_book.csv')  # 替换为你的清理后的 CSV 文件路径

@app.route('/')
def index():
    # 提取所有标签（去重）
    tags = df['tag'].dropna().unique().tolist()
    return render_template('index.html', tags=tags)

@app.route('/random_book', methods=['GET'])
def random_book():
    # 获取前端传来的筛选条件
    selected_tag = request.args.get('tag')
    min_star = float(request.args.get('min_star', 0))  # 默认最低星级为0

    # 根据筛选条件过滤数据
    filtered_df = df[df['star'] >= min_star]
    if selected_tag:
        filtered_df = filtered_df[filtered_df['tag'] == selected_tag]

    # 如果没有符合条件的数据，返回一个提示
    if filtered_df.empty:
        return jsonify({'message': '没有符合条件的书籍'})

    # 随机选择一行
    random_row = filtered_df.sample(n=1)
    book_name = random_row['book_name'].values[0]  # 获取书名
    return jsonify({'book_name': f'《{book_name}》'})  # 返回加书名号的书名

if __name__ == '__main__':
    app.run(debug=True)
