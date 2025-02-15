import json 
import sys

L = []

for year in range(1996,2022+1):
    with open(f'mainline{year}.json', encoding='utf-8') as data_file:
        data = json.loads(data_file.read())

        for d in data :
            # print(year,"----",len(d['ChaseCar']))
            # if(len(d['ChaseCar'])> 1):
            #     sys.exit()

            if(d['ChaseCar'] not in L and len(d['ChaseCar']) > 0):
                print(d['ChaseCar'])
                L.append(d['ChaseCar'])
                if(d['ChaseCar'][0] == "Super Ultimate Chase"):
                    print(year,"--",d['ToyID'])
                    sys.exit()

print(L)