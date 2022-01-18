# 초기값 설정
owner = '홍길동'
amount = 0
menu_list = [1,2,3]
init_password = 1234
password_switch = 1
password_correct = 1

# 클래스 설정

class CAccount:
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
            else: print('정확한 금액을 입력하세요.')
    def withdraw(self):
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
            
while True:
    print(f'{owner} 통장')
    print("-"*30)
    for i in range(1,len(menu_list)+2):
        list = ('잔액확인', '입금','출금','종료')
        print('{0}. {1}'.format(i,list[i-1]))
    print("="*30)
    menu_number = int(input("메뉴를 선택해 주세요. "))
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
        if menu_number in menu_list:
            if menu_number == 1:
                print(f' 1번선택 : 잔액은 {amount}입니다.')
                password_switch = 0
            elif menu_number == 2:
                number2 = CAccount(amount)
                amount = number2.deposit()
                password_switch = 0
            elif menu_number == 3:
                number3 = CAccount(amount)
                amount = number3.withdraw()
                password_switch = 0
        else:
            print("1,2,3,4 중 하나를 선택해주세요.")


