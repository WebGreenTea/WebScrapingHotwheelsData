from requests import session
from requests_html import HTMLSession
import bs4


'''
def getDataFromYear(year):

    session = HTMLSession()


    url = f'https://hotwheels.fandom.com/wiki/List_of_{year}_Hot_Wheels'

    r = session.get(url)
    #r.html.render(sleep=1)
    
    table = r.html.find('table',first=True)

    row = table.find('tr')




    for i in range(1,len(row)):
        
        #print(row[i].find('td')[0].text)

        yield {
            "Year":year,
            "Toy":row[i].find('td')[0].text,
            "Col":row[i].find('td')[1].text,
            "ModelName":row[i].find('td')[2].text,
            "Series":row[i].find('td')[3].text,
            "SeriesNumber":row[i].find('td')[4].text,
            "img_url":row[i].find('td')[5].find('a',first=True).attrs['href']
        }



for i in getDataFromYear(1995):
    print(i)
'''


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
                CarNumber=str(colums[1].text.strip())
                if((CarNumber.isdigit())):
                    print(CarNumber)
            except:
                pass
            
            
getDataFromYear(1995)



