from PyQt5.QtWidgets import *
import sys
import signal
import requests
import askmonapc.tabs
signal.signal(signal.SIGINT, signal.SIG_DFL)


app = QApplication(sys.argv)

window = QTabWidget()
window.setWindowTitle("AskMonaPC")

window.addTab(askmonapc.tabs.TopicList(), "トピック一覧")
window.resize(600,600)
window.show()

sys.exit(app.exec_())