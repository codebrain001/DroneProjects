
import detect_mask_video as fmd

from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import cv2
import os

import argparse
import os

# Importing the Tello Drone Library
from djitellopy import Tello

# Importing time package
import time

# Instatiating the Tello module
pkg = Tello()
# Connecting the drone to the python script after connecting to the Drone's WiFi
pkg.connect()

startCounter = 1
# 0: Flight & 1: Stationed

# Desired Image size
width = 320
height = 240


class Drone:
    def __init__(self, back_velocity, left_right_velocity, up_down_velocity, yaw_velocity, speed):
        self.back_velocity = back_velocity
        self.left_right_velocity = left_right_velocity
        self.up_down_velocity = up_down_velocity
        self.yaw_velocity = yaw_velocity
        self.speed = speed

        pkg.back_velocity = self.back_velocity
        pkg.left_right_velocity = self.left_right_velocity
        pkg.up_down_velocity = self.up_down_velocity
        pkg.yaw_velocity = self.yaw_velocity
        pkg.set_speed = self.speed

    def status(self):
        print(f" Current Battery: {pkg.get_battery()} %")
        print(f" Current Fly time: {pkg.get_flight_time()} s")
        print(f" Current Height: {pkg.get_height()} cm")
        print(f" Current Atmospheric Pressure: { pkg.get_barometer()} Pa")
        print(f" Current Temperature:{pkg.get_temperature()} K")
        print(f" Cureent Speed in the X-axis,Y-axis and Z-axis respectively: [{pkg.get_speed_x()}, {pkg.get_speed_y()}, {pkg.get_speed_z()}] cm/s")
        print(f" Current Yaw Velocity: {pkg.get_yaw()} degrees/s")
        print(f" Current State: { pkg.get_current_state()}")

    def camera_stream(self):
        pkg.streamoff()
        pkg.streamon()
        print("[INFO] starting video stream...")
        vs = VideoStream(src=0).start()
        time.sleep(2.0)


def detect_and_predict_mask(frame, faceNet, maskNet):
    # grab the dimensions of the frame and then construct a blob
    # from it
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300),
                                 (104.0, 177.0, 123.0))

    # pass the blob through the network and obtain the face detections
    faceNet.setInput(blob)
    detections = faceNet.forward()

    # initialize our list of faces, their corresponding locations,
    # and the list of predictions from our face mask network
    faces = []
    locs = []
    preds = []

    # loop over the detections
    for i in range(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with
        # the detection
        confidence = detections[0, 0, i, 2]

        # filter out weak detections by ensuring the confidence is
        # greater than the minimum confidence
        if confidence > args["confidence"]:
            # compute the (x, y)-coordinates of the bounding box for
            # the object
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # ensure the bounding boxes fall within the dimensions of
            # the frame
            (startX, startY) = (max(0, startX), max(0, startY))
            (endX, endY) = (min(w - 1, endX), min(h - 1, endY))

            # extract the face ROI, convert it from BGR to RGB channel
            # ordering, resize it to 224x224, and preprocess it
            face = frame[startY:endY, startX:endX]
            face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            face = cv2.resize(face, (224, 224))
            face = img_to_array(face)
            face = preprocess_input(face)

            # add the face and bounding boxes to their respective
            # lists
            faces.append(face)
            locs.append((startX, startY, endX, endY))

    # only make a predictions if at least one face was detected
    if len(faces) > 0:
        # for faster inference we'll make batch predictions on *all*
        # faces at the same time rather than one-by-one predictions
        # in the above `for` loop
        faces = np.array(faces, dtype="float32")
        preds = maskNet.predict(faces, batch_size=32)

    # return a 2-tuple of the face locations and their corresponding
    # locations
    return (locs, preds)

#construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--face", type=str,
	default="face_detector",
	help="path to face detector model directory")
ap.add_argument("-m", "--model", type=str,
	default="mask_detector.model",
	help="path to trained face mask detector model")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

# load our serialized face detector model from disk
print("[INFO] loading face detector model...")
prototxtPath = os.path.sep.join([args["face"], "deploy.prototxt"])
weightsPath = os.path.sep.join([args["face"],
	"res10_300x300_ssd_iter_140000.caffemodel"])
faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)

# load the face mask detector model from disk
print("[INFO] loading face mask detector model...")
maskNet = load_model(args["model"])





# initialize the video stream and allow the camera sensor to warm up
