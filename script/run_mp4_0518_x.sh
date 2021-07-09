#!/bin/bash

conda activate p37_yolov5

LIBDIR=/home/openposeadmin/davidkylee/PycharmProjects/yolov5/yolov5
export PYTHONPATH=$LIBDIR:$PYTHONPATH

VIDEO_DIR=/datadrive/data-yilanvideo
WORKDIR=/datadrive/davidkylee
PROJECT=${WORKDIR}/HDyolov5
LOGDIR=${WORKDIR}/log
WEIGHT=yolov5x.pt # yolov5m.pt / yolov5l.pt / yolov5x.pt

mkdir -p ${WORKDIR}
mkdir -p ${PROJECT}
mkdir -p ${LOGDIR}
cd ${WORKDIR}
for s in ${VIDEO_DIR}/*.mp4
do
python3 -u -m detect --source $s --weights ${WEIGHT} --project ${PROJECT} --name `basename $s`_xmodel --persononly --skipfps 0 &> ${LOGDIR}/`basename $s`_xmodel.log
done