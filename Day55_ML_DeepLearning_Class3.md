# TIL(Today I Learned)

___

> Mar/7th/2022_Multi campus_유선종 Day55

## 신경망 클래스 구현하기 계속
오차 역전파 학습에 대해 구현해보겠다.

### 1. 곱셈 계층
```python
class MulLayer:
    def __init__(self):
        self.x = None
        self.y = None

    def forward(self, x, y):
        self.x = x
        self.y = y
        out = x * y

        return out
    
    def backward(self, dout):
        dx = dout * self.y
        dy = dout * self.x

        return dx, dy
```
1. 곱셈에 대한 역전파 알고리즘은 미분값(dout)에 순전파와 정반대의 변수(순전파 변수가 x라면 역전파는 y)를 곱한 것을 변화분으로 갖는다.
2. 사과의 예시로 코드를 실행해보면 다음과 같다.

```python
apple = 100
apple_num = 2
tax = 1.1

mul_apple_layer = MulLayer()
mul_tax_layer = MulLayer()

### 순전파
apple_price = mul_apple_layer.forward(apple, apple_num)
price = mul_tax_layer.forward(apple_price, tax)

### 역전파
dprice = 1
dapple_price, dtax = mul_tax_layer.backward(apple, apple_num)
dapple, dapple_num = mul_apple_layer.backward(dapple_price)

print(price) # 220
print(dapple, dapple_num, dtax) # 2.2, 110, 200
```
1. 역전파를 실행하면 지불 금액당 사과 가격의 미분값인 2.2가 나오는 것을 확인할 수 있다.

### 2. relu 역전파 구현
```python
class Relu:
    def __init__(self):
        self.mask = None

    def forward(self, x):
        self.mask = (x <= 0)
        out = x.copy()
        out[self.mask] = 0

        return out
    
    def backward(self, dout):
        dout[self.mask] = 0
        dx = dout

        return dx
```
1. relu 함수는 입력값이 x > 0 이면 출력값을 x로, 입력값이 x <= 0 이면 출력값을 0으로 받아주는 함수이다.
2. 이를 y에 대한 미분값을 구하면 x > 0 이면 dy/dx = 1, x <= 0 이면 dy/dx = 0 이다.
3. 순전파에서 `dout[self.mask]`의 값이 0으로 정해지므로 역전파에서 해당 `dout[self.mask]` 값은 0이 된다.

### 3. Sigmoid 역전파 구현
```python
class Sigmoid:
    def __init__(self):
        self.out = None

    def forward(self, x):
        out = 1/ (1 + np.exp(-x))
        self.out = out
    
        return out

    def backward(self, dout):
        dx = dout * (1.0 - self.out) * self.out

        return dx
```
1. sigmoid 함수는 y = 1 / (1 + exp(-x))이다. 차근차근 미분해보자.
2. 분수의 미분은 dy/dx = - 1/x^2 = -y^2 이다. 따라서 출력값 L을 미분한 dL/dy에 -y^2를 곱해주면 -dL/dy * y^2이다.
3. 1 + exp(-x)에서 1을 미분하면 0이므로 그래도 전달된다.
4. 자연 상수 e의 미분은 그대로 e이므로 역전파 신호는 -dL/dy * y^2 * exp(-x)이다.
5. 또한, exp(-x)의 미분은 -exp(-x)이므로 위에서 마이너스를 곱해주면 dL/dy * y^2 * exp(-x)이다.

<img src="https://user-images.githubusercontent.com/97590480/157054340-98dd2c54-bc93-4c8f-8894-01897e383370.png">

> 이를 이미지로 보면 다음과 같다.

6. 위의 미분식을 간단히 하면 다음과 같다.

<img src="https://user-images.githubusercontent.com/97590480/157054551-10b3b44b-1687-4d03-b273-9e1520a7d681.png">

