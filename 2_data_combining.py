import pandas as pd

# 設定路徑
path1 = "/Users/remikc/Programming/Python/DA_Project/Data/"

# 讀取檔案
netflix = pd.read_csv(path1+"netflix_titles.csv")
disney = pd.read_csv(path1+"disney_titles.csv")
imdb_rating = pd.read_csv(path1+"title.ratings.tsv", sep="\t")
data_imdb = pd.read_csv(path1+"data_imdb.csv")

#%% raw data 

# netflix資料數量、欄位、空值概覽
netflix.info()
'''
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 8807 entries, 0 to 8806
Data columns (total 12 columns):
 #   Column        Non-Null Count  Dtype 
---  ------        --------------  ----- 
 0   show_id       8807 non-null   object
 1   type          8807 non-null   object
 2   title         8807 non-null   object
 3   director      6173 non-null   object
 4   cast          7982 non-null   object
 5   country       7976 non-null   object
 6   date_added    8797 non-null   object
 7   release_year  8807 non-null   int64 
 8   rating        8803 non-null   object
 9   duration      8804 non-null   object
 10  listed_in     8807 non-null   object
 11  description   8807 non-null   object
dtypes: int64(1), object(11)
memory usage: 825.8+ KB
'''

# disney資料數量、欄位、空值概覽
disney.info()
'''
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 1450 entries, 0 to 1449
Data columns (total 12 columns):
 #   Column        Non-Null Count  Dtype 
---  ------        --------------  ----- 
 0   show_id       1450 non-null   object
 1   type          1450 non-null   object
 2   title         1450 non-null   object
 3   director      977 non-null    object
 4   cast          1260 non-null   object
 5   country       1231 non-null   object
 6   date_added    1447 non-null   object
 7   release_year  1450 non-null   int64 
 8   rating        1447 non-null   object
 9   duration      1450 non-null   object
 10  listed_in     1450 non-null   object
 11  description   1450 non-null   object
dtypes: int64(1), object(11)
memory usage: 136.1+ KB
None
'''

# imdb_rating資料數量、欄位、空值概覽
imdb_rating.info()
'''
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 1260065 entries, 0 to 1260064
Data columns (total 3 columns):
 #   Column         Non-Null Count    Dtype  
---  ------         --------------    -----  
 0   tconst         1260065 non-null  object 
 1   averageRating  1260065 non-null  float64
 2   numVotes       1260065 non-null  int64  
dtypes: float64(1), int64(1), object(1)
memory usage: 28.8+ MB
None
'''
# 重複編號檢查：1260065(所有)編號為唯一值
len(imdb_rating["tconst"].unique()) # 1260065

#%% netflix & disney + web_crawling

# data_imdb資料數量、欄位、空值概覽
data_imdb.info()
'''
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 10257 entries, 0 to 10256
Data columns (total 15 columns):
 #   Column        Non-Null Count  Dtype 
---  ------        --------------  ----- 
 0   platform      10257 non-null  object
 1   show_id       10257 non-null  object
 2   type          10257 non-null  object
 3   title         10257 non-null  object
 4   director      7150 non-null   object
 5   cast          9242 non-null   object
 6   country       9207 non-null   object
 7   date_added    10244 non-null  object
 8   release_year  10257 non-null  int64 
 9   rating        10250 non-null  object
 10  duration      10254 non-null  object
 11  listed_in     10257 non-null  object
 12  description   10257 non-null  object
 13  search        10257 non-null  object
 14  tconst        9997 non-null   object
dtypes: int64(1), object(14)
memory usage: 1.2+ MB
'''

#%% use tconst to combine data and get imdb ratings

# 刪除用來爬蟲的column
data_imdb.drop(columns=["search"], inplace=True)
# 合併評分資料
data_imdb = data_imdb.merge(imdb_rating, how="left", on="tconst")

# 合併後data_imdb資料數量、欄位、空值概覽（有些tconst在imdb_rating中無資料）
data_imdb.info()
'''
<class 'pandas.core.frame.DataFrame'>
Int64Index: 10257 entries, 0 to 10256
Data columns (total 16 columns):
 #   Column         Non-Null Count  Dtype  
---  ------         --------------  -----  
 0   platform       10257 non-null  object 
 1   show_id        10257 non-null  object 
 2   type           10257 non-null  object 
 3   title          10257 non-null  object 
 4   director       7150 non-null   object 
 5   cast           9242 non-null   object 
 6   country        9207 non-null   object 
 7   date_added     10244 non-null  object 
 8   release_year   10257 non-null  int64  
 9   rating         10250 non-null  object 
 10  duration       10254 non-null  object 
 11  listed_in      10257 non-null  object 
 12  description    10257 non-null  object 
 13  tconst         9997 non-null   object 
 14  averageRating  9598 non-null   float64
 15  numVotes       9598 non-null   float64
dtypes: float64(2), int64(1), object(13)
memory usage: 1.3+ MB
'''
#%% prepare two datasets
# data_imdb按平台分割
netflix = data_imdb[data_imdb["platform"]=="Netflix"]
disney = data_imdb[data_imdb["platform"]=="Disney+"]

# 合併評分資料後netflix資料數量、欄位、空值概覽
netflix.info()
'''
<class 'pandas.core.frame.DataFrame'>
Int64Index: 8807 entries, 0 to 8806
Data columns (total 16 columns):
 #   Column         Non-Null Count  Dtype  
---  ------         --------------  -----  
 0   platform       8807 non-null   object 
 1   show_id        8807 non-null   object 
 2   type           8807 non-null   object 
 3   title          8807 non-null   object 
 4   director       6173 non-null   object 
 5   cast           7982 non-null   object 
 6   country        7976 non-null   object 
 7   date_added     8797 non-null   object 
 8   release_year   8807 non-null   int64  
 9   rating         8803 non-null   object 
 10  duration       8804 non-null   object 
 11  listed_in      8807 non-null   object 
 12  description    8807 non-null   object 
 13  tconst         8614 non-null   object 
 14  averageRating  8330 non-null   float64
 15  numVotes       8330 non-null   float64
dtypes: float64(2), int64(1), object(13)
memory usage: 1.1+ MB
'''
print("評分資料佔總資料: %.2f%%" % (netflix["averageRating"].count()/len(netflix)*100))
# 評分資料佔總資料: 94.58%

# 合併評分資料後disney資料數量、欄位、空值概覽
disney.info()
'''
<class 'pandas.core.frame.DataFrame'>
Int64Index: 1450 entries, 8807 to 10256
Data columns (total 16 columns):
 #   Column         Non-Null Count  Dtype  
---  ------         --------------  -----  
 0   platform       1450 non-null   object 
 1   show_id        1450 non-null   object 
 2   type           1450 non-null   object 
 3   title          1450 non-null   object 
 4   director       977 non-null    object 
 5   cast           1260 non-null   object 
 6   country        1231 non-null   object 
 7   date_added     1447 non-null   object 
 8   release_year   1450 non-null   int64  
 9   rating         1447 non-null   object 
 10  duration       1450 non-null   object 
 11  listed_in      1450 non-null   object 
 12  description    1450 non-null   object 
 13  tconst         1383 non-null   object 
 14  averageRating  1268 non-null   float64
 15  numVotes       1268 non-null   float64
dtypes: float64(2), int64(1), object(13)
memory usage: 192.6+ KB
'''
print("評分資料佔總資料: %.2f%%" % (disney["averageRating"].count()/len(disney)*100))
# 評分資料佔總資料: 87.45%

#%%
netflix.to_csv(path1+"netflix.csv", index=False)
disney.to_csv(path1+"disney.csv", index=False)
data_imdb.to_csv(path1+"data_imdb.csv", index=False)



