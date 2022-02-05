# TIL(Today I Learned)

___

> Jan/17th/2022_Multi campus_유선종 Day6

## 알고리즘 문제_은행잔고 알고리즘 만들기

```python
홍길동 통장
----------------
1. 잔액확인
2. 입금
3. 출금
4. 종료
________________
메뉴를 선택해 주세요.
계좌 비밀번호를 입력해 주세요. 

   1번선택 : 잔액은 ??? 입니다.
   2번선택 : 입금할 금액을 알려주세요. (1000)
                ??? 입금되었습니다. 잔액은 ??? 입니다.
   3번선택 : 출금할 금액을 알려주세요. (500)
                ??? 출금되었습니다. 잔액은 ??? 입니다.
   4번선택 : 계좌 거래가 종료되었습니다.
===========================
[class명]
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

### 메뉴창 만들기
```python
owner = '홍길동'
amount = 0
menu_list = [1,2,3,4]
init_password = 1234
while True:
    print(f'{owner} 통장')
    print("-"*30)
    for i in menu_list:
        list = ('잔액확인', '입금','출금','종료')
        print('{0}. {1}'.format(i,list[i-1]))
    print("="*30)
    menu_number = int(input("메뉴를 선택해 주세요."))
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
    elif menu_number not in menu_list:
        print("1,2,3,4 중 하나를 선택해주세요.")
        continue
    else:
        print("잘못된 메뉴 선택입니다. 다시 입력해주세요")
```
 - 아직 다 완성이 되지 않은 상태라 내일 수정이 필요하지만, 대충 어떤식으로 짰는지 설명하겠다.

```owner = '홍길동'
amount = 0
menu_list = [1,2,3,4]
init_password = 1234
```
 - 초기값을 설정해주는 파트이다. 패스워드는 임의의 값으로 성정했다.

```python
print(f'{owner} 통장')
    print("-"*30)
    for i in menu_list:
        list = ('잔액확인', '입금','출금','종료')
        print('{0}. {1}'.format(i,list[i-1]))
    print("="*30)
    menu_number = int(input("메뉴를 선택해 주세요."))
```
 - 계좌와 관련된 메뉴창을 보여주는 파트이다. 중간에 for문을 넣은 이유는 단지 익숙하게 연습하기 위해 넣은 것이다. 저렇게 하면 연산 시간이 늘어나므로 그냥 `print(""" """)`로 처리하자.

```python
menu_number = int(input("메뉴를 선택해 주세요."))
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
    elif menu_number not in menu_list:
        print("1,2,3,4 중 하나를 선택해주세요.")
        continue
    else:
        print("잘못된 메뉴 선택입니다. 다시 입력해주세요")
        continue
```
 - menu_number에서 사용자가 원하는 메뉴의 번호를 입력받는다. 만약 잘못된 번호를 입력하면 맨 밑에 elif 구문과 else에 의해 잘못된 메뉴라는 메세지가 뜨고 while문의 continue를 실행시켜 다시 메뉴 입력창으로 되돌아간다.
 - 제대로된 메뉴를 입력받으면 각 메뉴에 맞는 작업이 실행된다. 여기서 2,3번 메뉴는 클래스를 이용해야 하므로 이 작업은 내일 작성할 예정이다.