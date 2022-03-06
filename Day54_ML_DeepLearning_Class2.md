# TIL(Today I Learned)

___

> Mar/6th/2022_Multi campus_유선종 Day54

## 신경망 클래스 구현하기 계속

### 1. 기울기 함수 구현
기울기 함수를 구현하기 위해서는 중심 차분과 편미분을 구현해야 한다.

#### 1. 중심 차분
중심차분은 원래 차분의 정의인 (f(x+h) - f(x)) / h 를 할 경우에 컴퓨터에서는 매우 작은 값의 계산이 잘 이루어지지 않아서 이론과는 차이가 존재하는 미분값을 출력한다. 이를 해결하기 위해 중심 차분을 통해 어느정도 이론과 비슷한 차분을 구할 수 있다.
```python
def numerical_diff(f, x):
    h = 1e-4
    return (f(x+h) - f(x-h)) / (2*h)
```

#### 2. 편미분
편미분은 f(x) = x1 + x2 + x3 + ... 등 f(x)가 여러 변수들로 이루어졌을때, 이를 x1에 대해서 미분한 것을 x1에 대한 편미분이라 한다. 우선 f(x) = x0^2 + x1^2를 구현하면 다음과 같다.

```python
def function_2(x):
    return x[0]**2 + x[1]**2
    return np.sum(x**2)
```
> 둘 중에 아무거나 사용해도 괜찮다.

이번에는 편미분을 구현해보겠다.
```python
def numerical_gradient(f,x):
    h = 1e-4
    grad = np.zeros_like(x)                                                         #line 5

    for index in range(x.size):                                                     #line 6
        tmp_val = x[index]
        x[index] = tmp_val + h
        fxh1 = f(x)
        
        x[index] = tmp_val - h
        fxh2 = f(x)

        grad[index] = (fxh1 - fxh2) / (2 * h)
        x[index] = tmp_val
        grad[index] = (fxh1 - fxh2) / (2 * h)
    
    return grad

print(numerical_gradient(function_2, np.array([3.0, 4.0])))
#############
[6.,8.]
```
1. [line 5]에서 0으로 이루어진 영행렬을 x의 크기에 맞게 만들어서 편미분 값들이 들어갈 공간을 만들어준다.
2. [line 6]에서 for문을 이용해 각각의 편미분을 구해서 출력해준다.
3. 만약, 기울기 값에 마이너스(-1)를 붙여주면 아래와 같은 그림처럼 표시할 수 있다.

<img src="https://user-images.githubusercontent.com/97590480/156914684-e2a37b5e-983b-4077-9207-5f5eeacf7909.png">

- 위의 그림에서 화살표가 가리키는 흰색 부분이 편미분의 값이 가장 작은 부분을 가리킨다.
- 편미분의 값이 가장 작은 지점은 함수값의 최대값 or 최소값을 의미한다. 
- 이는 경사 하강법을 통해서 위의 편미분의 값이 가장 작은 지점을 구한다.

### 2. 경사하강법
```python
def gradient_descent(f, init_x, lr = 0.01, step_num = 100):
    x = init_x

    for i in range(step_num):
        grad = numerical_gradient(f, x)
        x -= lr * grad

    return x
```
f는 최적화하려는 함수, init_x는 초기값, lr은 learning rate(학습률)로 이동 보폭을 의미하며, step_num은 경사법에 따른 반복 횟수를 의미한다.

```python
def function_2(x):
    return x[0]**2 + x[1]**2

init_x = np.array([-3.0, 4.0])
gradient_descent(function_2, init_x=init_x, lr=0.1, step_num=100)
```

<img src="https://user-images.githubusercontent.com/97590480/156915085-4d71de8a-0318-4519-8044-28cf878594f1.png">

위의 코드를 실행하면 위의 이미지처럼 0에 가까운 값이 나오는 것을 확인함으로써 최저점인 것을 확인할 수 있다.

#### 학습률에 따른 결과
만약 학습률이 너무 크거나 너무 작으면 좋지 않은 결과가 나타난다. 예시를 통해 확인하자.

```python
gradient_descent(function_2, init_x=init_x, lr=10.0, step_num=100)
gradient_descent(function_2, init_x=init_x, lr=1e-10, step_num=100)
```

<img src="https://user-images.githubusercontent.com/97590480/156915592-d5f2ba52-f69b-4766-b915-5994c025a799.png">

<img src="https://user-images.githubusercontent.com/97590480/156915602-575521fd-7bd8-43ab-a75e-9336aea4cd71.png">

1. 학습률이 너무 클 경우 큰 값으로 발산하게 된다.
2. 반면에, 학습률이 너무 작으면 최솟값까지 진행되지 않고 중간에 갱신이 끝나게 되버린다.

### 3. 2층 신경망 클래스 구현
```python
class TwoLayerNetwork:
    def __init__(self, input_size, hidden_size, output_size, weight_init_std=0.01):
        self.params = {}
        self.params['W1'] = weight_init_std * np.random.randn(input_size, hidden_size)
        self.params['b1'] = np.zeros(hidden_size)
        self.params['W2'] = weight_init_std * np.random.randn(input_size, hidden_size)
        self.params['b2'] = np.zeros(output_size)

    def sigmoid(self,x):                                                
        return 1/ (1 + np.exp(-x))

    def softmax(self,x):
        exp_x = np.exp(x)
        sum_exp_x = np.sum(exp_x)
        return exp_x / sum_exp_x

    def predict(self, x):
        W1, W2 = self.params['W1'], self.params['W2']
        b1, b2 = self.params['b1'], self.params['b2']

        a1 = np.dot(x, W1) + b1
        z1 = sigmoid(a1)
        a2 = np.dot(z1, W2) + b2
        y = softmax(a2)

        return y
    
    def cross_entropy_error(self, y, t):
        if y.ndim == 1:                                                              
            t = t.reshape(1, t.size)                                                  
            y = y.reshape(1, y.size)

        batch_size = y.shape[0]                                                       

        return -np.sum(np.log(y[np.arange(batch_size), t] + 1e-7)) / batch_size 

    def loss(self, x, t):
        y = self.predict(x)
        
        return cross_entropy_error(y, t)
    
    def accuracy(self, x, t):
        y = self.predict(x)
        y = np.argmax(y, axis = 1)
        t = np.argmax(t, axis = 1)

        accuracy = np.sum(y == t) / float(x.shape[0])
        return accuracy

    def numericalgradient(self, f, x):
        h = 1e-4
        grad = np.zeros_like(x)                                                

        for index in range(x.size):                                                   
            tmp_val = x[index]
            x[index] = tmp_val + h
            fxh1 = f(x)

            x[index] = tmp_val - h
            fxh2 = f(x)

            grad[index] = (fxh1 - fxh2) / (2 * h)
            x[index] = tmp_val
            grad[index] = (fxh1 - fxh2) / (2 * h)

        return grad

    def numerical_gradient(self, x, t):
        loss_W = lambda W: self.loss(x, t)

        grads = {}
        grads['W1'] = numericalgradient(loss_W, self.params['W1'])
        grads['b1'] = numericalgradient(loss_W, self.params['b1'])
        grads['W2'] = numericalgradient(loss_W, self.params['W2'])
        grads['b2'] = numericalgradient(loss_W, self.params['b2'])

        return grads
```
1. 위의 클래스는 여태까지 배운 함수들을 모아서 종합적으로 구현한 2층 신경망 학습 클래스이다.
2. 하나하나 뜯어보면 우리가 배운 내용이기 때문에 특별할 것은 없다. 훈련 데이터를 통해 예측으로 학습을 하고 교차 엔트로피로 손실함수를 구한 후, 손실 함수에 따른 가중치를 `numerical_gradient`에서 업데이트 해주는 작업을 진행한다.

### 4. 미니배치 학습 구현
```python
train_loss_list = []

iters_num = 10000
train_size = x_train.shape[0]
batch_size = 100
learning_rate = 0.1

network = TwoLayerNetwork(input_size=784, hidden_size=50, output_size=10)

for i in range(iter_num):
    batch_mask = np.random.choice(train_size, batch_size)
    x_batch = x_train[batch_mask]
    t_batch = t_train[batch_mask]

    grad = network.numerical_gradient(x_batch, t_batch)

    for key in ('W1', 'b1', 'W2', 'b2'):
        network.params[key] -= learning_rate * grad[key]

    loss = network.loss(x_batch, t_batch)
    train_loss_list.append(loss)
```
- 여기서 batch size만큼 나눠서 for문을 진행하는 것을 볼 수 있다.

