# TIL(Today I Learned)

___

> Fab/20th/2022_Multi campus_유선종 Day40

## titanic 실습 계속
어제 성능 평가만 남겨두고 교차 검증까지 마무리했다. 그렇다면 이번에는 성능을 평가하는 여러 지표들에 대해 이론적으로 공부하고 구해보자.

### 1. 성능평가 지표
- 성능평가 지표는 회귀분석이냐 분류 분석이냐에 따라 다르게 평가한다.
- 우리는 지도학습(Supervised learning)을 회귀(Regression)와 분류(Classification)으로 나눈다고 했었다.
- 성능평가도 이에 따라 MSE와 정확도 등으로 나뉜다. 여기서 우리는 분류에 대한 평가 지표를 알아보자.

#### 1. Accuracy(정확도, 정분류율)
- Accuracy는 우리가 이때까지 지겹도록 구한 값이다. 이전에서 Accuracy를 구하는 방법은 훈련용 데이터로 모델을 만들고 만든 모델에 테스트 데이터를 넣어서 결과를 도출한 후에 실제 테스트 데이터의 결과값과 모델을 넣어서 구한 결과값이 얼마나 일치하냐에 따라 Accuracy를 구했다.
- 이번에는 좀더 정확하게 알아보자.

<img src="https://user-images.githubusercontent.com/97590480/154831073-46dba3c0-ba25-4d76-86f8-4d3535ed49eb.png">

1. 위의 이미지는 confusion matrix(정오분류표)라고 부른다.
2. TP,FP,TN,FN으로 약어로 부르는데, 기준은 predicttion이다. 예를들어, TP는 Positive로 예측(predict)했는데 실제로도 Positive하더라(True)이고, FP는 Positive로 예측했는데 실제로는 그렇지 않고 Negative더라(False)를 의미한다.
3. 그중에서 앞에 T가 들어간 것들이 우리의 예측과 실제값이 일치하는 것들이다. 즉, 타이타닉 실습에서 TP는 1(생존)이라고 예측한 값이 실제로도 1이였고, 0(사망)이라고 예측한 값이 실제로도 0인 경우이다.
4. 즉, 정확도는 예측과 실제값이 일치한 정도를 의미하므로 `(TP + TN) / (TP + TN + FP + FN) = Accuracy` 이다.
___
<img src="https://user-images.githubusercontent.com/97590480/154831545-c5a43f47-2b80-4112-b783-d0b54ddf7450.png">

1. 간단한 예시를 보자. 위의 이미지에서 밑에 있는 모델 예측값(Predict)을 기준으로 예측값이 T(Positive)인데 평가 데이터에서 실제로 T인 경우를 우리는 TP라고 했고, 여기서는 3개가 존재한다.
2. 모델 예측값이 F(Negative)인데 평가 데이터를 보면 실제로는 T인 경우를 FN이라고 하고 여기서는 1개가 존재한다.
3. 이런 식으로 각각의 갯수를 구해서 정확도를 구하면 (3 + 3)/(3 + 3 + 3 + 1) = 0.6 의 정확도를 구할 수 있다.
___
하지만 중요한 것은 언제나 해석이다. 만약, 우리에게 중요한 값은 1(생존)인데 1의 값보다 0(사망)의 값이 월등히 많다면 정확도가 높다고 하더라도 우리가 원하는 유의미한 결과를 도출하기는 힘들다. 즉, 정확도는 모델의 성능 평가를 완벽하게 설명하기에는 부족한 면이 존재한다.

#### 2. 정밀도(Precision), 재현율(Recall)
정확도의 한계를 보완해주는 지표로 정밀도(Precision)과 재현율(Recall; 민감도)이 있다. 

<img src="https://user-images.githubusercontent.com/97590480/154831116-b5e7ce6c-ab9c-49b7-8eca-b08e420b34fb.png">

1. 정밀도(Precision)은 Positive라고 예측했는데 실제로는 Negative(1종 오류)인 경우를 포함한다.
2. 정밀도의 식은 `TP/(TP + FP) = Precision`이고 1에 가까울수록 1종 오류가 없는 것이므로 1에 가까울수록 좋은 지표라고 말할 수 있다.
3. 반면에, 재현율(Recall)은 Negative라고 예측했는데 실제로는 Positive(2종 오류)인 경우를 포함한다.
4. 재현율의 식은 `TP/(TP + FN) = Recall`이고 1에 가까울수록 2종 오류가 없는 것이므로 1에 가까울수록 좋은 지표라고 말할 수 있다.
5. 정밀도와 재현율은 내가 분석하는 대상이 어떤 특징을 가지고 있느냐에 따라 중요도가 달라진다.
   - 예를 들어, 타이타닉 실습에서 중요한 것은 1(생존)이다. 여기서 1을 Positive, 0을 Negative라고 해보자.
   - 모든 예측이 정확하면 좋겠지만, 실수가 발생할 수 있으므로 1종 오류와 2종 오류 중에서 어떤 실수를 더 줄일 것인가에 대한 문제에 직면한다.
   - 둘다 줄일 수 있으면 좋겠지만, 이론적으로 1종 오류와 2종 오류는 상충 관계(trade off)에 있기 때문에 동시에 줄이는 것은 불가능하다.
   - 만약, 0이라고 예측했는데 실제로는 1이라면 Thanks to God이다. 왜냐하면 죽은 줄 알았는데 살았기 때문에 그나마 다행인 상황이다.
   - 반면에, 1이라고 예측했는데 실제로는 0이라면 절망적이다. 내 가족이 살아있는 줄 알았는데 사실은 죽었다고 생각해보자.
   - 즉, 여기서는 1이라고 예측했는데 실제로는 0인 상황이 존재하지 않도록 정밀도의 값이 높아야 한다.
> 암기 방법은 정밀도는 Positive 예측이므로 p.p.p but.. 으로 암기하자.
___
#### 3. 타이타닉 성능평가
그렇다면 실제로 타이타닉에서 의사결정나무를 사용하여 평가한 정확도, 정밀도, 재현율을 보자.

```python
from sklearn.model_selection import GridSearchCV                                                                #line 1
from sklearn.metrics import precision_score, recall_score                                                       #line 2

parameters = {
    'max_depth' : [2,3,5,10], 'min_samples_split' : [2,3,5], 'min_samples_leaf' : [1,5,8]                       #line 3
    }
grid_dclf = GridSearchCV(dt_clf, param_grid = parameters, scoring = 'accuracy', cv = 5)                         #line 4
grid_dclf.fit(x_train, y_train)                                                                                 #line 5

print('GridSearchCV 최적 하이퍼 파라미터 : ', grid_dclf.best_params_)
print('GridSearchCV 최고 정확도 : {0:.4f}'.format(grid_dclf.best_score_))
best_dclf = grid_dclf.best_estimator_                                                                           #line 6

dpredictons = best_dclf.predict(x_test)                                                                         #line 7
accuracy = accuracy_score(y_test, dpredictions)                                                                 #line 8
precision = precision_score(y_test, dpredictions)                                                               #line 9
recall = recall_score(y_test, dpredictions)                                                                     #line 10
print('테스트 세트에서의 DecisionTreeClassifier 정확도 : {0:.4f}'.format(accuracy))
print('테스트 세트에서의 DecisionTreeClassifier 정밀도 : {0:.4f}'.format(precision))
print('테스트 세트에서의 DecisionTreeClassifier 재현율 : {0:.4f}'.format(recall))
```
1. [line 1]에서 하이퍼 파라미터를 평가하기 위해 `GridSearchCV`클래스를 불러온다.
2. [line 2]에서 정밀도와 재현율을 평가하기 위해 `precision_score, recall_score`을 불러온다.
3. [line 3]에서 임의의 하이퍼 파라미터를 선택해서 리스트에 넣어준다. 여기서 우리는 분석가의 경험이 필요하게 된다. 혹은 최적이 나올때까지 for문으로 다 넣어보면 된다.
4. [line 4]에서 `GridSearchCV('알고리즘', '하이퍼파라미터', '평가방법', '그룹수')`를 받아서 grid_dclf인스턴스에 넣어준다.
5. [line 5]에서 `fit`매서드를 이용해서 훈련용 데이터를 이용해 모델을 훈련시킨다.
6. [line 6]에서 가장 높은 정확도를 보이는 하이퍼 파라미터 셋으로 훈련시킨 의사결정나무 모델을 best_dclf에 담는다.
7. [line 7]에서 테스트용 데이터를 이용해서 예측을 실시한다.
8. [line 8]에서 모델을 이용해서 예측한 결과와 실제 데이터 결과와 얼마나 일치하는 지를 평가한다. 이는 정확도가 된다.
9. [line 9]에서 정밀도를 계산한다.
10. [line 10]에서 재현율을 계산한다. 결과는 다음과 같다.

<img src="https://user-images.githubusercontent.com/97590480/154832204-f7cb395c-8345-4d19-9992-efb3c5465b3b.png">

- 재현율보다 정밀도의 값이 높은 것을 봐서 어느정도 우리가 경계하는 1종 오류를 줄인 결과라고 볼 수 있다.