import time
import json
from requests_html import HTMLSession
import bs4


YEAR = 2018
EXCLUSIVE = ['Target Exclusive', 'Walmart Exclusive',
    'Dollar General Exclusive', 'Kroger Exclusive', 'GameStop Exclusive','Costco exclusive','Sam\'s Club Exclusive','Kmart Exclusive','Toys R Us Exclusive','Toys R Us Promo','Walgreens Exclusive']
NEW = ['New for 2021!', 'New in Mainline','New In Mainline','New for 2013!','2014 New Models','New for 2015!','2016 New Models','New for 2017!','New for 2018!','New for 2019!','New for 2020!','New Model','Ryu\'s Rides','New for 2022!']
CHASE = ['Super Treasure Hunt', 'Treasure Hunts','Treasure Hunt','Hot Wheels id'] 


#for check Duplicate 
TOYID = []
MODELNAME=[]
def isDuplicate(toyid,name):
    try:    
        if(TOYID.index(toyid) == MODELNAME.index(name)):
            return True
        else:
            TOYID.append(toyid)
            MODELNAME.append(name)
        return False
    except:
        TOYID.append(toyid)
        MODELNAME.append(name)
        return False
    

#for get all data from wiki
def getDataFromYear(year):
    #filter for some year before start
    #<=2012
    if(year<=2012):
        NEW.remove("New Model")

    #start
    session = HTMLSession()
    url = f'https://hotwheels.fandom.com/wiki/List_of_{year}_Hot_Wheels'
    r = session.get(url)
    soup = bs4.BeautifulSoup(r.html.raw_html, "html.parser")
    tables = soup.find_all('table')
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            colums = row.find_all('td')
            try:
                if(( len(colums) > 2 and not("Photo" in (str(colums[len(colums)-1].text).strip()))) ):
                    CarNumber = str(colums[1].text).strip()
                    if(not(CarNumber.isdigit())):
                        CarNumber = ''

                    #get series and image url
                    SeriesNumber = ''
                    try:
                        SeriesNumber = str(colums[4].text).strip().replace('\u200b', '')
                        imgUrl = str(colums[5].find('a')['href']).strip()
                    except:
                        SeriesNumber = ''
                        imgUrl = str(colums[4].find('a')['href']).strip()

                    #get series name, exclusive, chaseCar, newcar text
                    series = str(colums[3].text).strip()
                    
                    exclusive = []
                    newcar = []
                    chaseCar = []
                    #find exclusive in series column and cut it
                    for exc in EXCLUSIVE:
                        if (exc in series):
                            exclusive.append(exc)
                            l = series.split(exc)
                            series = " ".join(l).strip()

                    #find newcar_text in series column and cut it
                    for new in NEW:
                        if (new in series):
                            newcar.append(new)
                            l = series.split(new)
                            series = " ".join(l).strip()

                    #find chase_text in series column and cut it
                    for chase in CHASE:
                        if (chase in series):
                            # chaseCar.append(chase)
                            l = series.split(chase)
                            if('Hot Wheels id' in chase):
                                series = series.strip()
                            elif(year<=2012):
                                if(not(" ".join(l).strip()[0].isdigit())):
                                    series = " ".join(l).strip()
                                else:
                                    series = f'{year} Treasure Hunts Series'
                                break
                            else:
                                series = " ".join(l).strip()
                            if(chase == "Super Treasure Hunts" or chase == "Treasure Hunts"):
                                chase = chase[:-1]
                            chaseCar.append(chase)
                    
                    #get ToyID and ModelName
                    Toyid = str(colums[0].text).strip()
                    modelName = str(colums[2].text).strip()

                    #check duplicate
                    if(isDuplicate(Toyid,modelName)):
                        print(f'{Toyid} {modelName} is dupicate!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')


                    #filter for some year after scrap
                    #2000
                    if(YEAR == 2000 and (series == "2000 Virtual Collection" or series == "2000 Hot Wheels")):
                        SeriesNumber = ''
                    #2001
                    if(YEAR == 2001 and len(exclusive) > 0 and (exclusive[0] == 'Costco exclusive' or exclusive[0] == 'Sam\'s Club Exclusive')):
                        series = '2001 Hot Wheels'
                    #2018
                    if(YEAR == 2018 and Toyid == "FTT37"):
                        exclusive.append("Super Ultimate Chase")

                    item = {
                        # "id": ID+("{:04d}".format(numID)),
                        "YEAR": year,
                        "ToyID": Toyid,
                        "NumbersInYear": CarNumber,
                        "ModelName": modelName,
                        "Series": series,
                        "SeriesNumber": SeriesNumber,
                        "ChaseCar": chaseCar,
                        "Exclusive": exclusive,
                        "img_url": imgUrl
                    }
                    print(f'{series}')
                    # print(f'{Toyid}\t{modelName}\t\t\t\t{series}\t\t{SeriesNumber}')
                    print('-------------------------------------------')

                    #print(item)

                    yield item
            except Exception as e:
                print(e)



# getDataFromYear(YEAR)

allDataInYear = [item for item in getDataFromYear(YEAR)]
with open(f"data/mainline{YEAR}.json", "w") as outfile:
    json.dump(allDataInYear, outfile)