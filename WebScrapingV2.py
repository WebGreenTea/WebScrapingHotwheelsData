from firebase_admin import firestore
from firebase_admin import credentials
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
# DATABASEURI=os.getenv("DATABASEURI")
#client = pymongo.MongoClient(DATABASEURI)
#db = client.get_database('HotWheels')
#records = db.Mainline

# print(records.count_documents({}))


# FROMYEAR=2021
# UNTILYEAR=2021


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


YEAR = 2022
EXCLUSIVE = ['Target Exclusive', 'Walmart Exclusive',
    'Dollar General Exclusive', 'Kroger Exclusive', 'GameStop Exclusive','Costco exclusive','Sam\'s Club Exclusive','Kmart Exclusive','Toys R Us Exclusive','Toys R Us Promo','Walgreens Exclusive']
NEW = ['New for 2021!', 'New in Mainline','New In Mainline','New for 2013!','2014 New Models','New for 2015!','2016 New Models','New for 2017!','New for 2018!','New for 2019!','New for 2020!','New Model','Ryu\'s Rides','New for 2022!']
CHASE = ['Super Treasure Hunt', 'Treasure Hunts','Treasure Hunt','Hot Wheels id']  # !!! sth before th only
ID = "ML"+str(YEAR)


TOYID = []
MODELNAME=[]


def isDuplicate(toyid,name):    
    if(toyid in TOYID and name in MODELNAME):
        return True
    else:
        TOYID.append(toyid)
        MODELNAME.append(name)
        return False


def getDataFromYear(year):
    numID = 0
    session = HTMLSession()

    url = f'https://hotwheels.fandom.com/wiki/List_of_{year}_Hot_Wheels'

    r = session.get(url)
    # r.html.render(sleep=1)
    soup = bs4.BeautifulSoup(r.html.raw_html, "html.parser")

    tables = soup.find_all('table')

    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            colums = row.find_all('td')
            try:
                # print(str(colums[len(colums)-1].text).strip())
                lastcol = str(colums[len(colums)-1].text).strip()

                if((not("Photo" in lastcol)) and len(colums) >2):
                    CarNumber = str(colums[1].text).strip()
                    if(not(CarNumber.isdigit())):
                        CarNumber = ''

                    # SeriesNumber=str(colums[4].find('a')['href']).strip()
                    # if(SeriesNumber):
                    #     imgUrl=SeriesNumber
                    #     SeriesNumber=''

                    try:
                        SeriesNumber = str(colums[4].text).strip()
                        imgUrl = str(colums[5].find('a')['href']).strip()
                    except:
                        SeriesNumber = ''
                        imgUrl = str(colums[4].find('a')['href']).strip()

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
                            if('Hot Wheels id' in chase):
                                series = series.strip()
                            elif(YEAR<=2012):
                                series = series.strip()
                                if(YEAR>=2007):
                                    break
                            else:
                                series = " ".join(l).strip()
                    numID += 1
                    Toyid = str(colums[0].text).strip()
                    modelName = str(colums[2].text).strip()

                    if(isDuplicate(Toyid,modelName)):
                        print(f'{Toyid} {modelName} is dupicate!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

                    #filter for some year
                    #2000
                    if(YEAR == 2000 and (series == "2000 Virtual Collection" or series == "2000 Hot Wheels")):
                        SeriesNumber = ''
                    #2001
                    if(YEAR == 2001 and len(exclusive) > 0 and (exclusive[0] == 'Costco exclusive' or exclusive[0] == 'Sam\'s Club Exclusive')):
                        series = '2001 Hot Wheels'

                    item = {
                        "id": ID+("{:04d}".format(numID)),
                        "YEAR": year,
                        "ToyID": Toyid,
                        "NumbersInYear": CarNumber,
                        "ModelName": modelName,
                        "Series": series,
                        "SeriesNumber": SeriesNumber,
                        "ChaseCar": chaseCar,
                        "Exclusive": exclusive,
                        #"NewCar": newcar,
                        "img_url": imgUrl
                    }

                    #print(f'{series}')
                    print(f'{modelName}\t\t\t\t{series}\t\t{SeriesNumber}')
                    print('-------------------------------------------')

                    #print(item)

                    yield item
            except Exception as e:
                print(e)


# get data
allDataInYear = [item for item in getDataFromYear(YEAR)]

# to database
# for data in allDataInYear:
#     db.collection('mainline').add(data)


time.sleep(1)
print(f'{YEAR} complate')
print(f'{len(allDataInYear)} car')  # count of record


# write to json file
with open(f"mainline{YEAR}.json", "w") as outfile:
    json.dump(allDataInYear, outfile)
