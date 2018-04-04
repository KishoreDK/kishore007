import sys,os
from shutil import rmtree
from PyQt5.QtWidgets import QMainWindow, QToolBar, QInputDialog, QApplication, QDesktopWidget, QGridLayout, QMessageBox, QWidget, QPushButton, QAction, QFileDialog, QLabel
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtCore import Qt,QSize
from PIL import Image, ImageEnhance
from PIL.ImageQt import ImageQt

 
class App(QMainWindow):
 
    def __init__(self):
        super().__init__()
        self.initUI()
 
    def initUI(self):

        self.setWindowTitle("Photo-Smash")
        self.setWindowState(Qt.WindowMaximized)
        self.screen = QDesktopWidget().screenGeometry(-1)
        self.setMinimumSize(self.screen.width()-40,self.screen.height()-40)
        self.initMenu()
        self.initToolBar()
        
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.centralWidget.setStyleSheet("background-color:#555555;")


        self.gridLayout = QGridLayout()
        self.centralWidget.setLayout(self.gridLayout)

        # Create Image widget
   
        self.pic = QLabel(self)
        self.pic.setAlignment(Qt.AlignCenter)
        self.im = Image.open('test.jpg')
        self.image = ImageQt(self.im)
        self.pic.setPixmap(QPixmap.fromImage(self.image))
        
        
        self.gridLayout.addWidget(self.pic,0,0)



 
        self.show()
    
    def initMenu(self):
    	mainMenu = self.menuBar()
    	mainMenu.setStyleSheet("background-color:#333333;color:#000000;selection-background-color:#7aecd4;selection-color:#222222;")
    	fileMenu = mainMenu.addMenu('File')
    	editMenu = mainMenu.addMenu('Edit')
    	imageMenu = mainMenu.addMenu('Image')
    	adjustMenu = mainMenu.addMenu('Adjust')
    	helpMenu = mainMenu.addMenu('Help')

    	# File Menu 

    	importButton = QAction('Import Image', self)
    	importButton.setShortcut('Ctrl+N')
    	importButton.triggered.connect(self.openImportImageDialog)
    	fileMenu.addAction(importButton)

    	loadUrlButton = QAction('Load from URL', self)
    	loadUrlButton.setShortcut('Ctrl+U')
    	loadUrlButton.triggered.connect(self.openLoadUrlDialog)
    	fileMenu.addAction(loadUrlButton)

    	exitButton = QAction('Exit', self)
    	exitButton.setShortcut('Ctrl+Q')
    	exitButton.triggered.connect(self.exitapp)
    	fileMenu.addAction(exitButton)

    	undoButton = QAction('Undo', self)
    	undoButton.setShortcut('Ctrl+Z')
    	undoButton.triggered.connect(self.undoAction)
    	editMenu.addAction(undoButton)

    	redoButton = QAction('Redo', self)
    	redoButton.setShortcut('Ctrl+Y')
    	redoButton.triggered.connect(self.redoAction)
    	editMenu.addAction(redoButton)


    	#Image Menu

    	rotclk90Button = QAction('Rotate Cloclwise 90*', self)
    	rotclk90Button.triggered.connect(self.rotclk90Action)
    	imageMenu.addAction(rotclk90Button)

    	rotaclk90Button = QAction('Rotate Anti-Cloclwise 90*', self)
    	rotaclk90Button.triggered.connect(self.rotaclk90Action)
    	imageMenu.addAction(rotaclk90Button)

    	rot180Button = QAction('Rotate 180*', self)
    	rot180Button.triggered.connect(self.rot180Action)
    	imageMenu.addAction(rot180Button)
    

    	# Adjust Menu

    	contrastButton = QAction('Contrast', self)
    	contrastButton.triggered.connect(self.contrastAction)
    	adjustMenu.addAction(contrastButton)

    def openImportImageDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Import Image", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
        	ext = fileName.split(".")[-1]
        	if ext=="jpg" or ext=="jpeg" or ext=="png":
        		self.im = Image.open(fileName)
        		self.image = ImageQt(self.im)
        		self.pic.setPixmap(QPixmap.fromImage(self.image))

        	else:
        		print("wrong file type")


    def openLoadUrlDialog(self):
    	print("load from url")
    
    def undoAction(self):
    	print("undo")

    def redoAction(self):
    	print("redo")

    def rotclk90Action(self):
    	self.im = self.im.rotate(-90)
    	self.image = ImageQt(self.im)
    	self.pic.setPixmap(QPixmap.fromImage(self.image))


    def rotaclk90Action(self):
    	self.im = self.im.rotate(90)
    	self.image = ImageQt(self.im)
    	self.pic.setPixmap(QPixmap.fromImage(self.image))

    def rot180Action(self):
    	self.im = self.im.rotate(180)
    	self.image = ImageQt(self.im)
    	self.pic.setPixmap(QPixmap.fromImage(self.image))

    def contrastAction(self):
    	self.con = ImageEnhance.Contrast(self.im)
    	self.im = self.con.enhance(1.3)
    	self.image = ImageQt(self.im)
    	self.pic.setPixmap(QPixmap.fromImage(self.image))


    def initToolBar(self):
    	toolbarBox = QToolBar(self)
    	self.addToolBar(Qt.LeftToolBarArea, toolbarBox)
    	toolbarBox.setMovable(False)
    	toolbarBox.setStyleSheet("background-color:#444444;color:#000000;")
    	

    	resize = QAction(QIcon('Resize.png'),"Resize",self)
    	toolbarBox.addAction(resize)
    	toolbarBox.actionTriggered[QAction].connect(self.toolBtnPressed)

    def toolBtnPressed(self,t):
    	tool = t.text()
    	if (tool == "Resize"):
    		print("resize box",self.pic.width(),self.pic.height())
    		self.resizeAction()
    	elif (tool == ""):
    		pass
    	else:
    		pass


    def resizeAction(self):
    	ival, okPressed = QInputDialog.getInt(self, "Resize Image","Enter Resize Percentage% (1-200)", 100, 1, 200, 1)
    	if okPressed:
    		self.out = self.im.resize((int(self.pic.width()*(ival/200)),int(self.pic.height()*(ival/200))))
    		self.image = ImageQt(self.out)
    		self.pic.setPixmap(QPixmap.fromImage(self.image))
    

    def exitapp(self):
    	self.close()

    def closeEvent(self, event):
    	if  os.path.exists("pstemp"):
    		try:
    			rmtree("pstemp")
	    	except:
	    		pass
    	event.accept()
 
if __name__ == '__main__':
	if  os.path.exists("pstemp"):
		try:
			rmtree("pstemp")
			os.mkdir("pstemp")
		except:
			pass
	else:
		os.mkdir("pstemp")

	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())