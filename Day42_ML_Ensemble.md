# TIL(Today I Learned)

___

> Fab/22nd/2022_Multi campus_유선종 Day42

## 앙상블
앙상블은 조화롭다는 그 말의 뜻 그대로 다른 머신러닝 기법을 섞어서 사용하는 것을 말한다. 다양한 머신러닝 기법을 섞어서 사용할 경우 대체로 성능이 상승하는 것을 볼 수 있다. 머신러닝 기법이나 데이터를 어떻게 조화시키냐에 따라 앙상블이 나뉘어진다.

### 1. 앙상블의 종류
앙상블은 크게 보팅, 배깅, 부스팅, 랜덤포레스트가 있다. 
1. 보팅은 여러 개의 모델로부터 산출된 결과를 다수결에 의해서 최종 결과를 선정하는 방식이다.
   1. 예를 들어, 붓꽃 데이터를 평가하는데 KNN, 의사결정나무, 로지스틱 회귀 모델을 학습시켜 각각 예측값이 1,2,1이 나왔다면 1이 가장 많으므로 1을 선택하는 방법이다. 이를 하드 보팅이라 한다.
   2. 반면에, 각 모델의 1,2가 나올 확률이 각각 (0.3,0.7), (0.5, 0.5), (0.2, 0.8)이라면 각각의 확률을 평균해 최종 결과를 1,2가 나올 확률은 (0.33, 0.66)으로 결과를 도출하는 것을 소프트 보팅이라 한다.
2. 배깅은 하나의 모델로 학습하되, 데이터를 여러개로 나눠 학습시키는 것을 말한다. 배깅은 훈련자료를 모집단으로 생각하고 평균예측모형을 구하여 분산을 줄이고 예측력을 향상시키는 장점이 있다.
3. 부스팅은 예측력이 약한 모델들을 결합하여 강력한 예측모델을 만드는 방법이다. 여러개의 분류기를 설정하고 가중치를 조정함으로써 배깅같은 이진분류의 한계점을 보완한 방법이다.
4. 랜덤 포레스트는 기본적으로 의사결정나무를 기반으로 만들어졌으며, 의사결정나무가 분산이 크다는 점을 고려하여 배깅과 부스팅보다 더 많은 무작위성을 줘서 약한 학습기들을 생성한 후에 선형 결합하여 최종 학습기를 만드는 방법이다.

### 2. 보팅 실습
```python
import pandas as pd
from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

cancer = load_breast_cancer()
data_df = pd.DataFrame(cancer.data, columns = cancer.feature_names)
lr_clf = LogisticRegression()
knn_clf = KNeighborsClassifier(n_neighbors = 8)

vo_clf = VotingClassifier(estimators=[('LR', lr_clf),('KNN', knn_clf)], voting = 'soft')                            #line 1
X_train, X_test, y_train, y_test = train_test_split(cancer.data, cancer.target, test_size = 0.2, random_state = 156)

vo_clf.fit(X_train, y_train)                                                                                        #line 2
pred = vo_clf.predict(X_test)                                                                                       #line 3
print('Voting 분류기 정확도 : {0:.4f}'.format(accuracy_score(y_test, pred)))

classifiers = [lr_clf, knn_clf]
for classifier in classifiers:
    classifier.fit(X_train, y_train)
    pred = classifier.predict(X_test)
    class_name = classifier.__class__.__name__                                                                      #line 4
    print('{0} 정확도: {1:.4f}'.format(class_name, accuracy_score(y_test, pred)))
```

<img src="https://user-images.githubusercontent.com/97590480/155140208-1660430f-6874-470d-8180-0a1f8280d0d6.png">

1. [line 1]에서 `VotingClassifieer`모델을 설정해준다. 여기서는 2가지 모델을 섞었다. `estimators = ([(로지스틱회귀),(K Neighbor)], 소프트보팅)`속성을 통해서 로지스틱 회귀와 KNN을 섞었다.
2. [line 2]에서 다른 모델과 비슷하게 훈련용 데이터로 보팅을 학습시킨다.
3. [line 3]에서 학습한 모델을 가지고 예측을 시행한다.
4. [line 4]에서 `classifier.__class__.__name__`은 각각의 머신러닝 모델 클래스 안에 __class__라는 함수가 있는데 거기서 클래스명을 가져온다는 의미힌다.
5. 위의 이미지를 보면 일반적인 로지스틱회귀와 KNN을 할 때 보다 보팅의 정확도가 더 높은 것을 알 수 있다.

### 3. 랜덤 포레스트 실습
```python
def get_new_feature_name_df(old_feature_name_df):                                                                   #line 5
    feature_dup_df = pd.DataFrame(data=old_feature_name_df.groupby('column_name').cumcount(), columns=['dup_cnt'])  #line 6
    feature_dup_df = feature_dup_df.reset_index()                                                                   #line 7
    new_feature_name_df = pd.merge(old_feature_name_df.reset_index(), feature_dup_df, how = 'outer')                #line 8
    new_feature_name_df['column_name'] = new_feature_name_df[['column_name',
     'dup_cnt']].apply(lambda x : x[0] + '_' + str(x[1]) if x[1] > 0 else x[0], axis = 1)                           #line 9
    
    new_feature_name_df = new_feature_name_df.drop(['index'], axis = 1)                                             #line 10
    return new_feature_name_df
```
1. [line 5]에서 중복되는 열이 있을경우 구분하여 새롭게 생성하는 함수를 만든다.
2. [line 6]에서 `.cumcount()` 매서드를 이용해서 중복되는 열의 갯수가 몇개인지 누적으로 보여주고, 이를 `dup_cnt` 열에 저장한다. 가령, study 열이 5개가 중복된다면 study열 중에서 앞에 열부터 `dup_cnt`열에 1,2,3,4,5 값이 생성된다.
3. [line 7]에서 `reset_index()`를 사용하여 행의 이름으로 사용하던 열 이름을 다시 열로 가져온다. 예를 들어, 행의 이름이 r1 : a,b,c 였다면, 이 행이 열로 변하고 행은 0,1,2로 바뀐다.
4. [line 8]에서 `outer`방식으로 데이터프레임을 병합하는데, 아우터 방식은 합집합 형태로 합쳐지는 것을 의미한다. 즉, 서로 겹치지 않는 열과 행이 있다면 그대로 보존하여 생성하고 겹치는 부분은 중복을 제거하고 합친다.
5. [line 9]에서 `dup_cnt`열에 넣어놨던 값을 중복되는 열 이름에 `_1, _2, ...`형태로 만들어줌으로써 중복을 피한다.
6. [line 10]에서 `reset_index()`로 생성된 `index`열을 제거함으로써 마무리한다.
___
```python
def get_human_dataset():
    feature_name_df = pd.read_csv('./human_activity/features.txt', sep='\s+', header=None, names = ['column_index','column_name'])
    
    new_feature_name_df = get_new_feature_name_df(feature_name_df)
    
    feature_name = new_feature_name_df.iloc[:, 1].values.tolist()
    
    X_train = pd.read_csv('./human_activity/train/X_train.txt', sep='\s+', names = feature_name)
    X_test = pd.read_csv('./human_activity/test/X_test.txt', sep='\s+', names = feature_name)
    
    y_train = pd.read_csv('./human_activity/train/y_train.txt', sep='\s+', header= None, names = ['action'])
    y_test = pd.read_csv('./human_activity/test/y_test.txt', sep='\s+', header= None, names = ['action'])
    
    return X_train, X_test, y_train, y_test
```
이 함수는 훈련용 데이터와 테스트 데이터를 생성하는 함수이다. 특이한 것은 `sep = \s+` 속성인데 이것은 구분자의 길이가 정해지지 않은 공백이나 다른 쉼표를 제외한 구분자를 구별하여 데이터프레임에 넣어주는 속성이다.
___
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pandas as pd
import warnings
warnings.filterwarnings('ignore')                                                                                   #line 11

X_train, X_test, y_train, y_test = get_human_dataset()

rf_clf = RandomForestClassifier(random_state = 0)                                                                   #line 12
rf_clf.fit(X_train, y_train)
pred = rf_clf.predict(X_test)
accuracy = accuracy_score(y_test, pred)
print('랜덤 포레스트 정확도 : {0:.4f}'.format(accuracy))
```
<img src="https://user-images.githubusercontent.com/97590480/155147151-648d4485-5fd4-48d9-aaf1-dd27975643f7.png">

1. [line 11]에서 오류메세지가 나올 경우 무시해주는 명령어를 입력해준다. 모델을 실행하면 빨간색줄의 오류가 마구마구 뜨는데 모델을 돌리는데에는 아무런 문제가 없으니 이 명령어를 통해서 깔끔하게 결과창을 만들 수 있다.
2. [line 12]에서 랜덤포레스트를 설정하여 모델을 학습시키고 정확도를 계산한다.
3. 보팅보다는 낮은 정확도를 보인다. 이처럼 어떤 모델이 더 좋다는 것이 아니라 평가 결과가 더 뛰어난 모델을 선택해서 학습하면 된다.
___

```python
from sklearn.model_selection import GridSearchCV

params = {
    'n_estimators':[90],
    'max_depth' : [9],
    'min_samples_leaf' : [10],
    'min_samples_split' : [2]
}
rf_clf = RandomForestClassifier(random_state = 0, n_jobs = -1)
grid_cv = GridSearchCV(rf_clf, param_grid = params, cv = 5, n_jobs=-1)
grid_cv.fit(X_train, y_train)

print('최적 하이퍼 파라미터 : \n', grid_cv.best_params_)
print('최고 예측 정확도: {0:.4f}'.format(grid_cv.best_score_))
```

<img src="https://user-images.githubusercontent.com/97590480/155148124-a2c9fc2a-9195-4397-af0e-2c71e73da821.png">

여기서는 하이퍼 파라미터를 설정해준 랜덤포레스트의 결과이다. 기본적으로 랜덤포레스트는 의사결정모델을 기반으로 만들어졌기 때문에 동일한 하이퍼 파라미터를 설정하되 n_estimators를 설정해줘야 한다.

### 4. GradientBoostingClassifier
부스팅 기법은 분류기마다 가중치를 주는 분류 방법이다. 훈련용 데이터는 각 분류기를 거쳐가면서 오분류 데이터와 정분류 데이터로 나뉘고 오분류 데이터는 버리고 정분류 데이터는 다시 분류기를 거쳐간다. 이것을 반복하여 최종 분류기를 만드는 방법이 부스팅이다. 그래디언트 부스팅은 손실함수를 이용하여 손실함수를 최소화하는 방식으로 부스팅을 진행한다. 
```python
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import GradientBoostingClassifier

X_train, X_test, y_train, y_test = get_human_dataset()
gb_clf = GradientBoostingClassifier(random_state = 0)
params = {
    'n_estimators' : [100, 500],
    'learning_rate' : [0.05, 0.1]                                                                                   #line 13
}
grid_cv = GridSearchCV(gb_clf, param_grid = params, cv = 2, verbose = 1)                                            #line 14
grid_cv.fit(X_train, y_train)
gv_pred = grid_cv.best_estimator_.predict(X_test)
gb_accuracy = accuracy_score(y_test, gb_pred)
print('GBM 정확도 : {0:.4f}'.format(gb_accuracy))
```

<img src="https://user-images.githubusercontent.com/97590480/155148945-bafb881a-ed50-4d18-9a72-e5b5d316f878.png">


1. [line 13]에서 `learning_rate`에서 분류기에 대한 가중치 하이퍼 파라미터를 설정해준다.
2. [line 14]에서 `verbose = 1`은 시간이 지남에 따라 로그를 찍어주는 역할을 한다.