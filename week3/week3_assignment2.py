# 連線先取得最新的3個page的網址
import urllib.request as req
url = "https://www.ptt.cc/bbs/Lottery/index.html"
request = req.Request(url, headers={
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
})
with req.urlopen(request) as reponse:
    data = reponse.read().decode("utf-8")


import bs4
root = bs4.BeautifulSoup(data, "html.parser")
pages = root.find_all("a", class_="wide")
secound_page = pages[1].get('href')
secound_page_index = secound_page[18:22]

target_pages = ['https://www.ptt.cc/bbs/Lottery/index.html']
target_pages.append("https://www.ptt.cc/bbs/Lottery/index" + secound_page_index +".html")
target_pages.append("https://www.ptt.cc/bbs/Lottery/index" + str(int(secound_page_index)-1) +".html")


# 找出每一個page底下的文章url
def getPagesUrl(url):
    request = req.Request(url, headers={
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
    })
    with req.urlopen(request) as response:
        data = response.read().decode('utf-8')
    root = bs4.BeautifulSoup(data, 'html.parser')
    titles = root.find_all("div", class_="title")
    url_list = []
    for x in titles:
        if x.a != None:
            url = "https://www.ptt.cc" + x.a.get('href')
            url_list.append(url)
    return url_list


url_list = []
for url in target_pages:
    sublist = getPagesUrl(url)
    url_list.extend(sublist)

# 找出每一個文章url的info
def getContentInfo(url):
    import urllib.request as req
    request = req.Request(url, headers={
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
    })
    with req.urlopen(request) as response:
        context_data = response.read().decode("utf-8")


    # 透過bs4解析資料
    import bs4
    root = bs4.BeautifulSoup(context_data, "html.parser")

    # 取得title與create_time
    time_tag = root.find_all("span", class_="article-meta-value")
    title = root.title.string
    index = title.find(' - 看板 Lottery - 批踢踢實業坊')
    title = title[:index]
    if time_tag == []:
        create_time = ''
    else:
        create_time = time_tag[3].string

    # 找到推與噓的標籤物件
    like = root.find_all("span", class_="hl push-tag")
    dislike = root.find_all("span", class_="f1 hl push-tag")

    # 計算推與噓的數量
    count = {}
    for x in like:
        if x.string not in count:
            count[x.string] = 1
        else:
            count[x.string] += 1
    for x in dislike:
        if x.string == "→ ":
            pass
        elif x.string not in count:
            count[x.string] = 1
        else:
            count[x.string] += 1
        
    if '推 ' not in count:
        count['推 '] = 0
    if '噓 ' not in count:
        count['噓 '] = 0

    info = [title, count['推 '] + count["噓 "], create_time]
    return info

info_lists = []
for url in url_list:
    info = getContentInfo(url)
    info_lists.append(info)

# 存入CSV
import csv
with open('article.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(info_lists)