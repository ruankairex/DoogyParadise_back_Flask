from flask import Flask, request, jsonify, render_template
import cv2
import numpy as np
from keras.applications import ResNet50
from keras.applications.resnet import preprocess_input
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('upload.html')

# 預訓練的 ResNet 模型，不含分類器
resnet_model = ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# 圖片數據，用 Google 雲端的路徑的話（必須先連雲端）
database_image_paths = [
    'images\\1.jpg',
    'images\\2.jpg',
    'images\\3.jpg',
    'images\\5.jpg',
    'images\\7.jpg',
    'images\\9.jpg',
    'images\\10.jpg',
    'images\\11.jpg',
    'images\\12.jpg',
    'images\\14.jpg',
]

# 圖片處理
def preprocess_image(image):
    image = cv2.resize(image, (224, 224))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # BGR轉RGB(圖片)
    image = preprocess_input(image)  # 圖片處理
    return image

# 提取圖片特徵向量
database_images = [cv2.imread(image_path) for image_path in database_image_paths]
database_features = [resnet_model.predict(np.expand_dims(preprocess_image(img), axis=0))[0] for img in database_images]

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    image = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_COLOR)
    user_image_processed = preprocess_image(image)
    user_features = resnet_model.predict(np.expand_dims(user_image_processed, axis=0))[0]
    
    similarities = [cosine_similarity([user_features.flatten()], [db_features.flatten()])[0][0] for db_features in database_features]
    most_similar_index = np.argmax(similarities)
    most_similar_image_path = database_image_paths[most_similar_index]
    
    return jsonify({'most_similar_image_path': most_similar_image_path})

if __name__ == '__main__':
    app.run(debug=True)