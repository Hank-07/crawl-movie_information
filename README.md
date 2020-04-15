# 電影影評爬取

## 為何做 (心路歷程)
作為學習爬蟲技術的一道較為簡單的題目，爬取靜態網頁，分析其中的tag，找尋想要的資訊  
主要功能:爬取網頁上所有的電影名稱、網址、類型、內容，並上傳到資料庫
## 使用到的Libary
爬蟲:requests、bs4   
資料庫:pymongo  
## 程式分析
程式分為三個部分:爬蟲-處理資料、上傳資料庫 

* 爬蟲-處理資料:
先抓到每個頁面的電影資訊
```python
url = ["https://news.agentm.tw/category/%E9%9B%BB%E5%BD%B1%E5%BD%B1%E8%A9%95/page/{}/"
        .format(pn) for pn in range(1,34)]
for page in url:
    res = requests.get(page).text
    soup = BeautifulSoup(res, "lxml") 
``` 

電影資訊放在class="excerpt-straight"的標籤下方，有網址、名稱、類型，將其變成json格式
```python
for item in soup.find_all(class_="excerpt-straight"):
    movieTag = getType(item)
    content = {
        'href' : item.a['href'],
        'title' : movieTitle(item.text),
        'type' : movieTag
    }
``` 
再爬取頁面中的電影內容，並且加入json當中
```python
res = requests.get(content['href']).text
soup = BeautifulSoup(res, "lxml")
item = soup.find(class_="content")
content['data'] = item.text
con.insert_one(content) #上傳資料的指令
```

* 資料庫的部分:
使用pymongo連接mongoDB
```python
#因為架設在本地，不需要連接伺服器的動作
client = MongoClient()
db = client.get_database(dataBaseName) #要連接的資料庫名稱
collection = db.get_collection(collectionName) #要連接的資料表
```
## 執行方式
```
python movie.py
```

## 改進

* 整合資料，可以做為API使用，作為開發推薦系統
