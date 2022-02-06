# TIL(Today I Learned)

___

> Fab/6th/2022_Multi campus_유선종 Day26

## 주가예측 프로젝트
오늘은 금요일에 시작한 주가예측 알고리즘 코딩 프로젝트에 대한 정리를 하려고 한다.

### 1. pymysql로 mysql접속

```python
import pymysql

conn = pymysql.connect(host='localhost', user='root', password = 'yousj928', charset='utf8')
cur = conn.cursor()
```


1. 첫번째로 내가 할 작업은 웹에서 해당 기업의 과거 주가를 긁어오는 작업을 하기 전에 데이터베이스에 스키마를 생성하고 테이블을 생성하여 저장공간을 만드는 작업이다.
2. `import pymysql`은 mysql을 파이썬에서 조작할 수 있는 라이브러리를 불러온다.
3. pymysql에서 가장 먼저 해야할 작업은 크게 2가지이다.
    1. mysql에 접속해주는 명령어를 작성해준다. 명령어는 `pymysql.connect(host='localhost', user = '계정이름', password = '비밀번호', DB = '스키마 이름', charset = 'UTF-8')`이다.
       1. host 속성은 현재 접속하려는 host의 IP 주소를 입력한다. 보통 개인 컴퓨터에서 작업을 하면 로컬 속성이기 때문에 'localhost'를 기본으로 깔고 시작한다고 생각하자.
       2. user은 계정을 입력한다. 여기서 나는 root계정밖에 없기 때문에 root를 입력한다.
       3. password는 해당 계정의 비밀번호를 입력한다. 비밀번호가 없다면 'NULL'을 입력해주면 된다.
       4. DB는 내가 입력하려는 스키마를 입력한다. 위의 코드에서는 DB가 없는데 내가 생성하려는 스키마가 현재 존재하지 않기 때문이다. 즉, 새로운 스키마를 생성해서 작업하고 싶다면 생략하자.
       5. charset은 charater set의 약자로 문자 코드에 대한 설정이다. 한글을 사용하면 UTF-8을 사용해야 한다.
    2. 접속을 했다면 mysql에서 명령어를 입력할 수 있도록 제어해주는 명령어가 필요하다. `conn.cursor()`을 입력하면 위에서 입력한 user로 들어가서 커서를 제어한다.
    > Day08_file_cursor를 보면 파일에서 포인터의 역할에 대해 서술한 내용이 있는데, 파일에서의 포인터가 여기서는 커서라고 생각하면 된다. 즉, 이제부터 쿼리문을 한줄한줄 작성했을때 실행시켜주는 커서 역할을 cur에 부여한다.
    > 또한 여기서도 커서는 포인터의 역할을 하기 때문에 이중 for문을 중복할경우 충돌하는 문제가 발생한다. 이에 대한 내용은 아래에서 더 자세히 서술하겠다.
___
### 2. 데이터베이스에 테이블 생성하기

```python
cur.execute("drop database if exists StockPrice")
cur.execute("create database IF NOT EXISTS StockPrice")  ## StockPrice 데이터베이스 생성
cur.execute("USE StockPrice")   ## StockPrice 선택
cur.execute("DROP TABLE IF EXISTS company_info")    ## 이전 자료 삭제
cur.execute("create table if not exists company_info(code char(6), Korean_name varchar(150))") ## company_info 생성
```

1. `cur.execute("drop database if exists StockPrcie")` 명령어는 cursor를 작동시켜서 명령어를 실행(execute)해주는데, 괄호안의 명령어를 실행해준다. 여기서 drop database는 존재하는 스키마를 삭제해준다. if exists는 StockPrice라는 스키마가 존재할 경우에만 drop database를 실행해준다.
> 여기서 drop database를 첫번째로 넣은 이유는 내가 짠 코드가 잘못될 경우 잘못 형성된 스키마가 그대로 남아있기 때문에 잘못된 코드를 고쳐도 여전히 남아있는 잘못된 스키마 때문에 실행이 안된다. 간혹 이런 사소한 것 때문에 시간을 날리는 경우가 있으니 꼭 작성해주자.

2. `cur.execute("create database if not exists StockPrice")` 명령어는 만약 StockPrice 스키마가 없을 경우에 생성을 해주는 명령어를 실행해준다.

3. `cur.execute("USE StockPrice")`명령어는 StockPrice에서 작업을 하겠다고 선언하는 명령어이다. 보통은 `pymysql.connect`명령에서 내가 작업할 DB를 선언하지만, 위에서 나는 생략했으므로 여기서 선언해줘야 한다.
4. `cur.execute("DROP TABLE IF EXISTS company_info")` 명령어는 company_info라는 테이블이 존재한다면 삭제해준다. 이 명령어를 넣은 이유는 1.에서의 이유과 같다.
5. `cur.execute("create table if not exists company_info(code char(6), Korean_name varchar(150))")` 명령어는 필드를 생성하는 명령어이다.
    - code는 상장주식에 대해 표준코드를 부여하는데, 이중 6자리의 숫자와 영어만 사용하는 단축 코드를 의미한다. 예를들어, 삼성전자의 단축코드는 005930이다. 무조건 6자리의 숫자와 영어가 들어가기 때문에 char(6)으로 제한을 뒀다.
    - Korean_name은 상장주식의 한글 회사명이다. 여기서 한글은 3 byte의 크기를 차지한다. 따라서 한글로만 이루어진 문자열인 경우 `varchar(3*글자수)`로 입력해줘야 한다. 여기서는 넉넉하게 공간을 할당했다.
___
### 3. 테이블에 데이터 입력

```python
import pandas as pd

table = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header = 0)     ## KRX에서 종목 크롤링

for i in range(len(table[0]['회사명'])):    ## 원하는 회사 갯수 설정
    code = str(table[0]['종목코드'][i])     ## 종목코드
    name = str(table[0]['회사명'][i])       ## 회사명
    if len(code) != 6:
        code = code.zfill(6)        ## 5자리 이하의 숫자 앞에 0 넣어주기
    cur.execute("insert into company_info values ('%s', '%s')" % (code,name))       ## 데이터베이스에 입력
conn.commit()
```

1. `pd.read_html`명령어를 이용해서 한국거래소(KRX)에서 제공하는 상장 주식에 대한 정보가 담긴 url 주소를 입력한다. 여기서 크롤링을 통해 데이터를 입력할것이다.
2. `len(table)`을 실행하면 결과값으로 1이 나오는데, 여기서 print(table)을 실행한 결과는 다음과 같다.

<img src="https://user-images.githubusercontent.com/97590480/152682216-2ff9455d-5e9e-4218-ad3e-c45f5c8069a6.png">

> pandas에서 배웠던 DataFrame 형태로 데이터가 담겨있는 것을 볼 수 있다.
   1. 이 경우에 평소의 파이썬의 인덱싱이 아니라 pandas의 인덱싱을 사용해야 한다. 우리가 원하는 종목코드와 회사명이므로 `table['종목코드']`를 이용해서 인덱싱할 수 있다.
   2. 하지만 실제로 실행하면 오류가 난다. `type(talbe)`을 실행하면 list로 나온다. 즉, `len(table)`이 1로 나온 이유는 리스트 안에 DataFrame이 담겨져 있기 때문이다.
   3. 그러므로 `table[0]['종목코드']`를 입력해줘야 오류 없이 인덱싱이 된다.
3. `if len(code) != 6: code = code.zfill(6)` 명령어는 6자리를 맞춰주기 위해서이다.
    - 여기서 규칙을 발견할 수 있었는데, 만약 단축코드가 '123'이라면 이는 앞의 '000'을 생략해서 작성한 것을 알 수 있었다. 즉, 우리가 원하는 데이터는 000이 생략되지 않은 '000123'이므로 데이터 앞에 0을 채워주는 `.zfill(6)` 명령어를 사용한다. 괄호안의 숫자는 0을 몇개 넣을지를 제한을 설정해주는 자릿수를 의미한다.
4. `cur.execute("insert into company_info values ('%s', '%s')" % (code,name))`을 이용해서 데이터를 입력해주고, for문을 이용해서 반복해주면 데이터가 잘 입력되는 것을 볼 수 있다.
5. `conn.commit()`은 입력된 데이터가 잘 들어갔다는 확인 도장을 한번 꾹 찍어주는 느낌의 명령어이다. 많은 데이터를 입력했을 경우 한번씩 넣어주자.
___

### 4. 종가 데이터 입력할 공간 생성

```python
cur.execute("DROP TABLE IF EXISTS daily_price") ## 이전 데이터 삭제
cur.execute("create table if not exists daily_price(code char(6), date DATE,price int, volume int)") ## 넣을 공간 생성
cur.execute("select * from company_info")   ## 종목 코드를 읽기 위해 테이블 열기

list = []
while True:
    row = cur.fetchone()    ## company_info에서 한줄씩 읽기
    if row == None:
        break
    list.append(row[0]) ## 이렇게 하나의 메모리로 담지 않으면 cur을 두번 사용하게 됨
```

<img src="https://user-images.githubusercontent.com/97590480/152685357-c53867c2-d8c1-4f65-a08b-f4c256af2e6b.png">

> 위의 코드를 실행한 결과 리스트 안에 종목코드들이 잘 담긴 것을 볼 수 있다.

1. 이번에도 위에서 동일하게 종가 데이터를 입력할 공간을 만들어준다. date는 날짜 데이터인 DATE를, price는 가격, volume은 거래량이므로 정수 데이터로 속성을 지정해줬다.
2. `cur.execute("select * from company_info)` 명령어를 입력한다. 이는 우리가 company_info에 입력한 종목코드를 불러와서 사용하기 위해 입력해줘야 한다. 밑의 `fetchone()`명령어가 종목코드를 읽는 명령어인데, 둘이 한 세트이므로 반드시 같이 입력해주자.
3. while문을 이용해서 종목코드의 데이터를 리스트에 담아준다. 여기서 `fetchone()`은 파일에서 포인터와 비슷한 역할을 한다. 포인터가 내려가면서 한줄한줄 데이터를 읽듯, `cur.fetchone()`을 사용해서 한줄한줄 내려가면서 데이터를 읽는다.
4. 그러므로 한줄한줄 읽다가 마지막 데이터를 읽으면 더이상 데이터가 없어 row에 None값이 들어가게 된다. 이때 if문을 사용해서 break로 while문을 빠져나오게 된다.
___
### 5. 셀레니움을 통해 종가 데이터 긁어오기
우선 셀레니움을 사용하면 안된다. 간단한 작업이라면 셀레니움이 가능하지만 매우 많은 작업을 수행할 경우 컴퓨터에 부하가 걸릴 수 있다. 물론 난 이걸 몰랐고 이미 작성한 코드가 아깝기 때문에 여기서 소개하고 다음에 bs4를 이용한 크롤링을 소개하겠다.

```python
from selenium import webdriver

driver = webdriver.Chrome(r"/Users/yuseonjong/Downloads/chromedrive
page = 1 ## 페이지

for code in list:
    while True:
        url = f"https://finance.naver.com/item/sise_day.naver?code={code}&page={page}"    ## 네이버 시세창만 보여주는 페이지
        driver.get(url)     ## 크롬 열기

        dates = driver.find_elements_by_class_name("tah.p10.gray03")    ## 날짜 데이터
        numbers = driver.find_elements_by_class_name("tah.p11") ##### 모든 숫자 데이터 긁어오기 // 0 : 종가, 1 : 전일비, 2 : 시가, 3 : 고가, 4 : 저가, 5 : 거래량
        prices = []
        volumes = []
        for i in range(0,len(numbers),6):
            prices.append(''.join(numbers[i].text.split(',')))      ### 종가 데이터에서 쉼표(,)를 제외하고 리스트 안의 모든 요소를 join을 이용해서 하나로 이어붙이기
            volumes.append(''.join(numbers[i+5].text.split(',')))     ### 종가 데이터에서 쉼표(,)를 제외하고 리스트 안의 모든 요소를 join을 이용해서 하나로 이어붙이기
        for date, price, volume in zip(dates,prices,volumes):   ### zip을 이용해서 한줄한줄 읽도록 만들기
            date = '-'.join(date.text.split('.'))     ## 텍스트만 발라내서 date 형식으로 만들어주기 // 예시 : 2022-01-20
            price = int(price)  ## int로 바꿔주기
            volume = int(volume)    ## int로 바꿔주기
            cur.execute("insert into daily_price values ('%s', '%s','%d','%d')" % (row[0],date,price,volume))    ## 값 입력 0 : 코드, 1 : 날짜, 2 : 가격, 3 : 거래량
        page += 1   ## 다음 페이지

        if bool(driver.find_elements_by_xpath(f"""//*[text()='맨뒤
	        	']""")) != True : break  ## 만약, 마지막 페이지를 넘어가면 종료시키기 ("맨뒤" 가 존재하지 않으면 가장 마지막 페이지)

conn.commit()
conn.close()
```
1. 여기서 사용한 웹페이지는 네이버 주식 페이지인데, 위에서처럼 종목코드와 페이지를 제외하고는 동일했기 때문에 포맷팅을 사용하여 종목코드와 페이지를 입력하면 해당 url로 이동하도록 url을 만들었다.
2. dates와 numbers에 날짜 데이터와 숫자 데이터를 넣었다. 물론 모든 숫자 데이터가 필요하지는 않지만 클래스 이름이 모두 겹쳤기 때문에 어쩔 수 없이 모든 숫자 데이터를 수집하고 필요한 데이터만 인덱싱을 통해서 뽑아내는 방식을 채택했다.
3. 날짜 데이터는 '2022.01.01', 숫자 데이터는 '75,300'처럼 각자 점과 쉼표가 포함되어 있기 때문에 점과 쉼표를 `split`을 이용해서 발라내주고 리스트에 따로따로 저장되어 있기 때문에 숫자는 `''.join`을 이용해서 그냥 붙이고 날짜 데이터는 입력할 때 '-'로 구분해주기 때문에 `'-'join`을 이용한다. 또한 날짜 데이터는 문자열로 입력해주면 된다.
4. 데이터베이스에 입력할 수 있게 적절히 데이터를 변형해주고 `cur.execute("insert into daily_price values ('%s', '%s','%d','%d')" % (row[0],date,price,volume))`를 이용해서 데이터를 테이블에 넣어주면 된다. 
5. 밑에 있는 if문은 while문을 종료시키기 위한 조건이다. 웹페이지 아래에 페이지를 선택하는 칸이 있는데, 그 중에 "맨뒤"가 존재하는 것을 확인할 수 있었다. 이 "맨뒤"는 가장 마지막 페이지를 선택하면 웹페이지 상에서 사라지므로 가장 마지막 데이터를 수집하고 나서 더이상 수집하지 않도록 만드는 스위치 역할을 부여했다.
6. for문을 다 시행하면 모든 상장주식에 대한 과거의 종가 데이터를 수집 완료하므로 `conn.commit()`으로 확인 도장을 찍어주고 `conn.close()`를 통해 mysql을 종료해준다.
___
### 6. fetchone()을 사용할 때 발생하는 오류
위에서 cursor()를 설명할 때 for문을 중복 사용할 경우 충돌하는 문제가 발생한다고 말했었다. 이와 관련된 내용을 아래에 서술하고자 한다. 우선 코드를 보자.

```python
while True:
    row = cur.fetchone()   ########### <============== 충돌 지점 
    if row == None:
        break
    DATA = row[0]
    page = 1
    for code in DATA ############# <================= 충돌 지점
        while True:
            url = f"https://finance.naver.com/item/sise_day.naver?code={code}&page={page}" 
            driver.get(url)    

            dates = driver.find_elements_by_class_name("tah.p10.gray03")    
            numbers = driver.find_elements_by_class_name("tah.p11") 
            prices = []
            volumes = []
            for i in range(0,len(numbers),6):
                prices.append(''.join(numbers[i].text.split(','))) 
                volumes.append(''.join(numbers[i+5].text.split(','))) 
            for date, price, volume in zip(dates,prices,volumes):   
                date = '-'.join(date.text.split('.'))  
                price = int(price) 
                volume = int(volume)    
                cur.execute("insert into daily_price values ('%s', '%s','%d','%d')" % (row[0],date,price,volume))  ########## <================= 충돌 지점
            page += 1   

            if bool(driver.find_elements_by_xpath(f"""//*[text()='맨뒤
    	        	']""")) != True : break  

conn.commit()
conn.close()
```
- 위의 코드는 내가 설명했던 코드와 거의 유사하다. 단지 다른 점은 밑의 `for code in list`에서 `for code in DATA`로 바꾸고 for문을 while문 안에 넣어 이중으로 돌렸다는 것이 다른 점이다.
- 그러나 이 경우에 커서는 오직 하나의 작업만 실행하므로 충돌하게 된다.
    1. `row = cur.fetchone()`을 사용하여 한줄한줄씩 데이터를 읽는 명령어를 할당했다. 여기서 우리는 커서를 한번 사용했다.
    2. `cur.execute("insert into daily_price values ('%s', '%s','%d','%d')" % (row[0],date,price,volume))`을 사용하여 데이터를 입력하는 명령어를 할당했다.
- 나는 당연히 execute를 사용하고 다시 fetchone 명령어를 실행할줄 알았지만 두번째 코드부터는 row에 None이 할당되면서 break로 빠져나왔다.
  - 즉 우리는 커서를 fetchone을 이용해 첫번째 코드를 찾는데 한번 사용했고, 두번째부터는 2번째 코드를 찾는데 커서를 사용하는 것이 아닌 데이터를 입력하는 execute명령어를 실행하는데 사용하였다. 그리고 커서는 마지막까지 내려가 더이상 읽을 데이터가 없어서 None을 할당하고 끝나버렸다. *왜 None이 할당되었는지는 밑에서 자세하게 설명한다.*
  - 파일에서 포인터가 파일을 한줄한줄 읽고 마지막까지 내려가면 더이상 읽을 데이터가 없듯이, cursor도 비슷한 문제가 발생한 것이다.
- 우리는 이중 for문의 포인터 문제를 해결하기 위해서는 두가지 해결책을 제시할 수 있었다.
    1. 포인터를 다시 위로 올려주는 명령어를 입력해준다. 이는 `f.seek(0)`를 이용해 포인터를 다시 처음으로 올려주었다.
    2. 포인터가 충돌하지 않도록 이중 for문을 사용하지 않는다.
___
#### 여기서 우리는 cursor도 첫번째처럼 명령어를 사용해서 해결할 수 있을까 생각할 수 있지만 이는 귀찮은 작업이 들어간다. 억지로 fetchone을 이용해서 위에서 의도한 코드를 작성해보겠다.

```python
fetchone_repeat = 1
while True
    cur.execute("select * from company_info") ## 테이블 변경
    for i in range(fechone_repeat):
        row = cur.fehchone()    
    DATA = row[0]
    for code in DATA:
        #### 이하 동문 ####
    fethone_repeat += 1
```

1. 우리는 위에서 fetchone과 `select * from company_info`가 한 세트라는 것을 배웠다. 즉, select문으로 테이블을 열고 fetchone으로 테이블의 데이터를 한줄한줄 읽는다. __문제는 cursor를 진행하면서 테이블이 daily_price로 바뀐 것이다.__
2. 여기서 오류가 난 코드에서는 while문 안에 `select * from company_info`이 없었기 때문에 현재 우리가 사용하고 있는 테이블은 `daily_price`이다. __왜냐하면 우리는 `cur.execute("insert into daily_price ~~")`를 실행하여 daily_price 테이블로 이동하여 데이터를 입력해줬다.__
3. 여기서 fetchone을 사용하면 `daily_price`에서 입력한 마지막 데이터 행의 다음 행으로 넘어가게 된다. 당연히 입력한 데이터가 없기 때문에 None이 뜬다.
4. 즉, 우리의 커서는 현재 `daily_price`에 존재하기 때문에 코드를 찾을 수 없었던 것이다. 이를 `company_info` 테이블로 변경해주기 위해서 `select * from company_info` 명령어를 while문 안에 추가로 넣어줘야 한다.
5. select문을 넣어줬다고 해도 fetchone을 사용하면 __다시 첫번째 줄부터__ 읽게 된다. 테이블을 바꿨기 때문에 다시 초기화가 된 것이다.
6. 결국 내가 원하는 줄 데이터를 뽑기 위해 for문으로 반복해주고, 몇번째 줄을 뽑을지는 `fetchone_repeat`를 입력해서 반복수를 정해줘야 한다. 그러므로 while문 마지막에 `fetchone_repeat += 1`을 입력하여 while문의 루프 횟수를 세주는 명령어를 넣어줘야 한다.
7. 물론 이런식으로 코딩해도 되지만 파일에서 `f.seek(0)` 명령어 하나만으로 첫번째 줄로 이동하는 것에 비해 입력해야 하는 명령어가 많은 편이다. 차라리 2. 이중 for문을 사용하지 않는 것이 경제적이라 할 수 있다.
