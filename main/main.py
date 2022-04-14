from PySide2.QtWidgets import QApplication,QMessageBox
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile,QDate,QTimer,QDateTime,Qt
from PySide2.QtGui import QIcon
import requests
import json
import os


class MusicDlg:

    # 创建列表,后面下载需要

    music_list = []
    def __init__(self):
        #

        qfile_stats = QFile("./ui/kuwoui.ui")
        qfile_stats.open(QFile.ReadOnly)
        qfile_stats.close()

        self.ui = QUiLoader().load(qfile_stats)
        self.ui.Bsearch.clicked.connect(self.search)
        self.ui.Bload.clicked.connect(self.music_download)
        time = QDateTime.currentDateTime()
        strBuffer = time.toString("yyyy/MM/dd  hh:mm:ss")
        self.ui.label.setText(strBuffer)
        self.ui.timer = QTimer(self.ui)  # 初始化一个定时器
        self.ui.timer.timeout.connect(self.dlgTime)  # 计时结束调用operate()方法
        self.ui.timer.start(1000)  # 设置计时间隔并启动
        # self.ui.setWindowIcon(QIcon(":/icon/myicon.ico"))
        # self.ui.setWindowFlag(QtCore.Qt.FramelessWindowHint)
    def search(self):
        self.music_list=[]
        counter = self.ui.listWidget.count();
        if counter!=0:
            # self.ui.listWidget.disconnect()
            self.ui.listWidget.clear()
        self.ui.label_status.setText("正在搜索...")
        # song_name=self.ui.lineEdit.text()

        kw = self.ui.lineEdit.text()
        # 请求头
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36 Edg/84.0.522.63",
            "Cookie": "_ga=GA1.2.1083049585.1590317697; _gid=GA1.2.2053211683.1598526974; _gat=1; Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1597491567,1598094297,1598096480,1598526974; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1598526974; kw_token=HYZQI4KPK3P",
            "Referer": "http://www.kuwo.cn/search/list?key=%E5%91%A8%E6%9D%B0%E4%BC%A6",
            "csrf": "HYZQI4KPK3P",
        }
        # 参数列表
        params = {
            "key": kw,
            # 页数
            "pn": "1",
            # 音乐数
            "rn": "10",
            "httpsStatus": "1",
            "reqId": "cc337fa0-e856-11ea-8e2d-ab61b365fb50",
        }

        url = "http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?"
        res = requests.get(url=url, headers=headers, params=params)
        res.encoding = "utf-8"
        text = res.text
        # 转成json数据
        json_list = json.loads(text)
        # 发现data中list是存主要数据的地方
        datapack = json_list["data"]["list"]
        print(datapack)
        # 遍历拿到所需要的数据，音乐名称，歌手，id...
        for i in datapack:
            # 音乐名
            music_name = i["name"]
            # 歌手
            music_singer = i["artist"]
            # 待会需要的id先拿到
            rid = i["rid"]
            # 随便试听拿到一个音乐的接口,这是的rid就用得上了
            api_music = "http://www.kuwo.cn/url?format=mp3&rid={}&response=url&type=convert_url3" \
                        "&br=128kmp3&from=web&t=1598528574799&httpsStatus=1" \
                        "&reqId=72259df1-e85a-11ea-a367-b5a64c5660e5".format(rid)
            api_res = requests.get(url=api_music)
            # 打印发现真实的url确实在里面
            # print(api_res.text)
            music_url = json.loads(api_res.text)["url"]
            # 大功告成，试试效果
            self.ui.listWidget.addItem(music_name+"-"+music_singer)
            # 把数据存到字典方便下载时查找
            music_dict = {}
            music_dict["name"] = music_name
            music_dict["url"] = music_url
            music_dict["singer"] = music_singer
            self.music_list.append(music_dict)
            self.ui.label_status.setText("搜索完成")

    def music_download(self):
        index = self.ui.listWidget.currentRow()
        self.ui.label_status.setText("正在下载"+self.music_list[index]["name"]+"-"+self.music_list[index]["singer"])
        # self.ui.label_status.setText("当前选择"+self.music_list[index]["name"]+"-"+self.music_list[index]["singer"])
        root = 'E://下载的music//'
        if not os.path.exists(root):
            os.mkdir(root)
        # 拿到字典中对应的音乐url数据
        music_content = requests.get(url=self.music_list[index]["url"]).content
        with open(root + "{}-{}.mp3".format(self.music_list[index]['name'], self.music_list[index]['singer']), "wb") as f:
            f.write(music_content)
            self.ui.listDownload.addItem("成功下载{}-{}.mp3".format(self.music_list[index]['name'], self.music_list[index]['singer']))
    def dlgTime(self):

        time = QDateTime.currentDateTime()
        strBuffer = time.toString("yyyy/MM/dd  hh:mm:ss")
        self.ui.label.setText(strBuffer)


app = QApplication([])
app.setWindowIcon(QIcon('3’.png'))
# app.setWindowFlag(Qt.FramelessWindowHint)
dlg = MusicDlg()
dlg.ui.show()
app.exec_()

# pyinstaller main.py --noconsole --hidden-import PySide2.QtXml --icon="//.ico" 转exe