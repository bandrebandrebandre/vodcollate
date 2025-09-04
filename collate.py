import audalign as ad
import sys
import os
import subprocess

def align(dir): # should be at least two files
    fingerprint_rec = ad.FingerprintRecognizer()
    fingerprint_rec.config.set_accuracy(3)
    os.mkdir(dir + '/audalign')
    result = ad.align(\
        dir,
        destination_path=dir + '/audalign',
        recognizer=fingerprint_rec
    )
    fns = os.listdir(dir)
    parsed_result = {}
    for fn in fns:
        if (fn != 'total.wav') and (fn != '.DS_Store') and os.path.isfile(dir + '/' + fn):
            parsed_result[fn] = result[fn]
    return parsed_result


def front_trim(video_path, output_path, timecode):
    args = [
    'ffmpeg',
    '-y',
    '-ss',
    str(timecode),
    '-i',
    video_path,
    '-c:v',
    'copy',
    output_path
    ]
    subprocess.run(args)

def collate(dir):
    offsets = align(dir)
    print(str(offsets))

    os.mkdir(dir + '/trim')
    largest_offset = 0

    for fn in offsets.keys():
        if offsets[fn] > largest_offset:
            largest_offset = offsets[fn]

    contents = [dir + '/' + f for f in os.listdir(dir) if (os.path.isfile(dir + '/' + f) and f != '.DS_Store')]
    print("HELLOLHELLLO")
    print(contents)

    print("BYEBYE")
    for c in contents:
        fn = c.split('/')[-1]
        trim_timecode = largest_offset - offsets[fn]
        front_trim(c, dir + '/trim/' + fn, trim_timecode)


    print("HELLOOOOO")

if __name__ == "__main__":
    collate(sys.argv[1])
