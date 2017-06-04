from PyQt5.QtWidgets import QTreeView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
import requests
from askmonapc import const
import datetime
from .topicWidget import TopicWidget
class TopicList(QTreeView):
    def __init__(self):
        super(TopicList, self).__init__()
        self.topics = []
        self.reload()
        @self.doubleClicked.connect
        def open(signal):
            topic = self.topics[self.selectedIndexes()[0].row()]
            self.topicWidget = TopicWidget(topic)
            self.topicWidget.show()
    def reload(self):
        self.topics = requests.get(const.API_URL+"topics/list",headers = const.HTTP_HEADERS).json().get("topics", [])
        def mapfunc(item):
            return item["title"]
        listModel = QStandardItemModel(0, 3, self)
        listModel.setHeaderData(0, Qt.Horizontal, "トピック名")
        listModel.setHeaderData(1, Qt.Horizontal, "勢い")
        listModel.setHeaderData(2, Qt.Horizontal, "age日")
        for topic in self.topics:
            title_item = QStandardItem(topic.get("title", "(無題)"))
            title_item.setEditable(False)
            ikioi_item = QStandardItem(str(int(topic.get("count", 0) / ((int(datetime.datetime.now().strftime("%s")) - topic.get("created", 0))/60) * 60 * 24 * 1000000) / 1000000))
            ikioi_item.setEditable(False)
            age_item = QStandardItem(datetime.datetime.fromtimestamp(topic.get("updated")).strftime("%Y/%m/%d %H:%M:%S"))
            age_item.setEditable(False)
            listModel.appendRow([title_item, ikioi_item, age_item])
        self.setModel(listModel)
        self.resizeColumnToContents(0)
