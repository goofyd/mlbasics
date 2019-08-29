from cricket.Scorecard_Scraper import EspnCricinfo

match_id = [1188625, 1152848]

for m in match_id:
    cric = EspnCricinfo(m)
    cric.parse_page()
    cric.get_scorecard()
    print("**********************************************")