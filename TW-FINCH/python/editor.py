import numpy as np
import argparse
import cv2
import os
import glob

from pandas import array

'''
Video editor for partitions
'''

def partition_video(partitions:np.ndarray, part_level, input_video:str, output_dir:str, max_videos=None):
    '''
    partitions - array of partitions structured as (N frames * M partition levels (each level has a partition number for the frame))
    part_level - level of partitions to use
    input_video - path to input video
    output-dir - path to directory for output videos 
    max_videos - max number of videos to make from partitions 
    '''

    for zippath in glob.iglob(os.path.join(output_dir, 'output*.mp4')):
        os.remove(zippath)
    
    try:
        partitions_ = partitions[:, part_level].flatten()
    except:
        partitions_ = partitions[:,].flatten()

    cur_part = -1
    num_videos = 0

    cap = cv2.VideoCapture(input_video)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out = None

    for i in range(len(partitions_)):

        if partitions_[i] != cur_part:
            if out is not None:
                out.release()
                num_videos += 1
                print(num_videos, i, cur_part)

                if num_videos == max_videos:
                    break

            cur_part = partitions_[i]

            fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            out = cv2.VideoWriter(os.path.join(output_dir, f'output{int(num_videos)}-' + os.path.basename(input_video)), fourcc, fps, (width, height))

        ret, frame = cap.read()

        out.write(frame)

    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--part', required=True, help='Specify the path to your partition csv file.')
    parser.add_argument('--vid', required=True, help='Specify the path to your video mp4 file.')
    parser.add_argument('--output', default=None, help='Specify the folder to write back the results.')
    parser.add_argument('--part_lvl', default=-1, help='Partition level for clustering (starts at 0)')
    args = parser.parse_args()

    partition_video(np.loadtxt(open(args.part, "rb"), delimiter=",", skiprows=1), int(args.part_lvl), args.vid, args.output, max_videos=10)



