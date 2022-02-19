# TIL(Today I Learned)

___

> Fab/19th/2022_Multi campus_유선종 Day39

## titanic 실습 계속
어제는 데이터 탐색 중에서 데이터를 살펴보는 작업을 했다. 이제 데이터를 분석하기 좋게 데이터를 변환해주는 데이터 전처리(preprocessing)를 실시하고 모델 평가를 통해 적절한 모델을 선택하는 것까지 진행해보도록 하자.

### 1. 데이터 전처리(preprocessing)
- 데이터 전처리는 데이터 셋에 존재하는 이상치(Outlier), 결측치(Missing Value)를 확인해서 필요하다면 제거를 하거나 적절하게 바꿔주는 단계이다. 
- 우리가 앞에서 데이터를 살펴보는 이유도 이러한 데이터 전처리를 위한 부분도 존재한다.
- 여기서 제대로 처리가 되지 않으면 분석이 제대로 실행이 안되거나 이상한 결론이 도출되기 때문에 데이터를 살펴보고 전처리를 실시한 이후에 추가적으로 전처리를 다시 시행해야 하는 경우도 존재한다.

#### 1. 이상치(Outlier)
이상치란 데이터가 모여있는 범위(lier)보다 훨씬 더 떨어져있는(out) 몇개의 데이터를 의미한다. 쉽게 생각해서 호랑이 1만마리 중에 백호가 태어나면 이상치는 백호가 된다. 대부분의 호랑이들은 갈색 계열의 털색깔을 가지고 있지만 백호는 흰색 털색깔을 가지고 있기 때문에 이러한 경우는 특이한 경우로 보고 제거를 해주거나 범위를 재설정해줘야 한다.
1. 이상치인지 아닌지를 구별하는 방법은 다양하지만, 대표적으로 많이 쓰는 것이 상자그림(boxplot)과 표준화점수(z-score)이다.
___
##### 1. 상자그림(boxplot)

<img src="https://user-images.githubusercontent.com/97590480/154796565-7967ee22-ab16-4093-a067-c11a0e0b49b1.png">

> 박스플롯은 Day08에서 날씨 크롤링을 할때 사용했던 기록이 있으므로 한번 참고하는 것도 좋다.

1. 박스플롯은 중앙값을 기준으로 일분위수(25%), 삼분위수(75%) 값에서 상자로 표시를 한다.
2. 여기서 삼분위수와 일분위수를 뺀 것을 Inner quantile Range(IQR)이라고 하는데 IQR에 1.5를 곱하여 일분위수와 삼분위수에 1.5IQR 거리만큼을 양 사이드로 더 늘린 것을 표시하고 그 이상 혹은 그 이하에 존재하는 값들을 이상치로 본다.
3. 여기서 이상치가 유의미하게 많이 있다면 범위를 늘려주기 위해 1.5를 바꿔주면 되는데 이를 터키 계수라고 한다. 터키 계수를 보통 많이 잡으면 2 혹은 3으로 잡고서 한다.
4. 이러한 이상치는 데이터를 분석할 때 갯수가 별로 없어서 큰 의미를 도출하기는 힘들지만 결과에는 영향을 주기 때문에 제거하거나 의미를 발견할 수 있다면 남길 수도 있다.
___
이러한 이상치를 처리하는 방법은 이상값 제외(trimming), 이상값 대체(winsorization), 변수변환 등이 있다.
1. 이상값 제외는 이상값을 제거하는 것이다. 그렇지만 정보 손실이 발생하고 추정량 왜곡이 발생할 수도 있다.
2. 이상값 대체는 우리가 정한 정상값(여기서는 1.5IQR 안에 들어오는 값)을 이용해서 이상값을 정상값의 최댓값, 최솟값으로 바꿔주는 방법이다. 이상값의 숫자가 적기 때문에 어느정도 분포의 손실을 최소화하는 방법이다.
3. 변수변환은 변수를 로그나 제곱근 등으로 변환하는 방법이다. 우리가 다루는 데이터의 숫자가 매우 클 경우 로그 변환을 취할 경우 매우 좋은 결과를 얻어낼 수 있다.
___
##### 2. 표준화점수(z-socre)
1. 표준화점수는 각각의 데이터들을 표준 정규화를 통해서 이상치로 규정하는 것을 의미한다.
2. 표준정규화를 할 경우에 우리는 95% 신뢰구간이라고 가정했을 때, 평균이 0인 지점에서 1.96만큼 떨어진 지점까지는 우리가 신뢰할 수 있는 구간이다.
3. 즉, 표준화점수는 이를 이용하여 표준화점수가 2(정확히는 1.96)를 넘어가는 데이터는 이상치로 보는 것이다.
4. 만약 신뢰구간을 99%로 잡을 경우에는 2.58이므로 대략 3이상 넘어가면 이상치로 보는 것이다.

> 표준정규분포는 고등학교때 배우는 내용이므로 자세한 설명은 하지 않겠다. 기억이 안난다면 구글링을 하자.
___
#### 2. 결측치(Missing Value)
- 결측치는 누락된 데이터를 의미한다. 원래부터 입력이 되어있지 않은 자료이기 때문에 함부로 추측하기 힘들다.
- 만약, 결측치가 너무 많다면 결측치 그 자체로 납두거나 그 특징변수를 사용하지 않을 수도 있다.
- 반면에, 결측치가 그렇게 많지 않다면 결측치를 대체하는 방법이 있다.
    1. 완전제거법(list-wise deletion)은 그냥 하나 이상의 결측치가 존재하면 그 변수를 제거하는 것이다. 매우 많다면 적절할 수 있겠지만 대체로 사용하지 않는다.
    2. 평균대체법(mean value imputation)은 결측치를 제외한 데이터들의 평균을 구해서 평균값으로 대체하는 방법이다. 하지만 평균값이 증가함으로써 표준오차가 과소 추정되는 문제가 발생한다.
    3. 핫덱대체법(hot deck imputation)은 동일한 데이터 내에서 결측치가 관찰된 데이터와 유사한 특성을 가진 다른 데이터의 값을 넣어주는 방법이다. 예를 들어, 결측치가 남성의 나이라면 해당 남성과 비슷한 요금, 클래스, 부모의 수 등 여러 특징이 비슷한 남성의 나이와 동일한 나이로 기록하는 것이다.

___
#### 3. 타이타닉 결측치
우리가 분석하던 타이타닉 실습에서 발견되었던 결측치는 나이, 사물함, 승선위치였다. 여기서 나이는 평균대체법을, 나머지는 결측치가 많기 때문에 N으로 대체하여 결측치라는 것을 표시하도록 코딩을 하겠다.

```python
def fillNA(df):
    df['Age'].fillna(df['Age'].mean(), inplace = True)                                                      #line 1
    df['Cabin'].fillna('N', inplace = True)                                                                 #line 2
    df['Embarked'].fillna('N', inplace = True)
    return df                                                                                               #line 3
```

1. [line 1]에서 `.fillna()`매서드를 이용해서 결측치를 Age의 평균값으로 적용해준다. `inplace = True`는 바뀐 값을 기존 값에 적용해주는 속성이다.
2. [line 2]에서 `.fillna()`매서드를 이용해서 결측치를 `N`으로 바꿔준다.
3. [line 3]에서 바꾼 데이터 프레임을 결과값으로 받도록 해준다.
___
#### 4. 불필요한 데이터 삭제
타이타닉의 특성변수 중에서 passengerID와 Name, Ticket에서는 어떤 특정 의미를 찾아내기 어렵다. 이럴 경우 과감히 해당 변수들을 제거해준다.

```python
def drop(df):
    df.drop(['PassengerId', 'Name', 'Ticket'], axis = 1, inplace = True)                                    #line 4
```
- `.drop()`매서드를 이용해서 불필요한 열을 삭제해주자. axis = 1은 열, 0은 행을 의미하는 속성이다.
___
#### 5. 범주형(category) 데이터 변환
- 타이타닉의 특성변수 중에서 성별은 'male', 'female'로 표시된다. 이를 분석하기 위해서는 0과 1의 숫자형 데이터로 바꿔줘야 분석을 실시할 수 있다. 
- 여기서 0과 1은 단지 male과 female을 지칭하기 위한 숫자로 사용되는데, 이를 우리는 더미변수(dummy variable) 혹은 label 데이터라고 한다.
- 여기서 목표변수가 되는 생존여부 또한 label 데이터이기 때문에 나는 더미변수라고 부르겠다.

```python
def format_features(df):
    from sklearn import preprocessing                                                                       #line 5
    df['Cabin'] = df['Cabin'].str[:1]                                                                       #line 6
    features = ['Cabin', 'sex', 'Embarked']                                                                 #line 7
    for feature in features:
        le = preprocessing.LabelEncoder()                                                                   #line 8
        le = le.fit(df[feature])                                                                            #line 9
        df.[feature] = le.transform(df[feature])                                                            #line 10
```

<img src="https://user-images.githubusercontent.com/97590480/154802129-083e8753-1453-447f-887a-ffdfe472b8cd.png">

1. [line 5]에서 `preprocessing` 클래스를 불러온다.
2. [line 6]에서 사물함이 'C25'처럼 앞의 문자가 사물함을 분류해주는 기준이므로 `.str[:1]`인덱싱을 이용해서 문자열의 첫번재 문자만 뽑아낸다.
3. [line 7]에서 각 열 이름을 features에 넣는다.
4. [line 8]에서 `preprocessing.LabelEncoder()`를 le 인스턴스에 받아서 클래스를 선언한다.
5. [line 9]에서 `.fit(df[feature])` 매서드를 이용해서 각 열을 적용시킨다.
6. [line 10]에서 `.transform()` 매서드를 이용해서 특성변수를 더미변수로 변환해준다.
___
#### 6. 데이터 변환 적용
위에서 변환해주는 함수들을 이용해 변수들을 feature와 label로 나누고 feature에만 적용시킨다.

```python
def transform_features(df):
    df = fillna(df)
    df = drop_features(df)
    df = format_features(df)
    return df

titanic_df = pd.read_csv('./titanic/titanic_train.csv')                                                     #line 11
y_titanic_df = titanic_df['Survived']                                                                       #line 12
x_titanic_df = titanic_df.drop('Survived', axis = 1)                                                        #line 13

x_titanic_df = transform_features(x_titanic_df)                                                             #line 14
```

1. [line 11]에서 pandas를 이용해서 데이터를 불러온다.
2. [line 12]에서 label인 생존여부만 뽑아서 종속변수(목표변수, label, 반응변수 등으로 읽을 수 있다)로 설정한다.
3. [line 13]에서 feature인 생존여부 데이터를 제외한 나머지를 독립변수(입력변수, feature, 설명변수 등으로 읽을 수 있다)로 설정한다.
4. [line 14]에서 feature만 위에서 변환하기 위해 설정한 함수를 이용해서 전처리를 해준다.
___
### 2. 모델 적합도 테스트
- 이제 우리는 분석을 실시하기 위한 사전 작업을 끝마쳤다. 이제는 모델을 사용해서 결과를 도출하기만 하면 된다.
- 여기서 우리는 어떤 모델을 사용할 것인가에 대한 고민이 생길 수 밖에 없다.
- 가장 단순한 방법은 분류에 사용되는 모든 알고리즘을 적용해보는 것이다.

#### 1. 정확도(accuracy) 테스트

```python
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(x_titanic_df, y_titanic_df, test_size = 0.2, random_state = 11)

dt_clf = DecisionTreeClassifier(random_state = 11)                                                          #line 15
rf_clf = RandomForestClassifier(random_state = 11)                                                          #line 16
lr_clf = LogisticRegression()                                                                               #line 17

dt_clf.fit(x_train, y_train)
dt_pred = dt_clf.predict(x_test)
print('DecisionTreeClassifier 정확도 : {0:.4f}'.format(accuracy_score(y_test, dt_pred)))

rf_clf.fit(x_train, y_train)
rf_pred = rf_clf.predict(x_test)
print('RandomForestClassifier 정확도 : {0:.4f}'.format(accuracy_score(y_test, rf_pred)))

lr_clf.fit(x_train, y_train)
lr_pred = lr_clf.predict(x_test)
print('LogisticRegression 정확도 : {0:.4f}'.format(accuracy_score(y_test, lr_pred)))
```

1. [line 15]에서 의사결정나무 클래스를 불러온다. 그 결과 정확도는 0.7877이 나왔다.
2. [line 16]에서 랜덤 포레스트 클래스를 불러온다. 그 결과 정확도는 0.8547이 나왔다.
3. [line 17]에서 로지스틱 회귀 클래스를 불러온다. 그 결과 정확도는 0.8492가 나왔다. 이 근거를 통해 우리는 랜덤 포레스트가 셋 중 적합한 모델로 보고 랜덤 포레스트를 사용해야 하지면 예제에서는 의사결정나무를 사용했으므로 의사결정나무로 우선 진행하겠다.

<img src="https://user-images.githubusercontent.com/97590480/154803031-16bd902d-416b-46a0-b3c7-a55212bcea3b.png">

___
#### 2. 의사결정나무 K-fold 검증
```python
from sklearn.model_selection import KFold                                                                   #line 18
import numpy as np

kfold = KFold(n_splits = 5)                                                                                 #line 19
scores = []

for iter_count, (train_index, test_index) in enumerate(kfold.split(x_titanic_df)):                          #line 20
    x_train, x_test = x_titanic_df.values[train_index], x_titanic_df.values[test_index]
    y_train, y_test = y_titanic_df.values[train_index], y_titanic_df.values[test_index]
    
    dt_clf.fit(x_train, y_train)                                                                            #line 21
    predictions = dt_clf.predict(x_test)                                                                    #line 22
    accuracy = accuracy_score(y_test, predictions)                                                          #line 23
    scores.append(accuracy)
    
    print("교차 검증{0} 정확도 : {1:.4f}".format(iter_count+1, accuracy))
    
mean_score = np.mean(scores)
print(f"평균 정확도 : {mean_score:.4f}")
```

1. [line 18]에서 K-fold 검증을 시행하기 위해 `sklearn.moderl_selection`에서 KFold 클래스를 불러온다.
2. [line 19]에서 그룹을 5개로 나누는 K-fold(K=5)를 kfold 인스턴스에 넣어준다.
3. [line 20]에서 `kfold.split`매서드를 이용해서 그룹에 따라 임의로 데이터를 나누는 인덱싱 값들을 train_index와 test_index에 넣어준다. 이를 이용해서 x,y를 각각 훈련용과 테스트용으로 나눈다.
4. [line 21]에서 의사결정나무 모델에 훈련용 데이터 셋을 적용한다.
5. [line 22]에서 테스트용 데이터의 예측한 데이터를 받는다.
6. [line 23]에서 예측도와 y의 라벨과 얼마나 일치하는지를 나타내는 정확도를 계산한다. 정확도는 아래의 이미지처럼 나온다.

<img src="https://user-images.githubusercontent.com/97590480/154805523-5344efa2-2f5b-4336-9e0c-fc23e4e99367.png">

___

#### 3. 교차검증도(cross validate score)
이번에는 stratified K-fold와 동일한 알고리즘을 갖는 교차검증을 통해 정확도를 구해보자.

```python
from sklearn.model_selection import cross_val_score                                                         #line 24

scores = cross_val_score(dt_clf, x_titanic_df, y_titanic_df, cv = 5)                                        #line 25
for iter_count, score in enumerate(scores):                                                                 #line 26
    print("교차 검증{0} 정확도 : {1:.4f}".format(iter_count+1, score))

print(f"평균 정확도 : {score:.4f}")
```
1. [line 24]에서 교차검증도 클래스를 불러온다.
2. [line 25]에서 `cross_val_score('모델',feature,label,cv = '그룹수')`를 이용해서 교차검증도를 구한다.
3. [line 26]에서 교차검증도는 리스트형태로 저장되어 있기 때문에 enumerate 함수를 이용해서 각각 뽑아내서 밑의 이미지처럼 출력한다.

<img src="https://user-images.githubusercontent.com/97590480/154805702-d45e9ad4-fa82-426e-b97e-a3d18e95e9dd.png">

___
- 남은 작업은 교차검증을 이용해 최적의 hyperparameter를 구하고 정확도, 정밀도, 재현율을 통해 모델 평가를 하는 것만 남았다.
- 그러나 정확도, 정밀도, 재현율에 대한 이론적인 설명이 필요하기 때문에 이에 관한 설명은 내일로 미뤄서 이론과 함께 알아보고자 한다.