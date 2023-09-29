from PyQt5.QtCore import QObject, QThread, pyqtSignal
import requestApiSNCF
from time import sleep
import queue

class SNCFDepartures(QObject):
    update = pyqtSignal(list)
    gare = "87141002" #Nancy station

    def __init__(self, testQueue,parent: None):
        """
        Method constructor.
        """
        super().__init__(parent)
        self.sncf = requestApiSNCF.UseApiSNCF()
        self.myQueue = testQueue
        
        
    def run(self):
        """
        Method run().\n
        While application is up, he works.\n
        each 30second, he updates trains departure and send signal to updatedScreen().
        """
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
        """
        Method changeCity(), slot of cityChangeSignal() signal.\n
        A setter.
        """
        print("changed")
        self.gare = city
        
        
