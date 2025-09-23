import audalign as ad
import sys
import os
from renders import *
import numpy as np

def collate(dir):

    contents = [dir + '/' + f for f in os.listdir(dir) if (os.path.isfile(dir + '/' + f) and f != '.DS_Store')]

    try:
        print("AUDALIGN")
        os.mkdir(dir + '/audalign')
        offsets = align(dir)

        print("TRIM")
        os.mkdir(dir + '/trim')
        largest_offset = 0

        for fn in offsets.keys():
            if offsets[fn] > largest_offset:
                largest_offset = offsets[fn]

        for c in contents:
            fn = c.split('/')[-1]
            trim_timecode = largest_offset - offsets[fn]
            front_trim(c, dir + '/trim/' + fn, trim_timecode)

        front_trim(dir + '/audalign/total.wav', dir + '/trim/syncced_total.wav', largest_offset)
    except FileExistsError:
        pass

    mov_fps = []
    wav_fps = []
    print("CONTENTS " + str(contents))
    for fp in contents:
        if fp.split('.')[-1].lower() == 'mov':
            mov_fps.append(fp)
        if fp.split('.')[-1].lower() == 'wav':
            wav_fps.append(fp)

    try:
        print('HSTACK')
        os.mkdir(dir + '/hstack')
        print('LEN MOVFPS ' + str(mov_fps))
        if len(mov_fps) == 2:
            run_hstack(dir + '/trim/' + mov_fps[0].split('/')[-1], dir + '/trim/' + mov_fps[1].split('/')[-1], dir + '/hstack/horizontally_stacked.mov'), 
    except FileExistsError:
        pass

    try:
        print("APPLE CODEC")
        os.mkdir(dir + '/apple_codec')
        apple_codec(dir + '/hstack/horizontally_stacked.mov', dir + '/apple_codec/codec.mov')
    except FileExistsError:
        pass

    try:
        print("CROP TO SQUARE")
        os.mkdir(dir + "/crop")
        square_crop(dir + '/apple_codec/codec.mov', dir + '/crop/square.mov')
    except FileExistsError:
        pass

    try:
        print("AV_MAP")
        os.mkdir(dir + '/av_map')
        if len(wav_fps) == 1:
            av_map(dir + '/crop/square.mov', wav_fps[0], dir + '/av_map/square_mix_only.mov')
        av_map(dir + '/crop/square.mov',  dir + '/trim/syncced_total.wav', dir + '/av_map/square_total_audio.mov')
    except FileExistsError:
        pass

    try:
        print("CONCAT")
        os.mkdir(dir + '/concat')
        video_duration = get_duration(dir + '/trim/' + mov_fps[0].split('/')[-1])
        print("DURATION " + str(video_duration))

        trimmed_contents = [dir + '/' + f for f in os.listdir(dir + '/trim') if (os.path.isfile(dir + '/trim/' + f) and f != '.DS_Store')]
        print('TrIMMED CONTENTS ' + str(trimmed_contents))

        t_mov_fps, t_wav_fps = [], []
        for fp in trimmed_contents:
            if fp.split('.')[-1].lower() == 'mov':
                t_mov_fps.append(fp)
            if fp.split('.')[-1].lower() == 'wav':
                t_wav_fps.append(fp)

        cut_duration = .25

        with open('concat_demux.txt', 'a') as demux_file:
            for itr in np.arange(0, video_duration, cut_duration * len(t_mov_fps)):
                loop_itr = itr
                for fp in t_mov_fps:
                    demux_file.write(fp + '\n')
                    demux_file.write('inpoint ' + str(loop_itr) + '\n')
                    demux_file.write('outpoint ' + str(loop_itr + cut_duration) + '\n')
                    loop_itr = loop_itr + cut_duration

    except FileExistsError:
        pass


if __name__ == "__main__":
    collate(sys.argv[1])
