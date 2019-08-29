from requests import get
from bs4 import BeautifulSoup
from pymongo import MongoClient
import json

class EspnCricinfo():
    response=""
    soup=""

    def __init__(self, match_id):
        result = get("https://www.espncricinfo.com/series/19430/scorecard/" + str(match_id))
        self.response = result.content

    def parse_page(self, show_html=False):
        self.soup = BeautifulSoup(self.response, 'html.parser')

        if show_html:
            print(self.soup.prettify())

    def get_scorecard(self):
        matches = self.soup.find_all("div", {"class": "wrap batsmen"})

        for m in matches:
            details = m.find_all('div')
            for d in details:
                print(d.get_text(), end="\t")
            print("\n")

        dnb = self.soup.find_all("div", {"class": "wrap dnb"})

        fow = ""
        for r in dnb:
            data = r.find("div").get_text().strip()
            fows = data.split(":")
            if not (fows[1].strip()[0].isalpha()):
                fow += fows[1].strip() + "|"

        print(fow)


class Cricbuzz():
    __url_cricbuzz = "https://www.cricbuzz.com"
    __archives_path="/cricket-scorecard-archives/"
    __page = ""
    __response = ""
    __year=""
    __series_path=""
    client = ""
    db = ""

    def __init__(self, year):
        self.client = MongoClient()
        self.db = self.client['cricket_db']
        self.__year=year
        self.__archives_path += str(self.__year)

    def __get_content(self, data):
        self.__response = get(self.__url_cricbuzz + data).content
        self.__series_path=data

    def get_series_lists(self):
        self.__get_content(self.__archives_path)
        self.__page = BeautifulSoup(self.__response, "html.parser")
        series_list = self.__page.find_all("a", {"class": "text-hvr-underline"})
        series_dict = {}
        for list in series_list:
            if list.get("href")[0:2] != "ht":
                series_dict[list.get_text()]=list.get("href")
                series_collection = self.db.series
                series_collection.insert_one(json.loads(json.dumps({"series_name": list.get_text(), "year": self.__year, "url":self.__url_cricbuzz, "path":list.get("href")})))
        return series_dict

    def get_match_lists(self, series):
        self.__get_content(series)
        self.__page = BeautifulSoup(self.__response, "html.parser")
        matches_list = self.__page.find_all("a", {"class": "text-hvr-underline"})
        matches_dict = {}
        for list in matches_list:
            if list.get("href")[0:2] != "ht":
                matches_dict[list.get_text()] = {"url": list.get("href").replace("cricket-scores","live-cricket-scorecard")}
                series_collection = self.db.series
                series_id = series_collection.find_one({"path": self.__series_path}).get("_id")
                matches_collection = self.db.matches
                matches_collection.insert_one(json.loads(json.dumps(
                    {"series_id":str(series_id),"match_name": list.get_text(), "year": self.__year,
                     "url": self.__url_cricbuzz, "path": list.get("href").replace("cricket-scores","live-cricket-scorecard")})))
        return matches_dict

    def get_scorecard(self, match):
        self.__get_content(match)
        self.__page = BeautifulSoup(self.__response, "html.parser")
        fows = self.__page.find_all("div", {"class": "cb-col cb-col-100 cb-scrd-sub-hdr cb-bg-gray text-bold"})
        fow_data = [g.find_next("div").get_text() for g in fows]

        fows_list = []

        for f in fow_data:
            fows = []
            g = f.split(",")
            for gg in g:
                hj = gg.strip().replace("(", "").replace(")", "").split(" ", 1)
                for jj in hj:
                    fows.append(jj)
            fows_list.append(fows)

        match_details = self.__page.find_all("div", {"class": "cb-col cb-col-100 cb-mtch-info-itm"})
        details = {}
        for ggh in match_details:
            child_items = ggh.find_all("div")
            details[child_items[0].get_text().strip()]=child_items[1].get_text().strip()

        innings = self.__page.select("div[id^='innings']")
        inn = {}
        in_count = 0
        for i in innings:
            scores = i.find_all("div", {"class": "cb-scrd-itms"})
            batsmen = True
            bowler = False
            dnb = False
            batting = []
            bowling = []
            extra = []
            total = []
            for sb in scores:
                if (sb.get_text().strip().startswith("Extras")):
                    batsmen = False
                    ex = [g.get_text().strip() for g in sb.find_all("div")]
                    extra.append({
                        "extras": ex[1],
                        "count": ex[2]
                    })

                if bowler:
                    bowl = [g.get_text().strip() for g in sb.find_all("div")]
                    bowling.append(
                        {
                            "bowler": bowl[0],
                            "overs": bowl[1],
                            "maidens": bowl[2],
                            "runs": bowl[3],
                            "wickets": bowl[4],
                            "no_ball": bowl[5],
                            "wide": bowl[6],
                            "economy": bowl[7]
                        }
                    )
                    matches_collection = self.db.matches
                    match_id = matches_collection.find_one({"path": self.__series_path})
                    bowler_collection = self.db.bowler
                    bowler_collection.insert_one(json.loads(json.dumps(
                        {"series_id": match_id.get("series_id"), "match_id": str(match_id.get("_id")),
                         "match_name": match_id.get("match_name"), "year": self.__year,
                         "name": bowl[0], "runs": bowl[3],
                         "wickets": bowl[4], "maidens": bowl[2], "no_ball": bowl[5], "wide": bowl[6], "economy": bowl[7], "overs":bowl[1]})))
                if dnb:
                    bowler = True

                if batsmen:
                    bat = [g.get_text().strip() for g in sb.find_all("div")]

                    batting.append(
                        {
                            "batsmen": bat[0],
                            "how_out": bat[1],
                            "runs": bat[2],
                            "balls_faced": bat[3],
                            "fours": bat[4],
                            "sixes": bat[5],
                            "SR": bat[6]
                        }
                    )
                    matches_collection = self.db.matches
                    match_id = matches_collection.find_one({"path": self.__series_path})
                    batsmen_collection = self.db.batsmen
                    batsmen_collection.insert_one(json.loads(json.dumps(
                        {"series_id": match_id.get("series_id"), "match_id": str(match_id.get("_id")),
                         "match_name": match_id.get("match_name"), "year": self.__year,
                         "name": bat[0], "runs":bat[2], "balls_faced":bat[3],
                         "fours":bat[4], "sixes": bat[5], "SR":bat[6]})))


                if (sb.get_text().strip().startswith("Total")):
                    dnb = True
                    tot = [g.get_text().strip() for g in sb.find_all("div")]
                    total.append({
                        "total": tot[1],
                        "wickets_overs": tot[2]
                    })
            try:
                inn["innings_" + str(in_count)] = {
                    "batting": batting,
                    "bowling": bowling,
                    "extras": extra,
                    "total": total,
                    "fow": fows_list[in_count]
                }
            except:
                inn["innings_" + str(in_count)] = {
                    "batting": batting,
                    "bowling": bowling,
                    "extras": extra,
                    "total": total,
                    "fow": ""
                }
            in_count += 1
        inn["match_info"]=details
        matches_collection = self.db.matches
        match_id = matches_collection.find_one({"path": self.__series_path})
        scorecard_collection = self.db.scorecard
        scorecard_collection.insert_one(json.loads(json.dumps(
            {"series_id": match_id.get("series_id"), "match_id": str(match_id.get("_id")),
             "match_name": match_id.get("match_name"), "year": self.__year,
             "scorecard":inn})))
        return inn
#****************************************************************************************
