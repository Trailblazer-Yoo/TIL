# TIL(Today I Learned)

___

> Jan/27th/2022_Multi campus_유선종 Day16

## 셀레니움
셀레니움은 웹 페이지를 코딩을 통해 자동으로 제어하는 모듈이다. 내가 매일매일 주식창과 분석창 등 하나하나 마우스로 클릭하여 정보를 얻기 귀찮다면 코딩으로 실행 버튼 하나만 누르면 모든 창이 켜지고 정보를 알아서 얻어올 수 있다.
> 내 개인적으로는 귀찮은 것을 정말 싫어하기 때문에 셀레니움을 처음 배웠을 때 갑자기 정신이 맑아지고 집중력이 최대로 올라가는 것을 느꼈다. 셀레니움은 사랑이다.
그러면 오늘은 셀레니움에 대해 공부하고 다음 시간에 실습을 기술하여 상세하게 알아보겠다.

### 1. chromedriver
- 여기서 셀레니움을 하기 위해서는 크롬과 크롬 드라이버가 필요하다. 크롬은 요새 대부분 많이 쓰는 브라우저이기 때문에 문제 없이 설치가 되어있을 것이다.
- 여기에 크롬 드라이버라는 것이 필요한데 구글에 크롬 드라이버라고 검색해서 다운받아주면 된다.

<img src="https://user-images.githubusercontent.com/97590480/151349132-9100a1b8-71ed-4332-96f5-2e263cdfa1c5.png">

> 맨 위의 링크를 들어가서

<img src="https://user-images.githubusercontent.com/97590480/151349420-00912e3d-21d1-47f8-ba82-3de01191ab11.png">

> 크롬 버전에 맞는 크롬 드라이버를 다운 받으면 된다.

크롬 드라이버를 어디 라이브러리에 넣어도 괜찮다. 나는 다운로드 폴더에서 그대로 사용해보겠다.
___

### 2. 네이버 열기
네이버를 알아서 열어주는 기능을 만들어보자.
```python
from selenium import webdriver

url = "http://naver.com"
driver = webdriver.Chrome(r"/Users/yuseonjong/Downloads/Chromedriver")

driver.get(url)
```

- `from selenium import webdriver`을 이용해서 webdriver 클래스를 가져온다.
- 내가 열고 싶은 네이버 주소를 url에 담아준다.
- `webdriver.Chrome(구글드라이버 위치)`를 driver에 넣어준다. 보통 셀레니움을 할 때 driver을 관례상 많이 쓴다. 또한, webdriver.Safari 처럼 사용할 수 있다. 그러나 크롬이 가장 사용하기 좋은 브라우저이기 때문에 웬만하면 크롬을 사용하자.
- 이렇게 driver에 Chromedriver를 r로 읽기 모드로 실행시키는 명령어를 담아주고 `driver.명령어`을 사용하면 구글 드라이버를 매개로 명령어를 크롬에 실행시켜준다. 즉, `driver.get(url)` 명령어를 입력하면 url이 실행된다. 즉, 네이버가 켜진다.
> veryvery nice하다

### 3. 검색창에 검색하기
네이버의 검색창에 '네이버 주식'을 검색하여 들어가보자.

<img src="https://user-images.githubusercontent.com/97590480/151352022-09890ede-ccca-44ab-b088-9212a3a7f6c1.png">

> 여기서도 크롤링의 방법을 이용해야 한다. 오른쪽 개발자 도구를 사용해서 검색창의 태그를 확인하자.
```python
from selenium import webdriver
from selenium.webdriver.common.keys import keys

url  = "http://naver.com"
driver = webdriver.Chrome(r"/Users/yuseonjong/Downloads/Chromedriver")

driver.get(url) ## 네이버창 오픈
element = driver.find_element_by_id("query") ## id = "query" 인 어떤 종류의 태그 찾기
element.send_keys("네이버 주식")
element.send_keys(Keys.ENTER)
```

- `driver.get(url)`로 네이버 창을 연다.
- `driver.find_element_by_id`는 id를 찾는 명령어이다. 보통 id는 고유값을 갖기 때문에 그 요소을 갖는 어떠한 태그를 가져온다. 즉, 위에 사진에서 빨간색 네모 안의 태그를 가져온다.
- `.send_keys("입력할 내용")` 을 이용해서 네이버 주식이라는 텍스트를 넣는다. `<input>` 태그이기 때문에 텍스트를 입력하면 그 텍스트를 입력받는다.
- `send_keys(Keys.ENTER)` 명령어는 우리 키보드의 엔터키를 입력하는 명령어이다. 즉, 어떤 태그이든 엔터가 먹히는 태그는 이 명령어를 사용할 수 있다.

### 4. 네이버 아이디 접속하기
이번에는 네이버 아이디를 접속해보자.

<img src="https://user-images.githubusercontent.com/97590480/151353705-2b9cc0cc-bed6-4ab4-95f5-04fe6058baa9.png">

- 우선 네이버 로그인 창으로 접속하자.
```python
from selenium import webdriver
from selenium.webdriver.common.keys import keys

url  = "http://naver.com"
driver = webdriver.Chrome(r"/Users/yuseonjong/Downloads/Chromedriver")

driver.get(url) ## 네이버창 오픈
driver.find_element_by_class_name("link_login").click() ## class = "link_login" 인 어떤 종류의 태그 찾고 클릭
```
- 검색창에 입력할때는 element 안에 find 명령어를 넣었다. 필요할 때는 어떤 변수에 넣어도 좋지만, 간단하다면 뒤에 `.명령어`를 입력되도 괜찮으니 유용하게 사용하자.
- 또한, 위에서는 `find_element_by_id`를 사용했지만 이번에는 클래스를 찾아야 하므로 `find_element_by_class_name`을 사용했다.

<img src="https://user-images.githubusercontent.com/97590480/151355390-21ec9f75-2a20-4b62-b6d9-092eb96ccacd.png">

```python
driver.find_element_by_id("id").send_keys("본인 ID") ## ID입력
driver.find_element_by_id("pw").send_keys("본인 password") ## 패스워드 입력
driver.find_element_by_id(log.login).click() ## 로그인 클릭
```
- 위에처럼 입력하면 검색창에서 했던 것처럼 send_keys를 이용해서 로그인을 하는 방법이다. 그러나 네이버에서는 로그인이 안되는 것을 볼 수 있는데, 네이버에서 이렇게 로그인하는 것을 보안을 위해 막은 것이다.
- 그렇기 때문에 복사를 해서 입력을 해줘야 한다.

```python
import pyperclip

pyperclip.copy("본인 아이디") ## ID 복사
driver.find_element_by_id("id").send_keys(Keys.COMMAND, 'v') ## 붙여넣기
pyperclip.copy("본인 패스워드")
driver.find_element_by_id("pw").send_keys(Keys.COMMAND, 'v')
element = driver.find_element_by_css_selector("span.blind") ## IP보안 태그 찾기
driver.execute_script("arguments[0].innerText = 'off'", element) ## IP보안 취소
driver.find_element_by_class_name("btn_login").click() # 로그인 클릭
```
- 여기서 pyperclip이라는 모듈이 필요한데, 파이퍼클립은 Ctrl + c 를 하면 생기는 클립보드를 이용하는 모듈이다. 즉, `pyperclip.copy`로 내용을 복사하고, `send_keys(Keys.CTRL + V)`를 이용해서 붙여넣는다. 나는 맥이기 때문에 COMMAND를 입력한다.
- 이렇게 입력하면 정상적으로 로그인이 된다.
- 그리고 최근 IP보안 때문에 바로 로그인이 안되고 이상한 문제를 풀게 되어있다. 나는 이것도 짜증나서 푸는 명령어를 입력했다.
- `driver.find_element_by_css_selector`는 css 속성값을 이용해서 태그를 찾는 명령어이다. 즉, `<span>` 태그를 찾을 때 사용하는데, 여기서는 `<span class = "blind" id="switch_blind>on</span>`이므로 span.속성값을 이용해서 찾는다.
- `driver.execute_script("arguments[0].innerText = 'off'", element)`는 스크립트를 입력할 때 사용한다. 즉, `<span>on`에서 'on'이라는 스크립트를 'off'로 바꿔는 명령어라고 보면 된다.
>arguemnts[0]이 들어가는 이유는 arguments가 *args를 의미한다. 즉, 수많은 요소들 중에서 첫번재를 의미하고, 여기서는 [0]은 element를 지칭한다. 즉, (arguments[], element, element2, element3, ...) 해서 다른 수많은 element를 지칭할 수 있지만, 굳이 그럴 필요는 없기에 여기서는 하나만 넣고 arguments도 [0]을 넣어서 첫번째 것만 지칭한다.
- 이렇게 하면 정상적으로 로그인되는 모습을 볼 수 있다.

### 5. 셀레니움을 이용한 파싱
셀레니움 또한 파싱을 사용할 수 있다. 이전에 사용했던 간단한 파싱을 넣어보자.

```python
### 네이버 웹툰에서 순위에 따른 웹툰 제목 긁어오기
url = "https://comic.naver.com/webtoon/weekday"
driver = webdriver.Chrome(r"/Users/yuseonjong/Downloads/Chromedriver")

driver.get(url)
r1 = driver.find_element_by_id("realTimeRankFavorite") ## 셀레니움을 이용해 html 값 긁어오기
r2 = r1.find_all("a")
list = []
for row in r2:
    list.append(row.text)
print(list)
```
- 위에서처럼 셀레니움을 이용해서 파싱을 할 수 있다. 좋은 점은 귀찮게 parser 선언을 하지 않아도 된다는 점이다.
- 이걸 이용해서 실행 버튼 하나면 셀레니움으로 자동으로 들어가서 데이터를 알아서 수집해준다. 너무나도 편하디 편한 기능이다. 프로젝트를 하게 된다면 셀레니움으로 코드를 만들고 나중에 활용하자.