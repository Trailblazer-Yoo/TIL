# TIL(Today I Learned)

___

> Fab/10th/2022_Multi campus_유선종 Day30

## 주가 예측을 위한 데이터베이스 생성 2
어제에 이어서 네이버의 주가를 DB에 저장하는 알고리즘을 알아 보고자 한다. 특히 코드나 페이지를 설정하는 옵션을 설정하는  등의 부가적인 기능들에 초점을 두겠다.

### 1. DB에 네이버 주식 데이터를 입력
Day29에서 마지막 내용은 네이버에서 주식 데이터를 크롤링해 리턴값으로 주식 데이터가 담긴 데이터프레임을 받는 내용이었다. 그 다음은 리턴값을 DB에 입력하는 함수를 알아 보고자 한다.

```python
    def replace_into_db(self, df, num, code, company):                                          #line 1
        with self.conn.cursor() as curs:                                                        #line 2
            for r in df.itertuples():                                                          #line 3
                sql = f"REPLACE INTO daily_price VALUES ('{code}', "\
                    f"'{r.date}', {r.open}, {r.high}, {r.low}, {r.close}, "\
                    f"{r.diff}, {r.volume})"
                curs.execute(sql)                                                               #line 4
            self.conn.commit()
            
            print('[{}] #{:04d} {} ({}) : {} rows > REPLACE INTO daily_'\
                'price [OK]'.format(datetime.now().strftime('%Y-%m-%d %H:%M'),
                                    num+1, company, code, len(df)))                             #line 5
```

1. [line 1]에서 함수의 요소로 df, num, code, company를 입력받는다. 해당 변수들은 나중에 다른 함수를 이용해서 입력받으므로 그 의미만 확인하고 넘어가자. df는 주식 데이터가 담긴 데이터프레임, num은 숫자, code는 종목코드, company는 회사명이다.
2. [line 2]에서 with문으로 커서를 불러온다.
3. [line 3]에서 `df.itertuples()`라는 명령어를 꼭 암기하자. 이 명령어는 iterate tuples의 약자로 데이터프레임의 행을 하나하나 읽어줄 때 사용한다. 즉, for문으로 `df.intertuples()`를 범위로 설정해주면 r에 각 행의 모든 데이터를 가져온다.
4. [line 4]에서 각 열에 맞는 데이터들을 daily_price 테이블에 넣기 위해 `REPLACE INTO`문을 작성하여 실행시킨다.
5. [line 5]에서 현재 시간과 회사명, 코드, 데이터 길이를 표시하는 로그를 생성해서 데이터가 잘 들어가고 있는지 확인할 수 있도록 출력해주는 명령어를 입력한다.
___
### 2. 네이버의 주식 시세를 다운받아 DB에 업데이트
1.에서 DB에 네이버 주식 데이터를 입력하는 함수를 생성했다. 여기서는 실제로 네이버에서 시세를 다운받는 함수를 만들고 `self.replace_inot_DB` 함수를 마지막에 입력하여 DB에 업데이트되도록 하는 코드를 알아보고자 한다.
```python
def update_daily_price(self, pages_to_fetch):                                                   #line 6
        
        for idx, code in enumerate(self.codes):                                                 #line 7
            
            if code != '005930':                                                                #line 8
                continue                                                                        #line 9
            
            df = self.read_naver(code, self.codes[code], pages_to_fetch)                        #line 10
            
            if df is None:                                                                      #line 11
                continue
            
            self.replace_into_db(df, idx, code, self.codes[code])                               #line 12
```

1. [line 6]에서 `pages_to_fetch` 변수를 설정하여 내가 원하는 페이지 수 만큼 크롤링하는 코드를 실행한다. 페이지수는 뒤에 페이지를 설정하는 함수를 통해 설정해준다.
2. [line 7]에서 `self.codes`에 이미 담겨있는 딕셔너리형 데이터를 가져와서 `enumerate`함수를 이용해 인덱스값과 키값을 idx, code로 받아서 가져온다. 여기서 for문을 돌릴때, 딕셔너리형은 키값만 가져온다. 밸류값을 가져오고 싶다면 `self.codes[key값]`으로 입력해줘야 한다.
3. [line 8]에서 내가 원하는 종목코드의 데이터만 뽑고 싶다면 설정해준다. 여기서 `005930`은 삼성전자의 종목코드이므로 삼성전자의 데이터만 크롤링해준다. 만약 종목을 설정하고 싶지 않으면 명령어를 없애주면 된다.
4. [line 9]에서 continue를 이용해서 for문의 처음으로 다시 돌아가서 실행해주는 명령어를 입력한다. break와 continue는 명령어를 중지시켜주는 것에서 공통점이 있지만, break는 실행하고 있는 반복문을 break이후로 전부 종료시켜준다. 즉, 다시 처음으로 되돌아가지 않는다. 반면에, continue는 빠져나오는 조건에 해당되는 것을 만났을 때 continue 아래의 코드의 실행을 중단하고 다시 for문의 처음으로 돌아가서 for문을 실행한다.
5. [line 10]에서 `self.read_naver()`함수를 실행시켜줌으로써 네이버에서 크롤링을 해온다.
6. [line 11]에서 df에 데이터가 없다면 시행을 중시킴으로써 DB에 없는 데이터가 들어가지 않도록 막아주는 역할을 한다.
7. [line 12]에서 df에 담은 데이터를 `self.replace_into_db()`함수를 이용해 DB에 저장해준다.
___
### 3. 최신 데이터를 자동으로 업데이트 해주는 함수
DB에 한번 저장하면 그 이후에 새로 데이터를 다운받지 않는다면 계속 동일한 데이터를 가지고 있을 것이다. 그러나 주식 데이터는 주중에 매일 갱신되므로 알아서 매일매일 데이터를 가져오는 함수를 설정해준다.

```python
def execute_daily(self):
        self.update_comp_info()                                                                 #line 13
        
        try:                                                                                    #line 14
            with open('config.jason', 'r') as in_file:                                          #line 15
                config = json.load(in_file)                                                     #line 16
                pages_to_fetch = config['pages_to_fetch']                                       #line 17
        except FileNotFoundError:
            with open('config.json', 'w') as out_file:                                          #line 18
                pages_to_fetch = 5
                config = {'pages_to_fetch': pages_to_fetch}
                json.dump(config, out_file)                                                     #line 19

        self.update_daily_price(pages_to_fetch)                                                 #line 20
```

1. [line 13]에서 KRX에서 제공하는 최신의 종목코드와 회사명을 가져온다.
2. [line 14]에서 try구문을 이용해서 오류가 날때 다른 명령어를 실행해준다. if구문을 사용해도 괜찮다.
3. [line 15]에서 with구문을 이용해서 제이슨 파일을 연다. 제이슨 파일은 데이터를 딕셔너리 형태로 저장해주는 txt파일이라고 생각하면 된다.
4. [line 16]에서 제이슨 페일을 열고 안의 데이터를 `json.load`를 이용해서 가져온다. 안에 있는 데이터는 `{"pages_to_fetch" : 100}`처럼 pages_to_fetch를 키값으로 갖고 밸류값으로 페이지수를 가진다.
5. [line 17]에서 불러온 데이터의 밸류값을 pages_to_fetch에 담아준다.
6. [line 18]에서 만약에 파일이 없다는 오류가 발생하면 제이슨 파일을 하나 생성한다.
7. [line 19]에서 생성한 파일에 페이지수가 5인 딕셔너리 데이터를 `json.dump`명령어를 이용해서 덮어쓴다. 여기서 기본값으로 5를 설정해줬을 뿐이고 숫자는 의도에 따라 바꿀수 있다.
8. [line 20]에서 제이슨 파일에서 가져온 페이지 수를 `self.update_daily_price()`명령어의 변수로 입력해주고 실행한다. 비로소 최신의 데이터를 포함한 모든 주식 데이터를 DB에 입력해준다.
___
이제 알아서 17시에 데이터를 업데이트 해주는 예약 명령어를 입력해주자.
```python
        tmnow = datetime.now()                                                                  #line 21
        lastday = calendar.monthrange(tmnow.year, tmnow.month)[1]                               #line 22
        
        if tmnow.month == 12 and tmnow.day == lastday:                                          #line 23
            tmnext = tmnow.replace(year=tmnow.year+1, month = 1, day = 1, hour = 17, minute = 0, second = 0)
        elif tmnow.day == lastday:                                                              #line 24
            tmnext = tmnow.replace(month=tmnow.month+1, day = 1, hour = 17, minute = 0, second = 0)
        else:                                                                                   #line 25
            tmnext = tmnow.replace(day = tmnow.day+1, hour = 17, minute = 0, second = 0)
            
        tmdiff = tmnext - tmnow                                                                 #line 26
        secs = tmdiff.seconds                                                                   #line 27
        t = Timer(secs, self.execute_daily)                                                     #line 28
        print("Waiting for next update ({}) ...".format(tmnext.strftime('%Y-%m-%d %H:%M')))     #line 29
        t.start()                                                                               #line 30
```

1. [line 21]에서 datetime 라이브러리를 이용해서 `datetime.now()`를 입력하여 현재 날짜를 가져온다.
2. [line 22]에서 현재 날짜의 연과 월을 `calendar.monthrange()`에 입력해준다. 이 명령어는 요일의 숫자값과 해당 월의 일수를 가져온다. 만약, 오늘이 2월 10일 목요일이라면 `(3,28)`을 결과값으로 받는다. 요일은 차례대로 `0:월, 1:화, 2:수, 3:목, 4:금, 5:토, 6:일` 이다.
3. [line 23]에서 만약 12월 31일이라면, 해가 바뀌기 때문에 연도와 월, 일을 바꿔준다.
4. [line 24]에서 만약, 월의 마지막 일 예를 들어 2월 28일 이라면 월이 바뀌기 때문에 월과 일을 바꿔준다.
5. [line 25]에서 위에 해당하지 않는 일반적인 날에는 그 다음날을 표시하기 위해 현재 일에 +1을 해준다.
6. [line 26]에서 위에서 구한 그 다음날과 오늘 날짜의 차이를 tmdiff에 넣어준다.
7. [line 27]에서 그 차이의 단위를 초로 바꿔준다. 날짜를 계산해줄때에는 초 단위로 바꿔줘야 한다.
8. [line 28]에서 `Timer(초단위의 숫자, 실행할 명령어)`를 입력하여 입력한 숫자만큼의 초가 지나면 해당 명령어를 실행시켜준다. 즉, 명령어를 실행한 순간 내가 설정한 시간에 명령어를 실행해준다.
9. [line 29]에서 다음날에 언제 업데이트를 해주는지 표시해주기 위해 다음날 업데이트해주는 시간을 출력해준다.
10. [line 30]에서t `t.start()`를 사용하여 타이머를 실행시켜준다. 실행시켜주면 터미널에 커서가 켜져있는 상태로 가만히 있는 것을 볼 수 있는데, 이는 그 다음날 해당 날짜가 되기 전까지 타이머가 실행되어 있는 것이다. 해당 시간이 되면 타이머가 끝나면서 업데이트해주는 명령어가 실행되어 데이터가 업데이트되고 다시 타이머를 설정한다.
___
### 4. 실행되는 순서
위의 클래스는 다양한 함수가 서로 얽혀있는데, 함수가 실행되는 순서를 집합을 이용하여 같이 표시해주면 편하다.

<img src = "https://user-images.githubusercontent.com/97590480/153405406-ddc4db7f-3260-492b-b02e-e886418cf8fd.png">

- 위의 필기를 보면 `execute_daily()`를 실행하여 안의 `update_comp_info()`와 `update_daily_price()`를 실행한다. 또한, `update_comp_info()`안에 `read_krx_code()`, `update_daily_price()`안에 `read_naver()`와 `replace_into_db()`를 실행해줌으로써 `execute_daily()`명령어를 실행시키면 총 5개의 함수가 실행된다.
- `execute_daily()`는 타이머에 의해 설정해둔 시간에 자동으로 실행되므로 5개의 함수 또한 자동으로 최신 데이터로 업데이트된다.
- 즉, 클래스 선언과 `execute_daily()`만 실행해주면 자동으로 알아서 모든 함수를 실행시켜 주식 데이터를 가져온다.