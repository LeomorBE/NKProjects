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
        print("emit2")
        match catWindow:
            case 1:
                self.newWindow = MainWindow()
            case 2:
                self.newWindow = KeyWindow()
            case _:
                print("error")
        self.window.hide()
        self.newWindow.show()

    def isInternetConnection(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        s.settimeout(5)
        #s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

        ip_header = b'\x45\x00\x00\x1c' # Version, IHL, Type of Service | Total Length
        ip_header += b'\xab\xcd\x00\x00' # Identification | Flags, Fragment Offset
        ip_header += b'\x40\x01\x6b\xd8' # TTL, Protocol | Header Checksum
        #ip_header += bytes(socket.gethostbyname(socket.gethostname()))
        ip_header += b'\xc0\xa8\x92\x83' # Source Address
        ip_header += b'\x08\x08\x08\x08' # Destination Address

        #icmp_header = b'\x08\x00\xe5\xca' # Type of message, Code | Checksum
        #icmp_header += b'\x12\x34\x00\x01' # Identifier | Sequence Number

        #packet = ip_header + icmp_header
        icmp_header = b'\x08\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f'
        s.sendto(icmp_header, ('8.8.8.8', 0))
        response, _ = s.recvfrom(1024)

        # Check if the response is an ICMP Echo Reply (type 0)
        if response[20] == 0:
            print("Internet connection is available.")
        else:
            print("No internet connection.")
        
        s.close()

    def ping(self, host)->bool:
        """
        Returns True if host (str) responds to a ping request.
        Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
        """

        # Option for the number of packets as a function of
        try:
            param = '-n' if platform.system().lower()=='windows' else '-c'

            # Building the command. Ex: "ping -c 1 google.com"
            command = ['ping', param, '1', host]
            return subprocess.call(command) == 0
        except:
            return False


        
   

def main():
    ctrl = Controller()
    ctrl.run()



if __name__ == '__main__':
   main()

