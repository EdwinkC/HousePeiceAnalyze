import sys, copy
from PyQt5.QtWidgets import QSizePolicy, QApplication
from sqlutil.db import MysqlDB
import matplotlib
matplotlib.use("Qt5Agg")  # 声明使用QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']

theData=[]

class Data(object):
    theData=[]
    DbHandle = object()
    dict1={}
    dict0 = {}
    mySet = set()

    def __init__(self):
        self.mydb = MysqlDB(user='root', pwd='123456', db='house')
        self.mydb.connectDB()

    def __del__(self):
        self.mydb.close()

    theNum=1
    def getData(self):
        data1 =self.mydb.fetchall("select distinct name from house")
        for value in data1:
            self.dict0[value[0]] = copy.deepcopy(self.dict1)
            self.mySet.add(str(value[0]))
            # print(self.theNum)
            # self.theNum+=1
            # print("'%s',"%(value[0]))

        data0 = self.mydb.fetchall(" select * from house order by date")
        for row in data0:
            self.dict0[row[1]][row[4]] = row[2]

        for i in range(0, len(self.mySet)):
            temp = []
            string = self.mySet.pop()
            """
            if string != '北京':
                continue"""
            theFirst = 2010
            theLast = 2019
            for begin in range(2010, 2020):
                if str(begin) in self.dict0[string]:
                    theFirst = begin
                    break
            for begin in range(2010, theFirst + 1):
                temp.append(self.dict0[string][str(theFirst)])
            for end in range(2010, 2020):
                end0 = 4029 - end
                if str(end0) in self.dict0[string]:
                    theLast = end0  # thelast有数据
                    break
            midNum = 0
            for mid in range(theFirst + 1, theLast):  # thefirst+1是没有数据的。  循环中的是没有数据的。但是中间有可能有数据。
                if midNum != 0:
                    midNum -= 1
                    continue
                theNow0 = self.dict0[string][str(theFirst)]
                theNow1 = self.dict0[string][str(theLast)]
                if str(mid) in self.dict0[string]:
                    temp.append(self.dict0[string][str(mid)])
                    theNow0 = self.dict0[string][str(mid)]
                else:
                    midLast = 0
                    for midMid in range(mid, theLast + 1):  # 这里。
                        if str(midMid) in self.dict0[string]:
                            theNow1 = self.dict0[string][str(midMid)]
                            midLast = midMid
                            break

                    for midMid0 in range(mid, midLast):  # midMid0都是不再的。
                        nowNow = int((theNow0 + theNow1) / 2)
                        temp.append(nowNow)
                        # print( " 左边=%d  右边=%d "%( theNow0,theNow1 ) )
                    midNum = midLast - mid - 1

            for end in range(theLast, 2020):  # 2010到2019  十年的。
                temp.append(self.dict0[string][str(theLast)])

            if len(temp) == 11:
                temp.pop()
            """
            print(string)
            print(temp)
            print(len(temp))
            print()"""
            self.theData.append(temp)

        return self.theData

    def transpose(self, matrix):
        new_matrix = []
        for i in range(len(matrix[0])):
            matrix1 = []
            for j in range(len(matrix)):
                matrix1.append(matrix[j][i])
            new_matrix.append(matrix1)
        return new_matrix

class MyBoxPlot(FigureCanvas):

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
        self.setWindowTitle('全国近十年房价数据箱线图')
        self.test()
        self.draw()

    def compute_initial_figure(self):
        pass

    def test(self):
        data = Data()
        theData = data.getData()
        theData = data.transpose(theData)
        self.axes.boxplot(x = theData, positions=[2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019],
                          patch_artist=True, showmeans=True,  boxprops = {'color':'black','facecolor':'#CCFFCC'},
                          flierprops={'marker': 'o', 'markerfacecolor': 'red', 'color': 'black'},
                          meanprops={'marker': 'D', 'markerfacecolor': 'indianred'},
                          medianprops={'linestyle': '--', 'color': 'red'}
                          )
        self.axes.set_xlabel('年份')
        self.axes.set_ylabel('房价（元/平方米）')
        self.axes.set_title('全国房价箱线图')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    bp = MyBoxPlot()
    bp.show()
    sys.exit(app.exec_())