# TIL(Today I Learned)

___

> Fab/23th/2022_Multi campus_유선종 Day43

## 회귀모형
지도 학습중에 지금까지는 분류 모형에 대해서 배웠다. 그러나 여러 모델 중에서 통계적 모형을 빼먹을수는 없다. 지도학습중에서 통계적 모델을 담당하는 회귀 모형에 대해서 알아보겠다.

### 1. MSE
- 회귀 모델의 목표는 선형 관계를 도출하는 것이다.
- 예를 들어, 나이에 따른 소득의 관계가 `y = 10x + 1000`이라고 하면 x는 나이, y는 소득을 의미한다.
- 만약, 이러한 관계식을 구할수만 있다면 우리는 나중의 소득에 대해 예측하고 그 예측값이 실제로 맞아떨어지는 결과를 볼 수 있을 것이다.
- 그러나 우리는 이러한 관계식을 모른다. 오직 신만이 안다.
- 따라서 우리는 신만이 알고 있는 이 관계식을 관측값을 통해서 추정해보고자 한다.
- 이때, 관측값과 추정된 관계식과의 차이를 MSE라고 하고 머신러닝에서 성능을 평가하는 지표로 사용된다.
- 예를들어, 위의 관계식을 추정해냈다고 가정하자. 그런데 관측값은 x =1 일때, y = 1030이라고 하자. 그렇다면 실제 관계식의 결과값인 1010과 20이 차이가 난다. 이 20을 거리로 표현하기 위해 제곱을 해주고 제곱한 값들을 더해서 평균한 값이 MSE가 된다.

### 2. 보스턴 집값 요인 실습
이번에는 실습을 통해 알아보자. 보스턴의 집값을 결정하는 다양한 요인들을 입력변수로, 집값을 목표변수로 설정하고 분석한다.
```python
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib import rc
from scipy import stats
from sklearn.datasets import load_boston
%matplotlib inline

rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False

boston = load_boston()
bostonDF = pd.DataFrame(boston.data, columns = boston.feature_names)

fig, axs = plt.subplots(figsize=(16,12), ncols = 4, nrows = 2)
lm_features = ['RM', 'ZN', 'INDUS', 'NOX', 'AGE', 'PTRATIO', 'LSTAT', 'RAD']
lm_label = ['방 개수','25,000평방피트를 초과하는 지역 비율','비상업지역 넓이 비율','일산화탄소 농도',
              '1940년 이전에 지어진 주택 비율', '교사와 학생수 비율', '하위 계층의 비율', '고속도로 접근 용이도']
i = 0
for feature, title in zip(lm_features, lm_label):
    row = int(i/4)
    col = i%4
    i += 1
    sns.regplot(x = feature, y = 'PRICE', data=bostonDF, ax = axs[row][col]).set(title = title)
```

<img src="https://user-images.githubusercontent.com/97590480/155334155-c37cecaa-fb5f-473e-a5bb-cd7359bf9269.png">

위의 그림을 보면 직선이 그어져 있고 그 주변으로 여러 점들이 찍혀있는 것을 볼 수 있다. 직선을 회귀선이라 하고 회귀선을 기준으로 점들이 넓게 퍼져있으면 MSE값이 크고 추정하는데 어려움이 크다. 반면에, 회귀선에 점들이 모여있다면 관계식을 추정하는데 신뢰성있게 추정이 잘 된다고 볼 수 있다.

### 3. 회귀계수값 도출
이번에는 `y = 10x 1000` 에서 10을 도출해보고자 한다. 우리는 이 10을 기울기값이라 부르는데, 이 기울기값을 추정을 통해서 구한 값을 회귀계수(coefficient)라 부른다.

```python
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

y_target = bostonDF['PRICE']
X_data = bostonDF.drop(['PRICE'], axis = 1, inplace = False)
X_train, X_test, y_train, y_test = train_test_split(X_data, y_target, test_size = 0.3, random_state = 156)

lr = LinearRegression()                                                                                     #line 1
lr.fit(X_train, y_train)
y_preds = lr.predict(X_test)                                                                                
mse = mean_squared_error(y_test, y_preds)                                                                   #line 2
rmse = np.sqrt(mse)                                                                                         #line 3

print('MSE : {0:.3f}, RMSE : {1:.3f}'.format(mse, rmse))
print('Variance score : {0:.3f}'.format(r2_score(y_test, y_preds)))
print('절편 값 : ', lr.intercept_)
print('회귀 계수값 : ', np.round(lr.coef_, 1))
```
1. [line 1]에서 `LinearRegression()` 클래스를 불러와 이전에 우리가 머신러닝에서 하던 방식과 동일하게 fit하고 predict을 해주면 끝난다.
2. [line 2]에서 `mean_squared_error`를 통해서 MSE를 구한다.
3. [line 3]에서 RMSE를 구하는데, 우리는 회귀선과 점의 사이의 거리에 제곱을 한 것을 MSE라고 불렀다. 즉, 진짜 거리를 측정하기 위해서는 MSE에 루트를 한 RMSE를 할 경우에 실질적인 거리 표현으로 나타낼 수 있다.
4. 밑의 결과를 보면 회귀계수 중에서 `-19.8`이 나온 일산화탄소 농도가 가장 기울기의 절대값이 높게 나왔다. 이는 가장 영향력이 큰 변수라는 의미인데 우리의 상식상 일산화탄소가 보스턴 가격을 결정하는 가장 큰 요인이라는 것에는 동의하기 어렵다.
5. 이럴때 우리는 신뢰도를 봐야하는데, 여기서부터는 더 통계적인 내용이기 때문에 신뢰도를 보지는 않는다.
6. 하지만 이런식의 편향(bias)를 보정해줄 무엇인가가 필요한데, 이때 필요한 것이 경사하강법, 비용함수이다. 이것은 당장 하기에 애매한 부분이 많아서 내일 한번에 다루도록 한다.

<img src="https://user-images.githubusercontent.com/97590480/155336096-9773518e-0188-4bd7-9b2e-39dbc8b55e3d.png">