from indian_railways.Trains_Scraper import ClearTrip
import math

list_pages = [5]

loader="*"
blank="_"
for pages in list_pages:
    extracter = ClearTrip()
    trains = extracter.get_train_details(pages)
    print(" Extracting: " + " [" + loader * (pages) + blank * (
                len(list_pages) - pages) + "]" + str(math.floor((pages / len(list_pages)) * 100)) + "%")
    for train in trains:
        extracter.get_train_route(train)
