# DBMS_Final_Project
### Main Idea
東京是全球最受歡迎的旅遊目的地之一，融合了傳統文化與現代城市魅力，吸引了來自世界各地的旅客。然而，許多旅客在選擇住宿時，面對眾多選項往往感到困惑，難以找到最符合需求的住宿體驗。因此，我們的期末專題目標是建立一個以東京地區為核心的Airbnb匯總網頁，提供使用者全面而直觀的住宿資訊。
我們的網站將整合東京Airbnb房源的詳細資料，包含價格範圍、地理位置、以及星等評價等，幫助使用者快速篩選符合自身需求的住宿，讓旅客可以規劃住宿與行程的一站式服務。

### Source
本研究以 Kaggle 平台上公開的 Airbnb 東京房源資料集為基礎進行分析。該資料集於 2021 年 12 月 6 日擷取，內容為截至 2021 年 10 月 28 日東京地區所有 Airbnb 房源的詳細資訊，包括房源基本資料、使用者評論以及每日租賃情況。資料集總計包含 10,700 筆樣本，但部分特徵存在缺失資料，需進行適當的資料前處理。
資料集來源: [Tokyo Airbnb Open Data(2023)](https://www.kaggle.com/datasets/lucamassaron/tokyo-airbnb-open-data-2023/data?select=calendar.csv)

### ER Diagram
![螢幕擷取畫面 2024-12-27 231242](https://github.com/user-attachments/assets/9c645f37-edb7-480c-ac1b-868d39834187)

### Function
1.註冊帳號
2.登錄帳號
3.個人清單
4.基本搜尋功能(價格、地區、評價和民宿名字)

### Advanced
為了讓更多人能夠體驗和使用我們的功能，我們選擇了
Google Cloud Platform(GCP)來對外開放我們的服務。
我們透過在GCP上建立VM執行個體，並在上面建立Mysql
資料庫，然後再更改Mysql中的bind-address來讓遠端主機
能夠登入並使用。這樣我們就可以把我們的資料load到GCP上的Mysql資料庫中，並上傳我們的程式碼到VM上。
最後在main.py中把Flask設定成在外部可存取的 IP 和Port上執行，並以nohup python3 main.py &來執行main.py, 
這樣就能將 python3 main.py 命令放入後台, 藉此確保程式
在終端機關閉後仍會繼續執行。
能夠從外部存取的網址:[Tokyo Airbnb](http://35.201.204.93:8080)

