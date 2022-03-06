# TIL(Today I Learned)

___

> Mar/5th/2022_Multi campus_유선종 Day53

## 신경망 클래스 구현하기
지금까지 배운 내용을 가지고 신경망 학습을 구현해보도록 하겠다.

### 1 3층 신경망 구현
```python
import numpy as np

def init_network():                                                         #line 1
    network = {}
    network['b1'] = np.array([0.1,0.2,0.3])
    network['W1'] = np.array([0.1,0.3,0.5], [0.2,0.4,0.6])      
    network['b2'] = np.array([0.1,0.2])
    network['W2'] = np.array([0.1,0.4], [0.2,0.5], [0.3,0.6])     
    network['b3'] = np.array([0.1,0.2])  
    network['W3'] = np.array([0.1,0.3], [0.2,0.4])

    return network

def sigmoid(x):                                                             #line 2
    return 1/ (1 + np.exp(-x))

def identity_function(x):                                                   #line 3
    return x

def forward(network, x):                                                    #line 4
    W1, W2, W3 = network['w1'], network['w2'], network['w3']
    b1, b2, b3 = network['b1'], network['b2'], network['b3']

    a1 = np.dot(x, W1) + b1
    z1 = sigmoid(a1)
    a2 = np.dot(z1, W2) + b2
    z2 = sigmoid(a2)
    a3 = np.dot(z2, W3) + b3
    y = identity_function(a3)

    return y

network = init_network()
x = np.array([1.0, 0.5])
y = forward(network, x)
print(y)
#########
[0.31682708, 0.69627909]
```

1. [line 1]에서 `init_network`함수는 가중치와 편향 값을 설정하는 함수이다. 3층 신경망이므로 w1, w2, w3까지 설정한다.
2. [line 2]에서 시그모이드 함수를 설정한다.
3. [line 3]에서 항등함수를 설정한다.
4. [line 4]에서 순전파 3층 신경망을 구현한다. 단지 행렬의 곱으로만 이루어진 것 뿐이다.

### 2. 소프트맥스 함수 구현
```python
def softmax(x):
    exp_x = np.exp(x)
    sum_exp_x = np.sum(exp_x)
    return exp_x / sum_exp_x

def softmax_overflow(x):
    c = np.max(x)
    exp_x = np.exp(x-c)
    sum_exp_x = np.sum(exp_x)
    return exp_x / sum_exp_x
```
1. 위의 소프트맥스는 각 출력값의 비중으로 바꿔줌으로써 우리가 아는 확률값으로 바꿔주는 소프트맥스 함수이다.
2. 아래의 소프트맥스 함수는 너무 작은 값일때 컴퓨터가 계산하지 못하는 overflow문제를 해결하기 위해 최댓값으로 보정해주는 소프트맥스 함수이다.

### 3. 배치 처리 구현
배치 처리는 수많은 데이터를 처리하다보면 병목현상이 발생하여 몇개씩 쪼개서 계산하는 것을 말한다. 묶음(batch)으로 데이터를 처리한다고 생각하면 좋다.

```python
x, t = get_data()
network = init_network()

batch_size = 100
accuracy_cnt = 0

for i in range(0, len(x), batch_size):
    x_batch = x[i:i+batch_size]
    y_batch = predict(network, x_batch)
    p = np.argmax(y_batch, axis = 1)
    accuracy_cnt = np.sum(p == t[i:i+batch_size])
```
여기서 중요한 것은 `range(0,len(x), batch_size)`이다. range 함수에서 0부터 len(x)까지 batch_size만큼 간격으로 숫자를 생성하므로 for문을 묶음으로 나눠서 계산해준다.

### 4. 교차 엔트로피 구현
```python
def cross_entropy_error(y, t):
    delta = 1e-7
    return -np.sum(t * np.log(y + delta))

t = [0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
y = [0.1, 0.05, 0.6, 0.0, 0.05, 0.1, 0.0, 0.1, 0.0, 0.0]
cross_entropy_error(np.array(y), np.array(t))
#######
0.51082545709933802
y = [0.1, 0.05, 0.1, 0.0, 0.05, 0.1, 0.0, 0.6, 0.0, 0.0]
cross_entropy_error(np.array(y), np.array(t))
#######
2.3025840929945458
```
1. t는 정답 레이블이다. 교차 엔트로피는 정답 레이블에 해당하는 확률에 따라 정보량을 계산해주는 함수이다.
2. 위에서 정답 레이블에 해당하는 확률은 0.6, 아래에서는 0.1이다. 확률이 높으면 새롭게 얻는 정보량이 낮으므로 교차 엔트로피 값이 낮고, 확률이 낮으면 새롭게 얻는 정보량이 높으므로 교차 엔트로피 값이 높은 것을 확인할 수 있다.

___

### 5. 배치용 교차 엔트로피 구현
신경망을 배치 처리를 해준다면 교차 엔트로피도 이에 맞게 설정해줘야 한다.

```python
def cross_entropy_error(y, t):
    if y.ndim == 1:                                                                 #line 1
        t = t.reshape(1, t.size)                                                    #line 2
        y = y.reshape(1, y.size)
    
    batch_size = y.shape[0]                                                         #line 3
    return -np.sum(np.log(y[np.arange(batch_size), t] + 1e-7)) / batch_size         #line 4
```
1. [line 1]에서 nump의 `ndim` 매서드를 이용하여 y가 1차원 벡터일 경우에 y와 t의 차원을 바꿔주는 조건문의 형태이다.
2. [line 2]에서 `reshape` 매서드를 사용하는데, 이를 이용하여 차원을 바꿔준다.
3. [line 3]에서 `y.shape[0]`을 이용해 [행, 열] 중에서 행의 갯수(데이터의 갯수)를 배치 사이즈로 설정해준다.
4. [line 4]에서 `np.log(y[np.arange(batch_size), t])`는 `np.arange(batch_size)`로 [0,1,2,...,batch_size]의 리스트를 생성하고 t는 정답 레이블이 저장되어 있으므로 y[batch_size, t]으로 인덱싱하여 해당 위치에 있는 y의 요소값을 받는다. 예를들어, t = [0,0,1,0,0]이라면 y 행렬에서 1열의 데이터 4개, 2열의 데이터 1개를 가져온다.
___

### numpy reshape 함수
reshape 함수에 대해서 상세히 서술하겠다.
#### 1. 1차원을 2차원으로 변환
```python
import numpy as np
vector = np.array([1,2,3,4,5,6,7,8])
print(vector.reshape(2,4))
print(np.reshape(vector, (4,2)))
```

<img src="https://user-images.githubusercontent.com/97590480/156909864-775e9e3a-abb6-4aed-933a-c4e156c89d2c.png">

위의 코드를 실행하면 위와 같은 결과가 나온다. `reshape(2,4)`에서 2는 행의 갯수, 4는 열의 갯수이다.
> 만약 vector가 [1,2,3,4,5,6,7,8]의 리스트 형태라면 `vector.reshape`는 `numpy.ndarray` 타입만 가능하므로 리스트 형태는 오류가 발생한다. 하지만 `np.reshape((vector), (4,2))`는 리스트 형태도 사용이 가능하므로 데이터 타입에 신경을 쓰기 싫다면 아래처럼 작성해주면 좋다.

___

#### 2. 1차원을 3차원 변환
```python
vector = np.arange(1,9)
print(vector.reshape(2,2,2))
```

<img src="https://user-images.githubusercontent.com/97590480/156909954-f77e4499-cf89-4dcd-b6d2-1d579145f264.png">

1. 1차원을 3차원으로 변환하고 싶다면 `reshape(2,2,2)`처럼 속성을 하나 더 설정해주면 된다. 
2. `np.arange(1,9)`는 `range(1, 9)` 함수와 동일한 역할을 해주는데, 타입을 `numpy.ndarray`로 받는다.
3. 출력 결과를 보면 '\n'를 통해 3차원 데이터라는 것을 표시해주고 있다.

___

#### 3. reshape(-1)의 의미
가끔 `reshape(-1, 3)`처럼 -1이 들어간 코드를 볼 수 있다. 그 의미를 간단히 설명하겠다.

```python
vector = np.arange(1,13)
print(vector.reshape(-1, 2))
```

<img src="https://user-images.githubusercontent.com/97590480/156910090-09eaab67-081d-4cc8-a6f8-40b0d38ad267.png">

`reshape(-1, 2)`는 2개의 열로 행을 자동적으로 조정해준다. 만약, 열은 우리가 정한대로 지정하되, 행이 얼마나 들어올지 모르겠다면 행을 -1로 설정해주면 알아서 행을 조절해준다. 이는 열 속성에 -1을 설정해줘도 동일하다.

```python
print(vector.reshape(-1))
print(vector.reshape(1,-1))
```

<img src="https://user-images.githubusercontent.com/97590480/156910165-657c9606-14a7-48bc-98b9-4e01311e5ddc.png">

1. `reshape(-1)`의 출력결과를 보면 1차원 배열을 반환하는 것을 볼 수 있다.
2. 반면에, `reshape(1, -1)`은 `reshape(-1)`과 동일한 형태의 배열을 보이지만 2차원 배열을 반환하는 것을 확인할 수 있다.
