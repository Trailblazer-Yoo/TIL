# TIL(Today I Learned)

___

> Jan/30th/2022_Multi campus_유선종 Day19

## class 복습
설날 연휴를 맞이하여 내가 약하다고 생각하는 부분들을 다시 한 번 정리하는 시간을 가질려고 한다. 

### 1. class
파이썬에서 클래스는 여러가지 함수를 담는 공간을 의미한다고 생각하면 된다.
- 클래스를 쓰는 이유는 함수(매서드)의 반복을 피하기 위해서이다.

```python
result = 0
def add(number):
    global result
    rusult += number
    return result

print(add(3))
print(add(4))
```
  
1. 예를 들어, 위의 코드처럼 다음과 같은 global값을 사용하는 함수를 정의했다고 하자.
2. global 함수는 함수 안에서 뿐만 아니라 함수 밖의 모든 코드에 영향을 받는 명령어이다. 즉, `global result`는 함수 밖의 result 값을 가져온다는 의미이다.
3. 이 코드를 실행하면 3과 7의 결과가 출력된다.
4. 이 코드를 실행하고 add 함수를 실행하여 다른 값을 출력하고 싶다고 add함수를 사용하면 이전에 입력했던 값이 그대로 남아있기 때문에 7 + 다른값을 결과값으로 받는다.

- 이렇게 내가 원하는 방식대로 각각 결과값을 받고 싶을때, 클래스 안에 함수를 넣어서 사용한다.
- 이러한 이유뿐만 아니라 클래스를 통해 이미 만들어놓은 함수들을 다른 코드에 사용하기 위해서 사용한다. 즉, 내가 원하는 쿠키 모양을 만들기 위해 쿠키 틀을 만든다고 생각하면 된다.
___
#### 1. 그러면 클래스는 어떻게 사용해?
우리는 두개의 숫자를 입력받아 더하는 클래스를 만들어보고 싶다. 다음과 같은 예시를 통해 이해해보자

```python
class Calculator:
    def setdata(self, first, second):
        self.first = first
        self.second = second
    def add(self):
        result = self.first + self.second
        return result
a = Calculator()
a.setdata(4,2) ## 변수 설정
sum = a.add()
print(sum)
```

1. 클래스를 만들기 위해서는 클래스를 선언해줘야 한다. class를 입력하고 클래스 이름을 지어주면 된다. 이때, 이름의 첫 글자는 대문자로 입력하는 것이 관례이다.
2. 클래스를 선언했다면 클래스에 사용할 변수들을 정의해줘야 한다. 여기서는 `setdata`라는 함수를 정의함으로써 클래스에서 사용할 변수들을 정의한다.
    - 여기서 self, first, second 변수들을 입력받는데, self는 인스턴스를 입력받는다.
    - 인스턴스란 클래스로 만든 객체를 의미한다.
        1. 객체는 어떤 속성값과 행동을 갖고 있는 데이터를 의미한다. `a = setdata()` 라는 코드에서 객체는 a다. setdata()라는 함수의 행동을 갖고 있기 때문이다.
        2. 이러한 여러 객체들 중에서 클래스에서 만든 객체는 인스턴스라고 한다. `a = Calculator()`일때 Calculator라는 클래스의 인스턴스이다.
        3. 이러한 인스턴스를 클래스 안에서 self라는 변수를 이용해서 입력받는다. `setdata(self, first, second)` 에서 `a = Calculator`라는 인스턴스가 존재할때, self는 인스턴스인 a를 받는다.
        4. 즉, self에 들어가는 자리에는 a라는 인스턴스를 입력해줘야 한다. 즉, `a.setdata(4,2)`는 `a.first = 4`, `a.second = 2`를 실행한다.
    - `setdata(self)`에서 self자리에 a를 넣지 않는다. a의 자리는 괄호 안에 넣지 않고 `a.setdata` 처럼 함수 앞에 입력한다.
    > 반대로 (self)안에 a를 넣고 싶다면 `Calculator.setdata(a,4,2)`로 입력해야 한다. 입력해야 하는 타자수가 더 많아지므로 `a.setdata(4,2)`로 입력하자.
3. 이렇게 `setdata(4,2)`를 통해 a.first와 a.second의 변수를 입력받았다면 원래 목적인 add 함수를 실행한다. `add(self)`에서 self만 있기 때문에, `a.add()`만 입력하면 된다.
___
#### 2. `__init__`
우리는 변수를 입력하는 함수를 사용해서 더하기 함수를 사용해서 어떤 결과를 도출했다. 만약, 처음부터 데이터를 무조건 설정하고 시작하는 명령어인 `__init__`을 사용할 수 있다.

```python
class Calculator:
    def __init__(self, first, second):
        self.first = first
        self.second = second
    def add(self):
        result = self.first + self.second
        return result
a = Calculator(4,2) ## 변수 설정
sum = a.add()
print(sum)
```
- 위에서 본 setdata와 결과는 동일하지만 다른 점이 있다. 이전에는 `a = Calculator()`로 a가 Calculator의 인스턴스라는 선언만 해줬다.
- 반면에 `__init__`을 넣어주면 `a = Calculator(4,2)`처럼 인스턴스를 선언할 때, 변수도 넣어줘야 한다.
- 만약에 입력하지 않으면 오류가 생긴다. 정말 필요한 변수가 있을때 `__init__`을 사용하면 좋다.
___
#### 3. 클래스 상속
클래스 상속이란 이미 존재하는 클래스를 다른 클래스에 집어넣는 것을 의미한다. 즉, 자식이 부모의 유전자를 그대로 물려받는 것과 비슷하다. 그렇지만 자식이 부모의 유전자를 물려받는다고 완벽히 똑같지는 않듯이, 자식 클래스에서 부모 클래스를 변형할수도 있다. 위의 예시를 이용해보자.

```python
class Calculator:
    def __init__(self, first, second):
        self.first = first
        self.second = second
    def add(self):
        result = self.first + self.second
        return result
class Add(Calculator):
    pass
a = Add(4,2)
sum = a.add()
print(sum)
```

pass는 지나친다는 의미로, 여기서는 부모 클래스의 명령어를 그대로 실행한다는 의미이다. 이때는 부모 클래스와 자식 클래스가 동일한 상태이다.

```python
class Calculator:
    def __init__(self, first, second):
        self.first = first
        self.second = second
    def add(self):
        result = self.first + self.second
        return result
class Add(Calculator):
    add(self):
    result self.first + self.second * 2 ## 매서드 오버라이딩
a = Add(4,2)
sum = a.add()
print(sum)
```

이렇게 add라는 함수를 재정의해서 덮어씌우는 것을 매서드(함수) 오버라이딩이라고 한다. 이제 결과는 4 + 2 * 2 = 8이 나온다.

> 매서드 오버라이딩은 함수뿐만 아니라 변수도 가능하다. 다음과 같은 예시를 살펴보자.
```python
class Family:
    lastname = '김'
Family.lastname = '박'
```
이 경우에 `print(Family.lastname)`을 실행하면 '박'이 나온다. 클래스 밖에서 `클래스명.클래스안의변수 = '바꿀 내용'`을 실행하면 오버라이딩이 실행되면서 실행한 이후의 lastname이 '박'으로 바뀐다. 클래스 안의 `lastname = '김'`은 그대로이기 때문에 상속받은 클래스에서 변수를 변경하고 싶을때 사용한다.

#### 4. 모듈
이러한 클래스가 여러개 모인 것이 모듈이다. 모듈은 보통 .py로 저장된 파일이고 이것을 불러오는 명령어를 실행해줘야 한다.

```python
import function
from function import Calculator
```

1. 위에처럼 function.py를 불러올려면 `import function`을 입력하면 된다.
2. 여기서 function.py 파일은 같은 폴더안에 있어야 한다. 만약 다른 폴더에 있다면 경로를 지정해줘야 한다. 경로 지정은 `function.path.append("경로")` 명령어를 사용한다.
3. function이라는 모듈에서 Calculator 클래스만 불러오고 싶다면 두번째 줄을 입력하면 된다.

- 가끔 모듈 안을 들어가면 `if __name__ == "__main__":` 이 있을 수도 있는데, 이것은 다른 파일에서 if문 내용을 실행하지 않는다는 것을 의미한다. 오직 모듈 파일에서만 실행이 된다. 예시를 입력하고 싶을때 사용한다.
___
#### 5. 라이브러리
이러한 모듈이 모인 것이 라이브러리(패키지)이다. 이미 이전에 사용한 numpy, matplotlib, pandas, selenium 등이 모두 라이브러리이다. 바퀴를 새로 만들지 말라는 격언이 적용되는 것이 이 라이브러리이다. 우리는 이 라이브러리를 불러와서 적용만 해주면 된다.
