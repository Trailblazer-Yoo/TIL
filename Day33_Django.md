# TIL(Today I Learned)

___

> Fab/13th/2022_Multi campus_유선종 Day33

## 장고 3일차
어제는 장고의 아주 간단한 웹 페이지를 만드는 법을 알아보았다. 이번엔 좀더 복잡해진다.

### 1. css를 포함한 웹 페이지 만들기
css는 웹 페이지를 만들때 다양한 디자인적인 설정을 하는 파일이라고 생각하면 된다. 우선 `python manage.py startapp index`를 실행시켜 index폴더를 만들어주고 Investar1 폴더의 urls에 웹 페이지 설정을 추가해주자.

<img src="https://user-images.githubusercontent.com/97590480/153748778-7250e154-c0e2-4892-9638-0a52dba73cd6.png">

> 위의 처럼 패스를 설정해주면 'localhost:8000/index'를 입력했을 시에 해당 페이지에 views에 설정한 웹 페이지가 나오게 된다.

또한, settings.py에 index를 추가해주고, views를 설정해준다.

<src="https://user-images.githubusercontent.com/97590480/153748880-6ad5f242-1da1-47f0-bc60-6c1c1198bac2.png">

이때 views에 `render(request, index.html)`은 index.html을 불러온다는 의미이다. request는 그냥 넣어줘야 하는 변수이므로 넣어줘야 한다.

```html
{% load static %}
<html>
    <head>
        <title>This is title.</title>
        <link rel="stylesheet" href={% static "index/style.css" %} /> 
    </head>
    <body>
        <h1>This is heading1 text.</h1>
        <h2>This is heading2 text.</h2>
        <h3>This is heading3 text.</h3>
        <p>This is a paragraph.</p>
        This is plain text.<br /> 
        <b>This is bold text.</b><br />
        <i>This is Italic text.</i><br />
        <s>This is strike text.</s><br />
        <ol>
            <li>the first orderd list</li>
            <li>the second orderd list</li>
            <li>the third orderd list</li>
        </ol>
        <ul>
            <li>unorderd list</li>
            <li>unorderd list</li>
            <li>unorderd list</li>
        </ul>
        <table border=1>
            <tr>
                <th>table header 1</th>
                <th>table header 2</th>
                <th>table header 3</th>
            </tr>
            <tr>
                <td>table data 4</td>
                <td>table data 5</td>
                <td>table data 6</td>
            </tr>
            <tr>
                <td>table data 7</td>
                <td>table data 8</td>
                <td>table data 9</td>
            </tr>
        </table><br />
        <a href="www.djangoproject.com">Visit Django homepage!<br />
        <img src="Django_Logo.jpg"/>
        <img src={% static "index/Django_Logo.jpg" %} /></a>
    </body>
</html>
```

- 위의 코드는 index.html 파일의 코드이다. 여기서 맨 윗줄의 `{% load static %}`를 반드시 써줘야 한다. 이 말의 뜻은 static을 가져오겠다는 뜻이다. 폴더 구조를 한번 살펴보자.

<img src="https://user-images.githubusercontent.com/97590480/153749049-cfc71ec9-442f-4be0-b4c1-80ab8c7d9937.png">

> 여기서 html파일은 반드시 templates에 넣어둬야 경로를 읽고 가져온다.

<img  src="https://user-images.githubusercontent.com/97590480/153749059-958632f0-2d6b-439a-a229-938028484a5b.png">

> html과 마찬가지로 static 파일에 css와 이미지 파일이 있어야 관련된 디자인이 적용이 된다.

- 위의 폴더를 참고해보면 static을 load해서 관련 파일을 모듈로 불러오겠다는 의미이다.
- `<link rel="stylesheet" href={% static "index/style.css" %} /> `와 `<img src={% static "index/Django_Logo.jpg" %} /></a>`는 static 폴더 안에 있는 css파일과 이미지 파일에 관련된 설정이다.

```css
table td, table th {
    border: 1px solid #ddd;
    padding: 8px;
}

/* 테이블 행이 짝수 번째일 경우의 색상 지정 */
table tr:nth-child(even){background-color: #f2f2f2;}

/* 테이블 행에 마우스 커서를 올렸을 때의 색상 지정*/
table tr:hover {background-color: #ddd;}

/*테이블 헤더에 대한 스타일 지정*/
table th {
    padding-top: 12px;
    padding-bottom: 12px;
    text-align: left;
    background-color: #4CAF50;
    color: white;
}
```

- 위의 코드 처럼 각 태그에 대한 글자 크기나 색상 등을 지정할 수 있다.
- 이러한 설정을 했을 경우 다음과 같은 웹 페이지가 나오게 된다.

<img src="https://user-images.githubusercontent.com/97590480/153749310-bd6beef2-fb7e-4a82-97e0-182449922a10.png">

### 2. 내 잔고 확인하기
두번째는 네이버에서 주식 가격과 상승률을 크롤링해서 내 잔고를 표시해주는 웹 페이지를 만들어보겠다.

1. `python manage.py startapp balance`로 balance파일을 추가해주고 settings.py에 balance를 추가하며, urls에 다음과 같이 작성해주자.

<img src="https://user-images.githubusercontent.com/97590480/153749414-7cb5d434-6960-4d5d-b24d-bd3321142f87.png">

2. balance 폴더에 가서 views에서 크롤링하는 코드를 작성해준다.

```python
from django.shortcuts import render
from bs4 import BeautifulSoup
from urllib.request import urlopen
# Create your views here.

def get_data(symbol):
    url = 'http://finance.naver.com/item/sise.nhn?code={}'.format(symbol)
    with urlopen(url) as doc:
        soup = BeautifulSoup(doc, "lxml", from_encoding="euc-kr")
        cur_price = soup.find('strong', id='_nowVal')  # ①
        cur_rate = soup.find('strong', id='_rate')  # ②
        stock = soup.find('title')  # ③
        stock_name = stock.text.split(':')[0].strip()  # ④
        return cur_price.text, cur_rate.text.strip(), stock_name

def main_view(request):
    querydict = request.GET.copy()
    mylist = querydict.lists()  # ⑤
    rows = []
    total = 0

    for x in mylist:
        cur_price, cur_rate, stock_name = get_data(x[0])  # ⑥      
        price = cur_price.replace(',', '')
        stock_count = format(int(x[1][0]), ',')  # ⑦
        sum = int(price) * int(x[1][0])
        stock_sum = format(sum, ',')         
        rows.append([stock_name, x[0], cur_price, stock_count, cur_rate,
            stock_sum])  # ⑧
        total = total + int(price) * int(x[1][0])  # ⑨

    total_amount = format(total, ',')       
    values = {'rows' : rows, 'total' : total_amount}  # ⑩
    return render(request, 'balance.html', values)  # ⑪
```
크롤링에 대한 내용은 저번주에 많이 설명했으므로 생략하겠다.

3. templates 안에 balance.html 파일과 static에 balance라는 폴더를 생성하고 css파일을 만들어서 넣는다.

```html
{% load static %}
<html>
    <head>
        <title>Balance: {{ total }}</title>  <!-- ① --> 
        <link rel="stylesheet" href="{% static 'balance/b_style.css' %}"/>
    </head>
    <body>
         <table>
            <tr>
                <th>종목명</th>
                <th>종목코드</th>
                <th>현재가</th>
                <th>주식수</th>
                <th>등락률</th>
                <th>평가금액</th>
            </tr>
            {% for row in rows %}
            <tr>
                {% for x in row %}
                <td>{{ x }}</td>  <!-- ② -->
                {% endfor %}
            </tr>
            {% endfor %}
            <tr>
                <th colspan=3>계좌 잔고</th>
                <th colspan=3>{{ total }}</th>  <!-- ③ -->
            </tr>
        </table>
    </body>
</html>
```

```css
/* 테이블 폰트 및 테두리선 설정 */
table {
    font-family: Arial, Helvetica, sans-serif;
    border-collapse: collapse;
}

/* 테이블 데이터 및 테이블 헤더 설정 */
table td, table th {
    border: 1px solid #ddd;
    padding: 8px;
}

/* 테이블 행이 짝수 번째일 때의 색상 지정 */
table tr:nth-child(even){background-color: #f2f2f2;}

/* 테이블 행 위에 마우스 컬러가 올려졌을 때의 색상 지정 */
table tr:hover {background-color: #ddd;}

/* 테이블 헤더의 스타일 지정 */
table th {
    padding-top: 12px;
    padding-bottom: 12px;
    background-color: #4D92AA;
    text-align: center;
    color: white;
}

/* 테이블 데이터의 텍스트 정렬 방식을 지정 */
table td:nth-child(1){text-align: left;}
table td:nth-child(2){text-align: center;}
table td:nth-child(3){text-align: right;}
table td:nth-child(4){text-align: right;}
table td:nth-child(5){text-align: right;}
table td:nth-child(6){text-align: right;}
```
- 이런 식으로 작성해서 넣어준다. 코드를 하나하나 설명하고 싶지만 솔직히 나도 모른다. 내가 html과 css에 대해 아는 것이 없기 때문에 대충 이러한 느낌으로 작성하는구나만 확인하고 넘어가자. 우리는 데이터를 분석하는 사람이지 웹페이지를 만드는 사람들이 아니다. ~~물론 배우면 좋지만 하나부터 잘하고 보자~~

- 이렇게 만든 웹페이지의 결과물은 다음과 같다.
  
<img src="https://user-images.githubusercontent.com/97590480/153749742-3afcfeed-8aff-4e71-868e-b23b77f37820.png">

위에 주소창에 주식종목과 내가 가지고 있는 주식 갯수를 포함하는 것을 볼 수 있다. 그리고 해당 주식종목에 대한 상승률과 평가금액이 나타나는 것을 볼 수 있다.