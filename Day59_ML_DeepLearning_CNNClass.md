# TIL(Today I Learned)

___

> Mar/11th/2022_Multi campus_유선종 Day59

## 합성곱 신경망(CNN) 클래스 구현
합성곱 신경망은 크게 Conv, relu, 풀링 층으로 구성되어 있다. relu는 구현을 했으므로 나머지 Colv와 풀링 층을 구현해보겠다.

### 1. Conv(합성곱 계층)

#### 1. 4차원 배열
```python
x = np.random.rand(10, 1, 28, 28)                                                       #line 1
x[0]. shape # (1, 28, 28)                                                               #line 2
x[1]. shape # (1, 28, 28)
```

CNN에서는 4차원 데이터를 다루므로 4차원의 형태의 array 형태를 다뤄야 한다.
1. [line 1]에서 무작위의 (높이, 너비, 채널) = (28, 28, 1)인 데이터 10개를 생성한다.
2. [line 2]에서 [0]과 [1]의 데이터는 모두 (높이, 너비, 채널) = (28, 28, 1)인 데이터이다.
3. 만약 첫번째 데이터의 첫 채널의 공간 데이터의 접근하고자 한다면 x[0][0]을 입력하면 된다.

#### 2. 계층 구현
```python
class Convolution:
    def __init__(self, w, b, stride = 1, pad = 0):
        self.w = w
        self.b = b
        self.stride = stride
        self.pad = pad

    def forward(self, x):
        FN, C, FH, FW = self.w.shape
        N, C, G, W = x.shape
        out_h = int(1 + (H + 2*self.pad - FH) / self.stride)
        out_w = int(1 + (W + 2*self.pad - FW) / self.stride)

        col = im2col(x, FH, FW, self.stride, self.pad)
        col_W = self.w.reshape(FN, -1)
        out = np.dot(col, col_w) + self.b

        out = out.reshape(N, out_h, oout_w -1).transpose(0, 3, 1, 2)

        return out
```
1. 여기서는 저자의 함수인 im2col이 있는데, 이는 3차원 혹은 4차원 데이터를 2차원으로 줄이는 함수이다.
2. 위의 Conv 층의 핵심은 __차원__ 이다. 계산 과정에서 4차원을 2차원으로 변형해서 계산하고 이를 다시 4차원으로 출력해주기 때문에 차원을 잘 맞춰주는 것이 중요하다.

### 2. 풀링 계층
풀링은 max pooling 과 average pooling이 있지만 대체로 max pooling을 사용하기 때문에 max pooling을 구현해보고자 한다.

```python
class Pooling:
    def __init__(self, pool_h, pool_w, stride = 1, pad = 0)
        self.pool_h = pool_h
        self.pool_w = pool_w
        self.stride = stride
        self.pad = pad

    def forward(self, x):
        N, C, H, W = x.shape
        out_h = int(1 + (H - self.pool_h) / self.stride)
        out_w = int(1 + (w - self.pool_w) / self.stride)

        col = im2col(x, self.pool_h, self.pool_w, self.stride, self.pad)
        col = col.reshape(-1, self.pool_h * self.pool_w)

        out = np.max(col, axis = 1)

        out = out.reshape(N, out_h, out_w, C).transpose(0, 3, 1, 2)

        return out
```
1. 풀링 계층은 입력 데이터를 2차원으로 전개하고 그 중에서 행별 최댓값을 구하여 1차원의 데이터를 다시 3차원의 데이터로 바꿔준다.
2. 아래 이미지를 보면 더욱 이해가 쉽다.

<img src="https://user-images.githubusercontent.com/97590480/157880865-2fef4688-de56-4c59-af7d-ffdc30120ff3.png">
