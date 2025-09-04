import subprocess
import audalign as ad
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
