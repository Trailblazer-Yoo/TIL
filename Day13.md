# TIL(Today I Learned)

___

> Jan/24th/2022_Multi campus_유선종 Day13
## html 기초
- html은 웹 문서를 만들기 위한 기본적인 웹 언어 중 하나이다. 
- 오늘날 인터넷 홈페이지는 이 hmtl 문법을 따르고 있으므로 인터넷에서 정보를 뽑아내는 크롤링을 하기 위해서는 기본적인 html 문법을 알아야 한다. 그렇다고 엄청 깊숙한 내용을 다루지 않아도 된다.
___

### 1. html 태그의 기본 요소
 - html 태그는 간략히 표현하면 하나의 함수이다. 문법에 맞는 함수를 태그로 표현하여 각각의 태그가 모여 하나의 문서를 이룬다.
 - 태그의 기본 구조는 다음과 같다.`<태그 속성 = 속성값;>콘텐츠</태그>`
 - 예를 들면, `<p>Hello World!</p>` 를 입력하면 Hello World! 라는 문자가 표시된다. 여기서는 속성에 어떤 값도 설정하지 않아 기본값으로 설정된다.
 - 더 쉽게 표현하면 <열기>내가 쓸 내용</닫기>이다. 내가 작성할 태그를 <열기>로 알려주고 </닫기>로 마친다. 그 사이에 내가 쓸 내용을 넣으면 된다.
___
### 2. html 문서의 구성
 - html 문서는 다음과 같은 기본적인 문법 요소를 가진다.
```html
<html>
<head>
</head>
<body>
    <p>Hello World!</p> 
</body>
</html>
```
- 첫번재로 인터넷 창틀을 의미하는 `<html></html>`을 작성해줘야 한다. 그림을 그릴 도화지라고 생각하면 된다.
- 두번째로 `<head></head>`를 작성해야 한다. 어떤 글을 작성하면 글의 제목과 소개에 해당되는 내용이다.
- 마지막으로 `<body></body>`를 입력하면 된다. body에는 내가 넣을 컨텐츠들이 들어가는 본문 영역이라고 생각하면 된다. 

### 3. head
head에 대해 알아보자.

<img src="https://user-images.githubusercontent.com/97590480/150734090-77cd1387-a631-482d-9191-6f4c0e575dd1.png">

```html
<html>
    <head>
        <meta charset = "UTF-8">
    </head>
    <body>
        <p>Hello World!</p> 
    </body>
</html>
```
- `<meta charset = "UTF-8">`은 맥에서 글씨가 깨지는 것을 방지해주는 태그다.
- 제목에 대한 어떤 태그도 없기 때문에 파일의 이름인 hello.html이 탭의 제목으로 표시되고, 페이지에는 Hello World!라는 내용이 표시된다.
- 그러면 이제 탭의 제목을 바꿔보자
___
```html
<html>
    <head>
        <meta charset = "UTF-8">
        <title>웹 프로그래밍 기초</title>
    </head>
    <body>
        <p>Hello World!</p> 
    </body>
</html>
```

<img src="https://user-images.githubusercontent.com/97590480/150735266-0087ea30-3ad1-4aea-8d6f-b7e4b50bba43.png">

- title 태그를 이용해서 제목을 '웹 프로그래밍 기초'라고 지었다. 이런식으로 내가 원하는 제목으로 바꿔줄 수 있다.
___
### 4. body
 - body에는 우리가 평소에 보는 홈페이지의 요소들을 넣는 공간이다. 다양한 태그들을 알아보자.
___
#### 1. <a>

<img src="https://user-images.githubusercontent.com/97590480/150767142-9fbe00a1-06ae-4714-8073-e65e1117df67.png">

```html
<html>
    <head>
        <meta charset = "UTF-8">
    </head>
    <body>
        <a href = "http://www.naver.com" target = "_blank" title = "네이버로 이동">네이버</a>
    </body>
</html>
```
- 여기서 a는 anchor의 줄임말로써 a 태그는 하이퍼링크를 연결하기 위한 태그이다. href는 하이퍼링그 속성이고, 네이버 주소는 속성값이다.
- 네이버라는 글씨가 페이지에 나오는데, 네이버를 클릭하면 네이버로 이동한다.
- 여기서 target은 페이지를 여는 방식을 결정한다. `"_blank"`는 새로운 탭에 네이버 홈페이지를 연다. 반대로 `"_self"`는 내 현재 탭에서 네이버 홈페이지로 이동한다.
- title은 제목을 넣어준다. 이것을 넣어도 겉으로는 변화가 없다. 하지만 네이버 위에다가 마우스를 놓고 몇초 기다리면 "네이버로 이동"이라는 말풍선이 생긴다.
___
#### 2. <img>

<img src="https://user-images.githubusercontent.com/97590480/150767699-e6a7c8b7-0497-4b1d-ab43-e841cd96ef97.png">>

```html
<html>
    <head>
        <meta charset = "UTF-8">
    </head>
    <body>
        <img src = "logo.png" width = "300px" height = "300px" alt = "로고">
    </body>
</html>
```
- img 태그는 이미지를 불러오는 태그이다. src에서 현재 폴더의 이미지 파일 이름을 넣어주면 된다.
- 혹은 src에 인터넷 이미지 주소를 복사해서 붙여넣어도 된다.
- width와 height는 각각 밑과 높이를 조절하고, alt는 이미지가 어떤 오류로 인해 나오지 않는다면 대체할 메세지를 의미한다.
___
#### 3. <h>
- h 태그는 제목을 설정하는 태그이다. 여기서 제목은 진짜 제목을 의미한다.
> 컴퓨터에서는 h가 들어가는 태그는 제목으로만 쓰이는 영역으로 내용이 들어가서는 안된다. 평소의 우리라면 단지 제목으로 쓰일 부분만 좀 진하고 크게 바꿔주지만, h는 아예 제목 영역을 지정하는 의미이다.

<img src="https://user-images.githubusercontent.com/97590480/150768484-5e9ee71b-627b-4cc8-afdb-47898f3efac3.png">

```html
<html>
    <head>
        <meta charset = "UTF-8">
    </head>
    <body>
        <h1>Hello World</h1>
        <h2>Hello World</h2>
        <h3>Hello World</h3>
        <h4>Hello World</h4>
        <h5>Hello World</h5>
        <h6>Hello World</h6>
    </body>
</html>
```
- 이런 식으로 굵기와 크기가 이미 정해져있다. 따라서 h1 ~ h6을 순서에 맞춰서 제목 영역으로 지정해야 한다.
___
#### 4. <p> & <span>

<img src="https://user-images.githubusercontent.com/97590480/150768934-0f0e75c7-521d-4f75-8bd7-c42b8dc46314.png">

```html
<html>
    <head>
        <meta charset = "UTF-8">
    </head>
    <body>
        <p>Hello, <span style = "color: red;">World!</span></p>
    </body>
</html>
```
- <p>는 문단을 정의하는 기능을 하고, <span>은 그 사이에 문장에 어떤 속성을 지정하기 위한 태그이다.
- 위에처럼 <span>이 없다면 단지 Hello, World! 만 출력이 되겠지만, 중간에 span으로 색깔을 빨간색으로 지정한 것을 볼 수 있다.
___
#### 5. 리스트 태그(<ol>,<ul>,<li>)
- 리스트를 생성하는 태그는 <ol>과 <ul>이다.

<img src="https://user-images.githubusercontent.com/97590480/150769503-66a2fa83-21c8-4fec-9b6e-31066b5f0487.png">

```html
<html>
    <head>
        <meta charset = "UTF-8">
    </head>
    <body>
        <ol>
            <li>순서가 있는 리스트(1)</li>
            <li>순서가 있는 리스트(2)</li>
            <li>순서가 있는 리스트(3)</li>
        </ol>
        <ul>
            <li>순서가 없는 리스트(1)</li>
            <li>순서가 없는 리스트(2)</li>
            <li>순서가 없는 리스트(3)</li>
        </ul>
    </body>
</html>
```
- 위에서 보듯 <ol> 태그는 순서가 있는 리스트를 형성할때, <ul> 태그는 순서가 없는 리스트를 형성할때 사용한다.
- 그리고 각 객체마다 <li>로 리스트 데이터임을 표시해준다.
___
#### 6. <imput>
<input> 태그는 설문조사같이 어떤 사람이 입력한 데이터를 받는 역할을 한다.

<img src="https://user-images.githubusercontent.com/97590480/150770191-0d6db6c0-5f96-4ed5-b319-985213dedc72.png">

```html
<html>
    <head>
        <meta charset = "UTF-8">
    </head>
    <body>
        <input type="text" value = "이름">
        <input type="submit" value = "제출">
        <p>당신의 취미는 무엇입니까?</p>
        <input type="checkbox">영화감상
        <input type="checkbox">사진
        <input type="checkbox">운동
    </body>
</html>
```
- <input> 태그에 type에 따라 다른 모습을 보이는데, text는 초기값을 value로 갖는 텍스트 입력창이다.
- submit은 value값을 단추로 보여주고 클릭하면 데이터를 보내주는 역할을 한다.
- checkbox는 체크박스로 선택/해제할 수 있다. 그 옆에 텍스트를 써주면 옆에 텍스트가 나온다.
___
#### 7. <br>
- <br>은 줄을 바꿔주는 기능을 한다. br을 넣지 않으면 동일한 태그에서는 한 줄에 연이어서 출력이 된다.
- 즉, '안녕하세요감사합니다'를 나눠주고 싶다면 `<p>안녕하세요</p><br><p>감사합니다</p>`를 입력하면 안녕하세요   감사합니다. 라고 입력이 된다.
> 이정도에서 html에 대한 내용을 마친다. html의 기본 구조를 알아야 여기서 데이터를 뽑아낼 수 있기 때문에 적어도 html의 문법에 대해 큰 구조를 파악하고 있어야 크롤링을 실시할 수 있다.