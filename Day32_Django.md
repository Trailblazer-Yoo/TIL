# TIL(Today I Learned)

___

> Fab/12th/2022_Multi campus_유선종 Day32

## 장고 2일차
어제는 장고의 환경을 설정하는 것을 알아보았다. 이번에는 직접 장고를 통해 웹을 만드는 것을 해보고자 한다.

### 1. 어플리케이션 생성하기
장고는 특이한 방식으로 어플리케이션을 만들 수 있는데, 우선 코드를 보자.
```python
python manage.py startapp hello
python manage.py migrate
```

 여기서 `python manage.py startapp hello` 명령어를 입력하면 hello라는 폴더를 생성해준다. 그러나 이 폴더는 일반 폴더와는 다르게 장고에서 필요로 하는 개발 환경이 이미 갖춰진 상태로 폴더를 만들어주기 때문에 이 명령어를 통해서 폴더를 만들어줘야 한다.

### 2. settings
장고는 모듈을 불러와서 저장하는 방식을 사용한다. 이게 무슨 말인지는 처음에 와닿지는 않지만 차근차근 알아보자.

<img src="https://user-images.githubusercontent.com/97590480/153715081-2e8e40c6-d3d7-4978-ada0-5c8ef39df651.png">

1. 여기 보면 Investar1 폴더 안에 여러 폴더가 있는 것을 볼 수 있다. 그 중에서 우리가 방금 생성했던 hello라는 폴더도 있고, Investar1 이라는 동일한 이름의 폴더 또한 있는 것을 볼 수 있다.
2. 여기서 동일한 이름을 가진 폴더는 전체적인 개발환경을 다룬다고 보면 된다. 그래서 우리는 hello라는 하나의 어플리케이션을 전체 개발환경에 등록을 해줘야 한다.
3. Investar1 폴더 안에 있는 Investar1 폴더 안에 settings.py 파일을 열어서 hello를 추가해줘야 한다.

<img src="https://user-images.githubusercontent.com/97590480/153715243-403ab29e-df6c-4578-a61b-c26ed52bc193.png">

1. 여기서 빨간색으로 된 영역 안에 내가 새로 만들 어플리케이션의 이름을 적어줘야 한다. 그래야 장고가 지금 만든 어플리케이션을 인식을 한다.

### 3. urls

<img src="https://user-images.githubusercontent.com/97590480/153715392-0cb58940-a0ed-4ceb-b152-f2deb38515a6.png">

1. 이번에 조작해줘야 하는 것은 urls.py 파일이다. 위에서 settings.py에 내 새로운 어플리케이션을 장고에 인식시켰다면, 웹에 내가 만든 어플리케이션을 띄우기 위해 urls.py에서 설정을 해줘야 한다.

<img src="https://user-images.githubusercontent.com/97590480/153715476-c5b1d377-2e74-43b4-97d6-0c3f084b70b6.png">

2. 빨간색 영역처럼 만들어줘야 하는데, `from hello import views`는 우리가 생성했던 폴더인 hello에서 views라는 것을 불러오겠다는 것이다. 여기서 views는 우리가 웹에 띄울 내용을 말하고, html을 만들거나 명령어를 통해서 어떤 값을 표시해주는데 사용된다.
> 여기서 노란색 밑줄이 쳐지면서 오류가 발생한 것처럼 나오는데 문제없이 실행되는 것을 확인할 수 있으므로 당황하지 말자.
3. 밑에 있는 코드들은 나도 자세히 모른다. 우리가 장고를 핵심으로 배우는 것이 아니기 때문에 자세한건 구글링을 통해 입력해주자.

### 4. views
urls.py에서 import해오는 views를 설정해줘야 한다.

<img src="https://user-images.githubusercontent.com/97590480/153715645-e8dad889-111b-40c3-9096-d8df6c06abe3.png">

여기서 우리가 의도하는 것은 hello라는 문구를 웹에 띄우기 위해서 관련 코드를 입력했다. 이제 웹 브라우저에 장고를 접속해서 해당 문구가 나오는지 확인할 수 있다.

### 5. 웹 브라우저에 출력
웹에 출력이 되는지 확인하기 위해서는 먼저 접속을 해줘야 한다. 현재 폴더가 Investar1에 위치되어있는 상태에서 터미널 명령어를 실행시켜주자.

```python
python manage.py runserver 0.0.0.0:80000
```
위 코드로 접속해주고 웹 브라우저에서 `localhost:8000` 을 입력하면 오류가 난 것 같은 페이지가 나온다. 그러나 `localhost:8000/Django`라고 입력해주면 제대로 잘 출력되는 것을 확인할 수 있다.

<img src="https://user-images.githubusercontent.com/97590480/153715891-51d626d9-46d1-4a12-888f-cc55b57c4e24.png">

> 다음과 같이 잘 출력된다.

### 6. migrate
이제 잘 만들어진 어플리케이션을 저장해줘야 하는데 이때 사용하는 명령어가 `python manage.py migrate`이다. 이 명령어는 깃처럼 커밋을 생성하는 것이라고 이해하면 좋다. 즉, 버전 업그레이드를 하는 것처럼 한번 찍히면 삭제가 불가능하다. ~~물론 삭제가 가능하지만 복잡해진다.~~