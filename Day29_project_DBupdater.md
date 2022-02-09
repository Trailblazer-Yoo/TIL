# TIL(Today I Learned)

___

> Fab/9th/2022_Multi campus_유선종 Day29

## 주가 예측을 위한 데이터베이스 생성
지금까지 Day26 ~ Day28 동안 주가 예측을 위한 데이터베이스 생성을 나 혼자의 힘으로 코딩을 해봤다. 오늘부터는 조금 더 세련되게 코딩하는 것을 배워 보도록 하겠다.

### 1. __init__설정
__init__은 생성자 함수로 클래스를 선언할 때 제일 처음으로 실행해주는 함수이다. 내가 했던 __init__은 mysql에 접속하는 함수만 설정했다. 여기서는 스키마와 테이블을 형성하는 함수를 설정한다.

```python
import pandas as pd
from bs4 import BeautifulSoup
import pymysql, calendar, time, json
import requests
from datetime import datetime
from threading import Timer

class DBUpdater:                                                            #line 1
    def __init__(self):                                                     #line 2
        self.conn = pymysql.connect(host='localhost', user='root',          #line 3
            password='1111', db='INVESTAR10', charset='utf8')               #line 4
        
        with self.conn.cursor() as curs:                                    #line 5
            sql = """                                               
            CREATE TABLE IF NOT EXISTS company_info (
                code VARCHAR(20),
                company VARCHAR(40),
                last_update DATE,
                PRIMARY KEY (code))
            """
            curs.execute(sql)                                               #line 6
            sql = """
            CREATE TABLE IF NOT EXISTS daily_price (
                code VARCHAR(20),
                date DATE,
                open BIGINT(20),
                high BIGINT(20),
                low BIGINT(20),
                close BIGINT(20),
                diff BIGINT(20),
                volume BIGINT(20),
                PRIMARY KEY (code, date))
            """
            curs.execute(sql)                                               #line 7
            
        self.conn.commit()                                                  #line 8
        self.codes = dict()                                                 #line 9
```
1. [line 1]에서 `class DBUpdater:`로 클래스를 설정한다.
2. [line 2]에서 `__init__(self)` 함수를 설정한다. 여기서는 생성자 함수에 변수를 설정하지 않았지만, pymysql의 속성값들을 설정해주기 위해 변수를 설정해주는 것이 더 낫다.
3. [line 3,4]에서 `self.conn = pymysql.connect()`를 설정해줌으로써 자동으로 self.conn이 실행되게 만든다. __init__안에서 자동으로 변수가 실행되도록 만들기 위해서는 self를 붙여줘야 한다.
4. [line 5]에서 `with self.conn.cursor() as curs:`는 with 안에서 `self.conn.cursor()`를 curs로 실행해주고 with구문을 빠져나가면 자동으로 `self.conn.cursor()`을 빠져나온다. 즉, 커서에 접근했던 것을 빠져나오는 것이다. 대부분 cursor로 실행이 되지만 다른 명령어를 실행할때 오류가 발생할 수 있으므로 with구문을 같이 사용해주면 깔끔하다.
5. [line 5]에서 종목코드, 회사명, 최근 업데이트된 날짜 필드를 가지는 company_info 테이블을 생성하는 쿼리문을 작성하고 그 쿼리문을 `curs.execute(sql)`을 통해 실행시킨다. [line 7]도 동일하다.
6. [line 8]에서 위에서 실행한 쿼리문을 `self.conn.commit()`으로 도장을 찍어준다.
7. [line 9]는 나중에 필요한 딕셔너리형 틀을 만드는 명령어이다. 이런 식으로 나중에 필요한 리스트나 딕셔너리 저장소를 미리 만들어놓는 것도 하나의 방법이다.
___
### 2. __del__함수
__del__은 소멸자함수로 클래스를 빠져 나올때 자동으로 실행해주는 명령어이다. 예를 들어, `a = DBUpdate()`를 실행시킨 후에 `print('Bye class')`명령어를 실행할 경우 클래스 변수와 관련이 없는 명령어이기 때문에 클래스를 빠져나온 것으로 간주하고 __del__함수를 실행한다.

```python
    def __del__(self):
        self.conn.close()                                                   #line 10
```
- [line 10]을 보면 `self.conn.close()`를 통해 자동적으로 mysql과의 연결을 끊는 명령어를 실행해준다.
___
### 3. krx데이터 크롤링
이제 krx에서 제공하는 데이터를 이용해 종목코드와 회사명을 크롤링하는 클래스를 만들어보자.

```python
def read_krx_code(self):
        url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method='\
            'download&searchType=13'                                        #line 11
        krx = pd.read_html(url, header=0)[0]                                #line 12
        krx = krx[['종목코드', '회사명']]                                       #line 13
        krx = krx.rename(columns={'종목코드': 'code', '회사명': 'company'})     #line 14
        krx.code = krx.code.map('{:06d}'.format)                            #line 15
        
        return krx                                                          #line 16
```

1. [line 11]에서 krx의 주소를 url에 저장한다.
2. [line 12]에서 `pd.read_html(url)`로 데이터를 읽어온다. 이때, 데이터는 리스트 안에 데이터프레임이 들어가있는 형태로 저장되어있다. 즉, 이대로 사용하면 데이터타입은 리스트이므로 데이터프레임 인덱싱을 하는데 문제가 생긴다. 리스트 인덱싱을 이용해서 리스트 안의 데이터프레임을 선택해서 데이터프레임만 저장되도록 `pd.read_html(url)[0]`으로 [0]을 뒤에 붙여주면 데이터프레임만 저장된다.
3. [line 13]에서 종목코드 열과 회사명 열만 뽑아내기 위해 데이터프레임 인덱싱을 해준다. 여기서 꼭 대괄호가 두개가 들어간다는 것을 유념하자.
4. [line 14]에서 한글로 된 인덱스값은 나중에 불편함을 야기하므로 `rename`을 사용해서 종목코드는 code로 회사명은 company로 열 이름을 바꿔주자.
5. [line 15]에서 종목코드가 `123`일 경우 `000123`으로 바꿔준다.
   1. `krx.code`는 krx중 열 이름이 code인 열 데이터 전체를 의미한다.
   2. `'{:06d}'.format`은 문자열을 포매팅하는 명령어이다. 예를 들어, `'{:06d}'.format(123)`일 경우 `000123`이 출력된다.
   3. `'{:06d}'.format()` 중에서 `?:` 물음표 영역(왼쪽 영역)은 format()에서 괄호 안의 인덱싱을 의미한다. 예를 들어, `'{3:06d}'.format(1,2,3,4,5)`을 출력하면 `000004`가 출력된다. 위에서는 아무런 숫자가 없는데, 이는 0이 기본값으로 생략되어있는 것이다.
   4. `'{:06d}'.format()` 중에서 `0`은 남은 공간에 채울 객체를 의미한다. 여기서는 0을 채워주고, =이나 다른 것들을 넣어주면 해당 객체로 채운다.
   5. `'{:06d}'.format()` 중에서 `6`은 공간을 의미한다. 즉, `format()`의 괄호안에 들어가는 변수가 4자리라면, 6자리 중에서 4자리 변수가 들어가고 2자리가 남는다. 이 2자리를 `0`으로 채운다. 괄호안의 변수가 6자리보다 많다면 6자리만 출력해주고 나머지는 출력해주지 않는다.
   6. `'{:06d}'.format()` 중에서 `d`는 입력값의 타입을 설정한다. 즉, 여기서 `d`는 정수이므로 format()괄호 안의 변수가 정수 데이터로 입력된다.
   7. 그리고 기본적으로 오른쪽 정렬이다. 즉, 괄호 안의 데이터가 오른쪽에 들어가고 나머지 공간은 왼쪽부터 채워준다. `'{:0>6d}'.format()`와 `'{:06d}'.format()`가 동일한 표현이다.
6. [line 16]에서 결과값으로 krx를 받는다. 즉, krx는 회사명과 6자리의 종목코드를 데이터프레임으로 저장한 변수이다.
___
### 4. 종목코드를 company_info 테이블에 저장 후 딕셔너리 형태로 저장
여기서 만들 함수는 위에서 krx 결과값을 가져와서 company_info에 저장하고 딕셔너리 형태로 저장하는 작업을 한다. 또한, 최근에 업데이트 됐는지 확인해서 그렇지 않다면 최신화를 해주는 작업까지 해줄 것이다.

```python
def update_comp_info(self):
        sql = "SELECT * FROM company_info"                                  #line 17
        df = pd.read_sql(sql, self.conn)                                    #line 18
        for idx in range(len(df)):                                          #line 19
            self.codes[df['code'].values[idx]] = df['company'].values[idx]  #line 20
        
        with self.conn.cursor() as curs:                                    #line 21
            sql = "SELECT max(last_update) FROM company_info"               #line 22
            curs.execute(sql)                                               #line 23
            rs = curs.fetchone()                                            #line 24
            today = datetime.today().strftime('%Y-%m-%d')                   #line 25
```
1. [line 17]에서 company_info 테이블을 불러온다. 현재는 데이터를 입력하지 않았으므로 아무런 데이터도 나오지 않는다.
2. [line 18]에서 `pd.read_sql`함수를 사용한다. sql문을 읽어서 데이터프레임 형태로 저장하는 함수이다.
> pd.read_sql 함수는 매우 많은 데이터가 존재할경우 누락하는 경우가 발생하므로 권장하지 않는 함수이다.
3. [line 19]에서 `range(len(df))`를 이용해서 데이터프레임의 행의 갯수를 가져와 범위를 설정해준다.
4. [line 20]에서 `df['code'].values[idx]`는 code 열에서 해당 인덱스의 값을 가져온다. 여기서 __init__에서 설정해줬던 `self.codes`를 이용해 코드값을 키값으로, 회사명을 밸류값으로 갖는 딕셔너리형 데이터를 생성한다.
5. [line 21]에서 with문을 이용해서 커서를 불러온다.
6. [line 22]에서 company_info 테이블에서 가장 최근의 날짜만 불러오는 쿼리문을 입력하고 [line 23]에서 해당 쿼리문을 실행한다.
7. [line 24]에서 [line 22]에서 불러온 최근 날짜를 읽는 `curs.fetchone()`을 실행하고, 실행하면 첫번째 행의 값을 가져오는데, 여기서 행에는 최근 날짜 열만 존재하므로 최근 날짜 데이터를 rs에 담는다.
8. [line 25]에서 오늘의 날짜를 불러오는 `datetime.today()`함수를 실행한다. 그 뒤에 `.strftime('%Y-%m-%d')`는 string from time의 약자로 괄호 안의 형식대로 날짜와 시간을 표시해주는 함수이다.
___
```python
            if rs[0] == None or rs[0].strftime('%Y-%m-%d') < today:         #line 26        
                krx = self.read_krx_code()                                  #line 27
                for idx in range(len(krx)):                                 #line 28
                    code = krx.code.values[idx]                             #line 29
                    company = krx.company.values[idx]                       #line 30
                    
                    sql = f"REPLACE INTO company_info (code, company, last"\
                        f"_update) VALUES ('{code}', '{company}', '{today}')"                                                   
                    curs.execute(sql)                                       #line 31
                    self.codes[code] = company                              #line 32
                    
                    # logs
                    tmnow = datetime.now().strftime('%Y-%m-%d %H:%M')       #line 33
                    print(f"[{tmnow}] #{idx+1:04d} REPLACE INTO company_info "\
                        f"VALUES ({code}, {company}, {today})")             #line 34
                
                self.conn.commit()
```
9. [line 26]에서 `if rs[0] == None or rs[0].strftime('%Y-%m-%d') < today:`을 해석하자면 company_info에 저장되어 있는 최신 날짜가 없거나 오늘보다 이전의 날짜라면 실행해준다는 의미이다. 현재는 최근 날짜 데이터가 없으므로 `rs[0] == None`이므로 아래의 코드를 실행한다.
10. [line 27]에서 위에서 실행한 함수인 `read_krx_code()`를 `self.`를 통해 실행한다. 위에서 `self.read_krx_code()`의 결과값은 krx였으므로 그 결과값을 krx에 넣어준다.
11. [line 28]에서 krx의 행의 갯수만큼 범위로 설정한다.
12. [line 29,30]에서 데이터프레임에 저장되어 있는 코드와 회사명 데이터를 하나하나 가져온다.
13. [line 31]에서 하나하나 가져온 데이터를 `replace into` 쿼리문을 이용해서 이전 데이터를 삭제하고 입력해준다.
14. [line 32]에서 [line 20]에서 했던 것처럼 코드를 키값으로, 회사명을 밸류값으로 갖는 딕셔너리형 데이터를 만들어준다.
15. [line 33]에서 현재 시간을 가져오는 `datetime.now()`를 이용해서 지금 데이터가 잘 들어가고 있는지 시간을 출력해주는 로그를 만들어준다.
16. [line 34]에서 로그를 출력해준다. 예를 들어 2315번째 데이터가 잘 들어갔다면 `[2022-02-09 21:44] #2315 REPLACE INTO company_info VALUES (093520, 매커스, 2022-02-09)`처럼 출력해준다.
___
### 5. 네이버 데이터 크롤링
이번 함수는 네이버에서 데이터를 크롤링하는 함수이다. 그리고 크롤링한 데이터를 다시 데이터프레임 형태로 만들어준다.
```python
def read_naver(self, code, company, pages_to_fetch):                        #line 35
        try:                                                                #line 36
            df = pd.DataFrame()                                             #line 37
            
            url = f"http://finance.naver.com/item/sise_day.nhn?code={code}" #line 38
            html = BeautifulSoup(requests.get(url,
                headers={'User-agent': 'Mozilla/5.0'}).text, "lxml")        #line 39
            
            pgrr = html.find("td", class_="pgRR")                           #line 40
            if pgrr is None:
                return None
            
            s = str(pgrr["href"]).split('=')                                #line 41
            lastpage = s[-1]                                                #line 42
            pages = min(int(lastpage), pages_to_fetch)                      #line 43
            
            for page in range(1, pages + 1):            
                pg_url = '{}&page={}'.format(url, page)                     #line 44               
                df = df.append(pd.read_html(requests.get(pg_url,
                    headers={'User-agent': 'Mozilla/5.0'}).text)[0])        #line 45
```
1. [line 35]에서 변수로 code 이름, 회사이름, 내가 원하는 페이지수를 받는다.
2. [line 36]에서 try를 이용해서 오류가 발생했을 경우 해당 오류가 출력되도록 만들어준다.
3. [line 37]에서 데이터프레임 형태의 틀을 만들어준다.
4. [line 38]에서 네이버 주식의 시세창 주소를 url에 넣는다. 특히, 원하는 코드가 있을 경우 위의 code변수를 통해 해당 코드의 시세창을 가져온다.
5. [line 39]에서 BeautifulSoup으로 requests.get으로 얻은 html을 파싱하는데, 이전에는 'parser' 형식을 썼다면 여기서는 'lxml'형식을 사용했다. 또한 네이버에서 주소 접근을 거부하는 것을 막기 위해 headers를 설정해준다.
6. [line 40]에서 페이지를 클릭하는 클래스에서 "맨뒤"를 클릭하는 창이 있는데, 이 태그가 없을 경우 마지막 페이지라는 것을 의미하므로 `return None`을 이용해서 try 안에서의 값을 None값을 갖도록 해준다.
7. [line 41]에서 "맨뒤"에 가장 마지막 페이지로 들어가는 하이퍼링크가 있는데, 그 중 마지막 페이지만 파싱하는 명령어이다. page='마지막페이지'형식으로 되어있으므로 `split('=')`으로 =를 제거하면 순수한 마지막 페이지 데이터가 리스트에 담긴다.
8. [line 42]에서 리스트에 담긴 마지막 페이지를 인덱싱한다. 가장 마지막에 있으므로 [-1]을 입력한다.
9. [line 43]에서 함수 변수로 입력한 `pages_to_fetch`와 위에서 파싱한 마지막 페이지 중 작은 값을 pages안에 넣는다. 즉, 내가 원하는 페이지가 마지막 페이지를 넘겼을 경우 내가 원하지 않은 데이터가 담기는 것을 막기 위해 보정해주는 작업이다. 혹은 내가 원하는 페이지가 마지막 페이지보다 작을 경우 내가 원하는 페이지를 pages로 설정해주는 작업이다.
10. [line 44]에서 위에서 찾은 페이지수 만큼 range로 범위를 설정해주고 각 페이지에 맞는 주소를 받아 파싱한다.
11. [line 45]에서 크롤링한 html을 텍스트 데이터만 가져오고 그 중 [line 12]처럼 리스트 안의 데이터프레임만 뽑아낸다.

```python
                
                tmnow = datetime.now().strftime('%Y-%m-%d %H:%M')           #line 46
                print('[{}] {} ({}) : {:04d}/{:04d} pages are downloading...'.
                    format(tmnow, company, code, page, pages), end="\r")
                
            df = df.rename(columns={'날짜':'date','종가':'close','전일비':'diff'
                ,'시가':'open','고가':'high','저가':'low','거래량':'volume'})    #line 47
            df['date'] = df['date'].replace('.', '-')                       #line 48
            df = df.dropna()                                                #line 49
            df[['close', 'diff', 'open', 'high', 'low', 'volume']] = df[['close',
                'diff', 'open', 'high', 'low', 'volume']].astype(int)       #line 50
            df = df[['date', 'open', 'high', 'low',
             'close', 'diff', 'volume']]                                    #line 51
            
        except Exception as e:
            print('Exception occured :', str(e))
            return None
        
        print(df)
        return df
```

12. [line 46]에서 [line 34]처럼 현재 진행상황을 알려주는 로그를 출력해준다.
13. [line 47]에서 필드 이름을 영어로 바꿔준다.
14. [line 48]에서 날짜를 '2022-02-08'형태로 바꿔준다.
15. [line 49]에서 `df.dropna()`은 Null 데이터를 삭제해주는 명령어이다.
16. [line 50]에서 .astype(int)는 리스트 안의 데이터를 정수로 바꿔주는 명령어이다. 이걸 까먹어서 나처럼 for문으로 하나하나 정수로 바꿔주고 다시 리스트에 넣는 귀찮은 짓을 하지 말자. 꼭 기억하자.
17. [line 51]에서 필드의 위치를 바꿔주는 명령어를 실행한다.