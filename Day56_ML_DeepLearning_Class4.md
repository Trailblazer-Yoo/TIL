# TIL(Today I Learned)

___

> Mar/7th/2022_Multi campus_유선종 Day55

## 신경망 클래스 구현하기 계속

### 1. softmax 역전파 함수 구현
```python
class SoftmaxWithLoss:
    def __init__(self):
        self.loss = None
        self.y = None
        self.t = None

    def forward(self, x, t):
        self.t = t
        self.y = softmax(x)
        self.loss = cross_entropy_error(self.y, self.t)
        return self.loss

    def backward(self, dout=1)
        batch_size = self.t.shape[0]
        dx = (self.y - self.t) / batch_size

    return dx
```

