#!/bin/bash

conda activate p37_yolov5

LIBDIR=/home/openposeadmin/davidkylee/PycharmProjects/yolov5/yolov5
export PYTHONPATH=$LIBDIR:$PYTHONPATH

WORKDIR=/datadrive/davidkylee
LOGDIR=${WORKDIR}/log
WEIGHT=yolov5s.pt # yolov5s.pt / yolov5m.pt / yolov5l.pt / yolov5x.pt
IMGSIZE=640
DATA=/home/openposeadmin/davidkylee/PycharmProjects/yolov5/yolov5/data/diaper.yaml
EPOCHS=200
BATCH=16

mkdir -p ${WORKDIR}
mkdir -p ${LOGDIR}
cd ${WORKDIR}

time python3 -u -m train --img ${IMGSIZE} --batch ${BATCH} --epochs ${EPOCHS} --data ${DATA} --weights ${WEIGHT} &> ${LOGDIR}/yolotrain_`date +%Y%m%d%H%M%S`.log %
