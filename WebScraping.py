from requests import session
from requests_html import HTMLSession
import bs4


FROMYEAR=1995
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
                CarNumber=str(colums[1].text).strip()
                if((CarNumber.isdigit())):
                    #print(CarNumber)
                    

                    yield {
                        "YEAR":year,
                        "ToyID":str(colums[0].text).strip(),
                        "CarNumber":CarNumber,
                        "ModelName":str(colums[2].text).strip(),
                        "Series":str(colums[3].text).strip(),
                        "SeriesNumber":str(colums[4].text).strip(),
                        "img_url":str(colums[5].find('a')['href']).strip()
                    }
            except:
                pass
            
            
for year in range(FROMYEAR,UNTILYEAR+1):    
    for item in getDataFromYear(year):
        print(item)



