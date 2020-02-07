try:
    from pygame import mixer

except ModuleNotFoundError:
    pass

finally:
    import sys


class SoundLoader(object):

    """
    Classe para carregar e reproduzir sons.
    """

    __mixer = False


    def __init__(self, buffer = 1024):

        if "pygame" in sys.modules:
            mixer.init(buffer = buffer)
            self.__mixer = True


    def pause(self):

        if self.__mixer:
            self.__mixer.music.pause()


    def play(self, filename: str):
        
        if self.__mixer:
            mixer.music.load(filename)
            mixer.music.play()


    def stop(self):

        if self.__mixer:
            mixer.music.stop()