# TIL(Today I Learned)

___

> Fab/11th/2022_Multi campus_유선종 Day31

## Django
장고는 웹 페이지를 만들수 있는 프레임워크이다. 다양한 웹 개발 프레임워크 중에서 우리가 장고를 배우는 이유는 장고가 __파이썬__ 을 기반으로 하는 프레임워크이기 때문에 파이썬을 기반으로 하는 개발자들에게 적합하기 때문이다.

### 1. 장고의 장점
- 장고는 이미 다양한 기업에서 사용하고 있는 프레임워크이다. 이런 기업들이 장고를 이용하는 이유 중 가장 큰 부분을 차지하는 것은 파이썬을 기반으로 한다는 것이다.
- 하지만 그것뿐만 아니라 장고는 html, css, 자바 스크립트뿐만 아니라 데이터베이스, 라우팅에 관한 기본적인 틀을 제공해준다. 장고를 시작하면 이러한 기능들을 기본적으로 사용할 수 있다는 장점이 있다.
> 장고를 사용하는 대표적인 앱은 인스타그램이 있다.

### 2. 장고 환경설정
그러면 이제 장고를 설정해보자. 우선 `pip install Django`로 장고를 다운받고 장고의 폴더를 생성할 위치에 터미널을 위치시킨다. 나는 홈 폴더에서 mySite라는 폴더 안에 장고에 관련된 폴더를 생성하고자 한다. 그렇다면 다음과 같은 명령어를 따라 입력해주면 된다.
```python
mkdir mySite
cd mySite
django-admin startproject Test
```
- 위의 명령어를 입력하면 mySite 폴더가 home폴더에 생성되고 mySite로 이동해서 Test라는 폴더를 생성해준다. 이때 Test폴더는 장고에서 실행하는 모든 명령어가 실행되는 폴더가 된다. 밑의 예를 보자.

```python
cd Test
python manage.py runserver 0.0.0.0:80000
```
- 위의 명령어를 입력하면 아까 생성했던 Test폴더로 이동하고 `python manage.py runserver 0.0.0.0:8000`은 장고의 서버에 접속하겠다는 명령어이다. 입력하면 웹에 접속이 되는데 만약 접속을 끊고 싶다면 Ctrl+C로 빠져나오면 된다. 접속이 됐는지 확인하기 위해 어떤 브라우저를 사용해도 상관없으니 크롬에서 주소창에 `localhost:8000`을 입력해보자.

<img src="https://user-images.githubusercontent.com/97590480/153601990-ff78e2be-c8da-4257-9f9c-f25855a2fd05.png">

- 위의 페이지가 나왔다면 잘 접속이 된 것이다. 이런 식으로 프로젝트를 만들고 웹 서버에 접속해서 다양한 형태의 웹 페이지를 만들 수 있다.
