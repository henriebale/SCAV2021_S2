import os, sys, subprocess, shlex, re
from subprocess import call
def motion_vectors():
    os.system("ffmpeg -flags2 +export_mvs -i BBB_video_cut.mp4 -vf codecview=mv=pf+bf+bb BBB_motion_vectors.mp4")
    os.system("ffplay BBB_motion_vectors.mp4")


def create_container(filename):
    # extract audio mp3
    command1 = f"ffmpeg -i {filename} -ss 00:00:00 -t 00:01:00 -ac 2 -map a BBB_audio_mp3.mp3"
    # extract audio aac and lower bitrate
    command2 = f"ffmpeg -i {filename} -ss 00:00:00 -t 00:01:00 -ac 2 -b:a 32k -c:a aac -map a BBB_audio_aac.aac"
    # replace audio mp3
    command3 = f"ffmpeg -i {filename} -i BBB_audio_mp3.mp3 -ss 00:00:00 -t 00:01:00 -c:v copy -map 0:v:0 -map 1:a:0 BBB_mp3.mp4"
    # replace audio aac
    command4 = f"ffmpeg -i {filename} -i BBB_audio_aac.aac -ss 00:00:00 -t 00:01:00 -c:v copy -map 0:v:0 -map 1:a:0 BBB_aac.mp4"
    os.system(command1)
    os.system(command2)
    os.system(command3)
    os.system(command4)
    print(f"Playing the mp3 stereo version (closa window to continue)")
    os.system("ffplay BBB_mp3.mp4")
    print(f"Playing the aac w/lower bitrate audio version (closa window to continue)")
    os.system("ffplay BBB_aac.mp4")


# extract audio and video codec and find the broadcasting standard adequate
def get_standard(filename):
    # extract audio and video codec
    p1 = subprocess.Popen(
        f"ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 {filename}",
        stdout=subprocess.PIPE, shell=True)
    (vout, err) = p1.communicate()
    p2 = subprocess.Popen(
        f"ffprobe -v error -select_streams a:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 {filename}",
        stdout=subprocess.PIPE, shell=True)
    (aout, err) = p2.communicate()
    print("Broadcasting standards: ")
    std = 0
    # find the broadcasting standard adequate
    if (vout == b'h264\n' or vout == b'mpeg2video\n') and (
            aout == b'aac\n' or aout == b'mp1\n' or aout == b'mp2\n' or aout == b'mp3\n' or aout == b'ac3\n'):
        print("DVB")
        std += 1
    if (vout == b'h264\n' or vout == b'mpeg2video\n') and (aout == b'aac\n'):
        print("ISDB")
        std += 1
    if (vout == b'h264\n' or vout == b'mpeg2video\n') and (aout == b'ac3\n'):
        print("ATSC")
        std += 1
    if (vout == b'h264\n' or vout == b'mpeg2video\n') and (
            aout == b'aac\n' or aout == b'mp1\n' or aout == b'mp2\n' or aout == b'mp3\n' or aout == b'ac3\n'):
        print("ATSC")
        std += 1
    if std == 0:
        print("ERROR")


def put_subtitles(filename, subtitles):
    # replace audio and apply subtitles
    os.system(f"ffmpeg -i {filename} -i {subtitles} -ss 00:00:00 -t 00:01:00 -c copy -c:s mov_text subtitles.mp4")


class video:
    # initialize with the video codec h264 and the audio codec aac
    video_codec = "b'h264\n'"
    audio_codec = "b'aac\n'"

    # name is the filename os the mp4
    def __init__(self, name):
        self.name = name

    def get_codecs(self):
        p1 = subprocess.Popen(
            f"ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 {self.name}",
            stdout=subprocess.PIPE, shell=True)
        (self.video_codec, err) = p1.communicate()
        p2 = subprocess.Popen(
            f"ffprobe -v error -select_streams a:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 {self.name}",
            stdout=subprocess.PIPE, shell=True)
        (self.audio_codec, err) = p2.communicate()

    def get_standard(self):
        print("Broadcasting standards: ")
        std = 0
        if (self.video_codec == b'h264\n' or self.video_codec == b'mpeg2video\n') and (
                self.video_codec == b'aac\n' or self.video_codec == b'mp1\n' or self.video_codec == b'mp2\n' or self.video_codec == b'mp3\n' or self.video_codec == b'ac3\n'):
            print("DVB")
            std += 1
        if (self.video_codec == b'h264\n' or self.video_codec == b'mpeg2video\n') and (self.video_codec == b'aac\n'):
            print("ISDB")
            std += 1
        if (self.video_codec == b'h264\n' or self.video_codec == b'mpeg2video\n') and (self.video_codec == b'ac3\n'):
            print("ATSC")
            std += 1
        if (self.video_codec == b'h264\n' or self.video_codec == b'mpeg2video\n') and (
                self.video_codec == b'aac\n' or self.video_codec == b'mp1\n' or self.video_codec == b'mp2\n' or self.video_codec == b'mp3\n' or self.video_codec == b'ac3\n'):
            print("ATSC")
            std += 1
        if std == 0:
            print("ERROR")

    def create_container(self):
        command1 = f"ffmpeg -i {self.name} -ss 00:00:00 -t 00:01:00 -ac 1 -b:a 32k -map a BBB_audio_cut_mono.mp3"
        command2 = f"ffmpeg -i {self.name} -i BBB_audio_cut_mono.mp3 -i subtitles.srt -ss 00:00:00 -t 00:01:00  -c:v copy -c:a aac -c:s mov_text subtitles.mp4"
        os.system(command1)
        os.system(command2)

    def test_sandard(self):

        os.system(f"ffmpeg -i {self.name} -acodec mp3 test_mp3.mp4")
        print("test_mp3.mp4")
        get_standard("test_mp3.mp4")

        os.system(f"ffmpeg -i {self.name} -acodec ac3 test_ac3.mp4")
        print("test_mp3.mp4")
        get_standard("test_mp3.mp4")

        os.system(f"ffmpeg -i {self.name} -vcodec mpeg2video test_mpeg2.mp4")
        print("test_mpeg2.mp4")
        get_standard("test_mp3.mp4")


ex = "1"
while ex != "0":
    print("Exercice Nº (insert 0 to end)")
    ex = input()
    print(f"Exercise {ex} selected")

    if ex == "1":
        motion_vectors()

    elif ex == "2":
        create_container("BBB_video.mp4")

    elif ex == "3":
        print("Select file:")
        filename = input()
        get_standard(filename)

    elif ex == "4":
        put_subtitles("BBB_video.mp4", "subtitles.srt")

    elif ex == "5":
        v = video("BBB_video.mp4")
        v.create_container()
        v.get_codecs()
        v.get_standard()
        v.test_sandard()

    else:
        print(f"Exercise {ex} doesn't exiat")
