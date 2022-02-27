# TIL(Today I Learned)

___

> Fab/27th2022_Multi campus_유선종 Day47

## 상관관계
- 통계를 공부한 사람이라면 한번쯤은 들어봤을 상관관계에 대해 알아 보고자 한다. 상관관계는 매우 중요한데, 왜냐하면 통계의 기본 가정은 각 설명변수(독립변수, 입력변수)들은 각각 독립이라는 가정이기 때문이다.
- 즉, 서로 상관관계가 존재하면 이 기본가정이 무너지게 되고 편향된 결과가 나오게 된다. 물론 딥러닝으로 넘어가면 이러한 상관관계를 오히려 이용하는 경우도 많다.
- 하지만 분석의 가장 기초는 상관관계를 알고 넘어가는 것이기 때문에 이 작업은 데이터 전처리 과정에 포함되어 매우 중요한 과정이므로 배우고 넘어가자.

### 1. 상관계수
두 변수의 상관관계를 구하기 위해서는 공분산의 개념을 알아야 한다.
1. 공분산은 확률변수의 선형 관계가 어느 정도인지를 나타내주는 지표로 식은 다음과 같다.

<img src="https://user-images.githubusercontent.com/97590480/155870066-b11992a2-dfc8-4f7c-a9ce-7724e41cf4cb.png">

2. 위의 이미지를 보면, 각 변수의 평균에서 얼마나 떨어져 있는지를 구해서 곱해줌으로써 두 변수의 상관관계의 선형관계가 얼마나 강한지를 알 수 있다.
3. 우리가 관심있는 것은 선형관계가 얼마나 강한지가 아니라 __선형관계가 존재하는지의 그 유무__ 이므로 이 공분산을 적절히 변형해서 우리가 관심있는 것을 알아낼 수 있다.

<img src="https://user-images.githubusercontent.com/97590480/155870210-4a76ea3d-dc0d-44a5-9abe-b9de83168783.png">

4. 위의 이미지에서 분자는 공분산, 분모는 각 변수의 표준오차이다. 우리는 이것을 상관계수라 부르고 로(ρ)라고 부른다.

<img src="https://user-images.githubusercontent.com/97590480/155870691-0aa9c2f7-10ae-457e-90a9-c73d801e786c.png">

5. `0 < ρ < 1`일때, 양의 선형관계가 존재하고, `ρ = 1` 일때 완벽한 양의 선형관계가 존재한다.
6. `-1 < ρ < 0`일때, 음의 선형관계가 존재하고, `ρ = -1`일때 완벽한 음의 선형관계가 존재한다. `ρ = 0`일때 어떠한 관계도 존재하지 않는다.
7. 즉, 우리는 독립변수간 선형관계가 존재하지 않는다고 가정하므로 `ρ = 0`에 가까워야 변수간 독립이므로 분석이 가능하다.
8. 이러한 가정은 통계에서 존재하므로 우리가 머신러닝에서 사용한 일반적인 분류에서는 상관관계를 구할 필요는 없다. 그러나 통계를 기본으로 하는 로지스틱 회귀나 엘라스틱인 경우에는 상관관계를 확인해줘야 한다.

### 2. 상관계수의 종류
상관관계를 측정하는 방법은 여러가지가 있다. 우선 측정방법을 나누기 위해서는 측정하는 변수의 특징을 알아야 한다.
1. 변수가 숫자처럼 연속형인가 혹은 성별, 인종 등의 범주형인가에 따라 나뉜다.
2. 범주형 중에서도 성별처럼 2개(binary)인 데이터인지, 혹은 인종처럼 3개 이상인지에 따라 나뉜다.
3. 또한, 범주형 중에서도 성별처럼 측정자의 의도가 들어가있지 않은 것과 성과를 상, 중, 하로 나눈 것처럼 측정자의 의도가 들어가있는 것으로 나뉜다.

- 이에 따라 다양한 상관계수 방법이 있지만 실습을 전부 하기에는 양이 너무 많으니 자주 쓰이는 방법과 코드를 서술하겠다. 여기서 사용하는 라이브러리는 `sklearn`,`spicy`이다.

___
#### 1. 두 독립변수가 연속형 - 연속형
1. Pearson correlation(피어슨 상관계수)
    - 연속형 자료가 정규분포임을 가정하는 모수적인 추론 방법이다.
    - `scipy.stats.pearsonr(x, y)`를 입력하면 측정이 가능하다.

2. Kendall correlation(켄달 상관계수)
    - 순위척도(1위, 2위, ..) 자료형에 대한 상관계수 추론 방법이다.
    - 비모수적 추론 방법이기 때문에 정규분포가 아니여도 사용이 가능하다.
    - `scipy.stats.kendalltau(x, y)`를 입력하면 측정이 가능하다.

3. Spearman correlation(스피어만 상관계수)
    - 캔달과 순위척도 자료형에 대한 상관계수 추론 방법이다.
    - 역시 비모수적 추론 방법이라 정규분포가 아니여도 사용이 가능하다.
    - `scipy.stats.spearmanr(x, y, axis=0, nan_policy='propagate')`를 입력하면 측정이 가능하다.
        1. `axis = 0`는 인덱스가 열이고 데이터가 행으로 나열되어 있을 경우에 사용한다. 디폴트가 0이므로 입력해주지 않으면 우리가 평소에 분석하던 방법이랑 동일하게 된다.
        2. `non_policy`는 Null값을 어떻게 처리하는지에 대한 속성이다. 디폴트값은 propagate로 Null값을 nan으로 반환해준다.

___
#### 2. 두 독립변수가 범주형 - 범주형
1. Matthews correlation coefficient(매튜 상관계수)
    - 파이 상관계수(Phi correlation)라고도 부른다. 
    - 원래는 범주 대상이 2개일 경우에 사용이 가능하다. 예를 들어 성별, 참/거짓, 참여 여부 등이 있다.
    - 그러나 sklearn에서 제공하는 matthews correlation은 3개 이상(multiclass)일 경우에도 사용이 가능하다.
    - `sklearn.metrics.matthews_corrcoef(y_true, y_pred)`를 입력하면 측정이 가능하다.
    - 매튜 상관계수를 구하는 방법은 다양한데 특히 confusion matrix를 이용해서 구할 수 있기 때문에 머신러닝에서도 사용된다. 식만 보고 넘어가겠다.

<img src="https://user-images.githubusercontent.com/97590480/155872005-1c982544-c7ec-4a22-ac5d-ae90abc63bbc.png">

1. cramer's v correlation coefficient(크래머의 V 상관계수)
   - 범주 대상이 3개 이상일 경우에 사용이 가능하다.
   - `scipy.stats.contingency.association(observed, method='cramer')`를 입력하면 측정이 가능하다. method 속성의 디폴트값은 cramer이므로 따로 입력하지 않아도 된다. 그러나 observed는 행렬의 형태로 변형해줘야 하므로 밑에서 실습을 통해 더 자세히 알아본다.

#### 3. 독립변수가 하나는 연속형, 하나는 범주형
1. point biserial corrlation
   - 범주 대상이 2개인 범주형 변수와 연속형 변수 사이의 상관관계를 구할 때 사용한다.
   - `scipy.stats.pointbiserialr(x, y)`를 입력하면 측정이 가능하다.

2. biserial, polyserial도 있지만 spicy에서 지원하지 않는다.

### 3. 상관관계 실습
실습을 통해 살펴보자.

```python
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
%matplotlib inline

student_df = pd.read_csv('./student.csv')
student_label = student_df[['math score', 'reading score', 'writing score']]
sns.pairplot(student_label)
```

<img src="https://user-images.githubusercontent.com/97590480/155884593-b9bab0e7-37a0-4cdf-ae75-a0666283a0b3.png">

1. 위의 이미지는 `sns.pairplot`을 이용해서 상관관계를 시각화한 것이다. 수학, 읽기, 쓰기 모두 강한 양의 상관관계를 보이는 것을 눈으로도 확인이 가능하다.

```python
from sklearn import preprocessing

### 성별 - 남/여 : 1/0, 인종 - A/B/C/D/E : 0/1/2/3/4, 점심 - 좋은 점심/공짜 점심 : 1/0, 시험 전 공부여부 : O/X - 1/0
features = ['gender','race/ethnicity', 'lunch']
for feature in features:
    le = preprocessing.LabelEncoder()
    le = le.fit(student_df[feature])
    student_df[feature] = le.transform(student_df[feature])
student_df['test preparation course'] = student_df['test preparation course'].replace(['completed', 'none'], [1,0])

### 부모의 학위 - 고등학교 중퇴/고졸/2년제/대학 중퇴/학사/석사 - 0/1/2/3/4/5
student_df['parental level of education'] = student_df['parental level of education'].replace([
    'some high school', 'high school', "associate's degree", 'some college',
    "bachelor's degree", "master's degree"], [0, 1, 2, 3, 4, 5])
```
여기서는 독립변수들 사이의 관계를 살펴보기 위해 명목변수들을 label화 시킨다.

```python
from scipy.stats import chi2_contingency

def cramers_V(x, y):
    cross = np.array(pd.crosstab(x,y, rownames = None, colnames = None))                                    #line 1
    chi2 = chi2_contingency(cross)[0]                                                                       #line 2
    obs = np.sum(cross)                                                                                     #line 3
    mini = min(cross.shape) - 1                                                                             #line 4
    return (chi2 / obs * mini)                                                                              #line 5
```
1. [line 1]에서 `pd.crosstab`을 이용해서 두 열을 행렬의 형태로 만들어준다. 예를 들어, 남자가 400명 여자가 300명이라면 1행 : [400, 0], 2행 : [0, 300]의 행렬을 만들어준다.
2. [line 2]에서 `chi2_contingency`를 이용해서 크래머의 V를 적용한다.
3. [line 3]에서 observation(관찰 갯수)를 구한다.
4. [line 4]에서 행과 열 중에서 최솟값을 (-1)해준 값을 mini에 넣는다.
5. [line 5]에서 크래머의 V를 결과값으로 받는다. obs나 mini는 cramer를 조정해주기 위해 넣는다.

```python
student_features = student_df.drop(['math score', 'reading score', 'writing score'], axis = 1, inplace = False)

row = []
for x in student_features:
    col = []
    for y in student_features:
        cramers = cramers_V(student_features[x], student_features[y])
        col.append(round(cramers,2))
    row.append(col)
    
cramers_result = np.array(row)
student_feature_corrmatrix = pd.DataFrame(cramers_result, columns = student_features.columns, index = student_features.columns)
sns.heatmap(student_feature_corrmatrix, annot = True)
```

<img src="https://user-images.githubusercontent.com/97590480/155885064-b2fed332-be27-4087-b95a-b30b5f6ef1ec.png">

1. 위의 코드를 입력하면 히트맵 결과를 얻어낼 수 있다. 결과를 보면 대부분 0에 가까우므로 독립변수는 서로서로 독립이라는 것을 알 수 있다.