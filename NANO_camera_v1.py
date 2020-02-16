#!/usr/bin/python
#
# Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#

# This solution utilises the original Python example from NVidia Git repo
# at https://github.com/dusty-nv/jetson-inference/blob/master/python/examples/imagenet-camera.py

# -----------------------------------------------------------
# Editor: Laziz Turakulov
# Edition dates: 01/01/2020 - 17/02/2020
# This code is now enhanced by the custom ML model saved from
# Google's Teachable Machine Web site at https://teachablemachine.withgoogle.com
# It's trained to recognise Rubik Cube and can be easily replaced by another model
# -----------------------------------------------------------

import tensorflow as tf
import numpy as np
import jetson.utils as jsu
from azure.iot.device import IoTHubDeviceClient, Message

# My constants
CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720
CAMERA_TYPE = "/dev/video0"
IMAGE_WIDTH = 124
IMAGE_HEIGHT = 124
LAZIZ_LABELS = ["ALARM: WRONG PUZZLE !!", "Rubik Cube", "I cannot find any puzzles ?!"]
AZURE_IOTHUB = "<IOTHUB_CONNECTION_STRING>"
AZURE_MSG = '{{"conf_index": {conf_index}, "confidence": {confidence}, "conf_min": 0, "conf_max": 1}}'

# Function to convert RGBA to RGB, published on Stackoverflow by Feng Wang
# https://stackoverflow.com/questions/50331463/convert-rgba-to-rgb-in-python
def rgba2rgb(rgba, background=(255,255,255)):
    row, col, ch = rgba.shape
    if ch == 3:
        return rgba
    assert ch == 4, "RGBA image has 4 channels"
    rgb = np.zeros((row, col, 3), dtype='float32')
    r, g, b, a = rgba[:,:,0], rgba[:,:,1], rgba[:,:,2], rgba[:,:,3]
    a = np.asarray(a, dtype='float32') / 255.0
    R, G, B = background
    rgb[:,:,0] = r * a + (1.0 - a) * R
    rgb[:,:,1] = g * a + (1.0 - a) * G
    rgb[:,:,2] = b * a + (1.0 - a) * B
    return np.asarray(rgb, dtype="uint8")

# Load savedmodel from the Google's Teachable Machine Web site
saved_model = tf.keras.models.load_model("savedmodel")
nano_model = saved_model.signatures["serving_default"]

# Create the camera and display
font = jsu.cudaFont()
camera = jsu.gstCamera(CAMERA_WIDTH, CAMERA_HEIGHT, CAMERA_TYPE)
display = jsu.glDisplay()

# Establish connectivity with Azure IoT hub
iot_client = IoTHubDeviceClient.create_from_connection_string(AZURE_IOTHUB)
iot_client.connect()

# Process frames and recognise objects until user exits
while display.IsOpen():
    # Capture the image
    img, width, height = camera.CaptureRGBA(zeroCopy=1)

    # Resize the image to the ML input requirements
    nano_image = rgba2rgb(jsu.cudaToNumpy(img, width, height, 4)) # Convert PyCapsule into NP array
    nano_image = tf.image.resize_with_pad(nano_image, IMAGE_HEIGHT, IMAGE_WIDTH)
    nano_image = np.expand_dims(nano_image, axis=0)

    # Classify the image
    prediction = nano_model(tf.constant(nano_image, dtype=float))["sequential_3"].numpy()

    # Find the prediction confidence and the object description
    confidence = max(prediction[0])
    conf_index = np.argmax(prediction[0])
    class_desc = LAZIZ_LABELS[conf_index]

    # Sending messages to Azure IoT Hub
    msg_formatted = AZURE_MSG.format(conf_index=conf_index, confidence=confidence)
    msg = Message(msg_formatted)
    print("Sending message: {}".format(msg))
    iot_client.send_message(msg)
    print("Message submitted to Azure IoT Hub")

    # Overlay the result on the image	
    font.OverlayText(img, width, height, "{:05.2f}% {:s}".format(confidence * 100, class_desc), 5, 5, font.White, font.Gray40)

    # Render the image
    display.RenderOnce(img, width, height)

    # Update the title bar
    display.SetTitle("Laziz's submission to NVidia's Hackster challenge")

# Disconnect Azure IoT hub
iot_client.disconnect()