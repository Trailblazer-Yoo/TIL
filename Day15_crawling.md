# TIL(Today I Learned)

___

> Jan/26th/2022_Multi campus_유선종 Day15

## 크롤링 실습
지난 시간에는 크롤링과 파싱에 대해 공부했다. 이제 실제로 네이버 웹툰 페이지에서 소스를 받아 원하는 데이터로 가공해보자.

### 1. requests
우선 requests를 이용해서 크롤링을 실시하고 제대로 크롤링이 되었는지 확인해야 한다. 

```python
import requests

url = "https://comic.naver.com/webtoon/weekday"
res = requests.get(url)
res.raise_for_status()
```

- 네이버 웹 주소를 url에 담고 `requests.get` 명령어를 사용해서 주소를 크롤링 해온다.
- `raise_for_status()` 명령어를 입력하고 실행했을 경우 아무런 문제 없이 지나갈 경우 오류가 발생하지 않고 정상적으로 크롤링이 되었다는 것을 의미한다. 
___
### 2. 파싱
BeautifulSoup를 이용해서 파싱을 하자.

```python
import requests
from bs4 import BeautifulSoup

url = "https://comic.naver.com/webtoon/weekday"
res = requests.get(url)
res.raise_for_status()

Soup = BeautifulSoup(res.text,"html.parser")
```
- Soup에 크롤링한 데이터를 텍스트화해서 각 태그마다 나눠준 파싱한 데이터를 담아준다.
- 이제 모든 준비가 다 끝났다. 원하는 데이터를 뽑아보자.
___
#### 1. 순위 데이터
먼저 웹툰 페이지에 오른쪽에 있는 오늘의 순위 데이터를 뽑아온다고 가정해보자.

<img src="https://user-images.githubusercontent.com/97590480/151163534-a9df6af6-ab56-4d84-9758-ba2bcbfceff1.png">

> 여기서 빨간색 네모칸에 있는 순위의 만화 제목을 데이터로 뽑아내고 싶다.

<img src="https://user-images.githubusercontent.com/97590480/151163727-eff53b59-8678-49f7-a570-30ac00d88429.png">

- 오른쪽에 검은색 창은 __개발자 도구__ 이다. f12 혹은 fn + f12 키를 누르면 창이 뜬다. 저기서 빨간색 원 안에 있는 하늘색으로 칠해진 버튼을 누르면 마우스 모양이 손가락 모양으로 바뀐다.
- 손가락 모양을 웹 페이지 위에 올려놓으면 이상한 영역이 지정되면서 오른쪽 개발자 도구가 바쁘게 움직이는 것을 볼 수 있다. 이것의 기능은 웹 페이지 상의 html 주소를 찾아주는 기능을 한다.
- 즉, 우리가 원하는 순위의 데이터의 html 값을 찾아내기 위해서는 개발자 도구를 열어서 손가락 모양의 마우스로 내가 알고 싶어하는 컨텐츠 위에 마우스를 올려놓으면 html 값을 찾아준다. 매우 편한 기능이다.

<img src="https://user-images.githubusercontent.com/97590480/151164921-0b26c1ce-9239-4541-913e-25f4e0ba1c51.png">

- 여기서 빨간색 줄은 오른쪽 개발자 도구의 빨간색 줄과 동일하다. `<a>`태그 안에 있으며, 하이퍼링크가 이어져 있어 클릭하면 해당 웹툰으로 이동할 것이다. 그리고 텍스트에는 웹툰의 제목 데이터가 있다.
- 파란색 동그라미는 '-'를 의미하는 이미지 데이터이다. 필요할 수도 있으나 거의 쓰지 않을 것 같다.
- 분홍색 줄은 이미지 태그의 텍스트 데이터인 `0`을 의미한다. 순위의 변동이 생기면 바뀐 순위에 따라 숫자값이 달라질 것이다. 현재 우리에겐 필요하지 않은 데이터이다.

> 여기서 우리는 순위값과 그에 따른 웹툰의 제목 데이터가 필요하다. 그러나 순위값은 파이썬에서도 코딩을 통해 부여할 수 있는 값이므로 파싱하지 않는다. 즉 파싱할 때에는 코딩으로 구현하기 어려운 데이터나 외부 데이터가 필요한 경우에 사용하는 것이 좋다.
___
- 여기서 1위의 웹툰 제목을 뽑아내고 싶다면 어떻게 코딩해야 할것인가? 다음과 같이 하면 된다.

```python
import requests
from bs4 import BeautifulSoup

url = "https://comic.naver.com/webtoon/weekday"
res = requests.get(url)
res.raise_for_status()

Soup = BeautifulSoup(res.text,"html.parser")
# ====================== 1 =========================== 
r1 = Soup.find("a", attrs = {"onclick" : "nclk_v2(event,'rnk*p.cont','747269','1')"})
r1 = Soup.find("a", attrs = {"title" : "전지적 독자 시점-087. Ep. 19 특이점 (1)"})
print(r1.text)
# ====================== 2 =========================== 
r1 = Soup.find("li", attrs = {"class" : "rank01"})
r2 = r1.next_sibling.next_sibling
print(r2.a.get_text())
```
- 위에 처럼 두가지 방식이 있다. 첫번째는 속성과 속성값의 딕셔너리 자료를 이용해서 해당 태그를 직접 찾는 방식이다.
- 두번째는 해당 태그보다 상위 태그(부모 태그)를 찾아서 그 다음값을 찾는 방식이다. 여기서 next_sibling을 두번 입력한 이유는 `</li>` 옆에 회색으로 `== $0` 이 숨겨져 있다. 이것도 넘어가야하기 때문에 두번 입력한다.
> 두번째 입력은 하나의 데이터만 찾는다면 유용하게 쓰일 수 있지만, 대부분 데이터를 어떤 규칙에 맞춰서 혹은 전부 긁어와야 하기 때문에 첫번째 식으로 데이터를 찾는 방식을 익히자.
___
- 그렇다면 순위 전부의 데이터를 뽑아내고 싶다면 어떻게 해야 할까?
- 우선 가장 중요한 것은 규칙을 잘못 적용하면 옆에 요일에 따른 웹툰 제목을 긁어올 수 있다. 따라서 영역을 먼저 지정하여 스크래핑을 하고 거기서 파싱을 하는 것이 중요하다.
  
```python
import requests
from bs4 import BeautifulSoup

url = "https://comic.naver.com/webtoon/weekday"
res = requests.get(url)
res.raise_for_status()

Soup = BeautifulSoup(res.text,"html.parser")
r1 = Soup.find("ol", attrs = {"id" : "realTimeRankFavorite"})
r2 = r1.find_all("a")
list = []
for row in r2:
    list.append(row.text)
print(list)
```
- 여기서 `Soup.find("ol", attrs = {"id" : "realTimeRankFavorite"})`는 인기급상순 웹툰의 리스트 태그이다. 즉, 순위 데이터들의 부모 태그이기 때문에 우선 부모 태그를 찾는다.
- 두번째, `r1.find_all("a")`을 이용해서 웹툰 제목이 텍스트로 들어가있는 `<a>`태그들을 전부 리스트 데이터에 넣는다. __주의하자 find_all을 이용하면 리스트 데이터에 각각 들어간다.__
- 세번째, 리스트 데이터에 들어간 문자열은 `<a>`태그로 시작하는 문자열이기 때문에 양 사이드의 태그를 없애줘야 한다. 그러기 위해서 for문을 이용해 데이터 하나하나 꺼내서 `.text`를 이용하여 텍스트 데이터만 뽑아낸 후, 다시 리스트에 담아주면 끝난다.
> 이런 식으로 html의 구조와 태그의 속성, find 명령어를 이용해서 쉽게 원하는 데이터를 뽑아낼 수 있다.
___
#### 2. 이미지 데이터
이번에는 다음의 각 연도마다 관람객 수가 많은 영화들의 이미지 데이터를 추출해보자. 우선 전체 코드는 다음과 같다.

```python
from bs4 import BeautifulSoup
import requests
for year in range(2017,2022):
    url = f"https://search.daum.net/search?w=tot&q={year}%EB%85%84%EC%98%81%ED%99%94%EC%88%9C%EC%9C%84&DA=MOR&rtmaxcoll=MOR"
    res = requests.get(url)
    res.raise_for_status()

    res_obj = BeautifulSoup(res.text, "html.parser")
    imgs = res_obj.findAll("img" ,{"class" : "thumb_img"})

    for i,img in enumerate(imgs):
        img_url = img["src"]
        if img_url.startswith("//"):
            img_url = "http:" + img_url
        
        img_res = requests.get(img_url)
        img_res.raise_for_status()

        with open("movie{}_{}.jpg".format(year,i+1), 'wb') as f:
            f.write(img_res.content)
        if i+1 >4:
            break
```

이제 하나하나 분석해보자.

<img src="https://user-images.githubusercontent.com/97590480/151173644-7beac346-59c5-4261-b657-2a6a98d92ae6.png">

```python
for year in range(2017,2022):
    url = f"https://search.daum.net/search?w=tot&q={year}%EB%85%84%EC%98%81%ED%99%94%EC%88%9C%EC%9C%84&DA=MOR&rtmaxcoll=MOR"
    res = requests.get(url)
    res.raise_for_status()

    res_obj = BeautifulSoup(res.text, "html.parser")
    imgs = res_obj.findAll("img" ,{"class" : "thumb_img"})
```
- for문을 이용해서 2017년도부터 2021년도까지의 영화 이미지를 수집하는 명령어를 넣었다.
- 여기서 다음의 영화 순위 웹 페이지에 규칙이 있었는데, 위에 {year}부분에 연도가 들어가고 나머지는 동일했다는 것이다. 우리는 이것을 이용해 포맷팅으로 각 연도에 맞는 페이지를 불러올 수 있다.
- 또한, 위의 이미지에서 빨간색으로 표시된 부분이 `imgs = res_obj.findAll("img" ,{"class" : "thumb_img"})`에 해당하는 부분이다. 즉, findall 명령어를 사용해서 5개의 데이터를 모두 불러온다.
___
```python
for i,img in enumerate(imgs):
        img_url = img["src"]
        if img_url.startswith("//"):
            img_url = "http:" + img_url
        
        img_res = requests.get(img_url)
        img_res.raise_for_status()
```

- 5개의 이미지 데이터에 관한 태그 데이터를 리스트 형태로 가져왔으므로 for문을 이용하여 하나하나 분리해서 원하는 데이터를 추출해보자.
    - enumerate는 순서와 리스트 안의 데이터를 나열해주는 명령어이다. 예를 들어 ['a','b','c']를 enumerate로 표현하면 `0 'a', 1 'b', 2 'c'`이다. 즉, i는 인덱싱 숫자를, img는 리스트 안의 데이터를 입력받는다.
- `img["src"]`은 `<img>`태그의 하이퍼링크 value값을 'src' 라는 key값으로 찾아내는 명령어이다. 잊자말자 속성은 딕셔너리 형태로 저장된다.
- `if img_url.startswith("//"): img_url = "http:" + img_url`은 하이퍼링크에 http:가 없는 경우가 있다. 따라서 옆에 http:를 붙여주는 명령어이다.
- 즉, img_url은 완전히 하이퍼링크 값을 가지게 된다.

<img width = "80%" src="https://user-images.githubusercontent.com/97590480/151175369-ef7e98d3-f68a-4e09-9214-82a94efde414.png">

> 하이퍼링크로 들어가면 위의 이미지처럼 나오게 된다.
- __여기서 중요한 것은 하이퍼링크라는 것이다. img_url은 이미지가 아니다. 그러나 하이퍼링크로 들어가면 이미지만 존재한다. 즉, 여기서 img_url로 재크롤링을 해야 된다는 것이다.__
- 따라서 `img_res = requests.get(img_url)`을 입력하여 하이퍼링크를 다시 한 번 크롤링을 해준다.
___

```python
with open("movie{}_{}.jpg".format(year,i+1), 'wb') as f:
    f.write(img_res.content)
if i+1 >4:
    break
```
- 이미지를 with 구문을 이용하여 저장할 수 있다. 이전에 txt파일로 파일을 읽고 여는 등의 명령어를 실행했던 적이 있다. 이번에는 이미지 파일이다.
- `'wb'` 는 'w'이긴 한데 binary 데이터이기 때문에 b를 붙여준다. 이미지는 바이너리 데이터인 것을 잊지 말자.
- 그러므로 저장할 때도 `f.write(img_res.txt)`가 아닌 `f.write(img_res.content)`를 써줘야 한다.
