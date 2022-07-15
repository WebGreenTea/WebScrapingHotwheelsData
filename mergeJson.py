import json
# import glob

# read_files = glob.glob("*.json")
# output_list = []

# for f in read_files:
#     with open(f, "rb") as infile:
#         output_list.append(json.load(infile))

# with open("merged_file.json", "wb") as outfile:
#     json.dump(output_list, outfile)

FROMYEAR = 1996
UNTILYEAR = 2022
output_list = []
for year in range(FROMYEAR,UNTILYEAR+1):
    file = f'mainline{year}.json'
    with open(file, "r") as infile:
        output_list += json.load(infile)

with open("mainline.json", "w") as outfile:
    json.dump(output_list, outfile)
