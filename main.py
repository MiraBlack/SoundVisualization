import argparse
import sys
import random

import ffmpeg

def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--audiofile', type=str, help="Path to the audio file", required = True)
    parser.add_argument('--gif', type=str, help="Path to the background gif file", required = True)
    parser.add_argument('--n', type=int, help='The number of seconds after which the color changes', required = True)
    return parser

def get_duration(audio_name):
    probe = ffmpeg.probe(audio_name)
    audio_duration = probe["streams"][0]["duration"]
    return audio_duration

def cut_audiostream(duration_of_cuts, audiostream, audio_duration): #cuts audiostream into equal parts 
    audiocuts = []
    start = 0

    for i in range(0, int(float(audio_duration)//duration_of_cuts)+1):
        cut = ffmpeg.filter(audiostream, "atrim", start=start, duration=duration_of_cuts).filter('asetpts', 'PTS-STARTPTS')
        audiocuts.append(cut)
        start += duration_of_cuts 

    #add last part, if any
    last_cut = ffmpeg.filter(audiostream, "atrim", start=start+duration_of_cuts, duration=float(audio_duration)-start+duration_of_cuts).filter('asetpts', 'PTS-STARTPTS')    
    audiocuts.append(last_cut) 
    return audiocuts

def create_wave(audio, color):
    return ffmpeg.filter(audio, "showwaves",  s="1600x300", colors=color, mode = 'line', scale = 'lin', draw='full')

def create_multiwaves(list_of_audiocuts): #creates multicolorful waves (with random color) from audiocuts
        waves = []

        for i in range(len(list_of_audiocuts)):
            color = "#"+''.join(random.sample('0123456789ABCDEF', 6))
            wave = create_wave(audiocuts[i], color)
            waves.append(wave)
            
        return waves


def create_video(multiwaves, background): #creates final audiowave, combines with background and return video file for output
    final_audiowave = ffmpeg.concat(*multiwaves, v=1, a=0)
    output_video = ffmpeg.overlay(background, final_audiowave, x=0, y=550,  shortest = 1).filter('fps',fps=25)
    return output_video
     

def run_video_with_audio(video,audio):
    ffmpeg.output(video, audio, 'output_video.mp4', s='1280x720').run(overwrite_output=True)


if __name__ == '__main__':
    parser = createParser()
    media_options = parser.parse_args(sys.argv[1:])

    audio = ffmpeg.input(media_options.audiofile)
    background = ffmpeg.input(media_options.gif, ignore_loop=0)

    audio_duration = get_duration(media_options.audiofile)
    audiocuts = cut_audiostream(media_options.n, audio, audio_duration)
    multiwaves = create_multiwaves(audiocuts)

    output_video = create_video(multiwaves, background)
    run_video_with_audio(output_video, audio)
    




 