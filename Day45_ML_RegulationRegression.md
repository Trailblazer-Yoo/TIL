# TIL(Today I Learned)

___

> Fab/25th/2022_Multi campus_유선종 Day45

## 규제가 있을때의 회귀 계속
어제는 릿지 함수에 대해 알아봤다. 릿지 함수는 MSE라는 손실함수에 회귀계수에 대한 제약을 부여하는 방식으로 손실함수를 구성하여 손실함수를 최소화하는 회귀계수를 가지는 함수이다. 라쏘 함수와 엘라스틱 함수도 손실함수에 제약을 부여하는데, 라쏘는 회귀계수의 절대값을, 엘라스틱은 릿지 함수와 라쏘 함수를 합친 함수이다.

### 1. 라쏘 회귀함수(Lasso Regression)
라쏘(Lasso) 함수는 회귀계수가 절대값이 된다고 말했다. 우선 식으로 살펴보자.

<img src="https://user-images.githubusercontent.com/97590480/155631359-9254cb23-41b4-4349-8eb8-188d4d0cac91.png">

1. 오른쪽에 제약을 보면 회귀계수가 절댓값으로 되어있는 것을 볼 수 있다. 거리를 표현하는 방법은 제곱과 절댓값이므로 릿지와 라쏘 둘다 거리를 이용해서 제약을 사용한 것이다. 이 제약을 L1-norm 이라고 한다.
2. 라쏘의 의미를 더 잘 파악하기 위해 Alternative Fomulation 형태로 살펴보면 다음과 같다.

<img src="https://user-images.githubusercontent.com/97590480/155629710-1ad282b4-1e3b-45f9-a2c8-bf82adf55b96.png">

3. 릿지 함수는 원 형태의 제약을 가지고 원과 접하는 지점에서 회귀계수가 결정됐다.
4. 라쏘 함수는 마름모꼴 형태의 제약을 가지고 이와 접하는 지점에서 회귀계수가 결정된다.
5. 그런데 라쏘 함수의 특징은 선형이기 때문에 x,y축에서 접하는 코너해가 발생할 가능성이 높다는 것이다. 코너해라는 것은 (x,y) = (1,0) or (0,1)처럼 두 변수중에 하나가 0이 되면서 x, y축에서 값을 가지는 것을 의미한다.
6. 그래서 릿지 함수는 필요없는 변수들이 점점 0에 가까워지는 반면에, 라쏘 함수는 변수들의 값이 0이 되어버린다.

### 2. 라쏘 회귀 실습
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
from sklearn.linear_model import Lasso

lasso_alphas = [0.07, 0.1, 0.5, 1, 3]

for alpha in lasso_alphas:
    model = Lasso(alpha = alpha)
    neg_mse_scores = cross_val_score(model, X_data, y_target, scoring = 'neg_mean_squared_error', cv = 5)
    avg_rmse = np.mean(np.sqrt((-1)*neg_mse_scores))
    print('alpha {0}일 때 5fold 세트의 평균 RMSE: {1:.3f}'.format(param, avg_rmse))
    model.fit(X_data, y_target)
    coeff = pd.Series(data = ridge.coef_, index = X_data.columns)                             
    colname = 'alpha : ' + str(alpha)
    coeff_df[colname] = coeff 
                
colname = 'alpha : ' + str(param)
coeff_df[colname] = coeff          
```

<img src="https://user-images.githubusercontent.com/97590480/155631009-6bc28f54-b3ab-44cf-b814-16be764e2f36.png">

1. 이미지를 보면 하이퍼 파라미터가 커질수록 회귀계수의 값이 0인 회귀계수가 많아진다. 즉, 적절한 하이퍼 파라미터를 설정해서 중요도가 낮은 변수들을 제거할 수 있다.

### 3. 엘라스틱 넷
엘라스틱 넷(Elastic Net)는 릿지 함수와 라쏘 함수를 더한 것이다. 식으로 표현하면 다음과 같다.

<img src="https://user-images.githubusercontent.com/97590480/155631407-0e61a174-3dd2-4736-957c-ab1691d35205.png">

1. 위의 식을 보면 L1-norm과 L2-norm이 동시에 존재한다. 그렇다면 릿지 회귀와 라쏘 함수의 특징을 동시에 가진 함수가 엘라스틱 넷이다.
2. 이번에는 Alternative Fomulation 형태로 살펴보자.

<img src="https://user-images.githubusercontent.com/97590480/155631680-e9d21e4e-5178-4fca-a23a-9ab828da4dd2.png">

3. 그림을 보면 릿지 함수와 라쏘 함수 사이에 있는 타원형의 원이 엘라스틱 넷이다.
4. 완벽한 원은 아니지만 그렇다고 완전한 직선은 아닌 완만한 곡선형태를 가진다.

### 4. 엘라스틱 넷 실습

```python
from sklearn.linear_model import Elastic

L2_alphas = [0.07, 0.1, 0.5, 1, 3]

for alpha in L2_alphas:
    model = ElasticNet(alpha = alpha, l1_ratio = 0.7)
    neg_mse_scores = cross_val_score(model, X_data, y_target, scoring = 'neg_mean_squared_error', cv = 5)
    avg_rmse = np.mean(np.sqrt((-1)*neg_mse_scores))
    print('alpha {0}일 때 5fold 세트의 평균 RMSE: {1:.3f}'.format(param, avg_rmse))
    model.fit(X_data, y_target)
    coeff = pd.Series(data = ridge.coef_, index = X_data.columns)                             
    colname = 'alpha : ' + str(alpha)
    coeff_df[colname] = coeff 
                
colname = 'alpha : ' + str(param)
coeff_df[colname] = coeff     
```

<img src="https://user-images.githubusercontent.com/97590480/155632092-bdcc4893-b0e1-4d24-b60e-23aa37b9d78e.png">

1. 위의 코드는 거의 똑같지만 엘라스틱 넷은 `alpha, l1_ratio` 두개의 하이퍼 파라미터를 설정해준다. L1-norm은 우리가 임의로 정하고 L2는 리스트로 최적을 찾아본다.
2. 이미지를 보면 처음에는 0에 가깝게 줄어들다가 어떤 회귀변수는 아예 0으로 변하는 것을 볼 수 있다. 이처럼 릿지와 라쏘의 특징을 동시에 지니고 있기 때문에 엘라스틱 넷을 많이 사용한다.