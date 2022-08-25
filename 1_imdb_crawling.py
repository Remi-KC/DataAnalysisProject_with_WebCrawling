import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup 
import time

# 設定路徑
path1 = "/Users/remikc/Programming/Python/DA_Project/Data/"

#%%
# 讀取檔案
netflix = pd.read_csv(path1+"netflix_titles.csv")
disney = pd.read_csv(path1+"disney_titles.csv")

# 增加平台標籤欄位
netflix.insert(0,"platform","Netflix")
disney.insert(0,"platform","Disney+")

# 合併兩資料集，使同樣流程可以一起處理
data = pd.concat([netflix, disney]).reset_index(drop=True)

# copy data["title"] to data["search"]
data["search"] = data["title"]

# 新增tconst欄位，預備加入爬取的IMDb_id
data["tconst"]=np.nan

#%% IMDb網頁觀察
'''
用片名(One Piece)搜尋IMDb，觀察IMDb搜尋結果網址
https://www.imdb.com/find?q=One+Piece&ref_=nv_sr_sm
1.發現網址規律 https://www.imdb.com/find?q=搜尋詞&ref_=nv_sr_sm
2.空白會被取代為"+"
'''
# regex--繼續觀察網址中，哪些符號會被替換掉，依此設定regex修改字串
data = data.replace({"search":{r'\s':"+",
                               r':':"%3A",
                               r'\(':"%28",
                               r'\)':"%29",
                               r',':"%2C",
                               r'\'':"%27",
                               r'&':"%26",
                               r'\?':"%3F",
                               r'!':"%21"}}, regex=True)

data.to_csv(path1+"data.csv", index=False)

#%% 爬蟲程式碼

for i in range(len(data)):
    url = "https://www.imdb.com/find?q=%s&ref_=nv_sr_sm" % data["search"][i]

    try:
        print("------index:%d------" % i)
        res = requests.get(url)
        if res.status_code == 200:
            print("%s 取得網頁內容成功" % data["title"][i])
            bs = BeautifulSoup(res.text, "lxml")
            # 判斷是否有搜尋結果
            if bs.h1.text.split()[0] == "Results":
                print("%s imdb_id查找中..." % data["title"][i])
                tconst = bs.find("td",{"class":"result_text"}).a.get("href").split("/")[2]     
                data["tconst"][i] = tconst
                print("tconst %s 加入成功！" % tconst)
                # 每加一筆資料都存檔，避免spyder突然閃退資料都沒存到
                data.to_csv(path1+"data_imdb.csv", index=False)
                print("寫入檔案成功！")
            else:
                print("%s 查無imdb資料" % data["title"][i])    
        else:
            print("%s 取得網頁內容失敗" % data["title"][i])
    # 例外處理
    except Exception as e:
        print("Error: There's something wrong...")
        print(repr(e))
    # 每查一筆休息5秒
    finally:
        time.sleep(5)
        

