# TIL(Today I Learned)

___

> Jan/28th/2022_Multi campus_유선종 Day17

## 셀레니움 실습
이번에는 비행기 티켓을 셀레니움을 이용해서 예매하는 실습을 진행하고자 한다.
### 1. 네이버 항공권 들어가기
- 1. 가장 쉬운 방법은 네이버 항공권의 url을 그대로 복사하는 방법이다.
- 2. 혹은 네이버 검색창을 이용해서 들어가는 방법이다.
> 나는 공부를 하는 입장이니 검색해서 들어가보겠다.

```python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

url = "http://naver.com"
driver = webdriver.Chrome(r"/Users/yuseonjong/Downloads/chromedriver")

driver.get(url) # 네이버 열기
driver.maximize_window() # 창 최대화
element = driver.find_element_by_id("query") # 네이버 검색창 선택
element.send_keys("네이버 항공권") #네이버 검색창에 네이버 항공권 입력
element.send_keys(Keys.ENTER) # 엔터 실행
```
1. 이 코드는 어제 설명했으니 잘 모르겠다면 Day16을 참고하자. 간단히 설명하자면 `driver.get`으로 네이버 창을 열고 `driver.maximize_window()`으로 웹 브라우저를 화면에 꽉 차게 최대화한다.
2. 검색창의 id가 "query" 이므로 find_element_by_id 명령어를 이용해서 검색창을 찾는다.
3. 검책창에 "네이버 항공권"을 입력하고 엔터키를 누른다.

<img src="https://user-images.githubusercontent.com/97590480/151469195-7b1499d1-8ce0-4652-b311-4a269b14cf1b.png">

> 그러면 위의 이미지처럼 이동한다.
___
### 2. 네이버 항공권 들어가기
여기서 네이버 항공권을 클릭해서 지정된 링크를 타고 네이버 항공권 페이지로 들어가야 한다. 이를 위해서 다음과 같은 코드를 짠다.

```python
driver.find_element_by_class_name("link_name").click() # 네이버 항공권 하이퍼링크 클릭
driver.switch_to.window(driver.window_handles[0]) #이전 네이버 탭으로 이동
driver.close() #네이버 탭 닫기
driver.switch_to.window(driver.window_handles[0]) #네이버 항공권 탭으로 이동
```

1. 하나하나 살펴보자. 우선 네이버 항공권 링크를 타기 위해 하이퍼링크가 있는 태그를 클래스를 이용해서 찾는다. 즉, `class = link_name`인 태그를 찾아서 클릭을 하면 링크를 들어갈 수 있다.
2. 이렇게만 해도 끝이 나지만, 네이버 항공권 탭만 남기고 네이버 탭을 지우고 싶다. 그래서 위와 같이 `driver.switch_to.window(driver.window_handles[0])` 명령어를 사용한다.
    - 이 명령어는 브라우저의 탭을 바꾸는 명령어이다. 즉, `driver.window_handles[]`는 현재 열려있는 탭의 위치를 받는 명령어이다. 현재 네이버와 네이버 항공권이라는 두개의 탭이 열려 있으므로 네이버 탭은 첫번째([0]), 네이버 항공권은 두번째([1])에 위치해있다.
    - 그러나 현재 내가 작업을 하고 있는 창은 네이버 항공권이다. 하이퍼링크를 타고 들어간 순간 나의 현재 윈도우 창은 그 링크 탭이 된다. 즉, 내가 어떤 명령어를 실행하면 네이버 항공권 창에서 실행이 된다.
    - 이것을 네이버 탭으로 바꿔주기 위해 `switch_to.window` 명령어를 사용해서 나의 현재 작업 창을 네이버로 바꿔준다.
3. 현재 내 작업 탭은 네이버이다. 여기서 `.close()` 명령어를 실행하면 현재 내 탭을 닫을 수 있다. 이 명령어를 사용해서 네이버를 닫는다.
4. 이렇게 되면 내 현재 작업창은 하나 남은 네이버 항공권으로 바뀐다. 그러나 수많은 탭이 있을 경우를 대비해서 `switch_to.window`명령어를 한번 더 이용해서 네이버 항공권 탭을 내 현재 작업창으로 바꿔준다.

___
### 3. 지연 시간 설정하기
 우리는 셀레니움을 예시를 볼 때, `time.sleep(5)`같은 명령어를 자주 볼 수 있다. 이런 명령어를 왜 넣지라는 생각을 처음에는 했지만, 우리는 현재 서버에 요청(request)하고 그 요청 내용을 받는(response) 단계를 거치기 때문에 서버와 연결되는데 시간이 걸린다. 코딩의 속도가 서버와 연결되는 시간보다 훨씬 빠르기 때문에 시간을 지연시켜주지 않으면 html 값들을 받기도 전에 코드가 실행되서 요소값이 없다는 오류가 발생한다.

```python
# element들을 파싱하기 전에 코드가 넘어가버리는 문제를 방지하기
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
WebDriverWait(driver,timeout=10).until(EC.presence_of_element_located((By.ID, "naver-splugin-dimmed")))
```

1. `WebDriverWait`명령어는 기다려주는 명령어이다. 우리가 셀레니움을 사용할 때 일부러 코딩 중간중간에 시간을 지연시키는 명령어를 넣어준다.
2. `until(EC.presence_of_element_located(By.ID,"naver-splugin-dimmed"))` 명령어는 ID가 "naver-splugin-dimmed"인 태그가 html에 나타날때 까지 기다린다는 명령어이다.
    -  우리가 어떤 링크를 들어갈때 웹 페이지에서 모든 요소가 한번에 빡 하고 나오지 않는다. 위에서부터 아래로 가면서 단계적으로 로딩되는 것을 볼 수 있다.
   -  나는 가장 아래에 네이버 회사 소개글이 나오는 것을 기준으로 이것이 나타나기 전까지 기다리라는 명령어를 입력하여 모든 요소들이 브라우저에 나타날때 까지 기다리라는 명령어를 입력했다.
3.  여기서 `EC.presence_of_element_located()` 명령어는 괄호 안이 나타날 때까지 기다린다는 명령어이다.
4.  `WebDriverWait(driver,timeout=10).until()` 명령어는 기다리라는 명령어이다. `EC`명령어도 기다리는 명령어인데 왜 중복해서 넣냐면 `timeout` 기능을 넣기 위해서이다. `EC`가 나타날때까지 기다리다가 `timeout = 10` 즉, 로딩 시간이 10초가 지나버리면 더이상 기다리지 않고 다음 코드로 넘어간다는 의미이다.

<img src="https://user-images.githubusercontent.com/97590480/151471938-bff439f0-82df-48dc-b6c7-35c54b60554f.png">

> 이제 이런 창만이 남았을 것이다.
___

### 4. 가는 날 클릭하기
이제 우리는 항공권을 예매하기 위해 가는 날짜를 설정해야 한다. 나는 다음과 같이 코딩했다.

```python
# 날짜 설정
start_date = '2022.1.28'
start_month = int(start_date.split('.')[1])
start_day = int(start_date.split('.')[2])
end_date = '2022.1.31'
end_month = int(end_date.split('.')[1])
end_day = int(end_date.split('.')[2])

# 가는 날 선택
import time
driver.find_elements_by_class_name("tabContent_option__2y4c6.select_Date__1aF7Y")[0].click()
time.sleep(3)
```

<img src="https://user-images.githubusercontent.com/97590480/151475272-13ae0ce6-2ebb-40e2-beb9-7bc22fa4a935.png">

1. 우선 날짜를 설정했다. 날짜는 시각적으로 보기 좋게 풀어서 썼다. `split('.')`은 문자열 안에 괄호를 제거하고 리스트로 저장하는 함수이기 때문에 월과 일을 구분해줬다.
2. 저 위에 가는 날을 클릭해줘야 한다. `find_element_by_class_name`을 이용해서 찾고 클릭하자.
   - 여기서 나는`elements`를 사용했다. 복수의 s가 붙었으므로, 동일한 클래스 이름을 가진 모든 태그를 가져오는 명령어라고 생각하면 된다. 그러면 리스트 형태로 저장하는데, 그중 나는 첫번째가 필요하므로 [0]으로 인덱싱해줬다.
   - __매우매우 중요한 것은 클래스 이름에 띄어쓰기(space)가 있으면 find 명령어는 해당 클래스를 찾지 못한다는 것이였다.__ 자세한 것은 모르겠지만 이를 해결하기 위해서는 __띄어쓰기를 점(.)으로 바꿔주면 띄어쓰기를 읽는다는 것이다.__ 
    > 물론 xpath를 복사해서 가져오면 되지만 이런 사소한 것을 몰라서 내가 원하는 방향대로 구현하지 못하는 것을 나는 싫어한다.
3. 클릭하면 창이 새로 열리기 때문에 여기서도 로딩 시간을 위해 time.sleep(3)을 입력했다. time.sleep을 이용할 때에는`import time`을 해줘야 한다.
___
### 5. 날짜 설정하기

<img src="https://user-images.githubusercontent.com/97590480/151474994-2b8aa8c1-3974-4ce8-930b-7dc072cb4b08.png">

```python
# 가는 날
day = driver.find_elements_by_xpath(f"//*[text()='{start_day}']")
monthday = day[start_month-1]
monthday.click()

# 오는 날
day = driver.find_elements_by_xpath(f"//*[text()='{end_day}']")
monthday = day[start_month-1]
monthday.click()
```

- 여기서 나는 xpath를 썼는데, xpath는 html의 인덱싱이라고 생각하면 좋다. 예를 들어 위의 4.가는 날 에서는 find_element를 이용해서 가는 날의 html값을 찾았다. 동일한 명령어를 xpath로 표현하면 다음과 같다.

```python
driver.find_element_by_xpath("//*[@id='__next']/div/div[1]/div[4]/div/div/div[2]/div[2]/button[1]").click() # 가는 날 선택 xpath 방법
```
> div/div[1]은 상위의 div 태그에서 하위의 div 태그들 중에서 2번째([1]) div로 내려간다. 즉, 위에서 아래로 차례대로 내려가 찾는다고 생각하면 된다.

1. 여기서 `find_elements_by_xpath("//*[text()='29']")`는 텍스트로 29을 갖는 모든 태그들의 xpath를 찾는다는 의미이다.
   - `text()='29'` 는 해당하는 텍스트를, `*` 은 모든 태그를 의미한다. 예를들어, `<a>`, `<input>` 등 원하는 태그를 입력하고 싶다면 * 대신에 a나 input을 넣어주면 된다.
   - elements이므로 29를 포함하는 모든 xpath를 찾는다는 의미이다. 이렇게하면 리스트 형태로 모든 xpath를 담아준다.
2. day[start_month-1]를 이용해서 내가 원하는 월의 29일을 선택하도록 입력했다.
    > 현재 day에는 `['1월 29일 xpath','2월 29일 xpath','3월 29일 xpath',...,'2023년 1월 29일 xpath']`의 데이터가 담겨있다. 즉 day는 13개의 데이터가 리스트 안에 담겨있고, 내가 원하는 날짜는 2022년 1월 데이터이기 때문에 첫번째([0]) xpath를 가져오면 된다.
3. 해당 xpath를 클릭하면 해당 날짜가 선택된다.
4. 오는 날도 동일하게 선택하면 기간이 설정이 된다.
___
### 6. 도착지 설정
위의 내용을 이해했다면 이제부터는 쉽다. 동일한 내용의 반복이다.

<img src="https://user-images.githubusercontent.com/97590480/151477330-6d491b63-94a9-498e-b40a-f5777aa4c3fc.png">

```python
airport = "로스엔젤레스" #공항 설정
# 도착지 선택
driver.find_element_by_class_name("tabContent_route__1GI8F.select_City__2NOOZ.end").click() 
driver.find_element_by_class_name("autocomplete_input__1vVkF").send_keys(f"{airport}") # LA공항 입력
time.sleep(1)
driver.find_element_by_class_name("autocomplete_search_item__2WRSw").click() # 공항 선택
```
- 여기서도 기간을 설정한 것처럼 동일한 명령어를 사용했다. 다만 다른 것은 공항을 직접 텍스트로 입력해야 하기 때문에 send_keys를 사용했다.
___
### 7. 인원수 설정

<img src="https://user-images.githubusercontent.com/97590480/151477510-cc07b3b7-f3c2-4c24-ab70-571f5192203a.png">

```python
population = 4 # 4명
driver.find_element_by_class_name("tabContent_option__2y4c6.select_Passenger__36sFM").click()
time.sleep(1)
# 4명 선택
for i in range(population-1):
    driver.find_element_by_class_name("searchBox_outer__9n6IB").click()
# 검색 클릭
for i in range(2):
    driver.find_element_by_class_name("searchBox_txt__3RoCw").click()
WebDriverWait(driver,timeout=30).until(EC.presence_of_element_located((By.ID, "jsx-672200263 btn as_top")))
```

- 이번에는 버튼을 클릭하는 것을 반복해야 되기 때문에 for문을 사용했다.
> Day16에서 소개한 것처럼 
```python
element = driver.find_element_by_css_selector("b.value")
driver.execute_script("arguments[0].innerText = "4", element)
```
> 을 입력해줘도 된다. 그러나 `b.value`와 동일한 태그가 많기 때문에 또 인덱싱을 해줘야 한다는 귀찮은 문제가 있다. 어쩔수 없이 인덱싱을 할 경우는 해야되지만, 지금처럼 버튼 클릭으로 가능하다면 최소한의 인덱싱을 통해 코딩을 하자.

#### 이제 실행을 하면 최저가 항공부터 쫘르륵 뜰 것이다. 이런 식으로 셀레니움을 통해서 내가 원하는 날짜의 항공권을 알아서 찾아주는 실습을 진행해봤다. 처음엔 복잡해보이지만 이해하면 쉽기 때문에 잘 이용해보자.