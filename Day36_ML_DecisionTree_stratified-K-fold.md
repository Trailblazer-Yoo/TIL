# TIL(Today I Learned)

___

> Fab/16th/2022_Multi campus_유선종 Day36

## 머신러닝 - 의사결정나무
어제는 의사결정나무를 모델링하여 평가하는 방법 중에 일반적인 방식과 k-fold 방식을 알아보았다. 이번에는 적절한 비율로 조정하는 stratified k-fold 방식과 초모수(hyperparameter)설정에 대해 알아보겠다.

### 1. K-fold
stratified K-fold를 하기 전에 K-fold와의 비교를 위해 어제 했던 K-fold를 이용해서 그룹이 어떻게 나뉘는지 보자.

```python
from sklearn.datasets import load_iris                                                               
from sklearn.tree import DecisionTreeClassifier                                                             
from sklearn.model_selection import train_test_split                                                      
from sklearn.metrics import accuracy_score                                                               

import numpy as np                                                                                       
import pandas as pd  

iris = load_iris()                                                                                              #line 1

iris_df = pd.DataFrame(data = iris.data, columns = iris.feature_names)                                          #line 2

kfold = KFold(n_splits = 3)                                                                                     #line 3

n_iter = 0
for train_index, test_index in kfold.split(iris_df):                                                            #line 4
    n_iter += 1
    label_train = iris_df['label'].iloc[train_index]                                                            #line 5
    label_test = iris_df['label'].iloc[test_index]                                                              #line 6
    print('## 교차 검증: {0}'.format(n_iter))
    print('학습 레이블 데이터 분포 : \n', label_train.value_counts())
    print('검증 레이블 데이터 분포 : \n', label_test.value_counts())
```

<img src="https://user-images.githubusercontent.com/97590480/154223327-346617b6-d2a0-4b79-a443-6163e735e930.png">

1. [line 1]에서 iris 데이터를 불러온다. 관련된 라이브러리를 불러오는 코드는 생략하겠다.
2. [line 2]에서 iris 데이터를 데이터프레임 형태로 저장한다.
3. [line 3]에서 k-fold를 불러오는데, `n_splits = 3`은 `K = 3`인 k-fold를 의미한다.
4. [line 4]에서 3그룹으로 나눈 인덱싱 값들을 가져온다.
5. [line 5]에서 훈련용 데이터를 가져온다. 이때, 데이터프레임 인덱싱에 활용되는 매서드인 `iloc`을 이용한다.
6. [line 6]에서 테스트용 데이터를 가져온다. 이미지를 보면 각 그룹별로 훈련용 데이터 100(50+50)개와 테스트용 데이터 50개로 나뉜 것을 볼 수 있다.
___
### 2. stratified K-fold
그러면 계층화 K겹(stratified K-fold) 평가 방식은 K-fold와 어떤 차이가 있는지 알아보자. 우선 유념해야 할 키워드는 일정 비율로 데이터를 뽑는다는 것이다.

```python
from sklearn.model_selection import StratifiedKFold                                                             #line 8

skf = StratifiedKFold(n_splits = 3)                                                                             #line 9
n_iter = 0

for train_index, test_index in skf.split(iris_df, iris_df['label']):
    n_iter += 1
    label_train = iris_df['label'].iloc[train_index]
    label_test = iris_df['label'].iloc[test_index]
    print('## 교차 검증: {0}'.format(n_iter))
    print('학습 레이블 데이터 분포 : \n', label_train.value_counts())
    print('검증 레이블 데이터 분포 : \n', label_test.value_counts())
```

<img src="https://user-images.githubusercontent.com/97590480/154223912-00fdc1ae-db92-4cdb-ac47-7df95e4e6949.png">

1. [line 8]에서 stratifiedKFold를 불러온다.
2. [line 9]에서부터 skf에 K=3인 stratified K-Fold를 넣는다. 그 이후부터는 위에서 K-Fold에서 했던 것과 동일하다.
3. k-fold와 비교해보면 그룹1에서 k-fold에서는 훈련용 데이터로 0(setosa)과 1(versicolor)의 데이터만 존재하고 테스트용 데이터에는 2(virginica)만 존재한다.
   1. 이렇게 데이터를 나눠서 모델을 학습하면 모델은 0과 1의 데이터로만 학습했으므로 데이터에 편향이 생겨 2의 데이터에 대해 전혀 특징을 잡아내지 못한다.
   2. 즉, 이 모델은 포유류 중에서 개와 고양이만 학습시켜서 세상에는 개와 고양이만 존재하는 줄 알고 있는데 여기서 돌고래를 주면 돌고래에 대해 포유류라고 전혀 인식하지 못한다.
   3. 이런 편향을 피하기 위해 0,1,2에 대한 데이터를 적절한 비율로 섞어서 훈련용 데이터와 테스트용 데이터로 나눈다. 그래서 그룹 1에서 훈련용 데이터는 2가 34개, 1이 33개, 0이 33개의 데이터로 구성이 된다.
___

### 3. 정확도 평가
```python
df_clf = DecisionTreeClassifier(random_state = 156)

skfold = StratifiedKFold(n_splits = 3)
n_iter=0
cv_accuracy = []

for train_index, test_index in skfold.split(features, label):
    X_train, X_test = features[train_index], features[test_index]
    y_train, y_test = label[train_index], label[test_index]
    
    dt_clf.fit(X_train, y_train)
    pred = dt_clf.predict(X_test)
    
    n_iter += 1
    accuracy = np.round(accuracy_score(y_test, pred),4)
    train_size = X_train.shape[0]
    test_size = X_test.shape[0]
    print('\n#{0} 교차 검증 정확도 : {1}, 학습 데이터 크기 : {2}, 검증 데이터 크기 : {3}'.format(n_iter, accuracy, train_size, test_size))
    print('#{0} 검증 세트 인덱스 : {1}'.format(n_iter,test_index))
    cv_accuracy.append(accuracy)
    
print('/n## 교차 검증별 정확도 : ', np.round(cv_accuracy, 4))
print('## 평균 검증 정확도 : ', np.mean(cv_accuracy))
```

<img src="https://user-images.githubusercontent.com/97590480/154229452-6ebe0e98-5d64-4d20-add4-2291c1e7e268.png">

1. 정확도를 구하는 과정은 Day35에 자세히 설명이 되어 있으므로 생략하고 넘어가도록 하겠다.
2. 위 이미지를 보면 정확도가 매우 높은 것을 볼 수 있다. 이렇게 stratified K-fold를 사용하면 일반적인 K-fold보다 정확도가 상승하므로 대부분 stratified K-fold를 사용한다.
3. sklearn에서는 이러한 stratified K-fold를 알아서 계산해주는 매서드를 제공한다.
___
```python
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score, cross_validate
from sklearn.datasets import load_iris
import numpy as np

iris_data = load_iris()
dt_clf = DecisionTreeClassifier(random_state=156)

data = iris_data.data
label = iris_data.target

scores = cross_val_score(dt_clf, data, label, scoring = 'accuracy', cv = 3)                                     #line 10
```

1. [line 10]에서 `cross_val_score('모델', 'x 데이터', 'y 데이터', '평가방법', '그룹수')`을 이용하면 교차검증을 이용한 정확도를 계산할 수 있다. 그 결과는 위에서 봤던 stratified K-fold와 동일하다.
2. 즉, 여기서 cross_validate는 교차검증으로 여기서 말하는 stratified K-fold 방식을 사용한다. 그런데 그냥 stratified K-fold를 사용하면 되는데 왜 굳이 교차검증을 사용할까?
    - 우리는 위에서 훈련용 데이터와 테스트용 데이터를 구별하여 훈련용 데이터로 학습을 하고 학습한 모델의 성능 평가를 테스트 데이터로 평가했다.
    - 여기서 우리는 hyperparameter(초모수)를 이해해야 한다. hyperparameter는 모델 밖에서 임의로 설정해주는 값이다. 예를 들어, 의사결정나무에서 브랜치를 나누는 기준이나 층을 몇층까지 만들것인가 등은 우리가 결정해야 하는 부분이다.
    - 그러나 우리는 이런 문제에 직면한다. "그러면 우리는 어떤 hyperparameter를 설정해줘야 하지?" 이를 해결하는 방법은 성능이 가장 좋은 hyperparameter를 사용하는 것이다.
    - 그래서 우리는 설정할 수 있는 모든 hyperparameter를 설정하여 모델을 돌려보고 그 중에서 가장 성과가 좋은 hyperparameter 묶음을 선택한다.
    - 이렇게 성과가 가장 좋은 모델을 다시 test 데이터로 또한번 평가하여 검증한다.
3. 최적의 hyperparameter set을 찾기 위해 사용하는 것이 교차검증이고, 여기서 교차검증은 stratified K-fold 방식을 채택하고 있다.

___

### 4. hyperparameter

```python
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV

iris_data = load_iris()
X_train, X_test, y_train, y_test = train_test_split(iris_data.data, iris_data.target, test_size = 0.2, random_state = 121)

dtree = DecisionTreeClassifier()

parameters = {'max_depth':[1,2,3], 'min_samples_split':[2,3]}                                                   #line 11

grid_dtree = GridSearchCV(dtree, param_grid = parameters, cv=3, refit = True)                                   #linw 12

grid_dtree.fit(X_train, y_train)

scores_df = pd.DataFrame(grid_dtree.cv_results_)
scores_df[['params', 'mean_test_score', 'rank_test_score', 'split0_test_score', 'split1_test_score', 'split2_test_score']]
```

<img  src="https://user-images.githubusercontent.com/97590480/154286823-234f4d9b-443e-4d59-8e02-7abfc95e9e0e.png">>

1. [line 12]에서 hyperparameters를 설정한다. 층의 갯수를 1, 2, 3으로 설정하고 브랜치를 나누는 최소한의 변수 갯수를 `min_samples_split으로 나누면 층이 2인 것과 3인 것으로 나뉜다
2. 즉, 우리는 하이퍼파리미터에 따라 그 결과가 달라지는 것이다.

```pythone
print('GridSearchCV 최적 파라미터 : ', grid_dtree.best_params_)
print('GridSearchCV 최고 정확도 : {0:.4f}'.format(grid_dtree.best_score_))
```
<img src="https://user-images.githubusercontent.com/97590480/154287054-6a9140dc-b3cd-4247-a555-93a7fec67a52.png">

1. 결과를 보면 하이퍼파라미털가 달라질때 마다 결과가 달라지고, 하이퍼파라미터가 달라짐에 따라 평가가 달라지면서 정호가도가 달라진다.
2. 여기서 가장 적합한 하이퍼파라미터느느 (3,2)로 노드의 층의 갯수는 3, 노드의 구별은 2로 최적이다.
3. 즉 우리는 이런 식으로 의사결정나무의 교차검증과 테스트를ㄹ 실힛한다.