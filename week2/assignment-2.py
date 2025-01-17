# Task1
print("====Task1====")
def find_and_print(messages, current_station):
    # your code here
    mrt_station_code = {
    "Xindian": 1,
    "Xindian City Hall":2,
    "Qizhang":3,
    "Xiaobitan": 3,
    "Dapinglin": 4,
    "Jingmei": 5,
    "Wanlong": 6,
    "Gongguan": 7,
    "Taipower Building": 8,
    "Guting": 9,
    "Chiang Kai-Shek Memorial Hall": 10,
    "Xiaonanmen": 11,
    "Ximen": 12,
    "Beimen": 13,
    "Zhongshan": 14,
    "Songjiang Nanjing": 15,
    "Nanjing Fuxing": 16,
    "Taipei Arena": 17,
    "Nanjing Sanmin": 18,
    "Songshan": 19
    }
    # 辨識出訊息中的站名, 紀錄每個朋友的站名
    friend_station = []
    for message in messages.values():
        for station in mrt_station_code:
            if station in message:
                friend_station.append(station)
    
    # 計算雙方的距離
    distance = []
    for index, f_station in enumerate(friend_station):
        diff = abs(mrt_station_code[f_station] - mrt_station_code[current_station])
        # 因為小碧潭在station code與七張相同，因此若其中1方在小碧潭，整體距離要+1
        if current_station == "Xiaobitan" and f_station != "Xiaobitan":
            diff += 1
        elif current_station != "Xiaobitan" and f_station == "Xiaobitan":
            diff += 1
        distance.append(diff)
    # 取得最小的距離
    min_distance = min(distance)
    
    # 找出誰是最小距離，先找出index，再用index印出
    for index, value in enumerate(distance):
        if value == min_distance:
            name_list = list(messages)
            print(name_list[index])

messages={
"Leslie":"I'm at home near Xiaobitan station.",
"Bob":"I'm at Ximen MRT station.",
"Mary":"I have a drink near Jingmei MRT station.",
"Copper":"I just saw a concert at Taipei Arena.",
"Vivian":"I'm at Xindian station waiting for you."
}

find_and_print(messages, "Wanlong") # print Mary
find_and_print(messages, "Songshan") # print Copper
find_and_print(messages, "Qizhang") # print Leslie
find_and_print(messages, "Ximen") # print Bob
find_and_print(messages, "Xindian City Hall") # print Vivian


# Task2
print("====Task2====")
def book(consultants, hour, duration, criteria):
    # your code here
    # 建立consultant的busy_hour紀錄
    for consultant in consultants:
        if "busy_hour" not in consultant:
            consultant["busy_hour"] = set()
    # 建立客人希望的時段, customer_hour
    customer_hour = set()
    for i in range(duration):
        customer_hour.add(hour+i)
    # 選出時段可以的consultant
    available_consultant = []
    for index, consultant in enumerate(consultants):
        if (consultant["busy_hour"] & customer_hour) == set():
            available_consultant.append(index)
    # 根據criteria媒合consultant
    if len(available_consultant) == 0:
        # 印出結果
        print("No Service")
    elif criteria == "price":
        price = []
        for i in available_consultant:
            price.append(consultants[i]["price"])
        min_price = min(price)
        for i in available_consultant:
            if consultants[i]["price"] == min_price:
                # 印出結果
                print(consultants[i]["name"])
                # 更新consultant的busy_hour
                consultants[i]["busy_hour"] = consultants[i]["busy_hour"].union(customer_hour)
                break
    elif criteria == "rate":
        rate = []
        for i in available_consultant:
            rate.append(consultants[i]["rate"])
        max_rate = max(rate)
        for i in available_consultant:
            if consultants[i]["rate"] == max_rate:
                # 印出結果
                print(consultants[i]["name"])
                # 更新consultant的busy_hour
                consultants[i]["busy_hour"] = consultants[i]["busy_hour"].union(customer_hour)
                break

consultants=[
{"name":"John", "rate":4.5, "price":1000},
{"name":"Bob", "rate":3, "price":1200},
{"name":"Jenny", "rate":3.8, "price":800}
]

book(consultants, 15, 1, "price") # Jenny
book(consultants, 11, 2, "price") # Jenny
book(consultants, 10, 2, "price") # John
book(consultants, 20, 2, "rate") # John
book(consultants, 11, 1, "rate") # Bob
book(consultants, 11, 2, "rate") # No Service
book(consultants, 14, 3, "price") # John


# Task3
print("====Task3====")
def func(*data):
# your code here
    middle = []
    # 取得每一個名字的middle name, ["大", "明", "明"]
    for name in data:
        if len(name) >= 4:
            middle.append(name[2])
        elif len(name) >= 2:
            middle.append(name[1])
    
    count = []
    for i in middle:
        count.append(middle.count(i))
    
    if 1 not in count:
        print("沒有")
    else:
        text = ""
        for index, i in enumerate(count):
            if i == 1:
                text = text + data[index] + " "
        text = text.strip()
        print(text)



# 取得每一個名字的middle name, ["大", "明", "明"]
# 計算每一個middle name出現次數, {"大":1, "明":2}
# 取得只出現1次的的middle name, ["大"]
# 只出現1次的middle name, 在原本list的index, [0]
# 印出原data[0]


func("彭大牆", "陳王明雅", "吳明") # print 彭大牆
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花") # print 林花花
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花") # print 沒有
func("郭宣雅", "夏曼藍波安", "郭宣恆") # print 夏曼藍波安


# Task4
print("====Task4====")
def get_number(index):
# your code here
    quotient = index // 3
    remainder = index % 3
    number = (4+ 4 -1) * quotient + 4 * remainder
    print(number)


get_number(1) # print 4
get_number(5) # print 15
get_number(10) # print 25
get_number(30) # print 70