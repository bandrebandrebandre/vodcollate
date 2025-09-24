import audalign as ad
import sys
import os
from renders import *
import numpy as np

def get_av_contents(dir):
    av = [dir + '/' + f for f in os.listdir(dir) if (os.path.isfile(dir + '/' + f) and f != '.DS_Store')]
    mov_fps, wav_fps = [], []
    for fp in av:
        if fp.split('.')[-1].lower() == 'mov':
            mov_fps.append(fp)
        if fp.split('.')[-1].lower() == 'wav':
            wav_fps.append(fp)
    return av, mov_fps, wav_fps


def collate(dir):

    contents, mov_fps, wav_fps = get_av_contents(dir)

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

    trimmed_contents, t_mov_fps, t_wav_fps = get_av_contents(dir + '/collate/trim')

    try:
        print("APPLE CODEC")
        os.mkdir(dir + '/collate/apple_codec')
        for fp in t_mov_fps:
            apple_codec(fp, dir + '/collate/apple_codec/' + fp.split('/')[-1])
    except FileExistsError:
        pass



def hstack(dir):

    cont, mov_fps, wav_fps = get_av_contents(dir + '/collate/apple_codec')
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
        if len(wav_fps) == 1:
            av_map(dir + '/hstack/crop/square.mov', wav_fps[0], dir + '/hstack/av_map/square_mix_only.mov')
        av_map(dir + '/hstack/crop/square.mov',  dir + '/collate/trim/syncced_total.wav', dir + '/hstack/av_map/square_total_audio.mov')
    except FileExistsError:
        pass



def concat(dir):
    try:
        print("CONCAT")
        os.mkdir(dir + '/concat')
        contents, mov_fps, wav_fps = get_av_contents(dir + '/collate/apple_codec')

    except FileExistsError:
        pass

    video_duration = get_duration(mov_fps[0])
    print("DURATION " + str(video_duration))

    try:
        print("CONCAT")
        os.mkdir(dir + '/concat/snippets')

        cut_duration = 2
        for itr in np.arange(0, video_duration, cut_duration * len(mov_fps)):
            loop_itr = itr
            snippet_fps = []
            for fp in mov_fps:
                snippet_fps.append(dir + '/concat/snippets/' + fp.split('/')[-1] + str(loop_itr))
                trim(fp, loop_itr, loop_itr + cut_duration, snippet_fps[-1])
                loop_itr = loop_itr + cut_duration
                if len(snippet_fps) != 1:
                    concat(snippet_fps[-2], snippet_fps[-1])


    except FileExistsError:
        pass



if __name__ == "__main__":
    collate(sys.argv[1])
    hstack(sys.argv[1])
    concat(sys.argv[1])

