import wx, os, sys, ID3
from os.path import basename, join
from MusicFile import MusicFile

DefaultPattern = '#(artist) - #(title)'

class Core:
    paths = []
    def getFiles(self):
        return self.paths
    def appendFile(self, path):
        return self.paths.append(path)
    def removeFile(self, n):
        del self.paths[n]
        return True
    def isUniqFile(self, path):
        return path not in self.paths

class Window(wx.Frame, Core):
    name = 'Music File Renamer'
    version = '0.0.3'
    images = 'images'
    icon = 'pill.png'
    size = (500, 545)
    def __init__(self):
        def setMenuBar():
            menus = {'file': wx.Menu(), 'help': wx.Menu()}
            menus['file'].Append(wx.ID_OPEN, '&Open Files')
            menus['file'].AppendSeparator()
            menus['file'].Append(wx.ID_EXIT, 'E&xit')
            menus['help'].Append(wx.ID_ABOUT, '&About')
            self.Bind(wx.EVT_MENU, self.onFileOpen, id = wx.ID_OPEN)
            self.Bind(wx.EVT_MENU, self.onClose, id = wx.ID_EXIT)
            self.Bind(wx.EVT_MENU, self.onAbout, id = wx.ID_ABOUT)
            bar = wx.MenuBar()
            bar.Append(menus['file'], '&File')
            bar.Append(menus['help'], '&Help')
            self.SetMenuBar(bar)
        def makeListBox(parent):
            self.listbox = wx.ListBox(parent, wx.ID_ANY, (0, 0), (494, 320), [], wx.LB_EXTENDED)
            buttons = {
                'add': wx.BitmapButton(parent, wx.ID_OPEN, wx.Bitmap(join(self.images, 'add.png'), wx.BITMAP_TYPE_PNG), (450, 325), style = wx.NO_BORDER),
                'del': wx.BitmapButton(parent, wx.ID_DELETE, wx.Bitmap(join(self.images, 'delete.png'), wx.BITMAP_TYPE_PNG), (470, 325), style = wx.NO_BORDER),
                }
            self.Bind(wx.EVT_LISTBOX, self.onSelect, self.listbox)
            self.Bind(wx.EVT_BUTTON, self.onFileOpen, buttons['add'])
            self.Bind(wx.EVT_BUTTON, self.onRemoveFile, buttons['del'])
        def makeController(parent):
            self.input = wx.TextCtrl(parent, 1, DefaultPattern, (10, 435), (380, -1))
            self.renameall = wx.Button(parent, wx.ID_OK, 'Rename All', (400, 435))
            self.Bind(wx.EVT_TEXT, lambda e: self.setStatus(MusicFile(self.getFiles()[self.listbox.GetSelections()[0]].encode('cp949')).getNewname(self.input.GetValue().encode('cp949'))), self.input)
            self.Bind(wx.EVT_BUTTON, self.onRenameAll, id = wx.ID_OK)
        def makeMusicInfo(parent):
            self.info = {'filename': wx.StaticText(parent, pos = (35, 325), size = (410, -1), style = wx.ST_NO_AUTORESIZE),
                         'artist': wx.StaticText(parent, pos = (35, 345), size = (410, -1), style = wx.ST_NO_AUTORESIZE),
                         'album': wx.StaticText(parent, pos = (35, 365), size = (410, -1), style = wx.ST_NO_AUTORESIZE),
                         'title': wx.StaticText(parent, pos = (35, 385), size = (410, -1), style = wx.ST_NO_AUTORESIZE),
                         'genre': wx.StaticText(parent, pos = (35, 405), size = (410, -1), style = wx.ST_NO_AUTORESIZE)}
            wx.StaticBitmap(parent, bitmap = wx.Bitmap(join(self.images, 'disk.png'), wx.BITMAP_TYPE_PNG), pos = (10, 325))
            wx.StaticBitmap(parent, bitmap = wx.Bitmap(join(self.images, 'user.png'), wx.BITMAP_TYPE_PNG), pos = (10, 345))
            wx.StaticBitmap(parent, bitmap = wx.Bitmap(join(self.images, 'cd.png'), wx.BITMAP_TYPE_PNG), pos = (10, 365))
            wx.StaticBitmap(parent, bitmap = wx.Bitmap(join(self.images, 'music.png'), wx.BITMAP_TYPE_PNG), pos = (10, 385))
            wx.StaticBitmap(parent, bitmap = wx.Bitmap(join(self.images, 'star.png'), wx.BITMAP_TYPE_PNG), pos = (10, 405))
        wx.Frame.__init__(self, None, -1, self.name, size = self.size, style = wx.MINIMIZE_BOX | wx.CLOSE_BOX | wx.SYSTEM_MENU | wx.CAPTION)
        self.panel = wx.Panel(self)
        self.panel.Layout()
        self.SetIcon(wx.Icon(join(self.images, self.icon), wx.BITMAP_TYPE_PNG))
        setMenuBar()
        makeListBox(self.panel)
        makeMusicInfo(self.panel)
        makeController(self.panel)
        self.SetStatusBar(wx.StatusBar(self, style = 0))
    def onFileOpen(self, e):
        wildcard = "All music files|*.mp3;*.wav;*wma;*.ogg|"\
                   "WAV (*.wav)|*.wav|"\
                   "OGG (*.ogg)|*.ogg|"\
                   "flac (*.wav)|*.wav|"\
                   "raw (*.wav)|*.wav|"\
                   "au (*.wav)|*.wav|"\
                   "MPEG Layer-3 (*.mp3)|*.mp3|"\
                   "gsm (*.wav)|*.wav|"\
                   "dct (*.wav)|*.wav|"\
                   "vox (*.wav)|*.wav|"\
                   "Advanced Audio Coding (*.wav)|*.wav|"\
                   "MPEG-4 (*.wav)|*.wav|"\
                   "Windows Media Audio (*.wav)|*.wav|"\
                   "All files (*.*)|*.*"
        dlg = wx.FileDialog(self,
            message = "Choose files",
            wildcard = wildcard,
            style = wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
            )
        if dlg.ShowModal() == wx.ID_OK:
            map(self.addFile, [x for x in dlg.GetPaths() if self.isUniqFile(x)])
    def onRemoveFile(self, e):
        for n in self.listbox.GetSelections()[::-1]:
            self.delFile(n)
    def onRenameAll(self, e):
        files = self.getFiles()
        for x in xrange(len(files)):
            m = MusicFile(files[x].encode('cp949'))
            m.rename(self.input.GetValue().encode('cp949'))
            self.changeFilename(x, m.filename)
    def onSelect(self, e):
        if len(self.listbox.GetSelections()) == 1:
            m = MusicFile(self.getFiles()[self.listbox.GetSelections()[0]].encode('cp949'))
#            map(lambda x: self.info[x].SetLabel(eval('m.' + x)), ['filename', 'artist', 'album', 'title', 'genre'])
            self.info['filename'].SetLabel(basename(m.filename))
            self.info['artist'].SetLabel(m.artist)
            self.info['album'].SetLabel(m.album)
            self.info['title'].SetLabel(m.title)
            self.info['genre'].SetLabel(m.genre)
            self.setStatus(m.getNewname(self.input.GetValue().encode('cp949')))
    def onClose(self, e):
        self.Close()
    def onAbout(self, e):
        self.Close()
    def addFile(self, path):
        self.listbox.Insert(basename(path), len(self.paths))
        self.appendFile(path)
    def delFile(self, n):
        self.listbox.Delete(n)
        self.removeFile(n)
    def changeFilename(self, n, name):
        self.listbox.Delete(n)
        self.listbox.Insert(basename(name), n)
        self.paths[n] = name
    def setStatus(self, txt):
        self.SetStatusText(txt)
        
class MenuBar(wx.MenuBar):
    def __init__(self, menus):
        wx.MenuBar.__init__(self)
        self.setMenus(menus)
    def setMenus(self, menus = {}):
        for menu in menus:
            currentmenu = wx.Menu()
            for action in menus[menu]:
                item = wx.MenuItem(currentmenu, wx.ID_ANY, action, menus[menu][action][1])
                self.Bind(wx.EVT_MENU, menus[menu][action][0], item)
                currentmenu.AppendItem(item)
            self.Append(currentmenu, menu)

class Application(wx.App):
    def OnInit(self):
        w = Window()
        w.Show()
        self.SetTopWindow(w)
        self.window = w
        return True

app = Application()
app.MainLoop()
