# TIL(Today I Learned)

___

> Jan/18th/2022_Multi campus_유선종 Day7

## 1. 알고리즘 문제_계속
Day06에서 완성하지 못한 은행 알고리즘 문제를 오늘 해결하고자 한다. 어제는 목록창에 대한 작업을 마쳤고, 오늘은 클래스 명령어를 만들어야 한다.

```[class명]
CAccount

[기능]
1. 입금 : deposit()
2. 출금 : withdraw()

[변수]
owner
amount : 초기값 0


[유의사항]
만약 입금, 출금액이 마이너스 값이면 : 정확한 금액을 입력하세요.
출금시 입력한 값이 잔액보다 많으면 : 잔액부족, 거래가 거절되었습니다. (종료)
```
### deposit()함수 정의
```class CAccount:
    def __init__(self, amount):
        self.amount = amount
    
    def deposit(self):
        switch = 1
        while switch:
            money = int(input(' 2번선택 : 입금할 금액을 알려주세요. '))
            if money > 0:
                self.amount = self.amount + money
                print('             {0}원이 입금되었습니다. 잔액은 {1}원 입니다.'.format(money, self.amount))
                switch = 0
                return self.amount
                break
            else: print('정확한 금액을 입력하세요.')
```
 - 우선 클래스에서 __init__을 이용하여 계좌에 들어있는 잔액을 amount라는 변수로 받고 self.amount에 넣어준다.
 - while문을 사용해서 입금할 금액이 음수이거나 문자일 경우 잘못됐다는 메세지를 출력하고 다시 처음부터 입력하도록 반복시켰다.
 - 입금할 금액이 제대로 됐다면 계좌의 잔액과 더해서 출력해준다. 또한 while문을 마치기 위해 switch를 0으로 만든다.
 > while문은 True값을 받을때 계속 반복하고 False값을 받을 때 멈추게 된다. 파이썬에서는 0은 False로 받는다. 따라서 switch를 0으로 만들어준다.

### withdraw()함수 정의
```def withdraw(self):
        switch = 1
        while switch:
            money = int(input(' 3번선택 : 출금할 금액을 알려주세요. '))
            if money > 0:
                if money > self.amount:
                    print('잔액부족, 거래가 거절되었습니다.(종료)')
                    break
                elif money <= self.amount:
                    self.amount = self.amount - money
                    print('         {0}원이 출금되었습니다. 잔액은 {1}원 입니다.'.format(money, self.amount))
                    switch = 0
                    return self.amount
            else: print('정확한 금액을 입력하세요.')
```
 - 출금할때는 계좌에 있는 금액보다 출금금액이 더 크면 오류가 뜨도록 조건을 더 걸어준다. 따라서 if문에 money > self.amount이면 바로 빠져나오도록 if문을 작성했다.

### 메뉴목록 수정
```menu_number = int(input("메뉴를 선택해 주세요."))
    if menu_number in menu_list:
        password = int(input("계좌 비밀번호를 입력해 주세요."))
        if init_password == password:
            if menu_number == 1:
                print(' 1번선택 : 잔액은 {amount}입니다.')
                continue
            elif menu_number == 2:
                CAcount.deposit()
            elif menu_number == 3:
                CAcount.withdraw()
            else:
                print(' 4번선택 : 계좌 거래가 종료되었습니다.')
                break
        else:
            print("계좌 비밀번호가 일치하지 않습니다. 다시 입력해주세요.")
            continue
```
위에 내용은 Day06에서 작성한 코드이다. 그러나 비밀번호를 한번만 입력하면 다시 입력하지 않는 기능을 추가하고 싶어서 아래와 같이 수정했다.
```menu_number = int(input("메뉴를 선택해 주세요. "))
    if menu_number == 4:
        print(' 4번선택 : 계좌 거래가 종료되었습니다.')
        break
    else:
        if password_switch == 1:
            while password_correct:
                password = int(input("계좌 비밀번호를 입력해 주세요. "))
                if init_password == password:
                    password_correct = 0
                else: print('잘못된 비밀번호입니다.')
        else: pass
```
 - 종료 메뉴는 비밀번호가 필요가 없으므로 맨 위로 올려줌으로써 비밀번호 입력에서 제외시켰다.
 - password_switch를 새로 추가해 한번 메뉴를 실행시키면 password_switch를 0으로 만들어 더이상 비밀번호를 입력하지 않도록 만들었다.
 - while문에 password_correct를 넣어 잘못된 비밀번호를 입력하면 다시 입력하도록 반복문을 넣어줬다.
 > 이번 과제를 통해 class에 대한 개념과 switch의 활용을 숙지했다.
## 2. Pandas
 - 판다스와 같이 파이썬에 내장되어 있지 않은 함수들을 정의하여 만들고 그것들을 여러개의 클래스 형태로 모아서 정리해놓은 것을 모듈이라고 한다. 우리는 `import` 명령어를 통해 이러한 모듈들을 불러와 필요한 함수들을 사용할 수 있다.
 > 특히 판다스에서는 기존의 R에서 사용하던 통계 함수들과 유사해서 데이터 분석을 하기 위해서는 필수적인 모듈이다.
 - 파이썬에서는 행렬 기능이 없기 때문에 numpy 모듈을 사용해서 작성해야 하지만, 판다스가 더 많은 기능과 익숙한 기능을 제공하기 때문에 numpy보다는 pandas에 익숙해지자. ~~그렇다고 numpy를 쓰지 않는다는 것은 아니다.~~
  ### pandas에서 행렬표현 익히기
  - 통계 분석에서 선형대수학을 모르면 분석이 불가능하다. 특히 빅데이터와 같이 자료가 방대해지면 질수록 행렬표현이 중요해지는데, pandas의 명령어를 통해 파이썬에서 행렬을 표현하는 방법을 익혀보자. _pandas랑 matlab이랑 명령어가 비슷해서 matlab을 익힌 분들은 pandas도 금방 익힐 것이다._
  - pandas를 사용하기 위해서는 `import pandas as pd` 명령어를 꼭 입력하고 시작하자. as pd는 입력하지 않아도 되지만 처리 속도를 위해 입력하는 것이 좋다.
  #### Series Data
    - Series Data는 선형대수학에서 벡터값을 의미한다고 생각하면 좋다. 만약 `[1,2,3]'` 의 3차원 벡터가 존재한다면, 이는 Series Data이다.
    - 여기서 [a,b,c]의 3차원 벡터가 [1,2,3]의 3차원 벡터와 동치라면 우리는 [a,b,c] = [1,2,3]이라고 표현한다.
      - 위의 표현을 우리는 딕셔너리 자료로 표현할 수 있다. 즉, `dict_data = {'a' : 1, 'b' : 2, 'c' : 3}`은 위의 3차원 벡터와 동일한 표현이다.
      > 좀더 정확히 말하자면 파이썬에서는 a의 key값이 1이라는 value를 갖기 때문에 a가 1을 포함하고 있다는 것이 정확한 표현이지만, 통계 분석을 위해서는 같다고 생각하는 것이 편하다고 생각한다.
    - `print(pd.Series(dict_data))`을 파이썬에서 실행해보면 다음과 같다.
      ```a   1
         b   2
         c   3
      ```
    - 딕셔너리 자료뿐만 아니라 리스트 형태의 자료도 Series Data를 표현할 수 있는데, `[1,2,3]` 이라는 리스트형 자료는 `print(pd.Series(dict_data))`을 실행해보면 다음과 같다.
        ```0   1
           1   2
           2   3
         ```
        - 즉, 왼쪽 열에서 리스트의 위치(index)값을 알려주고 오른족 열에서 위치값의 자료를 알려준다.
     > 물론 딕셔너리나 리스트 안에는 문자열(string)을 입력해도 된다. 판다스에서는 string 자료를 object라고 한다.
 #### Data Frame
   - 데이터 프레임은 행렬을 의미한다. __그런데 여기서 중요한 점은 딕셔러니 형태와 리스트 형태의 행렬 표현이 다르다는 점이다.__
   > Series Data에서는 값에 대한 위치값만 다를 뿐 요소값은 같았다. 하지만 이번에는 행렬 표현이 다르기 때문에 요소값이 달라질 수 있으므로 꼭 구별해서 사용하자.
   ##### 딕셔너리 형태의 Data Frame
     - `dict_data = {'A' : [1,2,3], 'B' : [4,5,6], 'C' : [7,8,9], 'D' : [10,11,12]}`라는 딕셔너리형 자료에 `print(pd.DataFrame(dict_data))`를 입력하면 다음과 같은 행렬이 나온다.
      |      | A    | B    | C    | D    |
      | ---- | ---- | ---- | ---- | ---- |
      | 0    | 1    | 4    | 7    | 10   |
      | 1    | 2    | 5    | 8    | 11   |
      | 2    | 3    | 6    | 9    | 12   |
      - 즉, __key값은 열 데이터로, Values값들은 열을 기준으로 위에서 아래로 정렬된다.__ 꼭꼭 기억하자.
   ##### 리스트 형태의 Data Frame
     - `list_data = [[1,2,3],[4,5,6],[7,8,9],[10,11,12]]`라는 리스트형 자료에 `print(pd.DataFrame(list_data))`를 입력하면 다음과 같은 행렬이 나온다.
      |      | 0    | 1    | 2    |
      | ---- | ---- | ---- | ---- |
      | 0    | 1    | 2    | 3    |
      | 1    | 4    | 5    | 6    |
      | 2    | 7    | 8    | 9    |
      | 3    | 10   | 11   | 12   |
     - __리스트형 자료는 왼쪽에서 오른쪽으로 정렬된다.__ 딕셔너리형은 열, 리스트형은 행을 기준으로 입력한다고 생각하면 좋다.
     - 딕셔너리 형태와 비슷해보이지만, 전혀 다른 행렬이 나오는 것을 알 수 있다. 주의해서 오류가 뜨지 않도록 조심하자.
     - 행과 열이 모두 목록(index)값으로 표시된 것을 알 수 있다. 따라서 행과 열을 설정해줘야 하는데, 명령어는 `print(pd.DataFrame(list_data, index = ['1행', '2행', '3행', '4행], columns = ['1열', '2열', '3열']))`이다. 즉, index는 행의 값, columns는 열의 값을 입력하면 된다.