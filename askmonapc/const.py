import enum
API_URL = "https://askmona.org/v1/"
HTTP_HEADERS = {
    "User-Agent": "AskMonaPC/0.1"
}
CATEGORY_ID = [
    "その他",
    "ばらまき",
    "初心者",
    "ニュース",
    "議論・討論",
    "趣味・生活",
    "創作・文化",
    "ネタ・雑談",
    "経済・社会",
    "科学・IT",
    "採掘",
    "R18"
]
class TOPIC_FLAG(enum.IntEnum):
    displayable = 1
    sendmoneyable = 2
    editable = 4
    writable = 8