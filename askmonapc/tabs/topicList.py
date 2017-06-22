import wx
import requests
from askmonapc import const
import datetime
from .topicWidget import TopicWidget
from askmonapc.utils import *
class TopicList(wx.ListCtrl):
    def __init__(self,parent = None):
        super(TopicList, self).__init__(parent, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.topics = []
        self.InsertColumn(0, "トピック名")
        self.InsertColumn(1, "勢い")
        self.InsertColumn(2, "age日") 
        self.reload()
        @bind(self, wx.EVT_LIST_ITEM_ACTIVATED)
        def activated(e):
            topic = self.topics[self.GetFirstSelected()]
            topicWidget = TopicWidget(topic, parent)
            parent.AddPage(topicWidget, topicWidget.topic_info.get("title", "無題のトピック"))
    def reload(self):
        self.topics = requests.get(const.API_URL+"topics/list",headers = const.HTTP_HEADERS).json().get("topics", [])
        def mapfunc(item):
            return item["title"]
        line = 0
        for topic in self.topics:
            self.InsertItem(line, topic.get("title", "(無題)"))
            self.SetItem(line, 1, (str(int(topic.get("count", 0) / ((int(datetime.datetime.now().timestamp()) - topic.get("created", 0))/60) * 60 * 24 * 1000000) / 1000000)))
            self.SetItem(line, 2, datetime.datetime.fromtimestamp(topic.get("updated")).strftime("%Y/%m/%d %H:%M:%S"))
            line+=1
        self.SetColumnWidth(0, -1)
        self.SetColumnWidth(2, -1)