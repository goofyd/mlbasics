from bs4 import BeautifulSoup
from requests import get
import json
from pymongo import MongoClient

class ClearTrip():

    __url = ""
    __client = ""
    __db = ""
    __response = ""
    __page= ""

    def __init__(self):
        self.__url = "https://www.cleartrip.com"
        self.__client = MongoClient()
        self.__db = self.__client['indian_railways_db']

    def __get_page_content(self, path):
        self.__response = get(self.__url+str(path))

    def get_train_details(self, pageno):
        self.__get_page_content("/trains/list?page="+str(pageno))
        self.__page = BeautifulSoup(self.__response.content, "html.parser")
        table = self.__page.find("table", {"class": "results"})
        rows = table.find_all("tr")
        train_nos = []
        for r in rows:
            cols = r.find_all("td")
            train_details = []
            train_keys = ["train_no", "train_path", "train_name", "start_station_path", "start_station_name", "end_station_path", "end_station_name"]
            if cols is not None:
                for c in cols:
                    if c.find("a") is not None:
                        train_details.append(c.find("a").get("href").strip())
                    train_details.append(c.get_text().strip())
            if not train_details == []:
                train_collection = self.__db.trains
                result = dict(zip(train_keys, train_details))
                result['url'] = self.__url
                train_collection.insert_one(json.loads(json.dumps(result)))
                train_nos.append(result['train_no'])
        return train_nos

    def get_train_route(self, train_no):
        self.__get_page_content("/trains/" + str(train_no))
        self.__page = BeautifulSoup(self.__response.content, "html.parser")
        table = self.__page.find("table", {"class": "results"})
        rows = table.find_all("tr")
        train_info = []
        train_title = self.__page.find("h1").get_text().strip().replace("\n","")
        train_info.append(train_title)
        out = {}
        route=[]
        try:
            train_details = self.__page.find("ul", {"class": "list-unstyled info-summary"})
            for detail in train_details.find_all("li"):
                train_info.append(detail.get_text().strip().replace("\n",""))
        except:
            for x in range(0,3):
                train_info.append("")

        train_info_title = ["train_name", "classes", "service_days", "other_info"]
        train_info_dict = dict(zip(train_info_title, train_info))

        for r in rows:
            cols = r.find_all("td")
            train_details = []
            train_keys = ["s_no", "station_name (code)", "arrives", "departs", "stop_time",
                          "distance_travelled", "day", "route"]
            if cols is not None:
                for c in cols:
                    train_details.append(c.get_text().strip())
            if not train_details == []:
                result = dict(zip(train_keys, train_details))
                route.append(result)
        train_route_collection = self.__db.train_route
        out['train_route'] = route
        out['url'] = self.__url
        out['train_info'] = train_info_dict
        out['train_no'] = train_no
        train_route_collection.insert_one(json.loads(json.dumps(out)))
