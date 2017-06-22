import wx
import wx.lib.agw.aui.auibook
import sys
import signal
import requests
import askmonapc.tabs
signal.signal(signal.SIGINT, signal.SIG_DFL)


app = wx.App()

window = wx.Frame(None)
window.SetTitle("AskMonaPC")
notebook = wx.lib.agw.aui.auibook.AuiNotebook(window)
notebook.AddPage(askmonapc.tabs.TopicList(notebook), "トピック一覧", False)
notebook.SetSizeWH(300,300)
window.Show()

sys.exit(app.MainLoop())