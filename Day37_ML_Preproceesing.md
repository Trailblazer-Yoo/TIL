# TIL(Today I Learned)

___

> Fab/17th/2022_Multi campus_유선종 Day37

## 머신러닝 - 데이터 전처리
데이터를 분석하기 위해서는 데이터를 적절히 재가공을 시켜야한다. 예를 들어 남자와 여자를 구분하고 싶고 이를 데이터 분석에 사용하고 싶다면 남자를 1로 여자를 0으로 더미 변수를 설정해줄 수 있을 것이다. 이런 식으로 분석을 실시하기 전에 데이터를 가공하는 것을 데이터 전처리(preprocessing)라고 한다.

### 1. 라벨인코딩(label encoding)
라벨 인코딩은 데이터를 라벨 데이터로 변환시켜주는 작업을 말한다. 라벨은 데이터를 분류할때 목표가 되는 데이터를 의미한다. 일반적인 데이터를 라벨 데이터로 바꾸는 방법은 고유한 숫자로 바꿔주면 된다. 혹은 행렬의 위치값으로 변환해주면 된다. 아래 예시를 보자.

```python
from sklearn.preprocessing import LabelEncoder                                                              #line 1

items = ['TV', '냉장고', '전자레인지', '컴퓨터', '선풍기', '선풍기', '믹서','믹서']                                     #line 2

encoder = LabelEncoder()                                                                                    #line 3
encoder.fit(items)                                                                                          #line 4
labels = encoder.transform(items)                                                                           #line 5
print('인코딩 변환값 : ', labels)

print('인코딩 클래스 : ', encoder.classes_)
print('디코딩 원본값 : ', encoder, encoder.inverse_transform([4,5,2,0,1,1,3,4,2]))
```

<img src="https://user-images.githubusercontent.com/97590480/154490597-9a7b0a00-3e1b-4eb3-912e-a69a39b508bc.png">

1. [line 1]에서 라벨 인코딩을 위해 `LabelEncoder`를 불러온다.
2. [line 2]에서 라벨로 바꿔줄 목표 데이터를 설정해준다. 여기서는 가전제품을 파는 회사에서 가전제품과 관련된 데이터를 가지고 분석을 실시하고자 하는 상황이다. 그러므로 가전제품의 이름을 고유한 숫자로 라벨링을 해줄 필요가 있다.
3. [line 3]에서 `LabelEncoder`클래스를 encoder 인스턴스에 담는다.
4. [line 4]에서 라벨링할 데이터를 encoder 인스턴스에 적용시킨다.
5. [line 5]에서 `.tansform` 매서드를 이용하면 알아서 각 데이터에 고유한 숫자로 바꿔준다. 위의 이미지에서 각 제품에 해당하는 숫자를 확인할 수 있다.
___

### 2. 원핫 인코더
원핫 인코더는 위에서처럼 고유한 숫자로 라벨링을 하는 것이 아니라 0과 1의 숫자만 사용하여 행렬로 변환한다. 예시를 보자.

```python
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
import numpy as np

items = ['TV', '냉장고', '전자레인지', '컴퓨터', '선풍기', '선풍기', '믹서','믹서']

encoder = LabelEncoder()
encoder.fit(items)
labels = encoder.transform(items)

labels = labels.reshape(-1,1)                                                                               #line 6
print(labels)

oh_encoder = OneHotEncoder()                                                                                #line 7
oh_encoder.fit(labels)
oh_labels = oh_encoder.transform(labels)                                                                    #line 8
print('원-핫 인코딩 데이터')
print(oh_labels.toarray())
print('원-핫 인코딩 데이터 차원')
print(oh_labels.shape)
```

<img src="https://user-images.githubusercontent.com/97590480/154491801-a7694607-23a6-4353-a6c3-951474f2d408.png">

1. [line 6]에서 reshape 매서드는 해당 데이터를 행렬로 바꿔주는 역할을 한다. 즉, `reshape(-1,1)`를 입력하면 행은 무제한으로 입력이 가능하고 열은 1열만 입력이 가능하다. 이렇게 입력하면 위의 이미지처럼 N행 1열의 행렬이 나온다.
2. [line 7]에서 `OneHotEncoder`클래스를 oh_encoder 인스턴스에 담아준다.
3. [line 8]에서 라벨링할 데이터를 변환시켜준다.
4. 위의 이미지를 보면 1열이 'TV', 2열이 '냉장고', 3열이 '믹서', 4열이 '선풍기', 5열이 '전자레인지', 6열이 '컴퓨터'를 의미한다. 만약 TV데이터라면 1열에 1을, 나머지 열에는 0을 입력함으로써 해당 행이 TV데이터라는 것을 알 수 있다. 

```python
import pandas as pd

df = pd.DataFrame({'item' : ['TV', '냉장고', '전자레인지', '컴퓨터', '선풍기', '선풍기', '믹서', '믹서']})
pd.get_dummies(df)
```

1. 위의 코드는 판다스를 이용해서 원핫 인코딩을 하는 방법이다.
2. 8행 1열의 데이터프레임 형태의 데이터가 df에 담긴다.
3. `get_dummies` 매서드를 이용하면 동일한 0과 1로 이루어진 행렬이 만들어진다.

### 3. 비율 조정
비율(Scale)조정은 서로 다른 두 데이터의 비율이 동일하게 되도록 조정해주는 것을 의미한다. 예를 들어, 0에서 100까지의 정수 데이터와 0에서 50까지의 정수 데이터가 있다고 하자. 이 경우에 동일한 50이라는 숫자값이더라도 첫번째 데이터에서는 중간값이고 두번째 데이터에서는 가장 큰 혹은 마지막 값이다. 이 경우에 동일한 50으로 비교를 하는 것을 적절하지 않을 것이다. 비교를 위해 상대적인 값으로 바꿔줘야 하는데 이때 사용하는 것이 비율 조정이다.

```python
from sklearn.preprocessing import MinMaxScaler                                                              #line 9
import numpy as np

train_array = np.arange(0,11).reshape(-1,1)                                                                 #line 10
test_array = np.arange(0,6).reshape(-1,1)                                                                   #line 11
scaler = MinMaxScaler()
scaler.fit(train_array)
train_scaled = scaler.transform(train_array)                                                                #line 12

print('원본 train_array 데이터 : ', np.round(train_array.reshape(-1),2))
print('Scale된 train_array 데이터 : ', np.round(train_scaled.reshape(-1), 2))
```

<img src="https://user-images.githubusercontent.com/97590480/154499981-2faedf79-6dc0-419e-8326-8550bc554bdd.png">

1. [line 9]에서 `MinMaxScaler`를 불러온다.
2. [line 10]에서 0에서 10까지의 데이터를 10행 1열의 벡터로 표현한다.
3. [line 11]에서 0에서 5까지의 데이터를 5행 1열의 벡터로 표현한다.
4. [line 12]에서 0에서 10까지의 데이터를 최대값이 1이 되는 비율 데이터로 표현한다. 위의 이미지를 보면 5가 0.5인 비율 데이터로 바뀐 것을 알 수 있다.

```python
test_scaled = scaler.transform(test_array)

print('원본 test_array 데이터 : ', np.round(test_array.reshape(-1),2))
print('Scale된 test_array 데이터 : ', np.round(test_scaled.reshape(-1), 2))
```

<img src="https://user-images.githubusercontent.com/97590480/154500623-6629106b-cc58-4a48-b8dc-f7edfccfb69d.png">

- 0에서 5의 데이터를 비율 데이터로 표현하면 위의 이미지처럼 표현된다. 즉, 여기서의 5는 최대값이 1이 되는 가장 높은 값이라는 것을 비율 조정을 통해 확인할 수 있다.