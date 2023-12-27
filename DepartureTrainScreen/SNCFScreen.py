import sys
import typing
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget
import threadSNCF
from datetime import datetime
import json
import queue
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from os import path


class MainWindow(QWidget):
   cityChangeSignal = pyqtSignal(str)
   windowChange = pyqtSignal(int)
   def __init__(self):
      """
      Method constructor.
      """
      super().__init__()
      self.resize(800,450)
      self.setWindowTitle("SNCF Display Departures")
      hLayout = QHBoxLayout()
      self.vLayout = QVBoxLayout()
      self.setWindowIcon(QIcon('clock.png'))

      toolBar = QToolBar()
      toolBar.setContentsMargins(0,0,0,0)
      menu1 = QPushButton("Train")
      menu1.setContentsMargins(0,0,0,0)
      menu = QMenu()
      menu.setContentsMargins(0,0,0,0)
      menu.addAction("SNCF")
      menu.addAction("SNCB")
      menu1.setMenu(menu)
      menu.triggered.connect(lambda action: print(action.text()))

      self.updatePromp = QLabel("test")
      self.updatePromp.setContentsMargins(0,0,10,0)
      self.cityAsk = QLineEdit()
      self.cityAsk.setContentsMargins(150,0,150,0)
      completer = QCompleter(self.getListOfCity())
      completer.setCaseSensitivity(Qt.CaseInsensitive)
      self.cityAsk.setCompleter(completer)
      self.cityAsk.editingFinished.connect(self.updateCity)
      self.cityAsk.returnPressed.connect(self.updateCity)

      toolBar.addWidget(menu1)
      toolBar.addWidget(self.cityAsk)
      toolBar.addWidget(self.updatePromp)
      #self.vLayout.setMenuBar(self.menu)
      self.vLayout.addWidget(toolBar)
      scrollbar = QScrollBar()
      self.vLayout.setAlignment(Qt.AlignTop)
      self.vLayout.setContentsMargins(0,0,0,0)
      self.vLayout.setSpacing(0)

      self.widgetVLayout = QWidget()
      self.widgetVLayout.setLayout(self.vLayout)
      hLayout.addWidget(self.widgetVLayout)
      hLayout.addWidget(scrollbar)
      hLayout.setContentsMargins(0,0,0,0)
      hLayout.setSpacing(0)
      self.initLayout()
      self.setLayout(hLayout)
      #self.run()

   def initLayout(self):
      """
      Method initLayout().\n
      Initialise main Layout.
      """

      self.listLabel = []
      self.listLines = []
      self.listImage = []
      
      for i in range(13):

         self.listLines.append(QWidget())
         self.listImage.append(QLabel())
         hBox = QHBoxLayout()
         hBox.setAlignment(Qt.AlignLeft)
         hBox.setContentsMargins(0,0,0,0)

         self.listLabel.append(QLabel(str(i)))
         hBox.addWidget(self.listImage[i])
         hBox.addWidget(self.listLabel[i])
         self.listLines[i].setLayout(hBox)
         
         if (i%2) == 0:
            self.listLines[i].setStyleSheet("background-color: lavender;color: black;")
         else:
            self.listLines[i].setStyleSheet("background-color: lavenderblush;color: black")

         hBox.addWidget(self.listLabel[i])
         self.listLines[i].setLayout(hBox)

         self.listLines[i].setFixedHeight(int((450-20)/13))
         self.listLines[i].setMaximumWidth(800)
         self.widgetVLayout.layout().addWidget(self.listLines[i])

   def getTypeTrainImagePath(self,train:str):
      """
      Method getTypeTrainImagePath().\n
      Take as argument a string represent type of train.\n
      Return a string represent path to png file.
      """

      match train:
         case "TER":
            return "SNCF_logo/TER.png"
         case "TGV INOUI":
            return "SNCF_logo/Logo-TGV-inOUI-Fd_Clair_resize.png"
         case "TGV":
            return "SNCF_logo/Logo-TGV-inOUI-Fd_Clair_resize.png"
         case "SNCF":
            return "SNCF_logo/LOGO_SNCF_GROUPE_RVB_resize.png"
         case "TER HDF":
            return "SNCF_logo/TER.png"
         case "TER NA":
            return "SNCF_logo/TER.png"
         case "RER":
            return "SNCF_logo/RER.png"
         case "TRANSILIEN":
            return "SNCF_logo/Logo_SNCF_Transilien_2019.png"
         case "Intercités de nuit":
            return "SNCF_logo/LOGO_SNCF_GROUPE_RVB_resize.png"
         case "Intercités":
            return "SNCF_logo/LOGO_SNCF_GROUPE_RVB_resize.png"
         case "OUIGO":
            return "SNCF_logo/TGV_Ouigo.png"
         case _:
            print("error")


   def updateScreen(self,listDepart):
      """
      Method updateScreen()
      Update the screen with the list of departure train.\n
      Take as argument a list of dictionnaries containing train informations.
      """
      print("update screen")
      for j in range(len(self.listLines)):
         self.listLines[j].layout().removeWidget(self.listLabel[j])
         self.listLines[j].layout().removeWidget(self.listImage[j])
      i = 0
      for departure in listDepart:
         print(departure)
         text = (departure["number"] + " en direction de " +departure["direction"] + " à " + departure["horaire"])
         pixmap = QPixmap(self.getTypeTrainImagePath(departure["type_train"]))
         pixmap = pixmap.scaled(60,33,Qt.KeepAspectRatio,Qt.SmoothTransformation)
         self.listImage[i].setPixmap(pixmap)
         self.listLabel[i].setText(text)
         self.listLines[i].layout().addWidget(self.listImage[i])
         self.listLines[i].layout().addWidget(self.listLabel[i])
         self.updatePromp.setText(datetime.now().strftime('%H:%M:%S'))
         i+=1
      
      if i <13:
         for j in range(i,13):
            self.listLabel[j].setText("")
            self.listLines[j].layout().addWidget(self.listLabel[j])

   def run(self):
      """
      Method run().\n
      Part of initialisation of application.
      """

      self.thread = QThread()
      self.myQueue = queue.Queue()
      self.sncf = threadSNCF.SNCFDepartures(self.myQueue,None)
      self.myQueue.put("87141002")
      self.sncf.moveToThread(self.thread)
      self.thread.started.connect(self.sncf.run)
      self.sncf.update.connect(self.updateScreen)
      self.cityChangeSignal.connect(self.sncf.changeCity)
      self.thread.start()

   def initMenu(self):
      """
      Method initMenu().\n
      Part of initialisation of application.
      """

      hMenu = QHBoxLayout()
      menuTrain = QMenu("Train")
      sncb = menuTrain.addAction("SNCB")
      scnf = menuTrain.addAction("SNCF")
      hMenu.addWidget(hMenu)
      wMenu = QWidget()
      wMenu.setLayout(hMenu)
      self.vlayout.addWidget(wMenu)

   def getListOfCity(self)->list:
      """
      Method getListOfCity().\n
      Get the list of different station in France with the liste-des-gares.json.\n
      Return a list containing stations name.
      """
      listCity = []
      with open("./liste-des-gares.json",'rt') as file:
         jsonFile = file.read()
         jsonDict = json.loads(jsonFile)
         for element in jsonDict:
            listCity.append(element["libelle"])
         file.close
      return listCity
   
   def getNumOfCity(self,city:str):
      """
      Method getNumOfCity().\n
      Compare stations with argument city.\n
      Return a string containing uic code.
      """
      with open("./liste-des-gares.json",'rt') as file:
         numCity = ""
         jsonFile = file.read()
         jsonDict = json.loads(jsonFile)
         for element in jsonDict:
            if element["libelle"] == city:
               numCity = element["code_uic"]
               break
         file.close()
         return numCity
   
   def updateCity(self):
      """
      Method updateCity().\n
      """
      if self.myQueue.empty():
         self.myQueue.put(self.getNumOfCity(self.cityAsk.text()))

class KeyWindow(QWidget):
   windowChange = pyqtSignal(int)
   
   def __init__(self,parent = None):
      """
      Method constructor.
      """
      super().__init__()
      self.resize(300,200)
      self.setWindowTitle("API Key")
      self.setWindowIcon(QIcon('clock.png'))
      self.vLayout = QVBoxLayout()
      self.instruction = QLabel("Please enter your API Key.")
      self.lineEdit = QLineEdit()
      self.button = QPushButton("Confirm")
      self.button.pressed.connect(self.verifKey)
      self.vLayout.addWidget(self.instruction)
      self.vLayout.addWidget(self.lineEdit)
      self.vLayout.addWidget(self.button)
      self.setLayout(self.vLayout)
      #self.widgetCentral = QWidget()
      #self.widgetCentral.setLayout(self.vLayout)
      #self.setCentralWidget(self.widgetCentral)

   def verifKey(self):
      """
      Method verifKey()\n
      """
      key = self.lineEdit.text()
      response = threadSNCF.requestApiSNCF.requests.get("https://api.navitia.io/v1/coverage?key="+key)
      convertToJson = json.dumps(response.json(),sort_keys=True, indent=4)
      jsonDict = json.loads(convertToJson)
      if(jsonDict.get("message") is not None):
         self.instruction.setText("Wrong key, please enter a Valid API key.")
      else:
         self.__encryptKeyMem(key)
         print("emit 1")
         self.windowChange.emit(1)
         #self.ex = MainWindow()
         #self.hide()
         #self.ex.show()
      

         
   def __encryptKeyMem(self, keyAPI:str):
      """
      Method __encryptKeyMem().\n
      """
      key = b'R\x0f|\x89\xf5\x9a\xb3\xa7#\xcf\x91\xeas\xd7\xb9p'
      cipher = AES.new(key, AES.MODE_EAX)
      ciphertext, tag = cipher.encrypt_and_digest(keyAPI.encode())
      file = open("key", "wb")
      [ file.write(x) for x in (cipher.nonce, tag, ciphertext) ]
      file.close()

def main():
   app = QApplication(sys.argv)
   try:
      if path.isfile("key"):
         print("here")
         ex = MainWindow()
      else:
         print("here2")
         ex =  KeyWindow()
      ex.show()
   except ConnectionError as e:
      print("No connection")
   sys.exit(app.exec_())
if __name__ == '__main__':
   main()
