#!/bin/bash

conda activate p37_yolov5

LIBDIR=/home/openposeadmin/davidkylee/PycharmProjects/yolov5/yolov5
export PYTHONPATH=$LIBDIR:$PYTHONPATH

VIDEO_PATH=/datadrive/data-yilanvideo/dlink_2c-20210518-115922-1621310362.mp4
WORKDIR=/datadrive/davidkylee
PROJECT=${WORKDIR}/output_diaper
NAME=dlink_2c-20210518-115922-1621310362.mp4
LOGDIR=${WORKDIR}/log
WEIGHT=/datadrive/davidkylee/runs/train/exp/weights/best.pt # yolov5m.pt / yolov5l.pt / yolov5x.pt

mkdir -p ${WORKDIR}
mkdir -p ${PROJECT}
mkdir -p ${LOGDIR}
cd ${WORKDIR}

python3 -u -m detect --source ${VIDEO_PATH} --weights ${WEIGHT} --project ${PROJECT} --name ${NAME} --save-txt &> ${LOGDIR}/yolodetect_`date +%Y%m%d%H%M%S`.log
