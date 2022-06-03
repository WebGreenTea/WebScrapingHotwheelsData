from requests import session
from requests_html import HTMLSession
import bs4
import pymongo
import os
from dotenv import load_dotenv 
import time
load_dotenv()
DATABASEURI=os.getenv("DATABASEURI")
client = pymongo.MongoClient(DATABASEURI)
db = client.get_database('HotWheels')
records = db.Mainline

print(records.count_documents({}))


FROMYEAR=1996
UNTILYEAR=2022

def getDataFromYear(year):

    session = HTMLSession()
    

    url = f'https://hotwheels.fandom.com/wiki/List_of_{year}_Hot_Wheels'

    r = session.get(url)
    #r.html.render(sleep=1)
    soup = bs4.BeautifulSoup(r.html.raw_html,"html.parser")

    tables = soup.find_all('table')

    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            colums = row.find_all('td')
            try:
                #print(str(colums[len(colums)-1].text).strip())
                lastcol=str(colums[len(colums)-1].text).strip()

                if((not("Photo" in lastcol)) and len(colums)>2):
                    CarNumber=str(colums[1].text).strip()
                    if(not(CarNumber.isdigit())):
                        CarNumber=''

                    # SeriesNumber=str(colums[4].find('a')['href']).strip()
                    # if(SeriesNumber):
                    #     imgUrl=SeriesNumber
                    #     SeriesNumber=''

                    
                    try:
                        SeriesNumber=str(colums[4].text).strip()
                        imgUrl=str(colums[5].find('a')['href']).strip()
                    except:
                        SeriesNumber=''
                        imgUrl=str(colums[4].find('a')['href']).strip()

                    item = {
                        "YEAR":year,
                        "ToyID":str(colums[0].text).strip(),
                        "CarNumber":CarNumber,
                        "ModelName":str(colums[2].text).strip(),
                        "Series":str(colums[3].text).strip(),
                        "SeriesNumber":SeriesNumber,
                        "img_url":imgUrl
                    }
                    #print(item)
                
                    yield item
            except Exception as e: print(e)
            
            
for year in range(FROMYEAR,UNTILYEAR+1):    
    records.insert_many([item for item in getDataFromYear(year)])
    time.sleep(1)
    print(f'{year} complate')
#     for item in getDataFromYear(year):
#         print(item)

    
    




