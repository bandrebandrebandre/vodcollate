import audalign as ad
import sys
import os
from renders import *


def collate(dir):

    try:
        os.mkdir(dir + '/audalign')
        offsets = align(dir)
    except FileExistsError:
        pass

    try:
        os.mkdir(dir + '/trim')
        largest_offset = 0

        for fn in offsets.keys():
            if offsets[fn] > largest_offset:
                largest_offset = offsets[fn]

        contents = [dir + '/' + f for f in os.listdir(dir) if (os.path.isfile(dir + '/' + f) and f != '.DS_Store')]

        for c in contents:
            fn = c.split('/')[-1]
            trim_timecode = largest_offset - offsets[fn]
            front_trim(c, dir + '/trim/' + fn, trim_timecode)

        front_trim(dir + '/audalign/total.wav', dir + '/trim/syncced_total.wav', largest_offset)
    except FileExistsError:
        pass


    try:
        os.mkdir(dir + '/hstack')
        if len(contents) == 2:
            run_hstack(dir + '/trim/' + contents[0].split('/')[-1], dir + '/trim/' + contents[1].split('/')[-1], dir + '/hstack/horizontally_stacked.mov'), 
    except FileExistsError:
        pass


    try:
        os.mkdir(dir + '/av_map')
        av_map(dir + '/hstack/horizontally_stacked.mov', dir + '/trim/syncced_total.wav', dir + '/av_map/hstack_ad_audio.mov')
    except FileExistsError:
        pass

if __name__ == "__main__":
    collate(sys.argv[1])
