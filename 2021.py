from requests import session
from requests_html import HTMLSession
import bs4
import pymongo
import os
from dotenv import load_dotenv 
import time
import json
import firebase_admin


load_dotenv()
#DATABASEURI=os.getenv("DATABASEURI")
#client = pymongo.MongoClient(DATABASEURI)
#db = client.get_database('HotWheels')
#records = db.Mainline

#print(records.count_documents({}))


#FROMYEAR=2021
#UNTILYEAR=2021


import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


YEAR =  2021


EXCLUSIVE = ['Target Exclusive','Walmart Exclusive','Dollar General Exclusive','Kroger Exclusive','GameStop Exclusive']
NEW = ['New for 2021!','New in Mainline']
CHASE = ['Super Treasure Hunt','Treasure Hunt','Hot Wheels id']#!!! sth before th only

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


                    series = str(colums[3].text).strip()
                    exclusive = []
                    newcar = []
                    chaseCar = []

                    for exc in EXCLUSIVE:
                        if (exc in series):
                            exclusive.append(exc)
                            l = series.split(exc)
                            series = " ".join(l).strip()
                    

                    for new in NEW:
                        if (new in series):
                            newcar.append(new)
                            l = series.split(new)
                            series = " ".join(l).strip()


                    for chase in CHASE:
                        if (chase in series):
                            chaseCar.append(chase)
                            l = series.split(chase)
                            if('Hot Wheels id' in chase ):
                               series =  series.strip()
                            else:
                                series = " ".join(l).strip()
                    
                    item = {
                        "YEAR":year,
                        "ToyID":str(colums[0].text).strip(),
                        "NumbersInYear":CarNumber,
                        "ModelName":str(colums[2].text).strip(),
                        "Series": series,
                        "SeriesNumber":SeriesNumber,
                        "ChaseCar": chaseCar,
                        "Exclusive": exclusive,
                        "NewCar": newcar,
                        "img_url":imgUrl
                    }
                    print(item)
                
                    yield item
            except Exception as e: print(e)
            


#get data
allDataInYear = [item for item in getDataFromYear(YEAR)]


for data in allDataInYear:
    db.collection('mainline').add(data)


time.sleep(1)
print(f'{YEAR} complate')
print(f'{len(allDataInYear)} car')#count of record
    


#write to json file
with open("sample.json", "w") as outfile:
    json.dump(allDataInYear, outfile)
    




