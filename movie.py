import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient


def movieTitle(item):
    if item.find('《'):
        start = item.find('《')
    else:
        return item
    if item.find('》'):
        pos = item.find('》')
    else:
        return item

    return item[start+1:pos]

def getType(item):
    movieTag = ''
    for tag in item.find(class_="ec-tags").find_all('a'):
        if tag.text.find('片') > 0 and movieTag == '':
            movieTag = movieTag + tag.text
        elif tag.text.find('片') > 0:
            movieTag = movieTag + ',' + tag.text

    if movieTag == '':
        movieTag = item.find(class_="ec-tags").find('a').text
    
    return movieTag

def connect(dataBaseName, collectionName):
    client = MongoClient()
    db = client.get_database(dataBaseName)
    collection = db.get_collection(collectionName)

    return collection


def detailInfo(soup, con):
    for item in soup.find_all(class_="excerpt-straight"):
        movieTag = getType(item)
        content = {
            'href' : item.a['href'],
            'title' : movieTitle(item.text),
            'type' : movieTag
        }
        res = requests.get(content['href']).text
        soup = BeautifulSoup(res, "lxml")
        item = soup.find(class_="content")
        content['data'] = item.text
        con.insert_one(content)


if __name__ == '__main__':
    con = connect('Scrapy', 'Movie')
    
    url = ["https://news.agentm.tw/category/%E9%9B%BB%E5%BD%B1%E5%BD%B1%E8%A9%95/page/{}/"
        .format(pn) for pn in range(1,34)]

    url[0] = "https://news.agentm.tw/category/%E9%9B%BB%E5%BD%B1%E5%BD%B1%E8%A9%95/"
    count = 1
    for page in url:
        try:
            res = requests.get(page).text
            soup = BeautifulSoup(res, "lxml") 
            detailInfo(soup, con)
            print("第{}頁已存儲完成".format(count))
            count+=1
        except:
            print(page)
            count+=1


