import audalign as ad
import sys
import os

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


def front_trim(video, timecode):
    video_fn = video.split('/')[-1]
    args = [
    'ffmpeg',
    '-y',
    '-ss',
    str(timecode),
    '-i',
    AV_filepath,
    '-c:v',
    'copy',
    'trim' + str(timecode) + video_fn
    ]
    subprocess.run(args)

def collate(dir):
    offset = align(dir)
    print(str(offset))
    os.mkdir(dir + '/trim')
    contents = [f for f in os.listdir(dir) if (os.path.isfile(dir + '/' + f) and f != '.DS_Store')]
    print("HELLOOOOO")
    print(contents)

if __name__ == "__main__":
    collate(sys.argv[1])
