# TIL(Today I Learned)

___

> Fab/24th2022_Multi campus_유선종 Day44

## 규제가 있을때의 회귀
어제는 어떠한 규제 없이 실시된 선형회귀에 대해서 배웠다. 이번에는 과대적합 등을 방지하기 위해 규제를 적용하는 선형회귀에 대해서 알아보자.

### 1. 경사하강법(Gradient descent)
경사하강법(Gradient descent)이란 최솟값을 점진적(Gredient)으로 구하는 방법을 말한다. 우리는 중고등학교때 2차 함수의 그래프를 그리고 최솟값을 구하는 방법을 수도없이 풀어봤다. 경사하강법도 단지 2차 함수의 최솟값을 구하는 것과 비슷하니 어렵게 생각하지 말자.

<img src="https://user-images.githubusercontent.com/97590480/155435413-37c62815-3587-46c3-bd00-b52089916417.png">

1. 이 그림은 경사하강법의 본질을 잘 설명하고 있다. 시작점이 어디든 상관없이 2차 함수의 기울기를 0으로 만드는 지점을 찾으면 그 점이 경사하강법의 도착지점이다.
2. 그런데 왜 하필 최저점일까? 그 이유는 저 2차 함수가 손실함수(cost function)이기 때문이다.
   1. 손실함수의 정확한 의미는 MSE이다. Day43에서 MSE가 크면 추정이 힘들고 MSE가 작으면 추정이 쉽다고 얘기했다.
   2. 즉, 우리는 MSE가 작으면 작을수록 추정하기가 쉬워지므로 비용이 적게 든다고 말할 수 있다.
   3. 여기서 손실함수의 y값은 비용(MSE)이고, x값은 회귀계수(coefficient)를 의미한다. 즉, MSE를 최소값으로 갖는 회귀게수를 찾는 것이 경사하강법의 핵심이다.
3. 식으로 나타내면 다음과 같다.

<img src="https://user-images.githubusercontent.com/97590480/155436024-7a530cc1-71fc-4b5c-83d0-840127afa56c.png">

- 여기서의 식은 코드로 나타낸 식이다. 즉, 오른쪽의 식이 x에 담기고 이를 반복하여 x가 더이상 변하지 않을때까지 반복한다.
- 오른쪽 식에서 알파(a)는 learning rate라 한다. 이 러닝레이트는 경사하강법의 속도를 결정하는 하이퍼 파라미터이다.
  1. 예를들어, learning rate가 10이라면 원래 기울기보다 10배가 반영되므로 기울기가 더 빨리 줄어들것이다.
  2. 반면에, learning rate가 0.1이라면 원래 기울기보다 0.1배가 반영되므로 기울기가 더 느리게 줄어들것이다.
  3. 그러므로 적절히으로 반영하는게 좋은데, 만약 기울기값이 크다면 최저점을 찾다가 최저점을 지나치는 경우가 발생하므로 learning rate를 작게 설정해준다.
  4. 반면에 기울기값이 작다면 최저점을 잘 찾기는 하지만 반영하는 속도가 너무 느리다는 단점이 발생한다. 이럴 경우에는 learning rate를 크게 설정해준다.
- 이러한 경사하강법은 최저점을 찾으면 더이상 움직이지 않게 된다. 이는 장점이자 단점인데, 만약 경사하강법으로 찾은 지점이 최저점이라면 베스트이다. 하지만 함수가 2차를 넘어 고차원의 함수라면 최저점이 여러 지점에서 발생하게 된다. 이럴 경우 지역(local)의 최저점이 전체(global) 최저점이라고 말할 수 없다. 하지만 이를 보완해서 머신러닝에서 가장 많이 쓰이는 방법이다.
___
### 2. 규제 회귀함수(Regulation Regression)
- 규제 회귀함수는 위의 손실함수를 반영하여 규제를 가하는 함수를 의미한다. 이전의 선형회귀에서 MSE를 구하기는 하지만 그것이 회귀계수를 결정하는 요소는 아니였다. 그러나 이번에는 MSE가 회귀계수를 결정하는데 간섭하게 되어 회귀계수가 적절히 조정된다.
- 규제 회귀함수에는 릿지(Ridge) 함수, 라쏘(Lasso) 함수, 엘라스틱(Elastic) 함수가 있다.

#### 1. 릿지(Ridge) 함수
릿지 함수는 손실함수에 규제를 부여하는 함수인데, 여기서 규제 방식을 L2 규제(Penalty)라고 한다. 식으로 표현하면 다음과 같다.

<img src="https://user-images.githubusercontent.com/97590480/155440144-03f23250-ee52-4ebe-8cc2-9298bb9f6e33.png">

1. 위의 이미지에서 손실함수(J)는 MSE와 규제(panelty)로 이루어져 있는데, 여기서 릿지 함수의 규제는 L2-norm이라고 부른다.
2. 우리의 목표는 손실함수를 최소로 만드는 회귀계수(W)를 구하는 것이 목표이다. 이를 구하기 위해서는 손실함수를 w로 미분해주면 된다.
___

<img src="https://user-images.githubusercontent.com/97590480/155441345-1cf3fccd-8138-4192-b8c8-ada191e074a9.png">

3. 위의 이미지처럼 1차 함수에 대한 손실함수를 미분하면 람다가 분모로 들어가는 것을 볼수 있다. 이처럼 다중선형회귀를 실시할 경우 람다의 크기에 따라 회귀계수가 바뀌게 되는데, 람다가 커지면 회귀계수는 감소하고 람다가 작아지면 회귀계수는 커진다.
> argmin은 argument minimize의 약자로 오른쪽의 식을 최소로 만드는 값을 함수값으로 갖는다는 의미이다.
___
1. 이를 Alternative Fomulation 형태로 표현하면 다음과 같다.

<img src="https://user-images.githubusercontent.com/97590480/155441714-a552602a-7712-4cb5-8db6-8e07a4ed9e0d.png">

5. 위에서는 손실함수를 미분한 값이 0이 되는 값을 찾는 것이 목표였다. 그러나 이번에는 subect to를 추가해서 L2-norm과의 미분과 MSE의 미분값이 같아지는 지점에서 회귀계수를 구하는 방식으로 변한 것이다.
6. 사실 2차함수의 최솟값은 미분한 값이 0이 되는 값이 아니라 2차함수의 y 값과 y = 0 인 직선과 만나는 지점을 표시한 것이다. 그런데 알고보니 이 지점의 미분값이 0인 것을 발견했고, 그래서 우리는 최솟값의 미분값이 0이 되는 성질을 이용해서 손실함수를 구한 것이다.
7. Alternative Fomulation은 원래의 의미인 두 함수의 만나는 지점을 이용해서 최솟값을 구하는 방식이다. 두 함수의 만나는 지점은 미분했을때 그 값이 같아지는 지점에서 만나게 된다. 따라서, L2-norm이라는 원과 MSE가 만나는 지점에서 회귀계수가 결정된다.
8. 위의 그림에서 원점에 근접한 원이 L2-norm이다. 반면에 오른쪽 원들은 MSE를 의미한다.
   1. 왼쪽의 그래프는 2차원 평면에 표현한 그래프이다. 여기서 x축과 y축은 두 회귀계수(w1, w2)를 의미한다.
   2. 오른쪽 원들의 집합을 MSE라고 했는데, 이는 오른쪽의 3차원그림을 2차원으로 표현하려고 원들의 집합으로 표현한 것이다.
   3. 원들의 집합을 다른말로 등고선이라 부르는데, 이 등고선은 지리 시간에 공부했던 등고선과 동일하다.
   4. 즉, 3차원 그림에서 동일한 z값을 갖는 지점을 이은 그래프가 왼쪽의 MSE 그래프인 것이다.
___
#### 2. 릿지 실습
이론적인 설명은 얼추 끝났고 이제부터는 코딩을 통해서 접근해보자.

```python
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib import rc
from scipy import stats
from sklearn.datasets import load_boston
%matplotlib inline

boston = load_boston()
bostonDF = pd.DataFrame(boston.data, columns = boston.feature_names)
```
> 여기서의 코드는 Day43에서 입력한 보스턴 집값의 연장선이다. 
```python
from sklearn.model_selection import cross_val_score                                                         #line 1

neg_mse_scores = cross_val_score(lr, X_data, y_target, scoring = "neg_mean_squared_error", cv = 5)          #line 2
rmse_scores = np.sqrt((-1) * neg_mse_scores)                                                                #line 3
avg_rmse = np.mean(rmse_scores)                                                                             #linr 4

print('5 folds의 개별 Negative MSE scores : ', np.round(neg_mse_scores, 2))
print('5 folds의 개별 RMSE scores : ', np.round(rmse_scores, 2))
print('5 folds의 평균 RMSE : {0:.3f}'.format(avg_rmse))
```
> 위의 코드는 규제를 하지 않았을 경우의 코드이다. 규제를 하지 않은 회귀는 Day43과 동일한데 cross_val_score를 사용해서 표현하고 싶어서 가져왔다.
1. [line 1]에서 교차검증을 위한 `cross_val_score` 클래스를 가져온다.
2. [line 2]에서 `scoring = "neg_mean_squared_erroe"` 속성을 이용하여 (-1) x MSE 로 평가를 한다. 그룹은 5그룹으로 나눴다.
    > 여기서 왜 그냥 MSE를 안쓰고 (-1) X MSE를 사용하냐면 표현상 헷갈릴수가 있기 때문이다. 우리가 그동안 사용하던 'accuracy'방식은 높게 나올수록 좋은 값인데 MSE는 높을수록 안 좋은 값이다. 따라서 곱하기 마이너스를 해줌으로써 관계를 accuracy와 동일하게 맞춰주기 위함이다.
3. [line 3]에서 마이너스값을 곱해줌으로써 MSE로 만들고 루트값을 취해줌으로써 RMSE값을 구한다.
4. [line 4]에서 평균값을 구해서 MRSE 값을 구한다.

___

이번에는 릿지 함수를 이용해서 RMSE를 구해보자
```python
alphas = [0.07, 0.1, 0.5, 1, 3]                                                                             #line 5

for alpha in alphas:
    ridge = Ridge(alpha = alpha)                                                                            #line 6
    neg_mse_scores = cross_val_score(ridge, X_data, y_target, scoring = "neg_mean_squared_error", cv = 5)
    avg_rmse = np.mean(np.sqrt((-1) * neg_mse_scores))
    print('alpha {0}일 때, 5 folds의 평균 RMSE : {1:.3f}'.format(alpha, avg_rmse))
```
1. [line 5]에서 L2 규제에 대한 하이퍼 파라미터인 람다값을 다양하게 돌려보기 위해 리스트 안에 여러 값들을 넣어서 돌려본다.
2. [line 6]에서 `Ridge(alpha = alpha)`함수를 이용해서 하이퍼 파라미터를 지정해준 릿지함수를 설정하고 RMSE를 구해본다. 결과는 다음과 같다.

<img src="https://user-images.githubusercontent.com/97590480/155444060-13283f62-9e5b-45e5-a0ed-be222347cb72.png">

alpha의 값이 커질수록 MSE가 작아지는 것을 볼 수 있다.
___
```python
coeff_df = pd.DataFrame()                                                                                   #line 7
for alpha in (alphas):
    ridge = Ridge(alpha = alpha)
    ridge.fit(X_data, y_target)
    coeff = pd.Series(data = ridge.coef_, index = X_data.columns)                                           #line 8
    colname = 'alpha : ' + str(alpha)
    coeff_df[colname] = coeff                                                                               #line 9

ridge_alphas = [0.07, 0.1, 0.5, 1, 3]
sort_column = 'alpha : ' + str(ridge_alphas[0])
coeff_df.sort_values(by = sort_column, ascending = False)                                                   #line 10
```
1. [line 7]에서 coeff_df 에 데이터프레임을 넣어두고 회귀계수를 넣을 공간으로 사용한다.
2. [line 8]에서 위에서 추정한 릿지 함수를 이용해 `ridge.coef_` 매서드를 입력하면 회귀계수를 계산해서 출력해준다. 이를 데이터프레임 형태로 넣어준다.
3. [line 9]에서 하이퍼 파라미터에 따른 회귀계수들을 잘 모아서 하나의 데이터프레임 형태로 담아준다.
4. [line 10]에서 위에서 모아둔 회귀계수 데이터프레임을 하이퍼 파라미터에 따라 정렬해주고 결과를 보자.

<img src="https://user-images.githubusercontent.com/97590480/155444979-7410dde7-7765-4367-bb14-467c7f69d106.png">

1. 표를 보면 대체로 값들이 alpha값이 증가함에 따라 줄어드는 회귀계수도 있는 반면에 증가하는 값들도 몇개 존재한다.
2. 이는 람다값이 증가함에 따라 과대적합한 회귀계수의 비중을 줄여주고 상대적으로 반영이 덜되던 회귀계수들의 값들이 증가하게 되는 것이다.
3. 즉, 일반적인 선형회귀를 했을때 일산화탄소가 가장 영향력이 높은 변수라고 추정했지만 람다값이 커짐에 따라 그 값이 줄어드는 것을 보면서 과대추정된 결과라는 것을 알 수 있다.