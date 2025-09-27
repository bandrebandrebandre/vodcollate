import audalign as ad
import sys
import os
from renders import *
import numpy as np

def get_av_contents(dir):
    av = [dir + '/' + f for f in os.listdir(dir) if (os.path.isfile(dir + '/' + f) and f != '.DS_Store')]
    mov_fps, wav_fps, ts_fps = [], [], []
    for fp in av:
        if fp.split('.')[-1].lower() == 'mov':
            mov_fps.append(fp)
        if fp.split('.')[-1].lower() == 'wav':
            wav_fps.append(fp)
        if fp.split('.')[-1].lower() == 'ts':
            ts_fps.append(fp)
    return av, mov_fps, wav_fps, ts_fps

def four_pad(number):
    result = str(number)
    pad = len(str(number).split('.')[0])
    for itr in range(pad, 4):
        result = '0' + result
    return result


def collate(dir):

    contents, mov_fps, wav_fps, ts_fps= get_av_contents(dir)

    try:
        os.mkdir(dir + '/collate')
        print("AUDALIGN")
        os.mkdir(dir + '/collate/audalign')
        offsets = align(dir, dir + '/collate/audalign')

        print("TRIM")
        os.mkdir(dir + '/collate/trim')
        largest_offset = 0

        for fn in offsets.keys():
            if offsets[fn] > largest_offset:
                largest_offset = offsets[fn]
        print("OFFSETS: " + str(offsets))
        print("CONTENTS: " + str(contents))
        for c in contents:
            fn = c.split('/')[-1]
            trim_timecode = largest_offset - offsets[fn]
            front_trim(c, dir + '/collate/trim/' + fn, trim_timecode)

        front_trim(dir + '/collate/audalign/total.wav', dir + '/collate/trim/syncced_total.wav', largest_offset)
    except FileExistsError:
        pass

    trimmed_contents, t_mov_fps, t_wav_fps, ts_fps = get_av_contents(dir + '/collate/trim')

    try:
        print("APPLE CODEC")
        os.mkdir(dir + '/collate/apple_codec')
        for fp in t_mov_fps:
            apple_codec(fp, dir + '/collate/apple_codec/' + fp.split('/')[-1])
    except FileExistsError:
        pass



def hstack(dir):

    cont, mov_fps, wav_fps, ts_fps = get_av_contents(dir + '/collate/apple_codec')
    try:
        print('HSTACK')
        os.mkdir(dir + '/hstack')
        os.mkdir(dir + '/hstack/hstack')
        print('LEN MOVFPS ' + str(mov_fps))
        if len(mov_fps) == 2:
            run_hstack(dir + '/collate/apple_codec/' + mov_fps[0].split('/')[-1], dir + '/collate/apple_codec/' + mov_fps[1].split('/')[-1], dir + '/hstack/hstack/horizontally_stacked.mov'), 
    except FileExistsError:
        pass

    try:
        print("CROP TO SQUARE")
        os.mkdir(dir + "/hstack/crop")
        square_crop(dir + '/hstack/hstack/horizontally_stacked.mov', dir + '/hstack/crop/square.mov')
    except FileExistsError:
        pass

    try:
        print("AV_MAP")
        os.mkdir(dir + '/hstack/av_map')
        c, m, dir_wav, ts_fps = get_av_contents(dir)
        if len(dir_wav) == 1:
            av_map(dir + '/hstack/crop/square.mov', dir_wav[0], dir + '/hstack/av_map/square_mix_only.mov')
        av_map(dir + '/hstack/crop/square.mov',  dir + '/collate/trim/syncced_total.wav', dir + '/hstack/av_map/square_total_audio.mov')
    except FileExistsError:
        pass



def concat(dir):
    try:
        print("CONCAT")
        os.mkdir(dir + '/concat')
        contents, mov_fps, wav_fps, ts_fps = get_av_contents(dir + '/collate/apple_codec')

        video_duration = get_duration(mov_fps[0])
        print("DURATION " + str(video_duration))

        print("CONCAT")
        os.mkdir(dir + '/concat/snippets')
        os.mkdir(dir + '/concat/snippets/movs')
        os.mkdir(dir + '/concat/snippets/mpegs')

        cut_duration = 1
        concat_queue = []
        for itr in np.arange(0, video_duration - (cut_duration * 6), cut_duration * len(mov_fps)):
            loop_itr = itr
            for fp in mov_fps:
                mov_snip = dir + '/concat/snippets/movs/' + str(four_pad(loop_itr)) + '-' + fp.split('/')[-1]
                trim(fp, loop_itr, cut_duration, mov_snip)
                ts_snip =  dir + '/concat/snippets/mpegs/' + str(four_pad(loop_itr)) + '-' + fp.split('/')[-1]
                make_ts(mov_snip, ts_snip)
                loop_itr = loop_itr + cut_duration
                concat_queue.append(ts_snip + '.ts')

        concat_video(sorted(concat_queue), dir + '/concat/concat.ts')
    except FileExistsError:
        pass


    try:
        os.mkdir(dir + '/concat/codec')
        apple_codec(dir + '/concat/concat.ts', dir + '/concat/codec/concat.mov')

    except FileExistsError:
        pass


    try:
        os.mkdir(dir + '/concat/av_map')
        contents, mov_fps, wav_fps, ts_fps = get_av_contents(dir + '/collate/trim')
        for fp in wav_fps:
            av_map(dir + '/concat/codec/concat.mov', fp, dir + '/concat/av_map/' + fp.split('/')[-1].split('.')[-2] + '.mov')
    except FileExistsError:
        pass


if __name__ == "__main__":
    collate(sys.argv[1])
    hstack(sys.argv[1])
    concat(sys.argv[1])

