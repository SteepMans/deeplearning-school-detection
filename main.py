from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from typing import List
import os
from fastapi.middleware.cors import CORSMiddleware

import torch
import numpy
import cv2

from model import *

origins = [
    "http://localhost",
    "http://localhost:3000"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

def load_image_into_numpy_array(data):
    npimg = numpy.frombuffer(data, numpy.uint8)
    frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return frame

@app.post("/v1/model/uploads")
async def custom_model_torch_uploads(model_name: str, files: List[UploadFile]):
    results = []

    try:
        model = Model(model_name, confidence = 0.5)
    except Exception as exp:
        print(exp)
        raise HTTPException(status_code=404, detail=str(exp))


    return results

@app.post("/v1/yolov5/uploads")
async def yolo_upload_files(files: List[UploadFile]):
    results = []
    
    for file in files:
        img = load_image_into_numpy_array(await file.read())
        predict = model(img)
        results.append(predict.pandas().xyxy[0].to_dict('records'))

    return results 

@app.post("/v1/yolov5/")
async def yolo_url(url: str):
    results = model(url)
    return results.pandas().xyxy[0].to_dict('records')

@app.get("/file/{name_file}")
def get_file(name_file: str):
    return FileResponse(path=os.getcwd() + "/" + name_file)