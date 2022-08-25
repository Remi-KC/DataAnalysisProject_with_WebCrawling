import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from plotly.offline import plot

# set path
path1 = "/Users/remikc/Programming/Python/DA_Project/Data/"
path2 = "/Users/remikc/Programming/Python/DA_Project/Plot/"

# load data
netflix = pd.read_csv(path1+"netflix_new.csv")
disney = pd.read_csv(path1+"disney_new.csv")
data = pd.read_csv(path1+"data.csv")

# 中文設定
plt.rcParams["font.family"] = ["Heiti TC"]
plt.rcParams["font.size"] = 13

#%% 影片出品國家分佈
# 資料前處理
loc = data[["platform", "country_main"]]
loc.info()
'''
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 10257 entries, 0 to 10256
Data columns (total 2 columns):
 #   Column        Non-Null Count  Dtype 
---  ------        --------------  ----- 
 0   platform      10257 non-null  object
 1   country_main  9207 non-null   object
dtypes: object(2)
memory usage: 160.4+ KB
'''
print("country_main的空值佔總資料%.2f%%" % ((1-data["country_main"].count()/len(data))*100))
# country_main的空值佔總資料10.24%

# 刪除空值---使用約90%共9207筆資料
loc.dropna(inplace=True)
# 計算兩個平台上各國影片數量
loc = loc.groupby(["platform", "country_main"]).size().reset_index().rename(columns={0:"count"})

loc.describe()
'''
             count
count   102.000000
mean     90.264706
std     352.663161
min       1.000000
25%       2.000000
50%       7.000000
75%      40.750000
max    3211.000000
'''
#%% 影片出品國家分佈
# 作圖
# 繪製Netflix部分
fig1 = px.choropleth(loc[loc["platform"]=="Netflix"],
              locations="country_main",
              locationmode="country names",
              color="count",
              projection="equirectangular",
              scope="world",
              title="Netflix 影片出品國家分佈",
              color_continuous_scale="Viridis_r")

fig1.update_layout(coloraxis_colorbar_title="數量") 

fig1.add_scattergeo(
  locations = loc[loc["platform"]=="Netflix"]["country_main"],
  locationmode="country names",
  text = loc[loc["platform"]=="Netflix"]["count"],
  mode="text") 

fig1.update_traces(textfont=dict(size=10, color="brown"),
                   selector=dict(type='scattergeo'))

plot(fig1)

# 繪製Disney+部分
fig2 = px.choropleth(loc[loc["platform"]=="Disney+"],
              locations="country_main",
              locationmode="country names",
              color="count",
              projection="equirectangular",
              scope="world",
              title="Disney+ 影片出品國家分佈",
              color_continuous_scale="Viridis_r")

fig2.update_layout(coloraxis_colorbar_title="數量") 

fig2.add_scattergeo(
  locations = loc[loc["platform"]=="Disney+"]["country_main"],
  locationmode="country names",
  text = loc[loc["platform"]=="Disney+"]["count"],
  mode="text") 

fig2.update_traces(textfont=dict(size=10, color="brown"),
                   selector=dict(type='scattergeo'))

plot(fig2)

#%% 影片類型分佈（/電影電視/劇情喜劇愛情恐怖/)
# 資料前處理
genre = data[["platform", "type", "listed_in"]]
genre.info()
'''
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 10257 entries, 0 to 10256
Data columns (total 3 columns):
 #   Column     Non-Null Count  Dtype 
---  ------     --------------  ----- 
 0   platform   10257 non-null  object
 1   type       10257 non-null  object
 2   listed_in  10181 non-null  object
dtypes: object(3)
memory usage: 240.5+ KB
'''
# 刪除空值
genre.dropna(inplace=True)

# 將genre["listed_in"]的內容轉換成list型態
genre["listed_in"] = genre["listed_in"].apply(lambda x: str(x).split(", ")).reset_index(drop=True)

# 展開genre["listed_in"]，使每個row只有一個值
genre = genre.explode("listed_in")

# 按照平台/種類(電影電視)/類型(劇情喜劇愛情恐怖)計算分類數量
genre = genre.groupby(["platform", "type", "listed_in"]).size().reset_index().rename(columns={0:"count"})

#%% 影片類型分佈（/電影電視/劇情喜劇愛情恐怖)
# 作圖
# 繪製Netflix部分
fig1 = px.sunburst(genre[genre["platform"]=="Netflix"], 
                  path=["type", "listed_in"], values="count",
                  color="count", color_continuous_scale="matter", 
                  title="Netflix 影片類型分佈比例")
fig1.update_traces(textinfo="label+percent parent")
fig1.update_layout(coloraxis_colorbar_title="數量") 
plot(fig1)

# 繪製Disney+部分
fig2 = px.sunburst(genre[genre["platform"]=="Disney+"], 
                  path=["type", "listed_in"], values="count",
                  color="count", color_continuous_scale="matter", 
                  title="Disney+ 影片類型分佈比例")
fig2.update_traces(textinfo="label+percent parent")
fig2.update_layout(coloraxis_colorbar_title="數量") 
plot(fig2)

#%% 平台作品分級--hue=type
plt.figure(figsize = (18, 6), dpi=200)

plt.subplot(1,2,1)
sns.countplot(x="rating", hue="type", data=netflix,
              order = netflix['rating'].value_counts().index,
              hue_order=["Movie", "TV Show"],
              palette=["#B81D24", "#221F1F"])
plt.title("Netflix 各個級數影片數量", fontsize=21)
plt.xticks(np.arange(4),["限制級", "輔導級", "保護級", "普遍級"])
plt.xlabel("節目分級", fontsize=18, labelpad=8)
plt.ylabel("影\n片\n數\n量", rotation=0, fontsize=18, labelpad=15)
plt.legend(labels=["電影", "電視"])
plt.grid()

plt.subplot(1,2,2)
sns.countplot(x="rating", hue="type", data=disney,
              order = disney['rating'].value_counts().index,
              hue_order=["Movie", "TV Show"],
              palette=["#113CCF", "#BFF5FD"])

plt.title("Disney+ 各個級數影片數量", fontsize=21)
plt.xticks(np.arange(3),["保護級", "普遍級", "輔導級"])
plt.xlabel("節目分級", fontsize=18, labelpad=8)
plt.ylabel("影\n片\n數\n量", rotation=0, fontsize=18, labelpad=15)
plt.legend(labels=["電影", "電視"])
plt.grid()

# 存檔
sns.despine()
plt.savefig(path2+"rating.png", bbox_inches="tight")
plt.show()

#%% 平台每月新增影片數量比較：繪圖資料前處理

# netflix日期數量計算
add_Ym_net = pd.DataFrame(netflix['f_date_add_Ym'].value_counts()).reset_index()
add_Ym_net.sort_values(by=["index"], inplace=True)
add_Ym_net["platform"]="Netflix" 

# disney+日期數量計算
add_Ym_dis = pd.DataFrame(disney['f_date_add_Ym'].value_counts()).reset_index()
add_Ym_dis.sort_values(by=["index"], inplace=True)
add_Ym_dis["platform"]="Disney+" 

# 合併
add_Ym = pd.concat([add_Ym_net, add_Ym_dis]).rename(columns={"f_date_add_Ym":"count"})
add_Ym["date"] = pd.to_datetime(add_Ym["index"], format='%Y-%m')
# 轉成wide-form方便繪圖
add_Ym_wide = add_Ym.pivot("date", "platform", "count")

#%% 平台每月新增影片數量比較：繪圖
# Netflix 1997-08成立，2008-01至2015-09每月新增不到10部，2017-08起每月穩定新增100部左右，2018-07起每月新增150部，甚至有些月份超過200部
# Disney+ 2019-12開始營運，營運前2019-11加入大量影片(730)，其餘月份則10-50部/每月

# 作圖
import matplotlib.gridspec as gridspec
import matplotlib.dates as md
# 設定上下方兩個子圖比例
gs = gridspec.GridSpec(2, 1, height_ratios=[1, 3])
fig = plt.figure(figsize = (18, 8), dpi=200)
fig.subplots_adjust(hspace=0.05)
ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])

# 畫折線圖
sns.lineplot(ax=ax1, data=add_Ym_wide, hue_order=["Netflix", "Disney+"], 
             marker="o", palette=["#B81D24", "#113CCF"])
sns.lineplot(ax=ax2, data=add_Ym_wide, hue_order=["Netflix", "Disney+"], 
             marker="o", palette=["#B81D24", "#113CCF"])

# 子圖(下)時間軸參數設定
ax2.xaxis.set_major_locator(md.YearLocator())
ax2.xaxis.set_major_formatter(md.DateFormatter('%Y-%m'))
ax2.xaxis.set_minor_locator(md.MonthLocator(bymonth=[3,5,7,9,11]))
ax2.xaxis.set_minor_formatter(md.DateFormatter('%m'))
plt.setp(ax2.xaxis.get_majorticklabels(), rotation = 75)
# 子圖(上)的時間軸雖然不顯示，但也要設定，不然grid會對不齊
ax1.xaxis.set_major_locator(md.YearLocator())
ax1.xaxis.set_minor_locator(md.MonthLocator(bymonth=[3,5,7,9,11]))

# x-tick參數設定
ax2.tick_params(axis="x", which="major", length=12, labelsize=12)
ax2.tick_params(axis="x", which="minor", length=5, labelsize=9)

# broken axis設定
ax1.set_ylim(720, 740)  # 界外值所在區域
ax2.set_ylim(-10, 300)  # 其他資料點
ax1.spines[["bottom", "top", "right"]].set_visible(False) # 移除子圖(上)的下、上、右邊框
ax2.spines[["top", "right"]].set_visible(False) # 移除子圖(下)的上、右邊框
ax1.xaxis.tick_top() # 將子圖(上)的x-tick移到上方
ax1.tick_params(which="both", top=False, labeltop=False)  # 不顯示子圖(上)的x-tick和標籤

# 繪製刪除線
d = .5  # proportion of vertical to horizontal extent of the slanted line
kwargs = dict(marker=[(-1, -d), (1, d)], markersize=12,
              linestyle="none", color='k', mec='k', mew=1, clip_on=False)
ax1.plot([0],[0], transform=ax1.transAxes, **kwargs)
ax2.plot([0],[1], transform=ax2.transAxes, **kwargs)

# 圖表標籤設定
fig.suptitle("平台每月新增影片數量", fontsize=25, y=0.95) 
ax2.set_xlabel("日期(年-月)", fontsize=21, labelpad=8)
ax2.set_ylabel("數\n量", rotation=0, fontsize=21, labelpad=15)
ax1.set_xlabel("")
ax1.set_ylabel("")
ax1.legend() 
ax2.legend().set_visible(False)          
ax1.grid()
ax2.grid()

# 存檔
plt.savefig(path2+"add_Ym.png", bbox_inches="tight")
plt.show()

#%% 作品發佈後多久會上架平台？（新作品上架比例）
# 異常值檢查
# 異常可能原因: 影集有很多季的情況下，date_added為第一季加入平台時間，但release_year為最新一季的發佈時間

print(min(netflix["diff_days"])) #-1006.0
print(min(disney["diff_days"])) #-14.0

print(max(netflix["diff_months"])) #1127
print(max(disney["diff_months"])) #1102

print("Netflix中 release_year資料異常筆數:", len(netflix[netflix["diff_days"]<0]))
# Netflix中 release_year資料異常筆數: 14
print("Disney+中 release_year資料異常筆數:", len(disney[disney["diff_days"]<0]))
# Disney+中 release_year資料異常筆數: 1

# 因為異常筆數很少，決定屏除異常資料再做EDA
diff_n = pd.DataFrame(netflix[netflix["diff_days"]>0][["f_date_add_Ym", "diff_months"]])
diff_d = pd.DataFrame(disney[disney["diff_days"]>0][["f_date_add_Ym", "diff_months"]])
# 營運初期可能大量加入經典老片，為了避免這些數據影響結果，只取近幾年的資料做分析，也較適合推論至現今的情況
diff_recentadd_n = diff_n[diff_n["f_date_add_Ym"]>"2019-11"]
diff_recentadd_d = diff_d[diff_d["f_date_add_Ym"]>"2019-11"]

#%% 作品發佈後多久會上架平台？（新作品上架比例）
# 僅採用2019-12之後的數據(Netflix (3578-14=)3564筆, Disney+ (706-1=)705筆)
# 作圖
plt.figure(figsize = (18, 6), dpi=200)

ax1 = plt.subplot(121)
sns.histplot(diff_recentadd_n, x="diff_months", stat="percent", 
             binwidth=3, cumulative=True, edgecolor='k', color="#F5F5F1")

# 設定特定bar的顏色
hightlight = [0, 1, 2, 3, 7, 11, 19]
for i in hightlight:
    if i > 2:
        ax1.patches[i].set_facecolor("#221F1F")
    else:
        ax1.patches[i].set_facecolor("#B81D24")     

# 設定每個bar標籤：只顯示要hightlight的bar上的數值
label = [round(ax1.containers[0].datavalues[i], 2) if i in hightlight else "" 
         for i in range(len(ax1.containers[0]))]
# 顯示bar數值
ax1.bar_label(ax1.containers[0], labels=label)   

# 設定主標題
plt.suptitle("影片發布到上架平台的時間差 vs 數量(累積百分比)", fontsize=21, y=1.02)
# 設定副標題
plt.title('Netflix |只顯示時間差5年內的數據',fontsize=18)           
plt.xlabel("時間差(月)", fontsize=18)
plt.ylabel("影\n片\n數\n量\n(%)", rotation=0, fontsize=18, labelpad=15)
plt.xticks(np.arange(0, 61, 3))
plt.xlim(0,60)
plt.grid()

ax2 = plt.subplot(122, sharey=ax1)
sns.histplot(diff_recentadd_d, x="diff_months", stat="percent", 
             binwidth=3, cumulative=True, edgecolor='k', color="#F5F5F1")

# 設定特定bar的顏色
for i in hightlight:
    if i > 2:
        ax2.patches[i].set_facecolor("#113CCF") 
    else:
        ax2.patches[i].set_facecolor("#BFF5FD")
        
# 設定每個bar標籤：只顯示要hightlight的bar上的數值
label = [round(ax2.containers[0].datavalues[i], 2) if i in hightlight else "" 
         for i in range(len(ax1.containers[0]))]
# 顯示bar數值
ax2.bar_label(ax2.containers[0], labels=label) 

plt.title('Disney+ |只顯示時間差5年內的數據',fontsize=18)  
plt.xlabel("時間差(月)", fontsize=18)
plt.ylabel("影\n片\n數\n量\n(%)", rotation=0, fontsize=18, labelpad=15)
plt.xticks(np.arange(0, 61, 3))
plt.xlim(0,60)
plt.grid()
sns.despine()

# 存檔
plt.savefig(path2+"diff_m.png", bbox_inches="tight")
plt.show()



#%% 上架作品分析：劇荒期vs.劇豐期在哪個月份？
import calendar
# 因為Disney+ 於2019-11上架大量影片，這裡只採用2019-12之後的數據(Netflix 3578筆, Disney+ 706筆)
add_m = data[data["f_date_add_Ym"]>"2019-11"][["platform", "f_date_add_Ym", "f_date_add_m"]]

# 按月份計算平台每月平均上架影片數量
add_m_mean = add_m.groupby(['platform', 'f_date_add_Ym', "f_date_add_m"]).size().groupby(['platform', 'f_date_add_m']).mean().reset_index()

# 月份轉換成縮寫
add_m_mean["f_date_add_m"] = add_m_mean["f_date_add_m"].apply(lambda x: calendar.month_abbr[int(x)])
add_m_mean = add_m_mean.rename(columns={0:"mean"})

#%% 上架作品分析：劇荒期vs.劇豐期在哪些月份？
# 作圖
plt.figure(figsize = (10, 6), dpi=200)
f = sns.lineplot(x="f_date_add_m", y="mean", hue="platform", data=add_m_mean,palette=["#B81D24", "#113CCF"],
             hue_order=["Netflix", "Disney+"], marker="o", markeredgecolor=None, alpha=.8)
f.axhline(add_m_mean[add_m_mean["platform"]=="Netflix"]["mean"].mean(),ls="--", lw=1.2, c="#221F1F", alpha=.5)
f.axhline(add_m_mean[add_m_mean["platform"]=="Disney+"]["mean"].mean(),ls="--", lw=1.2, c="DeepSkyBlue", alpha=.5)

y_n = list(add_m_mean[(add_m_mean["platform"]=="Netflix")&((add_m_mean["f_date_add_m"]=="Apr")|(add_m_mean["f_date_add_m"]=="Jul")|(add_m_mean["f_date_add_m"]=="Dec"))]["mean"])
x_n = ["Apr", "Jul", "Dec"]
f.scatter(x=x_n, y=y_n, marker="^", s=200, c="#B81D24")

y_n2 = list(add_m_mean[(add_m_mean["platform"]=="Netflix")&((add_m_mean["f_date_add_m"]=="Feb")|(add_m_mean["f_date_add_m"]=="Mar"))]["mean"])
x_n2 = ["Feb", "Mar"]
f.scatter(x=x_n2, y=y_n2, marker="v", s=200, c="#B81D24")

y_d = list(add_m_mean[(add_m_mean["platform"]=="Disney+")&((add_m_mean["f_date_add_m"]=="Apr")|(add_m_mean["f_date_add_m"]=="Jul")|(add_m_mean["f_date_add_m"]=="Nov"))]["mean"])
x_d = ["Apr", "Jul", "Nov"]
f.scatter(x=x_d, y=y_d, marker="^", s=200, c="#113CCF")

y_d2 = list(add_m_mean[(add_m_mean["platform"]=="Disney+")&((add_m_mean["f_date_add_m"]=="Feb")|(add_m_mean["f_date_add_m"]=="Mar"))]["mean"])
x_d2 = ["Feb", "Mar"]
f.scatter(x=x_d2, y=y_d2, marker="v", s=200, c="#113CCF")

for x, y in zip((x_n+x_d),(y_n+y_d)):
    plt.text(x, y, x,fontsize=16, c="Maroon")
for x, y in zip((x_n2+x_d2),(y_n2+y_d2)):
    plt.text(x, y, x,fontsize=16, c="#221F1F")

plt.title("平台近年各月份平均上架影片數量", fontsize=21, y=1.03)
plt.xlabel("月份", fontsize=18)
plt.ylabel("影\n片\n數\n量", rotation=0, fontsize=18, labelpad=15)

plt.legend(labels=["Netflix    |2019/12 - 2021/09", "Disney+ |2019/12 - 2021/11"])
plt.grid()
sns.despine()
# 存檔
plt.savefig(path2+"add_M_compare.png", bbox_inches="tight")
plt.show()

#%% Popularity:「熱門」影片(評分高，且有一定的評分人數)的作品數量(比例)
score = data[["platform", "country_main", "averageRating", "numVotes"]]
score.info()
'''
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 10257 entries, 0 to 10256
Data columns (total 4 columns):
 #   Column         Non-Null Count  Dtype  
---  ------         --------------  -----  
 0   platform       10257 non-null  object 
 1   country_main   9207 non-null   object 
 2   averageRating  9598 non-null   float64
 3   numVotes       9598 non-null   float64
dtypes: float64(2), object(2)
memory usage: 320.7+ KB
'''
print("country_main 空值比例: %.2f%%" % (score["country_main"].isna().sum()/len(score)*100))
print("averageRating 空值比例: %.2f%%" % (score["averageRating"].isna().sum()/len(score)*100))
print("numVotes 空值比例: %.2f%%" % (score["numVotes"].isna().sum()/len(score)*100))
# country_main 空值比例: 10.24%
# averageRating 空值比例: 6.42%
# numVotes 空值比例: 6.42%

# 刪除空值
score.dropna(inplace=True)
print("刪除空值後，使用資料佔原始資料%.2f%%，共%d筆" % (len(score)/10257*100, len(score)))
# 刪除空值後，使用資料佔原始資料86.22%，共8844筆

# 描述性統計資料--->決定「熱門」的指標: 評分>7.3 & 評分人數>3000
score.describe()
'''
      averageRating      numVotes
count    8844.000000  8.844000e+03
mean        6.505337  3.706285e+04
std         1.175142  1.199240e+05
min         1.400000  5.000000e+00
25%         5.800000  5.510000e+02
50%         6.600000  2.794000e+03
75%         7.300000  1.663725e+04
max         9.700000  2.300665e+06

'''
# 只看作品數量前三名，以及大部分台灣人常看的國家(N:美印英韓日台中，D:美英加)
filter1 = (score["platform"]=="Netflix")&((score["country_main"]=="United States")|(score["country_main"]=="India")|(score["country_main"]=="United Kingdom")|(score["country_main"]=="South Korea")|(score["country_main"]=="Japan")|(score["country_main"]=="Taiwan")|(score["country_main"]=="China"))
filter2 = (score["platform"]=="Disney+")&((score["country_main"]=="United States")|(score["country_main"]=="United Kingdom")|(score["country_main"]=="Canada"))
select_loc = score[filter1|filter2]

# 算各國作品總數
select_loc_count = select_loc.groupby(["platform", "country_main"]).size().reset_index().rename(columns={0:"count"})

# 篩選出「熱門」(評分>7.3 & 評分人數>3000)
select_loc_pop = select_loc[(select_loc["averageRating"]>7.3)&(select_loc["numVotes"]>3000)]

# 算各國「熱門」總數
select_loc_pop_count = select_loc_pop.groupby(["platform", "country_main"]).size().reset_index().rename(columns={0:"count"})

# 合併select_loc_count和select_loc_pop_count
select_p = select_loc_pop_count.merge(select_loc_count, how="left", on=["platform", "country_main"], suffixes=('_', '_total'))

# 計算百分比
select_p["popular"]=select_p["count_"]/select_p["count_total"]*100
select_p["total"]=100

#%% Popularity:「熱門」影片(評分高，且有一定的評分人數)的作品數量(比例)
# 作圖
select_p = select_p.sort_values(["platform","popular"], ascending=False)
select_p_n = select_p[select_p["platform"]=="Netflix"].reset_index(drop=True)
select_p_d = select_p[select_p["platform"]=="Disney+"].reset_index(drop=True)

plt.figure(figsize = (28, 8), dpi=200)

ax1 = plt.subplot(121)
sns.barplot(x="total", y="country_main", data=select_p_n,
            label="非熱門", color="#221F1F")

sns.barplot(x="popular", y="country_main", data=select_p_n,
            label="熱門", color="#B81D24")

for i in range(len(select_p_n)):
    ax1.annotate(f"{select_p_n['popular'][i]:.3}%", 
                    xy=(select_p_n["popular"][i]/2, i),
                    fontsize=12, color="#F5F5F1",
                    va="center", ha="center")

plt.title("Netflix 各國熱門影片比例", fontsize=21, loc="left")
plt.title("評分>7.3| 評分人數>3000          ", fontsize=12, loc="right")
ax1.legend(ncol=2, loc="lower right", shadow=True)
ax1.set(ylabel="", xlabel="")
plt.xticks(np.arange(0, 101, 10))

ax2 = plt.subplot(122)
sns.barplot(x="total", y="country_main", data=select_p_d,
            label="非熱門", color="#BFF5FD")

sns.barplot(x="popular", y="country_main", data=select_p_d,
            label="熱門", color="#113CCF")

for i in range(len(select_p_d)):
    ax2.annotate(f"{select_p_d['popular'][i]:.3}%", 
                    xy=(select_p_d["popular"][i]/2, i),
                    fontsize=12, color="#F5F5F1",
                    va="center", ha="center")

plt.title("Disney+ 各國熱門影片比例", fontsize=21, loc="left")
plt.title("評分>7.3| 評分人數>3000          ", fontsize=12, loc="right")
ax2.legend(ncol=2, loc="lower right", shadow=True)
ax2.set(ylabel="", xlabel="")
plt.xticks(np.arange(0, 101, 10))

sns.despine()
plt.subplots_adjust(wspace=0.15)

# 存檔
plt.savefig(path2+"popular.png", bbox_inches="tight")
plt.show()

#%% Good:「好片」(高評分，具評分可信度:numVotes>1000)的影片比例

# 只看作品數量前三名(N:美印英韓日台中，D:美英加)，以及大部分台灣人常看的國家 & 評分人數>1000
filter3 = (score["platform"]=="Netflix")&(score["numVotes"]>1000)&((score["country_main"]=="United States")|(score["country_main"]=="India")|(score["country_main"]=="United Kingdom")|(score["country_main"]=="South Korea")|(score["country_main"]=="Japan")|(score["country_main"]=="Taiwan")|(score["country_main"]=="China"))
filter4 = (score["platform"]=="Disney+")&(score["numVotes"]>1000)&((score["country_main"]=="United States")|(score["country_main"]=="United Kingdom")|(score["country_main"]=="Canada"))
select_loc_1000v = score[filter3|filter4]

# 算各國評分人數>1000作品總數
select_loc_1000v_count = select_loc_1000v.groupby(["platform", "country_main"]).size().reset_index().rename(columns={0:"count"})

# 篩選出「好片」(評分>7.3)
select_loc_good = select_loc_1000v[select_loc_1000v["averageRating"]>7.3]

# 算各國「好片」總數
select_loc_good_count = select_loc_good.groupby(["platform", "country_main"]).size().reset_index().rename(columns={0:"count"})

# 合併select_loc_1000v_count和select_loc_good_count
select_g = select_loc_good_count.merge(select_loc_1000v_count, how="left", on=["platform", "country_main"], suffixes=('_', '_total'))

# 計算百分比
select_g["good"]=select_g["count_"]/select_g["count_total"]*100
select_g["total"]=100

#%% Good:「好片」(高評分，具評分可信度:numVotes>1000)的影片比例
# 作圖
select_g = select_g.sort_values(["platform","good"], ascending=False)
select_g_n = select_g[select_g["platform"]=="Netflix"].reset_index(drop=True)
select_g_d = select_g[select_g["platform"]=="Disney+"].reset_index(drop=True)

plt.figure(figsize = (28, 8), dpi=200)

ax1 = plt.subplot(121)
sns.barplot(x="total", y="country_main", data=select_g_n,
            label="非好評", color="#221F1F")

sns.barplot(x="good", y="country_main", data=select_g_n,
            label="好評", color="#B81D24")

for i in range(len(select_g_n)):
    ax1.annotate(f"{select_g_n['good'][i]:.3}%", 
                    xy=(select_g_n["good"][i]/2, i),
                    fontsize=12, color="#F5F5F1",
                    va="center", ha="center")

plt.title("Netflix 各國好評影片比例（評分人數>1000）", fontsize=21, loc="left")
plt.title("評分>7.3           ", fontsize=12, loc="right")
ax1.legend(ncol=2, loc="lower right", shadow=True)
ax1.set(ylabel="", xlabel="")
plt.xticks(np.arange(0, 101, 10))

ax2 = plt.subplot(122)
sns.barplot(x="total", y="country_main", data=select_g_d,
            label="非好評", color="#BFF5FD")

sns.barplot(x="good", y="country_main", data=select_g_d,
            label="好評", color="#113CCF")

for i in range(len(select_g_d)):
    ax2.annotate(f"{select_g_d['good'][i]:.3}%", 
                    xy=(select_g_d["good"][i]/2, i),
                    fontsize=12, color="#F5F5F1",
                    va="center", ha="center")

plt.title("Disney+ 各國好評影片比例（評分人數>1000）", fontsize=21, loc="left")
plt.title("評分>7.3           ", fontsize=12, loc="right")
ax2.legend(ncol=2, loc="lower right", shadow=True)
ax2.set(ylabel="", xlabel="")
plt.xticks(np.arange(0, 101, 10))

sns.despine()
plt.subplots_adjust(wspace=0.15)

# 存檔
plt.savefig(path2+"good.png", bbox_inches="tight")
plt.show()

#%% 平台重疊作品---很少!!!
print("兩平台相同的影片數量: %d部" % (len(set(netflix["tconst"])&set(disney["tconst"]))-1))
# 兩平台相同的影片數量: 41部

