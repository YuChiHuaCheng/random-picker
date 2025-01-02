import pandas as pd
from flask import Flask, render_template, jsonify, request
import random

# 创建 Flask 应用
app = Flask(__name__)

# 读取 CSV 文件并加载数据
df = pd.read_csv('./merged_douban.csv')  # 替换为你的清理后的 CSV 文件路径

@app.route('/')
def index():
    # 提取所有类型（Type）
    types = df['Type'].dropna().unique().tolist()  # 生成类型下拉框内容
    return render_template('index.html', types=types)

@app.route('/get_genres', methods=['GET'])
def get_genres():
    selected_type = request.args.get('type')  # 获取选择的类型
    if not selected_type:
        return jsonify({'message': '请选择类型'})

    # 根据选择的类型获取对应的标签
    filtered_df = df[df['Type'] == selected_type]
    genres = filtered_df['Genres'].dropna().unique().tolist()

    return jsonify({'genres': genres})

@app.route('/random_item', methods=['GET'])
def random_item():
    # 获取前端传来的筛选条件
    selected_genre = request.args.get('genre')
    selected_type = request.args.get('type')
    min_score = float(request.args.get('min_score', 0))  # 默认最低评分为0

    min_score_str = request.args.get('min_score', '0')
    try:
        min_score = float(min_score_str)
    except ValueError:
        min_score = 0  #  优雅地处理无效输入
    # 根据筛选条件过滤数据
    filtered_df = df[df['Score'] >= min_score]
    if selected_genre:
        filtered_df = filtered_df[filtered_df['Genres'] == selected_genre]
    if selected_type:
        filtered_df = filtered_df[filtered_df['Type'] == selected_type]

    # 如果没有符合条件的数据，返回一个提示
    if filtered_df.empty:
        return jsonify({'message': '没有符合条件的项目'})

    # 随机选择一行
    random_row = filtered_df.sample(n=1)
    item_name = random_row['Item_name'].values[0]  # 获取名称
    return jsonify({'item_name': f'《{item_name}》'})  # 返回加名称号的名称

if __name__ == '__main__':
    app.run(debug=True)
