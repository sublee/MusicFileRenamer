import wx
import os, sys

class window(wx.Frame):
    opened_files = []
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'Music File Renamer', size = (500, 600))
        self.SetIcon(wx.Icon("D:\\x.ico", wx.BITMAP_TYPE_ICO))
        self.panel = wx.Panel(self)
        self._make_menu_bar()
        self._make_file_list()
        self.panel.Layout()

    def _make_menu_bar(self):
        #File
        file_menu = wx.Menu()
        file_menu.Append(wx.ID_OPEN, '&Open Files')
        file_menu.AppendSeparator()
        file_menu.Append(wx.ID_EXIT, 'E&xit')

        #Help
        help_menu = wx.Menu()
        help_menu.Append(wx.ID_ABOUT, '&About Application')
        
        wx.EVT_MENU(self, wx.ID_OPEN, self.OnOpenFiles)
        wx.EVT_MENU(self, wx.ID_EXIT, self.OnExit)
        wx.EVT_MENU(self, wx.ID_ABOUT, self.OnAbout)

        menu_bar = wx.MenuBar()
        menu_bar.Append(file_menu, '&File')
        menu_bar.Append(help_menu, '&Help')
        self.SetMenuBar(menu_bar)

    def _make_file_list(self):
        self.file_list = wx.ListBox(self.panel, -1, (0, 0), (350, 400), self.opened_files, wx.LB_SINGLE)
        plus, minus = wx.Button(self.panel, wx.ID_OPEN, '+', (296, 405), (24, 24)), wx.Button(self.panel, -1, '-', (326, 405), (24, 24))
        wx.EVT_BUTTON(self, wx.ID_OPEN, self.OnOpenFiles)

    def OnOpenFiles(self, e):
        wildcard = "All music files|*.mp3;*.wav;*wma;*.ogg|"\
                   "MPEG Layer-3 (*.mp3)|*mp3|"\
                   "All files (*.*)|*.*"
        dlg = wx.FileDialog(self,
            message = "Choose a file",
            wildcard = wildcard,
            style = wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
            )

        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            for path in paths:
                if path not in self.opened_files:
                    self.opened_files.append(path)
                    self.file_list.Insert(path, len(self.opened_files) - 1)

        # Compare this with the debug above; did we change working dirs?
        dlg.Destroy()
        
    def OnAbout(self, e):
        info = wx.AboutDialogInfo()
        info.Name = 'Music File Renamer'
        info.Version = '0.0.1'
        info.Description = ''
        info.WebSite = ('http://heungsub.net/', 'Heungsub\'s home page')
        wx.AboutBox(info)

    def OnExit(self, e):
        self.Close(True)

class app(wx.App):
    def OnInit(self):
        w = window()
        w.Show()
        self.SetTopWindow(w)
        return True

if __name__ == '__main__':
    a = app()
    a.MainLoop()
