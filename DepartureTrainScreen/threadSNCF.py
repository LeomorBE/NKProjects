from PyQt5.QtCore import QObject, QThread, pyqtSignal
import requestApiSNCB
from time import sleep
import queue

class SNCFDepartures(QObject):
    update = pyqtSignal(list)
    sncf = requestApiSNCB.UseApiSNCB("key") #remplacez key par la clé API de la SNCF
    gare = "87141002"

    def __init__(self, testQueue,parent: None):
        super().__init__(parent)
        self.myQueue = testQueue
        
    def run(self):
        i = 0
        while True:
            if i ==0 or not self.myQueue.empty():
                station = self.myQueue.get()
                print(station)
                self.update.emit(self.sncf.getInfoArrival(station))            
                i = 30
            else:
                i -=1
                sleep(1)
            
    def changeCity(self,city:str):
        print("changed")
        self.gare = city
        
        
