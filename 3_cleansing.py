import numpy as np
import pandas as pd

# set path
path1 = "/Users/remikc/Programming/Python/DA_Project/Data/"

# load data
data = pd.read_csv(path1+"data_imdb.csv")
netflix = pd.read_csv(path1+"netflix.csv")
disney = pd.read_csv(path1+"disney.csv")

#%% data cleansing & preprocessing

# 刪除DataFrame中非字元開頭
data = data.replace(r'^\W+', "", regex=True)

# 新增主要地區欄位，帶入country中第一個國家
data.insert(7,"country_main", data["country"].apply(lambda x: str(x).split(",")[0]))

# %% 影片分類名稱觀察

# listed_in分類計數：發現兩個平台的分類都很多 
genre = data["listed_in"].apply(lambda x: str(x).split(", ")).reset_index(drop=True)

print("Netflix原始分類數量:", len(set(genre[:len(netflix)].explode())))
# Netflix原始分類數量: 42
print("Disney+原始分類數量:", len(set(genre[(len(data)-len(disney)):len(data)].explode())))
# Disney+原始分類數量: 44

# listed_in欄位內容觀察與計數：發現netflix有太多不必要的細項了，決定合併雷同的分類 
print(genre[:len(netflix)].explode().value_counts())
'''
International Movies            2752
Dramas                          2427
Comedies                        1674
International TV Shows          1351
Documentaries                    869
Action & Adventure               859
TV Dramas                        763
Independent Movies               756
Children & Family Movies         641
Romantic Movies                  616
TV Comedies                      581
Thrillers                        577
Crime TV Shows                   470
Kids' TV                         451
Docuseries                       395
Music & Musicals                 375
Romantic TV Shows                370
Horror Movies                    357
Stand-Up Comedy                  343
Reality TV                       255
British TV Shows                 253
Sci-Fi & Fantasy                 243
Sports Movies                    219
Anime Series                     176
Spanish-Language TV Shows        174
TV Action & Adventure            168
Korean TV Shows                  151
Classic Movies                   116
LGBTQ Movies                     102
TV Mysteries                      98
Science & Nature TV               92
TV Sci-Fi & Fantasy               84
TV Horror                         75
Cult Movies                       71
Anime Features                    71
Teen TV Shows                     69
Faith & Spirituality              65
TV Thrillers                      57
Movies                            57
Stand-Up Comedy & Talk Shows      56
Classic & Cult TV                 28
TV Shows                          16
Name: listed_in, dtype: int64
'''
# listed_in欄位內容觀察與計數：disney+雖然分類重疊性不高，分類總數仍然很可觀 
print(genre[(len(data)-len(disney)):len(data)].explode().value_counts())
'''
Family                     632
Animation                  542
Comedy                     526
Action-Adventure           452
Animals & Nature           208
Coming of Age              205
Fantasy                    192
Documentary                174
Kids                       141
Drama                      134
Docuseries                 122
Science Fiction             91
Historical                  53
Music                       48
Musical                     44
Sports                      43
Biographical                41
Buddy                       40
Anthology                   28
Reality                     26
Romance                     20
Superhero                   19
Crime                       16
Mystery                     12
Variety                     12
Game Show / Competition     10
Parody                       9
Survival                     9
Lifestyle                    8
Western                      7
Concert Film                 7
Medical                      6
Dance                        6
Thriller                     5
Anime                        4
Series                       3
Spy/Espionage                3
Movies                       3
Romantic Comedy              2
Disaster                     2
Soap Opera / Melodrama       2
Travel                       1
Talk Show                    1
Police/Cop                   1
Name: listed_in, dtype: int64
'''

#%% 影片分類名稱處理

# 清理分類中不需要的字詞(同類型影片中，不再區分 TV Shows 和 Movies-->降低分類數量)
data = data.replace({"listed_in":{r'.?Movies|.?TV Shows|.?TV|TV|\'':""}}, regex=True)
# 取代特定字詞(同大類影片不再分細項-->降低分類數量) 
# regex的順序很重要!!!!(例：Musical|Music不能相反)
new_genre = {
    "listed_in":{
        r'Anime Features|Anime Series|Animation':"Anime",
        r'Classic & Cult|Classic|Cult':"Classic & Cult",
        r'Music & Musicals|Musical|Music':"Music & Musicals",
        r'Stand-Up Comedy & Talk Shows|Stand-Up Comedy':"Stand-Up Comedy & Talk Shows"}
    }
data = data.replace(new_genre, regex=True)

# 清除除非字元開頭
data = data.replace(r'^\W+', "", regex=True)
# 無資料處填入空值 
data["listed_in"] = data["listed_in"].replace("", np.nan)     
                                 
# 計算清理後分類數量
genre_new = data["listed_in"].apply(lambda x: str(x).split(", ")).reset_index(drop=True)
print("Netflix清理後分類數量:", len(set(genre_new[:len(netflix)].explode()))-1)#扣掉NAN
# Netflix清理後分類數量: 28
print("Disney+清理後分類數量:", len(set(genre_new[(len(data)-len(disney)):len(data)].explode()))-1)#扣掉NAN
# Disney+清理後分類數量: 41

#%% 清理分級標籤

# 輸出分級標籤
print(set(netflix.rating))
# {nan, 'TV-14', '84 min', 'TV-Y', 'UR', 'TV-Y7', 'NR', 'PG', '66 min', 'TV-PG', 
# 'PG-13', 'G', 'TV-Y7-FV', '74 min', 'TV-G', 'NC-17', 'TV-MA', 'R'}
print(set(disney.rating))
# {nan, 'TV-14', 'TV-Y', 'TV-Y7', 'PG', 'TV-PG', 'PG-13', 'TV-Y7-FV', 'TV-G', 'G'}

# netflix有一些奇怪的分級標籤(66 min, 74 min, 84 min)
# 觀察得知總數=3， 因為影響微乎其微，決定刪除這些標籤
print(netflix['rating'].value_counts())
'''
TV-MA       3207
TV-14       2160
TV-PG        863
R            799
PG-13        490
TV-Y7        334
TV-Y         307
PG           287
TV-G         220
NR            80
G             41
TV-Y7-FV       6
NC-17          3
UR             3
66 min         1
74 min         1
84 min         1
Name: rating, dtype: int64
'''

# 將美國的分級修改成台灣的分級，方便解讀，並刪除標籤(66 min, 74 min, 84 min)
new_rating = {
    "rating":{
        r'NR|UR|66 min|74 min|84 min':np.nan,
        r'TV-MA|R|NC-17':"Adults",
        r'PG-13|TV-14':"Teens",
        r'TV-Y7-FV|TV-Y7|TV-PG|PG':"Kids",
        r'TV-Y|TV-G|G':"AllAges"}
    }
data = data.replace(new_rating, regex=True)

#%% 日期欄位格式化、計算時間差並新增欄位

data["f_date_add"] = pd.to_datetime(data["date_added"]).dt.date
data["f_date_add_Ym"] = pd.to_datetime(data["date_added"]).dt.strftime("%Y-%m")
data["f_date_add_m"] = pd.to_datetime(data["date_added"]).dt.strftime("%m")
data["f_year_release"] = pd.to_datetime(data["release_year"],format='%Y').dt.date
data["diff_days"] = (data["f_date_add"]-data["f_year_release"]).astype('timedelta64[D]')
data["diff_months"] = (data["f_date_add"]-data["f_year_release"]).astype('timedelta64[M]')
data["diff_years"] = (data["f_date_add"]-data["f_year_release"]).astype('timedelta64[Y]')

#%% save data to .csv
data.to_csv(path1+"data.csv", index=False)

netflix_new = data[data["platform"]=="Netflix"]
netflix_new.to_csv(path1+"netflix_new.csv", index=False)

disney_new = data[data["platform"]=="Disney+"]
disney_new.to_csv(path1+"disney_new.csv", index=False)
