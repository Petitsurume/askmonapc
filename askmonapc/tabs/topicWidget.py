from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QSize, Qt
from askmonapc import const
import requests
import datetime
import re
class ResponseWidget(QWidget):
    def __init__(self, response_info):
        super(ResponseWidget, self).__init__()
        self.spacer1 = QVBoxLayout(self)
        # --- 名前欄
        self.spacer_name = QHBoxLayout()
        self.widget_num = QLabel(self)
        self.widget_num.setText(str(response_info.get("r_id", -1))+".")
        self.spacer_name.addWidget(self.widget_num)
        self.widget_name = QLabel(self)
        self.widget_name.setStyleSheet("QLabel {color: #080;}")
        self.widget_name.setText(response_info.get("u_name", "名無し")+response_info.get("u_dan", "さん")+" ("+str(response_info.get("u_id"))+")")
        self.spacer_name.addWidget(self.widget_name)
        self.widget_resdate = QLabel(self)
        self.widget_resdate.setText(": "+datetime.datetime.fromtimestamp(response_info.get("created", 0)).strftime("%Y/%m/%d %H:%M:%S"))
        self.spacer_name.addWidget(self.widget_resdate)
        self.spacer_name.addStretch(1)
        self.spacer1.addLayout(self.spacer_name)
        # --- 本文
        self.widget_body = QLabel(self)
        self.widget_body.setText(ResponseWidget.torich(response_info.get("response", "")))
        self.widget_body.setWordWrap(True)
        self.widget_body.setTextFormat(Qt.RichText)
        self.widget_body.setOpenExternalLinks(True)
        self.spacer1.addWidget(self.widget_body)
        self.setLayout(self.spacer1)
    def torich(message):
        message = message.replace("&", "&amp;")
        message = message.replace("<", "&lt;")
        message = message.replace(">", "&gt;")
        message = message.replace("\n", "<br>")
        # TODO: imgurのインライン表示対応
        # HTTP(S)の画像そのまま指定ではダメっぽいのでローカルに取得？
        # message = re.sub(r'https?://(i\.)?imgur\.com/[A-Za-z0-9_]+.(jpeg|jpg|png|gif)', '<a href="$0"><img src="$0" /></a>', message)
        return message
class TopicWidget(QListWidget):
    def __init__(self, topic_info):
        super(TopicWidget, self).__init__()
        self.topic_info = topic_info
        self.responses = []
        self.setWindowTitle(self.topic_info.get("title", "無題のトピック") + " - AskMonaPC")
        self.resize(640, 600)
        self.reload()
    def reload(self):
        self.responses = requests.get(const.API_URL+"responses/list", params = {
            "t_id": self.topic_info.get("t_id"),
            "to":1000
        }, headers = const.HTTP_HEADERS).json()
        print(self.responses)
        for response in self.responses.get("responses", []):
            print(response)
            wid = ResponseWidget(response)
            wid2 = QListWidgetItem()
            wid2.setSizeHint(wid.sizeHint())
            self.addItem(wid2)
            self.setItemWidget(wid2, wid)
