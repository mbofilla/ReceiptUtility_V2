import sys
from PyQt4.QtGui import *
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QSettings, QPoint, QSize
import random
from datetime import datetime
import pickle



zoom = 1.0
rect2text = {}
ex = 0

#field_dict = {0:'sku_number',1:'quantity',2:'how_sold',3:'description',4:'total_quantity',5:'unit_price',6:'per',7:'net_amount'}

def get_a_key():
   while True:
      keyval = random.randrange(1,999999)
      if keyval not in rect2text: break
   return int(keyval)


class boundingBox:
    def __init__(self,startp,stopp,fld,grp):
        self.start = startp
        self.stop = stopp
        self.group = int(float(grp))
        self.field = fld

class MyGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        self.startx = 0
        self.starty = 0
        self.stopx = 0
        self.stopy = 0
        self.selecteditem = -1
        self.lastupdate=-1
        self.indraw = False
        super(QGraphicsView, self).__init__(parent)
        self.parent = parent
        self.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)

    def updateBox(self,event):
        if self.indraw:
            p = self.mapToScene(event.pos())
            self.stopx = p.x()
            self.stopy = p.y()
            if (self.stopx < self.startx):
                temp = self.startx
                self.startx = self.stopx
                self.stopx = temp
            if (self.stopy < self.starty):
                temp = self.starty
                self.starty = self.stopy
                self.stopy = temp
            bwidth = (self.stopx - self.startx)
            bheight = (self.stopy - self.starty)
            self.r.setRect(self.startx, self.starty, bwidth, bheight)

    def contextMenuEvent(self, event,s):
        print "kablamo!!"
        print s

        menu = QtGui.QMenu()

        if (s == "sku_number"):
            sku_num = menu.addAction('***SKU_NUMBER***')
        else:
            sku_num = menu.addAction('sku_number')

        if (s == "quantity"):
            quan = menu.addAction('***QUANTITY***')
        else:
            quan = menu.addAction('quantity')

        if (s == "how_sold"):
            how_sold = menu.addAction('***HOW_SOLD***')
        else:
            how_sold = menu.addAction('how_sold')

        if (s == "description"):
            desc = menu.addAction('***DESCRIPTION***')
        else:
            desc = menu.addAction('description')

        if (s == "total_quantity"):
            tot_quan = menu.addAction('***TOTAL_QUANTITY***')
        else:
            tot_quan = menu.addAction('total_quantity')

        if (s == "unit_price"):
            unit_pri = menu.addAction('***UNIT_PRICE***')
        else:
            unit_pri = menu.addAction('unit_price')

        if (s == "per"):
            per = menu.addAction('***PER***')
        else:
            per = menu.addAction('per')

        if (s == "net_amount"):
            netamt = menu.addAction('***NET_AMOUNT***')
        else:
            netamt = menu.addAction('net_amount')

        aresult = menu.exec_(event.globalPos())
        if (aresult == sku_num):
            return "sku_number"
        if (aresult == quan):
            return "quantity"
        if (aresult == how_sold):
            return "how_sold"
        if (aresult == desc):
            return "description"

        if (aresult == tot_quan):
            return "total_quantity"
        if (aresult == unit_pri):
            return "unit_price"
        if (aresult == per):
            return "per"
        if (aresult == netamt):
            return "net_amt"

    print "done kablamoing..."

    def mousePressEvent(self, event):
        global rect2text
        global ex
        self.indraw = False
        self.downAt = event.pos()
        lastselecteditem = self.selecteditem
        if self.selecteditem != -1:
            self.selecteditem.setPen(QColor(0, 0, 255))
            self.selecteditem = -1
            ex.statusBar().showMessage("[no bounding box selected]")

        i = self.itemAt(event.pos())
        if i and type(i)==QGraphicsRectItem:
            print "clicked on something"
            if lastselecteditem == i:

                i.setPen(QColor(0, 255, 0))
                self.selecteditem = i

                new_str = self.contextMenuEvent(event,i.data(1).toString())
                print "new string"
                print new_str
                myGrp = int(i.data(0).toInt()[0])
                myKey = int(i.data(2).toInt()[0])
                print "found key " + str(myKey)
                rect2text[myKey].setPlainText("("+str(myGrp)+")("+new_str+")")
                ex.statusBar().showMessage("("+str(myGrp)+")("+new_str+")")
                i.setData(1,QtCore.QVariant(new_str))
            else:
                i.setPen(QColor(0,255,0))
                self.selecteditem = i
                myGrp = int(i.data(0).toInt()[0])
                myStr = str(i.data(1).toString())

                ex.statusBar().showMessage("(" + str(myGrp) + ")(" + str(myStr) + ")")

        else:

            p = self.mapToScene(event.pos())
            self.startx = p.x()
            self.starty = p.y()
            self.indraw = True
            self.r = self.scene().addRect(self.startx,self.starty,0,0)
            self.r.setPen(QColor(255, 0, 0))

            self.r.setData(0,QtCore.QVariant(1))
            self.r.setData(1,QtCore.QVariant('sku_number'))
            k = get_a_key()
            print "got key " + str(k)
            self.r.setData(2,QtCore.QVariant(k))

            t = QGraphicsTextItem()
            t.setPos(self.startx,self.starty)
            t.setPlainText('(1)(sku_number)')

            #ex.statusBar.showMessage("(1)(sku_number)")
            self.scene().addItem(t)

            rect2text[k]=t
            if k in rect2text:
                print str(k) + " key is in dictionary"
            else:
                print str(k) + " key is not in dictionary"

            print repr(rect2text[k])
            self.update()

    def mouseMoveEvent(self, event):
        self.updateBox(event)
        self.update()

    def mouseReleaseEvent(self, event):
        if self.indraw:
            xdist = abs(event.pos().x() - self.downAt.x())
            ydist = abs(event.pos().y() - self.downAt.y())
            print str(xdist) + " " + str(ydist)
            if ((xdist + ydist) < 10):
                self.indraw = False
                myKey = int(self.r.data(2).toInt()[0])
                self.scene().removeItem(rect2text[myKey])
                self.scene().removeItem(self.r)
                del rect2text[myKey]
            else:
                self.r.setPen(QColor(0,0,255))
                self.updateBox(event)
                self.indraw = False
                ex.statusBar().showMessage("[no bounding box selected]")

                self.lastupdate = self.r
                self.selecteditem = -1
                self.update()



class Example(QtGui.QMainWindow):

    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):


        self.menubar = self.menuBar()
        self.fileMenu = self.menubar.addMenu('&File')

        self.loadLayout = QtGui.QAction("Load Layout", self)
        self.loadLayout.setShortcut('Ctrl+L')
        self.loadLayout.setStatusTip('Save a receipt layout')
        self.loadLayout.triggered.connect(self.loadLayoutProc)

        self.saveLayout = QtGui.QAction("Save Layout", self)
        self.saveLayout.setShortcut('Ctrl+S')
        self.saveLayout.setStatusTip('Save a receipt layout')
        self.saveLayout.triggered.connect(self.saveLayoutProc)

        self.loadImage = QtGui.QAction("Load Image", self)
        self.loadImage.setShortcut('Ctrl+I')
        self.loadImage.setStatusTip('Load a receipt image')
        self.loadImage.triggered.connect(self.loadImageProc)

        self.exitAction = QtGui.QAction('Exit', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit application')
        self.exitAction.triggered.connect(QtGui.qApp.quit)

        #self.fileMenu = self.menubar.addMenu('&File')

        self.fileMenu.addAction(self.saveLayout)
        self.fileMenu.addAction(self.loadLayout)
        self.fileMenu.addAction(self.loadImage)
        self.fileMenu.addAction(self.exitAction)


        #self.scene.addText("Hello, world scene!")
        self.scene = QtGui.QGraphicsScene()

        self.view = MyGraphicsView(self.scene)
        self.setCentralWidget(self.view)

        self.view.setMouseTracking(True)
        self.view.setDragMode(QtGui.QGraphicsView.RubberBandDrag)
        self.statusBar()
        """

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.view)
        vbox.addWidget(self.statusBar)
        hbox = QtGui.QHBoxLayout()

        hbox.addLayout(vbox)
        self.setLayout(hbox)
        """
        self.setGeometry(300, 300, 390, 210)
        self.setWindowTitle('BuildPay Receipt Map Utility')
        self.settings = QSettings('BuildPay', 'ReceiptMapUtility')

        # Initial window size/pos last saved. Use default values for first time
        self.resize(self.settings.value("size", QSize(390, 210)).toSize())
        self.move(self.settings.value("pos", QPoint(300, 300)).toPoint())
        self.show()
        self.statusBar().showMessage("[no bounding box selected]")

    def closeEvent(self, e):
        # Write window size and position to config file
        self.settings.setValue("size", self.size())
        self.settings.setValue("pos", self.pos())

        e.accept()


    def update_group(self, item, n):
        global ex
        myKey = int(item.data(2).toInt()[0])

        rect2text[myKey].setPlainText("("+str(n)+")(" + item.data(1).toString()+")")
        ex.statusBar().showMessage("(" + str(n) + ")(" + item.data(1).toString()+ ")")
        item.setData(0, QtCore.QVariant(n))

    def keyPressEvent(self, event):
        key = event.key()
        print "got keyPressEvent " + str(key)
        global zoom
        global ex
        if key == 43:
            zoom *= 1.25
            self.redraw_main()

        if key == 45:
            zoom /= 1.25
            self.redraw_main()

    #print "ho"

        if key == 16777223:
            if self.view.selecteditem != -1:
                print "deleting something"
                myKey = int(self.view.selecteditem.data(2).toInt()[0])
                self.scene.removeItem(rect2text[myKey])
                self.scene.removeItem(self.view.selecteditem)
                del rect2text[myKey]

                self.view.selecteditem = -1
                ex.statusBar().showMessage("[no bounding box selected]")
        if key == 88:
                if self.view.lastupdate != None:
                    print "deleting something"
                    myKey = int(self.view.lastupdate.data(2).toInt()[0])
                    self.scene.removeItem(rect2text[myKey])
                    self.scene.removeItem(self.view.lastupdate)
                    del rect2text[myKey]
                    self.view.lastupdate = None


        if key == 16777220:
            if self.view.selecteditem != -1:
                #enter key, maybe trigger edit context menu
                pass

        if key == 16777219:
            if self.view.selecteditem != -1:
               grp = 0
               grp = int(self.view.selecteditem.data(0).toInt()[0])
               grp = int(grp / 10)
               self.update_group(self.view.selecteditem,grp)

        if (key>=48) and (key<=57):
            if self.view.selecteditem != -1:
               grp = 0
               grp = int(self.view.selecteditem.data(0).toInt()[0])
               grp *= 10
               grp += (key-48)
               self.update_group(self.view.selecteditem, grp)

    def redraw_main(self):
        global zoom
        print "zoom is " + str(zoom)
        self.view.resetTransform()
        self.view.scale(zoom,zoom)

    def loadImageProc(self):
        print "loadImage called"


        fileName = QtGui.QFileDialog.getOpenFileName(None, 'Open file', '/')
        try:
           self.scene.removeItem(self.p)
        except:
           pass
        finally:
           pass

        self.p = QtGui.QPixmap(fileName)

        self.scene.addPixmap(self.p)

    def generate_boxlist(self):
        boxList = []
        for i in self.scene.items():
            if type(i)==QGraphicsRectItem:
               #ii = boundingBox(QtCore.QPoint(0, 0), QtCore.QPoint(0, 0), "0", "0")
               #QGraphicsRectItem.rect
               rii = i.rect()
               myGrp = str(i.data(0).toString())
               myStr = str(i.data(1).toString())
               ii = boundingBox(QtCore.QPoint(rii.topLeft().x(),rii.topLeft().y()),QtCore.QPoint(rii.bottomRight().x(),rii.bottomRight().y()),myStr,myGrp)
               boxList.append(ii)
        return boxList


    def loadLayoutProc(self):
        print "loadLayout called"
        boxList = []

        fileName = fileName = QtGui.QFileDialog.getOpenFileName(None, 'Load file', '/')
        if fileName:

            for i in self.scene.items():
                if (type(i) == QGraphicsRectItem) or (type(i)==QGraphicsTextItem):
                    self.scene.removeItem(i)


            f = open(fileName, "r")
            s = f.read()
            f.close()
            boxList = pickle.loads(s)
            print len(boxList)
            for b in boxList:
                print b.start.x(), b.start.y(), b.stop.x()-b.start.x(), b.stop.y()-b.start.y()
                if b.stop.y() - b.start.y() < 45:

                   decide = raw_input("accept this?")
                   if decide != "y":
                       continue

                r = self.scene.addRect(b.start.x(), b.start.y(), b.stop.x()-b.start.x(), b.stop.y()-b.start.y())
                r.setData(0, QtCore.QVariant(int(b.group)))
                r.setData(1, QtCore.QVariant(str(b.field)))
                k = get_a_key()
                print "got key " + str(k)
                r.setData(2, QtCore.QVariant(k))

                t = QGraphicsTextItem()
                #t.setPos(self.startx, self.starty)
                t.setPos(b.start.x(), b.start.y())

                myGrp = int(r.data(0).toInt()[0])
                myStr = str(r.data(1).toString())
                t.setPlainText("(" + str(myGrp) + ")(" + str(myStr) + ")")

                rect2text[k] = t
                # ex.statusBar.showMessage("(1)(sku_number)")
                self.scene.addItem(t)

    def saveLayoutProc(self):

        print "saveLayout called"

        fileName = QtGui.QFileDialog.getSaveFileName(None, 'Save file', '/')
        if fileName:
            print fileName
            boxList = self.generate_boxlist()

            f = open(fileName, "w")
            f.write(pickle.dumps(boxList))
            f.close()



def main():
    global ex
    random.seed(datetime.now())
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    #filter = MFilter()
    #app.installEventFilter(filter)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


