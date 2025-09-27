import subprocess
import audalign as ad
import os

def align(dir, destination): # should be at least two files
    fingerprint_rec = ad.FingerprintRecognizer()
    fingerprint_rec.config.set_accuracy(3)
    result = ad.align(\
        dir,
        destination_path=destination,
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

def apple_codec(video_path, output_path):
    args = [
        'ffmpeg',
        '-i',
        video_path,
        '-pix_fmt',
        'yuv420p',
        output_path
    ]
    subprocess.run(args)

def square_crop(hstack_video_path, output_path):
    args = [
        'ffmpeg',
        '-i',
        hstack_video_path,
        '-vf',
        'crop=in_w-240:in_h',
        '-c:a',
        'copy', 
        output_path
    ]
    subprocess.run(args)

def get_duration(av_path):
    args = [
        'ffprobe -i ' + str(av_path) + 
        ' -show_entries format=duration -v quiet -of csv="p=0"',
    ]
    result = subprocess.run(args, shell=True, stdout=subprocess.PIPE)
    return float(str(result.stdout)[2:-4])

def concat_video(file_list, output_path):

    #ffmpeg -f data -i "concat:input1.ts|input2.ts|input3.ts" -map 0 -c copy -f data output.ts

    string_arg = 'concat:'
    for file in file_list:
        string_arg = string_arg + file
        if file != file_list[-1]:
            string_arg = string_arg + '|'
    print('STRING_ARG: ' + string_arg)

    args = [
        'ffmpeg',
        '-y',
        '-i',
        string_arg,
        '-c',
        'copy',
        output_path
    ]
    subprocess.run(args)


def trim(av_path, start, duration, output_path):
    args = [
        'ffmpeg',
        '-y',
        '-ss',
        str(start),
        '-i',
        av_path,
        '-t',
        str(duration),
        output_path
    ]
    subprocess.run(args)


def make_ts(video_path, output_path):
    args =[
        'ffmpeg',
        '-i',
        video_path,
        '-c',
        'copy',
        output_path + '.ts'
    ]
    subprocess.run(args)


