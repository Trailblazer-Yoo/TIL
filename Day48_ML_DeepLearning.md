# TIL(Today I Learned)

___

> Fab/28th/2022_Multi campus_유선종 Day48

## 딥러닝
딥러닝은 최근에 AI를 개발하는데 쓰이는 알고리즘으로 우리 뇌의 뉴런의 구조를 본따서 만든 알고리즘이다. 딥러닝이 중요한 파트이기 때문에 오늘부터 계속 딥러닝에 대해 알아볼 것이다. 오늘은 딥러닝의 코드를 한번 보면서 어떤 구조로 되어있고 어떤 이론을 배워야 하는지 살펴보고 내일부터는 딥러닝에 대한 이론을 심도있게 한번 다뤄볼 생각이다.
> 딥러닝의 코드는 매우 간단하다. 그렇기 때문에 코딩이 중요한 파트가 아니라 이론이 더욱 중요한 파트이다. 그래서 앞으로는 코딩이 나오지 않을 경우가 더 많을 것이다.   
> 딥러닝에 필수적인 라이브러리는 텐서플로우인데 맥, 특히 m1에서 텐서플로우를 설치하는 작업이 여간 까다로운 것이 아니다. 설치하는 과정을 모두 다루고 싶지만 나중에 버전도 달라지고 구글링하면 나보다 더 깔끔한 설명을 하는 분들이 많기 때문에 생략하겠다.

### 1. 딥러닝 코딩
```python
from tensorflow.keras.models import Sequential                                                              #line 1
from tensorflow.keras.layers import Dense                                                                   #line 2

import numpy as np
import tensorflow as tf                                                                                     #line 3

np.random.seed(3)
tf.random.set_seed(3)

Data_set = np.loadtxt("./ThoraricSurgery.csv", delimiter = ",")
```
1. [line 1]에서 케라스에서 Sequential을 불러온다. Sequential은 딥러닝에서 하나의 틀, 빈 공간을 만든다고 생각하면 된다.
2. [line 2]에서 케라스에서 Dense를 불러온다. Dense는 딥러닝에서 뉴런 혹은 은닉층(hiden layer)을 설정해주는 명령어이다.
3. [line 3]에서 텐서플로우를 tf로 불러온다. `tf.random.set_seed(3)`처럼 기본적인 함수들을 제공을 해준다. 나머지는 우리가 데이터분석을 하던 것처럼 해주면 된다.

___

```python
X = Data_set[:, 0:17]                                                                                       #line 4
Y = Data_set[:,17]                                                                                          #line 5

model = Sequential()                                                                                        #line 6
model.add(Dense(30, input_dim = 17, activation = 'relu'))                                                   #line 7
model.add(Dense(1, activation = 'sigmoid'))                                                                 #line 8

model.compile(loss = 'binary_crossentropy', optimizer = 'adam', metrics = ['accuracy'])                     #line 9
model.fit(X,Y,epochs = 100, batch_size = 10)                                                                #line 10
print("\n Accuracy: %.f4" %(model.evaluate(X,Y)[1]))                                                        #line 11
```
1. [line 4]에서 입력변수(feature)들을 설정해줘야 한다. 여기서는 1열부터 16열까지가 입력변수이다.
2. [line 5]에서 목표변수(label)를 설정해준다.
3. [line 6]에서 `Sequential()`를 이용해 틀을 만들어준다.
4. [line 7]에서 `add`매서드를 이용해서 틀 안에 우리가 설정하고자 하는 딥러닝을 넣는다. 이때, Dense를 사용한다.
    - `Dense([신경망 갯수], [설명변수 갯수], [활성화 함수])`를 설정해줘야 한다. 활성화함수는 가중치를 결정해주는 함수이다.
5. [line 8]에서 `Dense`를 이용해 하나의 신경망을 갖는 시그모이드 함수를 이용해 1과 0 값을 출력한다. 이를 이용해 실제 y값과 일치하는지를 비교할 예정이다.
6. [line 9]에서 `model.compile`을 이용해서 손실함수, 옵티마이저(최적화 프로그램), 모델 성능 평가를 설정해준다. 여기서는 각각 이진 엔트로피, 아담, 정확도를 설정했다.
7. [line 10]에서 모델을 훈련시키는데 `epochs` 속성은 모델 훈련을 몇번 반복할지를 설정하고, batch_size는 몇개로 쪼갤 것인가를 설정한다.
   - 예를 들어 500개의 데이터를 돌리는데 원래는 500개의 데이터를 한꺼번에 돌리지만 batch_size가 10이라면 50개씩 10번을 돌리게 된다.
8. [line 11]에서 `model.evaluate(X,Y)`를 통해 평과결과를 출력해준다. 출력결과는 다음과 같다.

<img src="https://user-images.githubusercontent.com/97590480/155992590-d871f20b-d6c8-4ef7-b08e-1b36b5407f0f.png">

> 100개까지 돌리고 마지막에 accuracy를 출력해준다.

___
지금까지 코드는 몇줄 작성하지 않았다. 그렇지만 그 안에 들어있는 이론은 어마어마하다. 그렇다면 우리가 모르는 내용들을 한번 정리해보자.
1. 대충 코드는 봤지만 어떤 흐름으로 학습이 되는지 알아봐야 한다.
2. activation(활성화함수)에 대한 정의와 relu, sigmoid 방법에 대해서 알아봐야 한다.
3. 손실함수는 규제가 있는 회귀에서 릿지나 라쏘에서 개념을 알지만 binary_crossentropy(이진 엔트로피)방법에 대해 좀더 알아봐야 한다.
4. optimizer(최적화 프로그램)에 대한 개념과 adam 방법에 대해서 알아봐야 한다.
- 즉, 우리는 활성화함수, 손실함수, 최적화 프로그램에 대해서 알아봐야 하고 신경망 모형에 대한 이해가 필요하다. 다음부터는 이에 대해 자세히 알아보겠다.