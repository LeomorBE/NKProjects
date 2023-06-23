import requests
import json
from datetime import datetime, date
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


class UseApiSNCB:

    def __init__(self):
        self.key = self.__myKey()
        #self.key = key
        self.url = "https://api.sncf.com/v1"

    def __myKey(self)->str:
        file_in = open("key", "rb")
        nonce, tag, ciphertext = [ file_in.read(x) for x in (16, 16, -1) ]
        file_in.close()

        key = b'R\x0f|\x89\xf5\x9a\xb3\xa7#\xcf\x91\xeas\xd7\xb9p'
        cipher = AES.new(key, AES.MODE_EAX, nonce)
        data = cipher.decrypt_and_verify(ciphertext, tag)
        
        keyAPI = data.decode()
        return keyAPI

    def getCurrentTime(self):
        dt = (datetime.now()).strftime("%Y%m%dT%H%M%S")
        return str(dt)

    def dateTrainScreen(self,horaire):
        date = horaire.split("T")
        hTrain = ( (date[1])[0] + (date[1])[1] + "H" + (date[1])[2] + (date[1])[3] )
        return hTrain

    def getListTrain(self,response):
        trainList = []
        convertToJson = json.dumps(response.json(),sort_keys=True, indent=4)
        jsonDict = json.loads(convertToJson)
        for element in (jsonDict["departures"]):
            horaire= self.dateTrainScreen((element["stop_date_time"])["arrival_date_time"])
            tDict = {"direction":(element["display_informations"])["direction"],
                     "name":(element["display_informations"])["name"],
                     "type_train":(element["display_informations"])["commercial_mode"],
                     "number":(element["display_informations"])["headsign"],
                     "horaire":horaire,
                     "description":(element["display_informations"])["description"],
                     "text_color":(element["display_informations"])["text_color"]}
            trainList.append(tDict)
        print(jsonDict["disruptions"])
        return trainList

    def getInfoArrival(self,gare):
        strRequest = self.url + ("/coverage/sncf/stop_areas/stop_area:SNCF:" +gare +"/departures?datetime=" + self.getCurrentTime())
        response = requests.get(strRequest,auth=(self.key,None))
        return self.getListTrain(response)
    
def verifKey(key:str)->bool:
    response = requests.get("https://api.navitia.io/v1/coverage?key="+key)
    convertToJson = json.dumps(response.json(),sort_keys=True, indent=4)
    jsonDict = json.loads(convertToJson)
    if(jsonDict.get("message") is not None):
        return False
    else:
        return True