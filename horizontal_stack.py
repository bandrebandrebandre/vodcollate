import audalign as ad
import sys
import os
import subprocess

def align(dir): # should be at least two files
    fingerprint_rec = ad.FingerprintRecognizer()
    fingerprint_rec.config.set_accuracy(3)
    result = ad.align(\
        dir,
        destination_path=dir,
        recognizer=fingerprint_rec
    )
    fns = os.listdir(dir)
    parsed_result = {}
    for fn in fns:
        if (fn != 'total.wav') and (fn != '.DS_Store'):
            parsed_result[fn] = result[fn]
    return parsed_result

def hstack(content_dir):
    args = ['ffmpeg']
    for file in os.listdir(dir):
        
    args.append('-i')
    args.append("total.wav")
    for v_path in video_filepaths:
        args.append('-i')
        args.append(v_path)
    args.append('-filter_complex')
    args.append('hstack')
    args.append('-map')
    args.append('0:a:0')
    args.append(out_path)
    result = subprocess.run(args)

def trim(video_path, timecode):
    video_fn = video_path.split('/')[-1]
    video_dir = '/'.join(video_path.split('/')[:-1])
    args = [
    'ffmpeg',
    '-y',
    '-ss',
    str(timecode),
    '-i',
    video_path,
    '-c:v',
    'copy',
    video_dir + '/trim-' + str(timecode) + '-' + video_fn
    ]
    subprocess.run(args)

def collate_av(dir):
    offsets = align(dir)
    print("HELLO")
    print(str(offsets))
    largest_offset = 0
    for fn in offsets.keys():
        if offsets[fn] > largest_offset:
            largest_offset = offsets[fn]
    for fn in offsets.keys():
        trim_timecode = largest_offset - offsets[fn]
        trim(dir + '/' + fn, trim_timecode)


def horizontal_stack(content_dir):
    collate_av(content_dir)
    

if __name__ == "__main__":
    horizontal_stack(sys.argv[1])
