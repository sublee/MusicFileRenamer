from eyeD3 import Tag
from os.path import basename, dirname
from chardet import detect
import re, os
Encoding = 'utf8'
class MusicFile:
    def __init__(self, filename = None):
        self.t = Tag()
        if filename:
            self.open(filename)
    def open(self, filename):
        if not isinstance(filename, unicode):
            filename = filename.decode(detect(filename)['encoding'])
        self.t.link(filename)
        self.filename = filename
    def __getattr__(self, name):
        if name == 'album':
            return self.t.getAlbum()
        elif name == 'artist':
            return self.t.getArtist()
        elif name == 'comment':
            return self.t.getComment()
        elif name == 'comments':
            return self.t.getComments()
        elif name == 'disc':
            return self.t.getDiscNum()
        elif name == 'genre':
            return self.t.getGenre()
        elif name == 'images':
            return self.t.getImages()
        elif name == 'lyric':
            return self.t.getLyrics()[0]
        elif name == 'playcount':
            return self.t.getPlayCount()
        elif name == 'publisher':
            return self.t.getPublisher()
        elif name == 'title':
            return self.t.getTitle()
        elif name == 'track':
            return self.t.getTrackNum()
        elif name == 'ver':
            return self.t.getVersionStr()
        elif name == 'year':
            return self.t.getYear()
        else:
            raise NameError
    def __repr__(self):
        return self.filename.encode(Encoding)
    def getNewname(self, pattern):
        if not isinstance(pattern, unicode):
            pattern = pattern.decode(detect(pattern)['encoding'])
        newname = pattern
        for match in re.compile('(#\\((title|album|artist|track|genre)(:(\\d*))?\\))').finditer(newname):
            newname = newname.replace(match.group(),
                                      self.__getattr__(match.groups()[1])
                                      [:int(match.groups()[3]) if match.groups()[3] else None]
                                      )
        return reduce(lambda s, x: s.replace(x, ''), [newname, '/', ':', '*', '?', '"', '<', '>', '|'])
    def rename(self, pattern):
        newname = self.getNewname()
        newpath = dirname(self.filename) + newname + '.' + self.filename.split('.')[-1] 
        os.rename(self.filename, newpath.encode(Encoding))
        self.open(newpath.encode(Encoding))
        return self
