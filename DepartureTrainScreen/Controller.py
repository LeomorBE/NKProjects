try:
    from SNCFScreen import MainWindow, KeyWindow
except ImportError:
    print("Cannot find SNCFScreen file")

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QObject, pyqtSlot
import sys
from os import path 
import socket
import platform    # For getting the operating system name
import subprocess  # For executing a shell command

class Controller(QObject):
    def __init__(self):
        super().__init__()
        self.app = QApplication(sys.argv)
        if path.isfile("key"):
            self.window = MainWindow()
        else:
            self.window =  KeyWindow()
        self.window.windowChange.connect(self.changeWindow)

    def run(self)->None:
        if self.ping('8.8.8.8'):
            print("has a connection\n")
            if(isinstance(self.window, MainWindow)):
                self.window.run()
            self.window.show()
            sys.exit(self.app.exec_())
        else:
            print("no connection")

    def changeWindow(self, catWindow:int)-> None:
        match catWindow:
            case 1:
                self.newWindow = MainWindow()
            case 2:
                self.newWindow = KeyWindow()
            case _:
                print("error")
        self.window.hide()
        self.newWindow.show()

    def ping(self, host)->bool:
        """
        Returns True if host (str) responds to a ping request.
        Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
        """
        try:
            param = '-n' if platform.system().lower()=='windows' else '-c'
            command = ['ping', param, '1', host]
            return subprocess.call(command) == 0
        except:
            return False


        
   

def main():
    ctrl = Controller()
    ctrl.run()



if __name__ == '__main__':
   main()

