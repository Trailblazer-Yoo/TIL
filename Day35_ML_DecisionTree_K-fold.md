# TIL(Today I Learned)

___

> Fab/15th/2022_Multi campus_유선종 Day35

## 머신러닝 - 의사결정나무
오늘은 머신러닝에서 분류분석에 포함되는 의사결정나무(DecisionTree)에 대해 배울 것이다. 또한, 훈련용 데이터를 이용해서 모델을 도출할 때 평가하는 방법들 중에서 K-fold방식을 사용할 것이다.

### 1. Decision Tree(의사결정나무)
1. 의사결정나무는 머신러닝 중에서 지도학습(supervised learning)에 속하고, 지도학습은 회귀와 분류로 나뉘는데 그 중에서 분류법에 속하는 모델이다. 
2. 의사결정나무는 분류함수를 의사결정 규칙으로 이뤄진 나무 모양으로 그리는 방법이다.
3. 의사결정나무는 크게 노드(node; 마디)와 브랜치(branch; 가지)로 구성된다. 노드는 변수가 담기는 공간이라고 생각하면 되고, 브랜치는 노드에서 뻗어나가는 나뭇가지라고 생각하면 된다. 또한, depth(깊이)는 마디로 구성되는 층이 있을터인데 그 층의 수를 의미한다. 아래 사진을 보자

<img src="https://user-images.githubusercontent.com/97590480/154072490-b6b2ca03-8014-40ca-8019-738af4ecbc29.png">

> 위에서부터 3개 층이 있는 것을 알 수 있다. 그러므로 depth는 3이다. 네모난 공간들은 노드이며, 노드에서 뻗어나온 직선은 브랜치이다.
- 오늘은 결정나무에 대한 내용보다는 test 데이터를 이용해서 훈련 데이터를 평가하는 것을 중점으로 알아보고자 한다.
___
### 2. 붓꽃(iris) 품종 예측 예제
머신러닝에서 많이 사용하는 iris데이러틀 이용해서 의사결정나무의 평가 방법에 대해 배워보도록 하겠다.

#### 1. 데이터 및 라이브러리 불러오기
```python
from sklearn.datasets import load_iris                                                                      #line 1
from sklearn.tree import DecisionTreeClassifier                                                             #line 2
from sklearn.model_selection import train_test_split                                                        #line 3
from sklearn.metrics import accuracy_score                                                                  #line 4

import numpy as np                                                                                          #line 5
import pandas as pd                                                                                         #line 6

iris = load_iris()                                                                                          #line 7
iris_label = iris.target                                                                                    #line 8
print('iris target값 : ', iris_label)
print('iris target명 : ', iris.target_names)
```

<img src="https://user-images.githubusercontent.com/97590480/154081597-2136d73f-3158-4adc-a94f-9cc4d77f0f84.png">

> 0은 setosa, 1은 versicolor, 2는 virginica를 의미한다.

1. [line 1]에서 머신러닝을 분석하는데 필요한 알고리즘을 제공하는 라이브러리인 scikitlearn을 이용해서 분석을 하기 위해 라이브러리를 불러온다. 그 중에서도 `sklearn.datasets` class 안에 있는 `load_iris` 매서드를 불러온다.
2. [line 2]에서 `sklearn.tree`에 담긴 의사결정나무에 관한 매서드인 `DecisionTreeClassifier`을 불러온다.
3. [line 3]에서 `sklearn.model_selection`에 담긴 `train_test_split` 매서드를 불러온다. 이 매서드는 훈련용 데이터와 테스트용 데이터를 랜덤하게 알아서 분리해주는 매서드이다.
4. [line 4]에서 `sklearn.metrics`에 담긴 `accuracy_score` 매서드를 불러온다. 이 매서드는 훈련용 데이터를 학습하여 만든 모델이 적절한지 테스트 데이터로 평가하는데 사용하는 매서드이다.
5. [line 5]에서 행렬 연산을 위한 `numpy`를 불러와 np에 담아준다.
6. [line 6]에서 행렬 표현으로 만들어주기 위한 `pandas`를 불러와 pd에 담아준다.
7. [line 7]에서부터 데이터 분석이 시작된다. 우선 `load_iris()`를 통해 붓꽃 데이터를 불러온다.
8. [line 8]에서 `iris.target`을 `iris_label`에 담아준다. 여기서 target은 우리가 구하고자 하는 답이 있는 변수를 의미하며, y값같은 종속변수와 비슷하다고 보면 된다. label은 붓꽃의 종류를 구분해주는 데이터인데, 여기서 우리가 구하고자 하는 것이 붓꽃의 종류를 구분하는 것이므로 target은 label과 동일하다고 볼 수 있다.
___

#### 2. 기초적인 정확도(accuracy) 평가방법
이제 우리는 다양한 정확도 계산 방법에 대해 배울 것이다. 크게 일반적인 평가 방법과 K-fold 방법으로 나눠서 알아보자.
```python
x_train, x_test, y_train, y_test = train_test_split(iris_data, iris_label, test_size = 0.2, random_state=11)#line 9

df_clf = DecisionTreeClassifier(random_state = 11)                                                          #line 10
df_clf.fit(x_train, y_train)                                                                                #line 11
pred = df_clf.predict(x_test)                                                                               #line 12
print('예측 정확도 : {0: .4f}'.format(accuracy_score(y_test, pred)))                                           #line 13
```

<img src="https://user-images.githubusercontent.com/97590480/154082535-5c169fef-6fc5-4e0d-9e91-09e3a616e34d.png">

1. [line 9]에서 `train_test_split`을 이용해서 훈련용 데이터와 테스트용 데이터로 나눈다. 속성은 `('x data', 'target data', '테스트 데이터 비율', '랜덤시드')`이다.
    - x 데이터는 붓꽃의 특징을 설명하는 설명변수, 독립변수 등을 의미한다.
    - target 데이터는 위에서 본 y, 종속변수 등을 의미한다.
    - 테스트 데이터 비율은 테스트용 데이터를 전체 중에서 몇퍼센트를 설정할 것인지에 관한 것이다. 여기서는 20%를 설정한다.
    - 랜덤시드는 훈련용 데이터와 테스트용 데이터를 랜덤하게 골고루 섞기는 한데 다른 사람들도 랜덤하게 나온 데이터가 동일하게 나오도록 설정해주는 것이다.
2. [line 10]에서 `DecisionTreeClassifier`을 불러와 df_clf에 넣어준다.
3. [line 11]에서 의사결정나무라고 선언한 df_clf에 `fit` 매서드를 사용해서 `x_train`, `y_train`을 이용해서 훈련을 시킨다. 이렇게 훈련시킨 모델은 df_clf에 담겨진다.
4. [line 12]에서 위에서 훈련시킨 모델의 예측력을 알아보기 위해 `predict`매서드를 사용해서 x_test를 넣었을 경우의 label값을 pred에 넣어준다.
5. [line 13]에서 pred에 담긴 x_test의 label 데이터와 y_test(label)와 얼마나 일치하는지를 판단해준다. 여기서는 0.9333의 정확도를 보인다.

#### 3. K-fold를 이용한 정확도 평가
```python
from sklearn.model_selection import KFold                                                                   #line 14

iris = load_iris()
features = iris.data
label = iris.target
dt_clf = DecisionTreeClassifier(random_state = 156)                                                         #line 15

kfold = KFold(n_splits = 5)                                                                                 #line 16
cv_accuracy = []

n_iter = 0                                                                                                  #line 17

for train_index, test_index in kfold.split(features):                                                       #line 18
    x_train, x_test = features[train_index], features[test_index]
    y_train, y_test = label[train_index], label[test_index]                                                 #line 19
    
    dt_clf.fit(x_train, y_train)
    pred = dt_clf.predict(x_test)
    n_iter += 1                                                                                             #line 20
    
    accuracy = np.round(accuracy_score(y_test, pred), 4)                                                    #line 21
    train_size = x_train.shape[0]
    test_size = x_test.shape[0]                                                                             #line 22
    
    print('\n#{0} 교차 검증 정확도 : {1}, 학습 데이터 크기 : {2}, 검증 데이터 크기 : {3}'.format(n_iter,accuracy, train_size, test_size))
    print('#{0} 검증 세트 인덱스 : {1}'.format(n_iter, test_index))
    cv_accuracy.append(accuracy)                                                                                        

print('\n## 평균 검증 정확도 : ', np.mean(cv_accuracy))                                                         #line 23
```

<img src="https://user-images.githubusercontent.com/97590480/154084646-c8b48954-4ef9-489f-82d2-48ccc91ca6c9.png">

1. [line 14]에서 K-fold 평가법을 사용하기 위해 `KFold`를 불러온다.
2. [line 15]에서 2.번에서 했던 의사결정나무 사전설정을 해준다.
3. [line 16]에서 K-fold를 사용하는데 K값을 5로 설정해준다. 이 말은 만약 전체 데이터가 100개라면 5그룹으로 나누고 1-20번째 데이터를 테스트용으로 사용하는 그룹 1, 21-40번재 데이터를 테스트용으로 사용하는 그룹 2, 이런 식으로 그룹3,4,5로 나눠서 정확도를 평가하는 방법이다.
4. [line 17]에서 몇번 반복했는지 표시해주는 iteracy를 설정해준다.
5. [line 18]에서 kfold에서 `split`를 사용해서 iris 데이터를 5그룹으로 나누는 인덱싱을 train_index와 test_index로 가져온다. 즉, 1그룹이라면 train_index는 [20:100], test_index는 [0:20]이 될 것이다.
6. [line 19]에서 위의 인덱싱에 맞게 설명변수와 label을 테스트용 데이터와 훈련용 데이터를 구분한다.
7. [line 20]에서 의사결정나무로 훈련용 데이터를 사용해서 모델링을 하고, `predict`매서드를 이용해서 label을 구한다.
8. [line 21]에서 이렇게 구한 데이터를 사용해서 accuracy를 구한다.
9. [line 22]에서 샘플 사이즈를 보기 위해서 `shape`매서드를 이용해서 각 데이터의 특징이 나오도록 한다.
10. [line 23]에서 위에서 구한 accuracy들의 평균을 구한다. 그러면 위의 사진처럼 나오게 된다.