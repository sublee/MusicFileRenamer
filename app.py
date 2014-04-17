#!/usr/bin/python
# -*- coding: 949 -*-

import wx, wx.aui, os, sys
import wx.lib.mixins.listctrl as listmix
import wxaddons.sized_controls as sc
from os.path import basename, join
from MusicFile import MusicFile

import cStringIO

class Window(wx.Frame):
    files = []
    selected = None
    def __init__(self, name, size, icon = None):
        wx.Frame.__init__(self, None, title = name, size = size, style = wx.DEFAULT_FRAME_STYLE|wx.SUNKEN_BORDER|wx.CLIP_CHILDREN)
        self.SetMinSize(wx.Size(400, 300))
        if icon:
            self.SetIcon(wx.Icon(icon, wx.BITMAP_TYPE_PNG))
        self.mgr = wx.aui.AuiManager()
        self.mgr.SetManagedWindow(self)
        self.makeMenuBar()
        self.makeFileList()
        self.makeEditTags()
        self.makeToolBar()
        self.makeStatusBar()
        self.mgr.Update()
    def makeMenuBar(self):
        menus = {'file': wx.Menu(), 'edit': wx.Menu(), 'options': wx.Menu(), 'help': wx.Menu()}
        menus['file'].Append(wx.ID_OPEN, '&Open Files')
        menus['file'].AppendSeparator()
        menus['file'].Append(wx.ID_EXIT, 'E&xit')
        menus['help'].Append(wx.ID_ABOUT, '&About')
        bar = wx.MenuBar()
        bar.Append(menus['file'], '&File')
        bar.Append(menus['edit'], '&Edit')
        bar.Append(menus['options'], '&Options')
        bar.Append(menus['help'], '&Help')
        self.Bind(wx.EVT_MENU, self.OnClose, id = wx.ID_EXIT)
        self.SetMenuBar(bar)
    def makeToolBar(self):
        wx.ID_SAVEALL = wx.ID_ANY
        tb = wx.ToolBar(self, style = wx.TB_FLAT|wx.TB_NODIVIDER)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(tb, 0, wx.EXPAND)
        self.SetSizer(sizer)
        tb.SetToolBitmapSize((18, 18))

        tb.AddTool(wx.ID_OPEN + 10, wx.Bitmap('images/page_white.png', wx.BITMAP_TYPE_PNG), shortHelpString = 'Clear File List')
        tb.AddTool(wx.ID_OPEN, wx.Bitmap('images/add.png', wx.BITMAP_TYPE_PNG), shortHelpString = 'Add Files')
        tb.AddTool(wx.ID_SAVE, wx.Bitmap('images/disk.png', wx.BITMAP_TYPE_PNG), shortHelpString = 'Save')
        tb.AddTool(wx.ID_SAVEALL, wx.Bitmap('images/disk_multiple.png', wx.BITMAP_TYPE_PNG), shortHelpString = 'Save All')
        tb.AddSeparator()

#        global ID_TOGGLE_EDIT_TAGS
        ID_TOGGLE_EDIT_TAGS = wx.ID_NEW

        tb.AddTool(ID_TOGGLE_EDIT_TAGS, wx.Bitmap('images/tag_blue.png', wx.BITMAP_TYPE_PNG), isToggle = True, shortHelpString = 'Show Edit Tags')
        tb.AddTool(2, wx.Bitmap('images/world_go.png', wx.BITMAP_TYPE_PNG), shortHelpString = 'Auto Fill Tag')
        tb.ToggleTool(ID_TOGGLE_EDIT_TAGS, True)
        tb.AddSeparator()
        
        tb.AddTool(3, wx.Bitmap('images/wrench_orange.png', wx.BITMAP_TYPE_PNG), shortHelpString = 'Configure')
        tb.AddTool(4, wx.Bitmap('images/information.png', wx.BITMAP_TYPE_PNG), shortHelpString = 'Information')

        self.Bind(wx.EVT_TOOL, self.OnFileOpen, id = wx.ID_OPEN)
        self.Bind(wx.EVT_TOOL, self.OnToggleEditTags, id = ID_TOGGLE_EDIT_TAGS)
        
        tb.Realize()
        self.mgr.AddPane(
                tb, wx.aui.AuiPaneInfo().Name('toolbar').
                ToolbarPane().Top().LeftDockable(False).RightDockable(False))
        self.toolbar = tb
        del tb
    def makeFileList(self):
        fl = wx.ListCtrl(self, 500, style = wx.LC_REPORT|wx.BORDER_NONE)
        fl.InsertColumn(0, '#', wx.LIST_FORMAT_RIGHT)
        fl.InsertColumn(1, 'File Name')
        fl.InsertColumn(2, 'Artist')
        fl.InsertColumn(3, 'Title')
        fl.InsertColumn(4, 'Album')
        fl.SetColumnWidth(0, 30)
        fl.SetColumnWidth(3, 100)
        fl.SetColumnWidth(4, 150)
        
        self.mgr.AddPane(fl, wx.aui.AuiPaneInfo().Name("filelist").CenterPane())
        self.filelist = fl
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelect, self.filelist)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnDeselect, self.filelist)
    def makeEditTags(self):
        et = sc.SizedPanel(self, 501, size = (210, 500))
        tc = {}

        p = wx.Panel(et)
        p = wx.Panel(p, size = (150, 150), pos = (30, 5), style = wx.BORDER_SUNKEN)
        tc['image'] = wx.StaticBitmap(p, wx.ID_NEW, size = (150, 150))
        tc['image'].Hide()

        def TagCtrl(parent, label, icon):
            p = wx.Panel(parent)
            p.SetSizerProps(expand = True)
            wx.StaticBitmap(p, wx.ID_NEW, icon, (5, 5))
            wx.StaticText(p, wx.ID_NEW, label, (25, 5), style = wx.ST_NO_AUTORESIZE)
            return wx.TextCtrl(et, wx.ID_NEW)

        p = wx.Panel(et)
        p.SetSizerProps(expand = True)
        wx.StaticBitmap(p, wx.ID_NEW, wx.Bitmap('images/bullet_red.png', wx.BITMAP_TYPE_PNG), (5, 10))
        wx.StaticText(p, wx.ID_NEW, 'Track Number', (25, 10), style = wx.ST_NO_AUTORESIZE)
        p = wx.Panel(et)
        tc['track1'] = wx.TextCtrl(p, wx.ID_NEW, pos = (6, 5), size = (25, -1))
        tc['track1'].SetMaxLength(2)
        wx.StaticText(p, wx.ID_NEW, '/', (40, 8), style = wx.ST_NO_AUTORESIZE)
        tc['track2'] = wx.TextCtrl(p, wx.ID_NEW, pos = (53, 5), size = (25, -1))
        tc['track2'].SetMaxLength(2)

        tc['artist'] = TagCtrl(et, 'Artist', wx.Bitmap('images/user.png', wx.BITMAP_TYPE_PNG))
        tc['title'] = TagCtrl(et, 'Title', wx.Bitmap('images/music.png', wx.BITMAP_TYPE_PNG))
        tc['album'] = TagCtrl(et, 'Album', wx.Bitmap('images/cd.png', wx.BITMAP_TYPE_PNG))
        tc['year'] = TagCtrl(et, 'Year', wx.Bitmap('images/date.png', wx.BITMAP_TYPE_PNG))
        
#        self.Bind(wx.EVT_TEXT, self.OnEditArtist, tc['artist'])
#        self.Bind(wx.EVT_TEXT, self.OnEditTitle, tc['title'])
#        self.Bind(wx.EVT_TEXT, self.OnEditAlbum, tc['album'])
#        self.Bind(wx.EVT_TEXT, self.OnEditYear, tc['year'])
        
        map(lambda x: x.SetSizerProps(expand = True), [tc[x] for x in tc if x[:5] != 'track' and x != 'image'])
        self.mgr.AddPane(et, wx.aui.AuiPaneInfo().Name("edittags").Caption('Edit Tags').Right())
#        self.Bind(wx.aui.EVT_AUI_PANE_CLOSE, lambda e: self.toolbar.ToggleTool(ID_TOGGLE_EDIT_TAGS, False), et)
        self.tagctrls = tc
        self.edittags = et
    def makeStatusBar(self):
        self.status = self.CreateStatusBar(1, wx.ST_SIZEGRIP)
    def AddFile(self, path):
        if True:
            m = MusicFile(path)
            self.files.append(m)
            i = self.filelist.InsertStringItem(sys.maxint, str(m.track))
            self.filelist.SetStringItem(i, 1, basename(m.filename))
            self.filelist.SetStringItem(i, 2, m.artist)
            self.filelist.SetStringItem(i, 3, m.title)
            self.filelist.SetStringItem(i, 4, m.album)
        """except:
            md = wx.MessageDialog(self, "This format don't support ID3.",
                'Format Error',
                wx.OK | wx.ICON_ERROR
            )
            md.ShowModal()
            md.Destroy()"""
    def SelectFile(self, n):
        global m, a
        a = self
        self.selected = m = self.files[n]
#        print m.artist, m.album, m.title, m.year, m.comment
        if m.images:
            i = wx.BitmapFromImage(wx.ImageFromStream(cStringIO.StringIO(m.images[0].imageData)))
            self.tagctrls['image'].SetSize((i.GetWidth(), i.GetHeight()))
            self.tagctrls['image'].SetBitmap(i)
            self.tagctrls['image'].Show()
        if m.track[0]:
            self.tagctrls['track1'].SetValue(str(m.track[0]))
        if m.track[1]:
            self.tagctrls['track2'].SetValue(str(m.track[1]))
        if m.artist:
            self.tagctrls['artist'].SetValue(m.artist)
        if m.album:
            self.tagctrls['album'].SetValue(m.album)
        if m.title:
            self.tagctrls['title'].SetValue(m.title)
        if m.year:
            self.tagctrls['year'].SetValue(m.year)
    def OnClose(self, e):
        self.Close()
    def OnFileOpen(self, e):
        fd = wx.FileDialog(self,
            message = "Choose files",
            style = wx.OPEN|wx.MULTIPLE|wx.CHANGE_DIR,
            wildcard = "All music files|*.mp3;*.wav;*wma;*.ogg|"\
                       "Waveform (*.wav)|*.wav|"\
                       "Ogg (*.ogg)|*.ogg|"\
                       "Free Lossless Audio Codec (*.flac)|*.flac|"\
                       "RAW (*.raw)|*.raw|"\
                       "MPEG Layer-3 (*.mp3)|*.mp3|"\
                       "Global System for Mobile communications (*.gsm)|*.gsm|"\
                       "Advanced Audio Coding (*.aac)|*.aac|"\
                       "MPEG-4 Part 14 (*.m4a;*.mp4)|*.m4a;*.mp4|"\
                       "Windows Media Audio (*.wma)|*.wma|"\
                       "All files (*.*)|*.*"
        )
        if fd.ShowModal() == wx.ID_OK:
            map(self.AddFile, [x for x in fd.GetPaths() if x not in [y.filename for y in self.files]])
    def OnToggleEditTags(self, e):
        p = self.mgr.GetPane('edittags')
        if p.IsShown():
            p.Hide()
        else:
            p.Show()
        self.mgr.Update()
    def OnSelect(self, e):
        self.SelectFile(e.m_itemIndex)
    def OnDeselect(self, e):
        self.tagctrls['image'].Hide()
        map(lambda x: x.Clear(), [self.tagctrls[x] for x in self.tagctrls if x != 'image'])
    def OnEditArtist(self, e):
        self.selected.artist = e.GetString()

class Application(wx.App):
    Name = 'Music Manager'
    Size = (800, 600)
    Icon = 'images\\pill.png'
    Ver = '0.0.6'
    def OnInit(self):
        w = Window(self.Name, self.Size, self.Icon)
        w.Show()
        self.SetTopWindow(w)
        self.window = w
        return True

if __name__ == '__main__':
    app = Application()
    app.MainLoop()
