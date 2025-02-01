import urllib.request as request
import json
src = "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1"
with request.urlopen(src) as response:
    data = json.load(response)
splist = data["data"]["results"]

# 將資料存成lists of list，且圖片只取第一張
all_info = []
for spot in splist:
    spot_info = []
    for value in spot.values():
        # 判斷value有無jpg，有=>只取第一個
        if str(value).lower().find('jpg') != -1:
            jpg_adjust = value[:(str(value).lower().find('jpg')+len('jpg'))]
            spot_info.append(jpg_adjust)
        elif str(value).find('jpg') == -1:
            spot_info.append(value)
    all_info.append(spot_info)


# 匯入assignment 2，mapping行政區
src2 = 'https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-2'
with request.urlopen(src2) as file:
    data2 = json.load(file)
mrt_list = data2['data']


all_info_2 = []
for spot in mrt_list:
    spot_info = []
    for value in spot.values():
        spot_info.append(value)
    all_info_2.append(spot_info)

# 增加行政區
for info in all_info_2:
    info.append(info[2][5:8])

# 進行mapping
import copy
all_info_3 = copy.deepcopy(all_info)
for i in all_info_3:
    for j in all_info_2:
        if i[7] == j[1]:
            i.append(j[0])
            i.extend(j[2:])

# 選擇需要的欄位
selected_columns = [1, 21, 3, 15, 13]
selected_info = []
for spot in all_info_3:
    select = []
    for index in selected_columns:
        select.append(spot[index])
    selected_info.append(select)

# 存成csv檔案
import csv
with open('spot.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(selected_info)


# 各地區景點
mrt = {}
for spot in all_info_3:
    if spot[19] in mrt:
        mrt[spot[19]].append(spot[1])
    elif spot[10] not in mrt:
        mrt[spot[19]] = []
        mrt[spot[19]].append(spot[1])

mrt = [[key] + value for key, value in mrt.items()]
with open('mrt.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(mrt)

