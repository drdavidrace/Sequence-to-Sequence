#!/usr/bin/env python
import os, sys
import subprocess
work_dir = os.getcwd()
vid_dir_name="OrigVideos"
speech_dir_name="Speech"
vid_dir = os.path.join(work_dir,vid_dir_name)
speech_dir = os.path.join(work_dir,speech_dir_name)
#Check Existence
if not os.path.isdir(vid_dir):
    print("The video directory must exist {}".format(vid_dir))
    print("\tPlease create the video directory.")
    sys.exit()
if not os.path.isdir(speech_dir):
    print("The speech directory must exist {}".format(speech_dir))
    os.mkdir(speech_dir)
if not os.path.isdir(speech_dir):
    print("There is a problem creating the speech dir.  Exiting!")
    sys.exit()
#Update name of video files
vid_list = os.listdir(vid_dir)
for old_video in vid_list:
    if " " in old_video:
        new_video = old_video.replace(" ","-")
        full_old_name = os.path.join(vid_dir,old_video)
        full_new_name = os.path.join(vid_dir,new_video)
        os.rename(full_old_name,full_new_name)
vid_list = os.listdir(vid_dir)
print("The video files:")
for video in vid_list:
    print(video)
#Clear the speech files
speech_list = os.listdir(speech_dir)
for old_speech in speech_list:
    full_speech_file = os.path.join(speech_dir,old_speech)
    os.remove(full_speech_file)
#Strip the audio from the video
vid_list = os.listdir(vid_dir)
for video in vid_list:
    in_video = os.path.join(vid_dir,video)
    part_file = os.path.splitext(video)[0]
    full_aud_name = ''.join([part_file,".flac"])
    audio_name = os.path.join(speech_dir,full_aud_name)
    #subprocess.run(["ffmpeg", " -i " + in_video + " -q:a 0 -map a  " + audio_name])
    #os.system("ffmpeg" + " -i " + in_video + " -q:a 0 -map a  " + audio_name)
    command = "ffmpeg" + " -i " + in_video + " -vn -sample_fmt s16 " + audio_name
    os.system(command)
    print(command)
