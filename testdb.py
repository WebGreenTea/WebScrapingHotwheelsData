import pymongo
import os
import re
from dotenv import load_dotenv 


MODELNAME = 'nissan'


load_dotenv()
DATABASEURI=os.getenv("DATABASEURI")
client = pymongo.MongoClient(DATABASEURI)
db = client.get_database('HotWheels')
records = db.Mainline

rgxName = re.compile(f'.*{MODELNAME}.*', re.IGNORECASE)  # compile the regex


for document in (records.find({"$or":[ {"YEAR":2010}, {"YEAR":2021}],'ModelName':rgxName})): 
    print(document)
    