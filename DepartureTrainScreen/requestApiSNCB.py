import requests
import json
from datetime import datetime, date

class UseApiSNCB:

    def __init__(self,key):
        self.key = key
        self.url = "https://api.sncf.com/v1"

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
                     "horaire":horaire}
            trainList.append(tDict)
        return trainList

    def getInfoArrival(self,gare):
        strRequest = self.url + ("/coverage/sncf/stop_areas/stop_area:SNCF:" +gare +"/departures?datetime=" + self.getCurrentTime())
        response = requests.get(strRequest,auth=(self.key,None))
        return self.getListTrain(response)