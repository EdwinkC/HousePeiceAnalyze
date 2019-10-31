import sys, random
from PyQt5.QtWidgets import (QWidget, QPushButton, QLabel, QComboBox, QDialog, QSizePolicy, QHBoxLayout, QApplication, QGridLayout)
from PyQt5 import QtWebEngineWidgets, QtCore
from sqlutil.db import MysqlDB
import matplotlib
matplotlib.use("Qt5Agg")  # 声明使用QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
#支持中文显示
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']
from boxplot import GraphV

# 数据库表名
TABLE_NAME = 'newdata'

# 当前的城市
city = '北京'
cityList = []

# 箱线图全局变量
x = [2010, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]
y = []
y0 = []

# 抽象的Canvas基类
class MyCanvas(FigureCanvas):

    def __init__(self, parent=None, width=11, height=5, dpi=100):
        # 创建一个Figure，注意：该Figure为matplotlib下的figure，不是matplotlib.pyplot下面的figure
        self.fig = Figure(figsize=(width, height), dpi=100)
        # 初始化父类
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        self.axes = self.fig.add_subplot(111)
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)

        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class MyControlCanvas(MyCanvas):
    def __init__(self):
        MyCanvas.__init__(self)
        self.axes.set_xlabel('年份')
        self.axes.set_ylabel('房价（元/平方米）')
        self.axes.set_title(city + '近十年房价走势图')
        self.axes.set_xlim(min(x) - 1, max(x) + 1, 1)

    def compute_initial_figure(self):
        self.axes.plot(x0, y0, linewidth=2)
        self.axes.bar(x, y, color='rgb')

    def update_figure(self):
        self.update_data()
        self.axes.clear()
        self.axes.plot(x, y0, linewidth=2)
        self.axes.bar(x, y, color='rgb')
        self.axes.set_xlabel('年份')
        self.axes.set_ylabel('房价（元/平方米）')
        self.axes.set_title(city + '近十年房价走势图')
        self.axes.set_xlim(min(x)-1, max(x)+1, 1)
        self.draw()

    def update_data(self):
        mydb = MysqlDB(user='root', pwd='123456', db='house')
        mydb.connectDB()
        result = mydb.fetchall("select date, price from " + TABLE_NAME + " where name = '%s' order by date"%(city))
        global x
        global y
        global y0
        x.clear()
        y.clear()
        y0.clear()
        for r in result:
            x.append(int(r[0]))
            y.append(r[1])
            y0.append(r[1] + max(y)*0.2)
        mydb.close()


class MainWin(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.dynamicButton = QPushButton('动态展示热门城市房价变化', self)
        self.dynamicButton.clicked.connect(self.showWebView)
        self.geoButton = QPushButton('地理坐标图', self)
        self.geoButton.clicked.connect(self.showGeo)
        self.boxButton = QPushButton('全国数据箱线图', self)
        self.boxButton.clicked.connect(self.showBoxPlot)
        self.label = QLabel('请选择城市：', self)
        # 下拉式列表
        self.combo = QComboBox(self)
        self.readData()
        for i in cityList:
            self.combo.addItem(i)
        self.combo.activated[str].connect(self.onActivated)
        # 绘制按钮
        self.button = QPushButton('绘制', self)
        self.button.clicked.connect(self.onClicked)

        # 绘图区
        self.fc = MyControlCanvas()

        grid = QGridLayout()
        grid.setSpacing(20)
        grid.addWidget(self.dynamicButton, 1, 1)
        grid.addWidget(self.geoButton, 2, 1)
        grid.addWidget(self.boxButton, 3, 1)
        grid.addWidget(self.label, 5, 1)
        grid.addWidget(self.combo, 6, 1)
        grid.addWidget(self.button, 8, 1)
        grid.addWidget(self.fc, 1, 5, 10, 5)
        self.setLayout(grid)

        self.setGeometry(50, 50, 350, 300)
        self.setWindowTitle('楼市价格可视化系统')

    def readData(self):
        mydb = MysqlDB(user='root', pwd='123456', db='house')
        mydb.connectDB()
        result = mydb.fetchall('select distinct name from ' + TABLE_NAME)
        for r in result:
            cityList.append(r[0])
        mydb.close()

    def onActivated(self, text):
        global city
        city = text
        print('选中城市：' + city)

    def onClicked(self):
        self.fc.update_figure()
        print('当前绘制的城市：' + city)

    def showWebView(self):
        print('showWebView')
        dw = MyWebDialog("./DynamicRanking/bargraph.html", '全国主要城市近10年数据动态展示(press F5 to refresh)')
        dw.setWindowModality(QtCore.Qt.ApplicationModal)
        dw.exec_()

    def showBoxPlot(self):
        print('showBoxPlot')
        bp = GraphV()
        bp.setWindowModality(QtCore.Qt.ApplicationModal)
        bp.exec_()

    def showGeo(self):
        print('showGeo')
        geo = MyWebDialog("./render.html", 'Geo坐标系统图(press F5 to refresh)')
        geo.setWindowModality(QtCore.Qt.ApplicationModal)
        geo.exec_()

class MyWebDialog(QDialog):
    def __init__(self, url='', title=''):
        super().__init__()
        self.initUI(url, title)

    def initUI(self, url, title):
        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.setWindowFlags(QtCore.Qt.WindowMinMaxButtonsHint | QtCore.Qt.WindowCloseButtonHint)
        self.webEngineView = QtWebEngineWidgets.QWebEngineView(self)
        self.webEngineView.setUrl(QtCore.QUrl(QtCore.QFileInfo(url).absoluteFilePath()))

        self.hlayout = QHBoxLayout()
        self.hlayout.addWidget(self.webEngineView)
        self.setLayout(self.hlayout)
        self.setWindowTitle(title)

    # 重写按键事件方法，实现F5刷新
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_F5:
            self.webEngineView.load(QtCore.QUrl(QtCore.QFileInfo(self.url).absoluteFilePath()))

if __name__ == '__main__':

    app = QApplication(sys.argv)
    mw = MainWin()
    mw.show()
    sys.exit(app.exec_())