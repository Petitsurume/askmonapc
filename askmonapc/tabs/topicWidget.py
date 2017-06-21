import wx
import wx.lib.scrolledpanel
from askmonapc import const
import requests
import datetime
import re

def watanabe2mona(watanabe):
    print(watanabe)
    watanabe = int(watanabe)
    r = ""
    r = "%d.%d" % (watanabe/100000000, watanabe%100000000)
    r = re.sub(r"\.?0+$", "", r)
    return r
class ResponseWidget(wx.Panel):
    def __init__(self, response_info, parent=None):
        super(ResponseWidget, self).__init__(parent)
        self.spacer0 = wx.BoxSizer(wx.HORIZONTAL)
        self.spacer0.AddSpacer(10)
        self.spacer1 = wx.BoxSizer(wx.VERTICAL)
        self.spacer1.AddSpacer(10)
        # --- 名前欄
        self.spacer_name = wx.BoxSizer(wx.HORIZONTAL)
        self.widget_num = wx.StaticText(self, label=str(response_info.get("r_id", -1))+".")
        self.widget_name = wx.StaticText(self, label=response_info.get("u_name", "名無し")+response_info.get("u_dan", "さん")+" ("+str(response_info.get("u_id"))+")")
        self.widget_name.SetForegroundColour("#008800")
        self.widget_resdate = wx.StaticText(self, label=": "+datetime.datetime.fromtimestamp(response_info.get("created", 0)).strftime("%Y/%m/%d %H:%M:%S"))
        self.widget_sendmona = wx.StaticText(self, label="+"+watanabe2mona(response_info.get("receive","0"))+"mona")
        self.spacer_name.AddMany([self.widget_num, self.widget_name, self.widget_resdate, self.widget_sendmona])
        self.spacer1.Add(self.spacer_name)
        # --- 本文
        self.widget_body = wx.StaticText(self, label=ResponseWidget.torich(response_info.get("response", "")))
        recvmona = int(response_info.get("receive","0"))/100000000
        base_fontsize = 12 / 0.85
        fontinfo = wx.FontInfo(base_fontsize)
        lv = 0
        if recvmona > 10:
            lv = 4
        elif recvmona > 2:
            lv = 3
        elif recvmona > 1:
            lv = 2
        elif recvmona > 0:
            lv = 1
        if lv == 0:
            # lv0
            fontinfo = wx.FontInfo(base_fontsize * 0.85)
        if lv == 1:
            # lv1
            # 何もしない
            fontinfo = fontinfo
        elif lv == 2:
            # lv2
            fontinfo = fontinfo.Bold()
        elif lv == 3:
            # lv3
            fontinfo = wx.FontInfo(base_fontsize * 1.25).Bold()
        elif lv == 4:
            # lv4
            fontinfo = wx.FontInfo(base_fontsize * 1.25)
            self.widget_body.SetForegroundColour("#2222ff")
        self.widget_body.SetFont(wx.Font(fontinfo))
        self.spacer1.Add(self.widget_body)
        self.spacer1.AddSpacer(10)
        self.spacer0.Add(self.spacer1)
        self.SetSizer(self.spacer0)
    def torich(message):
        return message
        message = message.replace("&", "&amp;")
        message = message.replace("<", "&lt;")
        message = message.replace(">", "&gt;")
        message = message.replace("\n", "<br>")
        # TODO: imgurのインライン表示対応
        # HTTP(S)の画像そのまま指定ではダメっぽいのでローカルに取得？
        # message = re.sub(r'https?://(i\.)?imgur\.com/[A-Za-z0-9_]+.(jpeg|jpg|png|gif)', '<a href="$0"><img src="$0" /></a>', message)
        return message
class TopicWidget(wx.Frame):
    def __init__(self, topic_info, parent = None):
        super(TopicWidget, self).__init__(parent)
        self.topic_info = topic_info
        self.responses = []
        self.SetTitle(self.topic_info.get("title", "無題のトピック") + " - AskMonaPC")
        self.SetSizeWH(640, 600)
        self.layout = wx.BoxSizer(wx.VERTICAL)
        self.layout_panel = wx.lib.scrolledpanel.ScrolledPanel(self)
        self.layout_panel.SetupScrolling(scroll_x=False)
        self.layout_res = wx.BoxSizer(wx.VERTICAL)
        self.layout_panel.SetSizer(self.layout_res)
        self.layout.Add(self.layout_panel)
        self.reload()
    def reload(self):
        self.responses = requests.get(const.API_URL+"responses/list", params = {
            "t_id": self.topic_info.get("t_id"),
            "to":1000
        }, headers = const.HTTP_HEADERS).json()
        print(self.responses)
        for response in self.responses.get("responses", []):
            wid = ResponseWidget(response, self.layout_panel)
            self.layout_res.Add(wid)