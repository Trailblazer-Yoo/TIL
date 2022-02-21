# TIL(Today I Learned)

___

> Fab/21st/2022_Multi campus_유선종 Day41

## Graphviz
그래피즈는 머신러닝에서 시각화를 해주는 라이브러리다. 그래피즈를 깔때 오류가 매우 잘 나기 때문에 꼭꼭 밑의 코드를 그대로 복사해서 설치를 해주자.   
`brew install graphviz`   
`conda install --channel conda-forge pygraphviz`
> 무조건 홈브루로 그래피즈를 깔고 콘다에 파이그래피즈를 깔아야 한다. 물론 Mac m1 기준이다. ~~이것때문에 4시간 날려먹었다.~~

### 1. 의사결정나무 시각화

#### 1. 하이퍼 파라미터를 설정하지 않았을 때의 의사결정나무
```python
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import pandas as pd

iris = load_iris()

iris_data = iris.data

iris_label = iris.target

iris_df = pd.DataFrame(data=iris_data, columns=iris.feature_names)
iris_df['label'] = iris.target

X_train, X_test, y_train, y_test =  train_test_split(iris_data, iris_label, 
                                    test_size=0.2, random_state=11)

dt_clf = DecisionTreeClassifier(random_state=11)
dt_clf.fit(X_train, y_train)
pred = dt_clf.predict(X_test)
```
1. 위의 코드는 의사결정나무에서 입력했던 코드 그대로를 가져왔다. 좀더 자세히 알고 싶다면 Day35,36을 참고하자.
2. 이 상태에서 의사결정나무를 시각화하기 위한 코드는 다음과 같다.

```python
from sklearn.tree import export_graphviz                                                                #line 1
export_graphviz(dt_clf, out_file="tree.dot", class_names= iris.target_names, 
               feature_names=iris.feature_names, impurity=True, filled=True)                            #line 2

import graphviz
with open("tree.dot") as f:                                                                             #line 3
    dot_graph = f.read()                                                                                #line 4
graphviz.Source(dot_graph)                                                                              #line 5
```
1. [line 1]에서 `sklearn.tree`에서 `export_graphviz` 클래스를 불러온다. sklearn은 graphviz를 지원하기 때문에 가능하다.
2. [line 2]에서 내가 적용할 모델을 파일로 저장하는 명령어이다.
    - `export_graphviz`의 속성으로, 1. 내가 적용할 모델, 2. out_file = '만들 파일의 이름', class_names = '목표변수', feature_names = '입력변수', impurity는 불순도로 평가를 한다는 뜻이고, filled는 색깔을 넣는다는 의미이다.
3. [line 3]에서 `export_graphviz`에서 생성한 파일을 연다. 여기서 파일에는 모델로 학습한 데이터에 대한 정보가 담겨있다.
4. [line 4]에서 파일을 읽는다.
5. [line 5]에서 읽은 파일을 `graphviz.Source`를 이용해서 시각화한다.

<img src="https://user-images.githubusercontent.com/97590480/154965857-f02fbed0-3aff-4c10-9749-a64e44af1d0b.png">

> 밑에 의사결정나무의 노드가 더 있다. 캡쳐화면으로는 다 담지 못했다.

여기서 빨간색 박스를 보면 샘플 수가 1인 노드가 있다. 이처럼 min_samples_leaf 파라미터를 조정하지 않아서 겨우 1개의 샘플을 위해 노드가 나뉘어지면서 과적합된 모델을 만들어내는 것을 볼 수 있다.

#### 2. 하이퍼 파라미터를 설정했을 때의 의사결정나무
코드는 위와 동일하나 min_sample_leaf = 3으로 설정한 경우의 시각화이다.

```python
dt_clf = DecisionTreeClassifier(min_samples_leaf=10, random_state=11)

dt_clf.fit(X_train, y_train)

pred = dt_clf.predict(X_test)

from sklearn.tree import export_graphviz

x_train, x_test, y_train, y_test = train_test_split(iris_data, iris_label, test_size=0.2, random_state=11)
dt_clf.fit(x_train, y_train)

export_graphviz(dt_clf, out_file="tree.dot", class_names=iris.target_names, feature_names= iris.feature_names, 
                impurity=True, filled=True)

import graphviz

with open("tree.dot") as f:
    dot_graph = f.read()
graphviz.Source(dot_graph)
```

<img src="https://user-images.githubusercontent.com/97590480/154966282-9a5bf292-3c9f-4e28-8400-113be0cba845.png">

여기서 보면 최소 샘플 수를 3으로 조정해줌으로써 과적합을 조정할 수 있다는 것을 볼 수 있다. 이런 이유로 min_samples_leaf는 무조건 2 이상은 설정해줘야 한다.

#### 3. 산점도로 표현한 의사결정나무
위의 그림이 의사결정나무의 가장 대표적인 그림이지만 산점도로 의사결정나무를 표현할 수 있다.

```python
from sklearn.datasets import make_classification
import matplotlib.pyplot as plt
%matplotlib inline

plt.title('3 Class values with 2 Features Sample data creation')                                        #line 6

X_features, y_labels = make_classification(n_features = 2, n_redundant = 0, n_informative = 2,          #line 7
 n_classes = 3, n_clusters_per_class = 1, random_state = 0)

plt.scatter(X_features[:, 0], X_features[:, 1], marker = 'o', c = y_labels, s= 25,                      #line 8
 cmap = 'rainbow', edgecolor= 'k')
```

<img src="https://user-images.githubusercontent.com/97590480/154967092-b931db35-eff5-4927-84d5-541482201b4d.png">

1. [line 6]에서 산점도의 제목을 설정해준다.
2. [line 7]에서 `make_classification(n_features = 2, n_redundant = 0, n_informative = 2, n_classes = 3, n_clusters_per_class = 1, random_state = 0)`클래스를 이용해서 목표함수와 입력함수를 설정한다.
    1. n_samples은 표본 데이터의 수이다. 기본값은 100이다.
    2. n_features은 독립변수의 수이다. 기본값은 20이다.
    3. n_repeated는 독립변수 중에서 단순 반복된 성분 수이다.
    4. n_informative는 독립변수 중에서 종속변수와 상관관계가 있는 성분의 수이다.
    5. n_redundant는 독립변수 중에서 informative와 선형 조합으로 나타낼 수 있는 성분의 수이다.
         - 여기서 중요한 것은 n_features = n_informative + n_repeated + n_redundant + a 라는 것이다.
         - 예를 들어, 독립변수 수는 5개인데 n_informative가 6개라면 말이 안된다. n_features가 위의 4가지를 포함한다.
         - 만약에 n_features > n_informative + n_repeated + n_redundant라면 random한 a를 생성해서 넣는다.
         - 여기서 a는 쓸모없는 변수인데, 쓸모가 없기 때문에 n_redundant와 동일한 변수이다.
             1. redundant는 독립변수와 선형 조합으로 나타낼 수 있는 성분 수라고 했다.
             2. 선형 조합이라는 뜻은 없앨 수 있는 성분이라는 뜻이다. 예를 들어, `x + y = 2`와 `2x + 2y = 4`는 동일한 방정식이다. 앞의 방정식을 2배 한것이 뒤의 방정식이기 때문이다.
             3. 이처럼 어떤 실수로 곱하거나 빼거나 더했을 때, 동일하다면 이는 똑같은 방정식이고, 선형관계가 존재한다고 말한다.
             4. 위의 redundant도 또한 informative 성분의 하나이다. 즉, 종속변수와 연관관계가 없는 성분이라는 것을 나타내기 위해 redundant를 사용할 뿐이지 설정하지 않아도 알아서 a로 적절히 만들어준다.
    6. n_classes는 클래스의 수를 의미한다. 산점도에서 색깔이 클래스를 의미한다.
    7. n_clusters_per_class는 클래스당 클러스터 숫자를 의미한다. class * cluster <= 2* informative를 만족해야 한다.
3. [line 8]에서 산점도를 만든다.

___

```python
import numpy as np

def visualize_boundary(model, X, y):
    fig, ax = plt.subplots()
    
    ax.scatter(X[:, 0], X[:, 1], c = y, s = 25, cmap = 'rainbow', edgecolor = 'k', clim= (y.min(), y.max()), zorder = 3)
    ax.axis('tight')
    ax.axis('off')
    xlim_start, xlim_end = ax.get_xlim()
    ylim_start, ylim_end = ax.get_ylim()
    
    model.fit(X,y)
    xx, yy = np.meshgrid(np.linspace(xlim_start, xlim_end, num = 200), np.linspace(ylim_start, ylim_end, num = 200))
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
    
    n_classes = len(np.unique(y))
    contours = ax.contourf(xx, yy, Z, alpha = 0.3, levels = np.arange(n_classes + 1) - 0.5, cmap = 'rainbow', clim = (y.min(), y.max()),zorder = 1)
```
산점도에서 경계를 설정해주는 함수이다. 이것도 하나하나 설명해주고 싶지만 강사님이 오픈소스로 다운받으면 된다 하니 따로 설명하지는 않겠다. 궁금하면 하나하나 뜯어보자.

___
```python
from sklearn.tree import DecisionTreeClassifier

dt_clf = DecisionTreeClassifier().fit(X_features, y_labels)
visualize_boundary(dt_clf, X_features, y_labels)
```

<img src="https://user-images.githubusercontent.com/97590480/154974012-9b303958-dea1-4698-bb71-246a1f60aa29.png">

위의 이미지를 보면 빨간색 성분 하나 때문에 파란색 클래스에 빨간색 클래스가 침투하는 모습을 보이면서 경계선이 세밀하게 되어있는 것을 볼 수 있다. 이는 과적합이 발생해서 세세한 클러스터에도 경계선을 표시하는 것이다.

___
```python
dt_clf = DecisionTreeClassifier(min_samples_leaf = 6).fit(X_features, y_labels)
visualize_boundary(dt_clf, X_features, y_labels)
```

<img src="https://user-images.githubusercontent.com/97590480/154974268-189a7677-aec5-4a29-b01c-63faff9989a4.png">

여기서는 min_samples_leaf = 6으로 설정해줌으로써 클러스터링이 세밀하지 않게 되면서 클래스의 경계면이 잘 나뉘어지는 것을 볼 수 있다. 이렇게 적절한 하이퍼 파라미터 설정은 좋은 모델을 학습하는데 필수적인 요소이다.