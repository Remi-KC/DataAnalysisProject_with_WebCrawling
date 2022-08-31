# Netflix vs Disney+ 影音串流平台比較 
## ---Data Analysis & Web Crawling Project 
<br>

## 一、	研究動機
自己是Netflix用戶，但是今年陸續有看到新聞報導Netflix出現退訂潮，而Disney+訂閱成長快速等消息。為了決定要不要換平台，或者再多訂閱一個平台，我從個人需求出發，在資料中探索Netflix和 Disney+平台內容的差異，並以此為分析主軸。

<br>

## 二、	資料概述
>程式碼請參考：[1_imdb_crawling.py](https://github.com/Remi-KC/DataAnalysisProject_with_WebCrawling/blob/main/1_imdb_crawling.py "看我的程式碼")、[2_data_combining.py](https://github.com/Remi-KC/DataAnalysisProject_with_WebCrawling/blob/main/2_data_combining.py "看我的程式碼")

總共使用三個原始資料集，再加上自己從網站爬取的資料，說明如下：

### 1.Netflix平台影片資料（8807筆）：
* 來源：[Kaggle](https://www.kaggle.com/datasets/shivamb/netflix-shows)
* 欄位：片名、影視分類、影片類型、國家、發行年份、上架日期、影片分級、導演、演員、作品描述
### 2.Disney+平台影片資料（1450筆）：
* 來源：[Kaggle](https://www.kaggle.com/datasets/shivamb/disney-movies-and-tv-shows)
* 欄位：片名、影視分類、影片類型、國家、發行年份、上架日期、影片分級、導演、演員、作品描述
### 3.IMDb影片評分資料（1260065筆）：
* 來源：[IMDb官網](https://www.imdb.com/interfaces/)
* 欄位：影片ID、影片平均評分、影片評分人數
### 4.用平台影片名稱爬取IMDb的影片ID（9907筆）：
* 用途：透過影片ID合併前三個資料集，將IMDb影片評分加入兩份平台資料集
<br>

## 三、	資料清理
>程式碼請參考：[3_cleansing.py](https://github.com/Remi-KC/DataAnalysisProject_with_WebCrawling/blob/main/3_cleansing.py "看我的程式碼")
### 1.	字串處理：
* 國家：只取出第一個主要國家做後續分析 
* 影片類型：以正則表達式清理不需要的修飾詞，並修改雷同的小分類至同一個大類，降低分類數量
* 影片分級：以正則表達式將美國的影片分級修改成臺灣的分級
### 2.	日期處理：
* 字串轉換成日期格式，並依分析需求格式化
* 計算時間差（影片上架日期-影片發行年份），並轉換成日、月、年格式
<br>

## 四、	資料分析
>程式碼請參考：[4_EDA.py](https://github.com/Remi-KC/DataAnalysisProject_with_WebCrawling/blob/main/4_EDA.py "看我的程式碼")
### 1.可以看到哪些國家的影片？
* Netflix 的影片來自世界各地，較多元化。其中又以來自美國（3211部）、印度（1008部）、英國（628部）的影片最多。亞洲國家也都各有約上百部影片，臺灣則有85部。
* Disney+ 的影片來源則明顯集中在英美。在1450部影片中就有1121部來自美國，英國50部，加拿大26部。其餘國家則是零星1-5部。
![image](https://github.com/Remi-KC/DataAnalysisProject_with_WebCrawling/blob/main/Plot/country_n.png)
![image](https://github.com/Remi-KC/DataAnalysisProject_with_WebCrawling/blob/main/Plot/country_d.png)

### 2.有什麼類型的影片？
* 影視作品的比例在Netflix 和Disney+ 差不多，電影約佔七成，電視則約佔三成。
* Netflix的影片類型以國際化內容為最多（21%），劇情片次多（16%），而喜劇位列第三（12%）。Disney+ 的影片類型則以家庭劇最多（16%），動畫片次多（15%），喜劇第三（14%），動作冒險片第四（12%）。
* 兩平台在影片類型的分佈上各有特色。此外，這樣的分佈比例不論在電視或電影作品裡面都相仿，可以看作是平台本身選擇影片類型的調性。
![image](https://github.com/Remi-KC/DataAnalysisProject_with_WebCrawling/blob/main/Plot/genre.png)

### 3.影片適合哪些人 （年齡層）？
* Netflix的影片大部分都是限制級，次多為輔導級，普遍級最少。較適合成年人。
* Disney+ 的影片幾乎都是保護級和普遍級，完全沒有限制級內容，適合有小孩的家庭。
![image](https://github.com/Remi-KC/DataAnalysisProject_with_WebCrawling/blob/main/Plot/rating.png)

### 4.影片上架數量夠多嗎？
* Netflix 自2008年起每月上架影片不到10部，到2015年每月上架影片才開始攀升，2017年開始每月有約100部新影片，2018年底開始每月上架150部影片左右，甚至有些月份超過250部。上架量相較Disney+ 大很多。
* Disney+ 自2019年12月開始營運，可以看到它在前一個月一次性上架了730部影片，這很可能是迪士尼公司本身的作品。但之後每個月的上架數量相較Netflix就低很多，大約20-50部左右。
![image](https://github.com/Remi-KC/DataAnalysisProject_with_WebCrawling/blob/main/Plot/add_Ym.png)

### 5.容易看到最新作品嗎？
* Netflix有8.36%的作品在發行後3個月內就上架平台了，相當快速，這個比例也比預期來得高。而發行半年內就上架的作品佔將近兩成，一年內上架的作品則佔近四成，近七成作品都在發行五年內上架。
* Disney+ 的影片相較Netflix而言，會在作品發行後較長的時間才上架。發行後3個月內上架平台的作品只有3.26%，發行一年內上架的作品佔三成，近六成作品在發行五年內上架。 
![image](https://github.com/Remi-KC/DataAnalysisProject_with_WebCrawling/blob/main/Plot/diff_m.png)

### 6.劇荒期不要來！（平台會不會特別在哪個月份上架較多或較少影片？）
* 在Netflix 跟Disney+ 都發現類似的規律。平台在2、3月份的時候上架影片數量會相對較少，而在4、7月及年底的時候會上架較多影片。這些月份的上架數量和總平均值相差約達一個標準差。
* 原本期待如果上架的規律不同，訂閱兩個平台可以截長補短，然而結果與預想不同。不過，這個發現或許能提供給片商參考，如果在上架數量較少的月份推出作品，可能提高作品的能見度。
![image](https://github.com/Remi-KC/DataAnalysisProject_with_WebCrawling/blob/main/Plot/add_M_compare.png)

### 7.好評佳作有多少？（只分析影片數量前三多和大家比較常看的來源）
>註1: 只取評分人數>1000的資料，避免評分數過少，造成評分可信度太低的問題。<br>
>註2: 好評佳作的定義，採用評分>7.3。這個數據來自評分的第三四分位數。
* Netflix 平台上，韓國跟日本的作品中，有超過一半的作品得到很高的評價。觀看這兩個國家的作品最不容易踩雷。而作品數量最多的美國、印度跟英國，他們的作品獲得好評的比例反而沒有日韓來得高。
* Disney+ 平台上，與Netflix 同樣來自美國跟英國的作品相較，在Disney+ 平台裡，這兩個國家的作品獲得好評的比例不如Netflix 多。
![image](https://github.com/Remi-KC/DataAnalysisProject_with_WebCrawling/blob/main/Plot/good.png)

### 8.大熱作品有多少？（只分析影片數量前三多和大家比較常看的來源）
>註: 熱門的定義，需要同時滿足評分>7.3，且評分人數>3000。評分人數的標準來自評分人數中位數。
* Netflix 平台上，日本的影片有最高的比例是熱門大作（31.6%）。接著擁有較高比例熱門作品的是英國（21.3%）和韓國（20.5%）。這三個國家同時也是擁有最高比例好評佳作的國家。在Netflix上選擇這幾個國家的影片，最可能看到叫好又叫座的作品。
* Disney+ 平台上，與Netflix同樣來自美國跟英國的作品相較，在Disney+ 平台裡，這兩個國家熱門作品的比例都不如Netflix 多。這個結果和好評佳作的情況相同。因此整體而言，Disney+ 上面好作品的比例較低。
* 另一個值得注意的點是，臺灣的作品在上一個分析中好評的比例有兩成，但熱門作品的比例相較其他國家，下降的幅度較多，只剩下4.71%。這可能是因為臺灣作品在國際上被觀看的次數不夠多，因此評分人數很難達到標準，甚至可能多部作品並未達到1000人次的評分數。品質以外，如何在題材上吸引更多國際觀眾對臺灣的作品感興趣，或許是製作單位未來應該考量的重點。
![image](https://github.com/Remi-KC/DataAnalysisProject_with_WebCrawling/blob/main/Plot/popular.png)

<br>

## 五、	分析結論
<br>

## 六、	問題解決
