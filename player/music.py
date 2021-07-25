''' music.py
    control audiobook functionality
    dependency: pip install python-vlc
'''

from pathlib import Path

import vlc

import constants as c


class Music():
    '''functionality to play audiobooks

    keep track of audio and vlc capabilities
    retrieve and save info on last played book
    '''

    def __init__(self):
        # path to audiobook loaded as media
        self.lastbook_file = Path(c.LASTBOOK_PATH)

        # path of last audiobook played before shutdown
        self.current_path, self.current_book = self.readf_lastbook()

        # last audiobook played with its position at shutdown
        self.position = self.readf_position()

        # the objects needed for vlc to play media files
        self.mediaplayer = vlc.MediaPlayer()
        if Path(self.current_path, self.current_book).exists():
            self.media = vlc.Media(Path(self.current_path, self.current_book))
            self.mediaplayer.set_media(self.media)

    def readf_lastbook(self) -> Path:
        '''
            read the first line of the file in lastbook_path
            and return it
        '''
        path = Path(c.DEFAULT_AUDIO_PATH)
        if self.lastbook_file.exists():
            path = Path(self.lastbook_file.read_text())
            if path.suffix == '.m4a' or path.suffix == '.mp3':
                return path.parent, path.name
        return path, ""

    def writef_lastbook(self):
        '''
            write path to file in self.lastbook_path
        '''
        book = Path(self.current_book)
        if book.suffix == '.m4a' or book.suffix == '.mp3':
            path = Path(self.current_path, self.current_book)
            self.lastbook_file.write_text(str(path))

    def readf_position(self) -> [str, float]:
        '''
            read the saved position of the audiobook to play
        '''
        position = 0.0001
        filepath = Path(self.current_path, "position.txt")
        if filepath.exists():
            position = filepath.read_text()
        return float(position)

    def writef_position(self, position: float):
        '''
            write current position in audiobook to file
        '''
        if 0 < position < 0.99:
            Path(self.current_path, "position.txt").write_text(str(position))

    def play(self):
        '''
            toggle play and pause of media playback
        '''
        if self.mediaplayer.is_playing():
            self.mediaplayer.pause()
            self.position = self.mediaplayer.get_position()
        else:
            self.mediaplayer.play()
            self.mediaplayer.set_position(self.position)

    def louder(self):
        vol = self.mediaplayer.audio_get_volume()
        self.mediaplayer.audio_set_volume(vol+5)

    def quieter(self):
        vol = self.mediaplayer.audio_get_volume()
        self.mediaplayer.audio_set_volume(vol-5)

    def set_book(self, path: Path):
        # change the current audiobook for the player
        self.audiobook = path
        self.media = vlc.Media(path)
        self.mediaplayer.set_media(self.media)

    def get_bookname(self) -> Path:
        # get the audiobook name currently loaded by vlc
        path = Path(self.media.get_mrl())
        return path.name

    def get_bookpath(self) -> Path:
        # get the path of the audiobook
        path = Path(self.media.get_mrl())
        head = str(path.parent)
        if head.startswith("file:"):
            path = Path(head[len("file:"):])
        return path.resolve()

    def save_position(self):
        # save the position and name of current audiobook
        position = self.mediaplayer.get_position()
        self.writef_position(position)
