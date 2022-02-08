# TIL(Today I Learned)

___

> Fab/7th/2022_Multi campus_유선종 Day28

## 주가예측 프로젝트 3일차
오늘은 여태까지 만든 코드를 클래스화하는 작업을 했다.

### 1. __init__, del
```python
class Crawling:
    def __init__(self, host, user, password, charset):  ## host = 호스트명, user = 유저 이름, password = 유저 비밀번호, charset = 문자열 코드
        self.conn = pymysql.connect(host=host, user=user, password = password, charset= charset)
        self.cur = self.conn.cursor()   ## 커서 설정
    
    def __del__(self):
        self.conn.close()
```
1. `class '클래스명'`으로 클래스를 정의한다.
2. `__init__(self,변수)`은 최초로 실행되는 매서드를 의미한다. 특히, mysql에서는 접속을 해줘야 하므로 초기값을 mysql에 접속할 때 필요한 변수들로 설정하는 것이 좋다.
3. 그러므로 초기값으로 `self.coon = pymysql.connect()`와 `self.cur = self.conn.cursor()`을 설정해 앞으로 실행되는 모든 함수에 접속이 되어있는 상태에서 커서가 작동하도록 코드를 작성해준다.
4. 또한,`__del__`은 소멸 메서드로 `__init__`이 초기 설정을 하는데 사용한다면 `__del__`은 빠져나올때 사용한다. mysql에서는 접속을 끊는 행위가 빠져나오는 행동이므로 `self.conn.close()`를 넣어줘서 __del__을 선언해준다. 이 경우 class를 빠져나올때(class와 연관이 없는 명령어를 실행할 때) 자동으로 `self.conn.close()`를 실행해준다.

### 2. 테이블 생성 함수
```python
    def make_DB(self, DB_name):     ## 스키마 생성
        self.cur.execute(f"drop database if exists {DB_name}")  ## 이미 존재하는 DB 제거하기 
        self.cur.execute(f"create database IF NOT EXISTS {DB_name}")  ## INVESTAR 스키마 생성
    
    def make_Table(self,Table_name,DB_name):        ## 테이블 생성
        self.cur.execute(f"USE {DB_name}")   ## INVESTAR 스키마 선택
        self.cur.execute(f"DROP TABLE IF EXISTS {Table_name}")    ## 이전 자료 삭제
        self.cur.execute(f"create table if not exists {Table_name} (code char(6), name varchar(150))") ## company_info 생성
        self.conn.commit()
```
1. 만약, `A = Crawling('localhost','root','1234','utf8')`로 A가 클래스라고 선언해줬다고 하자.
2. 이 경우 `A.make_DB('스키마 이름')`을 실행해주면 스키마 이름으로 데이터베이스를 만들어준다.
3. 밑의 함수도 비슷한 알고리즘이다. `A.make_Table('테이블이름','스키마이름')`을 입력하면 해당 스키마에 테이블을 만들어준다. 여기서는 미션을 위해 필드로 6자리 문자열 속성을 가진 종목코드와 150자리 변동문자열 속성을 가진 회사명을 생성한다.

### 3. 종목코드와 회사명 DB에 저장하기
```python
    def make_Stocks(self, url, Table_name):
        table = pd.read_html(f'{url}', header = 0)     ## KRX에서 종목 크롤링
        for i in range(len(table[0]['회사명'])):    ## 모든 회사의 종목코드와 회사명 저장
            code = str(table[0]['종목코드'][i])     ## 종목코드
            name = str(table[0]['회사명'][i])       ## 회사명
            if len(code) != 6:
                code = code.zfill(6)        ## 5자리 이하의 숫자 앞에 0 넣어주기 // 예) 종목코드가 123이라면 000123으로 만들어주기
            self.cur.execute("insert into %s values ('%s', '%s')" % (Table_name,code,name))       ## company_info 테이블에 입력
        self.conn.commit()
```
1. url은 내가 크롤링할 주소를 입력받는다. Table_name은 데이터를 담을 테이블을 입력해준다.
2. 크롤링한 데이터는 `pd.raed_html`을 이용해서 데이터프레임 형식으로 받는다. 이 경우에 table['필드명']을 이용해서 해당 열 데이터를 인덱싱해준다.
3. for문을 이용해서 종목코드와 회사명을 `insert into`를 이용해서 테이블에 입력해준다.
> 이때, 종목코드는 6자리가 아니면 앞에 0을 채워준다. 예를들어, 종목코드가 123이라면 000123이 될 수 있도록 바꿔준다. 크롤링한 데이터가 파이썬으로 넘어오면서 앞의 000을 생략하고 데이터를 받아오기 때문에 수정해줄 필요가 있다.

### 4. 네이버에서 긁어오는 데이터를 저장할 테이블 생성
```python
def make_PriceTable(self,Table_name2):      ## 데이터를 저장할 daily_price 테이블 생성
        self.cur.execute(f"DROP TABLE IF EXISTS {Table_name2}") ## 이전 데이터 삭제
        self.cur.execute(f"create table if not exists {Table_name2}(code char(6), name varchar(150),date Date, price_end int, price_compared int, price_start int, price_high int, price_low int, volume int)")
        #### 테이블의 컬럼 1: 종목코드 / 2: 회사명 / 3: 날짜 / 4: 종가 / 5: 전일대비 / 6: 시가 / 7: 고가 / 8: 저가 / 9: 거래량

```
네이버 시세창에서 제공하는 데이터는 날짜, 종가, 전일대비, 시가, 고가, 저가, 거래량으로 총 7가지 데이터를 제공한다. 또한, 기본키로 설정하거나 참조 데이터로 설정해줄 종목코드와 회사명을 같이 입력하도록 하여 총 9개의 열을 생성해준다.

### 5. 종목코드와 페이지를 입력하면 해당 종목과 페이지의 데이터를 긁어오는 함수 설정
주의하자. 매우 길다. 우선 하나하나 분리하기 전에 `if code_number:`와 `else:`를 나눠서 보자. 큰 구조를 파악하고 상세히 설명하겠다.
```python
    ### 종목코드와 회사명을 읽어올 테이블, 데이터를 넣을 테이블, 종목코드, 읽어올 페이지 수 ##
    ## ※ 주의 ※ 종목코드를 지정하지 않을 경우 모든 종목의 데이터를 긇어옴  /  ※ 주의 ※ 페이지를 설정하지 않을 경우 모든 페이지를 읽어옴 ####   
    def naver_Stockprice(self,read_Table, insert_Table, code_number = 0, pages = 99999):
        self.cur.execute(f"select * from {read_Table}")     ## read_Table의 데이터 불러오기
        code_list = []      ## 종목코드 리스트
        name_list = []      ## 회사명 리스트
        while True:
            row = self.cur.fetchone()
            if row == None:
                break
            a = row[0]
            b = row[1]
            code_list.append(a)
            name_list.append(b)
                    
        if code_number:  ## 코드넘버를 입력한 경우
            name_code = name_list[code_list.index(f'{code_number}')]    ## 회사명 리스트
            page = 1
            while True:
                url = f"https://finance.naver.com/item/sise_day.naver?code={code_number}&page={page}"    ## 네이버 시세창만 보여주는 페이지
                 ## header를 이용해서 거부된 agent를 허용된 agent로 바꿔주기
                headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.3'}
                res = requests.get(url, headers = headers)
                res.raise_for_status()    
    
                soup = BeautifulSoup(res.text, "html.parser")
                dates = soup.findAll("td", {"align" : "center"})    ## 날짜 데이터
                numbers = soup.findAll("td", {"class" : "num"})
                ##### 모든 숫자 데이터 긁어오기 // [0] : 종가, [1] : 전일비, [2] : 시가, [3] : 고가, [4] : 저가, [5] : 거래량 ####
                
                #### 저장공간 ####
                prices_end =[]
                prices_compared = []
                prices_start = []
                prices_high = []
                prices_low = []
                volumes = []
                
                for i in range(0,len(numbers),6): ### 종가 데이터에서 쉼표(,)를 없애고 리스트 안의 모든 요소를 join을 이용해서 하나로 이어붙이기
                    prices_end.append(''.join(numbers[i].text.split(',')))
                    prices_compared.append(''.join(numbers[i+1].text.split(','))) 
                    prices_start.append(''.join(numbers[i+2].text.split(',')))  
                    prices_high.append(''.join(numbers[i+3].text.split(',')))
                    prices_low.append(''.join(numbers[i+4].text.split(',')))
                    volumes.append(''.join(numbers[i+5].text.split(',')))
                print(prices_end)    
                for date, price_end, price_compared, price_start, price_high, price_low, volume in zip(dates,prices_end,prices_compared,prices_start,prices_high,prices_low,volumes):   ### zip을 이용해서 한줄한줄 읽도록 만들기
                    if price_end == "\xa0": break    ## None값처럼 없는 데이터 값이 나올 경우 break를 이용해서 패스해주기
                    date = '-'.join(date.text.split('.'))     ## 텍스트만 발라내서 date 형식으로 만들어주기 // 예시 : 2022-01-20
                    price_end = int(price_end)  ## int로 바꿔주기
                    price_compared = int(price_compared)  ## int로 바꿔주기
                    price_start = int(price_start)  ## int로 바꿔주기
                    price_high = int(price_high)  ## int로 바꿔주기
                    price_low = int(price_low)  ## int로 바꿔주기
                    volume = int(volume)    ## int로 바꿔주기
                    self.cur.execute("insert into %s values ('%s', '%s', '%s', '%d', '%d', '%d', '%d', '%d', '%d')" % (insert_Table, code_number, name_code, date, price_end, price_compared, price_start, price_high, price_low, volume))   
                if pages == page : break ## 원하는 페이지만큼 수집
                page = page + 1   ## 다음 페이지
            
                if bool(soup.find("td", {"class" : "pgRR"})) != True : break  ## 만약, 마지막 페이지를 넘어가면 종료시키기 ("맨뒤" 가 존재하지 않으면 가장 마지막 페이지)
            self.conn.commit()
            
        else:      ## 코드 넘버를 입력하지 않은 경우
            for code, name in zip(code_list, name_list):
                page = 1 ## 페이지
                while True:
                    url = f"https://finance.naver.com/item/sise_day.naver?code={code}&page={page}"    ## 네이버 시세창만 보여주는 페이지
                     ## header를 이용해서 거부된 agent를 허용된 agent로 바꿔주기
                    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.3'}
                    res = requests.get(url, headers = headers)
                    res.raise_for_status()    

                    soup = BeautifulSoup(res.text, "html.parser")
                    dates = soup.findAll("td", {"align" : "center"})    ## 날짜 데이터
                    numbers = soup.findAll("td", {"class" : "num"})
                    ##### 모든 숫자 데이터 긁어오기 // [0] : 종가, [1] : 전일비, [2] : 시가, [3] : 고가, [4] : 저가, [5] : 거래량 ####

                    #### 저장공간 ####
                    prices_end =[]
                    prices_compared = []
                    prices_start = []
                    prices_high = []
                    prices_low = []
                    volumes = []

                    for i in range(0,len(numbers),6): ### 종가 데이터에서 쉼표(,)를 없애고 리스트 안의 모든 요소를 join을 이용해서 하나로 이어붙이기
                        prices_end.append(''.join(numbers[i].text.split(',')))
                        prices_compared.append(''.join(numbers[i+1].text.split(','))) 
                        prices_start.append(''.join(numbers[i+2].text.split(',')))  
                        prices_high.append(''.join(numbers[i+3].text.split(',')))
                        prices_low.append(''.join(numbers[i+4].text.split(',')))
                        volumes.append(''.join(numbers[i+5].text.split(',')))

                    for date, price_end, price_compared, price_start, price_high, price_low, volume in zip(dates,prices_end,prices_compared,prices_start,prices_high,prices_low,volumes):   ### zip을 이용해서 한줄한줄 읽도록 만들기
                        if price_end == "\xa0": break    ## None값처럼 없는 데이터 값이 나올 경우 break를 이용해서 패스해주기
                        date = '-'.join(date.text.split('.'))     ## 텍스트만 발라내서 date 형식으로 만들어주기 // 예시 : 2022-01-20
                        price_end = int(price_end)  ## int로 바꿔주기
                        price_compared = int(price_compared)  ## int로 바꿔주기
                        price_start = int(price_start)  ## int로 바꿔주기
                        price_high = int(price_high)  ## int로 바꿔주기
                        price_low = int(price_low)  ## int로 바꿔주기
                        volume = int(volume)    ## int로 바꿔주기
                        self.cur.execute("insert into %s values ('%s', '%s', '%s', '%d', '%d', '%d', '%d', '%d', '%d')" % (insert_Table, code, name, date, price_end, price_compared, price_start, price_high, price_low, volume))   
                    if pages == page : break ## 원하는 페이지만큼 수집
                    page = page + 1   ## 다음 페이지

                    if bool(soup.find("td", {"class" : "pgRR"})) != True : break  ## 만약, 마지막 페이지를 넘어가면 종료시키기 ("맨뒤" 가 존재하지 않으면 가장 마지막 페이지)
                self.conn.commit()
```

#### 1. 종목코드와 회사명 리스트 만들기
```python
    def naver_Stockprice(self,read_Table, insert_Table, code_number = 0, pages = 99999):
        self.cur.execute(f"select * from {read_Table}")     ## read_Table의 데이터 불러오기
        code_list = []      ## 종목코드 리스트
        name_list = []      ## 회사명 리스트
        while True:
            row = self.cur.fetchone()
            if row == None:
                break
            a = row[0]
            b = row[1]
            code_list.append(a)
            name_list.append(b)
```
1. 여기서 필요한 변수는 `read_Table`이다. 즉, 우리가 테이블에 저장해둔 종목코드와 회사명을 다시 DB에서 불러오기 위해서 테이블을 설정해준다.
2. `cur.fetchone()`은 테이블의 제일 윗 행부터 차례로 한줄한줄 읽어주는 명령어이다. while을 통해 fetchone을 반복해서 내려가다가 더이상 값이 없으면 `if row == None:break`를 만나 끝나게 된다.
3. 종목코드와 회사명은 `code_list`와 `name_list`에 잘 담겨있다.

#### 2. 네이버 크롤링
```python
    def naver_Stockprice(self,read_Table, insert_Table, code_number = 0, pages = 99999):
        if code_number:  ## 코드넘버를 입력한 경우
            name_code = name_list[code_list.index(f'{code_number}')]    ## 회사명 리스트
            page = 1
            while True:
                url = f"https://finance.naver.com/item/sise_day.naver?code={code_number}&page={page}"    ## 네이버 시세창만 보여주는 페이지
                 ## header를 이용해서 거부된 agent를 허용된 agent로 바꿔주기
                headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.3'}
                res = requests.get(url, headers = headers)
                res.raise_for_status()    
    
                soup = BeautifulSoup(res.text, "html.parser")
                dates = soup.findAll("td", {"align" : "center"})    ## 날짜 데이터
                numbers = soup.findAll("td", {"class" : "num"})
##### 모든 숫자 데이터 긁어오기 // [0] : 종가, [1] : 전일비, [2] : 시가, [3] : 고가, [4] : 저가, [5] : 거래량 ####
```
1. 여기서 필요한 변수는 code_number이다. 맨 위를 보면 함수의 요소로 `code_number = 0`을 받는 것을 알 수 있는데, 이는 기본값으로 0을 받는다는 의미이다. 즉, 아무런 값을 입력하지 않으면 `code_number`는 0을 받고 bool값은 `False`를 받는다. 따라서 `if code_number:`를 실행할 때 기본값을 받았다면 `else:`로 건너뛰게 된다.
2. 만약, code_number값을 줬다면 bool값은 `True`가 되면서 위의 명령어를 실행한다.
3. `name_code = name_list[code_list.index(f'{code_number}')]`는 해당 코드명이 있는 리스트에서 해당 인덱스값을 가져와 name_list의 인덱싱을 할때 사용하여 해당 코드와 짝지어진 회사명을 찾겠다는 의미이다. 예를들어, 삼성전자의 종목코드가 123456일때, 123456이라는 숫자의 위치값을 찾아 삼성전자라는 회사명을 찾겠다는 소리이다.
4. while문으로 진입하면서 크롤링의 기본 과정을 수행한다. 여기서 headers는 네이버가 어떤 특정 유저가 아니면 접근을 차단하는데, 나는 이상한 유저가 아니니까 접근을 차단하지 말라는 것을 선언하는 명령어이다.
> 자세한 내용은 Day27을 참고하자.
5. beautifulsoup을 사용해서 날짜 데이터와 숫자가 들어있는 데이터를 뽑아온다. 숫자는 위에서 표시한 것과 같이 인덱싱값을 갖는다.

#### 3. 데이터 정제
```python
#### 저장공간 ####
                    prices_end =[]
                    prices_compared = []
                    prices_start = []
                    prices_high = []
                    prices_low = []
                    volumes = []

                    for i in range(0,len(numbers),6): ### 종가 데이터에서 쉼표(,)를 없애고 리스트 안의 모든 요소를 join을 이용해서 하나로 이어붙이기
                        prices_end.append(''.join(numbers[i].text.split(',')))
                        prices_compared.append(''.join(numbers[i+1].text.split(','))) 
                        prices_start.append(''.join(numbers[i+2].text.split(',')))  
                        prices_high.append(''.join(numbers[i+3].text.split(',')))
                        prices_low.append(''.join(numbers[i+4].text.split(',')))
                        volumes.append(''.join(numbers[i+5].text.split(',')))
```
1. 데이터를 담아줄 공간을 리스트 형태로 만들어준다.
2. 숫자 데이터는 65,500 처럼 중간에 쉼표(,)가 포함되어 있다. 이를 발라내기 위해 split으로 쉼표를 없애주고 join을 이용해서 split으로 인해 분리되었던 데이터들을 다시 붙여준다. 그러면 65,500이 65500으로 정제된다.

#### 4. 데이터 입력
```python
for date, price_end, price_compared, price_start, price_high, price_low, volume in zip(dates,prices_end,prices_compared,prices_start,prices_high,prices_low,volumes):   ### zip을 이용해서 한줄한줄 읽도록 만들기
                    if price_end == "\xa0": break    ## None값처럼 없는 데이터 값이 나올 경우 break를 이용해서 패스해주기
                    date = '-'.join(date.text.split('.'))     ## 텍스트만 발라내서 date 형식으로 만들어주기 // 예시 : 2022-01-20
                    price_end = int(price_end)  ## int로 바꿔주기
                    price_compared = int(price_compared)  ## int로 바꿔주기
                    price_start = int(price_start)  ## int로 바꿔주기
                    price_high = int(price_high)  ## int로 바꿔주기
                    price_low = int(price_low)  ## int로 바꿔주기
                    volume = int(volume)    ## int로 바꿔주기
                    self.cur.execute("insert into %s values ('%s', '%s', '%s', '%d', '%d', '%d', '%d', '%d', '%d')" % (insert_Table, code_number, name_code, date, price_end, price_compared, price_start, price_high, price_low, volume))   
                if pages == page : break ## 원하는 페이지만큼 수집
                page = page + 1   ## 다음 페이지
            
                if bool(soup.find("td", {"class" : "pgRR"})) != True : break  ## 만약, 마지막 페이지를 넘어가면 종료시키기 ("맨뒤" 가 존재하지 않으면 가장 마지막 페이지)
            self.conn.commit()
```
1. zip을 이용해서 모든 데이터들을 하나로 묶어준다. 예를 들어, (1,2,3), (4,5,6), (7,8,9)라는 튜플 데이터를 zip으로 묶어주면 (1,4,7), (2,5,8), (3,6,9)로 묶어준다.
2. `if price_end == "\xa0": break`는 네이버에서 데이터를 긁어올때 존재하지 않는 데이터라면 텍스트값으로 "\xa0"을 갖는것을 이용하여 이 값을 가지면 break로 빠져나오도록 설정했다.
3. date는 DATE 형식으로 만들어주기 위해서 점(.)을 제거하고 '-'으로 붙여줬다.
4. 숫자 데이터는 `int()`를 이용해서 정수로 바꿔주고 테이블에 `insert into`로 넣어준다.
5. 여기서 함수에 변수로 받았던 pages가 쓰인다. 만약 pages = 100 이라면 100페이지가 될 때까지는 while문을 실행한다. 그러나 page는 while문이 실행되면서 1씩 증가하고 pages = page가 되면 100페이지까지 데이터 수집이 마무리되므로 break를 이용해서 빠져나온다.
6. 그 밑에 `if bool(soup.find("td", {"class" : "pgRR"})) != True : break`은 pages를 설정하지 않으면 모든 페이지를 긁어오게 되는데 마지막 페이지에서 break로 빠져나오기 위해 설정해두었다.

#### 5. else문
else문은 모든 종목의 데이터를 긁어오는 명령어이다. 이는 Day27에서 자세히 설명했고, 위의 설명과 겹치는 부분이 많으므로 생략하도록 한다.

### 6. DB에서 주식 데이터 불러오기
```python
def take_data(self,insert_Table, name, start_date, end_date):  ## 회사명이 name인 데이터중에서 시작 날짜와 마지막 날짜 사이의 데이터 수집
        self.cur.execute(f"select * from {insert_Table} where name ='{name}' and date between '{start_date}' and '{end_date}'")
        Data = self.cur.fetchall()
        return pd.DataFrame(Data, columns = ['종목코드','회사명','날짜','종가','전일비','시가','고가','저가','거래량'])     ## 데이터프레임 형태로 데이터 저장
```
1. 여기서는 변수로 `name = 회사명`을 입력하면 해당 회사명을 찾아 시작날짜와 마지막 날짜 사이의 모든 데이터를 불러온다.
2. `cur.fetchall()`은 모든 행의 데이터를 한번에 불러온다.
3. fetchall로 불러온 데이터는 그 값을 pd.DataFrame에 넣어주면 자동으로 DataFrame형태로 변환해서 저장해준다. 매우 편리한 기능이지만 열 이름을 설정해주지는 않으므로 `colums = '열 이름'`속성을 설정해줘서 입력해주자.