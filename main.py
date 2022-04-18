#basic functionality: video/audio input, merging and output 

import ffmpeg

audio = ffmpeg.input("audio_files/Fallin' Down.mp3")
background = ffmpeg.input('background_gifs/background.gif', ignore_loop=0)

waves = ffmpeg.filter(audio, "showwaves",  s="1600x400", colors="#345c|#b0b8ff|#9d", mode = 'cline', scale = 'lin')
outv = ffmpeg.overlay(background, waves, shortest = 1)

ffmpeg.output(outv, audio, 'output_video.mp4').run(overwrite_output=True)
