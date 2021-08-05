import argparse
import cv2
import os
import numpy as np
import pandas as pd
from tqdm import tqdm

from utils.general import onerow2xyxy, classtxt2classlist
from utils.plots import plot_one_box, colors


def readtxtandplot(frame, names, txt_path, height, width, color_startindex=0):
    with open(txt_path, 'r') as f:
        for line in f.readlines():
            print('box', line.replace('\n', ''))
            c, xyxy = onerow2xyxy(line, width, height)
            label = names[c]
            plot_one_box(xyxy, frame, label=label, color=colors(color_startindex + c, True), line_thickness=3)


def main(flag):
    video_path = flag.video_path
    txt_dirs = flag.txt_dir.split(',')
    label_paths = flag.label_path.split(',')
    output_path = flag.output_path
    video_code = flag.video_code
    status_csv = flag.status_csv

    assert len(txt_dirs) == len(label_paths), print('len(txt_dirs)', len(txt_dirs), 'len(label_paths)',
                                                    len(label_paths))
    assert os.path.exists(video_path), 'video is not exist'
    assert all([os.path.exists(txt_dir) for txt_dir in txt_dirs]), 'txt_dir is not exist'
    assert all([os.path.exists(label_path) for label_path in label_paths]), 'label_txt is not exist'
    status_df = pd.read_csv(status_csv) if os.path.exists(status_csv) else None
    status_dflen = len(status_df) if status_df is not None else 0

    nameslist = [classtxt2classlist(label_path) for label_path in label_paths]
    num_list = [len(names) for names in nameslist]
    color_startindexs = np.array(num_list).cumsum() - num_list[0]

    print('nameslist', nameslist)
    print('num_list', num_list)
    print('color_startindexs', color_startindexs)

    video = cv2.VideoCapture(video_path)
    video_name = '.'.join(os.path.basename(video_path).split('.')[:-1])
    video_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    video_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    video_fps = video.get(cv2.CAP_PROP_FPS)
    print('video_name', video_name)
    print('video_width,video_height', video_width, video_height)
    print('fps', video_fps)

    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))
    output_video = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*video_code), video_fps,
                                   (video_width, video_height))

    frame_num = 0
    pbar = tqdm()
    while True:
        success, frame = video.read()
        if not success:
            print('end in', frame_num)
            break
        for index, (txt_dir, label_path) in enumerate(zip(txt_dirs, label_paths)):
            txt_path = os.path.join(txt_dir, video_name + '_' + str(frame_num) + '.txt')
            if os.path.exists(txt_path):
                readtxtandplot(frame, nameslist[index], txt_path, video_height, video_width,
                               color_startindex=color_startindexs[index])
        cv2.putText(frame, str(frame_num), (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1, cv2.LINE_AA)
        if status_df is not None and frame_num < status_dflen:
            cv2.putText(frame, status_df['status'][frame_num], (0, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1,
                        cv2.LINE_AA)
        output_video.write(frame)
        frame_num += 1
        pbar.update(1)

    pbar.close()
    video.release()
    output_video.release()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--video_path', type=str, required=True, help='video_path')
    parser.add_argument('--txt_dir', type=str, required=True, help='txt_dir, split by ","')
    parser.add_argument('--label_path', type=str, required=True, help='label_path, split by ","')
    parser.add_argument('--output_path', type=str, required=True, help='output_path')
    parser.add_argument('--video_code', type=str, default='mp4v', help='video_code')
    parser.add_argument('--status_csv', type=str, default='', help='status csv from ai')
    flag = parser.parse_args()
    print(flag)
    main(flag)
