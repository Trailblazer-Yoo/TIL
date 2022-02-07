# TIL(Today I Learned)

___

> Fab/7th/2022_Multi campus_유선종 Day27

## 주가예측 프로젝트 2일차
어제는 셀레니움을 사용해서 크롤링을 해봤다. 이번에는 BeautifulSoup을 이용해서 크롤링을 해보고자 한다.

### bs4를 이용한 크롤링
우선 이전 데이터와 동일한 코드를 첨부하겠다. 이 코드는 Day26과 동일하다.

```python
import pymysql
import pandas as pd
import requests

table = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header = 0)     ## KRX에서 종목 크롤링

################################ 데이터베이스 저장 공간 생성 ######################################

conn = pymysql.connect(host='localhost', user='root', password = 'yousj928', charset='utf8')
cur = conn.cursor()

cur.execute("drop database if exists StockPrice")
cur.execute("create database IF NOT EXISTS StockPrice")  ## StockPrice 데이터베이스 생성
cur.execute("USE StockPrice")   ## StockPrice 선택
cur.execute("DROP TABLE IF EXISTS company_info")    ## 이전 자료 삭제
cur.execute("create table if not exists company_info(code char(6), Korean_name varchar(150))") ## company_info 생성

#################### 데이터베이스에 종목코드와 종목명 입력하기 ###############################

for i in range(len(table[0]['회사명'])):    ## 원하는 회사 갯수 설정
    code = str(table[0]['종목코드'][i])     ## 종목코드
    name = str(table[0]['회사명'][i])       ## 회사명
    if len(code) != 6:
        code = code.zfill(6)        ## 5자리 이하의 숫자 앞에 0 넣어주기
    cur.execute("insert into company_info values ('%s', '%s')" % (code,name))       ## 데이터베이스에 입력
conn.commit()

########################### 네이버에서 해당 코드의 종가기준 가격 데이터 뽑아오기 ############################

cur.execute("DROP TABLE IF EXISTS daily_price") ## 이전 데이터 삭제
cur.execute("create table if not exists daily_price(code char(6), date DATE,price int, volume int)") ## 넣을 공간 생성
cur.execute("select * from company_info")   ## 종목 코드를 읽기 위해 테이블 열기

list = []
while True:
    row = cur.fetchone()    ## company_info에서 한줄씩 읽기
    if row == None:
        break
    a = row[0]
    list.append(a) ## 이렇게 하나의 메모리로 담지 않으면 cur을 두번 사용하게 됨

```
___
#### 1. request를 이용하여 크롤링하기
이제부터 bs4를 이용해서 크롤링을 해보겠다.

```python
import BeautifulSoup as bs4

for code in list:
    page = 1 
    while True:
        url = f"https://finance.naver.com/item/sise_day.naver?code={list[0]}&page={page}" 
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'} ## header를 이용해서 거부된 agent를 허용된 agent로 바꿔주기
        res = requests.get(url, headers = headers)
        res.raise_for_status()
```
1. url에 코드와 페이지에 따라 창이 열리도록 주소값을 할당한다.
2. headers는 네이버에서 접근을 거부하는 것을 풀어주는 명령어이다. 가끔 '웹페이지를 접근할 수 없습니다.' 하면서 오류 페이지가 뜨는 경우가 있는데, 이는 크롤링하는 나를 유저가 아니라고 판단하고 차단해서 발생한다. 우리는 로봇이 아니라 사람이라는 것을 알려주기 위해 위와 같은 headers 코드를 설정해준다.
> 위의 코드는 `http://www.useragentstring.com`에 들어가면 맨 위에 있다.
3. 나머지는 우리에게 익숙한 `requests.get`을 이용해서 html을 긁어오고 오류가 없는지 `res.raise_for_status()`로 확인해준다.

___
#### 2. bs4를 이용하여 파싱하기

```python
        soup = BeautifulSoup(res.text, "html.parser")

        dates = soup.findAll("td", {"align" : "center"})    ## 날짜 데이터
        numbers = soup.findAll("td", {"class" : "num"}) ##### 모든 숫자 데이터 긁어오기 // [0] : 종가, [1] : 전일비, [2] : 시가, [3] : 고가, [4] : 저가, [5] : 거래량

```
1. BeautifulSoup를 이용해서 html 데이터를 parser을 이용하여 html 구조로 텍스트화한다.
2. 날짜 데이터는 `<td align = center>`인 태그 안에 들어 있으므로 findAll을 이용해서 날짜 데이터를 찾아온다.
3. 숫자 데이터는 `<td class = num>`인 태그에 들어있고, 우선은 모든 숫자를 다 가져온다. 나중에 다른 숫자 데이터가 필요하다면 인덱싱을 통해 긁어올 수 있기 때문에 우선 다 저장해주자.
___

#### 3. 데이터를 데이터베이스에 저장하기
```python
        prices = []
        volumes = []
        for i in range(0,len(numbers),6):
            prices.append(''.join(numbers[i].text.split(',')))    
            volumes.append(''.join(numbers[i+5].text.split(','))) 
        for date, price, volume in zip(dates,prices,volumes):   
            date = '-'.join(date.text.split('.'))     
            if price == "\xa0": break    ##### 추가 코드 : 웹 페이지에서 데이터가 없을 경우 '\xa0'를 긁어오므로 이러한 데이터를 가져올경우 모든 종가 데이터를 긁어온 것으로 판단하고 break로 빠져나오기
            price = int(price) 
            volume = int(volume)    
            cur.execute("insert into daily_price values ('%s', '%s','%d','%d')" % (code,date,price,volume))    
        page = page + 1   
        
        if bool(soup.find("td", {"class" : "pgRR"})) != True : break  ## 만약, 마지막 페이지를 넘어가면 종료시키기 ("맨뒤" 가 존재하지 않으면 가장 마지막 페이지)
conn.commit()
conn.close()
```

1. 데이터를 저장하는 방식은 Day26과 동일하다.
2. 그런데 어제 코드를 돌리다가 한가지 오류가 발견되었다. 마지막 페이지에서 겉으로 보기에는 데이터가 없지만 `<td>`태그 틀은 그대로 존재하고 텍스트는 '\xa0'을 가지는 것을 볼 수 있었다.
3. `\xa0`는 int데이터가 아닌 텍스트 데이터이기 때문에 여기서 오류가 발생한다.
4. 따라서 `if price == "\xa0": break`를 넣어줌으로써 데이터가 없을 경우 빠져나오도록 설정해뒀다.
5. 그렇다면 마지막에 `if bool(soup.find("td", {"class" : "pgRR"})) != True : break`을 넣지 않아도 되는 것 아닌가 하는 생각을 할 수 있다. 왜냐하면 데이터가 없다면 모든 데이터를 긁어온 것으로 봐도 무방하다고 생각할 수 있다.
6. 그러나 모든 데이터가 완벽하지 않듯이 중간에 종가 데이터가 존재하지 않는 경우도 있다. 이 경우에 중간의 종가 데이터를 건너뛰고 그 이후의 종가 데이터도 수집해줘야 하기 때문에 맨 밑의 if문을 그대로 남겨두었다.