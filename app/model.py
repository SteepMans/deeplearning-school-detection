from torchvision.models import detection
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import pickle
import torch
import time
import cv2

MODELS = {
	"frcnn-resnet": detection.fasterrcnn_resnet50_fpn,
	"frcnn-mobilenet": detection.fasterrcnn_mobilenet_v3_large_320_fpn,
	"retinanet": detection.retinanet_resnet50_fpn
}

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
CLASSES = [
    '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stop sign',
    'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
    'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A', 'N/A',
    'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
    'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
    'bottle', 'N/A', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
    'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
    'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table',
    'N/A', 'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
    'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A', 'book',
    'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]

class Model():
	def __init__(self, model_name, confidence):
		if model_name not in MODELS:
			raise Exception("models not found")
		
		self.model_name = model_name
		self.model = MODELS[model_name](pretrained=True, progress=True, num_classes=len(CLASSES), pretrained_backbone=True)
		self.model.eval()
		self.confidence = confidence

	def predict(self, image):
		image = image.transpose((2, 0, 1))
		image = np.expand_dims(image, axis=0)
		image = image / 255.0
		image = torch.FloatTensor(image)

		image = image
		detections = self.model(image)[0]

		for i in range(0, len(detections["boxes"])):
			confidence = detections["scores"][i]

			if confidence > self.confidence:
				idx = int(detections["labels"][i])
				box = detections["boxes"][i].detach().cpu().numpy()
				(startX, startY, endX, endY) = box.astype("int")
				label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
				print("[INFO] {}".format(label))
		
		return detections

		

# IMAGE = "models/test/cats.jpg"
# model = "frcnn-resnet"
# COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
# model = MODELS[model](pretrained=True, progress=True,
# 	num_classes=len(CLASSES), pretrained_backbone=True).to(DEVICE)
# model.eval()

# image = cv2.imread(IMAGE)
# orig = image.copy()

# image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# image = image.transpose((2, 0, 1))

# image = np.expand_dims(image, axis=0)
# image = image / 255.0
# image = torch.FloatTensor(image)

# image = image.to(DEVICE)
# detections = model(image)[0]

# for i in range(0, len(detections["boxes"])):
# 	confidence = detections["scores"][i]
# 	if confidence > 0.5:

# 		idx = int(detections["labels"][i])
# 		box = detections["boxes"][i].detach().cpu().numpy()
# 		(startX, startY, endX, endY) = box.astype("int")
# 		label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
# 		print("[INFO] {}".format(label))
# 		print(detections["boxes"][i])

# 		cv2.rectangle(orig, (startX, startY), (endX, endY), COLORS[idx], 2)
# 		y = startY - 15 if startY - 15 > 15 else startY + 15
# 		cv2.putText(orig, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

# cv2.imshow("Output", orig)
# cv2.waitKey(0)