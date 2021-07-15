# yolov5
詳細yolov5請參考[這裡](https://github.com/KeYunLee/yolov5/tree/master/yolov5)或[yolov5官網](https://github.com/ultralytics/yolov5)

script使用範例在[script](https://github.com/KeYunLee/yolov5/tree/master/script)

## inference
* example code
```bash=
python detect.py --source 0  # webcam
                            file.jpg  # image 
                            file.mp4  # video
                            path/  # directory
                            path/*.jpg  # glob
                            'https://youtu.be/NUsoVlDFqZg'  # YouTube video
                            'rtsp://example.com/media.mp4'  # RTSP, RTMP, HTTP stream
```
* example script
```bash=
#!/bin/bash

conda activate p37_yolov5

LIBDIR=/home/openposeadmin/davidkylee/PycharmProjects/yolov5/yolov5
export PYTHONPATH=$LIBDIR:$PYTHONPATH

VIDEO_DIR=/datadrive/data-yilanvideo
WORKDIR=/datadrive/davidkylee
PROJECT=${WORKDIR}/HDyolov5
LOGDIR=${WORKDIR}/log
WEIGHT=yolov5s.pt # yolov5m.pt / yolov5l.pt / yolov5x.pt

mkdir -p ${WORKDIR}
mkdir -p ${PROJECT}
mkdir -p ${LOGDIR}
cd ${WORKDIR}
for s in ${VIDEO_DIR}/*.mp4
do
python3 -u -m detect --source $s --weights ${WEIGHT} --project ${PROJECT} --name `basename $s` --persononly --skipfps 0 &> ${LOGDIR}/`basename $s`.log
done
```
## train
* 訓練資料夾結構
```bash=
| ---- yolov5
| ---- xxx
|       | --- images
|                |  --- train
|                         | --- train_1.jpg
|                         | --- ...
|                         | --- train_n.jpg 
|                |  --- val
|                         | --- val_1.jpg 
|                         | --- ...
|                         | --- val_n.jpg 
|       | --- labels 
|                |  --- train
|                         | --- train_1.txt
|                         | --- ...
|                         | --- train_n.txt
|                |  --- val
|                         | --- val_1.txt
|                         | --- ...
|                         | --- val_n.txt
```
沒有obj的照片, 不需要txt檔
* 執行訓練
```bash=
# Train YOLOv5s on COCO128 for 200 epochs
python train.py --img 640 --batch 16 --epochs 200 --data coco128.yaml --weights yolov5s.pt --hyp data/hyps/hyp.finetune.yaml
```
