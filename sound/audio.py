from pygame import mixer
# from mutagen.mp3 import MP3
import mutagen


class Audio:
    def __init__(self):
        mixer.init()
        pass

    @staticmethod
    def play_sound(path, runWhilePlaying=None):
        mixer.music.load(path)
        mixer.music.play()

        if runWhilePlaying:
            while mixer.music.get_busy():
                runWhilePlaying()

    @staticmethod
    def stop_sound():
        mixer.music.stop()

    @staticmethod
    def get_sound_length(path):
        audio = mutagen.File(path)
        return audio.info.length
