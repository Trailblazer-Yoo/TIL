# TIL(Today I Learned)

___

> Jan/25th/2022_Multi campus_유선종 Day14

## 데이터 크롤링
지난 시간에는 html에 대해 공부했다. 이번에는 웹사이트에서 파이썬으로 정보를 가져오는 크롤링과 스크래핑에 대해 알아보자.
- 크롤링(crawling)은 웹 페이지의 하이퍼링크를 순회하면서 웹 페이지를 다운로드 하는 작업이다. 쉽게 생각하면 웹 페이지를 몽땅 가져온다고 생각하면 된다.
- 스크래핑(scraping)은 다운로드한 웹페이지에서 필요한 정보를 추출하는 작업이다. 예를 들어 네이버 주식창에서 주식 가격에 대한 정보만 추출한다면 이것을 스크래핑이라고 한다.
> 둘을 구별하는 것이 큰 의미는 없다. 결국에는 둘다 정보를 가져온다는 느낌만 가져가자.
- 파싱(parsing)은 웹페이지의 정보를 가져와서 정보를 가공하는 것이다. 
___
### 1. 크롤링에 대한 사전 지식 및 주의사항
- 우리가 보는 네이버창은 네이버 서버에서 보내온 정보를 내 컴퓨터에 받아온 결과물이다. 서버에서 받은 정보는 계속 연결시키면 과부하가 걸리기 때문에 한 번 받으면 연결을 끊고 필요할때 다시 연결한다.
  - 그러므로 우리는 웹브라우저에서 정보를 추출할때 정태적인 정보를 가져온다. 반면에, 5초마다 갱신되는 주식 가격은 그때그때 정보를 추출할려고 하면 정보가 바뀔 것이다. 정보 특성에 따라 다르지만 대부분 정태적인 정보이다.
- 우리는 웹 브라우저에 접근을 요청하는데, 이것을 request라고 한다. 웹 브라우저는 접근을 받아 요청사항에 따른 정보를 제공한다. 이를 Response라고 한다. Response받은 정보를 우리는 Source라고 하고 이것을 정제해서 데이터화 하여 저장하는 곳이 Database이다.
  - 즉, 지금의 작업은 우리가 정보를 분석하기 이전에 정보를 수집해서 원하는 분석을 위해 데이터를 정제하는 작업 중의 하나라고 생각하면 된다. 그중 크롤링과 스크래핑은 수집에 중점을 둔 작업이다.
- 데이터를 수집할 때 유의할 것은 저작권이나 JavaScript인지 등이다. 웹 브라우저에서 사용자가 접근하는 것을 막아놓은 것들이 있는데 naver.com/robots.txt를 통해 확인할 수 있다. 막아놓은 디렉토리에 억지로 접근하여 데이터를 수집하면 당연히 처벌받는다. 자바는 크롤링이 되지 않는 경우가 있으니 구별해야 한다.
___
### 2. requests(크롤링)
데이터 수집 단계를 다시 한 번 상기시켜보자. **Rquest(접근) - Response(반응) - Source(소스) - Database(데이터베이스)** 순이다. 그 중 Request와 Response를 수행하는 모듈이 requests이다.

```python
import requests
res = requests.get("http://naver.com")

print(res.status_code) # 정상일 경우 값 = 200
```
> 사용법은 간단하다.
- `requests.get("http://naver.com")` 명령어를 입력하면 네이버 창에 있는 모든 html 정보들을 담는다.
- `res.status_code` 명령어는 현재 내가 정보들을 정상적으로 크롤링했는지 판단해주는 명령어이다. 값이 200이 나와야 정상이고 나머지 값들이 나오면 오류가 발생한 것이다.
- `res.status_code` 대신에 `res.raise_for_status()`를 입력할 경우 정상적이라면 그냥 지나가고, 정상적이지 않으면 그 순간 break된다. 크롤링할 경우 위의 명령어를 꼭 같이 써주자.
___
### 3. BeautifulSoup(파싱)
데이터 수집 단계에서 크롤링을 통해 Source(소스)를 생성했다면 이를 데이터베이스에 저장하기 위해 소스를 가공하는 작업을 파싱이라 한다. 즉 우리가 받은 웹페이지에서 원하는 내용만 추출하는 작업이다.
- 이 작업을 수행하기 위해서 우리는 BeautifulSoup라는 모듈을 사용하게 된다. 예시를 통해 사용법을 익혀보자.
___
#### 1. text

```python
import bs4
html_str = """
<html>
    <body>
        <ul>
            <li>hello</li>
            <li><bye></li>
            <li>welcome</li>
        </ul>
    </body>
<html>
"""
bs_source = bs4.BeautifulSoup(html_str, "html.parser")
ul = bs_source.find("ul")
print(ul)
```

- 위에서 html_str은 html을 구조화해서 시각적으로 보기 좋게 만들어놓은 자료이다. 실제로 크롤링을 해서 html 자료를 가져오면 저렇게 깔끔하게 구성되어 있지는 않다.
  - 하지만 bs를 이용해 파싱하는 법은 동일하기 때문에 내가 필요한 정보를 웹페이지에서 f12를 누르고 개발자도구를 통해 html_str처럼 구조화된 html을 보면서 동시에 코딩을 해야 한다.
- 우선 `bs_source = bs4.BeautifulSoup(html_str,"html.parser")`을 선언해야 한다. 이 명령어는 html.parser을 선언함으로써 소스 데이터를 구분해주는 역할을 한다.
> 쉽게 생각해서 텍스트 형식으로 html_str처럼 써준다고 생각하면 된다. html_str은 문자 형태로 써져있기 때문에 그대로 사용해도 문제가 없지만 이해를 돕기 위해 파싱을 선언했다.
- 그다음 `bs_source.find("ul")` 명령어를 사용하면 `<ul>`에 있는 모든 정보를 추출한다. find는 괄호 안에 있는 문자열의 첫번째 태그 데이터를 찾아서 가져온다. 즉, 이 명령어를 실행하면 다음과 같이 추출된다.
```python
<ul>
<li>hello</li>
<li>bye</li>
<li>welcome</li>
</ul>
```

- 여기서 bye만 추출하고 싶다고 생각해보자. 그렇다면 `ul.find("li")`를 해야 된다고 생각할 것이다.

```python
bs_source = bs4.BeautifulSoup(html_str, "html.parser")
ul = bs_source.find("ul")
li = ul.find("li")
print(li)
```
- 이 명령어를 실행하면 다음과 같이 나온다.
  
```python
<li>hello</li>
```

- bye를 추출하고 싶었는데 hello가 나왔다. 거기다가 양 옆에 `<li>`가 붙어있다. 즉, find 명령어는 찾으려는 문자열이 있는 __가장 첫번째__ 데이터를 추출한다.
- 거기다 양 옆에 태그를 제거해줘야 한다. 이를 위해서는 다음과 같이 명령어를 입력해야 한다.

```python
bs_source = bs4.BeautifulSoup(html_str, "html.parser")
ul = bs_source.find("ul")
li = ul.findAll("li")
print(li[1].text)
```

- `findAll` 명령어는 괄호 안에 있는 문자열을 포함한 태그를 모두 리스트 형태 자료로 가져온다. 즉, 이 명령어를 실행했을 경우 데이터는 다음과 같이 들어가 있다.

```python
li = [<li>hello</li>, <li>bye</li>, <li>welcome</li>]
```

- 즉, 리스트 형태로 들어간 자료 중에 우리는 bye를 추출하고 싶기 때문에 `li[1]`을 입력해서 슬라이싱을 한다.
- 두번째로 bye만 추출하고 싶기 때문에 `<li></li>`를 제거하는 명령이 필요하다. 그것이 바로 `.text` 명령어이다. 결국 저 명령어를 실행하면 우리가 원하는 bye를 추출할 수 있다.
___
#### 2. 속성
- 앞에서는 텍스트를 얻는 작업을 했다. 그런데 만약 수많은 `<ul>`가 있다면, 또한 수많은 `<li>`가 있다면 우리는 어떻게 bye만을 추출할 수 있을까? 이중, 삼중, 사중 리스트를 하기에는 무리가 있다.
- 이럴 경우 속성값을 이용해 데이터를 더 구체적으로 지칭하여 찾을 수 있다. 다음의 예시를 보자.

```python
import bs4

html_str = """
<html>
    <body>
        <ul>
            <li>hello</li>
            <li>bye</li>
            <li>welcome</li>
        <ul>
        <ul class = "reply">
            <li>ok</li>
            <li>no</li>
            <li>sure</li>
    </body>
</html>
"""
bs_source = bs4.BeautifulSoup(html_str, "html.parser")
ul = bs_source.find("ul", {"class" : "reply"})
print(ul.text)
```

- 여기서 우리는 `ul = bs_source.find("ul", {"class" : "reply"})`가 다르다는 것을 알 수 있다.
- 속성과 속성값은 딕셔너리 형태로 저장이 되어있다. 즉, ul 중에서 속성값이 reply인 것을 찾기 위해서는 위와 같이 입력해주면 된다.
- 이렇게 명령어를 입력할 경우 추출되는 자료는 다음과 같다.

```python
<ul class="reply">
<li>ok</li>
<li>no</li>
<li>sure</li>
</ul>
```
___
#### 3. 하이퍼링크
- 위에서 속성값을 이용해서 인덱싱을 하는 것을 알아봤다. 그렇다면 속성값을 추출하고 싶다면 어떻게 해야 할까? 아래 예시를 보자.

```python
import bs4

html_str = """
<html>
    <body>
        <ul class = "ko">
            <li>
                <a href = "http://www.naver.com/">네이버</a>
            </li>
            <li>
                <a href = "http://www.daum.net/">다음</a>
            </li>
        </ul>
        <ul class = "sns">
            <li>
                <a href = "http://www.google.com/">구글</a>
            </li>
            <li>
                <a href = "http://www.facebook.com/">페이스북</a>
            </li>
        </ul>
    </body>
</html>
"""
bs_source = bs4.BeautifulSoup(html_str, "html.parser")
atag = bs_source.find("a", {"href" : "http://www.google.com/"})
print(atag['href'])
```

- 여기서 `bs_source.find("a", {"href" : "http://www.google.com/"})` 코드는 수많은 `<a>` 태그 중에서 하이퍼링크 속성값으로 구글 주소값을 갖는 앵커 태그를 가져온다는 뜻이다.
- 만약, `print(atag.text)`를 입력하면 `구글`이 나오게 된다. 반면에, `print(atag['href'])`를 입력하게 되면 {속성:속성값}의 딕셔너리 형태로 저장되어 있는 속성들 중에서 key값으로 'href'를 갖는 속성값인 `"http://www,facebook.com"`이 나오게 된다.   
기본적인 크롤링과 파싱 방법을 배웠다. 다음엔 실제로 웹 브라우저에서 데이터를 가져와 추출하는 것을 응용해보는 시간을 가져보자.