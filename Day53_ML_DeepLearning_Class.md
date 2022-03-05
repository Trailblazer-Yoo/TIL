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
