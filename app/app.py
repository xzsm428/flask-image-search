import os
import cv2
from flask import Flask, render_template, request, jsonify
from pyimagesearch.FeatureDescriptor import FeatureDescriptor
from pyimagesearch.searcher import Searcher

# 创建Flask实例，指定静态文件夹为static
app = Flask(__name__, static_url_path = "", static_folder = "static")
# 索引文件index.csv的路径
INDEX = os.path.join(os.path.dirname(__file__), 'index.csv')

# main route
@app.route('/')
def index():
    return render_template('index.html')

# upload route
@app.route('/upload', methods=['POST'])
def upload():
    if request.method == "POST":
        file=request.files['image']
        # get path
        image_path='queries/'+file.filename
        # 返回查询图像的路径
        return jsonify({'image_path': image_path})

# search route
@app.route('/search', methods=['POST'])
def search():
    if request.method == "POST":
        file=request.files['image']
        RESULTS_ARRAY = []
        # get path
        image_path='D:\\cv_design\\image_search\\app\\static\\queries\\'+file.filename
        # 输出查询图像的路径
        print(image_path)
        try:
            # 初始化FeatureDescriptor类
            # 8个色调bin，12个饱和度bin，3个value bin
            cd = FeatureDescriptor((8, 12, 3))
            # 读取查询图像
            query = cv2.imread(image_path)
            # 提取查询图像的特征
            features = cd.describe(query)
            # 使用Searcher类在索引文件中查询相似图像
            searcher = Searcher(INDEX)
            results = searcher.search(features)
            # 将检索结果存入RESULTS_ARRAY中，包含图像名和相似度
            for (score, resultID) in results:
                RESULTS_ARRAY.append(
                    {"image": str(resultID), "score": str(score)})
            # return success
            if len(RESULTS_ARRAY) == 0:
                return jsonify({"sorry": "Sorry, no results! Please try again."}), 500
            else:
                return jsonify(results=RESULTS_ARRAY)
        except:
            # return error
            return jsonify({"sorry": "Sorry, no results! Please try again."}), 500


# run!
if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)