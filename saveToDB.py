import mysql.connector
import json
connection  = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database='hw_collections'
)
db = connection.cursor()
YEAR = 2022
data = []
with open(f'./data/mainline{YEAR}.json', encoding='utf-8') as data_file:
   data = json.loads(data_file.read())
# print(data[70]['YEAR'])


# db.execute("INSERT INTO chase_type (title) VALUES (%s),(%s)", ("Super Treasure Hunt","Treasure Hunt"))
connection.commit()



for d in data:
    chaseCar = d['ChaseCar'][0]
    exclusive = d['Exclusive']
    year = d['YEAR']
    toyID = d['ToyID']
    NumbersInYear = int(d['NumbersInYear'])
    ModelName = d['ModelName']
    SeriesName = d['Series']
    SeriesNumber = str(d['SeriesNumber'])
    Image = d['img_url']
    exIDtoMap = []
    serieFK = None
    chaseFK = None

    #check and insert exclusive data
    if(len(exclusive) > 0):
        sqlCommand = ""
        sqlValue = ()
        # print(exclusive)
        if(len(exclusive) > 1):
            sqlCommand = 'SELECT exclusive_id,title FROM exclusive WHERE title IN ('
            for ex in exclusive:
                sqlCommand+=f'%s,'
                sqlValue+= ex,
            sqlCommand = sqlCommand[:-1]+")"
        else:
            sqlCommand = 'SELECT exclusive_id,title FROM exclusive WHERE title=%s'
            sqlValue+=exclusive[0],
        # print(sqlCommand)
        # print(sqlValue)
        db.execute(sqlCommand,sqlValue)
        Result = db.fetchall()
        print(Result)
        for row in Result:
            exIDtoMap.append(row[0])
        if(len(Result) != len(exclusive)):#insert new exclusive
            newEx = list(set(exclusive)-set(Result))
            for ex in newEx:
                db.execute("INSERT INTO exclusive (title) VALUES (%s)",(ex,))
                exIDtoMap.append(db.lastrowid)
            # print(sqlCommand)
            # print(sqlValue)

    #check and insert series
    if(SeriesName!=""):
        Result = []
        sqlCommand =  'SELECT series_mainline_id,title FROM series_mainline WHERE year=%s AND title=%s'
        sqlValue = (year,SeriesName)
        db.execute(sqlCommand,sqlValue)
        Result = db.fetchall()
        if(len(Result) > 0):
            serieFK = Result[0][0]
        else:
            maxofSeries = None
            if(SeriesNumber.find("/") != -1):
                maxofSeries = SeriesNumber.split('/')[1]
            db.execute("INSERT INTO series_mainline (title,max,year) VALUES (%s,%s,%s)",(SeriesName,maxofSeries,year))
            serieFK = db.lastrowid


    #check and insert chase
    if(chaseCar != ""):
        Result = []
        sqlCommand =  'SELECT chase_type_id,title FROM chase_type WHERE title=%s'
        sqlValue = (chaseCar,)
        db.execute(sqlCommand,sqlValue)
        Result = db.fetchall()
        if(len(Result) > 0):
            chaseFK = Result[0][0]
        else:
            db.execute("INSERT INTO chase_type (title) VALUES (%s)",(chaseFK,))
            chaseFK = db.lastrowid

    #insert to hw_mainline
    db.execute("INSERT INTO hw_mainline (year,toy_id,number_in_year,model_name,series_mainline_id,number_in_series,img_url,chase_type_id)",(year,toyID,NumbersInYear,ModelName,serieFK))

    # connection.commit()
    print("------")
        
                



