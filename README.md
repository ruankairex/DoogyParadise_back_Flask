## DoogyParadise寵物平台網站
詳細介紹請查看:https://github.com/ruankairex/DoogyParadise_backend
## 關於此Flask專案
- 檔案結構
    1. Controller_tokenizer.py : 分詞功能，主要運行檔案。
    2. Controller_graphSerch.py : 圖搜功能，開發完成，但專案中棄用。
    

- 為DoogyParadise網站的後端伺服器，主要處理動態牆系統中推文的詞頻率統計，並存入MongoDB。
- 使用Flask是因為Python在資料處理領域的套件多且教學豐富，並且可以有效分攤主要伺服器(Spring Boot)的負載(分詞功能使用的是雙向LSTM模型，跑大量資料還是很消耗資源)
- 若不運行此專案，DoogyParadise網站仍然可以運行(Vue+Spring Boot)，只是會失去員工後台->推文管理->圖表的功能。

### 版本
Python : 3.9.13
Flask : 3.0.2
### 套件
CkipTagger:https://github.com/ckiplab/ckiptagger
引入套件後，單純使用分詞功能(from ckiptagger import WS)，需自行下載。

### 優化方向
- 目前資料流是Spring Boot送出POST請求夾帶所有待分析資料到Flask，後期該request可能會非常巨大。
- 可以試著由主伺服器發出單純的分析請求，後續工作皆由子伺服器完成，如:至MySQL撈資料、分析、存入MongoDB...。
