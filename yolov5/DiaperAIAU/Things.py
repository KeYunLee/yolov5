import argparse
import cv2
import os
from utils.general import onerow2xyxy


def readyolov5txt2things(txt_path, names, width, height):
    activedetectthings = []
    with open(txt_path, 'r') as f:
        for line in f.readlines():
            # print('box', line.replace('\n', ''))
            c, xyxy = onerow2xyxy(line, width, height)
            # print('xyxy',xyxy)
            label = names[c]
            activedetectthing = {'label':label,'xyxy':xyxy}
            activedetectthings.append(activedetectthing)
    return activedetectthings

