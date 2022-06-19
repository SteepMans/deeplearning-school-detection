from fastapi import FastAPI, File, UploadFile
from typing import List

import torch
import numpy
import cv2

app = FastAPI()
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

def load_image_into_numpy_array(data):
    npimg = numpy.frombuffer(data, numpy.uint8)
    frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return frame

@app.post("/v1/yolov5/upload")
async def yolo_upload_files(file: UploadFile = File(description="A file read as UploadFile")):
    img = load_image_into_numpy_array(await file.read())
    results = model(img)
    return results.pandas().xywh[0].to_dict('list')

@app.post("/v1/yolov5/")
async def yolo_url(url: str):
    results = model(url)
    return results.pandas().xywh[0].to_dict('list')