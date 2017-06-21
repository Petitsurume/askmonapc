import wx
import sys
import signal
import requests
import askmonapc.tabs
signal.signal(signal.SIGINT, signal.SIG_DFL)


app = wx.App()

window = wx.Frame(None)
window.SetTitle("AskMonaPC")
notebook = wx.Notebook(window)
notebook.InsertPage(0, askmonapc.tabs.TopicList(notebook), "トピック一覧")
window.SetSizeWH(600,600)
window.Show()

sys.exit(app.MainLoop())