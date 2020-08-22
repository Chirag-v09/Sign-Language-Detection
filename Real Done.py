# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 20:16:41 2020

@author: Chirag
"""

# import the necessary packages
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import cv2
import imutils

bring_model = tf.keras.models.load_model("sld_model.h5")

def get_alpha(val):
    names = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5,'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10, 'L': 11, 'M': 12, 'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24, 'Z': 25, 'DEL': 26, 'NOTHING': 27, 'SPACE': 28}
    for key, value in names.items():
         if val == value:
             return key 
  
    return "key doesn't exist"

i = 0
j = 0
b_c = (255, 255, 255)
def con(image):
    global i
    global j
    global b_c
    global im
    
    i = i + 1
    
    image = cv2.GaussianBlur(image, (5, 5), 0)
    
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    lower_skin = np.array([0, 58, 30], dtype = np.uint8)
    upper_skin = np.array([33, 255, 255], dtype = np.uint8)
    
    mask = cv2.inRange(hsv, lower_skin, upper_skin)
    
    mask = cv2.erode(mask, None, iterations = 1)
    mask = cv2.dilate(mask, None, iterations = 9)
    
    cnts = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    cnts = imutils.grab_contours(cnts)
    
    if cnts:
        c = max(cnts, key=cv2.contourArea)
    else:
        return 0, 0, 0
    
    extLeft = tuple(c[c[:, :, 0].argmin()][0])
    extRight = tuple(c[c[:, :, 0].argmax()][0])
    extTop = tuple(c[c[:, :, 1].argmin()][0])
    extBot = tuple(c[c[:, :, 1].argmax()][0])
    
    image = im
    
    et = extTop[1] - 10
    el = extLeft[0] - 10
    er = extRight[0] + 10
    eb = extBot[1] + 10
    
    if(el < 0):
        el = 0
    if(et < 0):
        et = 0
    if(er > image.shape[1]):
        er = image.shape[1]
    if(eb > image.shape[0]):
        eb = image.shape[0]
    
    
    if i % 2 == 0:
        j = j + 1
        if j % 3 == 0:
            b_c = (0, 0, 255)
        if j % 3 == 1:
            b_c = (0, 255, 0)
        if j % 3 == 2:
            b_c = (255, 0, 0)
    
    image = cv2.rectangle(image, (el, et), (er, eb), b_c, 3)
    pre_image = image[et:eb, el:er]
    return image, mask, pre_image


string = []
string_text = ''
try:
    cap = cv2.VideoCapture(0)
    while(cap.isOpened()):
        ret, frame = cap.read()
        im = frame
        im2 = frame
        
        im2 = cv2.resize(im2, (224, 224), interpolation = cv2.INTER_AREA) / 255.0
        y_pred = bring_model.predict(im2.reshape((1, ) + im2.shape))
        
        frame1, mask, pre_image = con(frame)
        
        if not isinstance(frame1, np.ndarray):
            pre_image = frame
            frame1 = frame
        
        frame = frame1
        
        put_image = cv2.resize(pre_image, (70, 70))
        frame[0:70, 0:70] = put_image
        
        frame = cv2.line(frame, (0, 0), (70, 0), (255, 255, 255), 2)
        frame = cv2.line(frame, (0, 0), (0, 70), (255, 255, 255), 2)
        frame = cv2.line(frame, (70, 0), (70, 70), (255, 255, 255), 2)
        frame = cv2.line(frame, (0, 70), (70, 70), (255, 255, 255), 2)
        
        val = np.argmax(y_pred)
        Alphabet_pred = get_alpha(val)
        font = cv2.FONT_HERSHEY_COMPLEX
        
        if(Alphabet_pred != 'NOTHING' and Alphabet_pred != 'DEL' and Alphabet_pred != 'SPACE'):
            string.append(Alphabet_pred)
            string_text = ''.join(string)
        if(Alphabet_pred == 'DEL'):
            if (string):
                string = string[:-1]
                string_text = ''.join(string)
        if(Alphabet_pred == 'SPACE'):
            string.append(" ")
            string_text = ''.join(string)
        
        put_string = ''
        if len(string_text) > 15:
            put_string = '...' + string_text[-15: ]
        else:
            put_string = string_text
        
        alp_image = np.zeros((150, 640, 3), np.uint8)
        alp_image = cv2.putText(alp_image, Alphabet_pred, (20, 100), font, 3, (255, 255, 255), 5)
        alp_image = cv2.putText(alp_image, put_string, (20, 140), font, 1, (255, 255, 255), 1)
        #frame = cv2.putText(frame, Alphabet_pred, (10, 460), font, 2, (255, 255, 255), 5)
        
        res = np.concatenate((frame, alp_image), axis = 0)
        frame = cv2.line(res, (0, 480), (640, 480), (255, 255, 255), 3)
        cv2.imshow("Image", res)
        #cv2.imshow("Alphabet", alp_image)
        #cv2.imshow("Image1", put_image)
        cv2.imshow("Image2", mask)
        #cv2.imshow("hello", im)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    
    cap.release()
    cv2.destroyAllWindows()
