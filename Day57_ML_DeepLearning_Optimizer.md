# TIL(Today I Learned)

___

> Mar/9th/2022_Multi campus_유선종 Day57

## 옵티마이저(최적화 변수)
Optimizer는 손실 함수의 값을 가능한 한 낮추는 것이 목표인 신경망 학습에서 손실 함수 값을 낮추는 매개변수의 최적값을 찾는 것을 해결해주는 방법론을 말한다. 예를 들어, 우리가 지금까지 사용해온 옵티마이저로는 확률적 경사 방법(SGD)이 있다. 매개변수의 기울기 값인 미분값을 구해 이를 갱신하면서 최적값에 다가가는 것을 SGD라고 한다.

### 1. 확률적 경사 방법(SGD)
우선 SGD를 구현해보도록 하자. SGD의 식은 w = w - l * dL/dw 이다. 즉, 가중치 w에 학습률(learning rate) l을 곱한 손실 함수의 미분값을 빼줌으로써 w = w - 0 에 가까워질 때 최적이라고 정의하는 방법이다.

```python
class SGD:
    def __init__(self, lr = 0.01):
        self.lr = lr

    def update(self, params, grads):
        for key in params.keys():
            params[key] -= self.lr * grads[key]
```
1. 위의 SGD 클래스는 SGD식을 그대로 구현한 것이다.
2. SGD는 가장 정석적인 방식이지만, 기울기가 달라지는 함수일 경우에 탐색 경로가 비효율적이라는 단점을 가지고 있다.

<img src="https://user-images.githubusercontent.com/97590480/157451195-826cdb0a-d4df-40cb-b466-50fa1b7074b8.png">

> 위의 이미지에서 지그재그로 경로를 탐색하는 것을 볼 수 있다. 이럴 경우에 움직임이 너무 비효율적이다.

3. 이를 극복하기 위해 모멘텀(momentum), 에이다 그레이드(AdaGrad), 아담(Adam)이라는 방법이 존재한다. 더 많지만 여기서는 세가지만 다룬다.

### 2. 모멘텀
모멘텀은 운동량이라는 뜻으로 SGD에 가속도라는 변수를 추가한 것이다. 식은 `W = W + av - l * dL/dw`이다. 이를 구현해보면 다음과 같다.

```python
class Momentum:
    def __init__(self, lr=0.01, momentum=0.9):
        self.lr = lr
        self.momentum = momentum
        self.v = None

    def update(self, params, grads):
        if self.v is None:
            self.v = {}
            for key, val in params.items():
                self.v[key] = np.zeros_like(val)
        
        for key in params.keys():
            self.v[key] = self.momentum * self.v[key] - self.lr * grads[key]
            params[key] += self.v[key]
```
<img src="https://user-images.githubusercontent.com/97590480/157453161-5c58a64b-eb26-4c65-80e9-7a577e4d2a3f.png">

1. 위의 이미지를 보면 처음의 SGD보다 지그재그 정도가 덜한 것을 볼 수 있다.
2. 이는 x축의 힘은 아주 작지만 방향은 변하지 않아서 한 방향으로 일정하게 가속하기 때문이다.

### 3. AdaGrad
에이다 그레이드는 학습률 값을 감소시키는 SGD이다. 학습률이 너무 높으면 발산하여 정확한 값을 찾지 못하는 반면, 너무 작으면 학습시간이 너무 길어진다. 에이다 그레이드는 처음에는 높은 학습률로 효율적으로 탐색하다가 정밀하게 탐색해야 할 때에는 학습률을 낮춰서 최적의 지점을 찾는 방법이다.

<img src="https://user-images.githubusercontent.com/97590480/157453863-b90c5968-c2dc-4b64-a877-d89681ad073b.png">

1. 위에서 h는 기울기 값을 조정해주는 변수이고, 미분값 행렬의 각 원소별 곱셈을 한 값을 더해준 값을 갱신해줘서 학습률에 나눠준다.
2. 예를들어, 현재 미분값이 너무 크다면 그만큼 큰값으로 학습률을 나눠주므로 맞춤식으로 학습률을 조정해나간다.

```python
class AdaGrad:
    def __init__(self, lr=0.01):
        self.lr = lr
        self.h = None

    def update(self, params, grads):
        if self.h is None:
            self.h = {}
            for key, val in params.items():
                self.h[key] = np.zeros_like(val)
    for key in params.keys():
        self.h[key] += grads[key] * grads[key]
        params[key] -= self.lr * grads[key] / (np.sqrt(self.h[key] + 1e-7)
```

<img src="https://user-images.githubusercontent.com/97590480/157454911-8cc5b915-30f1-45e6-baec-1ca84a46f346.png">

위의 그림을 보면 지그재그의 정도가 거의 없어진 것을 볼 수 있다.

### 4. Adam
아담은 에이다 그레이드와 모멘텀을 합친 것과 같은 모습을 보인다.

<img src="https://user-images.githubusercontent.com/97590480/157455314-ff43c3fc-7d08-4086-84a3-2927a8a62752.png">

논문에서는 AdaGrad, RMSprop, SGDNesterov, AdaDelta보다 Adam이 더 성능이 높은 것으로 나타났기 때문에 아담이 현재 가장 많이 사용되는 옵티마이저이다.