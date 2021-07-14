import argparse
import cv2
import os
import numpy as np
from utils.plots import colors, plot_one_box
from utils.general import xywh2xyxy


def main(flag):
    video_path = flag.video_path
    txt_dir = flag.txt_dir
    label_path = flag.label_path
    output_path = flag.output_path
    video_code = flag.video_code
    assert os.path.exists(video_path), 'video is not exist'
    assert os.path.exists(txt_dir), 'txt_dir is not exist'
    assert os.path.exists(label_path), 'label_txt is not exist'
    # video_path = 'C:\\work\proj\\auocare\output_HDplot\dlink_2c-20210518-115922-1621310362.mp4\dlink_2c-20210518-115922-1621310362.mp4'
    # txt_dir = ''
    # output_path = 'C:\\work\proj\\auocare\output_HDplot\dlink_2c-20210518-115922-1621310362.mp4\dlink_2c-20210518-115922-1621310362_diaper.mp4'

    label_txt = open(label_path)
    names = []
    for line in label_txt:
        names.append(line.replace('\n', ''))
    print(names)
    label_txt.close()

    video = cv2.VideoCapture(video_path)
    video_name = '.'.join(os.path.basename(video_path).split('.')[:-1])
    video_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    video_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    video_fps = video.get(cv2.CAP_PROP_FPS)
    print('video_name',video_name)
    print('video_width,video_height',video_width,video_height)
    print('fps',video_fps)

    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))
    output_video = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*video_code), video_fps, (video_width, video_height))

    frame_num = 0
    while True:
        success, frame = video.read()
        if not success:
            print('end in',frame_num)
            break
        txt_path = os.path.join(txt_dir,video_name+'_'+str(frame_num)+'.txt')
        if os.path.exists(txt_path):
            with open(txt_path, 'r') as f:
                for line in f.readlines():
                    print('frame_num',frame_num,'box',line.replace('\n', ''))
                    c, x, y , w, h= line.replace('\n', '').split(' ')
                    c = int(c)
                    x = int(float(x)*video_width)
                    w = int(float(w)*video_width)
                    y = int(float(y)*video_height)
                    h = int(float(h)*video_height)
                    xywh = np.array([x, y , w, h])
                    xywh = xywh.reshape([1,-1])
                    xyxy = xywh2xyxy(xywh)
                    xyxy = xyxy.reshape([-1])
                    label = names[c]
                    plot_one_box(xyxy, frame, label=label, color=colors(c+1, True), line_thickness=3)
        output_video.write(frame)
        frame_num += 1

    video.release()
    output_video.release()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--video_path', type=str, required=True, help='video_path')
    parser.add_argument('--txt_dir', type=str, required=True, help='txt_dir')
    parser.add_argument('--label_path', type=str, required=True, help='label_path')
    parser.add_argument('--output_path', type=str, required=True, help='output_path')
    parser.add_argument('--video_code', type=str, default='XVID', help='video_code')
    flag = parser.parse_args()
    main(flag)