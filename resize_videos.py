from ctypes import resize
from pathlib import Path
import moviepy.editor as mp
import threading
import time
import os
import argparse
import time
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('--size', default=256, type=int)
parser.add_argument('--path', default='k400', type=str)
parser.add_argument('--resized_path', default='k400_resized', type=str)
args = parser.parse_args()

TARGET_SIZE = args.size
MAIN_PATH = args.path
SPLITS = ['train', 'val', 'test', 'replacement/replacement_for_corrupted_k400']

print(f'Resize all mp4 videos in {MAIN_PATH} to the short edge size of {TARGET_SIZE}')


def resize_videos(video_list, split: str):
    total_num = len(video_list)
    for i, video_path in enumerate(tqdm(video_list)):
        progress = str(i) + '/' + str(total_num)
        
        if not os.path.isfile(video_path):
            print("%s-%s: %s" % (progress, time.ctime(time.time()), 'Cannot Find: ' + video_path))
            continue

        try:
            clip = mp.VideoFileClip(str(video_path), audio=False)
            w, h = clip.size
            if w > h:
                clip_resized = clip.resize(height=TARGET_SIZE)
            else:
                clip_resized = clip.resize(width=TARGET_SIZE)

            resized_video_path = Path(args.resized_path) / split / video_path.name
            clip_resized.write_videofile(str(resized_video_path), logger=None)
            clip_resized.close()
            clip.close()
            # print(f'{video_path} is resized to {clip_resized.size}')
            
        except Exception as e:
            print("%s-%s: %s Due to %s" % (time.ctime(time.time()), 'Fail to process: ' + video_path, e))


# iteratively search all mp4 videos within the current folder or sub-folders
def get_video_list(split: str):
    split_path = Path(args.path) / split
    resized_split_path = Path(args.resized_path) / split
    resized_split_path.mkdir(parents=True, exist_ok=True)
    video_list = []
    for file in split_path.glob('*.mp4'):
        video_list.append(file)
    # for file in os.listdir(main_path):
    #     if file.endswith('mp4'):
    #         video_list.append(os.path.join(main_path, file))
    #     elif os.path.isdir(os.path.join(main_path, file)):
    #         child_list = get_video_list(os.path.join(main_path, file))
    #         video_list = video_list + child_list
    #     else:
    #         pass
    return video_list


# get video lists
for split in SPLITS:
    video_list = get_video_list(split)
    resize_videos(video_list, split)

# resize all videos
# resize_videos(video_list)
print("Completed!")