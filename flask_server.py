import numpy as np
from PIL import Image
from datetime import datetime
from flask import Flask, request, render_template, send_from_directory
from pathlib import Path
import tensorflow as tf
from PIL import ImageDraw
from transformers import pipeline
from transformers import AutoModelForImageClassification
import pickle
from transformers import AutoModelForZeroShotObjectDetection,AutoProcessor
import json
import cv2, uuid
from matplotlib import pyplot as plt


# Load the detector
with open('detector.pkl', 'rb') as f:
    loaded_detector = pickle.load(f)

def operation(img):
    img_path = f'{datetime.now().isoformat().replace(":", ".")}.png'
    predictions = loaded_detector(img, candidate_labels=["chair", "person"])
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    for pred in predictions:
        label = pred["label"]
        score = pred["score"]
        box = pred["box"]
        xmin, ymin, xmax, ymax = box["xmin"], box["ymin"], box["xmax"], box["ymax"]
        cv2.rectangle(img_cv, (xmin, ymin), (xmax, ymax), (0, 0, 255), 2)
        cv2.putText(img_cv, f"{label}: {score:.2f}", (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
    predictions = sorted(predictions, key=lambda x: x['box']['xmin'])
    img_with_boxes = Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))
    img_with_boxes.save(f'./scratch/{img_path}')
    return img_path, predictions
 
app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'GET':
            return render_template('index.html')
    file = request.files['query_img']
    img = Image.open(file.stream)
    img_path, predictions = operation(img)
    predictions_json = json.dumps(predictions)
    return render_template('index.html', img_path=img_path, predictions=predictions_json)


@app.route('/yasser', methods=["POST"])
def yasser():
    file = request.files['query_img']
    img = Image.open(file.stream)
    img_path, predictions = operation(img)
    return {
         'img_path': img_path,
         'predictions': predictions
    }

@app.route('/getImg', methods=["GET"])
def getImg():
    imgId = request.args.get('imgId', '')
    return send_from_directory('./scratch', imgId)
    
if __name__=="__main__":
    app.run("0.0.0.0")
