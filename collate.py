import audalign as ad
import sys
import os
from renders import *


def collate(dir):
    offsets = align(dir)
    print(str(offsets))

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


if __name__ == "__main__":
    collate(sys.argv[1])
