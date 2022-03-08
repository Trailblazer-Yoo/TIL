# TIL(Today I Learned)

___

> Mar/4th/2022_Multi campus_유선종 Day52

## 역전파 알고리즘(Back propagation)
- 역전파 알고리즘(Back propagation)은 이름에서 알수 있듯이 거꾸로 돌아가는 알고리즘을 의미한다. 
- 입력층에서 은닉층, 출력층의 순으로 진행되는 알고리즘을 순전파 알고리즘(Forward propagation)이라고 부른다.
- 반대로 출력층 혹은 은닉층의 마지막에서 다시 은닉충의 첫번째로 돌아가는 역의 진행을 역전파 알고리즘이라고 부른다. 그렇다면 역전파 일고리즘에 대해 좀더 자세히 알아보자.

### 1. 계산 그래프
우리는 역전파 알고리즘에 알기 위해서 순전파 알고리즘에 대해 알아야 한다. 하지만 순전파 알고리즘은 단지 입력층 - 은닉층 - 출력층의 순서로 진행되는 것을 의미하므로 계산 그래프를 통해 구체적인 예시로 이해도를 높여보자.

<img src="https://user-images.githubusercontent.com/97590480/156774702-93bcb6df-a746-452f-b64e-a106d1ec8c0f.png">

1. 위의 이미지는 우리가 사과를 구매할 때 지불 금액에 대한 순전파 알고리즘이다.
2. "보영이는 슈퍼에서 1개에 100원인 사과를 2개 구매하고자 한다. 이때 지불 금액은? 단, 소비세 10%는 별도로 부과된다." 라는 문제가 있다고 하자.
3. 첫번째 입력층에는 사과의 가격인 100원이 입력된다.
4. 그 다음 노드(신경망)에서는 x2 연산이 있고, 노드를 거치게 되면 100원에 x2를 해서 200원이 된다.
5. 그다음 노드에서는 소비세 10%를 나타내는 x0.1 연산이 있고, 이 노드를 거치게 되면 최종적으로 220원이라는 지불 금액이 출력된다. 흔히 우리가 문제를 푸는 과정이다.

<img src="https://user-images.githubusercontent.com/97590480/156778793-46db0825-9aac-4221-b1c4-cd59d4a38b90.png">

- 위의 이미지는 각 노드에 있는 숫자를 입력층으로 바꿔준 알고리즘이다. 은닉층의 각 노드들은 이제 곱하기 연산만 해주고 입력받은 숫자들을 곱해주기만 한다.
- 이러한 결과도 우리가 흔히 계산하는 방법과 동일하기 때문에 쉽게 이해가 될 것이다.

___

이번에는 문제를 좀더 복잡하게 해보자. 보영이가 100원짜리 사과 2개, 150원짜리 귤을 3개 샀다고 하자. 소비세는 동일할 경우에 지불 금액을 구해보자.

<img src="https://user-images.githubusercontent.com/97590480/156779416-129e7e5f-fef2-4371-a13c-ce7edd48ab33.png">

- 여기서는 은닉층이 총 3층으로, 1층에서는 사과와 귤 각각의 금액을 구해주고 2층에서 더해준뒤, 3층에서 소비세를 곱해주고 지불 금액을 구해준다.
- 문제가 복잡하다고 해서 당황할 필요없다. 단지 노드가 많아지고 층이 많아질뿐 본질은 동일하다.

### 2. 연쇄법칙
이제 역전파 알고리즘을 배울 차례인데, 역전파 알고리즘을 이해하기 위해서는 연쇄법칙을 알아야 한다. 연쇄법칙을 보기 전에 역전파 알고리즘을 찍먹 해보자.

<img src="https://user-images.githubusercontent.com/97590480/156780187-a138e5af-d292-4cbc-ac9d-6bb1aaf4e0c2.png">

1. 위의 이미지에서 순전파 알고리즘은 오른쪽을 가리키고 있는 화살표이다. 반대로 왼쪽을 가리키고 있는 화살표는 역전파 알고리즘이다.
2. 역전파 알고리즘은 출력층으로부터 입력층까지 진행하면서 __미분값__ 을 구하는 것을 말한다.
3. 출력층에서 은닉층으로 출발하는 화살표 밑에 1이 써져있는데, 이는 자기 자신에 대한 미분을 의미한다.
   - 소비세를 곱하고 난 결과를 그대로 출력층에 전달했으므로 dx/dx = 1 이다.
4. 그 다음 화살표에서 1.1은 소비세를 의미하는데, 1.1x = y 라는 식에서 1.1 * 200 = 220 의 결과가 나온 것이므로 dy/dx = 1.1이다.
5. 그 다음 화살표에서 2.2는 소비세와 사과의 갯수를 곱한 것을 의미한다. 1.1 * 200 = 1.1 * 2 * 100 이므로, 2.2 * x = y에서 dy/dx = 2.2이다.
6. 즉, 여기서 x값은 사과의 가격인 100을 의미하고 y값은 지불 금액인 220이다. 이를 미분한 결과는 2.2이다.

___

위의 계산과정을 일반화하기 위해서 연쇄법칙이 필요하다.
1. 연쇄법칙은 dy/dx = dy/dz * dz/dx 로 나눈 것이다.
2. 정확히는 합성 함수의 미분을 구할때는 합성 함수를 구성하는 각 함수의 미분의 곱으로 나타내야 되기 때문에 연쇄법칙을 사용한다.
3. 즉, 원래는 dy/dz * dz/dx를 구하기 위해 연쇄법칙이 사용되지만, 반대로 dy/dx를 dy/dz * dz/dx 처럼 바꿔서 구할 수 있다는 것을 시사한다.

<img src="https://user-images.githubusercontent.com/97590480/156782652-6633b568-8b19-4f8b-a8d6-6285485494e3.png">

1. 우리가 위에서 사과에 대한 역전파 알고리즘을 구한 방식에는 위의 이미지의 계산 과정이 숨겨져 있다.
2. 역전파 알고리즘을 따라 마지막 미분값인 dy/dy * dy/dt * dt/dx 는 약분해주면 dy/dx이다. 즉, 역전파 알고리즘은 연쇄법칙과 동일한 원리를 사용한다.

### 3. 덧셈 노드와 곱셈 노드의 역전파 알고리즘
우리는 역전파 알고리즘이 연쇄법칙을 통한 미분값을 구하는 것이라는 것을 알아냈다. 이번에는 노드가 덧셈과 곱셈일 경우의 역전파 알고리즘의 상황을 살펴보겠다.
> 뺄셈은 덧셈과, 나눗셈은 곱셈과 동일하다.

#### 1. 덧셈 노드
<img src="https://user-images.githubusercontent.com/97590480/156784011-d19b5bc6-b92a-41a4-8c45-46a6cb2e1d0d.png">

1. 위의 이미지를 보면 덧셈 노드를 거친 역전파는 x1를 해주므로 입력값과 동일하다.
2. 역전파 알고리즘에서 덧셈 노드가 있을 경우에는 이전의 입력값을 그대로 전달해준다.
3. 따라서 순전파 입력 신호값이 필요하지 않다.

#### 2. 곱셈 노드
<img src="https://user-images.githubusercontent.com/97590480/156784854-c36da829-0b70-4e36-bca1-cd3e482c5c59.png">

1. 위의 이미지를 보면 순전파일 때에는 x였던 입력층이 역전파를 거치면서 dL/dz * y로 입력을 받는 것을 볼 수 있다.
2. 즉, 순전파 입력 신호값이 __서로 바뀐__ 값을 출력한다.
3. 이렇게 순전파 입력 신호와 역전파 입력 신호가 반대되는 상황이기 때문에 곱셈 노드를 구현할 때에는 순전파 입력 신호를 저장해둔다.

### 4. 역전파 알고리즘을 사용하는 이유
1. 역전파 알고리즘을 사용하는 이유는 __계산 시간__ 때문이다.
2. 우리가 손실 함수를 구할 때 필요한 것은 각 변수의 미분값이다.
3. 그러나 각 미분값을 계산하려면 시간이 매우 오래 걸린다.
4. 하지만 역전파 알고리즘은 이러한 미분 계산 시간을 단축시켜준다. 단지 이전 노드로 이동하면서 미분값을 계산해주면 되기 때문에 국소적 미분값을 구하는 것보다 훨씬 빠르다.