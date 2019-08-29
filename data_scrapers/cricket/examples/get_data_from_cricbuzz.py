from cricket.Scorecard_Scraper import Cricbuzz
import json
import logging
import math
from pymongo import MongoClient

years_to_process=[1999]

#file = open("extracted_data.json", "w")
#file.close()

logging.basicConfig(filename="cricket_data_extractor.log", format='%(asctime)s %(message)s', level=logging.INFO)
logging.info("starting to log")
logging.info("***************************************starting********************************************")


for y in years_to_process:
    extracter=Cricbuzz(y)
    logging.info("__________________" + "Extracting Series for year :" + str(y) + "___________________")
    series = extracter.get_series_lists()
    logging.info(series)
    logging.info("__________________"+"Extracted Series for year :" + str(y) + "___________________")
    logging.info("total_series: "+ str(len(series)))
    matches = {}
    se=1
    loader="#"
    blank= "_"
    for s,m in series.items():
        matches[s]=extracter.get_match_lists(m)
        logging.info("\t"+s+" series_extracted: " + str(se) + "/" + str(len(series)) + " " +" ["+loader*(se)+ blank*(len(series)-se)+"]"+str(math.floor((se / len(series)) * 100))+"%")
        print(s+" series_extracted: " + str(se) + "/" + str(len(series)) + " " +" ["+loader*(se)+ blank*(len(series)-se)+"]"+str(math.floor((se / len(series)) * 100))+"%")
        logging.info("\t"+"matches in current series "+s+" : "+str(len(matches[s])))
        print("matches in current series "+s+" : "+str(len(matches[s])))
        n=1
        for mat, data in matches[s].items():
            result = extracter.get_scorecard(data["url"])
            matches[s][mat]['match_details']=result
            logging.info("\t"+"\t"+mat+" matches_extracted: "+str(n)+"/"+str(len(matches[s]))+" "+" ["+loader*(n)+ blank*(len(matches[s])-n)+"]"+str(math.floor((n/len(matches[s]))*100))+"%")
            print(mat+" matches_extracted: "+str(n)+"/"+str(len(matches[s]))+" "+" ["+loader*(n)+ blank*(len(matches[s])-n)+"]"+str(math.floor((n/len(matches[s]))*100))+"%")
            n+=1
            #with open('extracted_data.json', 'a') as file:
            #    file.write(json.dumps(matches))
        se+=1

logging.info("********************************************stopping***************************************************")
