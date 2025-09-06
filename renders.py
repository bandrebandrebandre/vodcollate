import subprocess
import audalign as ad
import os

def align(dir): # should be at least two files
    fingerprint_rec = ad.FingerprintRecognizer()
    fingerprint_rec.config.set_accuracy(3)
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


def run_hstack(video_path1, video_path2, output_path):
    args = [
        'ffmpeg',
        '-i',
        video_path1,
        '-i',
        video_path2,
        '-filter_complex',
        'hstack',
        output_path
    ]
    subprocess.run(args)

def av_map(video_path, audio_path, output_path):
    args = [
        'ffmpeg',
        '-i',
        video_path,
        '-i',
        audio_path,
        '-c:v',
        'copy',
        '-c:a',
        'aac',
        '-map',
        '0:v:0',
        '-map',
        '1:a:0',
        output_path
    ]
    subprocess.run(args)
